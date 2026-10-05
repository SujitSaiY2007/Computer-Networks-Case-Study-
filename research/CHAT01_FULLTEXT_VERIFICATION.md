# CHAT 01 — Full-Text Verification and Final Candidate Screening

**Project:** eBPF-Assisted Machine Learning for Cloud-Native Runtime Security  
**Screening date:** 5 October 2026  
**Baseline:** repository candidate set of 40 studies  
**Screening status:** VERIFIED SCREENING BASELINE — final detailed extraction/quality assessment remains a later phase.

## Screening method

Each candidate was checked against the frozen scope, bibliographic identifiers, publication type/status, technical relevance, and the evidence visible in the authoritative publisher/venue record or accessible full text. DOI/title consistency and retraction status were also checked in a batch scholarly audit.

Evidence strength:
- **High:** accessible full text or detailed publisher/venue record sufficient for screening-level technical evidence.
- **Moderate:** authoritative publisher/DOI/academic record and detailed abstract sufficient for screening, but full text still belongs in CHAT 02A acquisition.
- **Low:** metadata only; none of the retained 40 are accepted on metadata alone.

**NR = Not reported at screening level.** Missing values must be extracted from the full text later; they are not inferred.

## Critical correction

Candidate #34, **Extended Berkeley Packet Filter: An Application Perspective**, is explicitly a **review article**, not a primary study. It is therefore removed from the primary evidence set and retained only as background/comparison literature.

It is replaced by **Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks** (IEEE Transactions on Cloud Computing, 2026, DOI 10.1109/TCC.2026.3657486). The replacement is a peer-reviewed journal article that directly combines Kubernetes/cloud-native container security, eBPF system-call telemetry, lightweight ML anomaly detection, online learning, and container isolation. The scholarly identifier audit matched the title/DOI and found no retraction.

## Verified screening table

