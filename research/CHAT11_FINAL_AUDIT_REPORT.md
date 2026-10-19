# Chat 11 — Final Experimental Audit and Validation Report

**Audit date:** 19 October 2026  
**Final Status:** COMPLETE WITH DISCLOSED LIMITATIONS  
**Repository:** https://github.com/SujitSaiY2007/Computer-Networks-Case-Study-  
**Branch:** `main` (strictly maintained; no feature branch created or switched)  
**Starting Commit SHA:** `5e2bbd76485e1fb777f245712b1575d783f64655`  
**Execution Environment:** Windows 11 host (PowerShell 7 / Python 3.12.4) and Ubuntu 24.04.3 LTS on WSL2 (Linux kernel `6.6.87.2-microsoft-standard-WSL2`, Clang 18.1.3, GCC 13.3.0, bpftool 7.4.0, Python 3.12.3).  
**Primary Auditor:** Antigravity Pair Programmer (Autonomous Audit Session)  

---

## 1. Executive Summary

This report concludes the final validation, reproducibility audit, and manuscript closure phase (Chat 11). Operating directly on local clone `Computer-Networks-Case-Study` on authorized branch `main`, the audit has:
1. Verified existing safety backups and generated an additional timestamped safety backup outside the repository (`Computer-Networks-Case-Study-safety-backup-phase1-20261019-215628.tar.gz`).
2. Catalogued all 350 raw experiment JSON records and confirmed 100% byte-for-byte SHA-256 integrity before and after all audit operations.
3. Executed matrix validation (`validate_matrix.py`) and statistical analysis (`statistical_analysis.py`) against the raw dataset, both exiting with status 0.
4. Resolved the known numerical discrepancy regarding Configuration D inference latency: 4.186 μs ($\approx 4.19\ \mu\text{s}$) is the grand mean across all 70 raw runs, whereas 4.238 μs in `summary_by_configuration.csv` is the unweighted average of seven workload cell means resulting from `process_results.py` filtering out the single 0.0 μs observation in `run_D_B3_rep5.json` (where 0 events were consumed).
5. Fully reconciled telemetry event accounting across all 280 instrumented runs: 16,001 generated, 15,999 submitted (2 unsubmitted events across 2 runs), 15,970 consumed (29 unconsumed events across 23 runs), with 0 reservation failures and 0 sequence gaps.
6. Replicated summary table and metric generation in an isolated test environment, demonstrating zero content differences against committed processed CSV and JSON artifacts.
7. Executed all supported prototype tests: Python unit tests (4/4 PASS), software smoke pipeline (PASS), and native BPF compilation (PASS with Clang 18.1.3 and GCC 13.3.0). Live kernel probe loading was verified as BLOCKED due to standard unprivileged BPF restrictions (`unprivileged_bpf_disabled=2` requiring `CAP_BPF`/root).
8. Completed a full bibliographic audit: verified all 14 cited references against official DOI registries, proceedings, and the canonical repository evidence matrix, expanding all abbreviated author lists to full Harvard citations.
9. Corrected the manuscript (`paper/MAIN_MANUSCRIPT.md`) and package documentation (`experiments/README.md`) to reflect these reconciled findings.

**Final Verdict:** **COMPLETE WITH DISCLOSED LIMITATIONS.** The BACSE203 course study is defensible, mathematically reconciled, and reproducible. The manuscript explicitly qualifies all simulated enforcement, arithmetic benchmark speedups, and environment-specific constraints.

---

## 2. Safety and Backup Verification

Before executing any script or output-generating step, backup integrity was confirmed:
- **Pre-existing Safety Backup:** `Computer-Networks-Case-Study-safety-backup-20261019-161557.tar.gz` (Length: 63,284,735 bytes, tar header verified readable).
- **Additional Timestamped Backup Created:** `Computer-Networks-Case-Study-safety-backup-phase1-20261019-215628.tar.gz` (Length: 31,970,608 bytes, tar gzip archive excluding `.git`).
- **Outside Evidence Directory:** `C:\Users\sujit\.gemini\antigravity-ide\scratch\chat11_audit_evidence` created to store execution logs, checksum files, and diff comparisons without modifying repository tracking.
- **Raw Data Immutability:** Preflight SHA-256 checksums of all 350 raw JSON files were recorded in `raw_data_checksums.sha256`. Post-validation verification confirmed that 350/350 raw files remain byte-for-byte identical.

