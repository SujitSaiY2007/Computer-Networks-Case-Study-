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

**Current stage:** Review 2 preparation → full-text verification/screening

**Project principle:** repository state + original paper evidence + course guidelines are the durable source of truth.

---

## Current status

- Review 1: **COMPLETE**
- Review 2 candidate paper selection: **PROVISIONAL / COMPLETE FOR CANDIDATE STAGE**
- Candidate primary-study set: **40 papers**
- Candidate composition: **36 journals + 4 peer-reviewed conferences = 90% journals**
- Full-text verification: **NEXT**
- Paper acquisition/archive: **PLANNED IMMEDIATELY AFTER VERIFICATION**
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

> **CHAT 01 — Full-Text Verification and Final Candidate Screening**
>
> Continue the BACSE203 project from the current repository state. First read `project/CHAT_HANDOFF.md`, `project/MASTER_EXECUTION_PLAN.md`, `project/PROJECT_SCOPE_AND_RQS.md`, `research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md`, `research/RESEARCH_EVIDENCE_MATRIX.md`, `research/RELEVANCY_AUDIT.md`, and `research/SEARCH_LOG.md`. Do not restart Review 1 or invent a new paper list.
>
> Verify the 40 candidate papers against original publisher/DOI/academic records and full text where available. For every candidate, verify title, authors, year, venue, publisher, DOI, publication type, date-window eligibility, peer-review status, direct relevance to the project RQs, and actual technical evidence. Classify retained studies as core or supporting; classify reviews as background/comparison rather than primary evidence. Record an explicit exclusion reason for every excluded candidate. Do not reconstruct missing values by guesswork. Recalculate the final retained journal/conference ratio after screening.
>
> The goal is a defensible, auditable primary-study baseline for the paper-acquisition phase and subsequent extraction matrix. Do not move into implementation or final manuscript drafting in this chat.
>
> Before ending the chat, update `project/CHAT_HANDOFF.md` with: status, completed work, changed files, decisions frozen, unresolved issues, deviations from plan, the final retained-study count, and the exact continuation prompt for **CHAT 02A — Paper Acquisition & Archive**. Commit the updated handoff and related research files to GitHub.

---

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
