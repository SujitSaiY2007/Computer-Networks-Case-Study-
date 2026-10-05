# CHAT 04 — Critical Synthesis / Technology Taxonomy

**Project:** BACSE203 Computer Networks Case Study  
**Assessment date:** 5 October 2026  
**Status:** **COMPLETE**  
**Frozen baseline:** **40 primary studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals**  
**Scope boundary:** synthesis of the completed CHAT 02 evidence extraction and CHAT 03 qualitative quality assessment. No primary study was added, removed or replaced in CHAT 04.

## 1. Scope and methodology

CHAT 04 converts the field-level evidence in `research/CHAT02_EVIDENCE_EXTRACTION.md` and the qualitative evidence-strength assessment in `research/CHAT03_QUALITY_ASSESSMENT.md` into a cross-paper technology taxonomy.

Three evidence levels are kept separate:

1. **Reported evidence** — a study explicitly reports a mechanism, dataset, metric, result or limitation.
2. **Cross-paper synthesis** — a pattern, convergence, divergence or trade-off visible when multiple reported studies are compared.
3. **Inference** — a conclusion derived from the comparison rather than stated by an individual paper.

The synthesis therefore does not treat all 40 studies as equivalent. The 14 Core studies provide the strongest direct evidence for cloud/container runtime-security questions; the 26 Supporting/Adjacent studies primarily strengthen telemetry, networking, enforcement, safety, placement or threat-model understanding.

CHAT 04 does not redo extraction, re-score quality numerically, freeze final research gaps, design the final experiment, or select a prototype architecture.

## 2. Technology taxonomy

### 2.1 Telemetry sources / observation points

| Telemetry family | Representative active studies | Synthesis |
|---|---|---|
| Syscalls / kernel-function activity | P003, P005, P006, P010, P015–P021, P023, P025–P027, P030, P034, P036–P038 | The most recurrent host/runtime observation family. It supports container behaviour, access-control and anomaly detection, but event volume and semantic feature construction vary substantially. |
| Network packets / flows | P002, P007–P014, P018, P028, P031, P035, P038, P040 | Strong evidence for high-rate detection, XDP pre-filtering and network enforcement. Network telemetry is especially suited to low-latency filtering but is less expressive for purely host-local behaviour. |
| File access | P017, P019, P026 and related runtime-policy studies | Provides fine-grained evidence for file-access anomalies and policy generation; complementary to syscall/network telemetry rather than a universal replacement. |
| Process / container lifecycle | P001, P006, P018, P020, P022, P025–P029, P034, P038–P040 | Important for container identity, policy context and runtime state. |
| Timing / performance traces | P004, P021 | Useful for passive anomaly/performance inference and for linking runtime behaviour to resource consumption. |
| Kernel audit / namespace-aware events | P007, P010, P019, P020, P037 | Strong for container-granular policy and audit boundaries. Namespace/cgroup identity is an important context variable when translating host events into container-level decisions. |
| eBPF/XDP/LSM combinations | P005, P007, P010, P019, P025–P031, P034, P037 | These combinations show that telemetry and enforcement need not be located at a single hook. Different attachment points serve different latency, context and safety objectives. |

**Cross-paper synthesis:** syscall telemetry is the dominant runtime-security substrate, while network/XDP telemetry is the dominant high-throughput filtering substrate. File, process, timing and namespace-aware observations add complementary context. The evidence does **not** establish that one telemetry source is universally superior.

### 2.2 eBPF / kernel instrumentation mechanisms

