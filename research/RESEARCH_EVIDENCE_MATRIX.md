# Research Evidence Matrix — 45-Study Working Set

**Status:** working canonical evidence set as of 25 August 2026.
**Important:** this is not the final PRISMA-included set. Full-text screening, duplicate checking, quality assessment, and extraction must still be completed.

## Tier definitions

- **Core:** directly studies eBPF-assisted runtime security/detection/enforcement in containers/cloud-native environments.
- **Core/adjacent:** directly combines eBPF and ML/security but the environment or layer is broader than Kubernetes runtime security.
- **Supporting:** does not itself provide the complete eBPF+ML+cloud-native combination, but is important evidence for telemetry overhead, enforcement, verifier safety, or architecture.

| ID | Study | Year | Venue | Tier | Why it matters to this review | Verification/source |
|---:|---|---:|---|---|---|---|
| 1 | An In-Depth Analysis of eBPF-Based System Security Tools in Cloud-Native Environments | 2025 | IEEE Access | Core | Kubernetes runtime security; tool/overhead comparison | Initial uploaded list; bibliographic metadata should be checked in IEEE Xplore |
| 2 | KraKenGuard: Towards Fine-Grained eBPF Isolation in Multi-Tenant Environments | 2026 | USENIX NSDI '26 | Supporting | eBPF isolation, permissions, multi-tenant safety | USENIX |
| 3 | A Flow-Based IDS Using Machine Learning Entirely in eBPF | 2021 | IEEE/ACM-related; arXiv record | Core/adjacent | In-kernel decision-tree ML; avoids kernel/user-space copying | arXiv:2102.09980 |
| 4 | Leveraging eBPF/XDP for Real-Time Machine Learning Traffic Classification in 5G User Plane Functions | 2024 | IEEE/SBRC | Supporting | TinyML Random Forest in XDP; verifier/line-rate trade-off | Initial uploaded list; verify publisher record |
| 5 | Real-Time eBPF/XDP-Based Deep Learning Framework for Anomaly Traffic Detection in Internet of Things Networks | 2026 | IEEE Internet Computing | Supporting | Hybrid XDP feature selection + user-space deep learning | DOI:10.1109/MIC.2026.3692726 |
| 6 | CODAX: eBPF-Based Runtime Detection of Semantic DDoS Attacks in Linux Containers | 2025 | IEEE Access | Core | Container runtime DDoS detection; kernel telemetry and latency | DOI:10.1109/ACCESS.2025.3614389 |
| 7 | eBPF-PATROL: Protective Agent for Threat Recognition and Overreach Limitation in Containerized Environments | 2025 | arXiv | Core | Runtime syscall monitoring and BPF-LSM enforcement | arXiv:2511.18155; verify final venue |
| 8 | Low-Overhead Passive Resilience Monitoring for AIoT Gateways: End-to-End Anomaly Detection via eBPF Timing Traces and Autoencoders | 2026 | IEEE Access | Supporting | Passive eBPF timing telemetry + autoencoder/CUSUM | Initial uploaded list; verify publisher record |
| 9 | FedMon: Federated eBPF Monitoring for Distributed Anomaly Detection in Multi-Cluster Cloud Environments | 2025 | arXiv | Core | Kubernetes multi-cluster eBPF telemetry + VAE/Isolation Forest federated learning | arXiv:2510.10126 |
| 10 | DeSFAM: An Adaptive eBPF and AI-Driven Framework for Securing Cloud Containers in Real Time | 2025 | IEEE Access | Core | Syscall profiling + VAE/iForest + BPF-LSM enforcement | IEEE/DOAJ metadata; verify DOI |
| 11 | Detecting Cryptojacking Containers Using eBPF-Based Security Runtime and Machine Learning | 2025 | Electronics (MDPI) | Core | Tetragon syscall/flow telemetry + ML for cryptojacking | DOI:10.3390/electronics14061208 |
| 12 | Malware Detection in Cloud Native Environments | 2024 | ACM AICCC 2024 | Core | SkyShark eBPF sensor + ML ensemble for cloud-native malware/RCE behavior | Initial uploaded list; verify ACM record |
| 13 | Adaptive Runtime Security for Kubernetes Using eBPF Telemetry and Machine Learning | 2025/2026 | Preprint/technical report | Core | Sidecarless adaptive activation of heavier ML models | Initial uploaded list; verify final publication |
| 14 | AI-Enhanced Runtime Security for Kubernetes: Real-Time Threat Detection with eBPF Telemetry and Ensemble Learning | 2025 | Asian Journal of Research in Computer Science | Core | eBPF + Kafka + IF/LSTM/XGBoost + Kubernetes remediation | Initial uploaded list; verify bibliographic quality |
| 15 | Comparative Analysis of eBPF-Based Runtime Security Monitoring Tools in Monitoring and Threat Detection on Kubernetes | 2025 | SCITEPRESS RITECH | Core | Falco/Tetragon/Tracee comparison under Kubernetes attacks | DOI:10.5220/0014272700004928 |
| 16 | eBPF: A New Approach to Cloud-Native Observability, Networking and Security for Current (5G) and Future Mobile Networks (6G and Beyond) | 2023 | IEEE Access | Supporting | Sauron cloud-native eBPF architecture; observability and enforcement | DOI:10.1109/ACCESS.2023.3281480 |
| 17 | Secure Namespaced Kernel Audit for Containers | 2021 | ACM SoCC '21 | Core | Container-granular eBPF audit, IDS and access control in Kubernetes | DOI:10.1145/3472883.3486976 |
| 18 | BPFContain: Fixing the Soft Underbelly of Container Security | 2021 | arXiv / verify final venue | Supporting | eBPF-based container confinement and policy enforcement | arXiv:2102.06972 |
| 19 | The rise of eBPF for non-intrusive performance monitoring | 2020 | IEEE/IFIP NOMS 2020 | Supporting | Empirical eBPF profiling/tracing for containerized workloads; overhead rationale | DOI:10.1109/NOMS47738.2020.9110434 |
| 20 | BPFast: An eBPF/XDP-based high-performance packet payload inspection system for cloud environments | 2022 | Journal of KIISE/JKIISC | Supporting | Kernel-level container payload inspection; Kubernetes performance | DOI:10.13089/JKIISC.2022.32.2.213 |
| 21 | Secure Inter-Container Communications Using XDP/eBPF | 2023 | IEEE/ACM Transactions on Networking | Supporting | eBPF/XDP security enforcement for inter-container traffic | DOI:10.1109/TNET.2022.3206781 |
| 22 | Enhancing Packet Tracing of Microservices in Container Overlay Networks using eBPF | 2022 | ACM AINTEC '22 | Supporting | eBPF tracing in Kubernetes overlay networks; latency/sidecar trade-off | DOI:10.1145/3570748.3570756 |
| 23 | Container Instrumentation and Enforcement System for Runtime Security of Kubernetes Platform with eBPF | 2023 | Intelligent Automation & Soft Computing | Core | BPF-LSM runtime enforcement and Tracee-based monitoring in Kubernetes | DOI:10.32604/iasc.2023.039565 |
| 24 | Detection of Denial of Service Attack in Cloud Based Kubernetes Using eBPF | 2023 | Applied Sciences (MDPI) | Core | eBPF/XDP DDoS detection/mitigation and VM overhead evaluation | DOI:10.3390/app13084700 |
| 25 | Cross Container Attacks: The Bewildered eBPF on Clouds | 2023 | USENIX Security '23 | Core/supporting | Shows eBPF attack surface, cross-container compromise and permission-model weaknesses | USENIX Security '23 |
| 26 | eBPF-sec: A Defensive Framework Against eBPF Attacks on Containers | 2024 | IEEE ISCC 2024 | Supporting | Defense against offensive eBPF attacks in containers | DOI:10.1109/ISCC61673.2024.10733575 |
| 27 | SafeBPF: Hardware-assisted Defense-in-depth for eBPF Kernel Extensions | 2024 | arXiv | Supporting | Isolation/safety of eBPF runtime; macrobenchmark overhead | arXiv:2409.07508 |
| 28 | BeeBox: Hardening BPF against Transient Execution Attacks | 2024 | USENIX Security '24 | Supporting | BPF runtime hardening against speculative execution; performance/security trade-off | USENIX Security '24 |
| 29 | HIVE: A Hardware-assisted Isolated Execution Environment for eBPF on AArch64 | 2024 | USENIX Security '24 | Supporting | Hardware-assisted eBPF isolation and verifier-equivalent safety | USENIX Security '24 |
| 30 | Validating the eBPF Verifier via State Embedding | 2024 | USENIX OSDI '24 | Supporting | Finds verifier logic bugs; directly relevant to verifier trust and safety | USENIX OSDI '24 |
| 31 | Approximation Enforced Execution of Untrusted Linux Kernel Extensions | 2025 | USENIX Security '25 | Supporting | Constrains execution to verifier approximations to reduce trust in verifier soundness | USENIX Security '25 |
| 32 | The eBPF Runtime in the Linux Kernel | 2024 | arXiv | Supporting | Technical description of eBPF runtime design, verifier and production constraints | arXiv:2410.00026 |
| 33 | Practicality of in-kernel/user-space packet processing empowered by lightweight neural network and decision tree | 2024 | Computer Networks (Elsevier) | Core/adjacent | Quantifies ML packet-processing constraints in eBPF/XDP and kernel/user-space placement | DOI:10.1016/j.comnet.2024.110188 |
| 34 | SmartX Intelligent Sec: A Security Framework Based on Machine Learning and eBPF/XDP | 2024 | arXiv | Core/adjacent | BiLSTM + eBPF/XDP real-time security pipeline | arXiv:2410.20244 |
| 35 | Enhancing intrusion detection against denial of service and distributed denial of service attacks: Leveraging extended Berkeley packet filter and machine learning algorithms | 2025 | IET Communications | Core/adjacent | eBPF kernel capture + DT/RF/SVM/TwinSVM detection | DOI:10.1049/cmu2.12879 |
| 36 | Unsupervised Real-Time In-Kernel Intrusion Detection System Using Autoencoders and eBPF | 2026 | IEICE Transactions on Communications | Core/adjacent | Unsupervised QAT autoencoder inference inside eBPF; packet-rate comparison | DOI:10.23919/transcom.2025EBP3028 |
| 37 | Behavioral Anomaly Detection in Linux Systems using eBPF and LSTM Neural Networks: A Comparative Study with Traditional Machine Learning | 2026 | International Journal of Computer Applications | Supporting | eBPF syscall telemetry + LSTM autoencoder for host anomaly detection | DOI:10.5120/ijca502db8d4e336 |
| 38 | A Technique for Accurate Detection of Container Attacks with eBPF and AdaBoost | 2024 | Journal of The Korea Society of Computer and Information | Core | eBPF syscall patterns + AdaBoost for Dirty COW/Dirty Cred container attacks | DOI:10.9708/jksci.2024.29.06.039 |
| 39 | An Abnormal File Access Detection Model for Containers Based on eBPF Listening | 2026 | Mathematics (MDPI) | Core | eBPF file-access telemetry + attention autoencoder for abnormal container file access | DOI:10.3390/math14060991 |
| 40 | Hybrid Runtime Detection of Malicious Containers Using eBPF | 2026 | Computers, Materials & Continua | Core | Hybrid syscall + network-flow eBPF telemetry with ML multi-class classification | DOI:10.32604/cmc.2025.074871 |
| 41 | Cordon: Enhancing security through kernel-level control in containerized computing environments | 2025 | Computers & Security | Core/supporting | eBPF/LSM fine-grained autonomous container enforcement with low overhead | DOI:10.1016/j.cose.2025.104644 |
| 42 | BPFGuard: Multi-Granularity Container Runtime Mandatory Access Control | 2025 | IEEE Transactions on Cloud Computing | Core/supporting | Multi-granularity eBPF container MAC; Kubernetes metadata and performance | DOI:10.1109/TCC.2025.3551838 |
| 43 | Monitoring and Controlling Internal Container Activity Using LSM + eBPF in a Multi-Container Environment | 2026 | Journal of KIISE | Core/supporting | Container-level syscall/network/file monitoring and LSM enforcement in Kubernetes | DOI:10.5626/JOK.2026.53.1.1 |
| 44 | eBPF-based Container Activity Analysis System | 2024 | Journal of Korean Institute of Information Processing Systems | Supporting | Container/host event analysis and comparison of Tetragon, Falco and Tracee | DOI:10.3745/TKIPS.2024.13.9.404 |
| 45 | Monitoring Network Flows in Containerized Environments | 2022 | Springer LNCS | Supporting | bpfFlowMon telemetry for containerized/serverless flow analysis; useful for telemetry layer | DOI:10.1007/978-3-031-04036-8_2 |

