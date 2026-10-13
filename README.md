# BACSE203 Computer Networks Case Study — Canonical Source of Truth

## Topic
**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

## Live status — 13 October 2026 (Chat 09 Complete / Chat 10 Handoff)
- **Review 1: COMPLETE**
- **Review 2 presentation (Chat 12): COMPLETE**
- **Chat 07 prototype implementation and native validation: COMPLETE**
- **Chat 08 controlled experiments execution: COMPLETE (recovered, audited, and verified directly on `main`)**
- **Chat 09 results verification, empirical synthesis, and manuscript sections: COMPLETE**
- **Chat 10: NEXT — Manuscript Development (Abstract to Conclusion)**
- **Canonical working branch: `main` only**
- Chat 07 validation commit: [`66512d8efdf5e16a8a8e9c3edd65534681b3bbfd`](https://github.com/SujitSaiY2007/Computer-Networks-Case-Study-/commit/66512d8efdf5e16a8a8e9c3edd65534681b3bbfd)

**Read first:** [Active Chat Handoff](project/CHAT_HANDOFF.md) and [Authoritative Status Correction](project/STATUS_CORRECTION_2026-10-13.md). The status correction supersedes conflicting phase/status statements in older roadmap sections and historical records. All remaining work must be committed directly to `main`. Preserve historical branches; do not force-push or rewrite history.

## Frozen evidence counts
- **Primary-study baseline:** 40 studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals.
- **Review 2 reference corpus:** 50 references = 40 primary studies + 10 supporting/background references.
- These are distinct counts. Do not alter the baseline or reopen completed literature-review phases without a concrete, documented evidence defect.

## Current phase sequence
**Chat 08 Controlled Experiments (COMPLETE) → Chat 09 Results Analysis (COMPLETE) → Chat 10 Manuscript (NEXT) → Chat 11 Final Audit/Submission Package**

Review 2 is already complete; do not schedule it as a future phase.

## Chat 09 evidence gate & empirical synthesis
The Chat 09 recovery gate has **PASSED**. The original Chat 08 commit `5732f2f7f3d65d1eb0abb475895cd27805d18320` and all 350 raw runs (`experiments/raw/run_*.json`), environment manifests, calibration models, processing scripts, summary CSVs, and plots were recovered from local Git and restored directly to `main`. 

All 350 runs across the 35-cell matrix were independently audited and recomputed:
- **Application Slowdown:** $<0.20\%$ across all instrumented configurations.
- **Memory Footprint:** Peak RSS overhead $\le 0.55$ MB above baseline.
- **Ring Buffer Drops:** Exactly $0.0000\%$ event loss across $77,598$ security events.
- **Placement Speedup:** In-kernel fixed-point LR achieved a **39.84x mean speedup** ($4.25\ \mu\text{s}$ vs $169.20\ \mu\text{s}$) and **18.44x detection latency reduction** ($0.085$ ms vs $1.567$ ms, $p < 10^{-11}$).
- **Enforcement & Safety:** Mitigation latency of $1.17$ ms with $100\%$ rollback success ($16\ \mu\text{s}$).
- **Detection & Confounding:** Process execution burst $F_1 = 0.824$; benign process churn ($B3$) exhibited a $50\%$–$80\%$ false alarm rate due to linear feature confounding (proving Gap 2); zero recall on held-out connection burst ($A3$).
- **Deliverables:** Reconstructed `research/CHAT08_CONTROLLED_EXPERIMENTS_EXECUTION.md`, `research/CHAT09_RESULTS_ANALYSIS_AND_EMPIRICAL_SYNTHESIS.md`, `research/CHAT09_MANUSCRIPT_RESULTS_AND_DISCUSSION.md`, and `research/CHAT09_LIMITATIONS_AND_VALIDITY_THREATS.md`.

## Chat 07 evidence
The detailed report is `research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md`. It records gates A–G: native BPF compile/load, ring-buffer transport/accounting, container identity correlation, unit tests, end-to-end telemetry-to-ML smoke pipeline, reproducibility manifest, and fixed-point kernel-local Logistic Regression feasibility.

Recorded environment: Ubuntu 24.04.3 under WSL2, kernel `6.6.87.2-microsoft-standard-WSL2`, which differs from the originally pinned 6.8-series kernel. Preserve this deviation in any report. The observed zero loss applies to the recorded 87-event validation run only; fixed-point feasibility does not establish comparative superiority. Chat 08 must audit the manifest's `git_sha` because the Chat 07 report indicates it may contain the pre-Chat-07 SHA.

## Start here for every new project chat
1. Read `project/CHAT_HANDOFF.md`.
2. Read `project/STATUS_CORRECTION_2026-10-13.md`.
3. Read `project/MASTER_EXECUTION_PLAN.md` and the phase-specific evidence files.
4. Execute only the active continuation prompt.
5. Preserve existing work, raw evidence, branch history, and frozen scope.
6. Before closing, update the handoff, status documents, artifacts, and exact next prompt; commit and verify the resulting branch/commit.

## Key project files
- `project/CHAT_HANDOFF.md` — current state and exact next continuation prompt.
- `project/STATUS_CORRECTION_2026-10-13.md` — authoritative correction of stale phase/status references, Chat 07 caveats, and Chat 08 integrity gates.
- `project/MASTER_EXECUTION_PLAN.md` — durable roadmap and historical phase instructions; use the status correction to resolve stale entries.
- `project/PROJECT_SCOPE_AND_RQS.md` — frozen topic boundary, research questions, and contribution logic.
- `research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md` — primary-study baseline and screening rationale.
- `research/PAPER_ACQUISITION_AND_ARCHIVE.md` — legitimate-access and private/local PDF archive register.
- `research/CHAT02_EVIDENCE_EXTRACTION.md` — field-level extraction matrix.
- `research/CHAT03_QUALITY_ASSESSMENT.md` — quality assessment.
- `research/CHAT04_CRITICAL_SYNTHESIS.md` — critical synthesis and taxonomy.
- `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md` — evidence-based gaps and future agenda.
- `research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md` — frozen experimental architecture/testbed.
- `research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md` — Chat 07 implementation and native validation evidence.
- `review2/REVIEW_2_SLIDE_PLAN.md` — Review 2 presentation plan.
- `experiments/` — Chat 08 raw outputs, manifests, processed metrics, and summaries (to be populated).

## Research framing
The defensible contribution is the intersection of **eBPF telemetry, ML runtime detection, and kernel-level enforcement in cloud/container environments**, emphasizing telemetry overhead, ML placement, detection-to-mitigation latency, enforcement safety, and evaluation practice. Do not claim to be the first review of eBPF cybersecurity.

## Evidence and reporting rules
- Separate paper-reported results, cross-paper synthesis, inference, and project interpretation.
- Mark unreported fields as “Not reported”; do not reconstruct missing facts by guesswork.
- Do not fabricate measurements or claim superiority without direct empirical support.
- Report experimental repetitions, denominators, variability, event loss, failures, and deviations.
- Keep raw outputs immutable and derive summaries reproducibly.
- Store metadata, DOI/official links, acquisition status, and verification notes in the public repository; do not commit unauthorized copyrighted PDFs.


## Chat 08 repository verification gate

The supplied Chat 08 summary claims 350 controlled runs and commit abbreviation `5732f2f`, but that commit could not be resolved through GitHub and the claimed report/processed CSVs were not found on `main` during reconciliation. The summary is not a substitute for committed evidence. Follow [the reconciliation protocol](project/CHAT08_REPOSITORY_RECONCILIATION.md) before treating Chat 08 as verified or publishing quantitative conclusions. This does not establish that local work is lost; it establishes that local-to-remote synchronization must be checked. Do not rerun the full matrix before inspecting local Git history and artifacts.

**Single-branch rule:** canonical branch is `main`; all future project changes must be committed and pushed directly to `main`. At each handoff verify full local and remote HEAD SHAs, working-tree status, and the presence of required artifact paths. Keep raw data immutable and preserve historical branches/files.
