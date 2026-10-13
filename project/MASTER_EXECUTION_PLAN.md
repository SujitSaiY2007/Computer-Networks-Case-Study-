# Master Execution Plan — Multi-Chat Project Workflow

## Purpose

This file is the **master roadmap** for executing the BACSE203 literature-review case study across multiple future chats without losing context, repeating completed work, or silently changing project decisions.

Project:

**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

Review 1 and Review 2 (Chat 12) are COMPLETE. Chats 01–07 are COMPLETE, including Chat 07 native prototype validation. CHAT 08 — Controlled Experiments Execution is NEXT. The current status, Chat 07 caveats, and corrected remaining phase sequence are authoritative in `project/STATUS_CORRECTION_2026-10-13.md`; older phase prompts below are retained as historical planning material and must not override the live handoff.

---

## Live status override — 13 October 2026

For current phase/status, follow `project/STATUS_CORRECTION_2026-10-13.md` and `project/CHAT_HANDOFF.md`. Review 2 is already complete; do not run it again as a future phase. Chat 07 is complete; Chat 08 controlled experiments is next. Historical continuation prompts below document the original plan and must be treated as historical where they conflict with the live status correction.

Frozen counts: 40 primary studies (36 journals + 4 peer-reviewed conference papers) and 50 Review 2 references (40 primary + 10 supporting/background). These counts are distinct and must not be conflated.

## 1. Non-Negotiable Context Rule

Every future project chat must begin by treating the following repository files as the canonical project context:

1. `project/PROJECT_SCOPE_AND_RQS.md`
2. `project/MASTER_EXECUTION_PLAN.md` — this file
3. `project/CHAT_HANDOFF.md` — current state and the exact continuation prompt
4. `research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md`
5. `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`
6. `research/RESEARCH_EVIDENCE_MATRIX.md`
7. `research/RELEVANCY_AUDIT.md`
8. `research/SEARCH_LOG.md`
9. `review2/REVIEW_2_SLIDE_PLAN.md`
10. `review1/REVIEW_1_SLIDE_PLAN.md` when continuity with Review 1 is needed.

The assistant must **read the relevant repository files before making project-level decisions**. The assistant must not rely on an unstated memory of an earlier chat when the repository contains the relevant decision.

### Source hierarchy

When information conflicts:

1. Original publisher/DOI/full text for paper-level facts.
2. Course guideline document for assignment requirements.
3. Latest committed repository state for project decisions, scope, counts, selections and workflow.
4. Prior chat memory only when the information has not yet been committed and is explicitly recorded in the current handoff.
5. General model knowledge only when clearly labelled as background/inference and not presented as evidence from the project literature.

---

## 2. Current Baseline

- Review 1 is complete and the overall research idea has been accepted positively by the supervisor.
- The working evidence pool has been refined to a **40-paper candidate primary-study set**.
- Target composition: **36 journal articles + 4 peer-reviewed conference papers = 90% journals**.
- The 40-study primary set is the **verified screening baseline**. CHAT 01 verification, CHAT 02 extraction, CHAT 03 quality assessment, CHAT 04 synthesis and CHAT 05 gap consolidation are complete.
- Existing review papers are background/comparison literature, not primary studies.
- A 2026 eBPF cybersecurity systematic literature review exists; therefore this project must not claim to be the first review of eBPF cybersecurity. Its narrower contribution is the intersection of **eBPF telemetry + ML runtime detection + kernel enforcement in cloud/container environments**, with explicit attention to overhead, ML placement, detection-to-mitigation latency, enforcement safety and evaluation practice.
- Final manuscript should be a **critical synthesis**, not 40 independent paper summaries.

---

## 3. Execution Architecture

The project will be executed as a sequence of focused chats. Each chat has:

- one primary objective;
- explicit inputs;
- explicit deliverables;
- repository files to read;
- repository files to create/update;
- a completion checklist;
- an exact continuation prompt for the next chat.

A chat must **not silently start the next phase** unless that is necessary to resolve a dependency. It should finish its assigned phase, update the handoff, and leave the next chat ready to continue.

### Phase dependency chain

**A. Context/control setup**
→ **B. Full-text paper verification**
→ **C. Extraction matrix**
→ **D. Quality assessment**
→ **E. Evidence synthesis + technology taxonomy**
→ **F. Evidence-based gaps + future study design**
→ **G. Experimental architecture + testbed specification**
→ **H. Prototype implementation**
→ **I. Experimental evaluation**
→ **J. Review 2 presentation**
→ **K. Final manuscript**
→ **L. Final audit/submission package**

