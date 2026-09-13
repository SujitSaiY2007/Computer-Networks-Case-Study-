# Review 2 — Presentation Plan

## Objective
Show that the Review 1 topic has now been converted into a defensible literature-review design: a verified primary-study set, consistent extraction/quality criteria, an evidence-derived taxonomy, supported research gaps, and a concrete future research direction.

## Slide 1 — Title
**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security**

Subtitle: **Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

Keep the Review 1 title for continuity.

## Slide 2 — From Review 1 to Review 2
- Review 1 established the problem and motivation.
- Review 2 focuses on evidence verification and critical synthesis.
- The working 45-study pool has been audited and refined.
- Final target: 40 primary studies, 36 journals + 4 peer-reviewed conferences.
- Journal share: 90%.

## Slide 3 — Review Design and Guidelines Compliance
- Systematic mapping study / scoping-style evidence map with critical technical synthesis.
- Publication period: January 2020 to final search date.
- Minimum databases: Scopus/Web of Science, IEEE Xplore, ACM Digital Library.
- Additional specialist sources: SpringerLink, ScienceDirect, USENIX, arXiv where appropriate.
- PRISMA-style reporting and transparent screening.

## Slide 4 — Final Evidence Base
Show a simple 90/10 donut or bar:

- 36 journal articles — 90%
- 4 peer-reviewed conference papers — 10%

Group the 40 studies into:
1. eBPF telemetry/observability
2. ML detection
3. kernel/user-space ML placement
4. kernel enforcement
5. performance/overhead
6. threat/safety evidence

## Slide 5 — Paper Verification Framework
For every paper, show that the same extraction and quality criteria are applied:

- objective clarity
- technical description
- dataset/workload transparency
- baseline adequacy
- evaluation validity
- experimental detail
- reproducibility
- limitation disclosure
- external validity
- statistical reporting

Do not present a simple numerical quality score.

## Slide 6 — Existing Technology Landscape
Map the technologies rather than listing papers:

**Telemetry:** eBPF, kprobes, tracepoints, BPF-LSM, TC, XDP  
**Runtime tools:** Falco, Tetragon, Tracee, KubeArmor  
**ML:** DT/RF/SVM, Autoencoder, VAE/iForest, LSTM, quantized NN  
**Enforcement:** BPF-LSM, Seccomp, eBPF maps, XDP  
**Policy:** KubeRosy, BPFGuard, Cordon, Optimus, KubeAegis

## Slide 7 — What the Literature Consistently Shows
- eBPF provides fine-grained kernel-level runtime visibility.
- ML can use eBPF-derived behavioural telemetry for anomaly/attack detection.
- Kernel-level placement can reduce data movement but introduces verifier/model constraints.
- Enforcement can reduce response latency but creates safety and false-positive concerns.
- Telemetry richness improves visibility but increases event-processing cost.

Use cautious language: “the evidence indicates/suggests,” not “proves.”

## Slide 8 — Evidence-Based Research Gaps
Present 5–7 concise gaps:

1. Fragmented telemetry modalities.
2. Attack-specific/small datasets and weak distribution-shift evaluation.
3. No settled rule for in-kernel versus user-space ML placement.
4. Inconsistent overhead/latency benchmarks.
5. Detection studied more consistently than safe autonomous enforcement.
6. Limited adversarial robustness and eBPF meta-security evaluation.
7. Reproducibility and portability limitations.

## Slide 9 — Proposed Research Direction
Show:

**Kubernetes workloads → eBPF telemetry → feature extraction → ML detection → policy/risk score → kernel enforcement → mitigation**

Emphasize that the project is an experimental evaluation of this pipeline and its trade-offs, not a claim that eBPF+ML itself is new.

## Slide 10 — Evaluation Framework
Compare:

- baseline
- eBPF only
- eBPF + user-space ML
- eBPF + lightweight in-kernel ML
- eBPF + ML + enforcement

Metrics:
- detection quality
- CPU/memory
- event loss
- inference/detection latency
- detection-to-mitigation latency
- legitimate-workload blocking

## Slide 11 — Next Milestone
- Complete full-text verification of the 40 papers.
- Freeze the extraction matrix.
- Complete quality assessment.
- Finalize evidence-based gap table.
- Select the experimental architecture.
- Define dataset/workload/attack testbed.
- Begin prototype implementation.

## Presentation rule
Review 2 should still be a **literature-review presentation**, not an implementation demo. The goal is to demonstrate that the selected evidence is credible, relevant, comparable and sufficient to justify the proposed research direction.
