#!/usr/bin/env python3
"""Descriptive audit for the 350-run matrix.

This script deliberately avoids inferential tests whose design assumptions have
not been established. It summarizes observations by configuration/workload and
prints explicit measurement-boundary warnings. Raw JSON records are read-only.
"""
from __future__ import annotations
import glob
import json
import statistics
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "experiments" / "raw"
CONFIGS = ["A", "B", "C", "D", "E"]
WORKLOADS = ["B1", "B2", "B3", "B4", "A1", "A2", "A3"]

def mean(xs):
    return statistics.mean(xs) if xs else float("nan")

def median(xs):
    return statistics.median(xs) if xs else float("nan")

def iqr(xs):
    """Calculates spread using order-statistic index convention:
    sorted[3N // 4] - sorted[N // 4]. For N=70, this corresponds to index 52 minus index 17.
    """
    if not xs:
        return float("nan")
    ordered = sorted(xs)
    return ordered[3 * len(ordered) // 4] - ordered[len(ordered) // 4]

def load_runs():
    runs = []
    for path in sorted(glob.glob(str(RAW_DIR / "run_*.json"))):
        with open(path, encoding="utf-8") as stream:
            runs.append(json.load(stream))
    return runs

def main():
    runs = load_runs()
    print("DESCRIPTIVE EXPERIMENTAL AUDIT — NO CONFIRMATORY INFERENCE")
    print("Loaded " + str(len(runs)) + " raw records from " + str(RAW_DIR))
    lookup = {(r["config_id"], r["workload_id"], r["rep_idx"]): r for r in runs}
    expected = {(c, w, rep) for c in CONFIGS for w in WORKLOADS for rep in range(10)}
    observed = set(lookup)
    print("Expected matrix tuples: " + str(len(expected)) + "; observed unique tuples: " + str(len(observed)))
    print("Missing tuples: " + str(len(expected - observed)) + "; unexpected tuples: " + str(len(observed - expected)))
    if len(runs) != 350 or observed != expected:
        raise SystemExit("Matrix structure mismatch; investigate before interpreting summaries.")

    grouped = defaultdict(list)
    for run in runs:
        grouped[(run["config_id"], run["workload_id"])].append(run)

    print("\nPer-workload duration and RSS summaries")
    print("config,workload,n,duration_mean_s,duration_median_s,duration_iqr_s,rss_mean_mb")
    for config in CONFIGS:
        for workload in WORKLOADS:
            cell = grouped[(config, workload)]
            durations = [r["resources"]["workload_duration_seconds"] for r in cell]
            rss = [r["resources"].get("workload_mem_peak_mb", r["resources"].get("rss_peak_mb", 0.0)) for r in cell]
            row = [config, workload, len(cell), "%.6f" % mean(durations), "%.6f" % median(durations),
                   "%.6f" % iqr(durations), "%.4f" % mean(rss)]
            print(",".join(str(v) for v in row))

    print("\nDescriptive workload-duration differences versus A (percent of A cell mean)")
    print("config,workload,baseline_A_mean_s,config_mean_s,slowdown_pct")
    for config in CONFIGS[1:]:
        for workload in WORKLOADS:
            a = mean([r["resources"]["workload_duration_seconds"] for r in grouped[("A", workload)]])
            x = mean([r["resources"]["workload_duration_seconds"] for r in grouped[(config, workload)]])
            slowdown = ((x - a) / a * 100.0) if a else float("nan")
            print(",".join([config, workload, "%.6f" % a, "%.6f" % x, "%.4f" % slowdown]))

    print("\nInference timing summaries (Python software paths; valid inference runs only)")
    for config in ["C", "D", "E"]:
        vals = [r["latency"]["inference_latency_us"] for r in runs
                if r["config_id"] == config and r["latency"].get("inference_latency_us") and r.get("telemetry", {}).get("consumed_events", 0) > 0]
        print(config + ": n=" + str(len(vals)) + ", run_weighted_mean_us=" + ("%.4f" % mean(vals)) +
              ", median_us=" + ("%.4f" % median(vals)) + ", IQR_us=" + ("%.4f" % iqr(vals)))

    print("\nTelemetry counters (instrumented runs only)")
    total_gen = total_sub = total_consumed = total_fail = total_gaps = 0
    for run in runs:
        if run["config_id"] == "A":
            continue
        t = run.get("telemetry", {})
        total_gen += int(t.get("generated_events", 0))
        total_sub += int(t.get("submitted_events", 0))
        total_consumed += int(t.get("consumed_events", 0))
        total_fail += int(t.get("reservation_failures", 0))
        total_gaps += int(t.get("sequence_gaps", 0))
    print("generated=" + str(total_gen) + "; submitted=" + str(total_sub) + "; consumed=" + str(total_consumed))
    print("reservation_failures=" + str(total_fail) + "; sequence_gaps=" + str(total_gaps))
    print("WARNING: Do not label end-to-end event loss as zero unless generated/submitted/consumed counters reconcile.")
    print("WARNING: No paired tests, ANOVA, equivalence claims, or confirmatory p-values are produced.")
    print("Inference is descriptive. Future hypothesis tests require a justified observational unit and design.")

if __name__ == "__main__":
    main()