Some phases can overlap after their inputs are frozen, but the dependency chain above is the default order.

---

# 4. Chat-by-Chat Execution Plan

## CHAT 01 — Full-Text Verification and Final Candidate Screening

### Objective
Verify the 40 candidate papers against original publisher/DOI/academic records and full text where available. Decide: include, supporting/background, or exclude.

### Read first
- `project/PROJECT_SCOPE_AND_RQS.md`
- `project/MASTER_EXECUTION_PLAN.md`
- `project/CHAT_HANDOFF.md`
- `research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md`
- `research/RESEARCH_EVIDENCE_MATRIX.md`
- `research/RELEVANCY_AUDIT.md`
- `research/SEARCH_LOG.md`

### Work
For every candidate:
- verify title, authors, year, venue, publisher and DOI;
- verify publication type and peer-review status;
- verify date-window eligibility;
- verify direct relevance to the project RQs;
- verify actual technical evidence rather than keyword relevance;
- mark core / supporting / background-review;
- record exclusion reason if excluded;
- never reconstruct missing values by guesswork.

### Deliverables
- Verified candidate list.
- Exclusion log.
- DOI/metadata verification status.
- Final primary-study count after screening.
- Explicit journal/conference ratio after screening.

### Completion gate
No paper is treated as final merely because it was in the old 40-paper list. Every retained study has a documented inclusion rationale.

### Next continuation prompt
> Continue the BACSE203 project from the completed **full-text verification and screening phase**. First read `project/CHAT_HANDOFF.md`, `project/MASTER_EXECUTION_PLAN.md`, `project/PROJECT_SCOPE_AND_RQS.md`, and the updated paper-selection/evidence files. Do not restart paper selection. Use the verified retained-study set as the only primary-study baseline. Now build/finalize the **full extraction matrix** for every retained study, covering bibliographic data, environment, eBPF hook/telemetry, feature representation, ML method and placement, dataset/workload, attack scenario, baselines, testbed, CPU/memory overhead, event loss, detection metrics, latency, enforcement, reproducibility, limitations, and RQ mapping. Verify paper-level facts from original sources and explicitly mark anything not reported.

At the end, update `project/CHAT_HANDOFF.md` with the completed extraction status, decisions, unresolved items, changed files, and the exact next continuation prompt for quality assessment. Also update the relevant repository index/status files.

---

## CHAT 02A — Paper Acquisition & Archive

### Objective
Create a stable, auditable full-text access corpus after CHAT 01 verification and before evidence extraction.

### Current result — 5 October 2026
- Verified baseline preserved: 40 studies.
- Composition preserved: 36 journals + 4 peer-reviewed conferences.
- Legitimate full-text copies/routes located: 26.
- Institutional/library access required: 14.
- Legitimately unavailable: 0.
- New metadata/PDF mismatch requiring baseline correction: 0.
- No unauthorized PDFs committed.
- Local/private PDF materialization remains incomplete because the current execution environment could not successfully materialize an openly accessible PDF.

### Deliverables
- research/PAPER_ACQUISITION_AND_ARCHIVE.md with one row for every retained study.
- Legitimate publisher/DOI/institutional/author-repository access route for each study.
- Explicit acquisition status and PDF-to-record verification state.
- Private/local archive readiness before CHAT 02.

### Completion gate
CHAT 02A is **PARTIAL/BLOCKED** until the private/local PDF corpus is materialized or legitimate institutional/library access is available for the remaining records. No paper is excluded merely because access is difficult.

### Completion status
COMPLETE. Canonical extraction: research/CHAT02_EVIDENCE_EXTRACTION.md.

### Next phase
CHAT 03 — Quality Assessment.

## CHAT 02 — Evidence Extraction Matrix

### Objective
Convert the verified primary-study set into a structured, comparable evidence matrix.

### Required extraction fields
- Study ID
- Full title
- Authors
- Year
- Journal/conference
- Publisher
- DOI
- Publication type
- Research field
- Problem addressed
- Cloud/container/Kubernetes environment
- eBPF technology/hook
- Telemetry type
- Telemetry granularity
- Feature representation
- ML algorithm
- ML placement: user space / kernel / hybrid
- Dataset/workload
- Attack/threat scenario
- Baseline
- Testbed
- CPU overhead
- Memory overhead
- Event rate/buffering/event loss
- Accuracy/precision/recall/F1/FPR or other reported detection metrics
- Inference/detection latency
- Detection-to-mitigation latency
- Enforcement mechanism
- Legitimate-operation impact
- Reproducibility information
- Reported limitations
- External-validity concerns
- RQ1–RQ5 mapping
- Harvard citation

