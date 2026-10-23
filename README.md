> **Journal-submission status (2026-10-23):** The journal submission title is **“eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, In-Kernel Inference, and Containment Trade-offs.”** Requested author line: **Giri Nikhil Vaishnav, Sujit Sai Y, Shaik Mohammad Asif, and Ragavan K.** The supplied final PDF is the source of truth for the journal version. See [paper/JOURNAL_SUBMISSION_RECORD.md](paper/JOURNAL_SUBMISSION_RECORD.md) for frozen claims and the synchronization boundary. The existing [paper/MAIN_MANUSCRIPT.md](paper/MAIN_MANUSCRIPT.md) is explicitly marked as superseded; the repository is **not yet fully synchronized** until the final PDF and matching editable source are committed. No experiments are to be rerun or results re-evaluated.

---

# BACSE203 Computer Networks Case Study — Canonical Source of Truth

## Topic
**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

---

## Author & Project Details
- **Student / Author:** Sujit Sai
- **Course:** BACSE203 Computer Networks Case Study
- **Canonical Branch:** `main` only
- **Current Status:** **Chat 11 Complete with Disclosed Limitations** (Final validation, numerical reconciliation, reproducibility audit, and manuscript closure complete)
- **Primary Audit Report:** [`research/CHAT11_FINAL_AUDIT_REPORT.md`](research/CHAT11_FINAL_AUDIT_REPORT.md)
- **Authoritative Manuscript:** [`paper/MAIN_MANUSCRIPT.md`](paper/MAIN_MANUSCRIPT.md)
- **Claim-to-Evidence Map:** [`research/CHAT10_CLAIM_TO_EVIDENCE_MAP.md`](research/CHAT10_CLAIM_TO_EVIDENCE_MAP.md)
- **Project Handoff:** [`project/CHAT_HANDOFF.md`](project/CHAT_HANDOFF.md)
- **Master Plan:** [`project/MASTER_EXECUTION_PLAN.md`](project/MASTER_EXECUTION_PLAN.md)

---

## Executive Summary & Research Scope
This study investigates the practical boundary between kernel-space observation and user-space machine learning detection for cloud-native container runtimes. Using a controlled prototype and an offline 350-run experimental matrix, the research quantifies syscall tracepoint telemetry overhead, evaluates fixed-point Q16.16 arithmetic feasibility against floating-point inference, assesses detection trade-offs across diverse container workloads, and evaluates simulated mitigation latency.

The defensible contribution is an evidence-aligned empirical evaluation reporting both low telemetry overhead and significant detection failure modes (notably high false alarms during benign build churn and complete misses on held-out connection attacks), while clearly distinguishing measured software benchmarks from in-kernel execution and operating-system enforcement.

---

## Frozen Evidence Baseline
- **Primary-Study Baseline:** 40 studies = 36 journal articles + 4 peer-reviewed conference papers (90% peer-reviewed journals).
- **Review 2 Reference Corpus:** 50 references = 40 primary studies + 10 supporting/background works.
- **Experimental Dataset:** Exactly 350 immutable raw JSON runs across 35 configuration–workload cells (10 repetitions per cell) under `experiments/raw/`.

---

