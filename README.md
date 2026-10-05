# BACSE203 Computer Networks Case Study — Canonical Source of Truth

## Topic

**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

## Review 2 project status — 5 October 2026

- **CHAT 06 COMPLETE:** experimental architecture, testbed, telemetry, feature pipeline, ML placement, distribution-shift, staged enforcement, metrics, statistics, ablations, reproducibility and risk controls are frozen in `research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md`.
- **Selected architecture:** single-host Linux + native containers + eBPF syscall/process telemetry + ring buffer + common feature pipeline + user-space Logistic Regression, with a feasibility-gated fixed-point kernel-local LR variant and staged controlled enforcement.

- Review 1 established the problem, motivation and literature directions.
- The 45-study working pool was converted into a provisional 40-paper set and has now undergone CHAT 01 verification. The current primary-study baseline is the verified 40-study set.
- The Review 2 candidate target is **36 journal articles + 4 peer-reviewed conference papers = 90% journal references**.
- Preprints are not counted in the primary 40 unless their peer-reviewed publication status is later verified.
- Existing review papers are retained as background/comparison literature and are not counted as primary studies.
- CHAT 01, CHAT 02A, CHAT 02, CHAT 03, CHAT 04, CHAT 05 and CHAT 06 are COMPLETE. The canonical CHAT 06 architecture is in research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md. CHAT 07 prototype implementation / experimental infrastructure is next.

## 🚦 Multi-chat execution system

This project is now being executed through a **controlled multi-chat workflow** so that each future chat has complete context, performs one defined phase, and hands the project cleanly to the next chat.

### Start here for every new project chat

1. Read [`project/CHAT_HANDOFF.md`](project/CHAT_HANDOFF.md) first.
2. Read [`project/MASTER_EXECUTION_PLAN.md`](project/MASTER_EXECUTION_PLAN.md).
3. Read the canonical project/research files named by the active continuation prompt.
4. Execute the **Active Continuation Prompt** only; do not restart completed phases.
5. Before ending, update `project/CHAT_HANDOFF.md` with the completed work and replace its active continuation prompt with the next unfinished task.
6. Commit the updated handoff and relevant artifacts to GitHub.

### Current next chat

**CHAT 07 — Prototype Implementation / Experimental Infrastructure**

The live prompt is stored in `project/CHAT_HANDOFF.md`..

### Planned phase sequence

**01 Verification [COMPLETE] → 02A Acquisition [COMPLETE as access register] → 02 Extraction [COMPLETE] → 03 Quality Assessment [COMPLETE] → 04 Critical Synthesis/Taxonomy [COMPLETE] → 05 Evidence-Based Gaps [COMPLETE] → 06 Experimental Architecture [COMPLETE] → 07 Prototype / Experimental Infrastructure [NEXT] → 08 Experiments → 09 Results Analysis → 10 Review 2 PPT → 11 Manuscript → 12 Final Audit**

**Important:** Chat 02A is a mandatory checkpoint. We verify the retained studies first, then obtain/record legitimate full-text access, then perform detailed evidence extraction.

The handoff file is the live checkpoint; the master execution plan is the durable roadmap.

## Core research questions

1. What architectural patterns couple eBPF telemetry hooks with ML inference?
2. How is telemetry granularity traded against CPU, memory, buffering/event-loss, and scalability overhead?
3. Which ML methods are used, and how do they behave under container churn, concept drift, and adversarial evasion?
4. What kernel-level enforcement mechanisms exist, and what is the detection-to-mitigation latency?
5. How reproducible are datasets, testbeds, attack scenarios, metrics, and reported performance gains?

## Review design

**Systematic mapping study / scoping-style evidence map with critical technical synthesis.** The review is designed to classify the literature, compare evaluation practices and evidence, assess research quality, identify supported gaps and produce a defensible future research agenda.

## Evidence policy

The course guidance requires a transparent search, screening, quality assessment, extraction matrix, and critical synthesis rather than a sequence of paper summaries. It also requires Scopus or Web of Science, IEEE Xplore, and ACM Digital Library as the minimum databases, with specialist sources such as USENIX, SpringerLink, ScienceDirect and relevant repositories added as appropriate.

**Important:** a paper is not included merely because it contains the word eBPF. Direct relevance is judged against the technology + runtime-security problem + cloud/container environment + evidence requirements. Existing surveys/reviews are used for discovery and comparison, not automatically counted as primary studies.

## Review 2 working files