### Rule
If a paper does not report a field, write **Not reported**, not an inferred value.

### Deliverables
- Final extraction matrix.
- List of missing/weak evidence fields.
- Evidence coverage summary by RQ.

### Next continuation prompt
> Continue from the completed extraction matrix. Read `project/CHAT_HANDOFF.md` first and use the verified matrix as the evidence base. Do not re-extract papers unless a specific inconsistency is identified. Now perform the **formal quality assessment** across all retained primary studies using the project criteria: objective clarity, technical description, dataset/workload transparency, baseline adequacy, evaluation validity, experimental detail, reproducibility, limitations, external validity, and statistical reporting. Classify each as clearly reported / partially reported / not reported and justify borderline cases from the paper. Do not invent a numerical quality score unless the methodology explicitly requires one.
>
> At the end, update `project/CHAT_HANDOFF.md` and the relevant research files with quality-assessment results, unresolved evidence issues, and the exact continuation prompt for evidence synthesis/taxonomy.

---

## CHAT 03 — Quality Assessment and Evidence Reliability

### Objective
Assess how trustworthy and comparable the retained evidence is.

### Deliverables
- Quality-assessment matrix.
- Evidence reliability summary.
- Identification of studies with weak reporting.
- Identification of metrics that are not directly comparable.
- Identification of contradictory or context-dependent findings.

### Completion gate
The review must distinguish **reported result**, **cross-paper synthesis**, **inference**, and **project interpretation**.

### Next continuation prompt
> Continue from the completed paper verification, extraction matrix and quality assessment. Read `project/CHAT_HANDOFF.md` and the latest research matrices first. Now perform the **critical evidence synthesis and taxonomy construction**. Do not write 40 mini-summaries. Instead group studies by telemetry modality, ML role/placement, enforcement mechanism, cloud-native environment, threat type, and evaluation style. Identify recurring architectural patterns, performance patterns, conflicts, and evidence limitations. Build an evidence-derived taxonomy/framework that directly answers RQ1–RQ5 and can later become a manuscript figure and Review 2 slide.
>
> Update the handoff with the taxonomy, major findings, unresolved contradictions, and the exact next continuation prompt for research gaps/future-study design.

---

## CHAT 04 — Critical Synthesis and Technology Taxonomy

### Objective
Produce the literature-derived structure that explains what technologies exist and how they relate.

### Core taxonomy dimensions
1. Telemetry source/hook.
2. Telemetry granularity.
3. Feature representation.
4. ML model family.
5. ML placement.
6. Detection target.
7. Enforcement point.
8. Feedback/control loop.
9. Evaluation metrics.
10. Reproducibility level.

### Deliverables
- Evidence-derived taxonomy.
- Comparative synthesis table.
- Findings by RQ.
- Conflicting/conditional findings.
- Candidate manuscript figure.

### Next continuation prompt
> Continue from the completed evidence taxonomy and critical synthesis. Read `project/CHAT_HANDOFF.md`, `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`, and the latest evidence/quality files. Now turn the observed limitations into **evidence-based research gaps**. For every gap use the required structure: (1) evidence-based gap, (2) why it matters, (3) recommended future study, (4) measurable evaluation criteria. Explicitly identify existing technologies and explain what each does and what remains unresolved. Avoid generic statements such as “more research is needed.” Finish by defining the smallest defensible research contribution this project can make without claiming novelty that the literature does not support.
>
> Update the handoff and research-gap file with the finalized gap-to-study mapping and the exact continuation prompt for experimental architecture.

---

## CHAT 05 — Research Gaps and Future-Study Design

### Objective
Translate evidence gaps into a defensible future research direction.

### Required gap dimensions
- telemetry fragmentation;
- dataset/attack specificity and distribution shift;
- in-kernel vs user-space ML placement;
- lack of standardized overhead/latency benchmarking;
- detection vs safe autonomous enforcement;
- adversarial robustness;
- eBPF verifier/meta-security constraints;
- portability;
- reproducibility;
- integrated safety/efficiency/reliability evaluation.

### Deliverables
- Evidence-based gap table.
- Existing-technology comparison.
- Recommended future-study questions.
- Explicit project contribution boundary.

