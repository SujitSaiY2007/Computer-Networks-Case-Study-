# Project Scope, Research Questions, and Review Contribution

## Frozen working title
**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

## Domain
Computer Networks / Cloud-Native Security / eBPF Kernel Observability / Machine-Learning-Based Runtime Intrusion Detection.

## Scope statement
This review examines eBPF-assisted machine learning architectures for runtime intrusion detection and enforcement in cloud-native containerized environments. It covers primary studies published from January 2020 through the final search date that report telemetry extraction, ML inference, kernel-level policy enforcement, or measurable performance/security evidence relevant to the architecture and trade-offs. It excludes static image scanning, purely user-space intrusion detection without eBPF telemetry, traditional non-cloud-native NIDS without a meaningful eBPF connection, and speculative tutorials. Adjacent eBPF ML/network-security studies may be retained as supporting evidence when they directly inform in-kernel inference, telemetry overhead, verifier constraints, or enforcement latency.

## Research questions
- RQ1: What architectural patterns couple eBPF telemetry hooks (`kprobes`, `tracepoints`, `BPF-LSM`, `TC/XDP`) with ML inference pipelines?
- RQ2: How do systems trade telemetry granularity against CPU, memory, buffering/event loss, and scalability overhead?
- RQ3: Which ML methods are used, and what evidence exists concerning concept drift, container churn, and adversarial evasion?
- RQ4: What mechanisms support real-time kernel mitigation, and what is the detection-to-mitigation latency?
- RQ5: What datasets, cloud testbeds, attack scenarios, metrics, and reproducibility artifacts are used?

## Review contribution
The intended contribution is not simply a survey of eBPF tools. The review will build an evidence-derived taxonomy across **telemetry extraction → feature representation → ML placement → detection decision → kernel enforcement**, then compare studies using a common framework for **overhead, detection quality, latency, safety, and reproducibility**. The final research agenda will focus on evidence-supported gaps such as dynamic workload drift, constrained in-kernel inference, event loss under stress, safe active enforcement, adversarial robustness, portability and reproducibility.

## Review design
**Systematic mapping study / scoping-style evidence map with critical technical synthesis.** PRISMA 2020 is used as the reporting guide where appropriate. The field contains heterogeneous architectures, ML methods, datasets and evaluation environments, so the review prioritizes classification, evidence mapping, comparison and research-gap synthesis rather than pooled effect estimation.

## Review 2 evidence policy
The Review 2 primary evidence target is **40 studies: 36 journal articles and 4 peer-reviewed conference papers (90% journals)**. The 45-study working pool remains a broader discovery/evidence map; it is not automatically the final reference list. Preprints and generic cloud/AI architecture papers are not counted as primary evidence unless they later satisfy the frozen eligibility criteria.

Each final study is screened and extracted using the same fields: bibliographic metadata, publication status, research problem, cloud/container environment, eBPF hook, telemetry granularity, feature representation, ML method and placement, dataset/workload, attack scenario, baseline, evaluation environment, metrics, overhead, latency, event loss, enforcement mechanism, limitations, reproducibility and quality notes.

## Quality-assessment policy
Quality is assessed using the course-guideline categories **clearly reported / partially reported / not reported** for objective clarity, technical description, dataset/workload transparency, baseline adequacy, evaluation validity, experimental detail, reproducibility, limitation disclosure, external validity and statistical reporting. A numerical score is not used merely to create an artificial ranking.

## Citation policy
The manuscript will use **Harvard author–date** citation consistently. Every DOI and bibliographic record must be verified against a publisher, DOI registry or academic database before the reference list is frozen.

## Final synthesis framework
The final manuscript will organize evidence around:

**Telemetry extraction → feature representation → ML placement → detection decision → kernel enforcement**

and compare studies using:

**detection quality ↔ latency ↔ CPU/memory/event-processing overhead ↔ safety ↔ reproducibility.**