## Planned extraction fields for the final matrix

For every finally included study, extract authors, year, venue/publisher, DOI/persistent identifier, publication status, cloud/container environment, eBPF hook type(s), telemetry granularity, feature representation, ML model, inference placement, dataset/workload, testbed, attack scenario, baselines, CPU overhead, memory overhead, detection metrics, latency, event loss/buffering behavior, enforcement mechanism, reproducibility artifacts, limitations, and reviewer quality notes.


## CHAT 01 verification update — 5 October 2026

The 45-study working matrix has now been screened against the frozen scope and bibliographic records. The old provisional 40-study list contained one non-primary review article: **Extended Berkeley Packet Filter: An Application Perspective** (IEEE Access, 2022, DOI 10.1109/ACCESS.2022.3226269). It is retained as background/comparison literature and is no longer counted as primary evidence.

It was replaced by **Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks** (IEEE Transactions on Cloud Computing, 2026, DOI 10.1109/TCC.2026.3657486), a peer-reviewed journal primary study combining eBPF system-call telemetry, lightweight ML anomaly detection, container-specific online learning and isolation in Kubernetes/cloud-native microservices.

### Verified primary baseline after CHAT 01

- 40 retained primary studies.
- 36 journal articles.
- 4 peer-reviewed conference papers.
- 90.0% journals.
- 14 Core studies.
- 26 Supporting/Adjacent studies.
- 0 preprint-only studies retained.
- 0 duplicate studies removed.
- 0 retraction flags in the scholarly identifier audit.

