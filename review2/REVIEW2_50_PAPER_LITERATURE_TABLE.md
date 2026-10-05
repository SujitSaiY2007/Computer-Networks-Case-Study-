# Review 2 — 50-Paper Literature Survey Table

**Date:** 5 October 2026  
**Purpose:** Review 2 presentation compliance with the faculty requirement of **minimum 50 references and a literature-survey table covering all 50 papers**.

## Corpus rule

The project retains the **canonical 40-study primary evidence baseline** unchanged:

- 40 primary studies
- 36 journal articles
- 4 peer-reviewed conference papers
- 90% journals
- P001–P040 remain the primary evidence IDs used by CHAT 01–06.

For Review 2, the presentation literature corpus is expanded to **50 references** by adding **10 carefully selected supporting/background studies (R041–R050)**. These ten do **not** replace, renumber, or alter the canonical 40 primary studies.

The 10 additions were selected because they directly strengthen one or more Review 2 dimensions: cloud/container runtime security, eBPF telemetry, service-mesh/cloud-native performance, ML/kernel placement context, enforcement safety, verifier/security constraints, or evidence-synthesis context.

**Important:** R041–R050 are presentation/supporting references. Secondary studies/reviews among them are explicitly labelled and are not counted as primary evidence.

## Required Review 2 fields

