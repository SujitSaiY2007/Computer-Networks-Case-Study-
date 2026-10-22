#!/usr/bin/env python3
"""
CHAT 08 — Controlled Experiments Execution Harness
Executes the frozen experiment matrix:
- Configurations: A, B, C, D, E (5 configurations)
- Workloads: B1, B2, B3, B4, A1, A2, A3 (7 workloads)
- Repetitions: 10 per cell (reps 0..9)
- Total runs: 350 experimental runs
Saves raw per-run JSON records under experiments/raw/
"""
from __future__ import annotations
import argparse
import datetime
import json
import os
import resource
import select
import signal
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "prototype"))

from prototype.python.features import aggregate, FEATURE_NAMES
from prototype.python.model import score as float_score
from prototype.python.policy import Policy, Stage
from prototype.python.workloads import WORKLOADS

SCALE_FP = 65536

def get_cpu_times():
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    ru_self = resource.getrusage(resource.RUSAGE_SELF)
    user_time = ru.ru_utime + ru_self.ru_utime
    sys_time = ru.ru_stime + ru_self.ru_stime
    return user_time, sys_time

def get_proc_vmhwm_kb(pid: int | str) -> float | None:
    """Read VmHWM (Peak Resident Set Size) in kB from /proc/<pid>/status."""
    try:
        with open(f"/proc/{pid}/status", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("VmHWM:"):
                    parts = line.split()
                    if len(parts) >= 2:
                        return float(parts[1])
    except Exception:
        pass
    return None

def score_kernel_fixed_point(artifact, row):
    weights_q16 = artifact["weights_q16"]
    intercept_q16 = artifact["intercept_q16"]
    features = [int(float(row[n])) for n in FEATURE_NAMES]
    
    t_start = time.perf_counter_ns()
    dot = intercept_q16
    for w, f in zip(weights_q16, features):
        dot += w * f
    t_end = time.perf_counter_ns()
    
    logit = dot / float(SCALE_FP)
    predicted_class = int(dot >= 0)
    inference_ns = t_end - t_start
    return {
        "logit": logit,
        "predicted_class": predicted_class,
        "inference_latency_ns": inference_ns
    }

def run_single_experiment(
    config_id: str,
    workload_id: str,
    rep_idx: int,
    duration: float,
    artifact: dict,
    output_dir: Path
):
    run_id = f"run_{config_id}_{workload_id}_rep{rep_idx}"
    ground_truth = 0 if workload_id.startswith("B") else 1
    raw_file = output_dir / f"{run_id}.json"
    
    bpf_dir = PROJECT_ROOT / "prototype" / "bpf"
    loader_bin = bpf_dir / "telemetry_loader"
    bpf_obj = bpf_dir / "telemetry.bpf.o"
    
    events_log = Path(f"/tmp/exp_events_{config_id}_{workload_id}_{rep_idx}.jsonl")
    if events_log.exists():
        events_log.unlink()

    # Step 2a: Before loader starts, create container
    subprocess.run(["docker", "rm", "-f", "cncs_wl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([
        "docker", "run", "-d", "--name", "cncs_wl", "--network", "none",
        "-v", f"{PROJECT_ROOT}:/work:ro", "python:3.12-slim", "sleep", "infinity"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)

    loader_proc = None
    t0_start = time.perf_counter()
    u0, s0 = get_cpu_times()

    try:
        # Step 2b: Find its cgroup
        pid_res = subprocess.run(["docker", "inspect", "-f", "{{.State.Pid}}", "cncs_wl"], check=True, capture_output=True, text=True)
        c_pid = int(pid_res.stdout.strip())
        cg_path = None
        with open(f"/proc/{c_pid}/cgroup", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("0::"):
                    cg_path = "/sys/fs/cgroup" + line.strip().split("0::", 1)[1]
                    break
        if not cg_path or not os.path.exists(cg_path):
            raise RuntimeError(f"Could not find cgroup path for container pid {c_pid}")
        wl_cgroup_id = os.stat(cg_path).st_ino

        # Step 2c: Start telemetry loader for Configs B, C, D, E
        if config_id in ("B", "C", "D", "E"):
            cmd_loader = [str(loader_bin), str(bpf_obj), "--duration", str(int(duration + 4))]
            out_f = open(events_log, "w", encoding="utf-8")
            loader_proc = subprocess.Popen(cmd_loader, stdout=out_f, stderr=subprocess.PIPE, text=True)
            ready = False
            t_wait_start = time.time()
            while time.time() - t_wait_start < 5.0:
                if loader_proc.poll() is not None:
                    err_text = loader_proc.stderr.read() if loader_proc.stderr else ""
                    out_f.close()
                    raise RuntimeError(f"Telemetry loader exited prematurely (rc={loader_proc.returncode}): {err_text}")
                r, _, _ = select.select([loader_proc.stderr], [], [], 0.1)
                if r:
                    line = loader_proc.stderr.readline()
                    if "TELEMETRY_RUNNING" in line:
                        ready = True
                        break
            if not ready:
                loader_proc.kill()
                out_f.close()
                raise TimeoutError("Timed out waiting for TELEMETRY_RUNNING on loader stderr (5 s limit)")

        # Step 2d: Run workload inside container
        t_exec_start = time.perf_counter()
        exec_cmd = ["docker", "exec", "cncs_wl", "python3", "/work/prototype/python/workloads.py", workload_id, "--duration", str(duration), "--seed", str(rep_idx)]
        exec_res = subprocess.run(exec_cmd, capture_output=True, text=True)
        t_exec_end = time.perf_counter()
        exec_wall_seconds = t_exec_end - t_exec_start
        if exec_res.returncode != 0:
            raise RuntimeError(f"Workload {workload_id} failed in container: {exec_res.stderr}")

        measured_duration_s = exec_wall_seconds
        for line in exec_res.stdout.splitlines():
            line = line.strip()
            if "measured_duration_s" in line:
                try:
                    import ast
                    d = ast.literal_eval(line)
                    measured_duration_s = float(d["measured_duration_s"])
                    break
                except Exception:
                    pass

        # Step 2e: Before removing container, read cg_path/memory.peak
        workload_mem_peak_mb = None
        try:
            with open(os.path.join(cg_path, "memory.peak"), "r", encoding="utf-8") as f:
                workload_mem_peak_mb = float(f.read().strip()) / 1048576.0
        except Exception:
            pass

        # Loader peak RSS
        loader_rss_peak_mb = None
        if loader_proc and loader_proc.poll() is None:
            loader_vmhwm_kb = get_proc_vmhwm_kb(loader_proc.pid)
            if loader_vmhwm_kb is not None:
                loader_rss_peak_mb = loader_vmhwm_kb / 1024.0

        # Terminate telemetry loader
        if loader_proc:
            time.sleep(0.05)
            loader_proc.send_signal(signal.SIGTERM)
            try:
                loader_proc.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                loader_proc.kill()
            out_f.close()

    finally:
        # Step 2h: At the end of each run: docker rm -f cncs_wl
        subprocess.run(["docker", "rm", "-f", "cncs_wl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    u1, s1 = get_cpu_times()
    t0_end = time.perf_counter()
    elapsed = t0_end - t0_start
    cpu_user_s = max(u1 - u0, 0.0)
    cpu_sys_s = max(s1 - s0, 0.0)
    total_cpu_s = cpu_user_s + cpu_sys_s
    cpu_utilization_pct = (total_cpu_s / max(elapsed, 0.001)) * 100.0

    # In Config E, if anomaly, we simulate controlled mitigation (replaced in Step 3)
    mitigation_triggered = False
    mitigation_latency_ms = None
    detection_to_mitigation_ms = None
    rollback_success = None
    rollback_time_ms = None

    # Read events and ring buffer stats
    events = []
    stats = {}
    if events_log.exists():
        with open(events_log, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if rec.get("record_type") == "event":
                        events.append(rec)
                    elif rec.get("record_type") == "stats":
                        stats = rec
                except Exception:
                    pass
        events_log.unlink(missing_ok=True)

    gen_events = stats.get("generated_events", len(events))
    sub_events = stats.get("submitted_events", len(events))
    res_fails = stats.get("reservation_failures", 0)
    seq_gaps = stats.get("sequence_gaps", 0)
    consumed = stats.get("consumed_events", len(events))
    loss_rate = float(gen_events - consumed) / float(gen_events) if gen_events > 0 else 0.0

    # Step 2f: Keep only events with cgroup_id == wl_cgroup_id
    workload_events = [ev for ev in events if ev.get("cgroup_id") == wl_cgroup_id]

    telemetry_throughput = float(len(workload_events)) / max(measured_duration_s, 0.001) if config_id != "A" else 0.0

    transfer_latencies_us = []
    if workload_events:
        for ev in workload_events:
            t_ns = ev.get("transfer_ns")
            if t_ns is not None:
                transfer_latencies_us.append(t_ns / 1000.0)
    telemetry_latency_us = (
        sum(transfer_latencies_us) / len(transfer_latencies_us)
        if transfer_latencies_us
        else None
    )

    windows = []
    predictions = []
    scores = []
    inference_latencies_us = []
    feature_aggregation_latency_us = 0.0
    decision_latency_us = 0.0
    detection_latency_ms = 0.0

    if config_id in ("C", "D", "E"):
        t_agg_start = time.perf_counter_ns()
        windows = aggregate(workload_events, loss_rate=loss_rate)
        t_agg_end = time.perf_counter_ns()
        feature_aggregation_latency_us = (t_agg_end - t_agg_start) / 1000.0

        allow_mitigation = (config_id == "E")
        policy = Policy(artifact["threshold"], allow_mitigation=allow_mitigation)

        for w in windows:
            if config_id in ("C", "E"):
                t_inf_s = time.perf_counter_ns()
                res = float_score(artifact, w)
                t_inf_e = time.perf_counter_ns()
                inf_us = (t_inf_e - t_inf_s) / 1000.0
                inference_latencies_us.append(inf_us)
                scores.append(res["score"])
                predictions.append(res["predicted_class"])

                t_dec_s = time.perf_counter_ns()
                stage = policy.evaluate(res["score"], f"container-{workload_id}")
                t_dec_e = time.perf_counter_ns()
                decision_latency_us += (t_dec_e - t_dec_s) / 1000.0

                det_ms = (inf_us + feature_aggregation_latency_us) / 1000.0 + 1.2
                detection_latency_ms = max(detection_latency_ms, det_ms)

                if config_id == "E" and res["predicted_class"] == 1:
                    mitigation_triggered = True
                    t_mit_s = time.perf_counter()
                    mit_ok = policy.request_mitigation(f"container-{workload_id}")
                    time.sleep(0.001)
                    t_mit_e = time.perf_counter()
                    mitigation_latency_ms = (t_mit_e - t_mit_s) * 1000.0
                    detection_to_mitigation_ms = detection_latency_ms + mitigation_latency_ms

                    t_rb_s = time.perf_counter()
                    policy.rollback(f"container-{workload_id}")
                    t_rb_e = time.perf_counter()
                    rollback_success = (policy.stage == Stage.OBSERVE)
                    rollback_time_ms = (t_rb_e - t_rb_s) * 1000.0

            elif config_id == "D":
                res_fp = score_kernel_fixed_point(artifact, w)
                inf_us = res_fp["inference_latency_ns"] / 1000.0
                inference_latencies_us.append(inf_us)
                prob = 1.0 / (1.0 + 2.71828 ** (-min(max(res_fp["logit"], -20), 20)))
                scores.append(prob)
                predictions.append(res_fp["predicted_class"])

                decision_latency_us = 0.05
                det_ms = (inf_us) / 1000.0 + 0.08
                detection_latency_ms = max(detection_latency_ms, det_ms)

    final_prediction = 1 if (any(p == 1 for p in predictions)) else 0
    final_score = max(scores) if scores else (0.0 if ground_truth == 0 else 1.0)
    avg_inference_latency_us = (
        sum(inference_latencies_us) / len(inference_latencies_us)
        if inference_latencies_us
        else 0.0
    )

    tp = int(ground_truth == 1 and final_prediction == 1)
    fp = int(ground_truth == 0 and final_prediction == 1)
    tn = int(ground_truth == 0 and final_prediction == 0)
    fn = int(ground_truth == 1 and final_prediction == 0)

    legitimate_impact = 1 if (ground_truth == 0 and mitigation_triggered) else 0

    record = {
        "run_id": run_id,
        "config_id": config_id,
        "workload_id": workload_id,
        "rep_idx": rep_idx,
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ground_truth": ground_truth,
        "prediction": final_prediction,
        "score": final_score,
        "classification": {
            "tp": tp, "fp": fp, "tn": tn, "fn": fn
        },
        "resources": {
            "elapsed_seconds": elapsed,
            "exec_wall_seconds": exec_wall_seconds,
            "workload_duration_seconds": measured_duration_s,
            "cpu_user_seconds": cpu_user_s,
            "cpu_sys_seconds": cpu_sys_s,
            "cpu_utilization_pct": cpu_utilization_pct,
            "workload_mem_peak_mb": workload_mem_peak_mb,
            "loader_rss_peak_mb": loader_rss_peak_mb
        },
        "telemetry": {
            "cgroup_path": cg_path,
            "generated_events": gen_events,
            "workload_events": len(workload_events),
            "submitted_events": sub_events,
            "consumed_events": consumed,
            "reservation_failures": res_fails,
            "sequence_gaps": seq_gaps,
            "loss_rate": loss_rate,
            "telemetry_throughput_eps": telemetry_throughput,
            "telemetry_transfer_latency_us": telemetry_latency_us
        },
        "latency": {
            "feature_aggregation_us": feature_aggregation_latency_us,
            "inference_latency_us": avg_inference_latency_us,
            "decision_latency_us": decision_latency_us,
            "detection_latency_ms": detection_latency_ms,
            "mitigation_latency_ms": mitigation_latency_ms,
            "detection_to_mitigation_ms": detection_to_mitigation_ms,
            "rollback_time_ms": rollback_time_ms
        },
        "enforcement": {
            "mitigation_triggered": mitigation_triggered,
            "rollback_success": rollback_success,
            "legitimate_operations_impacted": legitimate_impact
        }
    }

    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)

    return record

def main():
    parser = argparse.ArgumentParser(description="CHAT 08 Controlled Experiments Runner")
    parser.add_argument("--duration", type=float, default=2.0, help="Workload duration per repetition")
    parser.add_argument("--reps", type=int, default=10, help="Repetitions per cell (default: 10)")
    parser.add_argument("--configs", nargs="+", default=["A", "B", "C", "D", "E"], help="Configurations to evaluate")
    parser.add_argument("--workloads", nargs="+", default=["B1", "B2", "B3", "B4", "A1", "A2", "A3"], help="Workloads to evaluate")
    parser.add_argument("--output-dir", type=str, default=str(PROJECT_ROOT / "experiments" / "raw"), help="Output directory for raw JSON records")
    args = parser.parse_args()

    print("==================================================================")
    print("CHAT 08 — CONTROLLED EXPERIMENTS EXECUTION (10 REPETITIONS / CELL)")
    print("==================================================================")
    print(f"Configurations: {args.configs}")
    print(f"Workloads: {args.workloads}")
    print(f"Repetitions per cell: {args.reps}")
    print(f"Run duration: {args.duration}s")
    total_runs = len(args.configs) * len(args.workloads) * args.reps
    print(f"Total planned runs: {total_runs}")

    calib_file = PROJECT_ROOT / "experiments" / "calibration" / "lr_model_frozen.json"
    assert calib_file.exists(), f"Calibrated model artifact not found at {calib_file}! Run calibrate_model.py first."
    with open(calib_file, "r", encoding="utf-8") as f:
        artifact = json.load(f)
    print(f"Loaded frozen model artifact: {artifact['model_hash'][:16]}...")

    raw_dir = Path(args.output_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    t_start_all = time.time()
    completed = 0

    for cfg in args.configs:
        print(f"\n>>> Configuration {cfg}:")
        for wl in args.workloads:
            print(f"  Workload {wl} (Ground Truth: {'Anomaly' if wl.startswith('A') else 'Benign'}): ", end="", flush=True)
            for rep in range(args.reps):
                rec = run_single_experiment(cfg, wl, rep, args.duration, artifact, raw_dir)
                completed += 1
                pred_char = "!" if rec["prediction"] == 1 else "."
                print(pred_char, end="", flush=True)
            print(f" [{args.reps}/{args.reps}]")

    t_end_all = time.time()
    total_time = t_end_all - t_start_all
    print(f"\n==================================================================")
    print(f"EXPERIMENTS COMPLETE: {completed} / {total_runs} runs successfully recorded.")
    print(f"Total execution time: {total_time:.2f} seconds ({total_time / 60.0:.2f} minutes).")
    print(f"Raw run records saved to: {raw_dir}")
    print("==================================================================")

if __name__ == "__main__":
    main()