The detailed screening table, explicit change log, evidence-strength labels and next-stage boundary are in research/CHAT01_FULLTEXT_VERIFICATION.md.

**Important:** this is a verified screening baseline, not yet the detailed extraction/quality-assessment matrix. Missing technical fields remain **NR** until the authoritative full texts are acquired and extracted.

## CHAT 02 corpus-gate checkpoint — 5 October 2026

**Status: BLOCKED — extraction not started.**

The verified 40-study baseline is unchanged: **36 journals + 4 peer-reviewed conferences = 90% journals**. The actual local/library availability check found no retained P001–P040 study PDFs in the mounted workspace or connected Library. The acquisition register remains the authoritative access map: 26 legitimate full-text routes are recorded, while 14 studies require institutional/library access.

Because an inaccessible paper's missing field cannot legitimately be classified as “Not reported,” the detailed extraction matrix has not been populated from inaccessible sources. No quality scoring, cross-paper conclusions, gap freezing, architecture design, prototype work, experiments, or Review 2 slide work was performed in this checkpoint.

**Unresolved access IDs:** P002, P009, P014, P015, P019, P020, P021, P024, P026, P027, P031, P034, P035, P037.

**Next action:** materialize the private/local full-text corpus or obtain legitimate institutional/library access, then resume CHAT 02 extraction.