### Next continuation prompt
> Continue from the finalized evidence-based gaps and proposed contribution. Read `project/CHAT_HANDOFF.md`, `project/PROJECT_SCOPE_AND_RQS.md`, and `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md`. Now design the **experimental architecture and testbed specification** that directly addresses the highest-value supported gap. Compare at least: baseline, eBPF-only, eBPF+user-space ML, eBPF+lightweight in-kernel ML, and eBPF+ML+enforcement. Specify telemetry hooks, feature pipeline, model placement, policy/risk decision, enforcement mechanism, workloads, attack scenarios, controls, metrics, ablations, safety conditions, and reproducibility requirements. Keep the design feasible for a student project and avoid adding components that are not needed to answer the RQs.
>
> Update the handoff with the frozen architecture, experiment matrix, dependencies, and the exact continuation prompt for testbed/dataset preparation.

---

## CHAT 06 — Experimental Architecture and Evaluation Protocol

### Objective
Freeze a technically feasible experiment that tests the literature-derived trade-offs.

### Recommended architecture
**Kubernetes/container workloads → eBPF telemetry → feature extraction → ML detection → policy/risk score → kernel enforcement → mitigation**

### Recommended configurations
1. Baseline/no eBPF ML.
2. eBPF telemetry only.
3. eBPF + user-space ML.
4. eBPF + lightweight in-kernel ML.
5. eBPF + ML + enforcement.

### Core metrics
- precision, recall, F1, FPR;
- CPU and memory;
- events/sec;
- dropped events/buffer pressure;
- inference latency;
- detection latency;
- detection-to-mitigation latency;
- legitimate-operation blocking;
- reproducibility.

### Deliverables
- Architecture diagram specification.
- Experiment matrix.
- Testbed specification.
- Threat model.
- Metrics and statistical plan.
- Ablation plan.

### Next continuation prompt
> Continue from the frozen experimental architecture and evaluation protocol. Read `project/CHAT_HANDOFF.md` first. Now prepare the **dataset, workload, attack-scenario and instrumentation plan**. Choose or construct scenarios that test the project RQs without creating an unmanageable testbed. Define benign workloads, malicious behaviors, ground truth, train/test split, distribution-shift test if feasible, telemetry collection, timestamps, resource measurement, event-loss measurement, and reproducible experiment scripts/configuration. Do not begin coding the whole system yet; first make the experiment reproducible on paper.
>
> Update the handoff with the finalized testbed plan, chosen scenarios, required software/tools, and the exact continuation prompt for prototype implementation.

---

## CHAT 07 — Dataset, Workload, Attack and Instrumentation Plan

### Objective
Make the experiment reproducible before implementation.

### Deliverables
- Dataset/workload definition.
- Attack scenario matrix.
- Ground-truth strategy.
- Instrumentation specification.
- Measurement procedure.
- Reproducibility checklist.

### Status
**COMPLETE** — Native Linux prototype implementation and validation gates (A–G) verified with empirical evidence in `research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md`.

### Next continuation prompt
> Continue from the fully validated prototype and experimental infrastructure. Read `project/CHAT_HANDOFF.md` and `research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md`. Now execute the **controlled experiments** for all frozen configurations (Options A–E). Run sufficient repetitions (10 runs) across baseline workloads (B1–B4) and anomaly workloads (A1–A3), preserve raw results, record environment/software versions, and do not selectively report only favorable outcomes. Measure detection quality, CPU/memory, event processing/loss, detection/inference latency, detection-to-mitigation latency, and legitimate-workload impact. Save raw and processed results under `experiments/`.
>
> Update the handoff with experiment completion status, raw-result locations, anomalies, failed runs, and the exact continuation prompt for analysis.

---

## CHAT 08 — Controlled Experiments Execution

### Objective
Execute the frozen experiment matrix and collect empirical measurements across all configurations.

### Deliverables
- 10-repetition experiment runs across Configurations A–E.
- Baseline (B1–B4) and anomaly (A1–A3) evaluation datasets.
- System metrics (CPU, memory, throughput, event loss).
- Security metrics (precision, recall, F1, FPR).
- Latency metrics (inference latency, detection-to-mitigation latency).
- Raw data preservation and run reproducibility records.

---

## CHAT 09 — Experimental Evaluation

### Objective
Run the agreed experiments and preserve auditable results.

### Deliverables
- Raw result files.
- Processed metrics.
- Run metadata.
- Failed-run/anomaly log.
- Reproducibility record.