| Mechanism | Primary contribution in the corpus |
|---|---|
| **eBPF generally** | Programmable kernel-level observation/control with maps, event transport and integration with runtime security. |
| **XDP** | Earliest-path packet inspection/filtering; attractive for high-rate traffic and pre-filtering. |
| **TC / traffic hooks** | Network processing and service-function chaining at a later network-processing point than XDP. |
| **kprobes / tracepoints** | Kernel event/function observation; useful for syscall and runtime telemetry with different stability/context properties. |
| **uprobes where used** | User-space function observation; complementary when kernel events do not expose the required semantic context. |
| **BPF-LSM** | Kernel enforcement for syscall, capability and security-policy decisions; important for active mitigation. |
| **seccomp + eBPF/LSM** | Lifecycle and syscall restriction; demonstrates that eBPF security can complement existing mandatory controls rather than replace them. |
| **Namespace/cgroup-aware mechanisms** | Bind observations and decisions to container identity, reducing ambiguity in multi-container hosts. |

**Synthesis:** the papers use eBPF as a family of attachment and control mechanisms, not as one homogeneous technology. XDP prioritizes packet-path speed; tracepoints/kprobes prioritize observation; BPF-LSM prioritizes security enforcement; namespace/cgroup context improves policy specificity.

### 2.3 Feature representations

The corpus spans a clear spectrum:

- **Raw/event streams:** tool-generated runtime events and audit records.
- **Counts/frequencies/distributions:** syscall frequencies, packet/flow statistics and event counts.
- **Sequences:** syscall sequences and behavioural traces, especially in container anomaly/lateral-movement work.
- **Statistical features:** CPU-time, flow and resource-consumption features.
- **Timing features:** eBPF timing traces and per-container performance relationships.
- **Semantic representations:** file paths, policy/context information and application-layer behavioural features.
- **Learned representations:** autoencoders, LSTM/VAE representations and attention-based encoders.
- **Multimodal representations:** combined syscall + network-flow evidence, most directly represented by P018 and related hybrid work.

**Handcrafted vs learned representations:** handcrafted/statistical features are generally easier to interpret and cheaper to compute, while learned representations can capture higher-order behaviour but introduce model-complexity, training-data and deployment constraints. The corpus does not establish a universal accuracy advantage for learned features because datasets, attack classes and baselines differ.

### 2.4 Machine-learning approaches

Reported ML/data-mining families include:

- Decision trees, Random Forest and related tree ensembles (P012, P013, P021, P031).
- AdaBoost (P016).
- SVM/TwinSVM (P013).
- Logistic/other classical classifiers where compared in the relevant studies.
- Neural networks and lightweight/quantized neural models (P002, P012, P014).
- Autoencoders, including LSTM and attention-enhanced variants (P004, P005, P014, P015, P017).
- VAE + Isolation Forest / anomaly-detection combinations (P005 and related adaptive work).
- GMM/Bayesian process-behaviour inference (P027).
- Association/itemset/rule mining (P023, P036).
- Multiclass and ensemble detection (P018, P038).
- Online/adaptive learning (P034).
- Non-ML security systems remain substantial in the corpus; they are retained because they provide the telemetry, enforcement and overhead baselines needed to interpret ML systems.

**Synthesis:** the corpus contains both supervised classification and anomaly/representation-learning approaches. Classical models often fit constrained deployment and tabular/event features; neural/autoencoder methods are used where sequence or representation learning is important. No model family can be ranked globally from the current evidence because evaluation inputs and objectives are heterogeneous.

### 2.5 ML placement

The corpus supports four main placement patterns:

1. **User-space ML:** kernel/eBPF telemetry is exported and richer models execute outside the kernel (e.g., P002, P005 and several host/network detectors).
2. **In-kernel ML:** lightweight/quantized inference executes inside eBPF/XDP (P012, P014 and related work).
3. **Hybrid kernel + user-space:** eBPF performs collection/pre-filtering while user space performs feature extraction or inference (P003, P005, P031 and related systems).
4. **Detection integrated with enforcement:** a score, threshold, rule or learned decision directly drives an eBPF/LSM/XDP action (P005, P031, P034 and enforcement-oriented systems).

