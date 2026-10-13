# Controlled Experiments Package (`experiments/`)

**Milestone:** CHAT 08 Controlled Experiments Execution & CHAT 09 Verification  
**Repository Branch:** `main`  
**Testbed Environment:** Ubuntu 24.04.3 LTS (`x86_64`), Linux kernel `6.6.87.2-microsoft-standard-WSL2`, Clang 18.1.3, bpftool 7.4.0, libbpf 1.4, Docker 29.1.3, Python 3.12.3.

---

## 1. Directory Structure

```
experiments/
├── calibration/
│   ├── calibration_dataset.json           # Isolated calibration samples (seed 999)
│   └── lr_model_frozen.json               # Frozen Logistic Regression model (SHA256: 00c3f945...)
├── manifests/
│   ├── env_manifest.json                  # Pinned testbed environment & toolchain manifest
│   └── experiment_matrix_manifest.json    # Formal 35-cell experimental matrix specification
├── plots/
│   ├── fig1_system_overhead_comparison.png       # CPU utilization & memory RSS across A–E
│   ├── fig2_latency_breakdown_by_stage.png       # Inference and detection latency breakdown
│   ├── fig3_telemetry_throughput_and_loss.png    # Event rate & zero-loss verification
│   ├── fig4_detection_quality_f1_fpr.png         # F1 score vs False Positive Rate
│   └── fig5_mitigation_latency_and_safety.png    # Mitigation latency & legitimate-operation impact
├── processed/
│   ├── detection_performance.csv          # Classification & security metrics per cell
│   ├── latency_breakdown.csv              # Latency breakdown (us/ms) per cell
│   ├── summary_by_configuration.csv       # Marginal summary across Configurations A–E
│   ├── summary_by_workload.csv            # Marginal summary across Workloads B1–B4, A1–A3
│   ├── summary_matrix_all_cells.csv       # Complete 35-cell summary matrix (mean & std)
│   └── summary_metrics.json               # Machine-readable JSON summary dataset
├── raw/
│   ├── run_A_A1_rep0.json ... run_E_B4_rep9.json # 350 immutable per-run raw JSON records
└── scripts/
    ├── calibrate_model.py                 # Isolated calibration & Gate G fixed-point parameter export
    ├── compute_stats.py                   # Statistical distribution extractor (mean, median, IQR, p95)
    ├── generate_plots.py                  # Publication figure renderer (Matplotlib)
    ├── process_results.py                 # Raw JSON parser & summary CSV generator
    ├── run_experiments.py                 # Automated 350-run matrix execution harness
    ├── statistical_analysis.py            # Reproducible hypothesis testing (Wilcoxon, t-test, Cohen's d, ANOVA)
    └── validate_matrix.py                 # Comprehensive 350-run matrix validation & integrity auditor
```

---

## 2. Experimental Matrix Specification

The controlled experimental design evaluates **5 Configurations** across **7 Workloads** with **10 Repetitions** each ($5 \times 7 \times 10 = 350$ runs):

### Configurations
- **A — Baseline:** Bare workload execution without instrumentation.
- **B — eBPF Telemetry Only:** Syscall tracepoint hooks attached (`execve`, `openat`, `connect`, `unlinkat`), 1 MB ring buffer active, counter accounting.
- **C — eBPF + User-Space LR:** eBPF telemetry + 1-second feature aggregation + user-space floating-point Logistic Regression (`model.py`).
- **D — eBPF + Kernel-Local LR:** eBPF telemetry + Q16.16 fixed-point linear classifier evaluated in kernel hook / fixed-point arithmetic (`kernel_lr_feasibility.bpf.c`).
- **E — eBPF + ML + Staged Enforcement:** Full pipeline with staged policy state machine (`OBSERVE` $\rightarrow$ `DETECT_LOG` $\rightarrow$ `CONTROLLED_MITIGATION` $\rightarrow$ `ROLLBACK`) and safe defaults.

### Workloads
- **Benign ($y=0$):** `B1` (Idle), `B2` (File processing), `B3` (Process churn), `B4` (Client-server socket).
- **Anomaly ($y=1$):** `A1` (Process execution burst), `A2` (Abnormal file access), `A3` (Connection burst to test sink).

---

## 3. Data Integrity & Leakage Prevention Rules

1. **Zero Train/Test Leakage:** Model calibration was executed strictly on an independent calibration split (`seed=999`). All 10 evaluation repetitions used seeds `0..9`.
2. **Raw Records Immutability:** Raw per-run JSON files in `raw/` represent immutable primary evidence. All derived CSVs and plots are generated deterministically by scripts.
3. **Transparent Denominators:** Denominators for event loss (total generated events), classification metrics (true/false counts per category), and rollback recovery (triggered containment events) are reported explicitly.

---

## 4. Reproduction Instructions

To reproduce the analysis, summary tables, and figures from the raw data:

```bash
# 1. Recompute statistical summary tables
python3 experiments/scripts/process_results.py

# 2. Extract distribution metrics (median, IQR, p95)
python3 experiments/scripts/compute_stats.py

# 3. Regenerate publication-quality figures
python3 experiments/scripts/generate_plots.py

# 4. Run unit and equivalence tests
./prototype/tests/run_unit_tests.sh

# 5. Run scientific integrity matrix validation
python3 experiments/scripts/validate_matrix.py

# 6. Run formal statistical hypothesis testing
python3 experiments/scripts/statistical_analysis.py
```

---

## 5. Scientific Integrity & Measurement Characterization

In accordance with `research/CHAT09_SCIENTIFIC_INTEGRITY_CORRECTION.md`:
- **Direct Measurements:** System overhead (<0.20% slowdown, $F=0.0264, p=0.9987$), peak host RSS (~0.35–0.55 MB overhead), zero event loss across 280 runs ($16,001$ events), and classification metrics ($A1$ F1=0.824, $B3$ FPR=50%–80%, $A3$ Recall=0%).
- **Fixed-Point Arithmetic Benchmark:** Inference latency in Config D measures a Python Q16.16 integer arithmetic benchmark (40.42x speedup over Python float LR), serving as the algorithmic baseline for Gate G BPF-verifiable in-kernel inference.
- **Formula-Derived Estimates:** End-to-end detection latencies ($1.57$ ms vs $0.08$ ms) are additive architectural estimates incorporating measured inference/aggregation plus standard transport queuing models.
- **Simulated Policy Workflow:** Mitigation latency ($1.17$ ms) and rollback ($15\ \mu\text{s}$) measure in-memory policy state transitions with synthetic verification sleep; kernel-level cgroup v2 freezes remain simulated.
