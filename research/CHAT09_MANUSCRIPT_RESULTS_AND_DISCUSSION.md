# Manuscript Results and Discussion: Empirical Evaluation and Literature Synthesis

**Document Class:** Academic Manuscript Component (Results & Discussion Sections)  
**Project:** BACSE203 Computer Networks Case Study  
**Title:** eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs  
**Author:** Sujit Sai  
**Citation Style:** Harvard Author-Date System  
**Evidence Baseline:** Chat 08 Controlled Experiment Execution (350 Runs, 35 Cells, 10 Repetitions)  
**Literature Base:** 40 Primary Studies (36 Journals, 4 Peer-Reviewed Conferences) + 10 Supporting Works  

---

## 1. Experimental Methodology and Evaluation Boundaries

### 1.1 Experimental Objective and Controlled Matrix
To address the five research questions formulated for cloud-native runtime security architectures, we evaluated a fully operational, kernel-integrated prototype across five architectural configurations ($\mathcal{C} \in \{A, B, C, D, E\}$) and seven standardized cloud-native workload conditions ($\mathcal{W} \in \{B1, B2, B3, B4, A1, A2, A3\}$). The full matrix comprises 35 distinct experimental cells, each subjected to 10 independent, sequentially isolated experimental repetitions with dedicated cgroup v2 namespaces and deterministic pseudo-random seeds ($S_{rep} = 42 + \text{rep}$), yielding $N = 350$ complete execution records.

The five evaluated architectural configurations represent distinct operational paradigms along the telemetry-to-enforcement pipeline:
1. **Configuration A (Uninstrumented Baseline):** Clean container execution without eBPF probes or user-space daemon overhead, providing the reference measurement for application throughput and host resource utilization.
2. **Configuration B (Telemetry Only):** Kernel-space telemetry extraction via raw tracepoints (`sys_enter_execve`, `sys_enter_connect`, `sys_enter_openat`, `sys_enter_kill`), ring buffer transport, and user-space aggregation daemon, measuring pure observability overhead.
3. **Configuration C (User-Space Inference):** Telemetry pipeline coupled with user-space floating-point Logistic Regression inference operating over 1-second rolling feature windows.
4. **Configuration D (Kernel-Local Inference):** Telemetry coupled with kernel-local fixed-point (Q16.16) Logistic Regression evaluated synchronously within the eBPF tracepoint handler via in-kernel feature maps.
5. **Configuration E (Closed-Loop Enforcement):** Full pipeline integrating detection inference with a three-stage mitigation state machine (`OBSERVE` $\to$ `CONTAIN` via network isolation and SIGSTOP $\to$ `TERMINATE` or `ROLLBACK` via SIGCONT and network restoration).

### 1.2 Evaluation Boundaries and Environmental Grounding
Experiments were conducted on a pinned Linux x86_64 environment running kernel `6.6.87.2-microsoft-standard-WSL2` with Clang/LLVM 18.1.3, libbpf 1.3.0, bpftool 7.4.0, and Python 3.12.3. All workloads were executed within isolated Docker containers constrained to dedicated CPU cores (`cpuset-cpus="2-3"`) and memory limits (`memory="512m"`).

Workload conditions were divided into:
- **Benign Baseline Workloads:** 
  - $B1$: Idle container state (background OS noise).
  - $B2$: HTTP synthetic API traffic (500 requests/s, simulating web microservices).
  - $B3$: High process churn (rapid compilation and shell fork/exec loops, simulating CI/CD builders).
  - $B4$: Intensive mixed I/O and network operations (concurrent block transfers and socket streams).
- **Adversarial / Anomaly Workloads:**
  - $A1$: Process execution burst (rapid spawn of unauthorized binary utilities, modeling privilege escalation and lateral movement).
  - $A2$: Malicious file access burst (unauthorized traversal of sensitive paths such as `/etc/shadow` and `/root/.ssh`).
  - $A3$: Rapid outbound connection burst (held-out topological anomaly simulating reverse shells and data exfiltration).

---

## 2. Quantitative Results: Telemetry Overhead, Memory, and Buffering (RQ2)

### 2.1 Application Slowdown and CPU Overhead
A primary concern in cloud-native production deployments is whether eBPF kernel probes introduce prohibitive runtime penalties into guest container applications. Across all 280 instrumented runs (Configurations B through E across all workloads), the measured workload completion time was compared directly against uninstrumented Baseline A runs executed under identical seed configurations.

Table 1 presents the aggregate duration and overhead metrics across all configurations pooled over the seven workloads ($n = 70$ runs per configuration).

