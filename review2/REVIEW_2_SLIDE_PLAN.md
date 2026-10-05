# Review 2 — Presentation Plan

## Objective
Show that the Review 1 topic has now been converted into a defensible literature-review design: a verified primary-study set, consistent extraction/quality criteria, an evidence-derived taxonomy, supported research gaps, and a concrete future research direction.

## Literature-corpus rule
The faculty requirement is a minimum 50 references with a literature-survey table covering all 50 papers.

The project therefore uses two explicitly separated layers:

- 40 canonical primary studies — the unchanged CHAT 01–06 evidence baseline: 36 journals + 4 peer-reviewed conferences = 90% journals.
- 10 supporting/background references — R041–R050, added only to complete the Review 2 50-reference presentation corpus and strengthen context on eBPF meta-security, verifier safety, cloud-native telemetry/latency, service-mesh performance and prior surveys.

The 10 additions do not replace, renumber or alter the canonical primary 40.

The complete Review 2 table is maintained in review2/REVIEW2_50_PAPER_LITERATURE_TABLE.md.

## Slide 1 — Title
**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security**

Subtitle: **Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

Keep the Review 1 title for continuity.

## Slide 2 — From Review 1 to Review 2
- Review 1 established the problem and motivation.
- Review 2 focuses on evidence verification and critical synthesis.
- The working literature pool was audited and refined.
- 50 references are surveyed in Review 2.
- 40 are the canonical primary evidence set.
- 10 are supporting/background references.
- The primary evidence set remains 36 journals + 4 peer-reviewed conferences = 90% journals.

## Slide 3 — Review Design and Guidelines Compliance
- Systematic mapping study / scoping-style evidence map with critical technical synthesis.
- Publication period: January 2020 to final search date, with older/seminal work only where technically necessary.
- Minimum databases: Scopus/Web of Science, IEEE Xplore, ACM Digital Library.
- Additional specialist sources: SpringerLink, ScienceDirect, USENIX and relevant repositories.
- PRISMA-style transparent screening.
- Primary studies and secondary/background studies are explicitly distinguished.

## Slide 4 — 50-Reference Literature Base
Show the corpus without implying that all 50 are primary:

- 40 primary studies
  - 36 journal articles — 90% of primary set
  - 4 peer-reviewed conference papers
- 10 supporting/background references
  - eBPF meta-security/verifier
  - cloud-native telemetry and latency
  - service-mesh performance
  - broader container/microservice runtime-security surveys

Recommended visual: 40 + 10 stacked/bar, with a separate 90/10 indicator for the primary 40.

## Slide 5 — 50-Paper Literature Survey
Use the detailed table from review2/REVIEW2_50_PAPER_LITERATURE_TABLE.md.

Required columns:
1. Serial number
2. Paper title
3. Journal/venue and year
4. Dataset/workload/evidence base
5. Methodology/algorithm
6. Advantages/novelty
7. Disadvantages/gaps/limitations

Do not put all 50 rows on one slide. Use 2–4 readable table slides or an appendix, while the main narrative summarizes the categories.

## Slide 6 — Paper Verification / Quality Framework
For the canonical 40 primary studies, show the frozen qualitative criteria:

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

Supporting/background references should be labelled as such and must not be presented as quality-assessed primary evidence.

Do not present a simple numerical quality score.

## Slide 7 — Existing Technology Landscape
Map the technologies rather than listing papers:

**Telemetry:** eBPF, kprobes, tracepoints, BPF-LSM, TC, XDP
**Runtime tools:** Falco, Tetragon, Tracee, KubeArmor
**ML:** DT/RF/SVM, Autoencoder, VAE/iForest, LSTM, quantized NN
**Enforcement:** BPF-LSM, Seccomp, eBPF maps, XDP
**Policy:** KubeRosy, BPFGuard, Cordon, Optimus, KubeAegis

## Slide 8 — What the Literature Consistently Shows
- eBPF provides fine-grained kernel-level runtime visibility.
- ML can use eBPF-derived behavioural telemetry for anomaly/attack detection.
- Kernel-level placement can reduce data movement but introduces verifier/model constraints.
- Enforcement can reduce response latency but creates safety and false-positive concerns.
- Telemetry richness improves visibility but increases event-processing cost.
- eBPF meta-security and verifier correctness are themselves important deployment constraints.

Use cautious language: “the evidence indicates/suggests,” not “proves.”

## Slide 9 — Evidence-Based Research Gaps
Present the five authoritative gaps plus supporting context:

1. G1 — fragmented/incomplete end-to-end telemetry, buffering and detection-to-mitigation measurement.
2. G2 — limited standardized distribution-shift robustness evaluation.
3. G3 — insufficient common-protocol comparison of ML placement.
4. G4 — less-standardized safe active-enforcement evaluation.
5. G5 — uneven environment/artifact reproducibility.

The supporting literature also reinforces the need to treat verifier safety, eBPF meta-security and multi-tenant isolation as constraints rather than unsupported novelty claims.

## Slide 10 — Proposed Research Direction
Show:

**Controlled workloads → eBPF telemetry → feature extraction → ML detection → policy/risk score → controlled kernel enforcement → mitigation/rollback**

Emphasize that the project is an experimental evaluation of this pipeline and its trade-offs, not a claim that eBPF+ML itself is new.

## Slide 11 — Evaluation Framework
Compare:

- baseline
- eBPF only
- eBPF + user-space ML
- eBPF + feasibility-gated lightweight kernel-local ML
- eBPF + ML + controlled enforcement

Metrics:
- detection quality
- CPU/memory
- event loss
- inference/detection latency
- detection-to-mitigation latency
- legitimate-workload blocking/recovery
- reproducibility/artifact completeness

## Slide 12 — Conclusion / Overall Summary
- The 50-reference survey establishes the technology landscape and evidence context.
- The 40 primary studies provide the authoritative evidence base.
- Five research gaps are supported by cross-paper synthesis.
- The proposed direction is an evaluation/integration contribution rather than an unsupported “first” claim.
- CHAT 06 has already frozen the feasible experimental architecture.
- CHAT 07 implementation is the next technical milestone.

## Presentation rule
Review 2 remains a literature-review presentation, not an implementation demo. The 50-paper table satisfies the faculty literature-survey requirement, while the canonical 40-study evidence baseline remains the basis for formal quality assessment and research-gap claims.
