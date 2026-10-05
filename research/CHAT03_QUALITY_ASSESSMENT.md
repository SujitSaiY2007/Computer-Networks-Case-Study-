# CHAT 03 — Formal Qualitative Quality Assessment

**Project:** BACSE203 Computer Networks Case Study  
**Assessment date:** 5 October 2026  
**Status:** **COMPLETE**  
**Frozen baseline:** **40 primary studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals**

## 1. Assessment methodology

CHAT 03 applies a qualitative, evidence-led assessment to the already-frozen 40-study corpus. No points, weights, ranks, or composite numerical quality score are assigned. The evidence base is heterogeneous: a network-function paper, an enforcement paper, a threat study and an ML detector do not require identical evidence to be methodologically useful.

Each dimension uses only:

- **Clearly reported** — sufficient evidence is explicitly present for the dimension relative to the study's own objective.
- **Partially reported** — relevant evidence exists, but important detail, breadth or validation is incomplete.
- **Not reported** — the inspected CHAT 02 evidence does not provide the information required for the dimension.

### Ten dimensions

1. Objective clarity — explicit research/problem objective and evaluation target.
2. Technical/system description — telemetry hooks, architecture, ML method/placement, enforcement and core mechanisms.
3. Dataset/workload transparency — datasets, workloads, attacks, container images or other evaluation inputs.
4. Baseline adequacy — meaningful comparison methods/configurations for the stated objective.
5. Evaluation validity — whether metrics and comparisons support the claims being made.
6. Experimental/testbed detail — hardware, software, kernel/runtime, topology, containers/orchestration and relevant configuration.
7. Reproducibility — code, datasets, configurations, artifacts or sufficiently precise procedures.
8. Limitation disclosure — scope limits, assumptions, failure modes or threats to validity.
9. External validity — evidence beyond a narrowly constructed workload, attack, device, cluster, kernel or environment.
10. Statistical reporting — repeated runs, variance, confidence intervals, significance tests or comparable uncertainty treatment.

### Core versus Supporting/Adjacent

Studies are judged against **their own objectives**. A Supporting networking or enforcement paper is not penalized merely because it has no ML experiment.

- **Core:** directly studies eBPF-assisted runtime security/detection/enforcement in containers/cloud-native environments.
- **Supporting:** supplies important telemetry, overhead, enforcement, networking, policy or threat evidence without necessarily providing the full eBPF+ML+cloud-native combination.

### Missing reporting versus technical weakness

**Not reported** means the evidence was absent from the inspected extraction. It does not prove the underlying method is technically poor. **Partially reported** identifies an evidence-quality limitation affecting comparability or confidence; it does not mean the method is incorrect.

## 2. Per-study quality matrix