### Next continuation prompt
> Continue from the completed experiment runs and raw results. Read `project/CHAT_HANDOFF.md` first and inspect the raw data before drawing conclusions. Now perform the **statistical and comparative analysis**. Compare configurations fairly, quantify trade-offs, report uncertainty where appropriate, identify performance/detection conflicts, and distinguish observed results from interpretation. Produce publication-quality evidence tables and figures for the manuscript and Review 2. Do not claim general superiority unless the data supports it.
>
> Update the handoff with finalized findings, limitations, figure/table inventory, and the exact continuation prompt for Review 2 presentation preparation.

---

## CHAT 10 — Results Analysis and Evidence Figures

### Objective
Turn experimental outputs into defensible findings.

### Deliverables
- Comparative results tables.
- Detection-quality analysis.
- Overhead analysis.
- Latency analysis.
- Enforcement/safety analysis.
- Statistical/uncertainty treatment.
- Figures.
- Final findings linked back to RQs and literature gaps.

### Next continuation prompt
> Continue from the finalized literature synthesis and experimental findings. Read `project/CHAT_HANDOFF.md`, `review2/REVIEW_2_SLIDE_PLAN.md`, and the latest research files. Now create the **Review 2 presentation**. Preserve continuity with Review 1, but make Review 2 evidence-focused: verified paper set, methodology/quality, technology taxonomy, evidence-based gaps, proposed/frozen research direction, and evaluation framework/results as appropriate. Do not turn Review 2 into an implementation demo. Every important claim should be traceable to a paper, dataset/result, or explicitly labelled project inference.
>
> Update the handoff with the completed presentation status, files, feedback issues, and the exact continuation prompt for manuscript drafting.

---

## CHAT 11 — Review 2 Presentation

### Objective
Produce the supervisor-facing Review 2 presentation.

### Required story
Review 1 problem → Review 2 evidence verification → quality/structure → technology landscape → what literature shows → evidence-based gaps → project contribution → evaluation framework/results → next milestone.

### Deliverables
- Final Review 2 PPT.
- Speaker notes if needed.
- Slide-to-evidence mapping.
- Compliance checklist against course guidelines.

### Next continuation prompt
> Continue from the completed Review 2 presentation and all frozen evidence/experimental results. Read `project/CHAT_HANDOFF.md` and the latest canonical files. Now draft the **literature-review manuscript** according to the course guidelines. Build a critical synthesis rather than paper-by-paper summaries. Include transparent review design, search/screening method, evidence base, taxonomy, comparative evidence tables, evaluation-metric limitations, evidence-based gaps, future research agenda, and the project contribution. Use Harvard author-date citation style consistently and verify references against original publisher/DOI records. Clearly distinguish primary studies from review/background papers.
>
> Update the handoff with manuscript sections completed, unresolved citation/evidence issues, and the exact continuation prompt for final audit.

---

## CHAT 12 — Manuscript Drafting

### Objective
Produce the complete literature-review manuscript using the verified evidence and project results.

### Required manuscript qualities
- critical and transparent;
- evidence-based;
- reproducible review method;
- primary-study majority;
- original evidence tables/figures;
- explicit limitations;
- evidence-linked research gaps;
- no unsupported novelty claims.

### Deliverables
- Full manuscript draft.
- References.
- Tables.
- Figures.
- Search/screening appendix as required.

### Next continuation prompt
> Continue from the completed manuscript draft. Read `project/CHAT_HANDOFF.md` and the course-guideline-derived project files. Now perform the **final submission audit**. Check every citation/reference, DOI, paper count, journal ratio, inclusion/exclusion consistency, RQ coverage, table/figure support, claims versus evidence, methodology transparency, Harvard formatting, plagiarism/copyright risks, reproducibility statements, and consistency between Review 1, Review 2, manuscript and repository. Identify and fix only evidence-supported issues; do not silently invent missing information. Produce a final submission checklist and archive the final project state in the repository.
>
> Update the handoff with final status, remaining risks, exact final files, and a concise post-project maintenance note.

---

## CHAT 13 — Final Audit and Submission Package

### Objective
Perform the final consistency and compliance audit before submission.

### Deliverables
- Final manuscript.
- Final Review 2 PPT.
- Final evidence matrix.
- Final gap/future-agenda table.
- Final search/screening/quality records.
- Final reproducibility package.
- Submission checklist.

### Completion condition
The project is considered complete only when the repository contains enough evidence to reconstruct why each primary study was included, what it contributed, what its limitations were, how the synthesis produced the gaps, and how the proposed/implemented experiment addresses those gaps.

