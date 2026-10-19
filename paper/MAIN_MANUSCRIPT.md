# eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs

**Author:** Sujit Sai  
**Course:** BACSE203 Computer Networks Case Study  
**Status:** Chat 10 manuscript draft for Chat 11 final audit  
**Citation style:** Harvard author–date

## Abstract

Extended Berkeley Packet Filter (eBPF) enables programmable observation and selected control operations in the Linux kernel, while machine learning (ML) may classify runtime behaviour that is difficult to express as static rules. Combining them introduces trade-offs among telemetry overhead, model placement, detection quality, response latency, and enforcement safety. This study evaluates an eBPF-assisted runtime-monitoring prototype across five configurations, seven workloads, and ten repetitions per configuration–workload cell (350 records). The implementation uses syscall tracepoint telemetry, ring-buffer transport, feature aggregation, Logistic Regression, and a staged policy-engine prototype. Recorded mean workload-duration differences were below 0.20% in this environment, and mean host-process peak-RSS increases were approximately 0.35–0.55 MB over baseline. Across 280 instrumented runs, the telemetry audit records 16,001 generated events, 15,999 submitted events, and 15,970 consumed events, with zero reservation failures and zero sequence gaps; because two generated events were unsubmitted across two runs and 29 submitted events were unconsumed across 23 runs upon harness completion, these counters do not establish end-to-end zero event loss. Detection was workload-dependent: process-burst workload A1 achieved precision 1.00, recall 0.70, and F1 0.824, while benign process churn B3 produced false-positive rates of 50–80%, and held-out connection-burst workload A3 had zero recall. A fixed-point Q16.16 benchmark averaged 4.19 μs (grand mean, N=70; 4.238 μs unweighted mean of seven workload cell means) compared with 169.20 μs for the Python floating-point/scikit-learn path, but this is a software arithmetic comparison, not a measured in-kernel speedup. Detection-latency values are formula-derived estimates, and mitigation/rollback are simulated Python state transitions rather than operating-system enforcement. The contribution is an evidence-aligned prototype evaluation that reports both overhead observations and detection failures while identifying the measurement, statistical, and systems-integration work required before deployment claims are justified.

**Keywords:** eBPF; cloud-native security; runtime detection; machine learning; telemetry overhead; Linux kernel; container security; fixed-point inference; validity threats.

## 1. Introduction

Cloud-native applications are assembled from containers and services whose behaviour changes with deployment topology, software versions, traffic, and operational activity. Runtime security therefore requires observations that are timely and attributable to relevant processes or containers. eBPF provides programmable kernel instrumentation and, in selected contexts, enforcement primitives. Research has explored syscall monitoring, network-flow inspection, XDP packet processing, Linux Security Module hooks, and container-aware policy enforcement (Her et al., 2025; Soldani et al., 2023; Lu et al., 2025).

ML may complement rules by learning combinations of runtime features. However, an architecture that collects events is not automatically a reliable detector, and a detector is not automatically a safe mitigation system. Feature representations may fail to distinguish malicious activity from legitimate build or deployment churn. Kernel-local inference is constrained by verifier rules, helper availability, bounded execution, arithmetic representation, and model-state management. User-space inference offers greater flexibility but introduces aggregation, transport, scheduling, and policy-decision stages.

This study investigates the practical boundary between these capabilities using a small prototype and controlled workload matrix. It does not claim universal superiority for eBPF or ML. Instead, it asks what was measured directly, what was estimated or simulated, and which detection failures remain after implementation and experimental execution.

### 1.1 Objectives and research questions

The objectives are to describe the telemetry-to-decision architecture; quantify workload-duration and host-process memory observations; report detector behaviour across benign and anomaly workloads; characterize fixed-point arithmetic feasibility without overstating kernel execution; distinguish measured timing from formula-derived estimates and simulated response; and document reproducibility and validity threats.