---

## 3. Command Execution and Validation Log

All commands required by the audit protocol were executed directly in the current environment. No commands were fabricated or skipped:

| Command | Working Directory / Environment | Exit Code | Outcome | Execution Details |
|---|---|---:|---|---|
| `git status --short --branch` | Repo root / Windows | 0 | PASS | Confirmed branch `main`, tracking `origin/main`, clean working tree. |
| `python experiments/scripts/validate_matrix.py` | Repo root / Windows | 0 | PASS | Checked 350 unique tuples, 35 cells × 10 reps, finite durations and RSS, classification consistency. |
| `python experiments/scripts/statistical_analysis.py` | Repo root / Windows | 0 | PASS | Loaded 350 records; reported cell durations, RSS, slowdowns, inference timings, and telemetry totals. |
| `python chat11_audit_evidence/run_deep_audit.py` | Evidence dir / Windows | 0 | PASS | Comprehensive schema audit of all 350 raw JSON files; 0 corrupted files, 0 duplicate IDs, 0 null/NaN fields. |
| `python chat11_audit_evidence/test_process_results.py` | Evidence dir / Windows | 0 | PASS | Deterministic recomputation of all 6 summary tables/JSON in isolated directory; 0 text differences against committed files. |
| `python -m unittest discover -s tests -p 'test_*.py' -v` | `prototype/` / Windows | 0 | PASS | 4/4 Python unit tests passed (deterministic aggregation, Q16.16 float equivalence, schema rejection, policy safe defaults). |
| `./prototype/tests/run_unit_tests.sh` | `prototype/tests/` / WSL2 | 0 | PASS | Executed bash unit test harness in Ubuntu 24.04 WSL2; 4/4 tests passed in 0.003s. |
| `python tests/run_software_smoke.py` | `prototype/` / Windows | 0 | PASS | End-to-end simulated smoke test passed all 9 stages; validated manifest generation and determinism. |
| `./prototype/preflight.sh` | Repo root / WSL2 | 0 | PASS | Environment preflight passed; verified kernel 6.6.87.2, clang 18.1.3, bpftool 7.4.0, BTF vmlinux, cgroup v2, numpy, sklearn. |
| `make clean && make` | `prototype/bpf/` / WSL2 | 0 | PASS | Cleanly compiled `telemetry.bpf.o`, `kernel_lr_feasibility.bpf.o` (Clang BPF target) and `telemetry_loader` (GCC C11). |
| `bpftool prog load kernel_lr_feasibility.bpf.o ...` | `prototype/bpf/` / WSL2 | 1 | BLOCKED | `Operation not permitted (1)` due to `unprivileged_bpf_disabled=2`. Requires root / `CAP_BPF`. Correctly preserved security controls. |

---

## 4. Numerical Reconciliation and Audit Table

The following explicit reconciliation table resolves all reported metrics, populations, and discrepancies between raw observations, processed tables, and manuscript text:

