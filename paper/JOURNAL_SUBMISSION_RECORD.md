# Journal Submission Record — Authoritative Metadata and Frozen Claims

**Status:** Editorial synchronization record, 23 October 2026  
**Source of truth:** The final 13-page submission PDF supplied by the author in this conversation, with the requested addition of Ragavan K to the author line.  
**Scope:** Manuscript and repository documentation only. No experiment was rerun, repeated, recalculated, or re-evaluated for this synchronization.

## Submission metadata

**Title:** eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, In-Kernel Inference, and Containment Trade-offs

**Authors (as requested):** Giri Nikhil Vaishnav; Sujit Sai Y; Shaik Mohammad Asif; Ragavan K.

Ragavan K is included as a supporting author at the author's request. Before journal submission, all authors should approve the final manuscript and confirm the author order, affiliations, contributions, and any journal-required declarations. No affiliation or contribution statement for Ragavan K is inferred here.

## Frozen headline claims from the supplied final PDF

These values are transcribed as reported in the final PDF; this file does not independently validate or recalculate them.

- Five configurations, seven Docker workloads (four benign and three anomalous), ten repetitions per configuration–workload combination: 350 randomized runs on one WSL2 host.
- Reported telemetry cost: 12–15 μs per recorded file/process event and approximately 25 μs per connection event.
- Reported throughput impact: no measurable loss at approximately 180 events/s and 54%–57% at 48,000 events/s.
- The PDF reports 8.87 million events and states that none were lost. This claim is transcribed from the supplied PDF and has not been reconciled against other repository records as part of this editorial-only task.
- The PDF reports Q16.16 fixed-point inference inside the eBPF probe, agreement with the user-space classifier on every run, median alert timing of 11.4 μs after the triggering syscall, and approximately 20 μs until user space received the alert.
- The PDF reports a median 9.1 ms to build features in the user-space path after a workload.
- Detection: all 20 trained-anomaly runs flagged with no false positives; all 10 held-out connection-burst runs missed.
- Reported median cgroup freeze time: 0.044 ms.
- The PDF also reports two earlier silent defects and their corrective tests.

## Important repository alignment note

The existing paper/MAIN_MANUSCRIPT.md was written for a different version of the study. Its title, author metadata, event accounting, workload-duration/RSS summaries, detection results, inference placement descriptions, and containment descriptions differ from the supplied final PDF. It is explicitly marked as superseded rather than silently edited to mix incompatible versions.

**Do not treat this record as a replacement for the complete manuscript.** The final submission PDF itself must be committed to this repository as a binary file, and a fully editable manuscript source matching that PDF must be prepared before calling the repository completely synchronized. The PDF artifact supplied in the conversation is available to download from the assistant's response; this record is the traceable metadata bridge until that artifact is added to GitHub.

## Editorial-only guardrails

- Do not rerun or reconduct any experiment.
- Do not recalculate or reinterpret the frozen results.
- Do not overwrite raw records, manifests, historical evidence, or prior audit reports.
- Do not claim the repository is fully synchronized until the exact final PDF and matching editable source are present in the repository.
- Journal formatting, references, and submission declarations may be edited without changing the reported evidence.
