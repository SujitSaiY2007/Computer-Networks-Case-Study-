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

**Current stage:** Review 2 preparation → CHAT 03 Quality Assessment

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
- Quality assessment: **NOT FINAL**
- Evidence taxonomy: **PROVISIONAL**
- Research-gap agenda: **PROVISIONAL / DEVELOPED**
- Experimental architecture: **PROPOSED, NOT FROZEN**
- Prototype: **NOT STARTED**
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

> **CHAT 02 — EVIDENCE EXTRACTION MATRIX — CORPUS GATE**
>
> Continue the BACSE203 Computer Networks Case Study from the latest committed GitHub state.
>
> The frozen primary baseline remains exactly **40 studies: 36 journal articles + 4 peer-reviewed conference papers = 90% journals**. Do not restart selection, substitute studies, or change the baseline.
>
> Before extracting any evidence, re-check the private/local corpus and legitimate institutional/library access using `research/PAPER_ACQUISITION_AND_ARCHIVE.md) as the authoritative access map.
>
> Current verification result from 5 October 2026:
> - No P001–P040 study PDFs are present in the mounted local workspace.
> - The connected Library search did not surface the retained study PDFs.
> - 26 studies have legitimate full-text routes recorded, but those routes do not establish local corpus materialization.
> - 14 studies still require legitimate institutional/library access: P002, P009, P014, P015, P019, P020, P021, P024, P026, P027, P031, P034, P035, P037.
> - 0 studies are legitimately unavailable.
>
> Therefore **do not begin field-level extraction yet** unless the missing full texts become legitimately accessible. Do not treat unavailable evidence as “Not reported”; that label is only valid after the authoritative full text has been inspected and the field is absent.
>
> Once the full-text corpus/access is stable, extract all 40 studies using only authoritative full text. Required fields include authors, year, venue/publisher, DOI/persistent identifier, publication type, cloud/container/Kubernetes environment, eBPF hook and telemetry type, telemetry granularity, feature representation, ML algorithm, ML placement, dataset/workload, attack/threat scenario, baseline, testbed, CPU overhead, memory overhead, event rate/buffering/event loss, detection metrics, inference/detection latency, detection-to-mitigation latency, enforcement mechanism, legitimate-operation impact, reproducibility artifacts, reported limitations, external-validity concerns, and RQ1–RQ5 mapping.
>
> Do not infer numerical values from abstracts, snippets, reviews, or other papers. Keep reported results separate from cross-paper interpretation. Do not perform formal quality scoring, final cross-paper conclusions, research-gap freezing, experimental architecture design, prototype implementation, or Review 2 slide creation.
>
> If the corpus is still incomplete, update the acquisition/access status and handoff only; do not fabricate completion.
>
> If extraction becomes complete, update `project/CHAT_HANDOFF.md` and all relevant research status files and create the exact continuation prompt for **CHAT 03 — Quality Assessment**.

## Chat completion log

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
- Inference is explicitly distinguished from reported evidence and cross-paper synthesis.

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
> See the exact CHAT 05 prompt at the top of this file. It must consolidate evidence-supported gaps from CHAT 04 without prematurely implementing the architecture or prototype.
