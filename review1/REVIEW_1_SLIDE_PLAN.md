# Review 1 — Slide Plan

## Slide 1 — Title
**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security**
Subtitle: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs

## Slide 2 — Domain + Why this title
- Domain: Computer Networks → Cloud-Native Security → Kubernetes/Containers → eBPF → ML-based runtime detection.
- Why eBPF: kernel-level visibility across processes, syscalls, files, sockets, namespaces and network paths without requiring a security sidecar in every application container.
- Why ML: eBPF produces high-volume behavioral telemetry; ML can detect patterns beyond fixed rules.
- Why the trade-off framing: richer telemetry can increase overhead; heavier models increase inference latency; stronger kernel enforcement improves response time but raises safety/verifier/false-positive concerns.

## Slide 3 — Papers: eBPF + ML foundations (2021–2024)
1. A Flow-Based IDS Using Machine Learning Entirely in eBPF — arXiv / research record — decision-tree ML entirely in eBPF; reports >20% performance improvement over userspace.
2. Secure Namespaced Kernel Audit for Containers — ACM SoCC — container-granular eBPF audit/IDS/access control in Kubernetes.
3. Detection of Denial of Service Attack in Cloud Based Kubernetes Using eBPF — MDPI Applied Sciences — eBPF/XDP-based Kubernetes DDoS detection/mitigation and overhead evaluation.
4. Container Instrumentation and Enforcement System for Runtime Security of Kubernetes Platform with eBPF — Tech Science Press — LSM-hook runtime enforcement for Kubernetes containers.
5. eBPF: A New Approach to Cloud-Native Observability, Networking and Security — IEEE Access — broad cloud-native eBPF architecture spanning observability, networking and security.

## Slide 4 — Papers: telemetry, detection and container security (2024–2025)
1. Malware Detection in Cloud Native Environments — ACM AICCC — SkyShark eBPF sensor + ML ensemble for RCE/malware behavior.
2. Detecting Cryptojacking Containers Using eBPF-Based Security Runtime and Machine Learning — MDPI Electronics — Tetragon/eBPF syscall + network telemetry and ML for cryptojacking.
3. DeSFAM — IEEE Access — hybrid syscall profiling + VAE/iForest + contextual risk + BPF-LSM enforcement.
4. Comparative Analysis of eBPF-Based Runtime Security Monitoring Tools on Kubernetes — SCITEPRESS — empirical Falco/Tetragon/Tracee runtime-security comparison.
5. CODAX — IEEE Access — eBPF container socket telemetry for semantic DDoS runtime detection.

## Slide 5 — Papers: enforcement, overhead and research gaps (2024–2026)
1. Practicality of in-kernel/user-space packet processing empowered by lightweight neural network and decision tree — Computer Networks / Elsevier — ML placement trade-offs between kernel and userspace.
2. Unsupervised Real-Time In-Kernel Intrusion Detection System Using Autoencoders and eBPF — IEICE — in-kernel unsupervised ML and throughput/latency trade-offs.
3. BPFGuard: Multi-Granularity Container Runtime Mandatory Access Control — IEEE TCC — eBPF container MAC and enforcement granularity/performance.
4. Validating the eBPF Verifier via State Embedding — USENIX OSDI — verifier correctness/safety evidence relevant to trustworthy enforcement.
5. Cordon: Enhancing Security Through Kernel-Level Control in Containerized Computing Environments — Computers & Security — kernel-level container enforcement and operational overhead.

## Presentation message
The literature is not one homogeneous block. The strongest direct evidence combines eBPF telemetry, ML detection, and cloud/container runtime security; adjacent studies are needed to understand in-kernel ML constraints and kernel safety. The review therefore focuses on a three-way trade-off: **telemetry richness ↔ ML detection/latency ↔ safe kernel enforcement**.