- `project/MASTER_EXECUTION_PLAN.md` — complete multi-chat execution roadmap, phase dependencies, deliverables and continuation prompts.
- `project/CHAT_HANDOFF.md` — live cross-chat checkpoint; always read this first and update it before ending a project chat.
- `project/PROJECT_SCOPE_AND_RQS.md` — frozen topic boundary, RQs, contribution logic.
- `research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md` — selected 40-paper candidate primary evidence set, 90% journal ratio, per-paper methodology/merits/demerits/field and quality-assessment framework.
- `research/PAPER_ACQUISITION_AND_ARCHIVE.md` — mandatory full-text acquisition, legitimate-access and private/local PDF archive protocol.
- `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md` — evidence-based gaps, existing technologies, proposed solution direction and evaluation framework.
- `review2/REVIEW_2_SLIDE_PLAN.md` — Review 2 presentation plan aligned with the course manuscript guidelines and Review 1.

## Repository structure

- `project/PROJECT_SCOPE_AND_RQS.md` — frozen topic boundary, RQs, contribution logic.
- `project/MASTER_EXECUTION_PLAN.md` — master execution roadmap and all chat-specific continuation prompts.
- `project/CHAT_HANDOFF.md` — live state, decisions, unresolved issues and the next exact prompt.
- `research/RESEARCH_EVIDENCE_MATRIX.md` — study-set/provenance control matrix.
- `research/CHAT02_EVIDENCE_EXTRACTION.md` — canonical CHAT 02 field-level extraction for all 40 active studies.
- `research/RELEVANCY_AUDIT.md` — audit of the initial 18-paper list and screening decisions.
- `research/SEARCH_LOG.md` — search sources, query families, and verification status.
- `research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md` — Review 2 candidate paper set and verification framework.
- `research/PAPER_ACQUISITION_AND_ARCHIVE.md` — paper download/access/archive workflow and register requirements.
- `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md` — evidence-based gaps and future agenda.
- `review1/REVIEW_1_SLIDE_PLAN.md` — Review 1 presentation structure and selected papers.
- `review1/Review_1_eBPF_Runtime_Security.pptx` — Review 1 presentation artifact.
- `review2/REVIEW_2_SLIDE_PLAN.md` — Review 2 presentation structure.

## Intended synthesis framework

The review will synthesize evidence across:

**Telemetry extraction → feature representation → ML placement → detection decision → kernel enforcement**

and compare studies using:

**detection quality ↔ latency ↔ CPU/memory/event-processing overhead ↔ safety ↔ reproducibility.**

## Paper PDF policy

Full-text PDFs are treated as research working materials. The public repository stores metadata, DOI/official links, acquisition status and verification notes—not unauthorized copyrighted publisher PDFs. Legitimately obtainable PDFs should be retained in the user's private/local research archive and linked to the study IDs used in the evidence matrix.

## Canonical-source rule

If later chats produce a conflicting paper count, relevance decision, scope statement, or project structure, **the latest committed repository state and especially `project/CHAT_HANDOFF.md` are the reference point**. New papers must be added through the same extraction fields and must not silently replace earlier records.

## Quality warning

Several papers in the initial user-provided list contain incomplete or garbled numeric fields. Those values are not reconstructed by guesswork. Publisher/DOI metadata is preferred where verified; otherwise the record remains marked for full-text verification.

## Workflow principle

The objective is not to create a long chain of disconnected chats. It is to create **one continuous research process with versioned checkpoints**. Each chat owns one phase; each phase leaves behind evidence, files, decisions and a customized continuation prompt for the next phase. This makes the GitHub repository the project's durable memory and prevents context loss between chats.


## Review 2 project status — 5 October 2026

- Review 1 established the problem, motivation and literature directions.
- CHAT 01 full-text verification/screening is **COMPLETE**.
- The verified primary-study baseline is **40 studies: 36 journal articles + 4 peer-reviewed conference papers = 90% journals**.
- One originally listed review article, *Extended Berkeley Packet Filter: An Application Perspective*, was removed from the primary set and retained as background/comparison literature.
- It was replaced by the verified 2026 IEEE Transactions on Cloud Computing primary study *Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks* (DOI: 10.1109/TCC.2026.3657486).
- CHAT 01 also corrected stale DOI/title metadata where authoritative records differed from the earlier working list.
- The 40-study primary baseline is now the starting point for paper acquisition; detailed extraction and formal quality assessment remain downstream.

### Current next chat

**CHAT 02A — Paper Acquisition & Archive**

The live prompt is stored in project/CHAT_HANDOFF.md. The mandatory acquisition protocol is stored in research/PAPER_ACQUISITION_AND_ARCHIVE.md.

### Current phase sequence

