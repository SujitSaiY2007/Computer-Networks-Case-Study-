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
The intended contribution is not simply a survey of eBPF tools. The review will build an evidence-derived taxonomy across **telemetry extraction → feature representation → ML placement → detection decision → kernel enforcement**, then compare studies using a common framework for **overhead, detection quality, latency, safety, and reproducibility**. The final research agenda will focus on evidence-supported gaps such as dynamic workload drift, constrained in-kernel inference, event loss under stress, and safe active enforcement.

## Review design
Working design: systematic mapping / scoping-style evidence map with critical technical synthesis. PRISMA 2020 is used as the reporting guide where appropriate. The course guide states that emerging fields with heterogeneous terminology and evidence are suitable for scoping or systematic mapping, while a systematic review requires explicit reproducible screening and quality assessment.
