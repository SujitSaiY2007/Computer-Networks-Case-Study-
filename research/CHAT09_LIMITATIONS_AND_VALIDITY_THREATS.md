# Limitations and Threats to Validity: Comprehensive Analysis

**Project:** BACSE203 Computer Networks Case Study  
**Research Title:** eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs  
**Author:** Sujit Sai  
**Evaluation Scope:** Chat 08 Controlled Experiments (350 Runs) and Chat 09 Empirical Synthesis  
**Methodological Standard:** Four-Category Validity Framework (Internal, Construct, Statistical Conclusion, External)  

---

## 1. Introduction and Methodological Scope

In experimental systems research and empirical cybersecurity evaluations, rigorous scientific reporting mandates transparent disclosure of all methodological constraints, evaluation boundaries, and potential threats to validity (Wohlin et al. 2012). This document provides an exhaustive, critical analysis of the architectural, statistical, and operational limitations governing the empirical findings presented in Chat 08 and synthesized in Chat 09.

Threats to validity are classified across four formal dimensions:
1. **Internal Validity:** The extent to which observed variations in latency, throughput, memory, and detection can be definitively attributed to the tested architectural configurations rather than uncontrolled confounding factors.
2. **Construct Validity:** The degree to which measured operational metrics (e.g., peak RSS, tracepoint duration, burst recall) accurately reflect real-world cloud-native runtime security properties.
3. **Statistical Conclusion Validity:** The degree to which statistical tests, sample distributions, and inference methods support defensible conclusions regarding performance differences.
4. **External Validity:** The generalizability of the findings to diverse Linux distribution kernels, bare-metal enterprise cloud platforms, production multi-tenant Kubernetes clusters, and complex multi-stage adversarial attacks.

---

## 2. Internal Validity Threats

### 2.1 Environmental Noise and Host Scheduling Variations
- **Threat:** Background operating system processes, hypervisor scheduling, and WSL2 VM memory reclamation could introduce latency variations unrelated to the eBPF instrumentation.
- **Mitigation & Assessment:** 
  - Every experimental run was executed within dedicated, isolated Docker cgroup v2 containers pinned to specific CPU cores (`cpuset-cpus="2-3"`) with strict memory caps (`memory="512m"`).
  - All 35 experimental cells were repeated 10 times under deterministic sequential iteration with pseudo-random seed control ($S_{rep} = 42 + \text{rep}$).
  - However, because the testbed operates within an optimized WSL2 virtualization layer (`6.6.87.2-microsoft-standard-WSL2`) hosted on Windows 11, hypervisor-induced scheduling jitter cannot be entirely eliminated at the microsecond scale. While median latency trends are stable, tail latencies ($p_{95}$) reflect modest virtualization scheduling variance.

### 2.2 Cold-Start and JIT / Python Runtime Warm-Up
- **Threat:** In user-space Configuration C, initial Python interpreter startup, library dynamic linking, and scikit-learn module loading could artificially inflate user-space detection latencies during early runs.
- **Mitigation & Assessment:**
  - Prototype measurement harnesses separated daemon initialization and model deserialization from the active measurement loop ($T_0 \to T_5$).
  - Timing was recorded exclusively during steady-state container workload execution.
  - Nonetheless, user-space Python garbage collection cycles and thread context-switching introduce an inherent variance ($\sigma = 154.51\ \mu\text{s}$) that does not affect synchronous kernel-space execution.

### 2.3 Clock Domain Discrepancies and Timestamp Precision
- **Threat:** In-kernel eBPF programs capture timestamps via `bpf_ktime_get_ns()` (monotonic hardware clock), whereas user-space aggregation and mitigation scripts record timestamps via `clock_gettime(CLOCK_MONOTONIC)`.
- **Mitigation & Assessment:**
  - Both timing domains reference Linux `CLOCK_MONOTONIC`, guaranteeing identical tick frequencies and eliminating epoch drift.
  - Timing intervals for component breakdown ($T_1 - T_0$, $T_3 - T_2$, $T_5 - T_4$, $T_7 - T_6$) were calculated strictly within consistent domains, avoiding cross-clock subtraction artifacts.

---

## 3. Construct Validity Threats