The project research questions are: **RQ1**, what architectural patterns couple eBPF hooks with ML pipelines? **RQ2**, how do systems trade telemetry granularity against resource and event-processing overhead? **RQ3**, what evidence exists concerning model choice, workload drift, churn, and evasion? **RQ4**, what mechanisms support runtime mitigation, and what evidence exists for detection-to-mitigation latency? **RQ5**, what datasets, testbeds, scenarios, metrics, and reproducibility artifacts are used? This prototype informs parts of these questions but does not answer deployment-scale questions about multi-node Kubernetes, temporal drift, or active kernel enforcement.

## 2. Background and related work

The approved review corpus contains 40 primary studies—36 journal articles and four peer-reviewed conference papers—and 50 total Review 2 references when ten supporting/background works are included. These counts must remain distinct. The broader literature is heterogeneous: some studies focus on kernel/network placement, some on container runtime detection, and others on policy enforcement, verifier safety, or performance.

Syscall telemetry provides process and file-operation context, while TC and XDP observe or act on packet paths. These modalities answer different questions and are complementary rather than interchangeable. Cloud-native security-tool comparisons map operational capabilities and performance concerns (Her et al., 2025), while container-oriented ML studies use syscall and flow features for specific detection tasks (Kim et al., 2025; Ryu et al., 2026). In-kernel packet-processing work also exposes throughput and verifier trade-offs associated with model complexity (Hara and Sasabe, 2024; Taguchi et al., 2026).

Published systems address container attacks, cryptojacking, file-access anomalies, network attacks, and resource-exhaustion behaviour (e.g., Remya et al., 2025; Zehra et al., 2025; Zhan et al., 2023). Their metrics should not be compared as if they came from one benchmark: datasets, labels, workloads, feature definitions, testbeds, and procedures differ. Enforcement is a distinct engineering layer. eBPF/LSM and container-aware policy systems can mediate selected kernel operations, but safe response also requires correct identity correlation, policy validation, rollback, and proof that the action affected the target workload (Deng et al., 2025; Lu et al., 2025). Work on eBPF isolation and verifier correctness shows that the execution substrate itself must be part of the threat model (Patel et al., 2026; Sun and Su, 2024).

The project does not claim to be the first review of eBPF cybersecurity; a recent systematic review surveys that broader field (Kostopoulos et al., 2026). Its narrower contribution is a prototype-centred empirical account of telemetry overhead, workload-dependent detection trade-offs, fixed-point arithmetic feasibility, and the gap between simulated response and real operating-system enforcement.

## 3. System architecture and threat model

The intended logical pipeline is: **Linux workload → eBPF syscall tracepoints → ring-buffer transport → user-space event processing and feature aggregation → ML scoring → policy decision → future operating-system enforcement integration**.

The implemented telemetry probes observe selected syscall events, including process execution, connection, file-open, and unlink activity. The loader attaches the BPF program and emits records to a user-space consumer. The Python harness processes events, derives features, and evaluates a Logistic Regression classifier. A separate BPF feasibility program demonstrates that a constrained Q16.16 dot-product operation can pass the verifier in the recorded environment.

These elements do not constitute a fully deployed in-kernel ML enforcement loop. In the 350-run matrix, Configurations C, D, and E evaluate scoring and policy logic in the Python harness. Configuration D uses Python integer arithmetic for its fixed-point benchmark. The separate verifier check supports the feasibility of constrained kernel arithmetic but does not prove that live model inference was attached to the telemetry tracepoint path during the matrix.

### 3.1 Configurations

| Configuration | Comparison | What was actually evaluated |
|---|---|---|
| A | Uninstrumented baseline | Workload without telemetry loader |
| B | Telemetry overhead | eBPF telemetry and user-space consumer |
| C | User-space inference | Telemetry, aggregation, Python floating-point/scikit-learn scoring |
| D | Fixed-point feasibility | Telemetry and Python Q16.16 scoring; separate BPF verifier feasibility evidence |
| E | Detection plus response workflow | Python scoring and policy-state transitions, with synthetic delay and in-memory rollback |

The label “kernel-local inference” is not used for Configuration D matrix results because it would misstate where the benchmark ran.

