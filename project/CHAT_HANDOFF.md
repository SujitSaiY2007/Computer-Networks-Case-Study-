# Active Chat Handoff — BACSE203 Project

## How to use this file

This is the **live continuity checkpoint** between project chats.

At the beginning of every new project chat:

1. Read this file first.
2. Read the canonical files named under **Read Before Starting**.
3. Execute only the task described by **Active Continuation Prompt** unless a dependency requires a small correction.
4. Do not assume that an old chat transcript is the source of truth when the repository contains a newer decision.

At the end of every project chat:

1. Complete the assigned task as far as possible.
2. Record what was actually completed.
3. Record every important decision or change.
4. Record unresolved issues and deviations.
5. Update the active continuation prompt so it points to the **next unfinished task**.
6. Commit the updated handoff and any project artifacts to GitHub.

This file is intentionally short enough to be the first context file opened, while `MASTER_EXECUTION_PLAN.md` contains the full roadmap and all phase prompts.

---

## Project identity

**Title:** eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs

**Course:** BACSE203 Computer Networks Case Study

**Current stage:** Review 2 preparation → CHAT 07 Prototype Implementation / Experimental Infrastructure

**Project principle:** repository state + original paper evidence + course guidelines are the durable source of truth.

---

## Current status

- Review 1: **COMPLETE**
- Review 2 candidate paper selection: **PROVISIONAL / COMPLETE FOR CANDIDATE STAGE**
- Verified primary-study baseline: **40 papers**
- Verified composition: **36 journals + 4 peer-reviewed conferences = 90% journals**
- CHAT 01 screening: **COMPLETE**
- Candidate correction: **1 survey removed; 1 verified journal primary study substituted**
- Paper acquisition/archive: **ACCESS REGISTER COMPLETE — local PDF archiving remains a private/local responsibility where required**
- CHAT 02 evidence extraction: **COMPLETE**
- Quality assessment: **COMPLETE**
- Evidence taxonomy: **COMPLETE**
- Research-gap agenda: **COMPLETE**
- Experimental architecture: **COMPLETE / FROZEN IN CHAT 06**
- Prototype: **CHAT 07 PARTIAL / BLOCKED PENDING NATIVE LINUX VALIDATION**
- Experiments: **NOT STARTED**
- Review 2 PPT: **PLAN EXISTS, FINAL PPT NOT COMPLETE**
- Manuscript: **NOT FINAL**

### Important scope correction

A recent 2026 systematic literature review on eBPF cybersecurity exists. Therefore the project must **not** claim to be the first review of eBPF cybersecurity. The defensible contribution is the narrower intersection of eBPF telemetry, ML runtime detection and kernel-level enforcement in cloud/container environments, emphasizing telemetry overhead, ML placement, detection-to-mitigation latency, enforcement safety and evaluation practice.

### Important evidence rule

The 40 papers are candidate studies selected for verification. They must not be described as fully verified/final until Chat 01 completes the screening and records inclusion/exclusion decisions.

### New paper-archive rule

After Chat 01 verifies the retained primary-study set, Chat 02A will acquire and archive legitimate full-text PDFs before detailed extraction. Actual copyrighted PDFs remain in the user's private/local archive and are **not** committed to the public GitHub repository. The repository will contain the access register, DOI/official links, acquisition status and verification notes.

---

## Read before starting the next chat

Mandatory:

- `project/CHAT_HANDOFF.md`
- `project/MASTER_EXECUTION_PLAN.md`
- `project/PROJECT_SCOPE_AND_RQS.md`
- `research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md`
- `research/RESEARCH_EVIDENCE_MATRIX.md`
- `research/RELEVANCY_AUDIT.md`
- `research/SEARCH_LOG.md`

For paper acquisition specifically:

- `research/PAPER_ACQUISITION_AND_ARCHIVE.md`

As needed:

- `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`
- `review2/REVIEW_2_SLIDE_PLAN.md`
- `review1/REVIEW_1_SLIDE_PLAN.md`

---

# Active Continuation Prompt