---

# 5. Rules for Every Future Chat

## Rule A — Start from the handoff
The first action in every project chat is to read `project/CHAT_HANDOFF.md` and the files named in its active continuation prompt.

## Rule B — Never restart completed work
If a phase is marked COMPLETE in the handoff, do not redo it from scratch. Audit only when the current task exposes a concrete inconsistency.

## Rule C — Repository is the memory
Important decisions must be committed to the repository. A decision mentioned only in chat is considered provisional until recorded in the handoff or a canonical project file.

## Rule D — Update the handoff before ending
Every project chat must update `project/CHAT_HANDOFF.md` before concluding. It must record:

- phase/chat number;
- status: COMPLETE / BLOCKED / PARTIAL;
- work completed;
- files changed;
- decisions frozen;
- evidence gaps/unresolved issues;
- deviations from plan;
- exact next continuation prompt.

## Rule E — Update the continuation prompt after completion
The **active continuation prompt** in `project/CHAT_HANDOFF.md` must always point to the next unfinished task. Once the current task is complete, replace the current prompt with the next prompt from this master plan and customize it with any newly discovered constraints.

## Rule F — Do not overclaim
Use language such as “the evidence indicates,” “the evaluated studies report,” or “our experiment observed” where appropriate. Do not convert one paper's result into a universal claim.

## Rule G — Preserve provenance
For every important evidence statement, maintain enough information to trace it to the original paper, dataset/result, or project experiment.

## Rule H — Primary studies vs reviews
Review papers help discover and compare literature but are not automatically counted as primary evidence.

## Rule I — Missing data means missing data
Use **Not reported** rather than estimating a metric from graphs, abstracts, snippets or unrelated papers unless the methodology explicitly permits such extraction and the method is documented.

## Rule J — Scope discipline
The project is about the intersection of eBPF telemetry, ML-based runtime security/detection and kernel-level enforcement in cloud/container environments. Supporting technologies may be included when they illuminate a specific RQ or trade-off, but they must be labelled as supporting evidence rather than presented as direct evidence.

---

# 6. Definition of Done for the Whole Project

The project is ready for final submission when:

- the primary-study set is fully verified;
- inclusion/exclusion reasons are auditable;
- journal/conference ratio satisfies the course requirement;
- every retained study has a complete extraction record or explicit “Not reported” fields;
- quality assessment is complete;
- the taxonomy is derived from evidence;
- research gaps follow the Evidence → Why it matters → Future study structure;
- existing technologies are identified and compared;
- the proposed solution is justified by the gaps rather than by unsupported novelty;
- the experimental design maps to the RQs;
- experiments preserve raw/auditable results;
- results are analyzed fairly;
- Review 2 and manuscript tell the same evidence-based story;
- Harvard citations/references and DOI metadata are verified;
- course guideline compliance is checked;
- the repository contains the final artifacts and enough records to reconstruct the project decisions.

---

# 7. Current Next Action

**Next chat: CHAT 02A — Paper Acquisition & Archive.**

The project should not move to detailed extraction until CHAT 02A establishes the legitimate full-text acquisition/access register for the verified 40-study baseline.


## CHAT 01 completion update — 5 October 2026

CHAT 01 is **COMPLETE**. The original provisional 40-paper list was screened against authoritative bibliographic records and available full-text/abstract evidence.

### Frozen result entering CHAT 02A

- **40 primary studies retained**
- **36 journal articles**
- **4 peer-reviewed conference papers**
- **90.0% journals**
- **14 Core**
- **26 Supporting/Adjacent**
- **0 preprint-only primary studies**
- **0 duplicates removed**
- **0 retraction flags in the scholarly identifier audit**

### Material correction

The provisional candidate **Extended Berkeley Packet Filter: An Application Perspective** was removed from the primary evidence set because it is a review article. It remains useful as background/comparison literature.

It was replaced by **Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks**, IEEE Transactions on Cloud Computing (2026), DOI 10.1109/TCC.2026.3657486, which is a primary journal study directly relevant to eBPF telemetry, ML anomaly detection/online learning, container isolation and cloud-native runtime security.

The detailed screening record is research/CHAT01_FULLTEXT_VERIFICATION.md.

### Current phase

**CHAT 02A — Paper Acquisition & Archive**

Do not restart CHAT 01. Do not begin detailed extraction yet. Follow research/PAPER_ACQUISITION_AND_ARCHIVE.md and the active prompt in project/CHAT_HANDOFF.md.