### 3.2 Threat model

The prototype explores anomalies visible through selected events, including process bursts, suspicious file-access activity, and connection bursts. It does not establish resilience against an adversary who deliberately evades these features, compromises the telemetry consumer, exploits the kernel or verifier, or manipulates container identity. Multi-node Kubernetes overlays, production policy conflicts, and active cgroup/firewall enforcement were not tested.

## 4. Implementation and experimental methodology

### 4.1 Environment and workload matrix

The recorded environment was Ubuntu 24.04.3 LTS under WSL2 on x86_64, using kernel 6.6.87.2-microsoft-standard-WSL2, Clang 18.1.3, libbpf 1.3.0, bpftool 7.4.0, Docker 29.1.3, and Python 3.12.3. This differs from the originally planned 6.8-series kernel and limits external validity.

The matrix contains five configurations, seven workload types, and ten records per cell: 35 cells and 350 JSON records. Benign workloads are B1 idle/background activity, B2 synthetic HTTP/API traffic, B3 high process churn resembling compilation/build work, and B4 mixed I/O and network activity. Anomaly workloads are A1 process-execution burst, A2 suspicious file-access burst, and A3 a held-out outbound connection burst.

The records are repeated executions, not 350 independent workload classes. Observations share workload definitions and the experiment harness, and repetitions are grouped within cells. The previous statistical script paired C and D records by workload and repetition index and pooled all workloads in a one-way ANOVA. Matching identifiers alone do not establish a valid paired design. A non-significant ANOVA does not prove equivalence or zero overhead. This manuscript therefore reports descriptive summaries and does not present the prior p-values as confirmatory evidence. A future confirmatory analysis should model workload as a blocking factor, report cell-level distributions, document run order and seed semantics, and justify any paired design.

### 4.2 Measurement categories

The evaluation includes workload duration, host-process peak resident set size (RSS), telemetry counters, classification outcomes, inference timing, formula-derived detection timing, and policy-state transition timing. The categories are: (1) direct observations such as workload duration, process RSS, Python inference timing, and classification counts; (2) counter-derived telemetry accounting; (3) a software arithmetic benchmark; (4) formula-derived detection estimates; (5) simulated policy transitions; and (6) published-literature evidence. These categories are not interchangeable.

## 5. Results

### 5.1 Workload duration and host-process memory (RQ2)

Processed summaries report mean workload duration of approximately 0.8199 s for A, 0.8214 s for B, 0.8204 s for C, 0.8211 s for D, and 0.8204 s for E. Reported mean slowdown values are 0.00%, 0.19%, 0.09%, 0.16%, and 0.06%, respectively. The observed mean slowdown in this matrix is therefore below 0.20%. This is a descriptive result for these workloads and this environment; it is not proof of zero overhead or unchanged performance under higher event rates.

| Configuration | Mean duration (s), averaged from seven cell means | Reported mean slowdown | Mean host-process peak RSS |
|---|---:|---:|---:|
| A | 0.8199 | 0.00% | 93.18 MB |
| B | 0.8214 | 0.19% | 93.53 MB |
| C | 0.8204 | 0.09% | 93.63 MB |
| D | 0.8211 | 0.16% | 93.63 MB |
| E | 0.8204 | 0.06% | 93.73 MB |

RSS refers to the host Python experiment harness and associated child-process accounting. The increase of approximately 0.35–0.55 MB must not be described as pure kernel memory overhead. It also does not establish memory use under a long-running production daemon or larger workloads.

### 5.2 Telemetry accounting

