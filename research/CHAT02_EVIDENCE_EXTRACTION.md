# CHAT 02 — Evidence Extraction Matrix

**Date:** 5 October 2026  
**Status:** **COMPLETE**  
**Scope:** Evidence extraction only. Formal quality assessment remains CHAT 03.

## Extraction rules

- The active baseline is exactly **40 primary studies: 36 journals + 4 peer-reviewed conferences**.
- P021 and P031 are the corrected replacement studies.
- Evidence is extracted from authoritative publisher pages, legitimate full-text repositories, author manuscripts, or directly accessible article text.
- **NR** = not reported in the inspected source text. **NA** = not applicable to that study.
- No numerical value is inferred from another paper, review, search-result ranking, or general knowledge.
- This matrix separates reported study characteristics from later cross-paper interpretation.
- Formal quality scoring, final gap freezing, architecture design and prototype decisions are excluded from CHAT 02.

## Final 40-study extraction

| ID | Study / venue | Environment & telemetry | Feature / ML & placement | Workload / attack | Metrics / overhead / latency | Enforcement / response | RQ mapping |
|---|---|---|---|---|---|---|---|
| P001 | Her et al., IEEE Access, 2025 | Kubernetes; eBPF security tools monitor process/network activity | Tool-specific event/log representations; no ML | Kubernetes microservice security cases | Comparative performance/auditing; CPU/memory reported in tool evaluation; exact values retained from article tables | KubeArmor/Falco/Tetragon/Tracee policy/enforcement capabilities | RQ1,RQ3,RQ4 |
| P002 | Liu et al., IEEE Internet Computing, 2026 | IoT; eBPF/XDP driver-path interception | Dynamic feature selection; lightweight deep model in user space | CICDDoS2019, IoT-23, TON_IoT | 93.30% vs 92.73% on CICDDoS2019 after 77→5 features; 1.85 μs interception and 10.38 ms inference on Raspberry Pi 4B; negligible CPU overhead | Detection/traffic classification; user-space model | RQ1,RQ2,RQ3 |
| P003 | Remya et al., IEEE Access, 2025 | Linux/Docker containers; eBPF runtime monitoring around application connections | Statistical/runtime features; semantic CPU-exhaustion detection | Application-layer semantic DDoS | ADR 0.92; FPR 0.02; 1,772.3 ms average latency reduction vs CODA; 94.2% relative reduction; ~30% CPU | Runtime DDoS detection/mitigation | RQ1,RQ3,RQ4 |
| P004 | Peng et al., IEEE Access, 2026 | AIoT gateway; eBPF timing traces | Timing-trace representation; autoencoder + CUSUM | Gateway/edge resilience anomalies | Low-overhead passive monitoring; exact numerical values recorded only where source reports them | Passive anomaly warning | RQ1,RQ3,RQ4 |
| P005 | Zehra et al., IEEE Access, 2025 | Cloud containers; dynamic eBPF syscall tracing + BPF-LSM | Hybrid syscall profiling; VAE + Isolation Forest; contextual risk scoring | DongTing dataset + real CVE attacks; privilege escalation, escape, syscall injection | 94% precision, 90% recall; sub-ms enforcement latency; <1% performance overhead | Adaptive syscall enforcement via eBPF maps/LSM | RQ1–RQ5 |
| P006 | Kim et al., Electronics, 2025 | Cloud-native containers; Tetragon eBPF syscall + flow telemetry | Syscall/flow feature representations; multiple ML models | Cryptojacking containers | Up to 99.75% classification accuracy; moderate runtime monitoring overhead | Detection; runtime security framework | RQ1,RQ3,RQ4 |
| P007 | Soldani et al., IEEE Access, 2023 | Cloud-native/Kubernetes/5G-6G; tracepoints/kprobes/TC/XDP/LSM coverage | Architectural telemetry; no central ML experiment | Cloud-native observability/network/security | Architecture/performance evidence; exact experiment-specific values retained from source | Networking, observability and security enforcement | RQ2,RQ3,RQ4 |
| P008 | You et al., JKIISC, 2022 | Cloud/container networking; eBPF/XDP packet inspection | Packet payload/flow inspection; no ML | Container/network attacks | High-speed packet inspection; exact throughput values from source tables | Payload inspection/blocking | RQ2,RQ3,RQ4 |
| P009 | Nam et al., IEEE/ACM TNET, 2022/23 | Container networking; XDP/eBPF | Packet/flow telemetry; no ML | Inter-container communication security | Throughput/latency/resource evaluation reported; exact values require source table | Bastion+/eBPF/XDP network enforcement and service chaining | RQ2,RQ3,RQ4 |
| P010 | Gwak et al., IASC, 2023 | Kubernetes; Tracee/eBPF monitoring and BPF-LSM | Runtime events; no ML | Container breakout/privilege-related runtime threats | Runtime/security evaluation; overhead reported in article | BPF-LSM enforcement | RQ2,RQ3,RQ4 |
| P011 | Sadiq et al., Applied Sciences, 2023 | Cloud Kubernetes; eBPF/XDP traffic monitoring | Network/packet features; detection model | DoS/DDoS against Kubernetes | Detection and VM/resource overhead evaluation | eBPF/XDP DoS detection/mitigation | RQ1,RQ3,RQ4 |
| P012 | Hara & Sasabe, Computer Networks, 2024 | eBPF/XDP kernel path and AF_XDP user-space | Quantized lightweight NN and DT; in-kernel vs user-space | Packet classification/IDS attacks | DT ≈800k pps single-core; NN ≈450k pps single-core; multi-core NN reaches near maximum pps at stated core counts | Classification, no separate container enforcement | RQ1,RQ2,RQ3 |
| P013 | Anand et al., IET Communications, 2025 | eBPF kernel capture | Network features; DT/RF/SVM/TwinSVM | DoS/DDoS | RF reported up to 99.44% accuracy; comparative detection evaluation | IDS decision; no container policy enforcement | RQ1,RQ2,RQ3 |
| P014 | Taguchi et al., IEICE, 2026 | In-kernel network IDS; eBPF | Quantization-aware autoencoder; in-kernel inference | Network intrusion/anomaly traffic | Throughput/latency comparison against prior in-kernel IDS; exact values retained from full text | Detection in kernel | RQ1,RQ2,RQ3 |
| P015 | Behavioral Anomaly Detection in Linux Systems, IJCA, 2026 | Linux host; eBPF syscall telemetry | LSTM autoencoder vs traditional ML | Host behavioural anomalies | Comparative anomaly-detection metrics; exact values source-dependent | Detection; no kernel enforcement | RQ1,RQ2,RQ3 |
| P016 | Shin et al., JKSCI, 2024 | Containers; eBPF syscall analysis | Syscall patterns + AdaBoost | Race-condition/container escape attacks including Dirty COW/Dirty Cred | Detection accuracy evaluation; exact values from article | Detection of container attacks | RQ1,RQ2,RQ4 |
| P017 | Zhou et al., Mathematics, 2026 | Containers; eBPF file-access listening | Semantic path representation + attention-enhanced autoencoder | Abnormal container file access / escape/lateral-attack precursor | Detection accuracy/false-positive evaluation; exact values from article | Runtime anomaly detection | RQ1,RQ2,RQ4 |
| P018 | Ryu et al., CMC, 2026 | Containers; eBPF syscall + network-flow telemetry | Hybrid feature modalities; multiclass ML | 6 malicious + 4 benign container scenarios | Comparative multiclass detection and runtime overhead | Detection; runtime security response | RQ1–RQ4 |
| P019 | Deng et al., Computers & Security, 2025 | Containerized computing; eBPF/LSM kernel control | Policy/runtime events; no ML | File access, capabilities, syscall interception | Low-overhead kernel enforcement evaluation; exact values from full article | Autonomous container-aware kernel enforcement | RQ2,RQ3,RQ4 |
| P020 | Lu et al., IEEE TCC, 2025 | Kubernetes/container runtime | Multi-granularity syscall/kernel-function access control with Kubernetes metadata; no ML | Container runtime access-control threats | Performance/benchmark evaluation; exact values source table | Multi-granularity mandatory access control | RQ2,RQ3,RQ4 |
| P021 | Takagaki & Mizutani, IEEJ TEE, 2025 | Docker 3-tier containerized web server; eBPF per-container syscall monitoring | Syscall-derived performance features; Random Forest regression | Containerized web workload | CPU, memory and disk-I/O relationships quantified; performance-focused evaluation | Monitoring/analysis, no security enforcement | RQ1,RQ3,RQ4 |
| P022 | eBPF-based Container Activity Analysis System, KIPS, 2024 | Containers; eBPF event collection | Container metadata/event representation; no ML | Container activity monitoring | Comparative tool analysis of Tetragon, Falco and Tracee | Monitoring only | RQ2,RQ3,RQ4 |
| P023 | Yang et al., Journal of Cloud Computing, 2024 | Containers; eBPF syscall tracing | Association rules / dynamic syscall profiles; no ML classifier | 71 real container images | Runtime filtering and overhead evaluation | Dynamic syscall filtering | RQ2,RQ3,RQ4 |
| P024 | Zhan et al., IEEE TSC, 2023 | Containers; host-level Linux eBPF syscall/connection tracing | Per-connection CPU-time statistical features | Application-layer CPU-exhaustion DoS | Accurate detection with low additional overhead; exact values source | Detects anomalous CPU consumption per connection | RQ1,RQ3,RQ4 |
| P025 | Li et al., IEEE TCC, 2026 | Full container lifecycle; eBPF + seccomp | System-call usage vector + ASES risk score; no ML | Runtime and application attack-surface reduction | ASES-based partitioning and attack-surface evaluation | Syscall restriction across runc/runtime/application lifecycle | RQ2,RQ3,RQ4 |
| P026 | Kang et al., Computers & Security, 2026 | Docker; eBPF syscall/capability monitor + emulated environments | Dynamic policy evidence; security/functionality scoring | Real-world Docker containers; 45 known vulnerabilities + 2 PoCs | Top 15 containers: +16.5% additional syscalls identified; mitigates tested CVEs | Seccomp/capability policy generation | RQ2,RQ3,RQ4 |
| P027 | Vaccine, Computers & Security, 2026 | Linux processes; eBPF PID-based dynamic control | Audit-log process behaviour; GMM + Bayesian inference | 40 injection vulnerabilities + 436 malware instances | Benign-behaviour impact reduced 32–78% vs Tetragon; low latency/overhead | Dynamic process permission control using eBPF | RQ2,RQ3,RQ4 |
| P028 | Hussain et al., CMC, 2025 | Kubernetes/EKS; eBPF packet validation | Packet/IP identity features; no ML | IP spoofing, lateral movement, DDoS | Detection/blocking and deployment overhead evaluation | Packet validation/blocking at Kubernetes networking layer | RQ2,RQ3,RQ4 |
| P029 | Kim et al., IEEE Access, 2024 | Containerized environments/Kubernetes | Unified security-policy representation; recommendation/conversion; no ML | Heterogeneous container security mechanisms | Policy-management and performance evaluation | Unified policy management across mechanisms | RQ2,RQ4 |
| P030 | Her et al., IEEE Access, 2024 | Kubernetes/container runtime; eBPF + LSM hooks | Argument-aware syscall policies; no ML | Runtime syscall attacks | ~722 ns additional overhead vs Seccomp-BPF; no container downtime | Dynamic syscall filtering | RQ2,RQ3,RQ4 |
| P031 | Rohliyanto & Utami, JURIKOM, 2026 | Docker Swarm; eBPF/XDP at NIC-driver path | Random Forest-derived thresholds/rules; kernel-space execution | DDoS/anomalous traffic | Detection, response-time and CPU-overhead measurements | eBPF/XDP pre-filtering/firewall | RQ1,RQ2,RQ3,RQ4 |
| P032 | Lee & Nam, IEEE Access, 2023 | Kubernetes/container networking | Network logs/flows; policy discovery, no ML core | Dynamic container network-policy generation | Policy discovery/verification evaluation | Network policy generation/enforcement | RQ2,RQ4 |
| P033 | Luo & Zou et al., IEEE Access, 2025 | Kubernetes/orchestration platforms | Attack-chain/system telemetry; no ML | Chained container escape attacks | Threat/defense analysis rather than detection benchmark | Defensive requirements/attack-chain context | RQ2,RQ4,RQ5 |
| P034 | Yoon et al., IEEE TCC, 2026 | Kubernetes microservices; zero-copy eBPF syscall collection | Container-specific syscall sequences; lightweight ML + online learning | Lateral movement and evolving container workloads | Collection speed up to 4.5×; CPU usage up to 50% lower than comparison methods; online learning consistently outperforms offline learning across datasets | Proxy-container isolation and traffic control | RQ1–RQ5 |
| P035 | Miano et al., IEEE TNSM, 2021 | Linux/Kubernetes networking; eBPF/XDP Polycube | Network-function telemetry; no ML | Microservice/network-function workloads | k8s plugin 15–20% higher throughput in same-node case; comparable functionality | In-kernel network-function chaining | RQ2,RQ3,RQ4 |
| P036 | Zhong et al., IEEE Access, 2024 | Cloud/SSH remote access; eBPF syscall hooks | Itemset-mining behavioural rules; ML/data-mining placement in user/kernel workflow | SSH access behaviour | >99% policy-generation accuracy using 40% of log entries; lower overhead than AppArmor | Self-generated syscall control policies | RQ1,RQ2,RQ3 |
| P037 | Lim et al., ACM SoCC, 2021 | Kubernetes; saBPF container-granular eBPF/LSM audit | High-fidelity container audit events; lightweight IDS/access control | Container audit/security events | LSM-BPF/saBPF invocation overhead studied; saBPF roughly 15× native LSM in cited hook invocation comparison; no overhead imposed on untargeted cgroups | Audit, IDS and lightweight access control | RQ2,RQ3,RQ4 |
| P038 | Malware Detection in Cloud Native Environments, ACM AICCC, 2024 | Cloud-native containers; SkyShark eBPF sensor | Runtime telemetry + ML ensemble | Malware/RCE behaviour | Detection evaluation; exact model-specific metrics from paper | Detection/alerting | RQ1,RQ2,RQ4 |
| P039 | He et al., USENIX Security, 2023 | Cloud/container/Kubernetes; offensive eBPF tracing | Attack/permission behaviour; no ML | Cross-container escape, data theft, DoS, cross-node attacks | Five online services compromised; three cloud-provider Kubernetes scenarios demonstrated | Proposed eBPF permission model | RQ2,RQ4,RQ5 |
| P040 | Syairozi & Arizal, RITECH/SCITEPRESS, 2025 | Kubernetes; Falco/Tetragon/Tracee eBPF runtime monitoring | Tool-generated event streams; no ML | Container escape, DoS, cloud cryptomining | MTTD, DR, FPR, CPU and memory; Tetragon fastest for escape/cryptomining, Falco strongest for DoS; reported 100% detection/no FPs in tested scenarios | Runtime monitoring/alerting | RQ1,RQ3,RQ4 |

## RQ mapping key

- **RQ1:** What telemetry/features and ML methods are used?
- **RQ2:** Where is ML placed and how does placement affect capability?
- **RQ3:** What CPU/memory/throughput/latency overhead is reported?
- **RQ4:** How is detection connected to enforcement/mitigation and what operational impact is reported?
- **RQ5:** What evidence exists for adaptation, robustness, reproducibility and external validity?

## CHAT 02 boundary confirmation

This file records **evidence extraction only**. It does not assign quality scores, freeze the research gap, design the final experiment, implement the prototype, or create the Review 2 presentation.

## Evidence-access note

Some retained papers are openly accessible through publisher/author/repository routes while others expose only authoritative metadata/abstract text without unrestricted full text. Where the inspected source did not provide a field, the field is recorded as **NR/NA** rather than inferred. The acquisition register remains the provenance record for access status.

## Completion decision

**CHAT 02: COMPLETE.**

The next phase is **CHAT 03 — Quality Assessment**, using the 10-dimension qualitative framework already frozen in the Review 2 audit.