| Placement | Strength | Main constraint |
|---|---|---|
| In-kernel | Low data movement and potentially low decision latency | Verifier, instruction, memory and model-complexity constraints |
| User-space | Rich models, easier updates and debugging | Transfer/buffering and process-boundary latency |
| Hybrid | Practical compromise between kernel observability and model richness | Pipeline coordination and end-to-end latency become important |
| Integrated enforcement | Fast response and direct policy application | False positives can directly affect legitimate workloads |

The evidence therefore supports a **placement trade-off**, not a single optimal location.

### 2.6 Detection targets

The 40-study corpus covers:

- DDoS/DoS and semantic application-layer resource exhaustion.
- Cryptojacking.
- Malware/RCE behaviour.
- Container escape and privilege-related attacks.
- File-access anomalies.
- Syscall anomalies.
- Lateral movement and chained container attacks.
- IP spoofing and malicious network traffic.
- Runtime attack-surface exposure and injected processes.
- Resource/performance anomalies.

**Evidence breadth:** network DoS/DDoS and container/runtime attack scenarios are comparatively well represented. Lateral movement, malware and file-access work provide meaningful but narrower evidence. Robust evaluation against unseen attack classes is much less established.

### 2.7 Enforcement / mitigation

The corpus contains both detection-only and active-response systems.

**Detection/monitoring only or primarily:** P001, P004, P006, P015, P018, P021, P022, P024, P038, P040 and several network IDS studies.

**Active enforcement/mitigation:** packet dropping/filtering (XDP), syscall filtering, BPF-LSM policy enforcement, capability control, process control, container isolation, namespace-aware control, network policy and attack-surface restriction.

A recurring architectural pattern is:

**observe → represent → detect/score → decide → enforce**

but many studies implement only a subset. In particular, detection is much more common than a rigorously measured **detection-to-mitigation** path.

### 2.8 Adaptation / continual learning

Evidence must be interpreted narrowly.

- **P034** directly reports online learning under evolving container workloads and compares it with offline learning.
- Dynamic policy generation in P023, P026, P029, P032 and P036 is **adaptation of policy/behaviour models**, not automatically continual ML.
- Periodic retraining or model replacement, where present, is not sufficient by itself to establish continual learning.
- Concept drift, unseen attacks, adversarial feature manipulation and poisoning are not systematically evaluated across the corpus.

**Synthesis:** adaptive behaviour exists, but robust continual-learning evidence is concentrated rather than corpus-wide.

### 2.9 Performance / overhead evaluation

Reported measurements span:

- CPU utilization/overhead.
- Memory overhead.
- Packet throughput / packets per second.
- Event-processing speed.
- Collection speed.
- Inference latency.
- Detection latency.
- Mitigation/enforcement latency in selected systems.
- End-to-end response or tool-level MTTD in selected evaluations.

Examples of concrete evidence include P002's microsecond-scale interception and millisecond-scale user-space inference, P003's reported latency reduction and CPU overhead, P005's sub-millisecond enforcement claim, P012's single-core packet-processing rates, P031's response-time/CPU measurements, and P034's collection-speed/CPU improvements.

**Critical distinction:** an inference-latency number measures model execution; it does **not** establish the time from event generation through buffering, feature extraction, inference, decision and enforcement. The latter end-to-end detection-to-mitigation latency is uncommon and inconsistently defined.

### 2.10 Dataset and workload taxonomy

The evaluation inputs include:

- Public datasets: CICDDoS2019, IoT-23 and TON_IoT among the explicitly reported examples.
- Private/study-specific datasets and traces.
- Real container images and container workloads.
- Vulnerability/PoC sets.
- Malware instances.
- Constructed attack scenarios.
- Network testbeds and controlled cloud/container environments.
- Kubernetes, Docker and Docker Swarm deployments.
- IoT/edge devices and host-level Linux environments.

**Synthesis:** the corpus has useful diversity, but evaluation realism is not proportional to dataset size. Real container images and live orchestration provide stronger deployment realism than purely synthetic traces, while public datasets improve reproducibility. No single dataset dominates the evidence.

### 2.11 Evaluation environments