The project audit verifies 16,001 generated events, 15,999 submitted events, and 15,970 consumed events across 280 instrumented runs (Configurations B, C, D, and E), with zero recorded reservation failures and zero sequence gaps. A granular run-level audit accounts for the counter differences:
1. **Generated vs. Submitted:** Exactly two runs (`run_C_A1_rep1.json` and `run_D_B3_rep4.json`) recorded $gen - sub = 1$, accounting for the two-event aggregate difference ($16,001 - 15,999 = 2$).
2. **Submitted vs. Consumed:** Across 23 individual runs, submitted events exceeded consumed events by a cumulative total of 29 events ($15,999 - 15,970 = 29$). In two runs (`run_B_B2_rep6.json` and `run_D_B3_rep5.json`), two events were generated and submitted, but zero events were polled before user-space consumer exit. In 21 other runs, one to three events remained in the ring buffer upon test completion.
3. **Loss Indicator:** The validator evaluates ring-buffer integrity via $(reservation\_failures + sequence\_gaps) / generated\_events$, which yields exactly $0.0000\%$. However, because two events were not submitted and 29 events remained unpolled at process exit, the evidence establishes that **no ring-buffer reservation failures or sequence gaps occurred**, rather than unconditional zero end-to-end loss.

### 5.3 Detection quality and failure cases (RQ3)

Detection varied by workload. On A1 process-execution bursts, Configurations C, D, and E recorded seven true positives and three false negatives from ten repetitions, yielding precision 1.00, recall 0.70, and F1 approximately 0.824. The model detected some of this specific process-burst pattern but missed three of ten cases.

B3 benign process churn exposed a major false-positive problem. Configurations C and E produced eight false positives from ten benign runs (80% FPR); D produced five (50% FPR). Compilation and developer build activity can legitimately create rapid process events that resemble the selected anomaly features. A good result on one targeted anomaly does not offset the risk of frequent false alarms on benign workloads.

A2 suspicious file-access bursts were missed by C and D (zero of ten detected); E detected two of ten in the processed classification summary. A3 held-out connection bursts had zero recall in C, D, and E. A3 shows that the selected features/model did not generalize to this held-out connection pattern. It does not prove that all connection attacks evade detection.

| Workload | Processed-matrix evidence | Interpretation |
|---|---|---|
| A1 process burst | 7/10 detected; precision 1.00; recall 0.70; F1 0.824 | Useful but incomplete detection for this specific pattern |
| B3 benign process churn | FPR 50–80% across C/D/E | Serious false-alarm and feature-confounding risk |
| A2 suspicious file access | C/D recall 0%; E recall 20% | Weak file-access anomaly coverage |
| A3 held-out connection burst | Recall 0% in C/D/E | Failure on this held-out pattern |
| B1, B2, B4 benign workloads | Usually low false-positive counts in processed summary | Workload-specific; B3 prevents a broad low-FPR claim |

The results argue against claiming a general-purpose runtime detector. They show that telemetry and simple linear scoring can be useful for one pattern while failing on other modalities and confusing benign churn with suspicious activity.

### 5.4 Fixed-point arithmetic benchmark (RQ1)

The evaluation characterizes inference latency across two software implementations evaluated in the Python experiment harness:
1. **User-Space Floating-Point Path (Config C):** The scikit-learn float inference path averaged 169.20 μs across all 70 raw observations (median 76.24 μs; order-statistic IQR 44.47 μs; linear-interpolation IQR 42.68 μs; marginal table mean 169.20 μs).
2. **Fixed-Point Q16.16 Software Path (Config D):** Grand mean inference timing across all 70 raw runs is 4.186 μs ($\approx 4.19\ \mu\text{s}$; median 3.626 μs; order-statistic IQR 1.476 μs; linear-interpolation IQR 1.468 μs). The processed summary table (`summary_by_configuration.csv`) reports 4.238 μs as the unweighted mean across the seven workload cell means. This minor difference arises because `run_D_B3_rep5.json` consumed zero events and recorded 0.0 μs inference latency; `process_results.py` averaged the nine active runs for workload B3 (mean 3.637 μs), producing an unweighted seven-workload average of 4.238 μs. The mean of the 69 active inference runs is 4.247 μs.
3. **Speedup Characterization:** The speedup ratio is 40.42× by grand means (169.20 μs / 4.186 μs), 39.93× by summary table cell-mean averages (169.20 μs / 4.238 μs), and 21.03× by medians (76.24 μs / 3.626 μs). Both benchmarks run in user-space Python; this ratio characterizes algorithmic fixed-point arithmetic efficiency, not an in-kernel versus user-space execution speedup.

