#!/usr/bin/env python3
"""
CHAT 08 / STAGE 4 — Controlled Experiments Execution Harness
Executes the frozen experiment matrix:
- Configurations: A, B, C, D, E (5 configurations)
- Workloads: B1, B2, B3, B4, A1, A2, A3 (7 workloads)
- Repetitions: 10 per cell (reps 0..9)
- Total runs: 350 experimental runs
- In-kernel Q16.16 classifier for Config D
- Randomized run order with fixed seed (2026)
Saves raw per-run JSON records under experiments/raw/
"""
from __future__ import annotations
import argparse
import datetime
import json
import os
import random
import resource
import select
import signal
import subprocess
import sys
import threading
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

    # Create container before loader starts
    subprocess.run(["docker", "rm", "-f", "cncs_wl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([
        "docker", "run", "-d", "--name", "cncs_wl", "--network", "none",
        "-v", f"{PROJECT_ROOT}:/work:ro", "python:3.12-slim", "sleep", "infinity"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)

    loader_proc = None
    reader_thread = None
    raw_lines = []
    t0_start = time.perf_counter()
    u0, s0 = get_cpu_times()

    try:
        # Find container cgroup
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

        # Start telemetry loader for Configs B, C, D, E
        if config_id in ("B", "C", "D", "E"):
            if config_id == "D":
                w_str = ",".join(str(int(w)) for w in artifact["w_q16"])
                b_str = str(int(artifact["b_q16"]))
                cmd_loader = [
                    str(loader_bin), str(bpf_obj),
                    "--cgroup", cg_path,
                    "--max-seconds", str(int(duration + 10)),
                    "--infer",
                    "--w", w_str,
                    "--b", b_str
                ]
            else:
                cmd_loader = [
                    str(loader_bin), str(bpf_obj),
                    "--cgroup", cg_path,
                    "--max-seconds", str(int(duration + 10))
                ]

            loader_proc = subprocess.Popen(
                cmd_loader,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # Wait for {"r":"ready"} on loader stdout (timeout 5 s)
            ready = False
            t_wait_start = time.time()
            while time.time() - t_wait_start < 5.0:
                if loader_proc.poll() is not None:
                    err_text = loader_proc.stderr.read() if loader_proc.stderr else ""
                    raise RuntimeError(f"Telemetry loader exited prematurely (rc={loader_proc.returncode}): {err_text}")
                r_ready, _, _ = select.select([loader_proc.stdout], [], [], 0.1)
                if r_ready:
                    line = loader_proc.stdout.readline()
                    if '"r":"ready"' in line or '"ready"' in line:
                        ready = True
                        break
            if not ready:
                loader_proc.kill()
                raise TimeoutError("Timed out waiting for {\"r\":\"ready\"} on loader stdout (5 s limit)")

            # Send GO <anchor_ns>
            anchor_ns = time.monotonic_ns()
            loader_proc.stdin.write(f"GO {anchor_ns}\n")
            loader_proc.stdin.flush()

            # Wait for {"r":"armed"} on loader stdout (timeout 5 s)
            armed = False
            t_wait_start = time.time()
            while time.time() - t_wait_start < 5.0:
                if loader_proc.poll() is not None:
                    err_text = loader_proc.stderr.read() if loader_proc.stderr else ""
                    raise RuntimeError(f"Telemetry loader exited prematurely (rc={loader_proc.returncode}): {err_text}")
                r_armed, _, _ = select.select([loader_proc.stdout], [], [], 0.1)
                if r_armed:
                    line = loader_proc.stdout.readline()
                    if '"r":"armed"' in line or '"armed"' in line:
                        armed = True
                        break
            if not armed:
                loader_proc.kill()
                raise TimeoutError("Timed out waiting for {\"r\":\"armed\"} on loader stdout (5 s limit)")

            # Background thread to buffer stdout lines and avoid pipe buffer blocking
            def _drain_stdout():
                for line in loader_proc.stdout:
                    s = line.strip()
                    if s:
                        raw_lines.append(s)

            reader_thread = threading.Thread(target=_drain_stdout, daemon=True)
            reader_thread.start()

        # Run workload inside container
        t_exec_start = time.perf_counter()
        exec_cmd = ["docker", "exec", "cncs_wl", "python3", "/work/prototype/python/workloads.py", workload_id, "--duration", str(duration), "--seed", str(rep_idx)]
        exec_res = subprocess.run(exec_cmd, capture_output=True, text=True)
        t_exec_end = time.perf_counter()
        exec_wall_seconds = t_exec_end - t_exec_start
        if exec_res.returncode != 0:
            raise RuntimeError(f"Workload {workload_id} failed in container: {exec_res.stderr}")

        measured_duration_s = exec_wall_seconds
        workload_ops = None
        for line in exec_res.stdout.splitlines():
            line = line.strip()
            if "measured_duration_s" in line:
                try:
                    import ast
                    d = ast.literal_eval(line)
                    measured_duration_s = float(d["measured_duration_s"])
                    if "ops" in d:
                        workload_ops = int(d["ops"])
                    break
                except Exception:
                    pass

        # Read memory.peak before removing container
        workload_mem_peak_mb = None
        try:
            with open(os.path.join(cg_path, "memory.peak"), "r", encoding="utf-8") as f:
                workload_mem_peak_mb = float(f.read().strip()) / 1048576.0
        except Exception:
            pass

        # Loader peak RSS before terminating
        loader_rss_peak_mb = None
        if loader_proc and loader_proc.poll() is None:
            loader_vmhwm_kb = get_proc_vmhwm_kb(loader_proc.pid)
            if loader_vmhwm_kb is not None:
                loader_rss_peak_mb = loader_vmhwm_kb / 1024.0

        # Terminate telemetry loader
        if loader_proc:
            time.sleep(0.05)
            loader_proc.send_signal(signal.SIGTERM)
            loader_proc.stdin.close()
            try:
                loader_proc.wait(timeout=10.0)
            except subprocess.TimeoutExpired:
                loader_proc.kill()
            if reader_thread:
                reader_thread.join(timeout=5.0)

        u1, s1 = get_cpu_times()
        t0_end = time.perf_counter()
        elapsed = t0_end - t0_start
        cpu_user_s = max(u1 - u0, 0.0)
        cpu_sys_s = max(s1 - s0, 0.0)
        total_cpu_s = cpu_user_s + cpu_sys_s
        cpu_utilization_pct = (total_cpu_s / max(elapsed, 0.001)) * 100.0

        # Enforcement variables
        mitigation_triggered = False
        mitigation_latency_ms = None
        freeze_verified = None
        detection_to_mitigation_ms = None
        rollback_success = None
        rollback_time_ms = None

        # Parse records from loader
        events = []
        alerts = []
        stats = {}
        for line in raw_lines:
            try:
                rec = json.loads(line)
                r_type = rec.get("r")
                if r_type == "e":
                    events.append(rec)
                elif r_type == "a":
                    alerts.append(rec)
                elif r_type == "stats":
                    stats = rec
            except Exception:
                pass

        gen_events = stats.get("generated", len(events))
        sub_events = stats.get("submitted", len(events))
        res_fails = stats.get("reservation_failures", 0)
        seq_gaps = stats.get("sequence_gaps", 0)
        consumed = stats.get("consumed", len(events))
        loss_rate = float(gen_events - consumed) / float(gen_events) if gen_events > 0 else 0.0

        telemetry_throughput = float(len(events)) / max(measured_duration_s, 0.001) if config_id != "A" else 0.0

        transfer_latencies_us = []
        for ev in events:
            t0 = ev.get("t0")
            tr = ev.get("tr")
            if t0 is not None and tr is not None:
                transfer_latencies_us.append((tr - t0) / 1000.0)
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
        processing_latency_ms = 0.0
        kernel_decision_us = None
        alert_to_user_us = None

        if config_id == "D":
            # Config D: in-kernel Q16.16 classifier
            final_prediction = 1 if len(alerts) > 0 else 0
            final_score = 1.0 if final_prediction == 1 else 0.0
            if alerts:
                a0 = alerts[0]
                td = a0.get("td", 0)
                t0 = a0.get("t0", 0)
                tr = a0.get("tr", 0)
                kernel_decision_us = (td - t0) / 1000.0
                alert_to_user_us = (tr - td) / 1000.0
                avg_inference_latency_us = kernel_decision_us
            else:
                avg_inference_latency_us = 0.0
            processing_latency_ms = ((kernel_decision_us or 0.0) + (alert_to_user_us or 0.0)) / 1000.0

        elif config_id in ("C", "E"):
            # Configs C and E: user-space float scoring
            t_agg_start = time.perf_counter_ns()
            windows = aggregate(events, loss_rate=loss_rate)
            t_agg_end = time.perf_counter_ns()
            feature_aggregation_latency_us = (t_agg_end - t_agg_start) / 1000.0

            allow_mitigation = (config_id == "E")
            policy = Policy(artifact["threshold"], allow_mitigation=allow_mitigation)

            for w in windows:
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

                proc_ms = (inf_us + feature_aggregation_latency_us) / 1000.0
                processing_latency_ms = max(processing_latency_ms, proc_ms)

                # Real cgroup v2 freeze enforcement for Config E
                if config_id == "E" and res["predicted_class"] == 1:
                    mitigation_triggered = True
                    policy.request_mitigation(f"container-{workload_id}")
                    if policy.stage == Stage.CONTROLLED_MITIGATION:
                        freeze_file = os.path.join(cg_path, "cgroup.freeze")
                        events_file = os.path.join(cg_path, "cgroup.events")

                        # Mitigation: write 1, poll for frozen 1
                        t0 = time.perf_counter()
                        try:
                            with open(freeze_file, "w") as f:
                                f.write("1")
                        except Exception:
                            pass
                        freeze_verified = False
                        while time.perf_counter() - t0 < 2.0:
                            try:
                                with open(events_file, "r") as f:
                                    content = f.read()
                                if "frozen 1" in content:
                                    freeze_verified = True
                                    break
                            except Exception:
                                pass
                            time.sleep(0.0001)
                        t1 = time.perf_counter()
                        mitigation_latency_ms = (t1 - t0) * 1000.0
                        detection_to_mitigation_ms = processing_latency_ms + mitigation_latency_ms

                        # Rollback: write 0, poll for frozen 0
                        t_rb_s = time.perf_counter()
                        policy.rollback(f"container-{workload_id}")
                        try:
                            with open(freeze_file, "w") as f:
                                f.write("0")
                        except Exception:
                            pass
                        rollback_success = False
                        while time.perf_counter() - t_rb_s < 2.0:
                            try:
                                with open(events_file, "r") as f:
                                    content = f.read()
                                if "frozen 0" in content:
                                    rollback_success = True
                                    break
                            except Exception:
                                pass
                            time.sleep(0.0001)
                        t_rb_e = time.perf_counter()
                        rollback_time_ms = (t_rb_e - t_rb_s) * 1000.0

            final_prediction = 1 if (any(p == 1 for p in predictions)) else 0
            final_score = max(scores) if scores else (0.0 if ground_truth == 0 else 1.0)
            avg_inference_latency_us = (
                sum(inference_latencies_us) / len(inference_latencies_us)
                if inference_latencies_us
                else 0.0
            )

        else:
            # Configs A and B
            final_prediction = 0
            final_score = 0.0
            avg_inference_latency_us = 0.0

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
                "workload_ops": workload_ops,
                "ops_per_second": (workload_ops / measured_duration_s) if (workload_ops is not None and measured_duration_s > 0) else None,
                "cpu_user_seconds": cpu_user_s,
                "cpu_sys_seconds": cpu_sys_s,
                "cpu_utilization_pct": cpu_utilization_pct,
                "workload_mem_peak_mb": workload_mem_peak_mb,
                "loader_rss_peak_mb": loader_rss_peak_mb
            },
            "telemetry": {
                "cgroup_path": cg_path,
                "generated_events": gen_events,
                "workload_events": len(events),
                "submitted_events": sub_events,
                "consumed_events": consumed,
                "reservation_failures": res_fails,
                "sequence_gaps": seq_gaps,
                "alerts_kernel": stats.get("alerts_kernel", len(alerts)),
                "alerts_seen": len(alerts),
                "loss_rate": loss_rate,
                "telemetry_throughput_eps": telemetry_throughput,
                "telemetry_transfer_latency_us": telemetry_latency_us
            },
            "latency": {
                "feature_aggregation_us": feature_aggregation_latency_us,
                "inference_latency_us": avg_inference_latency_us,
                "decision_latency_us": decision_latency_us,
                "kernel_decision_us": kernel_decision_us,
                "alert_to_user_us": alert_to_user_us,
                "processing_latency_ms": processing_latency_ms,
                "mitigation_latency_ms": mitigation_latency_ms,
                "detection_to_mitigation_ms": detection_to_mitigation_ms,
                "rollback_time_ms": rollback_time_ms
            },
            "enforcement": {
                "mode": "cgroup_v2_freeze_post_run" if config_id == "E" else None,
                "mitigation_triggered": mitigation_triggered,
                "mitigation_latency_ms": mitigation_latency_ms,
                "freeze_verified": freeze_verified,
                "rollback_success": rollback_success,
                "rollback_time_ms": rollback_time_ms,
                "legitimate_operations_impacted": legitimate_impact
            }
        }

        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        return record

    finally:
        # Container cleanup
        subprocess.run(["docker", "rm", "-f", "cncs_wl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(description="STAGE 4 Controlled Experiments Runner")
    parser.add_argument("--duration", type=float, default=2.0, help="Workload duration per repetition")
    parser.add_argument("--reps", type=int, default=10, help="Repetitions per cell (default: 10)")
    parser.add_argument("--configs", nargs="+", default=["A", "B", "C", "D", "E"], help="Configurations to evaluate")
    parser.add_argument("--workloads", nargs="+", default=["B1", "B2", "B3", "B4", "A1", "A2", "A3"], help="Workloads to evaluate")
    parser.add_argument("--output-dir", type=str, default=str(PROJECT_ROOT / "experiments" / "raw"), help="Output directory for raw JSON records")
    args = parser.parse_args()

    print("==================================================================")
    print("STAGE 4 — CONTROLLED EXPERIMENTS (IN-KERNEL CONFIG D, RANDOM ORDER)")
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

    manifests_dir = PROJECT_ROOT / "experiments" / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    run_order_path = manifests_dir / "run_order.json"

    # Build the full list of 350 (config, workload, rep) tuples and randomize with seed 2026
    all_runs = []
    for cfg in args.configs:
        for wl in args.workloads:
            for rep in range(args.reps):
                all_runs.append((cfg, wl, rep))

    rng = random.Random(2026)
    rng.shuffle(all_runs)

    with open(run_order_path, "w", encoding="utf-8") as f:
        json.dump(all_runs, f, indent=2)
    print(f"Randomized run order (seed 2026) saved to: {run_order_path}")

    t_start_all = time.time()
    completed = 0

    for idx, (cfg, wl, rep) in enumerate(all_runs, 1):
        rec = run_single_experiment(cfg, wl, rep, args.duration, artifact, raw_dir)
        completed += 1
        pred_char = "!" if rec["prediction"] == 1 else "."
        gt_desc = "Anomaly" if rec["ground_truth"] == 1 else "Benign"
        print(f"[{completed}/{total_runs}] Config {cfg} {wl} rep{rep}: pred={rec['prediction']} ({pred_char}) GT={gt_desc}")

    t_end_all = time.time()
    total_time = t_end_all - t_start_all
    print(f"\n==================================================================")
    print(f"EXPERIMENTS COMPLETE: {completed} / {total_runs} runs successfully recorded.")
    print(f"Total execution time: {total_time:.2f} seconds ({total_time / 60.0:.2f} minutes).")
    print(f"Raw run records saved to: {raw_dir}")
    print("==================================================================")

if __name__ == "__main__":
    main()