## Repository Structure
```
.
├── README.md                                  # Canonical project source of truth
├── paper/
│   └── MAIN_MANUSCRIPT.md                     # Authoritative Harvard-style manuscript
├── prototype/
│   ├── bpf/                                   # Native eBPF C programs and loader
│   │   ├── telemetry.bpf.c                    # Syscall tracepoint probe (ring buffer)
│   │   ├── kernel_lr_feasibility.bpf.c        # Fixed-point Q16.16 linear classifier
│   │   ├── telemetry_loader.c                 # Userspace ring-buffer consumer
│   │   └── Makefile                           # Clang/LLVM build configuration
│   ├── python/                                # Feature aggregation, ML scoring, policy
│   │   ├── features.py                        # Fixed 9-feature sliding window aggregation
│   │   ├── model.py                           # Logistic regression training & scoring
│   │   └── policy.py                          # Multi-stage mitigation/rollback engine
│   ├── tests/                                 # Unit, smoke, and feasibility tests
│   │   ├── run_unit_tests.sh                  # Python unit test runner (4/4 PASS)
│   │   ├── run_software_smoke.py              # End-to-end synthetic smoke pipeline (PASS)
│   │   └── test_kernel_lr_feasibility.py      # Q16.16 vs Float numerical verification
│   └── preflight.sh                           # Host environment and dependency audit
├── experiments/
│   ├── manifests/
│   │   ├── experiment_matrix_manifest.json    # 35-cell experimental matrix specification
│   │   └── env_manifest.json                  # Host hardware, kernel, and toolchain manifest
│   ├── raw/                                   # 350 immutable raw JSON execution records
│   ├── processed/                             # Six deterministic CSV/JSON summary tables
│   ├── plots/                                 # Publication-grade SVG/PNG visualizations
│   ├── scripts/
│   │   ├── validate_matrix.py                 # Strict matrix schema & data validator
│   │   ├── statistical_analysis.py            # Stratified descriptive statistics generator
│   │   ├── process_results.py                 # Raw-to-summary processing pipeline
│   │   ├── compute_stats.py                   # Statistical dispersion & hypothesis tests
│   │   └── generate_plots.py                  # Visualization generation script
│   └── README.md                              # Experiments package documentation & audit notice
├── research/
│   ├── CHAT11_FINAL_AUDIT_REPORT.md           # Authoritative Chat 11 closure report
│   ├── CHAT10_CLAIM_TO_EVIDENCE_MAP.md        # Line-by-line claim-to-evidence matrix
│   ├── CHAT09_SCIENTIFIC_INTEGRITY_CORRECTION.md # Categorization of empirical claims
│   ├── CHAT08_CONTROLLED_EXPERIMENTS_EXECUTION.md# Matrix execution records & provenance
│   ├── CHAT07_IMPLEMENTATION_AND_VALIDATION.md  # Prototype gates A–G validation
│   └── PAPER_ACQUISITION_AND_ARCHIVE.md       # Full literature register with DOIs
└── project/
    ├── CHAT_HANDOFF.md                        # Active chat-to-chat operational handoff
    ├── MASTER_EXECUTION_PLAN.md               # Multi-chat master execution roadmap
    └── STATUS_CORRECTION_2026-10-13.md        # Authoritative status and scope corrections
```

---

## Experimental Matrix Design
Confirmed by [`experiments/manifests/experiment_matrix_manifest.json`](experiments/manifests/experiment_matrix_manifest.json):
- **Total Experimental Runs:** Exactly 350 records (`run_{Config}_{Workload}_rep{0-9}.json`).
- **Matrix Cells:** 35 cells (5 Configurations $\times$ 7 Workloads $\times$ 10 Repetitions).
- **Configurations:**
  - `A`: Baseline (uninstrumented container workload).
  - `B`: Telemetry Overhead (eBPF syscall tracing + ring-buffer consumer).
  - `C`: Userspace Float Inference (telemetry + scikit-learn Logistic Regression).
  - `D`: Fixed-Point Feasibility (telemetry + Python Q16.16 integer scoring).
  - `E`: Detection + Mitigation Workflow (telemetry + scoring + simulated rollback).
- **Workloads:**
  - Benign: `B1` (idle), `B2` (file processing), `B3` (process churn), `B4` (local socket client-server).
  - Anomaly: `A1` (drop and execute), `A2` (read-only file sweep), `A3` (local connection burst).

---

## Validation Status & Execution Evidence