| Study ID | Short title | Role | Objective clarity | Technical/system description | Dataset/workload transparency | Baseline adequacy | Evaluation validity | Experimental/testbed detail | Reproducibility | Limitation disclosure | External validity | Statistical reporting | Evidence-based justification | Overall qualitative assessment | Important quality concern(s) |
| - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| P001 | eBPF System Security Tools in Cloud-Native Environments | Core | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Partially reported | Tool comparison; performance/auditing evidence is useful, but workload breadth and repeatability are limited. | Mixed | Selected scenarios/configurations may not represent production diversity; repeatability limited. |
| P002 | Real-Time eBPF/XDP Deep Learning Traffic Detection | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Partially reported | Named public datasets, feature reduction, explicit placement and latency/CPU measures are strong; broader deployment replication is limited. | Strong-to-mixed | IoT/Raspberry Pi setting limits direct cloud-container generalization; uncertainty limited. |
| P003 | CODAX Semantic DDoS Detection in Linux Containers | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | Clear container-DDoS objective, eBPF design and quantitative latency/CPU results; attack scope and statistical treatment are narrow. | Strong-to-mixed | Attack-specific evaluation; statistical uncertainty absent. |
| P004 | AIoT Gateway eBPF Timing-Traces Anomaly Detection | Supporting | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Partially reported | Not reported | Clear timing telemetry and anomaly pipeline; baseline breadth and testbed detail are less complete. | Mixed | Gateway setting is not directly equivalent to Kubernetes runtime security. |
| P005 | DeSFAM Adaptive eBPF + AI Container Security | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | Strong end-to-end syscall → ML → BPF-LSM chain with named threats and quantitative detection/overhead evidence. | Strong-to-mixed | External validity and statistical uncertainty are not established. |
| P006 | Cryptojacking Containers with eBPF and ML | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Clear cryptojacking workload, Tetragon telemetry and ML comparison; validation is concentrated on one threat class. | Mixed | Single attack class and bounded environment. |
| P007 | eBPF Cloud-Native Observability, Networking and Security | Supporting | Clearly reported | Clearly reported | Partially reported | Partially reported | Clearly reported | Partially reported | Partially reported | Partially reported | Clearly reported | Not reported | Hook coverage and cloud-native architecture are well described; dataset/statistical dimensions are inherently limited. | Mixed | Architecture study, not ML benchmark evidence. |
| P008 | BPFast High-Performance Packet Payload Inspection | Supporting | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Packet-inspection objective and eBPF/XDP performance are clear; runtime-ML transferability is limited. | Mixed | Network payload setting limits runtime-ML transferability. |
| P009 | Secure Inter-Container Communications Using XDP/eBPF | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Inter-container security and XDP/eBPF throughput/latency evaluation are explicit; broader environments are not established. | Mixed | Network enforcement rather than ML detection. |
| P010 | Kubernetes Runtime Security with eBPF and BPF-LSM | Core | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Direct Kubernetes monitoring/enforcement evidence with explicit BPF-LSM mechanisms and overhead evaluation. | Mixed | Selected runtime threats/testbed limit generalization. |
| P011 | eBPF/XDP Kubernetes DoS Detection | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Kubernetes DoS detection/mitigation and resource overhead are directly evaluated; broader runtime-security generalization is limited. | Mixed | DoS-only scope. |
| P012 | In-Kernel vs User-Space Lightweight ML Packet Processing | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Clearly reported | Partially reported | Direct kernel/user-space placement comparison with throughput/core results; security workload breadth is narrower. | Strong-to-mixed | Packet classification is not container runtime detection. |
| P013 | eBPF + ML IDS for DoS/DDoS | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Multiple ML baselines and quantitative DoS/DDoS results; environment and uncertainty reporting are limited. | Mixed | Network IDS focus limits cloud-native runtime generalization. |
| P014 | Unsupervised In-Kernel IDS with Autoencoders and eBPF | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Quantized in-kernel autoencoder and throughput/latency comparisons are explicit; artifacts and statistical evidence are limited. | Mixed | Results tied to network IDS conditions. |
| P015 | Behavioral Anomaly Detection in Linux with eBPF and LSTM | Supporting | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Partially reported | Not reported | LSTM/traditional-ML comparison is clear; host scope limits cloud/container transfer. | Mixed | Bounded attack set and no uncertainty analysis. |
| P016 | Container Attack Detection with eBPF and AdaBoost | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Concrete container attack scenarios, syscall telemetry and AdaBoost evaluation; replication evidence is weak. | Mixed | File-access modality is narrower than multimodal runtime behaviour. |
| P017 | Abnormal Container File-Access Detection with eBPF | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Fine-grained file-access telemetry and autoencoder detection are well defined; external validation is limited. | Mixed | Scenarios may not represent long-running production workloads. |
| P018 | Hybrid Runtime Detection of Malicious Containers | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Multimodal syscall/network telemetry and multiple malicious/benign scenarios provide direct evidence; production-like validation is limited. | Mixed | Enforcement-centric; no ML detector required. |
| P019 | Cordon Kernel-Level Container Security Control | Supporting | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Kernel-control objective, eBPF/LSM enforcement and overhead are well specified; ML is outside its objective. | Strong-to-mixed | Enforcement-centric; no ML detector required. |
| P020 | BPFGuard Multi-Granularity Container Runtime MAC | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Kubernetes/container MAC granularity and benchmark evidence are strong; artifacts and uncertainty are limited. | Strong-to-mixed | Performance workload does not test adversarial runtime security. |
| P021 | Deep Analysis of Containerized Web Server Performance Using eBPF | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Three-tier Docker workload plus eBPF syscall monitoring and Random Forest regression provide concrete performance evidence. | Mixed | Tool comparison is not an ML benchmark. |
| P022 | eBPF Container Activity Analysis System | Supporting | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Clear monitoring/tool comparison; not a controlled ML-security benchmark. | Mixed | Policy generation is not ML detection. |
| P023 | Optimus Dynamic Syscall Filtering | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | 71 real container images strengthen workload grounding and dynamic filtering evidence. | Mixed | Single attack family. |
| P024 | Coda CPU-Exhaustion DoS Detection | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Clear application-layer CPU-exhaustion objective and eBPF evaluation; generalization is limited. | Mixed | Policy mechanism is not conventional ML. |
| P025 | Hela Whole-Container-Lifecycle Syscall Restriction | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | Lifecycle-wide restriction is clearly evaluated; mechanism is not a conventional ML detector. | Strong-to-mixed | Statistical reporting limited. |
| P026 | BeaCon Automatic Container Policy Generation | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Partially reported | 45 vulnerabilities and two PoCs across real Docker containers provide strong practical grounding. | Strong | Linux-process scope limits Kubernetes generalization. |
| P027 | Vaccine Dynamic Process Control with eBPF | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | Large vulnerability/malware scenario counts strengthen practical evidence; Linux-process scope limits Kubernetes transfer. | Strong-to-mixed | Network identity attack scope is narrow. |
| P028 | Kubernetes IP Spoofing Prevention with eBPF | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | Kubernetes/EKS packet validation and blocking/overhead evaluation are concrete; attack scope is narrow. | Strong-to-mixed | Policy-management evidence. |
| P029 | KubeAegis Unified Container Security Policies | Supporting | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Partially reported | Not reported | Policy integration and conversion architecture are clear; reproducibility and external validation are weaker. | Mixed | Policy discovery is adjacent rather than ML-centric. |
| P030 | KubeRosy Dynamic Syscall Filtering | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | Argument-aware syscall filtering and quantified overhead are clear; workload diversity and statistics are limited. | Strong-to-mixed | Threat evidence should not be read as detector validation. |
| P031 | eBPF/XDP Random-Forest Docker-Swarm Firewall | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Direct Docker Swarm eBPF/XDP + Random Forest evaluation with detection, response and CPU measures. | Strong-to-mixed | Production diversity and independent artifacts remain uncertain. |
| P032 | Kunerva Automated Network Policy Discovery | Supporting | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Clearly reported | Partially reported | Not reported | Not reported | Container/Kubernetes policy discovery and verification are clear; experimental breadth is less extensive. | Mixed | Networking architecture evidence, not runtime ML security. |
| P033 | Container-to-Cluster Chained Escape Attacks | Supporting | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Threat scenarios and defensive implications are well documented; not a quantitative detector benchmark. | Strong-to-mixed | SSH/Linux scope is narrower than container orchestration. |
| P034 | Container-Specific Service Mesh Lateral-Movement Mitigation | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Clearly reported | Partially reported | Zero-copy eBPF collection, lightweight ML/online learning and quantitative collection/CPU comparisons provide strong direct evidence. | Strong | Focused testbed; statistical uncertainty absent. |
| P035 | eBPF-Based Network Functions for Microservices | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | Polycube/eBPF/XDP architecture and Kubernetes throughput evidence are strong; ML is outside its objective. | Strong-to-mixed | Bounded testbed. |
| P036 | ESX Self-Generated SSH Control Policy with eBPF | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | SSH policy generation and behavioural rules are explicit and quantitatively evaluated; cloud-native transfer is limited. | Strong-to-mixed | Malware/RCE generalization uncertain. |
| P037 | Secure Namespaced Kernel Audit for Containers | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | Namespace-aware saBPF auditing and explicit LSM overhead comparison are strong systems evidence. | Strong-to-mixed | Attack scenarios are specific; no ML detection evaluation. |
| P038 | Malware Detection in Cloud-Native Environments | Core | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Cloud-native eBPF sensing plus ML ensemble detection is directly relevant; artifact/cross-cluster validation is incomplete. | Strong-to-mixed | Results depend on selected scenarios/tool configurations. |
| P039 | Cross-Container Attacks: The Bewildered eBPF on Clouds | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Clearly reported | Partially reported | Not reported | Concrete cross-container/cloud attack paths support the threat model; it is not a detector benchmark. | Mixed | undefined |
| P040 | Comparative eBPF Runtime Security Monitoring Tools on Kubernetes | Supporting | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Clearly reported | Partially reported | Partially reported | Partially reported | Not reported | Kubernetes tool comparison reports MTTD, detection, false positives, CPU and memory; configuration/statistical uncertainty remains limited. | Strong-to-mixed | undefined |