> **CHAT 07 — RESUME PROTOTYPE IMPLEMENTATION / EXPERIMENTAL INFRASTRUCTURE**
>
> Continue from the partially implemented CHAT 07 state on the latest committed `main`.
>
> CHAT 01–06 remain COMPLETE. The canonical primary-study baseline remains exactly **40 studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals**. Do not add, remove, replace or re-screen any primary study. P021 and P031 remain unchanged.
>
> Read first:
> 1. `project/CHAT_HANDOFF.md`
> 2. `README.md`
> 3. `project/MASTER_EXECUTION_PLAN.md`
> 4. `research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md`
> 5. `research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md`
>
> CHAT 07 implementation files already exist under `prototype/`. Do not redesign the architecture.
>
> First run `prototype/preflight.sh` on the required Linux validation host. The previous execution environment was blocked because it lacked Docker, bpftool, libbpf development headers and a Clang BPF target.
>
> Then:
> 1. validate/build/load the BPF telemetry;
> 2. validate ring-buffer generated/submitted/consumed/reservation-failure/sequence-gap accounting;
> 3. validate container → process → cgroup → BPF-event identity;
> 4. run the Python unit tests and CI-equivalent tests;
> 5. run the complete workload → BPF → ring-buffer → feature vector → user-space LR → decision → recorded-result smoke test;
> 6. generate the reproducibility manifest;
> 7. only after all preceding gates pass, attempt the fixed-point kernel-local LR feasibility gate;
> 8. if the kernel-local gate fails, record exact verifier/load evidence and retain the user-space/hybrid fallback.
>
> Do not run the final 10-repetition experiment matrix, distribution-shift study, final statistical tests, ablation study or superiority comparison in CHAT 07.
>
> Update `research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md`, `README.md`, `project/MASTER_EXECUTION_PLAN.md` and this handoff with exact validation evidence. Mark CHAT 07 **COMPLETE only if every completion criterion in the original CHAT 07 specification is actually satisfied**. Otherwise keep it BLOCKED/PARTIAL and state the exact remaining gate.
>
> If CHAT 07 becomes complete, prepare the exact CHAT 08 continuation prompt for controlled experiments. If it remains incomplete, prepare the next CHAT 07 continuation prompt instead.


# Chat completion log

### CHAT 00 — Control/workflow setup
**Status:** COMPLETE

Completed:
- Established multi-chat execution model.
- Created the master phase-by-phase roadmap.
- Defined repository-as-memory rules.
- Defined mandatory end-of-chat handoff update.
- Defined exact continuation-prompt workflow.
- Established Chat 01 as the next project task.

### Workflow amendment — Paper acquisition phase
**Status:** COMPLETE

Completed:
- Inserted **CHAT 02A — Paper Acquisition & Archive** between verification and evidence extraction.
- Created `research/PAPER_ACQUISITION_AND_ARCHIVE.md`.
- Established legitimate-access and private/local-PDF rules.
- Established the paper access register requirements.
- Updated this handoff so Chat 01 now hands off to Chat 02A rather than directly to extraction.

Design decision:
- The existing Chat 02–13 numbering remains stable. The acquisition checkpoint is intentionally labelled **02A** rather than renumbering all later phases.

Changed files:
- `research/PAPER_ACQUISITION_AND_ARCHIVE.md`
- `project/CHAT_HANDOFF.md`
- `README.md` / workflow documentation as applicable

Next task:
- CHAT 01 — Full-text verification and final candidate screening.
- After Chat 01: CHAT 02A — Paper Acquisition & Archive.

---

## Handoff update template for every future chat

Copy this structure into the completion log when closing a chat:

### CHAT XX — [Task name]
**Status:** COMPLETE / PARTIAL / BLOCKED

**Completed work:**
- ...

**Files changed:**
- ...

**Decisions frozen:**
- ...

**Evidence/issues discovered:**
- ...

**Deviations from plan:**
- None / ...

**Next task:**
- CHAT XX — ...

**Updated continuation prompt:**
> [Exact prompt for the next chat, customized to the newly completed state.]


### CHAT 01 — Full-text verification and final candidate screening
**Status:** COMPLETE

**Completed work:**
- Audited the live repository state and canonical Review 2 control files.
- Verified the 40-study candidate set against authoritative publisher/venue/DOI records and accessible full-text/abstract evidence.
- Ran scholarly identifier/retraction checks across the candidate set.
- Corrected the CODAX bibliographic title/DOI record and the Optimus/Coda DOI records where the repository metadata was stale.
- Removed the non-primary review *Extended Berkeley Packet Filter: An Application Perspective* from the primary set.
- Added the verified 2026 IEEE TCC primary study *Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks* as the replacement.
- Confirmed the final screening baseline at 40 primary studies: 36 journals + 4 peer-reviewed conferences = 90% journals.
- Classified 14 as Core and 26 as Supporting/Adjacent.

**Files changed:**
- research/CHAT01_FULLTEXT_VERIFICATION.md
- research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md
- research/RESEARCH_EVIDENCE_MATRIX.md
- research/RELEVANCY_AUDIT.md
- project/CHAT_HANDOFF.md

**Decisions frozen:**
- The 40-study primary baseline is the verified starting point for CHAT 02A.
- Reviews remain background/comparison literature and are not counted as primary evidence.
- No preprint-only record is counted in the 40.
- Detailed extraction and formal quality assessment remain separate downstream stages.

