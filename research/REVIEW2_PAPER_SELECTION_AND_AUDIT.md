# Review 2 — Final Candidate Evidence Set and Paper Audit

**Project:** eBPF-Assisted Machine Learning for Cloud-Native Runtime Security  
**Review design:** Systematic mapping study / scoping-style evidence map with critical technical synthesis  
**Evidence period:** January 2020 to final search date, with older/seminal work only when technically necessary  
**Citation style:** Harvard author–date  
**Review 2 target:** 40 primary studies, with 36 journal articles and 4 peer-reviewed conference papers (**90% journals**).

## 1. Selection decision

The original 45-study working set is **not** being treated as the final reference list. It was a discovery/evidence pool containing direct studies, adjacent studies, preprints, conferences, and supporting technical work. For Review 2, the set has been tightened and supplemented with stronger peer-reviewed journal evidence so that the final primary-study set is both closer to the project objective and compliant with the team's additional requirement that journals make up 90% of the references.

A newly published 2026 systematic review of eBPF cybersecurity was also checked as a **background/comparison review**, not counted as a primary study. It confirms that the field is fragmented across IDS, container security, microservices, DDoS, networking, and tools, and highlights recurring issues such as verifier constraints, portability, production validation, adversarial robustness, and standardized evaluation. The review must therefore make its contribution through a narrower cloud-native runtime-security evidence map and critical comparison rather than claiming to be the first eBPF security review.

## 2. Final 40-primary-study composition

