# Relevancy Audit — Initial Uploaded Research List

## Audit basis
The uploaded `CN Relevant Research Content.docx` contains 18 numbered paper entries across Set 1 and Set 2. The course guide requires the final evidence set to be primary research, within the declared period, directly relevant to the scope, and supported by method/dataset/benchmark/testbed/technical evidence.

## Decision summary

| Initial entry | Decision | Rationale |
|---|---|---|
| An In-Depth Analysis of eBPF-Based System Security Tools in Cloud-Native Environments | INCLUDE — CORE | Direct Kubernetes runtime-security benchmarking and telemetry-overhead evidence. |
| KraKenGuard: Towards Fine-Grained eBPF Isolation in Multi-Tenant Environments | INCLUDE — SUPPORTING | Strong eBPF isolation/safety evidence, but not an ML detection study. |
| A Flow-Based IDS Using Machine Learning Entirely in eBPF | INCLUDE — CORE/ADJACENT | Direct ML + eBPF inference; network IDS rather than container runtime. Verified against arXiv/paper record. |
| Leveraging eBPF/XDP for Real-Time Machine Learning Traffic Classification in 5G User Plane Functions | INCLUDE — SUPPORTING | Strong in-kernel ML placement evidence, but 5G user-plane rather than Kubernetes runtime security. |
| Real-Time eBPF/XDP-Based Deep Learning Framework for Anomaly Traffic Detection in IoT Networks | INCLUDE — SUPPORTING | Hybrid in-kernel/user-space ML evidence; environment is IoT rather than cloud-native containers. |
| CODAX: eBPF-Based Runtime Detection of Semantic DDoS Attacks in Linux Containers | INCLUDE — CORE | Direct container runtime detection and eBPF telemetry. |
| eBPF-PATROL: Protective Agent for Threat Recognition and Overreach Limitation in Containerized Environments | INCLUDE — CORE | Direct container runtime monitoring and BPF-LSM enforcement; publication status must be recorded carefully. |
| Low-Overhead Passive Resilience Monitoring for AIoT Gateways | INCLUDE — SUPPORTING | Useful telemetry/overhead and anomaly-detection evidence, but not cloud-native runtime. |
| FedMon: Federated eBPF Monitoring for Distributed Anomaly Detection in Multi-Cluster Cloud Environments | INCLUDE — CORE | Direct multi-cluster/cloud telemetry + ML architecture; publication status needs verification. |
| DeSFAM | INCLUDE — CORE | Direct eBPF + ML + container security + BPF-LSM enforcement. |
| Detecting Cryptojacking Containers Using eBPF-Based Security Runtime and Machine Learning | INCLUDE — CORE | Direct container runtime ML detection and eBPF telemetry. |
| Malware Detection in Cloud Native Environments | INCLUDE — CORE | Direct cloud-native eBPF sensor + ML detection. |
| Adaptive Runtime Security for Kubernetes Using eBPF Telemetry and Machine Learning | INCLUDE — CORE/CANDIDATE | Very strong scope fit; publication status/venue must be verified before treating as peer-reviewed primary evidence. |
| AI-Enhanced Runtime Security for Kubernetes: Real-Time Threat Detection with eBPF Telemetry and Ensemble Learning | INCLUDE — CORE/CANDIDATE | Direct scope fit, but venue/metadata quality should be checked before final inclusion. |
| Comparative Analysis of eBPF-Based Runtime Security Monitoring Tools in Monitoring and Threat Detection on Kubernetes | INCLUDE — CORE | Direct Kubernetes runtime-security benchmark; not ML-centric but important baseline. |
| eBPF: A New Approach to Cloud-Native Observability, Networking and Security for Current (5G) and Future Mobile Networks | INCLUDE — SUPPORTING | Strong cloud-native eBPF architecture evidence, but broad observability/security and not ML detection. |
| Building AI-Driven Cloud-Native Applications with Kubernetes and Containerization | EXCLUDE FROM PRIMARY SET | Generic MLOps/platform architecture; no direct eBPF runtime-security evidence. Keep only as background if needed. |
| Designing Cloud-Native Reference Architectures for Enterprise-Scale AI/ML Platforms | EXCLUDE FROM PRIMARY SET | Generic enterprise AI/ML architecture; no direct eBPF runtime-security evidence. |

## Important correction
The source document contains **18 entries**, not 22. Four additional papers must therefore be recovered from the earlier working history or supplied by the team before claiming that the original collection contained 22.

## Evidence-quality rule
Do not copy numerical claims from the source document into the manuscript without checking the original paper. The source document contains missing/garbled numeric fields. The course guide explicitly requires verification of automatically imported references and warns against treating generated summaries as evidence.

## Recommended final composition
The 45-study working matrix is deliberately broader than the final PRISMA-included set. It contains direct core studies plus adjacent/supporting evidence for telemetry overhead, kernel enforcement, verifier safety, and eBPF isolation. This avoids artificially inflating the direct evidence base while still supporting the review's central trade-offs.