**Evidence/issues discovered:**
- Some retained studies have authoritative metadata/abstract evidence but require legitimate full-text acquisition before complete field-level extraction.
- The 2026 IJCA host-anomaly study is retained only as Supporting/Adjacent evidence; venue/indexing quality must be considered during formal quality assessment.
- Network/IoT/host-layer studies are intentionally retained only where they directly inform ML placement, telemetry overhead, safety, enforcement, or evaluation questions.

**Deviations from plan:**
- One candidate survey was removed because the frozen scope requires primary studies. One verified journal primary study was substituted to preserve the target composition without relabeling the survey.

**Next task:**
- CHAT 02A — Paper Acquisition & Archive.


---

## CHAT 02A — Paper Acquisition & Archive
**Status:** PARTIAL/BLOCKED

**Completed work:**
- Preserved the verified 40-study baseline exactly: 36 journal articles + 4 peer-reviewed conferences.
- Created/finalized the acquisition register in research/PAPER_ACQUISITION_AND_ARCHIVE.md with one row for every retained study.
- Located and recorded legitimate publisher, institutional, author-repository, KCI, USENIX, Springer, MDPI, TechScience, Wiley and other scholarly access routes where available.
- Checked accessible full-text records against title/DOI/publication metadata.
- Recorded institutional/library access requirements instead of excluding papers.
- Confirmed that no unauthorized or pirated source was used.
- Attempted local PDF materialization; the execution environment did not successfully download/materialize an openly accessible Springer PDF. Therefore no local PDF archive is falsely claimed as complete.

**Acquisition counts:**
- Retained studies: **40**
- Legitimate full-text copies/routes located and marked OBTAINED: **26**
- Institutional/library access required: **14**
- Legitimately unavailable: **0**
- Metadata/PDF records needing review: **0**

**Important qualification:** “OBTAINED” means a legitimate full-text copy was located/accessed through the recorded scholarly route; it does **not** mean that a local PDF file was successfully materialized in this environment.

**DOI/title/PDF mismatches:**
- No new mismatch requiring a change to the frozen 40-study baseline.
- The previously verified P004 author-version record contains pre-publication pagination artefacts; the DOI/publisher metadata remains canonical.
- P034 remains the verified replacement for the excluded review article; no new bibliographic issue was found.

**Unresolved acquisition problems:**
- Local/private PDF materialization remains incomplete.
- The 18 institutional/library-access records require the user's legitimate institutional/library route before detailed extraction.
- Supplementary-material availability has not yet been systematically checked.

**Files changed:**
- research/PAPER_ACQUISITION_AND_ARCHIVE.md
- project/CHAT_HANDOFF.md
- README.md
- project/MASTER_EXECUTION_PLAN.md

**Deviations from planned workflow:**
- CHAT 02A could not reach the local-PDF completion gate because the runtime could not materialize web-hosted PDFs. The project was deliberately left PARTIAL/BLOCKED rather than claiming completion.
- No paper-selection or classification decision was changed.

**Next task:** Resolve legitimate local full-text access/materialization, then begin **CHAT 02 — Evidence Extraction Matrix** only after the corpus is stable.

### Exact continuation prompt — CHAT 02 — Evidence Extraction Matrix

> Continue the BACSE203 Computer Networks Case Study from the latest committed GitHub state.
>
> First read:
> 1. project/CHAT_HANDOFF.md
> 2. README.md
> 3. project/MASTER_EXECUTION_PLAN.md
> 4. project/PROJECT_SCOPE_AND_RQS.md
> 5. research/CHAT01_FULLTEXT_VERIFICATION.md
> 6. research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md
> 7. research/RESEARCH_EVIDENCE_MATRIX.md
> 8. research/PAPER_ACQUISITION_AND_ARCHIVE.md
>
> Do not restart paper selection and do not alter the frozen 40-study baseline: 36 journals + 4 peer-reviewed conferences, 90% journals.
>
> First verify whether the private/local full-text corpus has been materialized or whether legitimate institutional/library access is available for the studies marked accordingly. Use the acquisition register as the authoritative access map. Do not exclude a study merely because access remains difficult.
>
> Once a stable full-text corpus is available, execute CHAT 02 — EVIDENCE EXTRACTION MATRIX. For each of the 40 retained studies extract only evidence supported by the authoritative full text: authors, year, venue/publisher, DOI, publication type, cloud/container/Kubernetes environment, eBPF hook and telemetry type, telemetry granularity, feature representation, ML algorithm, ML placement, dataset/workload, attack/threat scenario, baseline, testbed, CPU overhead, memory overhead, event rate/buffering/event loss, detection metrics, inference/detection latency, detection-to-mitigation latency, enforcement mechanism, legitimate-operation impact, reproducibility artifacts, limitations, external-validity concerns and RQ1–RQ5 mapping.
>
> Use “Not reported” whenever the paper does not provide a field. Do not infer numerical values from abstracts, search snippets, reviews, or other papers. Keep reported results separate from cross-paper interpretation.
>
> Do not perform formal quality scoring, final cross-paper conclusions, research-gap freezing, experimental architecture design, prototype implementation, or Review 2 slide creation in CHAT 02.
>
> At the end, update project/CHAT_HANDOFF.md and all relevant research status files with the extraction status, missing-evidence issues, files changed, and the exact next continuation prompt for CHAT 03 — Quality Assessment.