| S.No. | Paper title | Journal / venue + year | Dataset / workload / evidence base | Methodology / algorithm | Advantages / novelty relevant to this review | Disadvantages / gaps / limitations |
|---:|---|---|---|---|---|---|
| 1 | An In-Depth Analysis of eBPF-Based System Security Tools in Cloud-Native Environments | IEEE Access, 2025 | Kubernetes microservice security cases; KubeArmor, Falco, Tetragon, Tracee | Comparative architecture, auditing, performance and case-study evaluation | Direct cloud-native runtime-security baseline; compares widely used eBPF security tools | Tool-centric; no ML detection; findings depend on tested tools/scenarios |
| 2 | Real-Time eBPF/XDP-Based Deep Learning Framework for Anomaly Traffic Detection in Internet of Things Networks | IEEE Internet Computing, 2026 | CICDDoS2019, IoT-23, TON_IoT; Raspberry Pi 4B | eBPF/XDP interception + dynamic feature selection + lightweight deep model | Demonstrates hybrid kernel/user-space ML and feature-reduction trade-offs | IoT rather than Kubernetes/container runtime; network anomaly focus |
| 3 | CODAX: eBPF-Based Runtime Detection of Semantic DDoS Attacks in Linux Containers | IEEE Access, 2025 | Linux/Docker container workloads and semantic DDoS scenarios | eBPF runtime telemetry + semantic CPU-exhaustion detection | Direct container-runtime security; evaluates detection latency and overhead | Attack-specific; broader generalization remains to be demonstrated |
| 4 | Low-Overhead Passive Resilience Monitoring for AIoT Gateways: End-to-End Anomaly Detection via eBPF Timing Traces and Autoencoders | IEEE Access, 2026 | AIoT gateway timing traces / resilience anomalies | eBPF timing telemetry + autoencoder + CUSUM | Useful low-overhead telemetry and anomaly-detection evidence | AIoT gateway rather than cloud/container runtime |
| 5 | DeSFAM: An Adaptive eBPF and AI-Driven Framework for Securing Cloud Containers in Real Time | IEEE Access, 2025 | DongTing dataset + real CVE attack scenarios | Dynamic syscall profiling + VAE + Isolation Forest + contextual risk scoring + BPF-LSM | Very close to telemetry → ML → risk → enforcement pipeline; reports detection and enforcement overhead | Dataset and attack-scope limitations may affect external validity |
| 6 | Detecting Cryptojacking Containers Using eBPF-Based Security Runtime and Machine Learning | Electronics, 2025 | Cryptojacking container workloads | Tetragon eBPF syscall/flow telemetry + comparative ML models | Direct cloud-native/container ML detection; strong security-classification evidence | Cryptojacking-specific; limited workload/attack diversity |
| 7 | eBPF: A New Approach to Cloud-Native Observability, Networking and Security for Current (5G) and Future Mobile Networks (6G and Beyond) | IEEE Access, 2023 | Cloud-native/Kubernetes/5G-6G platform scenarios | Architectural eBPF hooks: tracepoints, kprobes, TC, XDP, LSM; Sauron platform | Strong architecture and placement context for cloud-native eBPF observability/security | Broad architecture study; not a controlled ML detection benchmark |
| 8 | BPFast: An eBPF/XDP-based high-performance packet payload inspection system for cloud environments | Journal of KIISE / JKIISC, 2022 | Kubernetes/container network traffic | Kernel-level eBPF/XDP packet header/payload inspection | Demonstrates high-speed cloud/container security inspection and performance benefits | Network payload focus; no ML runtime-behaviour detection |
| 9 | Secure Inter-Container Communications Using XDP/eBPF | IEEE/ACM Transactions on Networking, 2022/2023 | Inter-container communication/network workloads | Bastion+ eBPF/XDP security enforcement and service chaining | Strong container-network enforcement and performance evidence | Network-layer focus; no ML |
| 10 | Container Instrumentation and Enforcement System for Runtime Security of Kubernetes Platform with eBPF | Intelligent Automation & Soft Computing, 2023 | Kubernetes/container runtime security scenario | Tracee/eBPF monitoring + BPF-LSM policy enforcement | Direct Kubernetes runtime monitoring/enforcement baseline | No ML; evaluation scope is framework/testbed oriented |
| 11 | Detection of Denial of Service Attack in Cloud Based Kubernetes Using eBPF | Applied Sciences, 2023 | Cloud Kubernetes DoS/DDoS scenarios | eBPF/XDP traffic monitoring and detection/mitigation | Direct Kubernetes security and resource-overhead evidence | DDoS-specific; limited generalization |
| 12 | Practicality of in-kernel/user-space packet processing empowered by lightweight neural network and decision tree | Computer Networks, 2024 | Packet-classification/IDS workloads | Quantized lightweight NN and decision tree; in-kernel vs user-space eBPF/XDP | Direct common-model placement evidence; exposes verifier/throughput trade-offs | Packet classification rather than container runtime |
| 13 | Enhancing intrusion detection against denial of service and distributed denial of service attacks: Leveraging extended Berkeley packet filter and machine learning algorithms | IET Communications, 2025 | DoS/DDoS network traffic | eBPF kernel capture + DT/RF/SVM/TwinSVM | Direct eBPF + ML comparative detection evidence | Network attack focus rather than Kubernetes runtime |
| 14 | Unsupervised Real-Time In-Kernel Intrusion Detection System Using Autoencoders and eBPF | IEICE Transactions on Communications, 2026 | Network intrusion/anomaly traffic | Quantization-aware autoencoder executed in eBPF | Strong in-kernel ML feasibility/latency context | Network IDS; verifier/model complexity constrains scope |
| 15 | Behavioral Anomaly Detection in Linux Systems using eBPF and LSTM Neural Networks: A Comparative Study with Traditional Machine Learning | International Journal of Computer Applications, 2026 | Linux host behavioural/syscall workloads | eBPF syscall telemetry + LSTM autoencoder vs traditional ML | Behavioural anomaly perspective and ML-family comparison | Host-level rather than cloud-native/container-specific; venue evidence should be interpreted cautiously |
| 16 | A Technique for Accurate Detection of Container Attacks with eBPF and AdaBoost | Journal of The Korea Society of Computer and Information, 2024 | Dirty COW/Dirty Cred attack traces from MongoDB, PostgreSQL and Redis container workloads | eBPF syscall monitoring + AdaBoost | Container-specific ML detection with explicit attack workloads | Narrow attack/application set; generalization requires further evidence |
| 17 | An Abnormal File Access Detection Model for Containers Based on eBPF Listening | Mathematics, 2026 | Container file-access traces / abnormal file-access scenarios | eBPF file-access monitoring + semantic path representation + attention-enhanced autoencoder | Fine-grained file telemetry and false-positive-aware anomaly detection | File-access specific; not a complete runtime-security pipeline |
| 18 | Hybrid Runtime Detection of Malicious Containers Using eBPF | Computers, Materials & Continua, 2026 | Six malicious + four benign container scenarios | Hybrid eBPF host syscall + network-flow telemetry with multiclass ML | Direct multimodal container-runtime evidence; compares telemetry modalities | Scenario count is bounded; external validity needs broader workloads |
| 19 | Cordon: Enhancing security through kernel-level control in containerized computing environments | Computers & Security, 2025 | Real-world container workloads and attack vectors | Deployment-file policy generation + eBPF/LSM runtime enforcement | Autonomous, fine-grained container enforcement with performance evaluation | No ML; policy generation depends on deployment intent extraction |
| 20 | BPFGuard: Multi-Granularity Container Runtime Mandatory Access Control | IEEE Transactions on Cloud Computing, 2025 | Kubernetes/container runtime access-control workloads | Multi-granularity syscall/LSM/kernel-function MAC using eBPF and Kubernetes metadata | Strong enforcement granularity and benchmark evidence | Enforcement-focused; no ML |
| 21 | Deep Analysis of Containerized Web Server Performance Using eBPF-Captured Data | IEEJ Transactions on Electrical and Electronic Engineering, 2025 | Docker three-tier containerized web-server workloads | eBPF per-container syscall monitoring + Random Forest regression | Quantitative CPU/memory/disk-I/O telemetry useful for overhead baselines | Performance rather than security/detection; workload-specific |
| 22 | eBPF-based Container Activity Analysis System | Journal of Korean Institute of Information Processing Systems, 2024 | Container/host activity events | eBPF event collection and comparative analysis of Tetragon, Falco and Tracee | Useful telemetry/tool taxonomy | Monitoring-centric; no ML |
| 23 | Optimus: association-based dynamic system call filtering for container attack surface reduction | Journal of Cloud Computing, 2024 | 71 real Docker Hub container images | eBPF syscall monitoring + association analysis + dynamic syscall filtering | Real-container evaluation; dynamic attack-surface reduction and serviceability measurements | No ML anomaly detection; policy correctness remains important |
| 24 | Coda: Runtime Detection of Application-Layer CPU-Exhaustion DoS Attacks in Containers | IEEE Transactions on Services Computing, 2023 | Container application-layer CPU-exhaustion workloads | eBPF per-connection CPU-time monitoring and detection | Strong runtime detection/overhead evidence | DoS-specific |
| 25 | Hela: A System Call Restriction Framework for Protecting the Entire Containers Lifecycle | IEEE Transactions on Cloud Computing, 2026 | Container runtime/application lifecycle | Seccomp + eBPF syscall restriction and attack-surface scoring | Lifecycle-wide enforcement perspective | Enforcement rather than ML detection |
| 26 | BeaCon: Automatic container policy generation using environment-aware dynamic analysis | Computers & Security, 2026 | Real-world Docker containers; 45 known vulnerabilities + PoCs | Environment-aware dynamic analysis + eBPF syscall/capability monitor + security/functionality scoring | Automated policy generation; explicitly balances security and functionality | Policy-generation focus; not ML detection |
| 27 | Vaccine: Injection vulnerabilities mitigation through dynamic process control with eBPF | Computers & Security, 2026 | 40 injection vulnerabilities + 436 malware instances | eBPF PID/process control + behavioural inference | Active process-level response evidence | Host/process focus rather than Kubernetes runtime; not an ML-placement comparison |
| 28 | Preventing IP Spoofing in Kubernetes Using eBPF | Computers, Materials & Continua, 2025 | Kubernetes/EKS network traffic | eBPF packet validation integrated with Kubernetes CNI | Real Kubernetes deployment and blocking/overhead evaluation | IP-spoofing specific |
| 29 | KubeAegis: A Unified Security Policy Management Framework for Containerized Environments | IEEE Access, 2024 | Heterogeneous container security mechanisms | Unified policy representation, conversion and recommendation | Useful policy-integration layer across security mechanisms | No ML; integration complexity |
| 30 | KubeRosy: A Dynamic System Call Filtering Framework for Containers | IEEE Access, 2024 | Kubernetes/container runtime syscall workloads | eBPF + LSM dynamic syscall filtering with argument-aware policies | Strong runtime enforcement and low-overhead evidence | No ML; policy correctness remains central |
| 31 | Evaluasi Efektivitas Firewall Pre-filtering berbasis eBPF/XDP menggunakan Random Forest untuk Deteksi Anomali Trafik pada Docker Swarm | JURIKOM, 2026 | Docker Swarm anomalous/DDoS traffic | Offline Random Forest → threshold/rule conversion → eBPF/XDP kernel pre-filtering | Direct eBPF + ML + container orchestration and mitigation measurements | Docker Swarm/DDoS-specific; external validity requires broader testing |
| 32 | Kunerva: Automated Network Policy Discovery Framework for Containers | IEEE Access, 2023 | Container network logs/flows | Automated network-policy discovery and verification | Strong policy-generation complement for cloud-native security | Not ML/eBPF core |
| 33 | From Container to Cluster: Chained Escape Attacks in Kubernetes and Orchestration Platforms | IEEE Access, 2025 | Chained container-escape attack scenarios | Threat/attack-chain analysis and defence mapping | Strong threat-model context for runtime enforcement | Threat analysis rather than detection benchmark |
| 34 | Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks | IEEE Transactions on Cloud Computing, 2026 | Kubernetes/cloud-native microservices and evolving workloads | Zero-copy eBPF syscall collection + lightweight ML + container-specific online learning + isolation | Directly connects telemetry, ML, adaptation and response in cloud-native runtime security | Strong single-system evidence; common-protocol comparison with other placements remains limited |
| 35 | A Framework for eBPF-Based Network Functions in an Era of Microservices | IEEE Transactions on Network and Service Management, 2021 | Linux/Kubernetes network-function workloads | Polycube eBPF/XDP network-function chaining with user-space control plane | Strong programmable in-kernel architecture and placement evidence | Networking/NFV focus; no ML runtime security |
| 36 | ESX: A Self-Generated Control Policy for Remote Access With SSH Based on eBPF | IEEE Access, 2024 | SSH remote-access behaviour | eBPF syscall monitoring + itemset-mining behavioural policy generation | Adaptive policy-generation evidence | SSH-specific; indirect container relevance |
| 37 | Secure Namespaced Kernel Audit for Containers | ACM SoCC, 2021 | Kubernetes container audit/security events | saBPF container-granular eBPF/LSM auditing, IDS and access control | High-fidelity container-granular audit evidence | Conference; no ML |
| 38 | Malware Detection in Cloud Native Environments | ACM AICCC, 2024 | Cloud-native malware/RCE behaviours | SkyShark eBPF sensor + ML ensemble | Direct cloud-native eBPF + ML malware detection | Conference; dataset/scenario breadth requires cautious interpretation |
| 39 | Cross Container Attacks: The Bewildered eBPF on Clouds | USENIX Security, 2023 | Cloud/container/Kubernetes offensive scenarios | eBPF permission/attack analysis and exploit demonstrations | High-quality threat-model and meta-security evidence | Offensive-security focus; not a defensive ML benchmark |
| 40 | Comparative Analysis of eBPF-Based Runtime Security Monitoring Tools in Monitoring and Threat Detection on Kubernetes | SCITEPRESS RITECH, 2025 | Kubernetes container escape, DoS and cryptomining scenarios | Falco/Tetragon/Tracee comparative runtime monitoring | Direct baseline for MTTD, detection rate, FPR, CPU and memory | Conference; tool-centric and not ML-focused |
| **41** | **KRAKENGUARD: Towards Fine-Grained eBPF Isolation** | **USENIX NSDI, 2026** | Real-world eBPF programs, known CVEs and an XDP-as-a-Service multi-tenant use case | Policy-driven eBPF bytecode checking using symbolic execution; helper/memory/map/return-value constraints and cross-program interference analysis | Directly strengthens the safety/isolation dimension; supports multi-tenant and eBPF meta-security discussion | Security of the eBPF execution substrate rather than runtime ML detection; no container-ML benchmark |
| **42** | **BeeBox: Hardening BPF against Transient Execution Attacks** | **USENIX Security, 2024** | Linux BPF prototype; Katran benchmark and end-to-end seccomp-BPF/packet-filtering workloads; Spectre-PHT/Spectre-STL | SFI-like BPF sandboxing + static analysis + selective enforcement checks | Strong eBPF meta-security and overhead evidence; reports 20% Katran overhead vs 112% for current Linux mitigations and <1% end-to-end throughput degradation | Focuses on transient-execution threats, not cloud-runtime ML; security hardening adds implementation complexity |
| **43** | **Validating the eBPF Verifier via State Embedding** | **USENIX OSDI, 2024** | eBPF verifier test corpus / generated state-embedded programs | State-embedding technique for checking verifier approximation correctness | Revealed 15 previously unknown verifier logic bugs in one month, including exploitable cases; directly informs feasibility/safety of kernel-local ML | Verifier validation rather than runtime security detection; findings concern correctness/security, not detection accuracy |
| **44** | **Enhancing Packet Tracing of Microservices in Container Overlay Networks using eBPF** | **ACM AINTEC, 2022** | Kubernetes open-source microservice benchmarks and container overlay networks | eBPF-based distributed tracing; trace-context relocation + kernel timestamps for latency measurement | Direct cloud-native telemetry/latency methodology; reduced HTTP payload search space by about 80% without significant end-to-end latency change | Conference and tracing-focused; no ML or enforcement |
| **45** | **Monitoring Network Flows in Containerized Environments** | **LNCS, 2022** | Containerized/serverless network-flow workloads | bpfFlowMon: eBPF TC-hook flow inspector + user-space flow handling + management daemon | Clear hybrid telemetry architecture and explicit feasibility/performance investigation | Book chapter rather than journal/conference primary study; network-flow focus and no ML |
| **46** | **Network shortcut in data plane of service mesh with eBPF** | **Journal of Network and Computer Applications, 2024** | Istio Bookinfo and HipsterShop microservice benchmarks | eBPF socket redirection + TC redirection; latency-distribution analysis | Direct cloud-native performance evidence; up to 21% request-latency reduction, 1.73% CPU reduction and ~0.98% memory reduction | Optimization rather than security/ML; results depend on service-mesh topology and workloads |
| **47** | **Design and implementation of an intrusion detection system by using Extended BPF in the Linux kernel** | **Journal of Network and Computer Applications, 2022** | Modified Snort ruleset and network packet/IDS workloads | Two-stage IDS: eBPF kernel pattern pre-filtering + user-space rule matching | Direct kernel/user-space placement rationale; reported up to 3× throughput over Snort under tested conditions | Network IDS rather than container runtime; fixed rule matching rather than ML |
| **48** | **SoK: Run-time security for cloud microservices. Are we there yet?** | **Computers & Security, 2023** | Systematization of 807 initially identified papers, 48 retained publications and 30+ industry tools | Structured literature/systematization study with architectural-layer, security-property, solution and verification/validation taxonomy | Strong secondary context for cloud-microservice runtime-security gaps; explicitly highlights weak reproducibility and lack of benchmarks/PoCs | Secondary study; not primary evidence and predates several recent eBPF developments |
| **49** | **A Container Security Survey: Exploits, Attacks, and Defenses** | **ACM Computing Surveys, 2025** | Broad container-security literature covering exploits, attacks and defenses | Comprehensive survey/taxonomy of container threats and defenses, including eBPF's dual security role | Strong background for container threat model, shared-kernel risk and defense landscape | Secondary study; broad container scope rather than focused eBPF+ML evaluation |
| **50** | **eBPF-based cybersecurity mechanisms: a systematic literature review** | **International Journal of Information Security, 2026** | 3,735 screened records; 54 peer-reviewed primary studies (2018–2026) | PRISMA-based systematic review and seven-domain eBPF cybersecurity taxonomy | Most recent broad eBPF-security synthesis; directly informs comparison, verifier constraints, portability, meta-security and standardized-evaluation gaps | Secondary study and broader than this project; must be used for context/comparison, not as proof of the project's own gaps |