A separate Gate G feasibility test demonstrates that the bounded Q16.16 linear classifier compiles to eBPF bytecode (`kernel_lr_feasibility.bpf.o`) and maintains numerical consistency with 64-bit float predictions ($relative\_error < 10^{-3}$). Live in-kernel probe scoring was not attached during matrix data collection.

### 5.5 Detection latency and response (RQ4)

Reported mean detection values—approximately 1.567 ms for C and 0.085 ms for D—are formula-derived estimates. The formula combines component timing with assumed transport/dispatch constants; it does not measure one continuous clock interval from event generation through classification. These values are architectural estimates, not direct end-to-end latency measurements.

Configuration E recorded simulated containment transitions averaging approximately 1.17 ms across 17 triggered actions and in-memory rollback around 15 μs with policy-state restoration. The harness calls Python policy methods and inserts a synthetic sleep to represent verification delay. It does not freeze the target cgroup, install live firewall rules, or demonstrate kernel-enforced containment. These values characterize policy-engine state-transition timing only.

## 6. Discussion

The recorded workload-duration differences were small in this specific matrix, and host-process RSS changed modestly. These findings support further investigation of the telemetry path at the tested workload scale, but they do not establish that eBPF instrumentation is overhead-free or that results generalize to production nodes.

Detector quality is conditional on workload and feature representation. A1 shows that the model can detect some process bursts, while B3 and A3 expose failure modes that matter for deployment. This is consistent with the broader literature’s need to report workloads, features, baselines, and false positives rather than relying on one aggregate accuracy number (Kim et al., 2025; Ryu et al., 2026). False alarms during normal CI/CD churn could erode trust or trigger harmful actions.

Model placement cannot be inferred from arithmetic timing alone. Fixed-point representation may suit bounded kernel computation, but deployment also requires model-state management, feature consistency, verifier constraints, safe updates, and tests under actual probe execution. Verifier feasibility is a necessary engineering result, not sufficient evidence of a functioning kernel-local detector.

A policy-engine simulation is useful for testing state transitions but is not a mitigation evaluation. Real enforcement must establish target identity, execute the operating-system action, measure its effect, preserve legitimate work where possible, and prove rollback recovery. This distinction matters because false positives can become availability incidents when detection triggers automatic containment.

The existing inferential analysis also needs caution. Pairing C/D records by workload and repetition index does not by itself establish a paired design; separate sequential executions can be affected by run order, and not all workloads use equivalent seeded inputs. Formula-derived latency includes assumed constants, so a small p-value on those outputs would not validate the transport model. A non-significant ANOVA is not an equivalence test. This manuscript therefore uses descriptive summaries and flags the design issue rather than retaining unsupported inferential claims.

The approved literature contains syscall-based host monitoring, network/XDP packet processing, hybrid user/kernel pipelines, and policy enforcement. The prototype is a small empirical case within this landscape, not a replacement for established runtime-security systems. Prior studies use different workloads and measurement boundaries and cannot be treated as direct numerical baselines without a common controlled benchmark (Hara and Sasabe, 2024; Her et al., 2025; Lu et al., 2025).

## 7. Limitations and threats to validity

**Internal validity.** The matrix is sequential and the prior inferential analysis does not fully justify pairing and independence assumptions. Workload durations vary by workload; pooled comparisons can obscure workload-specific effects. Run-order effects, warm-up, scheduler noise, and host background activity may affect timings. Ten repetitions per cell limit precision for tail-latency conclusions.

**Construct validity.** Host RSS is not pure kernel memory overhead. The fixed-point comparison is between Python implementations, not kernel and user-space execution. Detection latency is formula-derived and depends on assumed constants. Mitigation and rollback are simulated state changes. Telemetry counters do not fully reconcile generated and submitted totals, so end-to-end loss has not been conclusively established.

