import json
import glob
import statistics
import os
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path("/home/sujitsaiy/cncs")
RAW_DIR = PROJECT_ROOT / "experiments" / "raw"

MANIFEST_NAMES = {
    "B1": "Idle / Background Service",
    "B2": "Synthetic File Processing",
    "B3": "Process Churn",
    "B4": "Local Client-Server Traffic",
    "A1": "Drop and Execute Payload",
    "A2": "Abnormal File Access",
    "A3": "Abnormal Connection Burst"
}

CONFIG_NAMES = {
    "A": "Baseline (No Instrumentation)",
    "B": "eBPF Telemetry Only",
    "C": "eBPF + User-Space Logistic Regression",
    "D": "eBPF + Python Q16.16 Fixed-Point Logistic Regression",
    "E": "eBPF + ML + Staged Controlled Enforcement"
}

WORKLOADS = ["B1", "B2", "B3", "B4", "A1", "A2", "A3"]
CONFIGS = ["A", "B", "C", "D", "E"]

def main():
    files = sorted(glob.glob(str(RAW_DIR / "run_*.json")))
    print(f"Loaded {len(files)} raw files.")

    data = defaultdict(list)
    for f in files:
        with open(f) as fp:
            d = json.load(fp)
            data[(d["config_id"], d["workload_id"])].append(d)

    # 1. Ops per second and % change vs A per workload and config
    print("\n" + "="*80)
    print("THROUGHPUT (OPS/SEC) AND % CHANGE VS BASELINE A")
    print("="*80)
    
    baseline_ops = {}
    for w in WORKLOADS:
        runs_a = data[("A", w)]
        ops_a = [r["resources"].get("ops_per_second", 0.0) for r in runs_a if r["resources"].get("ops_per_second") is not None]
        baseline_ops[w] = statistics.mean(ops_a) if ops_a else 0.0

    print(f"{'Workload':<35} {'Config':<10} {'Mean Ops/Sec':<15} {'Std Ops/Sec':<15} {'% Change vs A':<15}")
    print("-" * 90)
    for w in WORKLOADS:
        w_name = f"{w}: {MANIFEST_NAMES[w]}"
        for c in CONFIGS:
            runs = data[(c, w)]
            ops = [r["resources"].get("ops_per_second", 0.0) for r in runs if r["resources"].get("ops_per_second") is not None]
            m_ops = statistics.mean(ops) if ops else 0.0
            s_ops = statistics.stdev(ops) if len(ops) > 1 else 0.0
            if w == "B1":
                pct_str = "N/A (idle)"
            elif baseline_ops[w] > 0:
                pct = ((m_ops - baseline_ops[w]) / baseline_ops[w]) * 100.0
                pct_str = f"{pct:+.2f}%"
            else:
                pct_str = "N/A"
            print(f"{w_name:<35} {c:<10} {m_ops:<15.2f} {s_ops:<15.2f} {pct_str:<15}")

    # 2. Predictions flagged as attack out of 10 for C, D, E
    print("\n" + "="*80)
    print("PREDICTIONS FLAGGED AS ATTACK OUT OF 10 (CONFIGS C, D, E)")
    print("="*80)
    print(f"{'Workload':<35} {'Config C':<12} {'Config D':<12} {'Config E':<12}")
    print("-" * 75)
    for w in WORKLOADS:
        w_name = f"{w}: {MANIFEST_NAMES[w]}"
        counts = {}
        for c in ["C", "D", "E"]:
            runs = data[(c, w)]
            attack_count = sum(1 for r in runs if r.get("prediction") == 1)
            counts[c] = f"{attack_count}/10"
        print(f"{w_name:<35} {counts['C']:<12} {counts['D']:<12} {counts['E']:<12}")

    # Precision, Recall, F1 for A1 and A2; FPR for benign; Recall for A3
    print("\n" + "="*80)
    print("DETECTION METRICS (CONFIGS C, D, E)")
    print("="*80)
    for c in ["C", "D", "E"]:
        print(f"\n--- Config {c} ---")
        # Benign FPR
        for bw in ["B1", "B2", "B3", "B4"]:
            runs = data[(c, bw)]
            fp = sum(1 for r in runs if r.get("prediction") == 1)
            tn = sum(1 for r in runs if r.get("prediction") == 0)
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
            print(f"  FPR {bw} ({MANIFEST_NAMES[bw]}): {fpr*100:.1f}% ({fp}/{len(runs)})")

        # A1 and A2 combined
        tp = 0
        fn = 0
        for aw in ["A1", "A2"]:
            runs = data[(c, aw)]
            tp += sum(1 for r in runs if r.get("prediction") == 1)
            fn += sum(1 for r in runs if r.get("prediction") == 0)
        
        # total FP across all benign
        total_fp = sum(sum(1 for r in data[(c, bw)] if r.get("prediction") == 1) for bw in ["B1", "B2", "B3", "B4"])
        prec = tp / (tp + total_fp) if (tp + total_fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        print(f"  A1 & A2 Precision: {prec*100:.2f}% ({tp}/{tp+total_fp})")
        print(f"  A1 & A2 Recall:    {rec*100:.2f}% ({tp}/{tp+fn})")
        print(f"  A1 & A2 F1-Score:  {f1:.4f}")

        # A3 Recall
        runs_a3 = data[(c, "A3")]
        a3_tp = sum(1 for r in runs_a3 if r.get("prediction") == 1)
        a3_rec = a3_tp / len(runs_a3) if runs_a3 else 0.0
        print(f"  A3 ({MANIFEST_NAMES['A3']}) Zero-Shot Recall: {a3_rec*100:.1f}% ({a3_tp}/{len(runs_a3)})")

    # 3. Inference latency for C and D
    print("\n" + "="*80)
    print("INFERENCE LATENCY: CONFIG C vs CONFIG D (Python Q16.16 fixed-point)")
    print("="*80)
    for c, name in [("C", "Config C (User-space Float)"), ("D", "Config D (Python Q16.16 fixed-point)")]:
        all_inf = []
        for w in WORKLOADS:
            for r in data[(c, w)]:
                lat = r["latency"].get("inference_latency_us")
                if lat and lat > 0:
                    all_inf.append(lat)
        if all_inf:
            print(f"{name}:")
            print(f"  Mean:   {statistics.mean(all_inf):.3f} us")
            print(f"  Median: {statistics.median(all_inf):.3f} us")
            print(f"  Std:    {statistics.stdev(all_inf):.3f} us")
            print(f"  Min:    {min(all_inf):.3f} us")
            print(f"  Max:    {max(all_inf):.3f} us")

    # 4. Config E freezes per workload, freeze_verified rate, mitigation and rollback latency
    print("\n" + "="*80)
    print("CONFIG E: FREEZES, VERIFICATION RATE, MITIGATION & ROLLBACK LATENCIES")
    print("="*80)
    e_freezes = {}
    total_freezes = 0
    verified_freezes = 0
    mit_latencies = []
    rb_latencies = []
    for w in WORKLOADS:
        runs = data[("E", w)]
        freezes = sum(1 for r in runs if r.get("enforcement", {}).get("mitigation_triggered"))
        verified = sum(1 for r in runs if r.get("enforcement", {}).get("freeze_verified"))
        e_freezes[w] = (freezes, verified, len(runs))
        total_freezes += freezes
        verified_freezes += verified
        for r in runs:
            enf = r.get("enforcement", {})
            if enf.get("mitigation_triggered"):
                m_lat = enf.get("mitigation_latency_ms")
                if m_lat is not None:
                    mit_latencies.append(m_lat)
                r_lat = enf.get("rollback_time_ms")
                if r_lat is not None:
                    rb_latencies.append(r_lat)
        print(f"  {w} ({MANIFEST_NAMES[w]}): Freezes={freezes}/{len(runs)}, Verified={verified}/{freezes if freezes else 1}")

    ver_rate = (verified_freezes / total_freezes * 100.0) if total_freezes > 0 else 0.0
    print(f"\nOverall Freeze Verification Rate: {ver_rate:.2f}% ({verified_freezes}/{total_freezes})")

    if mit_latencies:
        print("\nMitigation Latency (ms):")
        print(f"  Mean:   {statistics.mean(mit_latencies):.3f} ms")
        print(f"  Median: {statistics.median(mit_latencies):.3f} ms")
        print(f"  Max:    {max(mit_latencies):.3f} ms")

    if rb_latencies:
        print("\nRollback Latency (ms):")
        print(f"  Mean:   {statistics.mean(rb_latencies):.3f} ms")
        print(f"  Median: {statistics.median(rb_latencies):.3f} ms")
        print(f"  Max:    {max(rb_latencies):.3f} ms")

    # 5. Totals generated, submitted, consumed, reservation failures, sequence gaps
    print("\n" + "="*80)
    print("TELEMETRY COUNTERS TOTALS (CONFIGS B–E)")
    print("="*80)
    tot_gen = 0
    tot_sub = 0
    tot_con = 0
    tot_res_fail = 0
    tot_seq_gaps = 0
    for c in ["B", "C", "D", "E"]:
        for w in WORKLOADS:
            for r in data[(c, w)]:
                t = r.get("telemetry", {})
                tot_gen += t.get("generated_events", 0)
                tot_sub += t.get("submitted_events", 0)
                tot_con += t.get("consumed_events", 0)
                tot_res_fail += t.get("reservation_failures", 0)
                tot_seq_gaps += t.get("sequence_gaps", 0)

    print(f"Generated Events:     {tot_gen}")
    print(f"Submitted Events:     {tot_sub}")
    print(f"Consumed Events:      {tot_con}")
    print(f"Reservation Failures: {tot_res_fail}")
    print(f"Sequence Gaps:        {tot_seq_gaps}")
    loss_rate = ((tot_gen - tot_con) / tot_gen * 100.0) if tot_gen > 0 else 0.0
    print(f"Overall Event Loss:   {loss_rate:.4f}%")

if __name__ == "__main__":
    main()