| # | Type | Year | Title | Publisher / venue | Methodology used | Merits | Demerits / limitation | Research field |
|---:|---|---:|---|---|---|---|---|---|
| 1 | Journal | 2025 | An In-Depth Analysis of eBPF-Based System Security Tools in Cloud-Native Environments | IEEE Access / IEEE | Comparative evaluation of KubeArmor, Falco, Tetragon and Tracee; architecture, auditing, performance and case studies | Direct Kubernetes runtime-security baseline; tool comparison | Tool-centric; no ML detection | Cloud-native runtime security |
| 2 | Journal | 2026 | Real-Time eBPF/XDP-Based Deep Learning Framework for Anomaly Traffic Detection in Internet of Things Networks | IEEE Internet Computing / IEEE | Hybrid eBPF/XDP feature extraction with deep learning for anomaly traffic detection | Links kernel telemetry with ML and placement trade-offs | IoT rather than Kubernetes/container runtime | eBPF/XDP ML anomaly detection |
| 3 | Journal | 2025 | CODAX: eBPF-Based Runtime Detection of Semantic DDoS Attacks in Linux Containers | IEEE Access / IEEE | eBPF runtime telemetry for semantic/application-layer DDoS detection with performance evaluation | Direct container runtime fit; latency/overhead focus | Attack-specific; generalization requires further evidence | Container runtime DDoS |
| 4 | Journal | 2026 | Low-Overhead Passive Resilience Monitoring for AIoT Gateways: End-to-End Anomaly Detection via eBPF Timing Traces and Autoencoders | IEEE Access / IEEE | eBPF timing telemetry + autoencoder/CUSUM anomaly detection | Useful evidence on low-overhead telemetry | AIoT gateway rather than cloud-native containers | Telemetry/overhead anomaly detection |
| 5 | Journal | 2025 | DeSFAM: An Adaptive eBPF and AI-Driven Framework for Securing Cloud Containers in Real Time | IEEE Access / IEEE | Static + dynamic syscall profiling, VAE/iForest detection, contextual risk scoring, eBPF-LSM enforcement | Very close to the proposed telemetry → ML → enforcement pipeline | Dataset/attack scenario scope may limit external validity | Container runtime ML + enforcement |
| 6 | Journal | 2025 | Detecting Cryptojacking Containers Using eBPF-Based Security Runtime and Machine Learning | Electronics / MDPI | Tetragon syscall/flow telemetry, n-gram features, ML model comparison and overhead evaluation | Direct Kubernetes/container ML detection | Focused on cryptojacking and a limited workload set | Container ML detection |
| 7 | Journal | 2023 | eBPF: A New Approach to Cloud-Native Observability, Networking and Security for Current (5G) and Future Mobile Networks (6G and Beyond) | IEEE Access / IEEE | Cloud-native eBPF architecture covering tracepoints, kprobes, TC/XDP, LSM, observability and enforcement | Strong architectural foundation for terminology and system placement | Broad architecture paper; not a controlled ML experiment | Cloud-native eBPF architecture |
| 8 | Journal | 2022 | BPFast: An eBPF/XDP-based high-performance packet payload inspection system for cloud environments | Journal of KIISE / KIISE | eBPF/XDP packet inspection and performance evaluation | Strong packet-processing/telemetry baseline | More network-payload focused than container ML runtime security | eBPF/XDP network security |
| 9 | Journal | 2023 | Secure Inter-Container Communications Using XDP/eBPF | IEEE/ACM Transactions on Networking / IEEE & ACM | Bastion+ eBPF/XDP network enforcement, security-function chaining and policy assistance | Strong container-network enforcement evidence | No ML; primarily network-layer | Container network security |
| 10 | Journal | 2023 | Container Instrumentation and Enforcement System for Runtime Security of Kubernetes Platform with eBPF | Intelligent Automation & Soft Computing / Tech Science Press | Tracee-based monitoring plus BPF-LSM enforcement for Kubernetes containers | Direct Kubernetes runtime monitoring/enforcement | No ML; framework/testbed scope must be assessed | Kubernetes runtime security |
| 11 | Journal | 2023 | Detection of Denial of Service Attack in Cloud Based Kubernetes Using eBPF | Applied Sciences / MDPI | eBPF/XDP-based Kubernetes DDoS detection/mitigation with overhead evaluation | Direct Kubernetes security and performance evidence | DDoS-specific | Kubernetes DDoS security |
| 12 | Journal | 2024 | Practicality of in-kernel/user-space packet processing empowered by lightweight neural network and decision tree | Computer Networks / Elsevier | Quantized NN and decision tree in eBPF/XDP versus AF_XDP/user-space; throughput, resource and detection evaluation | Excellent evidence for ML placement and verifier trade-offs | Packet classification rather than container runtime | In-kernel ML placement |
| 13 | Journal | 2025 | Enhancing intrusion detection against denial of service and distributed denial of service attacks: Leveraging extended Berkeley packet filter and machine learning algorithms | IET Communications / Wiley-IET | eBPF kernel capture with DT/RF/SVM/TwinSVM detection | Direct ML/eBPF comparison | Network-attack focus rather than Kubernetes runtime | eBPF ML intrusion detection |
| 14 | Journal | 2026 | Unsupervised Real-Time In-Kernel Intrusion Detection System Using Autoencoders and eBPF | IEICE Transactions on Communications / IEICE | Quantization-aware unsupervised autoencoder executed in eBPF | Strong in-kernel ML and latency/throughput evidence | Network IDS rather than Kubernetes; model complexity constrained by eBPF | In-kernel unsupervised ML |
| 15 | Journal | 2026 | Behavioral Anomaly Detection in Linux Systems using eBPF and LSTM Neural Networks: A Comparative Study with Traditional Machine Learning | International Journal of Computer Applications | eBPF syscall telemetry + LSTM autoencoder compared with traditional ML | Direct behavioural anomaly perspective | Venue strength and full indexing should be checked before final submission | Host anomaly detection |
| 16 | Journal | 2024 | A Technique for Accurate Detection of Container Attacks with eBPF and AdaBoost | Journal of The Korea Society of Computer and Information | eBPF syscall patterns + AdaBoost for container attack detection | Container-specific ML evidence | Specific attack set and limited generalization | Container attack detection |
| 17 | Journal | 2026 | An Abnormal File Access Detection Model for Containers Based on eBPF Listening | Mathematics / MDPI | eBPF file-access capture, semantic path representation, attention-enhanced autoencoder | Fine-grained telemetry and unsupervised detection; explicit false-positive evaluation | File-access specific | Container file-access anomaly detection |
| 18 | Journal | 2026 | Hybrid Runtime Detection of Malicious Containers Using eBPF | Computers, Materials & Continua / Tech Science Press | Hybrid flow + syscall telemetry and multiclass ML across benign/malicious containers | Direct comparison of telemetry modalities; highly relevant to RQ1/RQ2 | Six malicious and four benign scenarios; external validity limited | Hybrid container runtime ML |
| 19 | Journal | 2025 | Cordon: Enhancing security through kernel-level control in containerized computing environments | Computers & Security / Elsevier | Deployment-file policy generation plus eBPF/LSM runtime enforcement | Strong autonomous enforcement and policy-generation evidence | No ML; policy correctness depends on extracted intent | Container kernel enforcement |
| 20 | Journal | 2025 | BPFGuard: Multi-Granularity Container Runtime Mandatory Access Control | IEEE Transactions on Cloud Computing / IEEE | Multi-granularity syscall/LSM/kernel-function access control using eBPF and Kubernetes metadata | Strong enforcement granularity and benchmark evidence | Enforcement-focused; no ML | Container MAC/enforcement |
| 21 | Journal | 2025 | Deep Analysis of Containerized Web Server Performance Using eBPF-Captured Data | IEEJ Transactions on Electrical and Electronic Engineering / Wiley | eBPF per-container syscall monitoring + Random Forest regression of resource-performance relationships | Direct container telemetry and quantitative CPU/memory/disk-I/O evidence | Performance-focused rather than security/detection; supporting evidence | Container telemetry/performance |
| 22 | Journal | 2024 | eBPF-based Container Activity Analysis System | The Transactions of the Korea Information Processing Society / KIPS | eBPF event collection; comparative analysis of Tetragon, Falco and Tracee; container metadata integration | Useful tool/telemetry taxonomy | Monitoring-centric; no ML | Container observability/security |
| 23 | Journal | 2024 | Optimus: association-based dynamic system call filtering for container attack surface reduction | Journal of Cloud Computing / Springer Nature | eBPF syscall tracing + association analysis + dynamic filtering; evaluation on 71 container images | Real container images; strong runtime enforcement and overhead evidence | No ML anomaly detection | Container attack-surface reduction |
| 24 | Journal | 2023 | Coda: Runtime Detection of Application-Layer CPU-Exhaustion DoS Attacks in Containers | IEEE Transactions on Services Computing / IEEE | eBPF runtime monitoring of per-connection CPU consumption for application-layer DoS | Strong runtime and overhead evidence | DoS-specific; ML is not the central method | Container runtime DoS |
| 25 | Journal | 2026 | Hela: A System Call Restriction Framework for Protecting the Entire Containers Lifecycle | IEEE Transactions on Cloud Computing / IEEE | Seccomp + eBPF syscall restriction across container runtime and applications; attack-surface scoring | Covers whole lifecycle and attack-surface measurement | Enforcement rather than ML | Container syscall restriction |
| 26 | Journal | 2026 | BeaCon: Automatic container policy generation using environment-aware dynamic analysis | Computers & Security / Elsevier | Environment-aware dynamic analysis, eBPF syscall/capability monitor, policy generation and security/functionality scoring | Automated policy generation with real Docker evaluation | Policy-generation focus; not ML detection | Container policy automation |
| 27 | Journal | 2026 | Vaccine: Injection vulnerabilities mitigation through dynamic process control with eBPF | Computers & Security / Elsevier | eBPF-based dynamic process control to inhibit execution of injected payloads | Demonstrates active kernel response to exploitation | Host/process focus rather than Kubernetes; no ML | Kernel enforcement |
| 28 | Journal | 2025 | Preventing IP Spoofing in Kubernetes Using eBPF | Computers, Materials & Continua / Tech Science Press | Kubernetes CNI integration, eBPF packet validation, spoof detection/blocking on AWS EKS | Real Kubernetes deployment and overhead measurements | Attack-specific; packet/IP assumptions constrain scope | Kubernetes network enforcement |
| 29 | Journal | 2024 | KubeAegis: A Unified Security Policy Management Framework for Containerized Environments | IEEE Access / IEEE | Unified policy management, policy conversion/recommendation across heterogeneous container security mechanisms | Useful integration layer for multiple enforcement technologies | Not specifically ML; central policy-management complexity | Container security policy management |
| 30 | Journal | 2024 | KubeRosy: A Dynamic System Call Filtering Framework for Containers | IEEE Access / IEEE | eBPF + LSM dynamic syscall filtering with argument-aware policies and no container downtime | Strong enforcement/overhead evidence; direct runtime fit | No ML; policy correctness remains critical | Dynamic syscall enforcement |
| 31 | Journal | 2026 | Evaluasi Efektivitas Firewall Pre-filtering berbasis eBPF/XDP menggunakan Random Forest untuk Deteksi Anomali Trafik pada Docker Swarm | JURIKOM / STMIK Budi Darma | Random Forest trained offline, rules converted to thresholds, eBPF/XDP kernel-space pre-filtering with Docker Swarm evaluation | Direct eBPF/XDP + ML + container orchestration with full performance and mitigation measurements | DDoS-focused and Docker Swarm-specific; external validity requires assessment | Container/network ML enforcement |
| 32 | Journal | 2023 | Kunerva: Automated Network Policy Discovery Framework for Containers | IEEE Access / IEEE | Network-log policy discovery plus policy verification/enforcement | Useful policy-generation complement for cloud-native security | Not eBPF/ML core | Kubernetes network policy |
| 33 | Journal | 2025 | From Container to Cluster: Chained Escape Attacks in Kubernetes and Orchestration Platforms | IEEE Access / IEEE | Threat/attack-chain analysis of chained container escape scenarios and defenses | Strong threat-model context for enforcement requirements | Threat analysis rather than a detection benchmark | Kubernetes/container escape |
| 34 | Journal | 2026 | Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks | IEEE Transactions on Cloud Computing / IEEE | Zero-copy eBPF syscall collection + lightweight ML anomaly detection + container-specific online learning + isolation/traffic control | Direct Kubernetes/cloud-native runtime-security evidence combining telemetry, ML, adaptation and response | Single-system evaluation; common-protocol placement comparison and broader external validation remain limited | Cloud-native runtime ML + lateral-movement mitigation |
| 35 | Journal | 2021 | A Framework for eBPF-Based Network Functions in an Era of Microservices | IEEE Transactions on Network and Service Management / IEEE | Polycube framework for in-kernel eBPF/XDP network functions with user-space control plane; Kubernetes use case | Strong architecture, programmability and placement evidence | Networking/NFV focus; not ML runtime security | eBPF microservice networking |
| 36 | Journal | 2024 | ESX: A Self-Generated Control Policy for Remote Access With SSH Based on eBPF | IEEE Access / IEEE | eBPF runtime monitoring and self-generated SSH control policies | Demonstrates adaptive policy generation from runtime behaviour | SSH/remote-access focus; indirect container relevance | eBPF adaptive policy control |
| 37 | Conference | 2021 | Secure Namespaced Kernel Audit for Containers | ACM SoCC '21 / ACM | saBPF container-granular audit, IDS and lightweight access control in Kubernetes | Direct container/Kubernetes audit evidence; strong systems venue | Conference; no ML | Container audit/IDS |
| 38 | Conference | 2024 | Malware Detection in Cloud Native Environments | ACM AICCC 2024 / ACM | SkyShark eBPF sensor + ML ensemble for cloud-native malware/RCE behaviour | Direct cloud-native eBPF + ML malware detection | Conference; dataset/scenario scope requires quality assessment | Cloud-native malware detection |
| 39 | Conference | 2023 | Cross Container Attacks: The Bewildered eBPF on Clouds | USENIX Security '23 / USENIX | Threat analysis and exploitation of eBPF permissions/cross-container attack surface | High-quality safety/threat evidence; prevents one-sided defensive conclusions | Offensive-security focus rather than detection pipeline | eBPF/container threat model |
| 40 | Conference | 2025 | Comparative Analysis of eBPF-Based Runtime Security Monitoring Tools in Monitoring and Threat Detection on Kubernetes | SCITEPRESS RITECH 2025 / SciTePress | Quantitative comparison of Falco, Tetragon and Tracee using MTTD, detection rate, FPR, CPU and memory | Direct baseline for tool choice and evaluation metrics | Conference; tool-centric and not ML-focused | Kubernetes runtime-security tools |

