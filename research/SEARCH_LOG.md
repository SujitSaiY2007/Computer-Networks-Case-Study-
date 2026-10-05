# Search Log — Working Record

**Project:** eBPF-Assisted Machine Learning for Cloud-Native Runtime Security
**Search date:** 25 August 2026
**Status:** working log; final Boolean strings must be frozen and rerun in the required academic databases before final PRISMA counts are reported.

## Required academic sources from the course guide

1. Scopus or Web of Science
2. IEEE Xplore
3. ACM Digital Library

## Additional specialist sources

- USENIX / USENIX Security / OSDI / NSDI
- SpringerLink
- ScienceDirect / Elsevier
- arXiv (preprints clearly labeled)
- Publisher pages and author repositories for metadata verification

## Search concept blocks

### Technology
`eBPF OR "extended Berkeley packet filter" OR BPF-LSM OR XDP OR kprobe OR tracepoint OR "TC BPF"`

### Runtime/cloud-native security
`Kubernetes OR container* OR "cloud-native" OR "container runtime" OR "runtime security" OR "container security" OR "intrusion detection" OR "anomaly detection"`

### ML/evaluation/enforcement
`machine learning OR deep learning OR autoencoder OR LSTM OR "isolation forest" OR GNN OR inference OR overhead OR latency OR enforcement OR mitigation OR verifier`

## Search families

1. `(eBPF OR "extended Berkeley packet filter" OR BPF-LSM OR XDP) AND (Kubernetes OR container* OR "cloud-native") AND (security OR intrusion OR anomaly OR malware)`
2. `(eBPF OR XDP) AND ("machine learning" OR "deep learning" OR autoencoder OR LSTM OR "decision tree") AND (security OR intrusion OR anomaly)`
3. `(eBPF OR BPF-LSM) AND (runtime enforcement OR mitigation OR isolation OR access control) AND (container* OR Kubernetes)`
4. `(eBPF OR XDP) AND (overhead OR latency OR throughput OR "event loss" OR verifier) AND (security OR container* OR Kubernetes)`

## Verification examples

The following records were independently checked against publisher/academic pages during the working search:

- Bachl, Fabini & Zseby, **A flow-based IDS using Machine Learning in eBPF** — arXiv record confirms a decision-tree ML IDS running entirely in eBPF and reports >20% performance increase over a userspace implementation. 
- Lim et al., **Secure Namespaced Kernel Audit for Containers** — ACM SoCC '21 confirms saBPF, Kubernetes deployment, IDS/access control, and performance/security evaluation.
- Gwak, Doan & Jung, **Container Instrumentation and Enforcement System for Runtime Security of Kubernetes Platform with eBPF** — publisher page confirms Kubernetes runtime security, LSM-hook enforcement, and 2023 publication details.

## Search integrity rules

- Do not count search snippets as evidence.
- Verify DOI, venue, year, and publication status against the publisher, DOI registry, or academic database.
- Preprints remain candidates but must be labeled as preprints and should not silently be treated as peer-reviewed primary studies.
- Reviews/surveys are discovery/context sources, not automatic members of the primary evidence set.
- Do not report final PRISMA numbers until duplicate removal and full-text screening are completed.


## CHAT 01 verification update — 5 October 2026

CHAT 01 has completed the candidate-study verification stage.

### Result

- Verified primary baseline: **40 studies**
- Journals: **36**
- Peer-reviewed conferences: **4**
- Journal share: **90.0%**
- Core: **14**
- Supporting/Adjacent: **26**
- Preprint-only primary studies retained: **0**
- Retraction flags found in the scholarly identifier audit: **0**

### Screening correction

The provisional candidate *Extended Berkeley Packet Filter: An Application Perspective* was confirmed as a review article and therefore removed from the primary-study count. It remains background/comparison literature.

Replacement: *Container-Specific Service Mesh-Based System for Mitigating Lateral Movement Attacks*, IEEE Transactions on Cloud Computing (2026), DOI 10.1109/TCC.2026.3657486.

### Metadata corrections

CHAT 01 also reconciled stale working metadata against authoritative records for several studies, including CODAX, Optimus, Coda, BeaCon and Vaccine. The detailed row-level decisions are recorded in research/CHAT01_FULLTEXT_VERIFICATION.md.

### Next phase

**CHAT 02A — Paper Acquisition & Archive.**

Final PRISMA/search counts remain intentionally unfrozen until the required database searches, duplicate removal and subsequent full-text screening are formally documented.