| Metric | Existing Reported Value | Recomputed Value | Source / Population | Difference | Audit Decision | Manuscript Action |
|---|---|---|---|---|---|---|
| **Config D Inference Latency (Grand Mean)** | 4.19 μs | 4.1862 μs | All 70 raw runs of Config D (`run_D_*.json`) | -0.0038 μs (<0.1%) | Retain 4.19 μs as grand mean across all 70 evaluation runs. | Document as grand mean ($N=70$) in Abstract and Section 5.4. |
| **Config D Inference Latency (Summary Table)** | 4.238 μs | 4.2382 μs | Unweighted average of 7 workload cell means in `process_results.py` | +0.0002 μs (exact) | Explain mechanism: `run_D_B3_rep5.json` had 0 events consumed (0.0 μs latency); `process_results.py` averaged the 9 active runs for B3 (3.637 μs). | Disclose both 4.19 μs (grand mean) and 4.238 μs (cell-mean average) in Section 5.4. |
| **Config D Active Runs Mean** | Not previously reported | 4.2469 μs | 69 runs of Config D with non-zero inference ($x > 0$) | +0.0607 μs | Additional distribution detail for completeness. | Disclosed in Section 5.4. |
| **Config D Median & IQR** | Median ~3.63 μs; IQR ~1.48 μs | Median = 3.6255 μs; Order-stat IQR = 1.4760 μs; Linear-interp IQR = 1.4678 μs | 70 raw runs of Config D | Exact match | Confirmed. Document order-statistic quartile convention (index 52 minus index 17). | Added IQR convention docstring to `statistical_analysis.py`; noted in manuscript. |
| **Config C Inference Latency** | 169.20 μs | Grand mean = 169.2017 μs; Median = 76.2410 μs; IQR = 44.4680 μs | 70 raw runs of Config C | <0.002 μs | Verified exact. | Retain 169.20 μs; note median (76.24 μs). |
| **Inference Timing Ratio (C / D)** | ~40.4× mean ratio; ~21× median ratio | Grand mean ratio = 40.42×; Cell-mean ratio = 39.93×; Median ratio = 21.03× | Config C vs Config D inference distributions | Exact match | Retain 40.4× (grand means) and 39.9× (table means). Strictly qualify as Python software benchmark, not in-kernel speedup. | Reaffirmed qualification in Abstract and Section 5.4. |
| **Telemetry Events Generated** | 16,001 | 16,001 | 280 instrumented runs (Configs B, C, D, E) | 0 | Verified exact across all 280 runs. | Retained. |
| **Telemetry Events Submitted** | 15,999 | 15,999 | 280 instrumented runs | 0 | Verified exact. Exactly 2 runs recorded $gen - sub = 1$ (`run_C_A1_rep1` and `run_D_B3_rep4`). | Reconciled in Section 5.2. |
| **Telemetry Events Consumed** | Previously unverified | 15,970 | 280 instrumented runs | 29 events unconsumed at harness exit | Reconciled: 23 runs had submitted events exceeding consumed events by 1–3 events due to loop exit prior to buffer drain. | Reconciled in Section 5.2 and Abstract; confirms no claim of zero end-to-end loss. |
| **Ring-Buffer Reservation Failures** | 0 | 0 | 280 instrumented runs | 0 | Verified zero buffer drop events across all runs. | Retained. |
| **Ring-Buffer Sequence Gaps** | 0 | 0 | 280 instrumented runs | 0 | Verified zero sequence gaps across all runs. | Retained. |
| **Mean Slowdown vs Baseline A** | B: 0.19%, C: 0.09%, D: 0.16%, E: 0.06% | B: +0.19%, C: +0.09%, D: +0.16%, E: +0.06% | 350 raw runs; mean of cell differences relative to baseline A | Exact match (<0.01% rounding) | All observed slowdowns remain strictly <0.20%. | Retained as descriptive observations in testbed. |
| **Peak Resident Memory RSS** | A: 93.18, B: 93.53, C: 93.63, D: 93.63, E: 93.73 MB | A: 93.18, B: 93.53, C: 93.63, D: 93.63, E: 93.73 MB | 350 raw runs (`resources.rss_peak_mb`) | 0.00 MB | Verified exact. Represents host Python process RSS, not pure kernel memory overhead. | Retained with explicit measurement boundary. |
| **A1 Detection Performance** | TP=7, FN=3, FP=0, TN=0; F1=0.824 | TP=7, FN=3, FP=0, TN=0; Prec=1.000, Rec=0.700, F1=0.8235 | 30 runs of A1 in Configs C, D, E | Exact match | Verified exact. | Retained. |
| **B3 False Positive Rate** | C: 80%, D: 50%, E: 80% | C: 8/10 (80%), D: 5/10 (50%), E: 8/10 (80%) | 30 runs of B3 in Configs C, D, E | Exact match | Verified exact. Highlights major operational limitation. | Retained. |
| **A2 & A3 Detection Recall** | A2: C=0%, D=0%, E=20%; A3: 0% in C/D/E | A2: C=0/10, D=0/10, E=2/10; A3: 0/10 in C/D/E | 60 runs of A2/A3 in Configs C, D, E | Exact match | Verified exact. Demonstrates linear model generalization failures. | Retained. |
| **Mitigation & Rollback Latency (E)** | Mitigation ~1.17 ms; Rollback ~15 μs | Mitigation mean = 1.1720 ms (median 1.1549 ms); Rollback mean = 0.0150 ms = 15.0 μs (median 0.0140 ms) | 17 triggered actions in Config E | Exact match | Verified exact. Represents in-memory Python state machine with synthetic sleep. | Retained with simulation qualification. |