### Overall qualitative assessment labels

- **Strong** — most decision-relevant dimensions are clearly reported, with limited evidence-quality weaknesses.
- **Strong-to-mixed** — technically and experimentally useful, but at least one important evidence dimension is materially incomplete.
- **Mixed** — useful evidence is present, but several dimensions limit comparability, reproducibility or generalization.

These are descriptive summaries, **not numerical scores or rankings**.

## 3. Quality evidence summary

### Most consistently reported
**Objective clarity** and **technical/system description** are the strongest recurring dimensions. Most papers explain the target problem and identify the main eBPF/XDP/LSM mechanism, telemetry path or ML method. Evaluation validity and experimental/testbed detail are also commonly reported.

### Most frequently partial or missing
**Statistical reporting** is the clearest recurring weakness: repeated-run variance, confidence intervals, significance tests and comparable uncertainty estimates are rarely established. **Reproducibility** is commonly partial because code, data, configurations and artifacts are inconsistently available. **External validity** is frequently partial because many studies use one kernel/testbed, a small container set, selected attacks or one orchestration environment.

### Dataset/workload weaknesses
The corpus mixes public datasets (including CICDDoS2019, IoT-23 and TON_IoT), study-specific/private data, real container images, vulnerability/PoC sets, constructed attacks and focused application/network workloads. This diversity is useful but makes direct accuracy comparisons unsafe. Many studies remain attack- or workload-specific rather than testing unseen workloads, temporal shift or production-like churn.