### CHAT 02 — Corpus verification checkpoint — 5 October 2026
**Status:** BLOCKED AT CORPUS GATE

**Completed work:**
- Re-read the required canonical project/research control files from the latest committed `main` state.
- Preserved the frozen 40-study baseline exactly: 36 journals + 4 peer-reviewed conferences = 90% journals.
- Rechecked the authoritative acquisition map against the actual connected Library and mounted local workspace.
- Confirmed that no retained P001–P040 PDFs are present in the mounted local workspace.
- Confirmed that the connected Library search did not surface the retained study PDFs.
- Confirmed that the 14 institutional/library-access records remain unresolved from this environment.
- Did not start evidence extraction, because doing so would require treating inaccessible full text as if it had been inspected.

**Files changed:**
- project/CHAT_HANDOFF.md
- README.md
- project/MASTER_EXECUTION_PLAN.md
- research/RESEARCH_EVIDENCE_MATRIX.md
- research/PAPER_ACQUISITION_AND_ARCHIVE.md

**Decisions frozen:**
- The 40-study baseline is unchanged.
- No study is excluded because of access difficulty.
- “Not reported” will only be used after authoritative full-text inspection shows that the field is absent.
- CHAT 02 remains unfinished until the corpus/access gate is satisfied.

**Evidence/issues discovered:**
- 0 local P001–P040 PDFs found in the mounted workspace.
- 0 retained study PDFs surfaced by the connected Library search.
- 26 legitimate full-text routes remain recorded, but “OBTAINED” in the acquisition register does not prove local materialization.
- 14 studies still require legitimate institutional/library access: P002, P009, P014, P015, P019, P020, P021, P024, P026, P027, P031, P034, P035, P037.

**Deviations from plan:**
- CHAT 02 cannot honestly be marked complete. Extraction is deferred until the corpus/access gate is satisfied.

**Next task:**
- Resume CHAT 02 — Evidence Extraction Matrix after the private/local corpus is materialized or legitimate institutional/library access is available for the unresolved records.

**Updated continuation prompt:**
> Resume CHAT 02 — EVIDENCE EXTRACTION MATRIX from the latest committed state. Re-check the corpus/access gate first. Do not alter the frozen 40-study baseline. Once authoritative full texts are available, extract only supported evidence for all 40 studies, use “Not reported” only after full-text inspection, keep reported results separate from interpretation, and do not perform quality assessment or later phases. If extraction is completed, update the handoff with the exact continuation prompt for CHAT 03 — Quality Assessment.


## CHAT 02 replacement checkpoint — 5 October 2026

P021 → Takagaki & Mizutani (2025), DOI 10.1002/tee.70070. P031 → Rohliyanto & Utami (2026), DOI 10.30865/jurikom.v13i2.9618. Both are directly accessible journal primary studies. The replacement decision is complete; the full CHAT 02 extraction gate is not yet complete because the remaining corpus is not actually present in the current environment.


## CHAT 02 — Evidence Extraction Matrix
**Status:** COMPLETE

**Completed work:**
- Corrected P021 and P031 before extraction using directly accessible journal primary studies.
- Created `research/CHAT02_EVIDENCE_EXTRACTION.md` containing the canonical extraction for all 40 active studies.
- Extracted environment, telemetry, feature/ML placement, workload/attack, reported performance/latency, enforcement/response and RQ mapping.
- Preserved the rule that unavailable numerical fields are **NR/NA**, not guessed.
- Kept formal quality assessment and cross-paper conclusions outside CHAT 02.

**Files changed:**
- research/CHAT02_EVIDENCE_EXTRACTION.md
- project/CHAT_HANDOFF.md
- research/RESEARCH_EVIDENCE_MATRIX.md

**Decisions frozen:**
- 40-study baseline unchanged after the P021/P031 correction.
- Composition remains 36 journals + 4 peer-reviewed conferences.
- CHAT 02 is complete; CHAT 03 is the next phase.

**Next task:** CHAT 03 — Quality Assessment.


## CHAT 03 — Quality Assessment
**Status:** COMPLETE