| # | Candidate / verified publication | Venue/type | Direct relevance | Classification | eBPF mechanism | ML | Environment | Evidence strength | Decision | Reason |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | An In-Depth Analysis of eBPF-Based System Security Tools in Cloud-Native Environments — DOI 10.1109/ACCESS.2025.3605432 | IEEE Access / journal | Direct | Core | KubeArmor/Falco/Tetragon/Tracee eBPF monitoring/enforcement | None | Kubernetes/cloud-native | Moderate | Include | Primary comparative runtime-security study; strong baseline for telemetry, performance and tool choice. |
| 2 | Real-Time eBPF/XDP-Based Deep Learning Framework for Anomaly Traffic Detection in Internet of Things Networks — DOI 10.1109/MIC.2026.3692726 | IEEE Internet Computing / journal | Adjacent | Supporting | eBPF/XDP driver-path feature selection | Lightweight DL in user space | IoT/edge | Moderate | Include | Strong ML-placement/telemetry evidence, but not container/Kubernetes runtime. |
| 3 | eBPF-Based Runtime Detection of Semantic DDoS Attacks in Linux Containers (CODAX) — DOI 10.1109/ACCESS.2025.3614389 | IEEE Access / journal | Direct | Core | eBPF probes/system-call CPU monitoring | Detection logic; not central ML | Linux containers | High | Include | Direct container-runtime detection study with latency/overhead relevance. |
| 4 | Low-Overhead Passive Resilience Monitoring for AIoT Gateways: End-to-End Anomaly Detection via eBPF Timing Traces and Autoencoders — DOI 10.1109/ACCESS.2026.3685156 | IEEE Access / journal | Adjacent | Supporting | eBPF timing traces | Autoencoder/CUSUM | AIoT gateways | High | Include | Useful evidence for low-overhead telemetry and anomaly detection; environment is outside Kubernetes. |
| 5 | DeSFAM: An Adaptive eBPF and AI-Driven Framework for Securing Cloud Containers in Real Time — DOI 10.1109/ACCESS.2025.3592192 | IEEE Access / journal | Direct | Core | Dynamic eBPF syscall tracing, maps, LSM hooks | VAE + Isolation Forest/risk scoring | Cloud containers | High | Include | Closely matches telemetry → ML → enforcement architecture. |
| 6 | Detecting Cryptojacking Containers Using eBPF-Based Security Runtime and Machine Learning — DOI 10.3390/electronics14061208 | Electronics / journal | Direct | Core | Tetragon syscall and flow telemetry | Multiple ML models | Cloud-native containers/Kubernetes | High | Include | Direct container ML detection and overhead evidence. |
| 7 | eBPF: A New Approach to Cloud-Native Observability, Networking and Security for Current (5G) and Future Mobile Networks (6G and Beyond) — DOI 10.1109/ACCESS.2023.3281480 | IEEE Access / journal | Adjacent | Supporting | tracepoints, kprobes, TC/XDP, LSM | None | Cloud-native/mobile | Moderate | Include | Architectural evidence for hooks, observability and enforcement; not an ML experiment. |
| 8 | BPFast: An eBPF/XDP-Based High-Performance Packet Payload Inspection System for Cloud Environments — DOI 10.13089/JKIISC.2022.32.2.213 | JKIISC / journal | Adjacent | Supporting | eBPF/XDP payload inspection | None | Kubernetes/cloud | High | Include | Strong network telemetry/performance baseline relevant to overhead and enforcement. |
| 9 | Secure Inter-Container Communications Using XDP/eBPF — DOI 10.1109/TNET.2022.3206781 | IEEE/ACM TNET / journal | Adjacent | Supporting | XDP/eBPF network enforcement | None | Inter-container networking | Moderate | Include | Direct container-network security/enforcement evidence; no ML. |
| 10 | Container Instrumentation and Enforcement System for Runtime Security of Kubernetes Platform with eBPF — DOI 10.32604/iasc.2023.039565 | Intelligent Automation & Soft Computing / journal | Direct | Core | Tracee + BPF-LSM hooks | None | Kubernetes | High | Include | Direct Kubernetes runtime monitoring and enforcement study. |
| 11 | Detection of Denial of Service Attack in Cloud Based Kubernetes Using eBPF — DOI 10.3390/app13084700 | Applied Sciences / journal | Direct | Core | eBPF/XDP | Detection/mitigation logic; no central ML | Cloud/Kubernetes | High | Include | Direct Kubernetes attack detection and performance evidence. |
| 12 | Practicality of in-kernel/user-space packet processing empowered by lightweight neural network and decision tree — DOI 10.1016/j.comnet.2024.110188 | Computer Networks / journal | Adjacent | Supporting | eBPF/XDP and AF_XDP | Quantized NN + decision tree | Packet processing | High | Include | Strong evidence for in-kernel vs user-space ML placement, verifier constraints and throughput. |
| 13 | Enhancing intrusion detection against denial of service and distributed denial of service attacks: Leveraging extended Berkeley packet filter and machine learning algorithms — DOI 10.1049/cmu2.12879 | IET Communications / journal | Adjacent | Supporting | eBPF kernel traffic capture | DT/RF/SVM/TwinSVM | Network IDS | High | Include | Direct eBPF+ML comparison; network rather than container focus. |
| 14 | Unsupervised Real-Time In-Kernel Intrusion Detection System Using Autoencoders and eBPF — DOI 10.23919/transcom.2025EBP3028 | IEICE Transactions on Communications / journal | Adjacent | Supporting | eBPF in-kernel inference | QAT unsupervised autoencoder | Network IDS | High | Include | Strong in-kernel ML and latency/throughput evidence; not Kubernetes. |
| 15 | Behavioral Anomaly Detection in Linux Systems using eBPF and LSTM Neural Networks: A Comparative Study with Traditional Machine Learning — DOI 10.5120/ijca502db8d4e336 | International Journal of Computer Applications / journal | Adjacent | Supporting | eBPF syscall telemetry | LSTM autoencoder + traditional ML | Linux host | High | Include | Primary host anomaly study; useful but outside cloud/container scope. Venue/indexing quality should be recorded during quality assessment. |
| 16 | A Technique for Accurate Detection of Container Attacks with eBPF and AdaBoost — DOI 10.9708/jksci.2024.29.06.039 | Journal of The Korea Society of Computer and Information / journal | Direct | Core | eBPF syscall-pattern capture | AdaBoost | Containers | High | Include | Direct container attack-detection experiment with reported detection and overhead metrics. |
| 17 | An Abnormal File Access Detection Model for Containers Based on eBPF Listening — DOI 10.3390/math14060991 | Mathematics / journal | Direct | Core | Fine-grained eBPF file-access capture | Attention-enhanced autoencoder | Containers | High | Include | Direct container telemetry + ML anomaly detection; file-access-specific scope. |
| 18 | Hybrid Runtime Detection of Malicious Containers Using eBPF — DOI 10.32604/cmc.2025.074871 | Computers, Materials & Continua / journal | Direct | Core | Host syscall + network-flow eBPF telemetry | Multiclass ML | Containers/cloud-native | High | Include | Direct multimodal runtime ML study; strong RQ1/RQ2 evidence. |
| 19 | Cordon: Enhancing security through kernel-level control in containerized computing environments — DOI 10.1016/j.cose.2025.104644 | Computers & Security / journal | Direct | Supporting | eBPF/LSM enforcement | None | Containers | Moderate | Include | Strong kernel-enforcement evidence; no ML. |
| 20 | BPFGuard: Multi-Granularity Container Runtime Mandatory Access Control — DOI 10.1109/TCC.2025.3551838 | IEEE Transactions on Cloud Computing / journal | Direct | Supporting | eBPF syscall/LSM/kernel-function controls | None | Kubernetes/containers | High | Include | Strong enforcement granularity and performance evidence. |
| 21 | **REPLACEMENT:** Deep Analysis of Containerized Web Server Performance Using eBPF-Captured Data — DOI 10.1002/tee.70070 | IEEJ Transactions on Electrical and Electronic Engineering / journal | Adjacent | Supporting | eBPF per-container syscall monitoring via BCC/probe events | Random Forest regression | Docker 3-tier web application | High | Include | Direct full text; strong container telemetry and resource-performance evidence. Replaces unavailable P021. |
| 22 | eBPF-Based Container Activity Analysis System — DOI 10.3745/TKIPS.2024.13.9.404 | Transactions of KIPS / journal | Direct | Supporting | eBPF event collection and container metadata | None | Containers/cloud | High | Include | Useful telemetry/tool comparison evidence; not ML-centric. |
| 23 | Optimus: Association-Based Dynamic System Call Filtering for Container Attack Surface Reduction — DOI 10.1186/s13677-024-00639-3 | Journal of Cloud Computing / journal | Direct | Supporting | eBPF syscall monitoring + runtime filtering | Association analysis, not ML detection | Containers | High | Include | Strong real-container runtime enforcement and overhead evidence. |
| 24 | Coda: Runtime Detection of Application-Layer CPU-Exhaustion DoS Attacks in Containers — DOI 10.1109/TSC.2022.3194266 | IEEE Transactions on Services Computing / journal | Direct | Supporting | eBPF runtime CPU monitoring | None | Containers | Moderate | Include | Primary container runtime detection/overhead study; ML is not central. |
| 25 | Hela: A System Call Restriction Framework for Protecting the Entire Containers Lifecycle — DOI 10.1109/TCC.2026.3677796 | IEEE Transactions on Cloud Computing / journal | Direct | Supporting | seccomp + eBPF syscall restriction | ASES scoring, not ML | Container lifecycle | High | Include | Strong lifecycle enforcement and attack-surface evidence. |
| 26 | BeaCon: Automatic Container Policy Generation Using Environment-Aware Dynamic Analysis — DOI 10.1016/j.cose.2025.104789 | Computers & Security / journal | Direct | Supporting | eBPF syscall/capability monitoring | Heuristic scoring, not ML | Docker containers | High | Include | Primary automated policy-generation/enforcement study; directly informs safety/functionality trade-offs. |
| 27 | Vaccine: Injection Vulnerabilities Mitigation Through Dynamic Process Control with eBPF — DOI 10.1016/j.cose.2025.104788 | Computers & Security / journal | Adjacent | Supporting | eBPF dynamic process control | Behavioural deviation analysis, not ML | Linux processes | High | Include | Strong active-response evidence but not Kubernetes/ML. |
| 28 | Preventing IP Spoofing in Kubernetes Using eBPF — DOI 10.32604/cmc.2025.062628 | Computers, Materials & Continua / journal | Direct | Supporting | eBPF packet validation integrated with CNI | Rule/validation logic | Kubernetes/AWS EKS | High | Include | Direct Kubernetes network enforcement and overhead evidence. |
| 29 | KubeAegis: A Unified Security Policy Management Framework for Containerized Environments — DOI 10.1109/ACCESS.2024.3487990 | IEEE Access / journal | Direct/adjacent | Supporting | Policy integration across container security mechanisms | None | Container/cloud-native | Moderate | Include | Useful policy-management context for enforcement integration; not ML-centric. |
| 30 | KubeRosy: A Dynamic System Call Filtering Framework for Containers — DOI 10.1109/ACCESS.2024.3486772 | IEEE Access / journal | Direct | Supporting | eBPF + LSM argument-aware syscall filtering | None | Containers | Moderate | Include | Direct runtime enforcement/overhead evidence. |
| 31 | **REPLACEMENT:** Evaluasi Efektivitas Firewall Pre-filtering berbasis eBPF/XDP menggunakan Random Forest untuk Deteksi Anomali Trafik pada Docker Swarm — DOI 10.30865/jurikom.v13i2.9618 | JURIKOM / journal | Direct | Core | eBPF/XDP at NIC-driver path with eBPF config_map thresholds | Random Forest | Docker Swarm overlay network | High | Include | Direct full-text PDF; eBPF/XDP + ML + container orchestration with quantitative detection, response and CPU-overhead evaluation. Replaces unavailable P031. |
| 32 | Kunerva: Automated Network Policy Discovery Framework for Containers — DOI 10.1109/ACCESS.2023.3310281 | IEEE Access / journal | Adjacent | Supporting | Network-log policy discovery | Policy verification; no ML | Containers/Kubernetes | Moderate | Include | Useful policy-generation/enforcement complement; not eBPF/ML core. |
| 33 | From Container to Cluster: Chained Escape Attacks in Kubernetes and Orchestration Platforms — DOI 10.1109/ACCESS.2025.3627543 | IEEE Access / journal | Direct security context | Supporting | eBPF is not the central mechanism | None | Kubernetes/orchestration | Moderate | Include | Threat-model evidence for chained escapes and requirements on runtime enforcement; not a detection benchmark. |
| 34 | **REPLACEMENT:** Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks — DOI 10.1109/TCC.2026.3657486 | IEEE Transactions on Cloud Computing / journal | Direct | Core | Zero-copy eBPF syscall collection | Lightweight ML + container-specific online learning | Kubernetes/cloud-native microservices | High | Include | Strong replacement: primary journal study directly addressing eBPF telemetry, ML placement/adaptation, overhead and container isolation. |
| 35 | A Framework for eBPF-Based Network Functions in an Era of Microservices — DOI 10.1109/TNSM.2021.3055676 | IEEE TNSM / journal | Adjacent | Supporting | Polycube/eBPF/XDP in-kernel networking | None | Microservices/Kubernetes | High | Include | Strong architecture/placement evidence; not runtime ML security. |
| 36 | ESX: A Self-Generated Control Policy for Remote Access With SSH Based on eBPF — DOI 10.1109/ACCESS.2024.3450496 | IEEE Access / journal | Adjacent | Supporting | eBPF runtime monitoring/policy generation | Behavioural policy generation | Linux/SSH | Moderate | Include | Useful adaptive policy/enforcement evidence; indirect container relevance. |
| 37 | Secure Namespaced Kernel Audit for Containers — DOI 10.1145/3472883.3486976 | ACM SoCC '21 / conference | Direct | Core | saBPF namespace-aware audit | IDS/access-control logic | Kubernetes/containers | High | Include | Strong direct container audit/IDS primary study and systems venue. |
| 38 | Malware Detection in Cloud Native Environments — DOI 10.1145/3719384.3719465 | ACM AICCC 2024 / conference | Direct | Core | SkyShark custom eBPF sensor | ML ensemble | Cloud-native/Kubernetes | High | Include | Direct cloud-native eBPF + ML malware/RCE detection study. |
| 39 | Cross Container Attacks: The Bewildered eBPF on Clouds | USENIX Security '23 / conference | Direct security context | Supporting | Offensive eBPF tracing/permission model | None | Containers/cloud services/Kubernetes | High | Include | High-quality primary threat study; essential for the safety side of the review. |
| 40 | Comparative Analysis of eBPF-Based Runtime Security Monitoring Tools in Monitoring and Threat Detection on Kubernetes — DOI 10.5220/0014272700004928 | RITECH 2025 / conference | Direct | Supporting | Falco/Tetragon/Tracee eBPF monitoring | None | Kubernetes | High | Include | Direct comparative runtime-security benchmark; useful for MTTD, detection, CPU and memory baselines. |