**01 Verification [COMPLETE] → 02A Paper Acquisition & Archive [NEXT] → 02 Extraction → 03 Quality Assessment → 04 Critical Synthesis/Taxonomy → 05 Evidence-Based Gaps → 06 Experimental Architecture → 07 Testbed/Instrumentation → 08 Prototype → 09 Experiments → 10 Results Analysis → 11 Review 2 PPT → 12 Manuscript → 13 Final Audit**

CHAT 02A must not restart paper selection or begin detailed extraction. Its purpose is to establish a legitimate, auditable full-text corpus and access register for the already verified 40-study baseline.


---

## CHAT 02A status — 5 October 2026

CHAT 02A paper acquisition/archive is **PARTIAL/BLOCKED**.

- Frozen primary baseline: **40 studies**
- Composition: **36 journals + 4 peer-reviewed conferences = 90% journals**
- Legitimate full-text copies/routes located: **26**
- Institutional/library access required: **14**
- Legitimately unavailable: **0**
- New DOI/title mismatches requiring correction: **0**
- Unauthorized PDFs committed: **0**
- Local/private PDF corpus: **not yet materialized**

The complete row-level access register is in research/PAPER_ACQUISITION_AND_ARCHIVE.md. CHAT 02 evidence extraction must begin only after the local/private corpus is stable or legitimate institutional/library access has been obtained for the remaining records.

**Important:** “OBTAINED” in the register means a legitimate full-text copy was located/accessed; it does not claim that a local PDF file was successfully materialized in the current execution environment.


## Live status override — 5 October 2026

**Current phase:** CHAT 02 — Evidence Extraction Matrix, **BLOCKED at the full-text corpus gate**.

The 40-study baseline remains frozen at **36 journals + 4 peer-reviewed conferences = 90% journals**. A direct check of the connected Library and mounted local workspace found **no retained P001–P040 study PDFs**. The acquisition register still records 26 legitimate full-text routes and 14 institutional/library-access requirements, but those routes do not establish local corpus availability. Evidence extraction therefore has **not** begun and no inaccessible field is being labelled “Not reported.”

The next action is to materialize the private/local corpus legitimately or provide legitimate institutional/library access for the unresolved studies, then resume CHAT 02.

## CHAT 02 completion — 5 October 2026

CHAT 02 Evidence Extraction is COMPLETE. The canonical field-level matrix is research/CHAT02_EVIDENCE_EXTRACTION.md. Missing fields are explicitly marked NR/NA rather than inferred. The next phase is CHAT 03 — Quality Assessment.


## CHAT 03 completion checkpoint — 5 October 2026

**CHAT 03 — COMPLETE.** Formal qualitative quality assessment was completed for all 40 retained primary studies in `research/CHAT03_QUALITY_ASSESSMENT.md`. No numerical quality score was assigned and the baseline was not changed.

## CHAT 04 completion checkpoint — 5 October 2026

**CHAT 04 — COMPLETE.** The evidence-grounded critical synthesis and technology taxonomy are recorded in `research/CHAT04_CRITICAL_SYNTHESIS.md`. The frozen baseline remains **40 studies: 36 journals + 4 peer-reviewed conferences = 90% journals**. No study was added, removed or replaced. Preliminary gap observations remain explicitly non-final. The next phase is **CHAT 05 — Research Gap Consolidation / Evidence-to-Design Bridge**.

## CHAT 05 completion checkpoint — 5 October 2026

**CHAT 05 — COMPLETE.** The authoritative gap framework is in `research/CHAT05_RESEARCH_GAP_CONSOLIDATION.md` and `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`. Five validated gaps were retained: end-to-end latency/telemetry completeness, distribution-shift robustness, common-protocol ML placement comparison, safe enforcement evaluation, and reproducible environment/artifact specification. The frozen baseline remains **40 primary studies: 36 journals + 4 peer-reviewed conferences**. Next phase: **CHAT 06 — Experimental Architecture + Testbed Specification**.## CHAT 07 implementation checkpoint — 5 October 2026

**CHAT 07 is INCOMPLETE / BLOCKED, not COMPLETE.** The minimum prototype structure has been created under `prototype/`, including BPF telemetry source/loader, ring-buffer accounting, deterministic feature aggregation, user-space Logistic Regression, staged policy logic, reproducibility capture, tests and CI configuration.

Native BPF/container validation is blocked in the current execution environment because it lacks `bpftool`, Docker, libbpf development headers and a Clang installation with the BPF target. The exact evidence and remaining gates are recorded in `research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md`.

No final experiment, performance result, superiority claim, novelty claim, or kernel-local ML result is claimed.


