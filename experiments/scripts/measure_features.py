#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path("/home/sujitsaiy/cncs")
sys.path.insert(0, str(PROJECT_ROOT / "experiments" / "scripts"))
from calibrate_model import run_calibration_telemetry

MANIFEST_NAMES = {
    "B1": "Idle / Background Service",
    "B2": "Synthetic File Processing",
    "B3": "Process Churn",
    "B4": "Local Client-Server Traffic",
    "A1": "Drop and Execute Payload",
    "A2": "Abnormal File Access",
    "A3": "Abnormal Connection Burst"
}

def main():
    print("Measuring per-window features for all 7 workloads...")
    results = {}
    for wl in ["B1", "B2", "B3", "B4", "A1", "A2", "A3"]:
        print(f"Running {wl} ({MANIFEST_NAMES[wl]})...")
        windows = run_calibration_telemetry(wl, duration=2.0, seed=999)
        if not windows:
            print(f"  Warning: no windows for {wl}")
            results[wl] = {"exec": 0.0, "open": 0.0, "connect": 0.0, "unlink": 0.0, "windows": 0}
            continue
        n = len(windows)
        m_exec = sum(w["exec_count"] for w in windows) / n
        m_open = sum(w["open_count"] for w in windows) / n
        m_conn = sum(w["connect_count"] for w in windows) / n
        m_unlk = sum(w["unlink_count"] for w in windows) / n
        results[wl] = {
            "exec": m_exec,
            "open": m_open,
            "connect": m_conn,
            "unlink": m_unlk,
            "windows": n
        }
        print(f"  -> {n} windows: exec={m_exec:.1f}, open={m_open:.1f}, connect={m_conn:.1f}, unlink={m_unlk:.1f}")

    print("\n" + "="*80)
    print("PER-WORKLOAD MEAN PER-WINDOW FEATURE COUNTS")
    print("="*80)
    print(f"{'Workload ID':<12} {'Workload Name':<32} {'exec_count':<12} {'open_count':<12} {'connect_count':<14} {'unlink_count':<12}")
    print("-" * 88)
    for wl in ["B1", "B2", "B3", "B4", "A1", "A2", "A3"]:
        res = results[wl]
        print(f"{wl:<12} {MANIFEST_NAMES[wl]:<32} {res['exec']:<12.1f} {res['open']:<12.1f} {res['connect']:<14.1f} {res['unlink']:<12.1f}")

if __name__ == "__main__":
    main()