## How the 50-paper set is used

### Primary evidence

**P001–P040** remain the canonical primary-study evidence base used by CHAT 01–06.

### Supporting/background literature

**R041–R050** expand the Review 2 presentation/reference corpus without changing the primary evidence baseline.

Their roles are intentionally complementary:

- **R041–R043:** eBPF meta-security, verifier safety and multi-tenant isolation.
- **R044–R047:** telemetry, cloud-native latency, kernel/user-space processing and placement context.
- **R048–R050:** secondary literature that helps position the project against existing surveys/systematizations.

### Review 2 narrative rule

The presentation must not imply that all 50 papers are equivalent primary evidence.

Use:

> **50 references surveyed = 40 primary studies + 10 supporting/background references**

and retain:

> **Primary evidence baseline = 40 studies, 36 journals + 4 peer-reviewed conferences (90% journals).**

## Review 2 synthesis dimensions

The 50-paper table should be synthesized rather than presented as 50 isolated summaries:

**Telemetry → feature representation → ML placement → detection → enforcement/mitigation**

and compared using:

**detection quality ↔ latency ↔ CPU/memory/event-processing overhead ↔ safety ↔ reproducibility**

The ten added references specifically strengthen the presentation's treatment of:

1. eBPF runtime/meta-security;
2. verifier and isolation constraints;
3. cloud-native telemetry/latency;
4. kernel vs user-space processing;
5. service-mesh performance;
6. broader container-runtime threat context;
7. current secondary-review positioning.

