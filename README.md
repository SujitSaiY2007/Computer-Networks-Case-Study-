# BACSE203 Computer Networks Case Study — Canonical Source of Truth

## Topic

**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

## Review 2 project status — 13 September 2026

- Review 1 established the problem, motivation and literature directions.
- The 45-study working pool has now been converted into a **Review 2 candidate primary-study set of 40 papers** after a relevance/venue-quality audit and targeted supplementation.
- The Review 2 target is **36 journal articles + 4 peer-reviewed conference papers = 90% journal references**.
- Preprints are not counted in the primary 40 unless their peer-reviewed publication status is later verified.
- Existing review papers are retained as background/comparison literature and are not counted as primary studies.
- The final 40 remain subject to full-text screening, quality assessment, duplicate checking and final DOI/database verification before the manuscript reference list is frozen.

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

- `research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md` — selected 40-paper primary evidence set, 90% journal ratio, per-paper methodology/merits/demerits/field and quality-assessment framework.
- `research/RESEARCH_GAPS_AND_FUTURE_AGENDA.md` — evidence-based gaps, existing technologies, proposed solution direction and evaluation framework.
- `review2/REVIEW_2_SLIDE_PLAN.md` — Review 2 presentation plan aligned with the course manuscript guidelines and Review 1.

## Repository structure

- `project/PROJECT_SCOPE_AND_RQS.md` — frozen topic boundary, RQs, contribution logic.
- `research/RESEARCH_EVIDENCE_MATRIX.md` — broader 45-study working evidence table.
- `research/RELEVANCY_AUDIT.md` — audit of the initial 18-paper list and screening decisions.
- `research/SEARCH_LOG.md` — search sources, query families, and verification status.
- `review1/REVIEW_1_SLIDE_PLAN.md` — Review 1 presentation structure and selected papers.
- `review1/Review_1_eBPF_Runtime_Security.pptx` — Review 1 presentation artifact.

## Intended synthesis framework

The review will synthesize evidence across:

**Telemetry extraction → feature representation → ML placement → detection decision → kernel enforcement**

and compare studies using:

**detection quality ↔ latency ↔ CPU/memory/event-processing overhead ↔ safety ↔ reproducibility.**

## Canonical-source rule

If later chats produce a conflicting paper count, relevance decision, scope statement, or project structure, **this repository and its latest committed evidence matrix are the reference point**. New papers must be added through the same extraction fields and must not silently replace earlier records.

## Quality warning

Several papers in the initial user-provided list contain incomplete or garbled numeric fields. Those values are not reconstructed by guesswork. Publisher/DOI metadata is preferred where verified; otherwise the record remains marked for full-text verification.