**Completed work:**
- Assessed all 40 retained studies across the ten frozen qualitative dimensions.
- Used only Clearly reported / Partially reported / Not reported.
- Kept study role, reported evidence, quality judgement and cross-paper interpretation distinct.
- Did not alter the 40-study baseline or replace any study.
- Created `research/CHAT03_QUALITY_ASSESSMENT.md`.

**Key quality findings:**
- Objective clarity and technical/system description are the most consistently reported dimensions.
- Statistical reporting, reproducibility and external validity are recurring weaknesses.
- CPU/memory reporting is more common than standardized end-to-end latency, event-loss/buffering, or detection-to-mitigation latency.
- Core studies provide stronger direct runtime-security evidence; Supporting/Adjacent studies provide important architecture, networking, enforcement and threat evidence but are not equivalent end-to-end ML evidence.

**Files changed:**
- research/CHAT03_QUALITY_ASSESSMENT.md
- project/CHAT_HANDOFF.md
- README.md
- project/MASTER_EXECUTION_PLAN.md
- research/RESEARCH_EVIDENCE_MATRIX.md
- research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md

**Decisions frozen:**
- CHAT 03 is complete.
- The 40-study baseline remains unchanged: 36 journals + 4 peer-reviewed conferences.
- No numerical quality score is used.
- No final research gap is frozen in CHAT 03.

**Next task:** CHAT 04 — Critical Synthesis / Technology Taxonomy.

### Exact continuation prompt — CHAT 04

> Continue the BACSE203 Computer Networks Case Study from the latest committed GitHub state.
>
> **CHAT 03 — Quality Assessment is COMPLETE.** The canonical baseline remains exactly **40 primary studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals**. Do not restart selection, acquisition, or evidence extraction. Do not replace P021 or P031.
>
> Read before starting: `project/CHAT_HANDOFF.md`, `README.md`, `project/MASTER_EXECUTION_PLAN.md`, `project/PROJECT_SCOPE_AND_RQS.md`, `research/CHAT01_FULLTEXT_VERIFICATION.md`, `research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md`, `research/RESEARCH_EVIDENCE_MATRIX.md`, `research/CHAT02_EVIDENCE_EXTRACTION.md`, `research/PAPER_ACQUISITION_AND_ARCHIVE.md`, `research/CHAT03_QUALITY_ASSESSMENT.md`, and `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`.
>
> **CHAT 04 objective — Critical Synthesis / Technology Taxonomy:** synthesize the completed extraction + quality evidence without changing the corpus. Build an evidence-grounded taxonomy covering telemetry sources/hooks, feature representations, ML families, ML placement, detection targets, enforcement mechanisms, adaptation/continual learning, overhead/latency measurement, datasets/workloads, and evaluation practices.
>
> Compare Core against Supporting/Adjacent evidence explicitly. Distinguish direct evidence from architectural/supporting evidence. Identify convergence, contradictions, trade-offs and evidence-strength patterns. Do not yet freeze the final research gaps or design the final experimental architecture.
>
> Required outputs: `research/CHAT04_CRITICAL_SYNTHESIS.md`; update `research/RESEARCH_EVIDENCE_MATRIX.md`, `README.md`, `project/MASTER_EXECUTION_PLAN.md`, and `project/CHAT_HANDOFF.md`; record the exact next continuation prompt for **CHAT 05 — Research Gap Consolidation / Evidence-to-Design Bridge**.
>
> Keep reported evidence, cross-paper synthesis, and new inference clearly separated. No numerical quality scoring and no new paper search unless a genuine bibliographic inconsistency must be documented without changing the baseline.


### CHAT 04 — Critical Synthesis / Technology Taxonomy
**Status:** COMPLETE

**Completed work:**
- Built the cross-paper technology taxonomy from CHAT 02 evidence extraction and CHAT 03 qualitative assessment.
- Classified telemetry sources, eBPF/kernel mechanisms, feature representations, ML approaches and placement, detection targets, enforcement, adaptation, performance, datasets/workloads and evaluation environments.
- Synthesized convergence, divergence, trade-offs, recurring architecture/evaluation patterns and evidence strength.
- Explicitly separated Core evidence from Supporting/Adjacent evidence.
- Recorded literature-supported unresolved tensions and labelled evidence-to-gap observations as preliminary only.

**Files changed:**
- `research/CHAT04_CRITICAL_SYNTHESIS.md`
- `project/CHAT_HANDOFF.md`
- `README.md`
- `project/MASTER_EXECUTION_PLAN.md`
- `research/RESEARCH_EVIDENCE_MATRIX.md`
- `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`