The literature spans:

- Single Linux hosts.
- Docker and multi-container deployments.
- Kubernetes clusters.
- Docker Swarm.
- AWS/EKS/cloud environments.
- IoT/edge/Raspberry Pi settings.
- Network testbeds.
- Kernel/user-space comparisons.
- Security-tool comparisons.
- ML-model comparisons.

The most established evaluation dimensions are attack detection and basic CPU/memory/throughput measurements. Less standardized dimensions are multi-node churn, heterogeneous kernels/CNIs, event loss, repeated-run uncertainty and end-to-end response.

## 3. Cross-paper synthesis

### 3.1 Convergence

**Convergence 1 — eBPF is valuable because observation and control can occur close to the kernel.** Multiple independent studies use eBPF/XDP/LSM to reduce instrumentation intrusion, observe low-level runtime/network behaviour or apply enforcement without relying entirely on sidecars.

**Convergence 2 — placement matters.** In-kernel execution can reduce movement and latency but constrains model complexity; user-space inference supports richer models but introduces pipeline overhead. Hybrid placement repeatedly appears as a practical compromise.

**Convergence 3 — telemetry granularity affects cost.** Richer syscall, file and network observation provides more behavioural information but increases event volume, buffering and processing requirements.

**Convergence 4 — bounded testbeds dominate.** Most studies evaluate specific kernels, container sets, attacks, workloads or orchestration environments. This makes within-study conclusions useful while limiting direct cross-study generalization.

**Convergence 5 — active enforcement is technically feasible.** XDP filtering, BPF-LSM, syscall controls, process controls and container/network policy systems demonstrate that eBPF can participate in mitigation, not merely monitoring.

### 3.2 Divergence

**Divergence 1 — detection objectives differ.** Some papers classify known attacks; others detect anomalies; others generate policies or enforce known constraints. Accuracy numbers across these objectives are not directly comparable.

**Divergence 2 — telemetry semantics differ.** A syscall sequence, network flow and file path encode different aspects of behaviour. A model's apparent superiority may therefore reflect observation modality rather than model family.

**Divergence 3 — overhead definitions differ.** CPU percentage, packet rate, collection speed and latency are measured under different event rates, hardware and baselines.

**Divergence 4 — adaptation is heterogeneous.** Online ML, dynamic rules and policy generation are sometimes all described as “adaptive,” but they represent different technical mechanisms.

**Divergence 5 — enforcement safety evidence varies.** Some systems quantify blocking/legitimate-operation impact; others demonstrate enforcement functionality without a systematic false-positive or recovery analysis.

### 3.3 Trade-offs

| Trade-off | Evidence-grounded interpretation |
|---|---|
| Kernel placement ↔ model complexity | Kernel execution can improve locality/latency but constrains model size and programmability. |
| Rich telemetry ↔ overhead | More modalities/context can improve behavioural coverage but increases event-processing and buffering cost. |
| Detection accuracy ↔ generalization | High within-dataset performance does not establish robustness to new workloads, attacks or temporal drift. |
| Detection ↔ mitigation | Detection systems can optimize classification without proving safe, fast enforcement. |
| Public datasets ↔ deployment realism | Public data improves comparability/reproducibility; live container/cloud testbeds improve realism but are harder to reproduce. |
| Adaptive learning ↔ reproducibility | Online adaptation can respond to evolving behaviour but makes fixed, repeatable evaluation harder. |
| Strong enforcement ↔ operational flexibility | Aggressive controls can reduce attack surface while increasing the consequence of false positives. |
| Broad telemetry ↔ implementation complexity | Multi-source telemetry can provide richer context but complicates synchronization, buffering and feature construction. |

## 4. Recurring design and evaluation patterns

### 4.1 Recurring design pattern

A large subset of the corpus can be mapped to:

**kernel telemetry → feature extraction/representation → ML or rule-based decision → policy/risk decision → enforcement**