### Baseline weaknesses
Baselines are strongest where studies compare multiple ML models, security tools, enforcement mechanisms or kernel/user-space placements. They are weaker where a new system is compared with only one implementation or a non-equivalent baseline.

### Reproducibility weaknesses
Recurring issues include incomplete code/configuration disclosure, private datasets, unspecified kernel/runtime details, incomplete attack-generation procedures and missing full container/testbed manifests. Code availability should not be equated with full experimental reproducibility.

### Latency and overhead weaknesses
CPU and memory overhead are relatively common, but latency is not standardized. The corpus rarely measures the complete chain:

**event generation → buffering/transport → feature extraction → inference → decision → enforcement → recovery**

Detection/inference latency is therefore not interchangeable with **detection-to-mitigation latency**.

### Event loss and buffering
Event rate, buffer occupancy, dropped events and telemetry loss are not consistently measured. Strong detection accuracy therefore does not by itself prove telemetry completeness under high event rates.

### Adversarial robustness and concept drift
Selected work, especially P034, addresses online/adaptive learning, but systematic evaluation of deliberate evasion, feature manipulation, poisoning, realistic concept drift and unseen attack classes is not established across the corpus.

### External validity
The dominant pattern is bounded testbeds: a specific Linux kernel, device, container set, Kubernetes cluster, Docker deployment, network topology or attack scenario. Evidence across multiple kernels, heterogeneous runtimes/CNIs, multi-node churn and realistic cloud-provider conditions is limited.

### Core versus Supporting/Adjacent
**Core studies** provide stronger direct evidence for runtime telemetry, detection and/or enforcement in container/cloud-native settings. Their recurring weaknesses are narrow attack/workload scope and limited statistical/reproducibility evidence.

**Supporting/Adjacent studies** are especially valuable for architecture and systems evidence: in-kernel versus user-space placement, XDP throughput, syscall enforcement, policy generation, container lifecycle control and threat scenarios. They should not be treated as direct evidence of end-to-end eBPF+ML runtime-security performance.

## 4. Evidence-confidence observations

- **Strongly supported:** eBPF/XDP provides low-level telemetry or enforcement with measurable performance characteristics; multiple studies demonstrate container/Kubernetes runtime monitoring/enforcement; ML detection exists across syscall, network-flow, file-access and timing telemetry; placement affects throughput/latency; eBPF/LSM/seccomp-style mechanisms can operate at container/runtime granularity.
- **Narrow/attack-specific:** much detection evidence concerns DDoS, cryptojacking, container escape, file-access anomalies, malware/RCE or IP spoofing.
- **Bounded testbeds:** many results depend on limited container sets, one cluster/device, one kernel/runtime or a controlled network.
- **Synthetic/private data:** study-specific/private workloads reduce independent replication and cross-study comparison.
- **Missing realistic churn:** pod churn, rolling updates, node migration, autoscaling, service-mesh changes and heterogeneous workloads are not consistently evaluated.
- **Event loss/buffering:** event rates, queue/buffer occupancy and dropped events are not consistently reported.
- **Detection-to-mitigation latency:** end-to-end enforcement latency is uncommon even when inference/detection latency is reported.
- **Adversarial robustness/concept drift:** systematic evasion, poisoning, drift and unseen-attack testing are not established across the corpus.
- **Reproducibility artifacts:** artifact availability varies substantially and must be treated study-by-study.

## 5. CHAT 03 boundaries

This assessment does **not** alter the frozen baseline, add/replace primary studies, restart searching, freeze final research gaps, design the experimental architecture, implement the prototype, create the Review 2 PPT, or write the final manuscript.

It is the evidence-quality checkpoint feeding **CHAT 04 — Critical Synthesis / Technology Taxonomy**.

## 6. Canonical completion state

**CHAT 03 — COMPLETE**

**Next phase:** **CHAT 04 — Critical Synthesis / Technology Taxonomy**

The exact continuation prompt is recorded in `project/CHAT_HANDOFF.md`.