## 3. Journal-ratio confirmation

- Journal articles: **36 / 40 = 90%**
- Peer-reviewed conference papers: **4 / 40 = 10%**
- Preprints intentionally excluded from the primary 40 unless later peer-reviewed and re-verified.
- Existing review papers are kept as **background/comparison references**, not counted as primary evidence.

## 4. Paper-standard and structure check

Every final primary study must be checked against the same quality framework from the BACSE203 guidelines:

1. Objective clarity — the research objective is explicit.
2. Technical description — architecture, algorithm/model and system components are sufficiently described.
3. Dataset/workload transparency — dataset, workload, attack scenario, test conditions and testbed are identifiable.
4. Baseline adequacy — relevant baselines/comparison systems are present where appropriate.
5. Evaluation validity — metrics actually measure the stated objective.
6. Experimental detail — hardware, parameters, configurations and repeated trials are reported where relevant.
7. Reproducibility — code, data, models, traces or configuration availability is recorded.
8. Limitation disclosure — author-reported and reviewer-identified limitations are captured.
9. External validity — evidence beyond one small/artificial scenario is considered.
10. Statistical reporting — variance, confidence intervals, repeated trials or significance testing are recorded when appropriate.

Quality categories will be **Clearly reported / Partially reported / Not reported**, rather than an artificial numerical score. A paper can remain in the evidence map even when documentation is weak, but weak evidence will not be treated as equivalent to strong evidence.