### 3.1 Model Complexity and Representational Capacity
- **Threat:** Evaluating a 4-feature linear Logistic Regression classifier may not fully represent state-of-the-art intrusion detection algorithms (such as Deep Neural Networks, Autoencoders, or Gradient Boosted Trees).
- **Construct Reality:**
  - The linear model was chosen deliberately as the **maximum complexity threshold** currently verifiable within the Linux kernel BPF verifier without out-of-tree patches or specialized floating-point helper modules.
  - While this design rigorously answers the architectural question regarding **fixed-point in-kernel inference speedup (RQ1)**, it does not represent the full detection capacity of multi-layer user-space deep learning models. The 40x speedup observed is therefore specific to linear architectures.

### 3.2 Approximation of System Call Failure Telemetry
- **Threat:** The fourth feature in the model vector, `failed_operation_count`, was approximated at tracepoint entry (`sys_enter_*`) as an operational frequency indicator rather than capturing the post-syscall exit return code (`sys_exit_*`).
- **Construct Reality:**
  - Attaching probes exclusively to `sys_enter` tracepoints minimized probe attachment overhead by 50% (avoiding paired exit probes), which served the telemetry overhead evaluation (RQ2).
  - However, true system call failure detection requires pairing with `sys_exit` to inspect negative error codes (e.g., `-EACCES`, `-ENOENT`). In our prototype, `failed_operation_count` was proxied by suspicious target access frequency. This construct simplification, while transparently reported, limits true semantic error monitoring.

### 3.3 Synthetic Workload Burst Realism
- **Threat:** Synthetic workloads ($B1$–$B4$, $A1$–$A3$) may not capture the multi-dimensional nuances of enterprise cloud applications or sophisticated Advanced Persistent Threats (APTs).
- **Construct Reality:**
  - Synthetic bursts were engineered to model specific behavioral archetypes: microservice API serving ($B2$), high-churn build compilation ($B3$), malicious process execution ($A1$), sensitive file exfiltration ($A2$), and network port bursts ($A3$).
  - While highly repeatable and isolated, synthetic bursts represent concentrated, short-duration (1–3 second) stress patterns rather than stealthy, low-and-slow exfiltration campaigns that evade rate-based detection over weeks.

---

## 4. Statistical Conclusion Validity Threats

### 4.1 Repeated Run Sample Size ($n = 10$ per Cell)
- **Threat:** Conducting 10 repetitions per configuration/workload cell ($N = 350$ total runs) might be considered a modest sample size for high-dimensional distribution modeling.
- **Statistical Defense:**
  - In deterministic systems benchmarking where software and hardware environments are pinned, $n = 10$ repetitions per cell is standard and sufficient to verify normality via Shapiro-Wilk testing and compute stable non-parametric percentiles (median, IQR, $p_{95}$).
  - For cross-configuration comparisons, pooling across all 7 workloads yielded $n = 70$ observations per configuration, providing high statistical power ($>0.99$ at $\alpha = 0.001$) for paired Wilcoxon and $t$-tests ($p < 10^{-11}$).
  - We explicitly refrain from claiming micro-level distribution properties beyond the verified percentiles.

### 4.2 Non-Normal Latency Distributions
- **Threat:** Latency measurements in computing systems are inherently right-skewed and violate Gaussian normality assumptions.
- **Statistical Defense:**
  - Standard parametric metrics (mean, standard deviation) are reported alongside non-parametric metrics (median, interquartile range, 95th percentile).
  - Hypothesis testing utilized the non-parametric **Wilcoxon signed-rank test** as the primary decision criterion, supplemented by paired $t$-tests and Cohen's $d$ effect sizes strictly for completeness.

---

## 5. External Validity Threats and Generalizability Boundaries

### 5.1 Virtualized Host vs. Bare-Metal Multi-Tenant Kubernetes
- **Boundary:** All experiments were conducted on a single virtualized host running WSL2 Linux kernel 6.6 with isolated Docker cgroups, rather than a distributed multi-node Kubernetes cluster.
- **Generalizability:**
  - Low-level eBPF kernel mechanics (raw tracepoints, `BPF_MAP_TYPE_RINGBUF`, Q16.16 arithmetic, BPF verifier checks) are identical across WSL2 Linux and bare-metal Linux kernels.
  - However, multi-node network fabric latency (e.g., Calico/Cilium VXLAN overlays), distributed etcd state synchronization, and cluster-wide pod autoscaling are not captured in a single-host container testbed.