| Validation Check | Scope / Target | Command Executed | Result | Exit Code | Diagnostic Details |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Matrix Integrity** | All 350 raw JSON files | `python experiments/scripts/validate_matrix.py` | **PASS** | 0 | 35 cells $\times$ 10 reps verified; 0 schema violations, 0 nulls, 0 NaNs. |
| **Raw Data Immutability** | All 350 raw JSON files | SHA-256 verification against baseline manifest | **PASS** | 0 | 100% byte-for-byte identical; 0 files modified or corrupted. |
| **Descriptive Statistics** | Raw dataset | `python experiments/scripts/statistical_analysis.py` | **PASS** | 0 | Stratified cell and marginal summaries generated cleanly. |
| **Processed Reproduction** | Summary tables | `python experiments/scripts/process_results.py` | **PASS** | 0 | Deterministically reproduces all 6 CSV/JSON tables with 0 content diffs. |
| **Python Unit Tests** | Prototype core | `bash prototype/tests/run_unit_tests.sh` | **PASS** | 0 | 4/4 unit tests passed (`features`, `model`, `policy`, `kernel_lr_feasibility`). |
| **Software Smoke Test** | Synthetic pipeline | `python prototype/tests/run_software_smoke.py` | **PASS** | 0 | Synthetic fixture ingestion, aggregation, scoring, and policy PASS. |
| **Toolchain Preflight** | WSL2 environment | `bash prototype/preflight.sh` | **PASS** | 0 | Linux 6.6.87.2-WSL2, Clang 18.1.3, bpftool 7.4.0, libbpf verified. |
| **Native BPF Compilation**| C probes & loader | `make -C prototype/bpf clean && make -C prototype/bpf` | **PASS** | 0 | Clean ELF objects (`telemetry.bpf.o`, `kernel_lr_feasibility.bpf.o`, `telemetry_loader`). |
| **Live In-Kernel Load** | BPF program loading | `bpftool prog load prototype/bpf/telemetry.bpf.o ...` | **PASS / BLOCKED** | 0 / 1 | The 13 Oct matrix loaded the probe as root on WSL2 with full `CAP_BPF` / `CAP_SYS_ADMIN` privileges; only the later Chat 11 audit environment lacked privilege (`/proc/sys/kernel/unprivileged_bpf_disabled = 2`). |

---

## Independent Numerical Reconciliation

### 1. Configuration D Inference Latency
The previous apparent conflict between $4.19\ \mu\text{s}$ and $4.238\ \mu\text{s}$ has been fully reconciled from the raw records:
- **Exclusion of Non-Inference Run:** In run `run_D_B3_rep5.json`, zero events were consumed (`consumed_events = 0`), so no inference took place and $0.0\ \mu\text{s}$ was recorded. This record is excluded from valid inference measurements.
- **Run-Weighted Mean of Valid Runs ($N=69$):** **$4.247\ \mu\text{s}$** ($4.2469\ \mu\text{s}$; median $3.634\ \mu\text{s}$; order-statistic IQR $1.475\ \mu\text{s}$; linear-interpolation IQR $1.475\ \mu\text{s}$).
- **Summary Table Mean (`summary_by_configuration.csv`):** **$4.238\ \mu\text{s}$** ($4.2382\ \mu\text{s}$). The processing script (`process_results.py`) filtered out $0.0$ via `if r["latency"].get("inference_latency_us"):` (since `bool(0.0) is False`), calculating the B3 cell mean over the 9 active runs as $3.637\ \mu\text{s}$. The unweighted average of the seven workload cell means ($3.367, 3.956, 4.065, 4.247, 3.953, 3.637, 6.442\ \mu\text{s}$) yields exactly **$4.2382\ \mu\text{s}$**.
- **Historical Grand Mean ($N=70$):** **$4.186\ \mu\text{s} \approx 4.19\ \mu\text{s}$**. This older figure resulted from diluting the sum of latencies ($293.034\ \mu\text{s}$) by all 70 raw entries including the non-inference zero observation ($293.034 / 70$), which is mathematically invalid as a summary of inference latency.
- **Speedup Ratios (Config C vs. Valid Config D):** Comparing Config C float scikit-learn ($169.20\ \mu\text{s}$ mean, $76.24\ \mu\text{s}$ median) to valid Config D measurements yields **$39.84\times$** by run-weighted means ($169.20 / 4.247$), **$39.92\times$** by unweighted cell-mean averages ($169.20 / 4.238$), and **$20.98\times$** by medians ($76.24 / 3.634$). Both benchmarks measure **userspace Python execution** (Q16.16 integer arithmetic vs. scikit-learn float), characterizing algorithmic arithmetic feasibility rather than in-kernel execution.