## Explicit exclusions / changes

| Candidate | Decision | Reason |
|---|---|---|
| Extended Berkeley Packet Filter: An Application Perspective (old #34) | EXCLUDE FROM PRIMARY SET; retain as background | IEEE explicitly identifies it as a review of eBPF applications. It does not provide a primary runtime-security experiment. |
| AI-Enhanced Runtime Security for Kubernetes: Real-Time Threat Detection with eBPF Telemetry and Ensemble Learning | NOT selected as replacement | The retrieved record is primarily a discussion/synthesis of AI approaches rather than a sufficiently evidenced primary experimental study for this review. |
| Adaptive Runtime Security for Kubernetes Using eBPF Telemetry and Machine Learning | NOT selected as replacement | Verified as a 2026 IEEE conference paper, not a journal; keeping it would disturb the required 36-journal/4-conference composition. It remains useful background/candidate evidence outside the frozen 40. |

## Count check

- **Retained primary studies:** 40
- **Journals:** 36
- **Peer-reviewed conferences:** 4
- **Journal percentage:** 90.0%
- **Core:** 14
- **Supporting/adjacent:** 26
- **Background:** 0 in the primary set
- **Excluded from primary set during this screen:** 1 old candidate (replaced)
- **Duplicate studies removed:** 0
- **Preprint-only studies retained:** 0
- **Retraction flags:** 0 in the scholarly identifier audit

## Important interpretation

The 90% journal ratio is satisfied **after a substantive eligibility correction**, not by relabeling a survey as a primary study. The replacement was selected because it is materially closer to the frozen research questions than the excluded survey.

The next phase is paper acquisition/archive. Detailed field-by-field extraction, quality scoring/categories, and final research-gap claims remain deliberately unfrozen until CHAT 02/03.


## Replacement audit — 5 October 2026

P021 and P031 were unavailable in the corpus and were replaced with directly accessible primary journal studies. Both replacements preserve the 36-journal/4-conference composition.