**Table 1: Workload Execution Duration and Slowdown Relative to Baseline A**

| Configuration | Description | Mean Duration (s) | Std Dev (s) | Median (s) | IQR (s) | Slowdown vs Baseline (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **A** | Uninstrumented Baseline | 1.8398 | 0.8980 | 1.9890 | 1.7061 | Reference (0.00%) |
| **B** | Telemetry Only | 1.8433 | 0.8991 | 1.9904 | 1.7051 | +0.19% |
| **C** | User-Space LR | 1.8415 | 0.8993 | 1.9893 | 1.7088 | +0.09% |
| **D** | Kernel-Local Fixed-Point LR | 1.8427 | 0.8996 | 1.9912 | 1.7062 | +0.16% |
| **E** | Staged Enforcement | 1.8409 | 0.8990 | 1.9895 | 1.7062 | +0.06% |

As shown in Table 1, the mean workload execution slowdown across all instrumented configurations remained strictly below **0.20%**. The maximum observed slowdown was +0.19% (Configuration B), while the closed-loop enforcement pipeline (Configuration E) exhibited a mean slowdown of only +0.06%. The variations between instrumented configurations fall well within the empirical standard deviation of repeated execution ($\sigma \approx 0.899$ s), confirming that raw tracepoint hooks introduce negligible CPU execution friction on standard cloud-native application processes.

### 2.2 Host Memory Footprint (Peak RSS)
Memory overhead was quantified by monitoring the host-level peak Resident Set Size (RSS) during container execution:

$$\text{RSS}_{\text{overhead}} = \text{RSS}_{\text{instrumented}} - \text{RSS}_{\text{baseline}}$$

The empirical measurements demonstrate an exceptionally lightweight memory footprint:
- **Baseline A Mean Peak RSS:** $93.18 \pm 4.39$ MB (Median: $93.36$ MB, IQR: $4.48$ MB).
- **Configuration B Mean Peak RSS:** $93.53 \pm 4.41$ MB (Median: $93.73$ MB, IQR: $4.38$ MB), representing a net daemon and buffer allocation of $+0.35$ MB ($+0.38\%$).
- **Configuration C Mean Peak RSS:** $93.63 \pm 4.40$ MB (Median: $93.85$ MB, IQR: $4.42$ MB), adding $+0.45$ MB ($+0.48\%$).
- **Configuration D Mean Peak RSS:** $93.64 \pm 4.42$ MB (Median: $93.84$ MB, IQR: $4.40$ MB), adding $+0.46$ MB ($+0.49\%$).
- **Configuration E Mean Peak RSS:** $93.73 \pm 4.42$ MB (Median: $93.93$ MB, IQR: $4.44$ MB), adding $+0.55$ MB ($+0.59\%$).

The net memory overhead introduced by the entire telemetry, dual inference, and staged enforcement infrastructure did not exceed **0.55 MB** above baseline host utilization.

### 2.3 Ring Buffer Reliability and Zero Event Loss
A persistent risk highlighted in prior literature is kernel ring buffer overflow and telemetry event dropping during high-volume burst events (Miano et al. 2022; Xiang et al. 2023). Across all $N_{inst} = 280$ instrumented runs, encompassing $77,598$ generated kernel security events, the kernel ring buffer drop counter and user-space reservation failure counters were audited:

$$\text{Event Loss Rate} = \frac{\sum \text{Lost Events}}{\sum \text{Submitted Events}} = \frac{0}{77,598} = 0.0000\%$$

Zero event loss was sustained across all burst workloads ($B3, B4, A1, A2, A3$). This reliability is directly attributable to the non-blocking ring buffer architecture (`BPF_MAP_TYPE_RINGBUF`) with dedicated 256 KB memory mapping and synchronous per-CPU event submission, avoiding the cache contention typical of legacy `BPF_MAP_TYPE_PERF_EVENT_ARRAY`.

---

## 3. Quantitative Results: Inference Placement and Latency Dynamics (RQ1, RQ4)

### 3.1 Inference Latency: User-Space Floating-Point vs. In-Kernel Fixed-Point
To resolve the core architectural question concerning ML inference placement (RQ1), we benchmarked the inference execution latency of identical mathematical models implemented in user-space versus the kernel BPF verifier boundary. Both models utilize a four-feature linear logistic regression architecture:

$$z = w_0 + \sum_{i=1}^4 w_i x_i, \quad \hat{y} = \sigma(z) = \frac{1}{1 + e^{-z}}$$

In user space (Configuration C), inference is executed via Python 3.12 standard 64-bit IEEE-754 floating-point operations. In kernel space (Configuration D), inference is executed using 32-bit Q16.16 fixed-point arithmetic verified under standard BPF verifier complexity bounds (Gate G proof: maximum relative error $< 0.01\%$).

Table 2 presents the empirical latency distributions across 70 completed runs per configuration.

**Table 2: Inference and Detection Latency Profiles**

| Metric | Configuration C (User-Space) | Configuration D (Kernel-Local) | Unit | Speedup / Ratio |
| :--- | :---: | :---: | :---: | :---: |
| **Mean Inference Latency** | $169.20 \pm 154.51$ | $4.25 \pm 1.63$ | $\mu\text{s}$ | **39.84x (~40x)** |
| **Median Inference Latency** | $76.24$ | $3.63$ | $\mu\text{s}$ | **21.00x** |
| **Interquartile Range (IQR)** | $42.68$ | $1.48$ | $\mu\text{s}$ | — |
| **95th Percentile ($p_{95}$)** | $444.79$ | $6.08$ | $\mu\text{s}$ | **73.16x** |
| **Mean End-to-End Latency ($T_5 - T_0$)** | $1567.0$ ($1.567$ ms) | $85.0$ ($0.085$ ms) | $\mu\text{s}$ | **18.44x** |
| **Median End-to-End Latency** | $1532.0$ | $82.0$ | $\mu\text{s}$ | **18.68x** |

As demonstrated in Table 2, moving the inference decision directly into the eBPF tracepoint handler achieves a **39.84x mean speedup** (reducing mean inference time from $169.20\ \mu\text{s}$ to $4.25\ \mu\text{s}$) and a **21.0x median speedup**. At the tail distribution ($p_{95}$), the kernel-local model provides a **73.16x latency reduction** ($6.08\ \mu\text{s}$ versus $444.79\ \mu\text{s}$), completely eliminating Python user-space garbage collection and operating system scheduling jitter.

### 3.2 End-to-End Detection and Containment Response Latency
In cloud-native intrusion defense, the critical operational window is the total elapsed time from the occurrence of an adversarial kernel event ($T_0$) to active workload containment ($T_7$).

Under Configuration D, the total end-to-end detection latency ($T_5 - T_0$, incorporating tracepoint firing, in-kernel feature extraction, Q16.16 inference, and threshold evaluation) averaged **$85.0\ \mu\text{s}$** ($0.085$ ms), compared to **$1567.0\ \mu\text{s}$** ($1.567$ ms) in user-space Configuration C. This represents an **18.44x reduction** in detection delay.

Under Configuration E, upon anomaly trigger, the staged mitigation state machine executed container containment via cgroup v2 freeze and iptables/tc isolation:
- **Containment Action Latency ($T_7 - T_6$):** Mean $= 1.172 \pm 0.054$ ms (Median: $1.155$ ms, IQR: $0.096$ ms, $n = 17$ containment events).
- **Total Detection-to-Mitigation Latency ($T_7 - T_0$):** Mean $= 2.584 \pm 0.071$ ms (Median: $2.603$ ms, IQR: $0.119$ ms).

### 3.3 Safe Rollback Recovery Latency
When a containment action was identified as a false trigger, or upon administrative policy reversal, the rollback state machine executed container thawing (SIGCONT) and policy restoration:
- **Rollback Latency ($T_8 - T_7$):** Mean $= 16.0 \pm 0.0\ \mu\text{s}$ ($0.016$ ms).
- **Rollback Success Rate:** **100.0%** ($17 / 17$ verified rollback executions returned container to functional state with zero unhandled zombie or orphaned processes).

---

## 4. Quantitative Results: Detection Quality, Churn Confounding, and Evasion (RQ3)

### 4.1 Detection Accuracy on Targeted Attack Profiles
Detection effectiveness was evaluated across all 10 independent repetitions for each anomaly workload. Table 3 details the classification performance of the trained linear model on the targeted threat scenarios.

**Table 3: Detection Performance by Attack Workload (Configurations C & D)**

| Workload ID | Anomaly Description | Ground Truth Positives | True Positives | False Negatives | Precision | Recall | $F_1$-Score |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **A1** | Execution Burst (Process Anomaly) | 10 | 7 | 3 | **1.000** | **0.700** | **0.824** |
| **A2** | Sensitive File Access Burst | 10 | 0 | 10 | 0.000 | 0.000 | 0.000 |
| **A3** | Outbound Connection Burst (Held-Out) | 10 | 0 | 10 | 0.000 | 0.000 | 0.000 |

On Workload $A1$ (process execution bursts), the model achieved perfect precision ($1.000$) and a recall of $0.700$, yielding an $F_1$-score of **$0.824$**. The three false negatives occurred in repetitions where process spawn rates fell just below the static decision threshold ($\theta = 0.50$).

### 4.2 The Benign Churn Problem: Empirical Confounding (B3)
A vital empirical contribution of this study is the rigorous characterization of false alarm dynamics under benign cloud-native churn. On standard microservice workloads ($B1$ Idle, $B2$ HTTP API, and $B4$ Mixed I/O), the classifier produced **zero false positives** ($\text{FPR} = 0.000$), preserving uninterrupted application execution.

However, on Workload $B3$ (high-churn build and compilation environments):
- **Configuration C False Positive Rate:** **50.0%** ($5 / 10$ benign runs triggered false alerts).
- **Configuration D False Positive Rate:** **80.0%** ($8 / 10$ benign runs triggered false alerts).
- **Configuration E False Positive Rate:** **80.0%** ($8 / 10$ benign runs triggered false alerts and induced containment).

This failure mode provides direct quantitative evidence for a critical vulnerability in linear behavioral classifiers: **feature confounding**. In containerized CI/CD pipelines, rapid compilation scripts (`gcc`, `make`, `sh`) produce high rates of `sys_enter_execve` invocations. Because the linear model assigns a large positive weight to process spawn frequency, legitimate developer activity is misclassified as an adversarial execution burst.

### 4.3 Topological Blindspots and Held-Out Evasion (A3)
On Workload $A3$ (rapid outbound connection burst), the classifier exhibited **zero recall** ($\text{Recall} = 0.000$, $0 / 10$ attacks detected). Because model training was conducted on a four-feature system where network connection burst features had near-zero weights relative to process execution signals, the network anomaly completely evaded the linear decision boundary. This quantitatively demonstrates the catastrophic vulnerability of single-modality linear classifiers to out-of-distribution or topological attack shifts.

---

## 5. Statistical Rigor and Effect Size Analysis

To substantiate the observed latency differences between user-space (Configuration C) and in-kernel (Configuration D) inference, we performed paired non-parametric statistical hypothesis testing across all matched runs ($n = 70$ pairs):
- **Wilcoxon Signed-Rank Test:** $W = 0.0$, $p = 1.94 \times 10^{-12}$, rejecting the null hypothesis of equal median latencies at the $\alpha = 0.001$ significance level.
- **Parametric Paired $t$-Test:** $t(69) = 8.92$, $p = 3.65 \times 10^{-13}$.
- **Effect Size:** Cohen's $d = 1.508$ (representing an extremely large effect size, $d > 0.8$).

For total end-to-end detection latency ($T_5 - T_0$):
- **Wilcoxon Signed-Rank Test:** $W = 0.0$, $p = 1.94 \times 10^{-12}$.
- **Paired $t$-Test:** $t(69) = 17.84$, $p = 1.12 \times 10^{-26}$.
- **Effect Size:** Cohen's $d = 3.016$ (massive effect size).

These tests confirm that the observed 40x inference speedup and 18x detection latency reduction are statistically robust characteristics of the architectural placement rather than random measurement artifacts.

---

## 6. Synthesis and Critical Discussion against Primary Literature

### 6.1 Placement Trade-offs: Latency vs. Verifier Expressiveness (RQ1, RQ4)
Our empirical demonstration of a 40x inference speedup ($4.25\ \mu\text{s}$ vs. $169.20\ \mu\text{s}$) strongly corroborates the findings of in-kernel inference pioneers. Morichetta et al. (2024, *IEEE TNSM*) and Scholten et al. (2024, *ACM CoNEXT*) established that synchronous in-kernel packet filtering via XDP yields sub-microsecond classification. Our work extends this empirical proof to **cloud-native process and system call telemetry**.

However, our findings reveal the severe architectural tax imposed by in-kernel execution:
1. **The BPF Verifier Complexity Ceiling:** To pass the Linux BPF verifier without floating-point emulation, our in-kernel model was strictly constrained to a 4-feature linear model using Q16.16 fixed-point arithmetic. Complex non-linear models (e.g., Random Forests or Deep Neural Networks) cannot be verified in kernel space without instruction-count exhaustion or helper-function patching (Morichetta et al. 2024).
2. **The Expressiveness Penalty:** While user space allows arbitrary ensemble architectures and dynamic retraining, it incurs a $1.567$ ms detection penalty. Thus, cloud-native architectures face a fundamental trade-off: **ultra-low-latency linear screening in kernel space versus high-capacity, expressive detection in user space**.

### 6.2 Telemetry Scalability and Buffering Mechanics (RQ2)
Our observation of $<0.20\%$ application slowdown and zero event loss across $77,598$ events supports the claims of modern eBPF observability frameworks (e.g., KubeArmor, Tetragon) that raw tracepoints outperform traditional auditd or ptrace architectures (Pacheco et al. 2023, *Computers & Security*). 

Nevertheless, our critical analysis highlights an evaluation boundary: our experiments evaluated single-container burst loads up to 500 requests/s and rapid process churn. In massive multi-tenant Kubernetes nodes processing $>100,000$ events/s, ring buffer exhaustion remains an active operational threat unless adaptive sampling or in-kernel filtering is deployed (Xiang et al. 2023; Miano et al. 2022).

### 6.3 The Concept Drift and Benign Churn Dilemma (RQ3)
Our finding that benign container churn ($B3$) induces an $80\%$ false positive rate addresses an urgent gap in literature. While numerous primary studies report near-perfect $F_1$-scores ($>0.98$) on static benchmark datasets (such as DARPA or NSL-KDD), very few studies evaluate dynamic microservice churn. 

Our empirical results validate the theoretical critique raised by de Oliveira et al. (2024, *IEEE Access*): **high process creation frequency in cloud-native developer pipelines fundamentally mimics malicious execution bursts**. Without context-aware feature engineering (e.g., parent process ancestry, container image metadata, binary hash verification), purely statistical rate-based counters inevitably collapse into prohibitive false alarm rates.

### 6.4 Safe Enforcement and Asymmetric Blast Radius (RQ4)
The closed-loop mitigation latency measured in our prototype ($1.17$ ms containment, $2.58$ ms total response) proves that eBPF-triggered cgroup isolation can contain malicious workloads orders of magnitude faster than user-space orchestration controllers (e.g., Kubernetes admission webhooks, which operate on the scale of $100$–$500$ ms).

However, the high false alarm rate observed on $B3$ reveals the dangerous **asymmetric blast radius of active enforcement**: when false alarms occur, legitimate developer builds are frozen. Our implementation of an instantaneous ($16\ \mu\text{s}$) rollback state machine represents an essential architectural safety gate, proving that active kernel enforcement systems must incorporate low-latency compensation mechanisms to mitigate false containment actions.

---

## 7. Section Summary: Verified Claims vs. Unproven Hypotheses

To maintain absolute academic integrity, Table 4 delineates what this experimental evaluation has rigorously verified versus what remains unproven.

**Table 4: Status of Empirical Claims and Boundary Disclosures**

| Architectural Claim | Status | Empirical Grounding | Boundary / Limitation |
| :--- | :---: | :--- | :--- |
| **In-Kernel LR Speedup** | **VERIFIED** | $39.84$x mean speedup ($4.25\ \mu\text{s}$ vs $169.20\ \mu\text{s}$, $p < 10^{-11}$). | Limited to 4-feature fixed-point linear model. |
| **Telemetry CPU Overhead** | **VERIFIED** | Application slowdown $< 0.20\%$ across 280 runs. | Single-host WSL2/Docker testbed; max 500 req/s. |
| **Ring Buffer Zero Loss** | **VERIFIED** | $0$ drops across $77,598$ events in 280 runs. | 256 KB ring buffer; burst duration $\le 10$ s. |
| **Enforcement Latency** | **VERIFIED** | $1.17$ ms containment; $2.58$ ms detection-to-mitigation. | Direct cgroup v2 freeze; single host. |
| **Rollback Safety** | **VERIFIED** | $16\ \mu\text{s}$ rollback; $100\%$ container recovery. | Evaluated across 17 containment actions. |
| **Benign Churn Confounding** | **VERIFIED** | $50\%$–$80\%$ false positive rate on workload $B3$. | Linear rate features fail to separate compilation from attack. |
| **Production Generalization** | *UNPROVEN* | Evaluated in synthetic microservice benchmark. | Requires multi-node Kubernetes cluster evaluation. |
| **Complex Threat Defense** | *UNPROVEN* | Evaluated on process, file, and network bursts. | Advanced multi-stage APTs and kernel-space rootkits unverified. |
| **Universal Superiority** | *REFUTED* | In-kernel inference is faster but severely capacity-limited. | Trade-off between speed and classification capacity is fundamental. |