**Decisions frozen:**
- The 40-study baseline remains unchanged: 36 journals + 4 peer-reviewed conferences.
- P021 and P031 remain the active corrected records.
- CHAT 04 does not freeze final research gaps or the experimental architecture.
- Reported evidence, cross-paper synthesis and inference are explicitly separated.

**Evidence/issues discovered:**
- Syscall/kernel telemetry and network/XDP telemetry are the dominant evidence families, with file/process/timing/namespace context providing complementary information.
- ML placement is heterogeneous; in-kernel, user-space and hybrid approaches expose a clear complexity/latency/programmability trade-off.
- Detection evidence is broader than standardized detection-to-mitigation evidence.
- Event loss/buffering, repeated-run statistical uncertainty and cross-environment validation remain inconsistently reported.
- Online/adaptive learning evidence is concentrated rather than corpus-wide.

**Deviations from plan:**
- None.

**Next task:**
- CHAT 05 — Research Gap Consolidation / Evidence-to-Design Bridge.

**Updated continuation prompt:**
> See the exact CHAT 05 prompt at the top of this file.

---

## CHAT 05 — Research Gap Consolidation / Evidence-to-Design Bridge
**Status:** COMPLETE

**Completed work**
- Evaluated all six CHAT 04 candidate observations against the completed 40-study evidence base.
- Retained five final gaps; merged A and C as one end-to-end measurement/completeness gap.
- Mapped each retained gap to the actual RQs and to derived requirements.
- Formulated the central research problem and a cautious novelty position.
- Recorded rejected/downgraded overclaims and remaining uncertainty.
- Created `research/CHAT05_RESEARCH_GAP_CONSOLIDATION.md` and consolidated `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`.

**Files changed**
- `research/CHAT05_RESEARCH_GAP_CONSOLIDATION.md`
- `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`
- `research/RESEARCH_EVIDENCE_MATRIX.md`
- `README.md`
- `project/MASTER_EXECUTION_PLAN.md`
- `project/CHAT_HANDOFF.md`

**Decisions frozen**
- 40-study baseline unchanged: 36 journals + 4 peer-reviewed conferences.
- P021/P031 unchanged.
- Final gaps: G1 end-to-end latency/telemetry completeness; G2 distribution-shift robustness; G3 common-protocol ML-placement comparison; G4 safe enforcement evaluation; G5 reproducible environment/artifact specification.
- Contribution is framed as controlled evaluation/integration and reproducibility, not an unsupported “first” claim.

**Unresolved issues**
- Exact architecture, hardware/software constraints, datasets/workloads and attack scenarios remain open.
- Robustness and enforcement scope must remain student-feasible.

## Active continuation prompt — CHAT 06 — Experimental Architecture + Testbed Specification

> Continue the BACSE203 Computer Networks Case Study from the latest committed `main` state.
>
> CHAT 01, CHAT 02A, CHAT 02, CHAT 03, CHAT 04 and CHAT 05 are COMPLETE.
>
> The canonical baseline remains exactly **40 studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals**. Do not add, remove, replace or re-screen any primary study. P021 and P031 remain unchanged.
>
> Read first:
> 1. `project/CHAT_HANDOFF.md`
> 2. `README.md`
> 3. `project/MASTER_EXECUTION_PLAN.md`
> 4. `project/PROJECT_SCOPE_AND_RQS.md`
> 5. `research/CHAT01_FULLTEXT_VERIFICATION.md`
> 6. `research/PAPER_ACQUISITION_AND_ARCHIVE.md`
> 7. `research/CHAT02_EVIDENCE_EXTRACTION.md`
> 8. `research/CHAT03_QUALITY_ASSESSMENT.md`
> 9. `research/CHAT04_CRITICAL_SYNTHESIS.md`
> 10. `research/CHAT05_RESEARCH_GAP_CONSOLIDATION.md`
> 11. `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`
> 12. `research/RESEARCH_EVIDENCE_MATRIX.md`
>
> Objective: translate G1–G5 into a **feasible experimental architecture and testbed specification**. Do not silently change the RQs or claim novelty not established by the literature.
>
> Derive explicit requirements first: end-to-end timestamping/telemetry completeness; at least two feasible ML-placement variants; one feasible distribution-shift condition; staged measurable enforcement safety; and reproducible environment/artifact capture.
>
> Compare feasible alternatives before selecting one. At minimum assess:
> 1. baseline/no security ML;
> 2. eBPF telemetry only;
> 3. eBPF + user-space ML;
> 4. eBPF + lightweight in-kernel or kernel-local ML **only if technically feasible**;
> 5. eBPF + ML + controlled enforcement.
>
> Specify telemetry hooks, feature pipeline, model placement, decision/policy mechanism, enforcement point, benign workloads, attack scenarios, ground truth, train/test split, distribution-shift condition, controls, metrics, ablations, safety/rollback conditions and reproducibility artifacts. Every component must trace to an RQ or validated gap and remain student-feasible.
>
> Do not implement the prototype or run final experiments in CHAT 06. Produce the architecture/testbed specification first.
>
> Completion requires the architecture requirements traceability, selected architecture with alternatives rejected for explicit reasons, experiment matrix, workload/attack/test conditions, measurement/statistical plan, safety constraints, reproducibility plan, feasibility risks, updated control files, and the exact next continuation prompt.


