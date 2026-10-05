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

**Current stage:** Review 2 preparation → CHAT 02A paper acquisition/archive

**Project principle:** repository state + original paper evidence + course guidelines are the durable source of truth.

---

## Current status

- Review 1: **COMPLETE**
- Review 2 candidate paper selection: **PROVISIONAL / COMPLETE FOR CANDIDATE STAGE**
- Verified primary-study baseline: **40 papers**
- Verified composition: **36 journals + 4 peer-reviewed conferences = 90% journals**
- CHAT 01 screening: **COMPLETE**
- Candidate correction: **1 survey removed; 1 verified journal primary study substituted**
- Paper acquisition/archive: **NEXT — CHAT 02A**
- Extraction matrix: **NOT FINAL**
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