## Provenance and access notes

The ten additions were selected only after checking accessible scholarly/publisher/author sources. The project should record the actual access route used for each addition in the Review 2 reference register.

Full-text status must remain distinct from bibliographic verification. If a source was only inspected through an authoritative abstract/metadata page, do not claim full-text extraction from it.

## Citation records

- R041: Patel, J., Buhl-Nielsen, L.G., Ghosn, A. & Kogias, M. (2026), *KRAKENGUARD: Towards Fine-Grained eBPF Isolation*, USENIX NSDI 2026. DOI: none required; USENIX proceedings.
- R042: Jin, D., Gaidis, A.J. & Kemerlis, V.P. (2024), *BeeBox: Hardening BPF against Transient Execution Attacks*, USENIX Security 2024.
- R043: Sun, H. & Su, Z. (2024), *Validating the eBPF Verifier via State Embedding*, USENIX OSDI 2024.
- R044: Lee, C., Yoshitani, R. & Hirotsu, T. (2022), *Enhancing Packet Tracing of Microservices in Container Overlay Networks using eBPF*, ACM AINTEC 2022, DOI: 10.1145/3570748.3570756.
- R045: Repetto, M. & Carrega, A. (2022), *Monitoring Network Flows in Containerized Environments*, LNCS 13300, DOI: 10.1007/978-3-031-04036-8_2.
- R046: Yang, W., Chen, P., Yu, G., Zhang, H. & Zhang, H. (2024), *Network shortcut in data plane of service mesh with eBPF*, Journal of Network and Computer Applications 222, 103805, DOI: 10.1016/j.jnca.2023.103805.
- R047: Wang, S.-Y. & Chang, J.-C. (2022), *Design and implementation of an intrusion detection system by using Extended BPF in the Linux kernel*, Journal of Network and Computer Applications 198, 103283, DOI: 10.1016/j.jnca.2021.103283.
- R048: Minna, F. & Massacci, F. (2023), *SoK: Run-time security for cloud microservices. Are we there yet?*, Computers & Security 127, 103119, DOI: 10.1016/j.cose.2023.103119.
- R049: Jarkas, O., Ko, R., Dong, N. & Mahmud, M.R. (2025), *A Container Security Survey: Exploits, Attacks, and Defenses*, ACM Computing Surveys 57(7), 170, DOI: 10.1145/3715001.
- R050: Kostopoulos, S., Tsakonas, P. & Markakis, E.K. (2026), *eBPF-based cybersecurity mechanisms: a systematic literature review*, International Journal of Information Security 25, 150, DOI: 10.1007/s10207-026-01326-x.

## Final status

**Review 2 literature requirement: SATISFIED at the corpus level.**

The presentation now has a defensible 50-reference literature corpus while preserving the integrity of the 40-study primary evidence baseline.

No final experimental result, superiority claim or novelty claim is implied by this literature-corpus expansion.