---

## CHAT 06 — Experimental Architecture + Testbed Specification
**Status:** COMPLETE

**Completed work**
- Audited the committed main state at the end of CHAT 05.
- Converted G1–G5 into explicit architecture and testbed requirements.
- Compared baseline, eBPF-only, user-space ML, feasibility-gated kernel-local ML, and controlled-enforcement configurations.
- Selected a student-feasible single-host native-container architecture.
- Specified syscall/process telemetry, BPF ring-buffer transport, timestamps, event-loss accounting and feature pipeline.
- Selected Logistic Regression as the primary placement-comparison model because the same mathematical model can be represented in user space and a bounded fixed-point kernel-local implementation.
- Specified safe anomaly scenarios, development/ID/shifted distributions, staged enforcement, metrics, statistics, ablations and reproducibility artifacts.
- Added explicit feasibility gates and fallbacks rather than assuming kernel-local ML will work.
- Created `research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md`.

**Files changed**
- research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md
- research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md
- README.md
- project/MASTER_EXECUTION_PLAN.md
- project/CHAT_HANDOFF.md

**Decisions frozen**
- 40-study baseline unchanged; P021/P031 unchanged.
- Primary architecture: single-host Linux + native containers + syscall/process eBPF telemetry + ring buffer + common feature pipeline + user-space LR.
- Kernel-local fixed-point LR is feasibility-gated; hybrid/user-space fallback is mandatory if the gate fails.
- No GPU, Kafka, distributed cluster, continual-learning framework or multimodal telemetry in the primary experiment.
- Kubernetes is deferred for the primary controlled experiment.
- Enforcement is staged, isolated and reversible.
- CHAT 06 produced no prototype and no final experimental result.

**Evidence/technical basis**
- Current upstream Linux documentation was checked for BPF verifier, libbpf, ring buffer, BPF LSM and cgroup mechanisms.
- Ubuntu kernel documentation was checked for the LTS/GA kernel baseline.
- These sources establish mechanism availability, not performance results.

**Next task**
- CHAT 07 — Prototype Implementation / Experimental Infrastructure.

## Active continuation prompt — CHAT 07 — Prototype Implementation / Experimental Infrastructure

> Continue the BACSE203 Computer Networks Case Study from the latest committed main state.
>
> CHAT 01, CHAT 02A, CHAT 02, CHAT 03, CHAT 04, CHAT 05 and CHAT 06 are COMPLETE.
>
> The canonical primary-study baseline remains exactly **40 studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals**. Do not add, remove, replace or re-screen any primary study. P021 and P031 remain unchanged.
>
> Read first:
> 1. project/CHAT_HANDOFF.md
> 2. README.md
> 3. project/MASTER_EXECUTION_PLAN.md
> 4. project/PROJECT_SCOPE_AND_RQS.md
> 5. research/CHAT05_RESEARCH_GAP_CONSOLIDATION.md
> 6. research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md
> 7. research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md
> 8. research/RESEARCH_EVIDENCE_MATRIX.md
>
> Implement only the architecture frozen in CHAT 06. Do not broaden scope.
>
> Primary implementation target:
> - single-host Ubuntu 24.04 LTS baseline with the exact kernel package/version recorded in the environment manifest;
> - native Docker containers;
> - libbpf + bpftool + Clang/LLVM;
> - syscall/process tracepoint telemetry;
> - BPF ring-buffer transport with event sequence/loss accounting;
> - deterministic feature aggregation;
> - user-space Logistic Regression as the first ML path;
> - staged observe/log/controlled-mitigation state machine;
> - complete experiment manifest and reproducibility capture.
>
> Treat kernel-local fixed-point Logistic Regression as a feasibility-gated implementation. Attempt it only after the user-space path and telemetry accounting are stable. If the verifier/load or equivalence gate fails, use the documented hybrid fallback; do not weaken safety or invent a result.
>
> CHAT 07 must produce infrastructure and validation checks, not final research conclusions. Do not run the final experiment matrix or claim measured superiority.
>
> Required completion:
> 1. repository implementation structure created;
> 2. environment/preflight script created;
> 3. BPF telemetry loader and ring-buffer path implemented;
> 4. event sequence/loss accounting implemented;
> 5. feature pipeline and data schema implemented;
> 6. user-space LR training/inference path implemented;
> 7. staged policy state machine implemented in safe test mode;
> 8. reproducibility manifest capture implemented;
> 9. unit/integration/smoke tests pass;
> 10. kernel-local feasibility gate either passes or is explicitly blocked with evidence and fallback retained;
> 11. README, master plan and handoff updated;
> 12. exact CHAT 08 continuation prompt prepared.



