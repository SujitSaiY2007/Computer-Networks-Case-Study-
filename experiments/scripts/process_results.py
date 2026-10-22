#!/usr/bin/env python3
"""
CHAT 08 — Results Processing Script
Derives processed summary tables and statistical metrics reproducibly from raw run JSON files.
"""
from __future__ import annotations
import csv
import json
import math
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "experiments" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "experiments" / "processed"

CONFIGS = ["A", "B", "C", "D", "E"]
WORKLOADS = ["B1", "B2", "B3", "B4", "A1", "A2", "A3"]

def mean_std(values):
    if not values:
        return 0.0, 0.0
    m = sum(values) / len(values)
    var = sum((x - m) ** 2 for x in values) / (len(values) - 1) if len(values) > 1 else 0.0
    return m, math.sqrt(var)

def p50_p95(values):
    if not values:
        return 0.0, 0.0
    s = sorted(values)
    n = len(s)
    p50 = s[n // 2]
    p95_idx = min(int(math.ceil(0.95 * n)) - 1, n - 1)
    return p50, s[p95_idx]

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    raw_files = list(RAW_DIR.glob("run_*.json"))
    print(f"Loading {len(raw_files)} raw experiment run files...")
    
    cell_data = defaultdict(list)
    for rf in raw_files:
        try:
            with open(rf, "r", encoding="utf-8") as f:
                d = json.load(f)
                key = (d["config_id"], d["workload_id"])
                cell_data[key].append(d)
        except Exception as e:
            print(f"Error reading {rf}: {e}")

    # Verify run matrix completeness
    missing_cells = []
    for c in CONFIGS:
        for w in WORKLOADS:
            count = len(cell_data[(c, w)])
            if count != 10:
                missing_cells.append((c, w, count))
    if missing_cells:
        print(f"WARNING: Incomplete cells detected: {missing_cells}")
    else:
        print("PASS: Verified all 35 cells contain exactly 10 repetitions (350 total runs).")

    # Baseline A lookup for slowdown calculation
    baseline_durations = {}
    baseline_cpus = {}
    for w in WORKLOADS:
        runs_a = cell_data[("A", w)]
        if runs_a:
            durs = [r["resources"]["workload_duration_seconds"] for r in runs_a]
            cpus = [r["resources"]["cpu_utilization_pct"] for r in runs_a]
            baseline_durations[w] = sum(durs) / len(durs)
            baseline_cpus[w] = sum(cpus) / len(cpus)
        else:
            baseline_durations[w] = 1.0
            baseline_cpus[w] = 1.0

    all_cell_rows = []
    config_summary = defaultdict(lambda: defaultdict(list))
    workload_summary = defaultdict(lambda: defaultdict(list))
    summary_metrics_json = {}

    for c in CONFIGS:
        summary_metrics_json[c] = {}
        for w in WORKLOADS:
            runs = cell_data[(c, w)]
            n = len(runs)
            if n == 0:
                continue

            cpu_vals = [r["resources"]["cpu_utilization_pct"] for r in runs]
            rss_vals = [r["resources"]["rss_peak_mb"] for r in runs]
            dur_vals = [r["resources"]["workload_duration_seconds"] for r in runs]
            
            gen_vals = [r["telemetry"]["generated_events"] for r in runs]
            sub_vals = [r["telemetry"]["submitted_events"] for r in runs]
            loss_vals = [r["telemetry"]["loss_rate"] * 100.0 for r in runs]
            tput_vals = [r["telemetry"]["telemetry_throughput_eps"] for r in runs]
            tlat_vals = [r["telemetry"]["telemetry_transfer_latency_us"] for r in runs]

            agg_lat_vals = [r["latency"]["feature_aggregation_us"] for r in runs if r["latency"].get("feature_aggregation_us")]
            inf_lat_vals = [r["latency"]["inference_latency_us"] for r in runs if r["latency"].get("inference_latency_us")]
            dec_lat_vals = [r["latency"]["decision_latency_us"] for r in runs if r["latency"].get("decision_latency_us")]
            det_lat_vals = [r["latency"].get("processing_latency_ms", r["latency"].get("detection_latency_ms", 0.0)) for r in runs if r["latency"].get("processing_latency_ms") or r["latency"].get("detection_latency_ms")]
            mit_lat_vals = [r.get("enforcement", {}).get("mitigation_latency_ms", r["latency"].get("mitigation_latency_ms")) for r in runs if r.get("enforcement", {}).get("mitigation_latency_ms") is not None or r["latency"].get("mitigation_latency_ms") is not None]
            dtm_lat_vals = [r["latency"]["detection_to_mitigation_ms"] for r in runs if r["latency"].get("detection_to_mitigation_ms") is not None]
            rb_lat_vals = [r.get("enforcement", {}).get("rollback_time_ms", r["latency"].get("rollback_time_ms")) for r in runs if r.get("enforcement", {}).get("rollback_time_ms") is not None or r["latency"].get("rollback_time_ms") is not None]

            # Security metrics
            tp_sum = sum(r["classification"]["tp"] for r in runs)
            fp_sum = sum(r["classification"]["fp"] for r in runs)
            tn_sum = sum(r["classification"]["tn"] for r in runs)
            fn_sum = sum(r["classification"]["fn"] for r in runs)
            total_cases = tp_sum + fp_sum + tn_sum + fn_sum
            
            acc = (tp_sum + tn_sum) / total_cases if total_cases > 0 else 0.0
            prec = tp_sum / (tp_sum + fp_sum) if (tp_sum + fp_sum) > 0 else (1.0 if tp_sum == 0 and fp_sum == 0 else 0.0)
            rec = tp_sum / (tp_sum + fn_sum) if (tp_sum + fn_sum) > 0 else 0.0
            f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
            fpr = fp_sum / (fp_sum + tn_sum) if (fp_sum + tn_sum) > 0 else 0.0
            
            legit_impact_sum = sum(r["enforcement"]["legitimate_operations_impacted"] for r in runs)
            mit_trig_sum = sum(1 for r in runs if r["enforcement"]["mitigation_triggered"])
            rb_succ_sum = sum(1 for r in runs if r["enforcement"]["rollback_success"])

            cpu_m, cpu_s = mean_std(cpu_vals)
            rss_m, rss_s = mean_std(rss_vals)
            dur_m, dur_s = mean_std(dur_vals)
            slowdown_pct = ((dur_m - baseline_durations[w]) / baseline_durations[w]) * 100.0 if baseline_durations[w] > 0 else 0.0

            gen_m, gen_s = mean_std(gen_vals)
            loss_m, loss_s = mean_std(loss_vals)
            tput_m, tput_s = mean_std(tput_vals)
            tlat_m, tlat_s = mean_std(tlat_vals)
            
            agg_m, agg_s = mean_std(agg_lat_vals)
            inf_m, inf_s = mean_std(inf_lat_vals)
            dec_m, dec_s = mean_std(dec_lat_vals)
            det_m, det_s = mean_std(det_lat_vals)
            mit_m, mit_s = mean_std(mit_lat_vals)
            dtm_m, dtm_s = mean_std(dtm_lat_vals)
            rb_m, rb_s = mean_std(rb_lat_vals)

            row = {
                "config_id": c,
                "workload_id": w,
                "category": "benign" if w.startswith("B") else "anomaly",
                "repetitions": n,
                "cpu_util_mean_pct": round(cpu_m, 2),
                "cpu_util_std_pct": round(cpu_s, 2),
                "rss_peak_mean_mb": round(rss_m, 2),
                "rss_peak_std_mb": round(rss_s, 2),
                "workload_duration_mean_s": round(dur_m, 3),
                "workload_slowdown_pct": round(slowdown_pct, 2),
                "events_gen_mean": round(gen_m, 1),
                "event_loss_rate_mean_pct": round(loss_m, 4),
                "telemetry_tput_mean_eps": round(tput_m, 1),
                "telemetry_latency_mean_us": round(tlat_m, 2),
                "feature_agg_latency_mean_us": round(agg_m, 2),
                "inference_latency_mean_us": round(inf_m, 3),
                "decision_latency_mean_us": round(dec_m, 3),
                "detection_latency_mean_ms": round(det_m, 3),
                "mitigation_latency_mean_ms": round(mit_m, 3),
                "detection_to_mitigation_mean_ms": round(dtm_m, 3),
                "rollback_time_mean_ms": round(rb_m, 3),
                "tp": tp_sum,
                "fp": fp_sum,
                "tn": tn_sum,
                "fn": fn_sum,
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "fpr": round(fpr, 4),
                "mitigation_triggered_count": mit_trig_sum,
                "rollback_success_count": rb_succ_sum,
                "legitimate_operations_impacted": legit_impact_sum
            }
            all_cell_rows.append(row)
            summary_metrics_json[c][w] = row

            # Feed marginals
            config_summary[c]["cpu"].append(cpu_m)
            config_summary[c]["rss"].append(rss_m)
            config_summary[c]["loss"].append(loss_m)
            config_summary[c]["inf_lat"].append(inf_m)
            config_summary[c]["det_lat"].append(det_m)
            config_summary[c]["f1"].append(f1)
            config_summary[c]["fpr"].append(fpr)
            config_summary[c]["slowdown"].append(slowdown_pct)

            workload_summary[w]["gen_events"].append(gen_m)
            workload_summary[w]["tput"].append(tput_m)
            workload_summary[w]["loss"].append(loss_m)
            workload_summary[w]["cpu"].append(cpu_m)

    # 1. Summary Matrix (all 35 cells)
    summary_matrix_path = PROCESSED_DIR / "summary_matrix_all_cells.csv"
    with open(summary_matrix_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_cell_rows[0].keys(, lineterminator="\n")))
        writer.writeheader()
        writer.writerows(all_cell_rows)
    print(f"Written: {summary_matrix_path}")

    # 2. Summary by Configuration
    config_rows = []
    for c in CONFIGS:
        d = config_summary[c]
        config_rows.append({
            "config_id": c,
            "mean_cpu_pct": round(sum(d["cpu"]) / len(d["cpu"]), 2),
            "mean_rss_mb": round(sum(d["rss"]) / len(d["rss"]), 2),
            "mean_slowdown_pct": round(sum(d["slowdown"]) / len(d["slowdown"]), 2),
            "mean_event_loss_pct": round(sum(d["loss"]) / len(d["loss"]), 4),
            "mean_inference_lat_us": round(sum(d["inf_lat"]) / len(d["inf_lat"]), 3),
            "mean_detection_lat_ms": round(sum(d["det_lat"]) / len(d["det_lat"]), 3),
            "mean_f1": round(sum(d["f1"]) / len(d["f1"]), 4),
            "mean_fpr": round(sum(d["fpr"]) / len(d["fpr"]), 4)
        })
    config_csv_path = PROCESSED_DIR / "summary_by_configuration.csv"
    with open(config_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(config_rows[0].keys(, lineterminator="\n")))
        writer.writeheader()
        writer.writerows(config_rows)
    print(f"Written: {config_csv_path}")

    # 3. Summary by Workload
    wl_rows = []
    for w in WORKLOADS:
        d = workload_summary[w]
        wl_rows.append({
            "workload_id": w,
            "category": "benign" if w.startswith("B") else "anomaly",
            "mean_cpu_pct": round(sum(d["cpu"]) / len(d["cpu"]), 2),
            "mean_generated_events": round(sum(d["gen_events"]) / len(d["gen_events"]), 1),
            "mean_telemetry_tput_eps": round(sum(d["tput"]) / len(d["tput"]), 1),
            "mean_loss_rate_pct": round(sum(d["loss"]) / len(d["loss"]), 4)
        })
    wl_csv_path = PROCESSED_DIR / "summary_by_workload.csv"
    with open(wl_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(wl_rows[0].keys(, lineterminator="\n")))
        writer.writeheader()
        writer.writerows(wl_rows)
    print(f"Written: {wl_csv_path}")

    # 4. Latency Breakdown Table
    lat_rows = []
    for r in all_cell_rows:
        if r["config_id"] in ("C", "D", "E"):
            lat_rows.append({
                "config_id": r["config_id"],
                "workload_id": r["workload_id"],
                "telemetry_transfer_us": r["telemetry_latency_mean_us"],
                "feature_aggregation_us": r["feature_agg_latency_mean_us"],
                "inference_us": r["inference_latency_mean_us"],
                "decision_us": r["decision_latency_mean_us"],
                "detection_total_ms": r["detection_latency_mean_ms"],
                "mitigation_enforcement_ms": r["mitigation_latency_mean_ms"],
                "detection_to_mitigation_total_ms": r["detection_to_mitigation_mean_ms"],
                "rollback_recovery_ms": r["rollback_time_mean_ms"]
            })
    lat_csv_path = PROCESSED_DIR / "latency_breakdown.csv"
    with open(lat_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(lat_rows[0].keys(, lineterminator="\n")))
        writer.writeheader()
        writer.writerows(lat_rows)
    print(f"Written: {lat_csv_path}")

    # 5. Detection Performance Table
    det_rows = []
    for r in all_cell_rows:
        if r["config_id"] in ("C", "D", "E"):
            det_rows.append({
                "config_id": r["config_id"],
                "workload_id": r["workload_id"],
                "tp": r["tp"],
                "fp": r["fp"],
                "tn": r["tn"],
                "fn": r["fn"],
                "accuracy": r["accuracy"],
                "precision": r["precision"],
                "recall": r["recall"],
                "f1_score": r["f1_score"],
                "fpr": r["fpr"],
                "mitigations_triggered": r["mitigation_triggered_count"],
                "legitimate_ops_impacted": r["legitimate_operations_impacted"]
            })
    det_csv_path = PROCESSED_DIR / "detection_performance.csv"
    with open(det_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(det_rows[0].keys(, lineterminator="\n")))
        writer.writeheader()
        writer.writerows(det_rows)
    print(f"Written: {det_csv_path}")

    # 6. JSON Export
    json_path = PROCESSED_DIR / "summary_metrics.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary_metrics_json, f, indent=2)
    print(f"Written: {json_path}")
    print("\nSummary processing completed successfully.")

if __name__ == "__main__":
    main()