## 5. Mandatory extraction fields for the next pass

For every one of the 40 papers, the extraction sheet will contain:

- Title
- Authors
- Year
- Journal/conference
- Publisher
- DOI/persistent identifier
- Publication status
- Research field
- Research problem/objective
- Cloud/container environment
- eBPF hook/type (kprobe, tracepoint, BPF-LSM, TC, XDP, etc.)
- Telemetry granularity
- Feature representation
- ML method/model, if any
- ML inference placement
- Dataset/workload/testbed
- Attack scenario
- Baselines
- CPU overhead
- Memory overhead
- Detection metrics
- Latency / detection-to-mitigation latency
- Event loss/buffering behaviour
- Enforcement mechanism
- Merits
- Demerits/limitations
- Reproducibility artifacts
- Quality-assessment notes
- Relevance to RQ1–RQ5
- Harvard citation

## 6. Important distinction for the manuscript

The paper list must not become 40 independent summaries. The manuscript should synthesize the evidence into the project's intended framework:

**Telemetry extraction → feature representation → ML placement → detection decision → kernel enforcement**

and compare studies on:

**detection quality ↔ latency ↔ CPU/memory/event-processing overhead ↔ safety ↔ reproducibility.**

This is the contribution that connects the Review 1 story to the final literature review.