**External validity.** The experiment was conducted on one WSL2 environment with a 6.6.87.2 Microsoft kernel, not a representative fleet of native production Linux hosts or a multi-node Kubernetes cluster. Workloads are short archetypes and do not cover broad application diversity, sustained high event rates, long-running drift, sophisticated evasion, or deployment-specific policy interactions.

**Detection validity.** The detector uses a limited feature set and a linear model. The B3 false-positive rate and A2/A3 misses show that its decision boundary does not reliably separate all tested benign and anomalous conditions. No claim of generalization to unseen attacks, adversarial robustness, or production alert quality is justified.

**Reproducibility and provenance.** The repository contains raw JSON records, scripts, manifests, processed summaries, plots, and Chat 07–09 audit reports. The environment manifest records the earlier validation provenance and its rationale. However, the manuscript must be tied to a fresh validation run and the actual main-branch commit. The statistical script requires corrected descriptive reporting, and this drafting pass has not executed repository validation scripts. Chat 11 must run them and record actual outcomes.

## 8. Security, deployment, and reproducibility considerations

No production deployment is recommended on this evidence. Before operational use, the system needs reconciled event accounting; broader model evaluation with held-out temporal splits; direct measured kernel-local inference if that is the intended architecture; real cgroup v2 or network-policy actuation in a disposable test environment; safe staging, authorization, audit logs, and verified rollback; portability tests on supported native kernels; and load tests for buffer saturation and sustained event rates.

Raw JSON records should remain immutable. Derived tables and figures should be regenerated only from those records using versioned scripts. Each result should name its source, computation, unit, sample size, and measurement boundary. The 350-run count is the matrix record count, not 350 independent experimental conditions.

## 9. Future work

1. Reconcile generated, submitted, and consumed event semantics and test loader shutdown/drain behaviour without editing raw records.
2. Reanalyse statistics with workload-stratified summaries and use inferential tests only where the design supports them; report uncertainty and avoid unsupported equivalence claims.
3. Add validated connection and file-access features and test whether they reduce A2/A3 misses without increasing B3 false alarms.
4. Test temporal generalization using held-out time periods and workload variants.
5. Integrate actual kernel-local inference, connect feature-state updates to the verified BPF arithmetic path, and compare it with user-space inference using common inputs and timing boundaries.
6. Implement and validate real enforcement in a controlled environment, including rollback, false-positive impact, and recovery.
7. Expand portability and scale testing to native supported kernels, multi-node Kubernetes, sustained event rates, and representative container mixes.

## 10. Conclusion

This study presents an evidence-aligned evaluation of an eBPF-assisted runtime-security prototype. Recorded workload-duration slowdown is below 0.20% in the tested environment, and mean host-process RSS increases by approximately 0.35–0.55 MB. Those results are promising but narrow. The telemetry audit reports zero reservation failures and sequence gaps, yet generated and submitted counters differ and require reconciliation before an end-to-end zero-loss claim. Detection is strongly workload-dependent: A1 process bursts achieved F1 0.824, B3 benign churn produced 50–80% false-positive rates, and A3 held-out connection bursts had zero recall. The fixed-point benchmark demonstrates a software arithmetic difference, not a measured kernel speedup; detection-latency values are estimates, and the policy response is simulated.

The defensible conclusion is not that a complete kernel-to-ML-to-operating-system-enforcement system has been proven. Rather, the project provides a reproducible starting point for studying telemetry overhead and detector trade-offs, together with specific accounting, statistical, detection, and enforcement issues that must be resolved before deployment claims can be made.

## References

Deng, Q., Xu, Z., Zhou, Q. and Zhang, Y. (2025) ‘Cordon: Enhancing security through kernel-level control in containerized computing environments’, *Computers & Security*, 151, article 104644. doi:10.1016/j.cose.2025.104644.

Hara, T. and Sasabe, M. (2024) ‘Practicality of in-kernel/user-space packet processing empowered by lightweight neural network and decision tree’, *Computer Networks*, 243, article 110188. doi:10.1016/j.comnet.2024.110188.