### 2. Telemetry Event Accounting
Across the 280 instrumented runs (Configurations B, C, D, and E):
- **Generated Events:** **16,001**
- **Submitted Events:** **15,999** (difference of 2 unsubmitted events: 1 in `run_C_A1_rep1.json` and 1 in `run_D_B3_rep4.json`).
- **Consumed Events:** **15,970** (difference of 29 unconsumed events across 23 runs where the harness polling loop terminated with residual events in the ring buffer).
- **Reservation Failures:** **0**
- **Sequence Gaps:** **0**
- **Ring Buffer Drop Rate:** **$0.0000\%$**.
- **Claim Boundary:** While ring-buffer transport had zero internal drops or gaps, the presence of 31 unsubmitted/unconsumed boundary events at harness exit precludes an unconditional "zero end-to-end event loss" claim.

### 3. Key Detection Findings
- **A1 Process Bursts:** 7/10 detected (Precision 1.00, Recall 0.70, F1 0.824).
- **B3 Benign Churn (Builds):** 50%–80% False Positive Rate across C/D/E, demonstrating severe feature confounding with legitimate developer activity.
- **A2 File Access Bursts:** 0% recall in C/D; 20% in E.
- **A3 Connection Bursts:** 0% recall across all configurations (failure on held-out network pattern).

---

## Reproduction Guide

### Environment & Toolchain Prerequisites
- **Operating System:** Linux x86_64 (tested on Ubuntu 24.04 LTS under WSL2; kernel 6.6.87.2-microsoft-standard-WSL2).
- **Compilers & Tools:** Clang/LLVM 18.1.3, GCC 13.3.0, `make`, `bpftool v7.4.0`, `libbpf-dev` (v1.3.0).
- **Python Runtime:** Python 3.12+ with `numpy` and `scikit-learn`.

### Step-by-Step Reproduction Commands

1. **Verify Raw Data Integrity:**
   ```bash
   python experiments/scripts/validate_matrix.py
   ```

2. **Run Descriptive Statistics:**
   ```bash
   python experiments/scripts/statistical_analysis.py
   ```

3. **Reprocess Derived Summary Tables (Optional / Verification):**
   ```bash
   python experiments/scripts/process_results.py
   ```

4. **Execute Prototype Unit Tests:**
   ```bash
   cd prototype && python -m unittest discover -s tests -p 'test_*.py' -v && cd ..
   ```

5. **Execute Prototype Software Smoke Pipeline:**
   ```bash
   cd prototype && python tests/run_software_smoke.py && cd ..
   ```

6. **Compile Native eBPF Programs (Requires Linux/WSL2):**
   ```bash
   make -C prototype/bpf clean && make -C prototype/bpf
   ```

---

## Remaining Disclosed Limitations & Next Actions
1. **Live Kernel Probe Loading (BLOCKED):** `sys_bpf(BPF_PROG_LOAD)` requires elevated root privileges or `CAP_BPF` on Linux hosts where `/proc/sys/kernel/unprivileged_bpf_disabled = 2`. Native compilation and BPF verifier feasibility are established, but live probe evaluation remains future work.
2. **Formula-Derived Latency:** Detection latency values ($T_{\text{detect}}$) are additive architectural estimates incorporating component timings and assumed queuing constants, not direct hardware timestamp intervals.
3. **Simulated Mitigation:** Configuration E measures Python policy state transitions with synthetic delays; active operating-system enforcement (cgroup v2 freezing, iptables rules) remains simulated.
4. **Submission Status:** The manuscript is finalized and fully aligned with verified evidence. Reviewers and readers should treat all findings within the disclosed methodological bounds.