## 7. Review papers kept outside the primary set

At minimum, retain the following as comparison/background literature:

- Kostopoulos, S., Tsakonas, P. and Markakis, E.K. (2026), *eBPF-based cybersecurity mechanisms: a systematic literature review*, International Journal of Information Security.
- Any earlier eBPF/container-security surveys identified during the database search.

These reviews should be used to map terminology, prior taxonomies and gaps, but their tables/taxonomies must not be copied. The final review must derive its own synthesis from primary studies.

## 8. Status

**Review 2 paper list: SELECTED FOR FULL-TEXT VERIFICATION.**

This is the correct point to lock the candidate set, complete the extraction matrix and quality assessment, and then write the evidence-based gap table. A paper should be moved out of the final 40 only if full-text screening reveals a scope, publication-status, evidence-quality, duplication or accessibility problem. Any replacement must preserve the 90% journal target.


## CHAT 01 — Full-text verification/screening result (5 October 2026)

The provisional 40-study list has been screened and is **no longer accepted unchanged**. One candidate was found to be a review rather than a primary study:

- **Extended Berkeley Packet Filter: An Application Perspective** — IEEE Access, 2022, DOI 10.1109/ACCESS.2022.3226269. **Moved to background/comparison.**

A verified journal primary study was substituted:

- **Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks** — IEEE Transactions on Cloud Computing, 2026, DOI 10.1109/TCC.2026.3657486.

The replacement directly contributes eBPF telemetry, ML anomaly detection, online learning/adaptation, container isolation, and CPU/collection-efficiency evidence. The resulting primary composition remains **36 journals + 4 peer-reviewed conferences = 90% journals**.

See research/CHAT01_FULLTEXT_VERIFICATION.md for the auditable 40-row screening table, explicit decision reasons, evidence-strength labels and count check.

