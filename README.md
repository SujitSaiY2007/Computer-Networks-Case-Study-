# BACSE203 Computer Networks Case Study — Canonical Source of Truth

## Topic

**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

## Current project status — 25 August 2026

- Review boundary: cloud-native, containerized runtime security using eBPF/eBPF-derived telemetry and/or kernel enforcement, with ML as a central detection component where applicable.
- Publication window: January 2020 through the final search date.
- Minimum target evidence base: 45 relevant primary studies; course guidance recommends approximately 40–80 where the topic permits.
- Current uploaded research list contains **18 entries**, not 22. Two of those are generic cloud-native MLOps architecture papers and should not be counted in the primary runtime-security evidence set.
- This repository therefore treats the attached list as the **initial candidate pool**, audits it, and adds independently verified literature.
- The working evidence set currently contains **45 candidate studies** after the relevancy audit; each record is assigned a tier so adjacent eBPF studies are not presented as direct cloud-native ML evidence.

## Core research questions

1. What architectural patterns couple eBPF telemetry hooks with ML inference?
2. How is telemetry granularity traded against CPU, memory, buffering/event-loss, and scalability overhead?
3. Which ML methods are used, and how do they behave under container churn, concept drift, and adversarial evasion?
4. What kernel-level enforcement mechanisms exist, and what is the detection-to-mitigation latency?
5. How reproducible are datasets, testbeds, attack scenarios, metrics, and reported performance gains?

## Evidence policy

The course guidance requires a transparent search, screening, quality assessment, extraction matrix, and critical synthesis rather than a sequence of paper summaries. It also requires Scopus or Web of Science, IEEE Xplore, and ACM Digital Library as the minimum databases, with specialist sources such as USENIX, SpringerLink, ScienceDirect, arXiv, and relevant repositories added as appropriate.

**Important:** a paper is not included merely because it contains the word eBPF. Direct relevance is judged against the technology + runtime-security problem + cloud/container environment + evidence requirements. Existing surveys/reviews are used for discovery and comparison, not automatically counted as primary studies.

## Repository structure

- `project/PROJECT_SCOPE_AND_RQS.md` — frozen topic boundary, RQs, contribution logic.
- `research/RESEARCH_EVIDENCE_MATRIX.md` — canonical paper-level evidence table.
- `research/RELEVANCY_AUDIT.md` — audit of the uploaded 18-paper list and screening decisions.
- `research/SEARCH_LOG.md` — search sources, query families, and verification status.
- `review1/REVIEW_1_SLIDE_PLAN.md` — Review 1 presentation structure and selected papers.
- `review1/Review_1_eBPF_Runtime_Security.pptx` — generated presentation artifact.

## Canonical-source rule

If later chats produce a conflicting paper count, relevance decision, scope statement, or project structure, **this repository and its latest committed evidence matrix are the reference point**. New papers must be added through the same extraction fields and must not silently replace earlier records.

## Quality warning

Several papers in the initial user-provided list contain incomplete or garbled numeric fields in the source document. Those values are not reconstructed by guesswork. Where a publisher/DOI source was verified, the verified metadata is preferred; otherwise the record is marked for full-text verification.