# Live execution checkpoint — 5 October 2026

**CHAT 02 status: BLOCKED AT CORPUS GATE.**

The frozen primary baseline remains 40 studies: 36 journals + 4 peer-reviewed conferences (90% journals). A direct local/library verification found no retained P001–P040 PDFs in the mounted workspace or connected Library. The acquisition register's 26 “OBTAINED” entries represent legitimate full-text routes, not proof of local materialization. Fourteen records still require legitimate institutional/library access.

**CHAT 02 rule:** do not infer or mark fields “Not reported” for inaccessible papers. Resume field-level extraction only after the authoritative full text is legitimately available. If extraction completes, the next phase is CHAT 03 — Quality Assessment.

## Current checkpoint — 5 October 2026

CHAT 02 COMPLETE. All 40 active studies have a canonical extraction record. The next phase is CHAT 03 quality assessment; it must use qualitative reporting categories and must not introduce a numerical quality score or alter the frozen baseline without evidence.


## CHAT 03 completion checkpoint — 5 October 2026

**Status: COMPLETE.** The formal qualitative quality assessment of all 40 retained studies is recorded in `research/CHAT03_QUALITY_ASSESSMENT.md`. No numerical score was assigned and the 40-study baseline was not changed. Next phase: **CHAT 04 — Critical Synthesis / Technology Taxonomy**.


## CHAT 04 completion checkpoint — 5 October 2026

**Status: COMPLETE.** CHAT 04 translated the completed CHAT 02 extraction and CHAT 03 quality assessment into a cross-paper technology taxonomy and critical synthesis. The frozen 40-study baseline remains unchanged. The artifact is `research/CHAT04_CRITICAL_SYNTHESIS.md`. It distinguishes reported evidence, cross-paper synthesis and inference; separates Core from Supporting/Adjacent evidence; documents convergence/divergence/trade-offs; and labels candidate gap observations as preliminary rather than final.

### Next phase
**CHAT 05 — Research Gap Consolidation / Evidence-to-Design Bridge**

CHAT 05 must consolidate only evidence-supported research gaps and map them to RQs and design requirements. It must not add studies, alter the baseline, or implement the experimental architecture/prototype.

## CHAT 05 completion checkpoint — 5 October 2026

**Status: COMPLETE.** CHAT 05 validated the CHAT 04 candidates and produced five evidence-supported gaps. The central problem is an evaluation/integration limitation rather than absence of component technologies. Candidate A/C were merged; overclaims about missing continual learning, multimodal telemetry, universal placement superiority, absent enforcement and eBPF insecurity were rejected/downgraded.

Canonical artifact: `research/CHAT05_RESEARCH_GAP_CONSOLIDATION.md`.

**Next phase:** CHAT 06 — Experimental Architecture + Testbed Specification. CHAT 06 must translate G1–G5 into a feasible architecture, experiment matrix, workloads, metrics, safety controls and reproducibility plan without changing the RQs or 40-study baseline.


---

## CHAT 06 completion addendum — 5 October 2026

**Status: COMPLETE**

CHAT 06 froze the experimental architecture and testbed specification in `research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md`.

### Frozen architecture
Single-host Ubuntu 24.04 LTS baseline → native Docker containers → syscall/process eBPF telemetry → BPF ring buffer → common feature aggregation → user-space Logistic Regression, with a feasibility-gated fixed-point kernel-local LR placement variant → common threshold/policy → staged controlled enforcement → reproducibility recorder.

### Frozen controls
- 40-study evidence baseline unchanged.
- G1–G5 remain authoritative.
- No GPU/Kafka/distributed cluster/continual-learning framework/multimodal telemetry in the primary experiment.
- Kubernetes is deferred.
- Kernel-local ML is not assumed to be feasible.
- Enforcement is observe → detect/log → controlled mitigation with rollback.
- CHAT 06 contains no implementation or final experimental results.

### Next phase
**CHAT 07 — Prototype Implementation / Experimental Infrastructure**

The next phase must implement the frozen architecture, beginning with environment/preflight validation and the telemetry-only path before attempting kernel-local ML.


---

## CHAT 06 status correction

The authoritative CHAT 06 specification is `research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md`.

**CHAT 06 is COMPLETE.** The architecture is frozen for implementation, with a feasibility-gated kernel-local ML branch and an explicit hybrid/user-space fallback.

**Next:** CHAT 07 — Prototype Implementation / Experimental Infrastructure.


---

## CHAT 07 implementation checkpoint — 5 October 2026