---

## 5. Prototype Test Outcomes by Category

Tests were categorized by dependency and privilege level:

1. **Python Unit Tests:** **PASS**
   - Executed via `python -m unittest discover -s tests -p 'test_*.py' -v` and `./prototype/tests/run_unit_tests.sh`.
   - 4 test cases passed: deterministic feature aggregation, Q16.16 fixed-point vs float numerical equivalence, model schema rejection, and policy safe defaults.
2. **Software Smoke Pipeline:** **PASS**
   - Executed via `prototype/tests/run_software_smoke.py`.
   - Validated synthetic event generation, 1-second feature aggregation, model training and scoring determinism, policy state evaluation, and reproducibility manifest creation.
3. **Native Compilation & Preflight Checks:** **PASS**
   - Executed `./prototype/preflight.sh` in WSL2 Ubuntu 24.04: all tools and kernel facilities present (`PREFLIGHT=PASS`).
   - Cleanly compiled `prototype/bpf/` with Clang 18.1.3 and GCC 13.3.0 (`telemetry.bpf.o`, `kernel_lr_feasibility.bpf.o`, and `telemetry_loader`).
4. **Kernel / Live BPF Probing:** **BLOCKED (Documented)**
   - Executing `telemetry_loader` or `bpftool prog load` to attach live probes to kernel tracepoints returned `EPERM` because `/proc/sys/kernel/unprivileged_bpf_disabled` is set to `2`.
   - Running live in-kernel telemetry requires elevated root privileges (`CAP_BPF` / `CAP_SYS_ADMIN`), which are restricted in the current unprivileged session. This boundary is explicitly disclosed in accordance with Safety Rule 12.

---

## 6. Manuscript and Bibliography Audit

### 6.1 Textual and Quantitative Corrections Made

`paper/MAIN_MANUSCRIPT.md` was updated with the following specific, verified enhancements:
1. **Abstract:** Clarified telemetry counter reconciliation (16,001 generated, 15,999 submitted, 15,970 consumed, 0 reservation failures, 0 sequence gaps) and stated both the grand mean (4.19 μs) and cell-mean average (4.238 μs) for Configuration D.
2. **Section 2 (Background):** Added in-text citations for `Remya et al. (2025)`, `Zehra et al. (2025)`, and `Zhan et al. (2023)` in the container attack and resource exhaustion discussion, ensuring 100% agreement between text and reference list.
3. **Section 5.2 (Telemetry Accounting):** Added a structured breakdown explaining the 2 unsubmitted events across 2 runs and the 29 unconsumed events across 23 runs, confirming that zero reservation failures and sequence gaps prove ring-buffer capacity but not unconditional end-to-end zero loss.
4. **Section 5.4 (Fixed-Point Benchmark):** Documented the population decomposition for 4.19 μs (grand mean, $N=70$), 4.238 μs (unweighted mean of cell means in `process_results.py` filtering out the zero-latency run `run_D_B3_rep5.json`), and 4.247 μs (mean of 69 active inference runs). Reaffirmed speedup ratios (40.42× grand mean, 39.93× table mean, 21.03× median) as software arithmetic benchmarks.
5. **Section References:** Fully expanded all 14 reference entries from abbreviated `et al.` forms to complete Harvard references with verified author rosters, exact titles, venues, volume/page ranges, and DOIs.

### 6.2 Full Bibliography Verification Table

All 14 references in the manuscript were audited against official publisher records and verified:

| Reference Key | Verified Full Authors | Title | Venue & Year | Identifier / DOI | Verification Source |
|---|---|---|---|---|---|
| **Deng et al. (2025)** | Qiqing Deng, Zhen Xu, Qihui Zhou, Yan Zhang | Cordon: Enhancing security through kernel-level control in containerized computing environments | *Computers & Security*, 151, 2025 | doi:10.1016/j.cose.2025.104644 | ScienceDirect / Elsevier; P019 in archive |
| **Hara & Sasabe (2024)** | Takanori Hara, Masahiro Sasabe | Practicality of in-kernel/user-space packet processing empowered by lightweight neural network and decision tree | *Computer Networks*, 243, 2024 | doi:10.1016/j.comnet.2024.110188 | ScienceDirect / Elsevier; P012 in archive |
| **Her et al. (2025)** | Jin Her, Jongseop Kim, Jinwoo Kim, Seungsoo Lee | An In-Depth Analysis of eBPF-Based System Security Tools in Cloud-Native Environments | *IEEE Access*, 13, 2025 | doi:10.1109/ACCESS.2025.3605432 | IEEE Xplore; P001 in archive |
| **Kim et al. (2025)** | Riyeong Kim, Jeongeun Ryu, Sumin Kim, Soomin Lee, Seongmin Kim | Detecting Cryptojacking Containers Using eBPF-Based Security Runtime and Machine Learning | *Electronics*, 14(6), 2025 | doi:10.3390/electronics14061208 | MDPI Open Access; P006 in archive |
| **Kostopoulos et al. (2026)** | Savvas Kostopoulos, Panagiotis Tsakonas, Evangelos K. Markakis | eBPF-based cybersecurity mechanisms: a systematic literature review | *International Journal of Information Security*, 25, 2026 | doi:10.1007/s10207-026-01326-x | Springer Nature; R050 in register |
| **Lu et al. (2025)** | Hui Lu, Xiaojiang Du, Dawei Hu, Shen Su, Zhi Tian | BPFGuard: Multi-Granularity Container Runtime Mandatory Access Control | *IEEE Transactions on Cloud Computing*, 2025 | doi:10.1109/TCC.2025.3551838 | IEEE Xplore; P020 in archive |
| **Patel et al. (2026)** | Jialin Patel, Lucas G. Buhl-Nielsen, Antoine Ghosn, Marios Kogias | KRAKENGUARD: Towards Fine-Grained eBPF Isolation | *USENIX NSDI 2026*, 2026 | Proceedings of USENIX NSDI '26 | USENIX; R041 in register |
| **Remya et al. (2025)** | S. Remya, Manu J. Pillai, B. Niranjan, P. M. Ajith Kumar, K. Merin Shaju, K. Dinoy Raj, Somula Ramasubbareddy, Yongyun Cho | CODAX: eBPF-Based Runtime Detection of Semantic DDoS Attacks in Linux Containers | *IEEE Access*, 13, 2025 | doi:10.1109/ACCESS.2025.3614389 | IEEE Xplore; P003 in archive |
| **Ryu et al. (2026)** | Jeongeun Ryu, Riyeong Kim, Soomin Lee, Sumin Kim, Hyunwoo Choi, Seongmin Kim | Hybrid Runtime Detection of Malicious Containers Using eBPF | *Computers, Materials & Continua*, 82(3), 2026 | doi:10.32604/cmc.2025.074871 | Tech Science Press; P018 in archive |
| **Soldani et al. (2023)** | David Soldani, Francesco Monaco, Petrit Nahi, Fulvio Risso, Mohamed F. Soliman, Luigi Di Giovanna, Sahand Jafarizadeh, Gaetano Ognibene, Hamideh Bour | eBPF: A New Approach to Cloud-Native Observability, Networking and Security for Current (5G) and Future Mobile Networks (6G and Beyond) | *IEEE Access*, 11, 2023 | doi:10.1109/ACCESS.2023.3281480 | IEEE Xplore; P007 in archive |
| **Sun & Su (2024)** | Haoran Sun, Zhendong Su | Validating the eBPF Verifier via State Embedding | *USENIX OSDI 2024*, 2024 | Proceedings of USENIX OSDI '24 | USENIX; R043 in register |
| **Taguchi et al. (2026)** | Hotaka Taguchi, Takanori Hara, Shoji Kasahara | Unsupervised Real-Time In-Kernel Intrusion Detection System Using Autoencoders and eBPF | *IEICE Transactions on Communications*, E109.B(1), 2026 | doi:10.23919/transcom.2025EBP3028 | J-STAGE / IEICE; P014 in archive |
| **Zehra et al. (2025)** | Sehar Zehra, Hassan Jamil Syed, Fahad Samad, Ummay Faseeha | DeSFAM: An Adaptive eBPF and AI-Driven Framework for Securing Cloud Containers in Real Time | *IEEE Access*, 13, 2025 | doi:10.1109/ACCESS.2025.3592192 | IEEE Xplore; P005 in archive |
| **Zhan et al. (2023)** | Mengqi Zhan, Yang Li, Huiran Yang, Guangxi Yu, Bo Li, Weiping Wang | Coda: Runtime Detection of Application-Layer CPU-Exhaustion DoS Attacks in Containers | *IEEE Transactions on Services Computing*, 16(4), 2023 | doi:10.1109/TSC.2022.3194266 | IEEE Xplore; P024 in archive |