However, the corpus is better described as a collection of **partial implementations of this pipeline** than as evidence for one universal architecture.

Typical subsets are:

- telemetry → monitoring;
- telemetry → ML detection;
- telemetry → detection → alert;
- telemetry → detection → enforcement;
- telemetry → policy generation → enforcement;
- telemetry → lightweight kernel decision → user-space follow-up.

### 4.2 Recurring evaluation pattern

Most studies use a controlled workload and a defined attack set, then report one or more of:

- detection accuracy/precision/recall/F1;
- CPU/memory overhead;
- throughput;
- latency;
- comparison against a baseline tool/model.

The missing common layer is a standardized end-to-end measurement from **event generation to mitigation**, together with event-loss/buffering and repeated-run uncertainty.

## 5. Core vs Supporting/Adjacent synthesis

### What Core studies directly establish

The Core subset provides the strongest direct evidence that eBPF-based runtime telemetry can be used for cloud/container monitoring, attack detection and/or enforcement. It establishes concrete examples of syscall, network, file and runtime telemetry combined with ML or security controls, and it provides the most relevant evidence for the project's RQ1–RQ4 intersection.

Core evidence is strongest for:
- runtime telemetry feasibility;
- container/cloud attack detection;
- eBPF-assisted enforcement;
- practical ML placement choices;
- measured CPU/throughput/latency under bounded conditions.

### What Supporting/Adjacent studies contribute

Supporting/Adjacent studies strengthen claims about:
- XDP and packet-processing performance;
- kernel/user-space ML placement;
- eBPF verifier and runtime safety constraints;
- network-function chaining;
- container policy generation;
- namespace-aware auditing;
- offensive eBPF/container threats;
- telemetry and monitoring tool comparisons.

### What Supporting evidence cannot substitute for

A network-function or verifier-safety study cannot substitute for direct evidence that an ML detector generalizes to container runtime attacks. Likewise, an enforcement study cannot substitute for an end-to-end ML detection-to-mitigation measurement.

Supporting studies therefore **strengthen mechanisms and boundary conditions**, but they do not automatically establish the complete eBPF + ML + cloud-native runtime-security claim.

## 6. Evidence-strength synthesis from CHAT 03

### Strongly supported patterns

- eBPF/XDP/LSM can provide low-level telemetry or enforcement with measurable performance characteristics.
- Container/Kubernetes runtime monitoring and enforcement are demonstrated across multiple independent studies.
- ML detection is feasible over syscall, network-flow, file-access and timing telemetry.
- ML placement changes latency, throughput and implementation constraints.
- Container-granular identity/context can be integrated into runtime security decisions.

### Moderately supported patterns

- Hybrid telemetry can improve behavioural coverage, but the corpus does not establish a standardized multimodal representation.
- Adaptive/online learning can improve performance under evolving workloads in at least some settings, but evidence is concentrated.
- Active enforcement can be practical, but safety and rollback are not evaluated consistently.

### Narrow or bounded evidence

- Many detection results are attack-specific.
- Many experiments use small/controlled container sets or a single environment.
- Several studies rely on private or study-specific traces.
- Conference/tool-comparison evidence is useful but should not be treated as equivalent to broad multi-environment validation.

### Reproducibility limitations

CHAT 03 identifies incomplete code/configuration/data disclosure as a recurring weakness. Public datasets help, but reproducibility still depends on kernel version, runtime configuration, attack-generation procedures, container images and orchestration details.

### Statistical limitations

Repeated-run variance, confidence intervals and significance testing are uncommon. Consequently, small reported differences between tools/models should not automatically be interpreted as robust superiority.

### Latency limitations

Inference latency is reported more often than complete detection-to-mitigation latency. Event transport, buffering, feature extraction and enforcement time are often outside the reported number.

## 7. Technology evolution / architecture patterns

The evidence supports a technology progression:

**kernel telemetry → feature extraction → ML/rule detection → decision → enforcement**

but not a universal implementation.