**Status: PARTIAL / BLOCKED.**

The minimum prototype infrastructure has been created under `prototype/` and the detailed validation record is `research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md`.

Implemented capability:
- environment/preflight capture;
- BPF syscall/process telemetry source and libbpf loader;
- ring-buffer event stream and loss-accounting fields;
- deterministic 1-second feature aggregation;
- user-space Logistic Regression training/inference artifact;
- staged observe/detect-log/controlled-mitigation/rollback policy;
- reproducibility manifest;
- unit-test and CI scaffolding.

The current execution environment cannot validate native BPF/container integration because Docker and bpftool are absent, libbpf development headers are absent, and the installed Clang has no BPF target. Therefore BPF load, ring-buffer integration, container/cgroup identity, complete smoke test and the kernel-local feasibility gate remain unvalidated.

### CHAT 07 completion decision

**Not complete.** The project must not proceed to final experiments until the remaining infrastructure gates are passed on the required Linux validation host.

### Next continuation

Resume CHAT 07 on Ubuntu 24.04 LTS x86-64 with the pinned 6.8-series kernel and required Docker/libbpf/bpftool/Clang-BPF toolchain. Run preflight first, then complete native telemetry, ring-buffer accounting, container identity, Python tests, smoke test and reproducibility validation. Attempt kernel-local fixed-point LR only after those prerequisites pass. If it fails, record exact verifier/load evidence and retain the user-space/hybrid fallback.

Do not run the final experiment matrix or make scientific performance/superiority claims in CHAT 07.


---

## Review 2 literature-corpus completion checkpoint — 5 October 2026

**Status: COMPLETE**

The faculty Review 2 requirement for a minimum of 50 references and a literature-survey table covering all 50 papers has been integrated into the repository.

### Frozen distinction

- **Primary evidence baseline:** 40 studies, unchanged.
- **Primary composition:** 36 journal articles + 4 peer-reviewed conference papers = 90% journals.
- **Review 2 presentation corpus:** 50 references total.
- **Additional supporting/background references:** R041–R050.
- No primary study was replaced, renumbered or re-screened.

### Canonical Review 2 artifact

review2/REVIEW2_50_PAPER_LITERATURE_TABLE.md

This file contains the required Review 2 fields for the 50-reference presentation corpus: serial number, title, venue/year, dataset/workload/evidence base, methodology/algorithm, advantages/novelty and disadvantages/gaps/limitations.

### Next phase

Resume **CHAT 07 — Prototype Implementation / Experimental Infrastructure** on the required Linux validation host. The Review 2 literature requirement does not require CHAT 07 to be scientifically complete before PPT preparation.


---

## Live branch and Chat 08 synchronization protocol — 13 October 2026

This section supersedes any older instruction in this historical plan that suggests feature-branch-first work or says Chat 08 is certainly present on GitHub. **Use `main` as the sole canonical working branch for all remaining work.** Preserve old branches as historical references, but do not create/switch to feature branches for future chats, delete branches, force-push, or rewrite history.

The Chat 08 execution summary reports 350 runs and commit abbreviation `5732f2f`; GitHub did not resolve that commit and the Chat 08 report/processed CSVs were not found on `main` during reconciliation. Treat this as an unresolved local-to-remote synchronization/provenance discrepancy, not proof that the work was never done. The exact recovery gate and ChatGPT/AG division of responsibility are documented in `project/CHAT08_REPOSITORY_RECONCILIATION.md` and `project/CHAT_HANDOFF.md`.

**Required before Chat 09 analysis:** inspect local Git state, all branches/reflog and AG workspace; recover existing artifacts without destructive operations; identify the full SHA; validate raw-run completeness and regenerate summaries from raw JSON; commit/push all legitimate Chat 08 deliverables to `main`; verify GitHub file paths and local/remote SHA equality. Do not rerun the matrix unless a documented evidence audit proves runs are missing/invalid. Do not invent results or silently replace raw data.

**Mandatory handoff record:** at start and closure, document canonical branch, full local HEAD SHA, full `origin/main` SHA, clean/dirty status, last commit message, exact deliverable paths, validation commands/results, and the next chat prompt. A task is not complete merely because AG reports that commands ran; code, raw evidence, report, and reproduction instructions must be committed and remotely verifiable. Preserve frozen literature counts: 40 primary studies (36 journals + 4 peer-reviewed conferences) and 50 Review 2 references (40 primary + 10 supporting/background). Review 1 and Review 2 remain complete.