**Status after CHAT 01:** verified screening baseline complete; detailed full-text acquisition/archive is the next checkpoint; extraction and formal quality assessment remain unfrozen.

## CHAT 02 replacement checkpoint — 5 October 2026

P021 and P031 were replaced before detailed extraction with directly accessible journal primary studies. The frozen composition remains 40 studies: 36 journals + 4 peer-reviewed conferences.


## CHAT 02 extraction checkpoint — 5 October 2026

**Status: COMPLETE.** The frozen 40-study baseline (36 journals + 4 peer-reviewed conferences) has been field-extracted in `research/CHAT02_EVIDENCE_EXTRACTION.md`. P021 and P031 are the active corrected replacement records. CHAT 03 must assess quality using the qualitative framework already defined here and must not restart selection.


## CHAT 03 quality-assessment checkpoint — 5 October 2026

**Status: COMPLETE.** All 40 retained primary studies have undergone formal qualitative quality assessment using the frozen ten-dimension framework. No numerical quality score was assigned and no study was added, removed or replaced. See `research/CHAT03_QUALITY_ASSESSMENT.md`. Next phase: **CHAT 04 — Critical Synthesis / Technology Taxonomy**.


## 5. Review 2 50-reference presentation corpus — 5 October 2026

The faculty Review 2 instruction requires a literature-survey table for all 50 papers and a minimum of 50 references. To satisfy that presentation requirement without compromising the evidence methodology, the project now distinguishes:

- **40 canonical primary studies:** unchanged, 36 journals + 4 peer-reviewed conferences = 90% journals.
- **10 supporting/background references:** R041–R050, selected for direct relevance to eBPF meta-security, verifier safety, cloud-native telemetry/latency, service-mesh performance and established runtime-security surveys.

The 10 supporting references are **not counted as primary studies** and do not alter the CHAT 01–06 evidence baseline.

The complete faculty-format table is maintained in review2/REVIEW2_50_PAPER_LITERATURE_TABLE.md with the requested fields:

1. serial number;
2. paper title;
3. journal/venue and year;
4. dataset/workload/evidence base;
5. methodology/algorithm;
6. advantages/novelty;
7. disadvantages/gaps/limitations.

### Added references

| Ref. | Study | Role | Why added |
|---:|---|---|---|
| R041 | KRAKENGUARD: Towards Fine-Grained eBPF Isolation | Supporting technical | Multi-tenant eBPF isolation and policy-constrained loading |
| R042 | BeeBox: Hardening BPF against Transient Execution Attacks | Supporting technical | eBPF meta-security and performance/security trade-off |
| R043 | Validating the eBPF Verifier via State Embedding | Supporting technical | Verifier correctness and kernel-safety constraint |
| R044 | Enhancing Packet Tracing of Microservices in Container Overlay Networks using eBPF | Supporting technical | Kubernetes telemetry and latency measurement |
| R045 | Monitoring Network Flows in Containerized Environments | Supporting technical | Explicit eBPF flow-monitoring architecture and performance feasibility |
| R046 | Network shortcut in data plane of service mesh with eBPF | Supporting technical | Cloud-native service-mesh latency/CPU/memory context |
| R047 | Design and implementation of an intrusion detection system by using Extended BPF in the Linux kernel | Supporting technical | Kernel/user-space IDS placement and throughput context |
| R048 | SoK: Run-time security for cloud microservices. Are we there yet? | Background/secondary | Runtime-security taxonomy and reproducibility/benchmark context |
| R049 | A Container Security Survey: Exploits, Attacks, and Defenses | Background/secondary | Broad container threat/defense context and eBPF dual-role context |
| R050 | eBPF-based cybersecurity mechanisms: a systematic literature review | Background/secondary | Current 2026 eBPF-security synthesis and gap-positioning context |

### Methodological boundary

The 10 additions are presentation references, not a silent expansion of the primary systematic-mapping evidence set. The project must continue to use the 40-study baseline for formal CHAT 02 extraction, CHAT 03 quality assessment, CHAT 04 synthesis and CHAT 05 gap consolidation. Review papers are explicitly secondary evidence.

The complete table and source/provenance details are in review2/REVIEW2_50_PAPER_LITERATURE_TABLE.md.