1. **Telemetry foundation:** tracepoints, kprobes, XDP, TC and LSM provide observation/control points.
2. **Runtime context:** container, namespace, cgroup, process and workload identity contextualize raw events.
3. **Representation:** counts, distributions, sequences, statistical features and learned embeddings convert events into model inputs.
4. **Detection:** classical ML, anomaly detection, neural/autoencoder methods or rule mining classify/score behaviour.
5. **Decision:** thresholds, risk scores, policies or model outputs determine whether action is required.
6. **Enforcement:** XDP filtering, BPF-LSM, syscall/process controls, container isolation or network policy can implement mitigation.

Only subsets of this chain are implemented in most studies. The strongest full-chain examples remain bounded by workload, attack and environment assumptions.

## 8. Unresolved tensions exposed by the evidence

The following are **literature-supported tensions**, not final research gaps:

1. **Low-latency kernel processing vs complex ML models.**
2. **Telemetry richness vs CPU/memory/event-processing cost.**
3. **Adaptive learning vs reproducibility and controlled evaluation.**
4. **Detection accuracy vs cross-workload/generalization evidence.**
5. **Detection vs safe autonomous mitigation.**
6. **Public reproducible datasets vs realistic private/live workloads.**
7. **Centralized/richer user-space processing vs kernel-local response.**
8. **Fine-grained enforcement vs legitimate-workload disruption risk.**
9. **High event rates vs complete telemetry/buffering guarantees.**
10. **Portability across kernels/runtimes vs tightly optimized implementations.**

## 9. Preliminary evidence-to-gap observations

These are intentionally **candidate observations only**. They are not frozen final research gaps and must be re-evaluated in CHAT 05.

### Candidate observation A — end-to-end measurement remains fragmented

The corpus frequently reports CPU, throughput, collection speed or inference latency, but these measurements are not standardized into one event-to-mitigation timeline. This suggests a candidate need for a common end-to-end measurement framework.

### Candidate observation B — robustness evidence is narrower than within-scenario detection evidence

Many studies demonstrate strong results for named attacks/workloads, while temporal drift, unseen workloads, unseen attack classes and adversarial manipulation are less consistently evaluated. This is a candidate robustness-evaluation issue, not a claim that no robustness work exists.

### Candidate observation C — telemetry/event-loss evidence is under-standardized

Event rate, buffering, dropped events and telemetry completeness are not consistently reported. This creates a candidate measurement gap when comparing “low overhead” claims.

### Candidate observation D — safe enforcement evidence is less standardized than detection evidence

Several systems enforce policies, but false-positive consequences, rollback/recovery, policy conflict and legitimate-operation impact are not measured with a common methodology.

### Candidate observation E — placement comparisons are promising but heterogeneous

The corpus contains in-kernel, user-space and hybrid ML, but differences in model, workload and measurement methodology prevent a clean global conclusion about the best placement.

### Candidate observation F — reproducibility is a cross-cutting constraint

The ability to reproduce a result depends on artifacts beyond source code: kernel/runtime versions, container images, configuration, attack scripts, raw traces and evaluation procedures.

## 10. CHAT 04 boundary confirmation

CHAT 04 did **not**:

- change the 40-study baseline;
- add a new primary study;
- remove or replace P021 or P031;
- restart literature searching or acquisition;
- redo CHAT 02 extraction;
- redo CHAT 03 quality assessment;
- freeze final research gaps;
- design the final experimental architecture;
- implement the prototype;
- create the Review 2 PPT;
- write the final manuscript.

## 11. Completion and next phase

**CHAT 04 — COMPLETE**

The next phase is:

**CHAT 05 — Research Gap Consolidation / Evidence-to-Design Bridge**

CHAT 05 should treat the candidate observations in this document as hypotheses to test against the complete evidence base. It should consolidate only evidence-supported gaps, map them to the RQs and review contribution, and bridge them toward design requirements without prematurely implementing the prototype.