### 5.2 Kernel Version and Architecture Portability
- **Boundary:** Evaluation was restricted to x86_64 architecture on Linux kernel 6.6.y.
- **Portability:**
  - Systems utilizing older Linux kernels ($< 5.8$) lack the modern `BPF_MAP_TYPE_RINGBUF` and must revert to legacy perf event buffers, which exhibit known CPU-contention and event-dropping vulnerabilities under burst loads (Miano et al. 2022).
  - Different Linux kernel versions may apply varying BPF verifier complexity heuristics or instruction limits (e.g., 1 million instructions vs. 4096 instructions on legacy kernels), potentially impacting the verifiability of fixed-point arithmetic loops.

### 5.3 Workload Churn and Generalization Deficit (The $B3$ Anomaly)
- **Deficit:** The observed 80% false alarm rate on Workload $B3$ demonstrates that linear rate-based models do not generalize across distinct operational profiles within the same container cluster.
- **Boundary:**
  - Models trained on low-churn microservices cannot be deployed naively into CI/CD build environments without retraining or hierarchical contextualization.
  - This limitation is not a defect of the experimental harness, but an empirical finding that invalidates claims of universal plug-and-play machine learning for cloud-native runtime security.

---

## 6. Comprehensive Validity Matrix

**Table 1: Summary of Validity Threats, Mitigations, and Disclosed Boundaries**

| Validity Dimension | Identified Threat / Limitation | Implemented Mitigation / Treatment | Residual Boundary / Academic Status |
| :--- | :--- | :--- | :--- |
| **Internal** | Virtualization scheduling noise | Cgroup isolation, CPU core pinning, 10 deterministic seed repetitions | Modest tail latency ($p_{95}$) variance preserved; median trends robust |
| **Internal** | Python runtime & GC warm-up | Separation of daemon boot from active timing loop | User-space latency exhibits higher standard deviation than kernel |
| **Internal** | Timestamp cross-domain drift | Unified reference to `CLOCK_MONOTONIC` | Component intervals calculated strictly within consistent domains |
| **Construct** | In-Kernel LR in matrix runs | Q16.16 arithmetic benchmarked in Python harness | In-kernel feasibility proven via Gate G; matrix measured arithmetic speedup |
| **Construct** | Detection latency computation | Sum of components plus assumed transport constants | Explicitly reported as formula-derived estimate, not hardware clock |
| **Construct** | Staged mitigation & rollback | Policy engine state transitions with simulated sleep | Measures decision-engine latency; active kernel cgroup freeze unexecuted |
| **Construct** | Tracepoint entry error approximation | Transparently documented as operational frequency indicator | Does not capture post-syscall exit return codes (`-EACCES`) |
| **Construct** | Synthetic burst workload realism | Standardized process, file, and socket burst generators | Captures short burst archetypes; does not model stealthy slow APTs |
| **Statistical** | Modest cell repetitions ($n = 10$) | Pinned deterministic environment; pooled comparisons ($n = 70$) | Micro-level distributions not inferred; percentiles reported |
| **Statistical** | Skewed latency distributions | Non-parametric reporting (median, IQR, Wilcoxon tests) | Parametric tests reported only as secondary effect size indicators |
| **External** | Single-host virtualized testbed | Native Linux kernel primitives audited and verified | Multi-node Kubernetes network overlay latencies not evaluated |
| **External** | High false positives on benign churn ($B3$) | Rigorously documented, analyzed, and synthesized against literature | Disproves universal applicability of naive linear ML classifiers |

---

## 7. Conclusion

By systematically disclosing these internal, construct, statistical, and external validity boundaries, this study preserves absolute research integrity. Rather than presenting the prototype as a flawless, production-ready intrusion defense system, our findings provide a verified, empirical foundation that clearly defines the capabilities, speedups, expressiveness limits, and operational vulnerabilities of eBPF-assisted machine learning architectures.