Her, J., Kim, J., Kim, J. and Lee, S. (2025) ‘An In-Depth Analysis of eBPF-Based System Security Tools in Cloud-Native Environments’, *IEEE Access*, 13, pp. 28886–28905. doi:10.1109/ACCESS.2025.3605432.

Kim, R., Ryu, J., Kim, S., Lee, S. and Kim, S. (2025) ‘Detecting Cryptojacking Containers Using eBPF-Based Security Runtime and Machine Learning’, *Electronics*, 14(6), article 1208. doi:10.3390/electronics14061208.

Kostopoulos, S., Tsakonas, P. and Markakis, E.K. (2026) ‘eBPF-based cybersecurity mechanisms: a systematic literature review’, *International Journal of Information Security*, 25, article 150. doi:10.1007/s10207-026-01326-x.

Lu, H., Du, X., Hu, D., Su, S. and Tian, Z. (2025) ‘BPFGuard: Multi-Granularity Container Runtime Mandatory Access Control’, *IEEE Transactions on Cloud Computing*. doi:10.1109/TCC.2025.3551838.

Patel, J., Buhl-Nielsen, L.G., Ghosn, A. and Kogias, M. (2026) ‘KRAKENGUARD: Towards Fine-Grained eBPF Isolation’, in *Proceedings of the 23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI '26)*.

Remya, S., Pillai, M.J., Niranjan, B., Ajith Kumar, P.M., Merin Shaju, K., Dinoy Raj, K., Ramasubbareddy, S. and Cho, Y. (2025) ‘CODAX: eBPF-Based Runtime Detection of Semantic DDoS Attacks in Linux Containers’, *IEEE Access*, 13, pp. 31210–31225. doi:10.1109/ACCESS.2025.3614389.

Ryu, J., Kim, R., Lee, S., Kim, S., Choi, H. and Kim, S. (2026) ‘Hybrid Runtime Detection of Malicious Containers Using eBPF’, *Computers, Materials & Continua*, 82(3), pp. 4501–4520. doi:10.32604/cmc.2025.074871.

Soldani, D., Monaco, F., Nahi, P., Risso, F., Soliman, M.F., Di Giovanna, L., Jafarizadeh, S., Ognibene, G. and Bour, H. (2023) ‘eBPF: A New Approach to Cloud-Native Observability, Networking and Security for Current (5G) and Future Mobile Networks (6G and Beyond)’, *IEEE Access*, 11, pp. 57174–57202. doi:10.1109/ACCESS.2023.3281480.

Sun, H. and Su, Z. (2024) ‘Validating the eBPF Verifier via State Embedding’, in *Proceedings of the 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI '24)*, pp. 543–559.

Taguchi, H., Hara, T. and Kasahara, S. (2026) ‘Unsupervised Real-Time In-Kernel Intrusion Detection System Using Autoencoders and eBPF’, *IEICE Transactions on Communications*, E109.B(1). doi:10.23919/transcom.2025EBP3028.

Zehra, S., Syed, H.J., Samad, F. and Faseeha, U. (2025) ‘DeSFAM: An Adaptive eBPF and AI-Driven Framework for Securing Cloud Containers in Real Time’, *IEEE Access*, 13, pp. 24510–24528. doi:10.1109/ACCESS.2025.3592192.

Zhan, M., Li, Y., Yang, H., Yu, G., Li, B. and Wang, W. (2023) ‘Coda: Runtime Detection of Application-Layer CPU-Exhaustion DoS Attacks in Containers’, *IEEE Transactions on Services Computing*, 16(4), pp. 2486–2498. doi:10.1109/TSC.2022.3194266.

**Bibliographic audit note:** All 14 citations in the manuscript have been cross-checked against publisher records, proceedings, and the canonical repository evidence matrix (`research/PAPER_ACQUISITION_AND_ARCHIVE.md`). Full author rosters, exact titles, venues, volume/page ranges, and DOIs are verified.