---

## 7. Acceptance Criteria Assessment

| ID | Criterion | Final Status | Evidence / Reconciliation Result |
|---|---|---|---|
| **A1** | Repository state established | **PASS** | Default branch `main`, clean working tree, `HEAD` matching remote tracking at start. |
| **A2** | Experimental matrix validated | **PASS** | `validate_matrix.py` executed successfully; 350 files, 35 cells, 10 reps each verified. |
| **A3** | Revised analysis executed | **PASS** | `statistical_analysis.py` executed successfully; verified descriptive statistics and warnings. |
| **A4** | Derived outputs reconciled | **PASS** | Isolated recomputation produced 0 content diffs against committed CSV/JSON. 4.19 μs vs 4.238 μs discrepancy fully reconciled. |
| **A5** | Telemetry accounting audited | **PASS** | Counter accounting fully reconciled: 16,001 gen, 15,999 sub, 15,970 consumed, 0 drops, 0 gaps. Unconditional zero-loss claim removed. |
| **A6** | Detection metrics verified | **PASS** | Recomputed all cell classification metrics from raw JSON; matches processed tables exactly. |
| **A7** | Architecture claims verified | **PASS** | Manuscript explicitly separates Python software benchmarks, formula-derived latency estimates, and simulated policy states. |
| **A8** | Bibliography audited | **PASS** | All 14 citations verified with full authors, venues, years, and DOIs from official records. |
| **A9** | Manuscript corrected | **PASS** | Updated Abstract, Section 2, Section 5.2, Section 5.4, and References in `paper/MAIN_MANUSCRIPT.md`. |
| **A10** | Reproducibility assessed | **PASS** | Executed unit tests, software smoke test, and native BPF compilation; documented environmental boundaries. |
| **A11** | Git state verified | **PASS** | Audit executed strictly on `main`; changes prepared with minimal diff and no destructive operations. |
| **A12** | Handoff completed | **PASS** | Final audit report complete; handoff documentation updated. |

---

## 8. Disclosed Limitations and Submission-Readiness Statement

### 8.1 Disclosed Limitations
1. **Unprivileged Kernel Execution Boundary:** While BPF programs compile to valid eBPF bytecode, live tracepoint attachment in the testbed is blocked by `unprivileged_bpf_disabled=2`. Production deployment requires root privileges or dedicated capability delegation (`CAP_BPF`).
2. **Workload and Single-Node Scope:** Experiments were conducted on a single WSL2 development environment with micro-benchmark workloads. Multi-node Kubernetes clusters, production traffic variability, long-term concept drift, and advanced adversary evasion techniques were not evaluated.
3. **Software Arithmetic Benchmark:** Configuration D evaluates fixed-point Q16.16 arithmetic in user-space Python. It confirms the algorithmic feasibility of integer dot-products for eBPF verifier constraints, but does not represent a measured in-kernel probe execution speedup.
4. **Simulated Mitigation:** Configuration E measures Python policy state-machine transitions with synthetic verification sleep. Real cgroup v2 freeze or network policy actuation remains future engineering work.

### 8.2 Final Submission-Readiness Statement
**The manuscript is READY FOR SUBMISSION within the academic scope of the BACSE203 Computer Networks Case Study.** All empirical numbers are verified from raw evidence, all cited references are verified against authoritative publisher records, and all architectural boundaries and methodological limits are transparently disclosed.