---

## CHAT 07 implementation checkpoint — 5 October 2026

**Status: PARTIAL / BLOCKED — do not mark COMPLETE.**

Implemented the minimum prototype infrastructure under `prototype/` and recorded the validation state in `research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md`.

### Implemented
- preflight/environment capture;
- BPF syscall/process telemetry source and libbpf loader;
- ring-buffer event stream and accounting fields;
- deterministic 1-second feature aggregation;
- user-space Logistic Regression artifact/inference path;
- staged safe-default policy state machine;
- reproducibility manifest;
- baseline configuration;
- unit tests and GitHub Actions CI configuration.

### Validation blocker
The current execution host is not the frozen CHAT 06 environment: Docker and bpftool are absent, libbpf development headers are absent, and the installed Clang has no BPF target. Therefore native BPF load, ring-buffer integration, container identity integration and the full smoke path could not honestly be marked passed.

The kernel-local LR feasibility gate was correctly **not attempted** because its prerequisites are not yet validated.

### Scientific boundary
No performance, detection, robustness, enforcement, superiority or novelty claim is made from CHAT 07 implementation work.

### Next
Resume CHAT 07 on the required Ubuntu 24.04 LTS / 6.8-series validation host and complete the blocked gates before starting CHAT 08.


---

## Review 2 literature-corpus integration checkpoint — 5 October 2026

**Status: COMPLETE**

The faculty Review 2 instruction was checked and the remaining ten relevant, accessible references have been integrated into the repository without disturbing the canonical primary evidence baseline.

### Completed

- Built the Review 2 **50-reference literature corpus**.
- Preserved the canonical **40 primary studies = 36 journals + 4 peer-reviewed conferences**.
- Added **R041–R050** as explicitly labelled supporting/background references.
- Created review2/REVIEW2_50_PAPER_LITERATURE_TABLE.md with the required faculty columns.
- Updated review2/REVIEW_2_SLIDE_PLAN.md for the 50-reference requirement.
- Updated research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md, README.md and this handoff.
- Kept secondary reviews clearly separate from primary evidence.
- No final experimental, performance, superiority or novelty claim was introduced.

### Important methodological decision

The ten additions are a **Review 2 presentation/reference expansion**, not a replacement or silent modification of the 40-study systematic evidence baseline. CHAT 02–05 evidence and gap conclusions continue to use the canonical 40.

### Active next task

Resume **CHAT 07 — Prototype Implementation / Experimental Infrastructure** on the required Ubuntu 24.04 LTS / pinned 6.8-series validation host.

The immediate CHAT 07 gates remain:
1. preflight;
2. native BPF build/load;
3. ring-buffer event accounting;
4. container PID/cgroup identity;
5. feature pipeline and user-space LR;
6. staged policy smoke test;
7. reproducibility manifest;
8. kernel-local LR feasibility gate only after prerequisites pass.

Do not run the final experiment matrix or make superiority claims in CHAT 07.

## Active continuation prompt — CHAT 07 after Review 2 corpus completion

> Continue the BACSE203 Computer Networks Case Study from the latest committed main state.
>
> The **Review 2 literature-corpus requirement is COMPLETE**. The presentation corpus is now 50 references = 40 canonical primary studies + 10 supporting/background references. Do not alter this corpus unless a concrete bibliographic error is discovered.
>
> The canonical primary evidence baseline remains exactly **40 studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals**.
>
> Read first:
> 1. project/CHAT_HANDOFF.md
> 2. README.md
> 3. project/MASTER_EXECUTION_PLAN.md
> 4. research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md
> 5. research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md
> 6. research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md
> 7. review2/REVIEW2_50_PAPER_LITERATURE_TABLE.md
>
> Resume CHAT 07 only. Run the required environment preflight on Ubuntu 24.04 LTS x86-64 with the pinned 6.8-series kernel and required Docker/libbpf/bpftool/Clang-BPF toolchain. Complete native telemetry, ring-buffer accounting, container identity, Python tests, smoke test and reproducibility validation. Attempt kernel-local fixed-point Logistic Regression only after those prerequisites pass. If the kernel-local gate fails, record the exact verifier/load evidence and retain the user-space/hybrid fallback.
>
> Do not run the final experiment matrix and do not make scientific performance, superiority or novelty claims in CHAT 07.
