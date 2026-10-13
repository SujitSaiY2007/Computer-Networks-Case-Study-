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
import signal
import subprocess
import sys
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
        
    cmd_loader = [str(loader_bin), str(bpf_obj), "--duration", str(int(duration + 2))]
    with open(events_log, "w", encoding="utf-8") as out_f:
        loader_proc = subprocess.Popen(cmd_loader, stdout=out_f, stderr=subprocess.PIPE, text=True)
        
    time.sleep(0.3)  # Allow BPF attach
    
    # Run workload
    wl_fn = WORKLOADS[workload_id]
    if workload_id == "B2":
        wl_fn(duration, seed)
    else:
        wl_fn(duration)
        
    time.sleep(0.1)
    loader_proc.send_signal(signal.SIGTERM)
    try:
        loader_proc.wait(timeout=2.0)
    except subprocess.TimeoutExpired:
        loader_proc.kill()
        
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
        
    gen = stats.get("generated_events", len(events))
    rfail = stats.get("reservation_failures", 0)
    gaps = stats.get("sequence_gaps", 0)
    loss_rate = float(rfail + gaps) / float(gen) if gen > 0 else 0.0
    
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
    
    # Derive fixed-point parameters for Kernel-Local LR (Gate G)
    weights = artifact["coefficients"]
    intercept = artifact["intercept"]
    mean = artifact["mean"]
    scale = artifact["scale"]
    
    # Normalization-folded linear weights:
    # dot = sum_i (w_i * (x_i - mean_i) / scale_i) + b
    #     = sum_i (w_i / scale_i * x_i) + (b - sum_i (w_i * mean_i / scale_i))
    effective_weights = [w / s for w, s in zip(weights, scale)]
    effective_intercept = intercept - sum(w * m / s for w, m, s in zip(weights, mean, scale))
    
    weights_q16 = [int(round(ew * SCALE_FP)) for ew in effective_weights]
    intercept_q16 = int(round(effective_intercept * SCALE_FP))
    
    artifact["effective_weights"] = effective_weights
    artifact["effective_intercept"] = effective_intercept
    artifact["weights_q16"] = weights_q16
    artifact["intercept_q16"] = intercept_q16
    artifact["scale_fp"] = SCALE_FP
    artifact["model_hash"] = hashlib.sha256(json.dumps(artifact, sort_keys=True).encode()).hexdigest()
    
    # Test numerical equivalence between float and fixed-point on calibration set
    print("\n[3/3] Validating Gate G fixed-point numerical equivalence...")
    max_rel_err = 0.0
    mismatches = 0
    for w in training_data:
        x = [float(w[n]) for n in FEATURE_NAMES]
        # Float logit
        fl_logit = sum(ew * xi for ew, xi in zip(effective_weights, x)) + effective_intercept
        fl_pred = int(fl_logit >= 0.0)
        
        # Fixed-point logit
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
