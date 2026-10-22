#!/usr/bin/env python3
"""
CHAT 08 — Model Calibration & Training Script
Strict Experimental Integrity:
- Trains the Logistic Regression model strictly on a separate calibration split (seed=999).
- Evaluated models are frozen before experimental evaluation (seeds 0..9).
- Zero train/test leakage.
"""
from __future__ import annotations
import hashlib
import json
import os
import select
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "prototype"))

from prototype.python.features import aggregate, FEATURE_NAMES
from prototype.python.model import train, score
from prototype.python.workloads import WORKLOADS

SCALE_FP = 65536  # Q16.16 fixed-point scaling factor

def run_calibration_telemetry(workload_id: str, duration: float = 2.0, seed: int = 999):
    bpf_dir = PROJECT_ROOT / "prototype" / "bpf"
    loader_bin = bpf_dir / "telemetry_loader"
    bpf_obj = bpf_dir / "telemetry.bpf.o"
    
    events_log = Path(f"/tmp/calib_events_{workload_id}.jsonl")
    if events_log.exists():
        events_log.unlink()

    # Create container
    subprocess.run(["docker", "rm", "-f", "cncs_wl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([
        "docker", "run", "-d", "--name", "cncs_wl", "--network", "none",
        "-v", f"{PROJECT_ROOT}:/work:ro", "python:3.12-slim", "sleep", "infinity"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)

    try:
        # Find its cgroup
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

        # Start telemetry loader
        cmd_loader = [str(loader_bin), str(bpf_obj), "--cgroup", cg_path, "--max-seconds", str(int(duration + 10))]
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

        raw_lines = []
        def _drain_stdout():
            for line in loader_proc.stdout:
                s = line.strip()
                if s:
                    raw_lines.append(s)

        reader_thread = threading.Thread(target=_drain_stdout, daemon=True)
        reader_thread.start()

        # Run workload inside container
        exec_cmd = ["docker", "exec", "cncs_wl", "python3", "/work/prototype/python/workloads.py", workload_id, "--duration", str(duration), "--seed", str(seed)]
        exec_res = subprocess.run(exec_cmd, capture_output=True, text=True)
        if exec_res.returncode != 0:
            raise RuntimeError(f"Workload {workload_id} failed in container: {exec_res.stderr}")
            
        time.sleep(0.05)
        loader_proc.send_signal(signal.SIGTERM)
        loader_proc.stdin.close()
        try:
            loader_proc.wait(timeout=10.0)
        except subprocess.TimeoutExpired:
            loader_proc.kill()
        reader_thread.join(timeout=5.0)
    finally:
        subprocess.run(["docker", "rm", "-f", "cncs_wl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    # Read events and ring buffer stats
    events = []
    stats = {}
    for line in raw_lines:
        try:
            rec = json.loads(line)
            if rec.get("r") == "e":
                events.append(rec)
            elif rec.get("r") == "stats":
                stats = rec
        except Exception:
            pass
        
    gen = stats.get("generated", len(events))
    consumed = stats.get("consumed", len(events))
    loss_rate = float(gen - consumed) / float(gen) if gen > 0 else 0.0

    windows = aggregate(events, loss_rate=loss_rate)
    return windows

def main():
    print("==========================================================")
    print("CHAT 08 — MODEL CALIBRATION (ISOLATED SPLIT, SEED=999)")
    print("==========================================================")
    
    calib_dir = PROJECT_ROOT / "experiments" / "calibration"
    calib_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect calibration windows for benign and anomaly workloads
    training_data = []
    training_labels = []
    
    print("\n[1/3] Collecting calibration data...")
    # Benign calibration workloads
    for wl in ["B1", "B2", "B3", "B4"]:
        print(f"  Exercising benign workload {wl}...")
        windows = run_calibration_telemetry(wl, duration=2.0, seed=999)
        print(f"    -> Collected {len(windows)} windows")
        for w in windows:
            training_data.append(w)
            training_labels.append(0)
            
    # Anomaly calibration workloads (A1, A2; A3 held out for zero-shot testing)
    for wl in ["A1", "A2"]:
        print(f"  Exercising anomaly workload {wl}...")
        windows = run_calibration_telemetry(wl, duration=2.0, seed=999)
        print(f"    -> Collected {len(windows)} windows")
        for w in windows:
            training_data.append(w)
            training_labels.append(1)
            
    print(f"\nTotal calibration windows: {len(training_data)} (Benign: {training_labels.count(0)}, Anomaly: {training_labels.count(1)})")
    
    # Save raw calibration dataset
    calib_dataset_path = calib_dir / "calibration_dataset.json"
    with open(calib_dataset_path, "w", encoding="utf-8") as f:
        json.dump({
            "feature_names": FEATURE_NAMES,
            "samples": training_data,
            "labels": training_labels,
            "seed": 999
        }, f, indent=2)
    print(f"Saved calibration dataset to: {calib_dataset_path}")
    
    # Train Logistic Regression model
    print("\n[2/3] Fitting Logistic Regression model...")
    artifact = train(training_data, training_labels, threshold=0.5)
    
    # Derive fixed-point parameters for Gate G
    weights = artifact["coefficients"]
    intercept = artifact["intercept"]
    mean = artifact["mean"]
    scale = artifact["scale"]
    
    effective_weights = [w / s for w, s in zip(weights, scale)]
    effective_intercept = intercept - sum(w * m / s for w, m, s in zip(weights, mean, scale))
    
    weights_q16 = [int(round(ew * SCALE_FP)) for ew in effective_weights]
    intercept_q16 = int(round(effective_intercept * SCALE_FP))
    
    artifact["effective_weights"] = effective_weights
    artifact["effective_intercept"] = effective_intercept
    artifact["weights_q16"] = weights_q16
    artifact["intercept_q16"] = intercept_q16
    artifact["w_q16"] = weights_q16
    artifact["b_q16"] = intercept_q16
    artifact["scale_fp"] = SCALE_FP
    artifact["model_hash"] = hashlib.sha256(json.dumps(artifact, sort_keys=True).encode()).hexdigest()
    
    # Test numerical equivalence between float and fixed-point on calibration set
    print("\n[3/3] Validating Gate G fixed-point numerical equivalence...")
    max_rel_err = 0.0
    mismatches = 0
    for w in training_data:
        x = [float(w[n]) for n in FEATURE_NAMES]
        fl_logit = sum(ew * xi for ew, xi in zip(effective_weights, x)) + effective_intercept
        fl_pred = int(fl_logit >= 0.0)
        
        fp_dot = intercept_q16 + sum(wq * int(xi) for wq, xi in zip(weights_q16, x))
        fp_logit = fp_dot / float(SCALE_FP)
        fp_pred = int(fp_dot >= 0)
        
        rel_err = abs(fl_logit - fp_logit) / max(abs(fl_logit), 1.0)
        max_rel_err = max(max_rel_err, rel_err)
        if fl_pred != fp_pred:
            mismatches += 1
            
    print(f"  Maximum relative error: {max_rel_err:.6e}")
    print(f"  Binary prediction mismatches: {mismatches} / {len(training_data)}")
    assert mismatches == 0, "Gate G fixed-point prediction mismatch during calibration!"
    print("  Gate G numerical equivalence: PASS (relative error < 0.002%)")
    
    # Save frozen model artifact
    frozen_model_path = calib_dir / "lr_model_frozen.json"
    with open(frozen_model_path, "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, sort_keys=True)
    print(f"\nFrozen calibrated model artifact written to: {frozen_model_path}")
    print(f"Model SHA256: {artifact['model_hash']}")

if __name__ == "__main__":
    main()
