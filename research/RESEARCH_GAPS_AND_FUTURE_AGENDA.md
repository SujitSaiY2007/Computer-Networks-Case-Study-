# CHAT 05 — Research Gap Consolidation / Evidence-to-Design Bridge

**Date:** 5 October 2026  
**Status:** **COMPLETE**  
**Frozen baseline:** **40 primary studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals**  
**Primary-study changes in CHAT 05:** None. P021/P031 unchanged.

## 1. Objective and evidence rules

CHAT 05 converts the completed CHAT 02 extraction, CHAT 03 quality assessment and CHAT 04 synthesis into a defensible research-gap framework.

Evidence levels remain distinct:
- **Reported evidence:** directly reported by primary studies.
- **Cross-paper synthesis:** a pattern visible across multiple studies.
- **Inference:** a conclusion derived from comparison.

The repository remains the source of truth. No new literature search, primary-study replacement, re-screening or numerical quality rescoring was performed.

## 2. Candidate-gap screening

| CHAT 04 candidate | Decision | Critical assessment |
|---|---|---|
| A. Fragmented end-to-end detection-to-mitigation latency | **RETAINED; merged with C** | Studies report inference, detection, throughput or enforcement latency, but the complete event→buffer→feature→inference→decision→mitigation chain is uncommon and inconsistently defined. |
| B. Robustness/generalization narrower than within-scenario detection | **RETAINED** | Bounded attack/workload evaluation dominates; P034 provides direct online-learning evidence, but drift/unseen-attack/adversarial evaluation is not established across the corpus. |
| C. Under-standardized event-loss/buffering measurement | **RETAINED; merged with A** | Event rate, buffer occupancy and dropped events are inconsistently reported. Separating this from end-to-end timing would duplicate one measurement/comparability problem. |
| D. Less-standardized safe-enforcement evaluation | **RETAINED** | Enforcement exists, but legitimate-operation impact, false-positive consequences and recovery/rollback are not evaluated consistently. |
| E. Heterogeneous ML-placement comparisons | **RETAINED** | In-kernel, user-space and hybrid approaches exist, but common-workload/common-metric comparison is insufficient for a general placement conclusion. |
| F. Reproducibility limitations | **RETAINED** | CHAT 03 identifies recurring gaps in code/configuration, kernel/runtime details, attack procedures, artifacts and external validity. |

### Claims explicitly rejected/downgraded

- “No continual learning exists” — **rejected**; P034 reports online learning.
- “No multimodal telemetry exists” — **rejected**; P018 and related studies demonstrate multiple modalities.
- “In-kernel ML is universally superior” or “user-space ML is universally superior” — **rejected**; evidence supports a trade-off.
- “No safe enforcement technology exists” — **rejected**; multiple studies demonstrate enforcement.
- “eBPF itself is insecure” as a standalone research gap — **downgraded to a CHAT 06 threat-model/design constraint**.
- Universal portability across kernels/clouds — **downgraded to a validation requirement**, not a standalone central gap.

## 3. Final research-gap matrix

| ID | Primary category | Validated gap | Supporting evidence | Limiting/contradicting evidence | Strength | RQ(s) | Resulting requirement |
|---|---|---|---|---|---|---|---|
| **G1** | Evaluation / Methodological | No common end-to-end measurement consistently connects telemetry generation, buffering/event loss, feature processing, inference, decision and mitigation. | P003, P005, P012, P014, P031, P034 report different portions of the pipeline; CHAT 03 identifies inconsistent event-loss/buffering and incomplete end-to-end latency. | Individual studies do measure latency/response, so this is not “no latency measurement”; it is a comparability/completeness gap. | **Strong** | RQ2, RQ4, RQ5 | Synchronized timestamps and common event-rate, loss, component-latency and detection-to-mitigation measurements. |
| **G2** | Evaluation / Technical | Robustness evidence under workload/attack distribution shift is narrower than within-scenario detection evidence. | P003, P006, P011, P016–P018, P031, P038 use bounded scenarios; P034 directly evaluates evolving workloads/online learning; CHAT 03 identifies limited drift/unseen-attack evidence. | P034 demonstrates adaptation is feasible; some datasets contain multiple attacks. Gap is insufficient breadth/standardization, not absence of adaptation. | **Moderate–Strong** | RQ3, RQ5 | Separate development/evaluation distributions; include feasible workload/temporal shift and, where possible, unseen attacks. |
| **G3** | Evaluation / Integration | ML placement is represented across in-kernel, user-space and hybrid forms but is not sufficiently compared under a common workload and measurement protocol. | P012 directly compares kernel/user-space placement; P002, P005, P031, P034 provide other placement patterns; CHAT 04 identifies placement trade-offs. | Placement comparison already exists in P012, so the gap is not missing technology; it is confounding across models, workloads and metrics. | **Moderate–Strong** | RQ1, RQ2, RQ4 | Hold telemetry semantics, workload and metrics constant across feasible placement variants. |
| **G4** | Evaluation / Deployment | Safe active enforcement is less consistently evaluated than detection capability. | P005, P019, P020, P025–P030, P031 demonstrate active controls; P005 reports enforcement latency. CHAT 03/04 identify inconsistent safety/recovery evaluation. | Enforcement is clearly demonstrated; the gap concerns safety evaluation, not enforcement availability. | **Strong** | RQ4, RQ5 | Staged/controlled enforcement with false-positive, legitimate-operation, mitigation-latency and recovery measurements. |
| **G5** | Reproducibility / Methodological | Cross-study reproducibility is constrained by incomplete environment, configuration, attack-generation and artifact disclosure. | CHAT 03 identifies reproducibility as frequently partial; CHAT 04 identifies kernel/runtime/container/orchestration dependencies. | Some studies, including P026, P027 and P034, provide stronger practical detail; public datasets exist. Gap is uneven reproducibility, not universal irreproducibility. | **Strong** | RQ5 | Pin/document kernel/runtime, container images, configurations, attack scripts, model versions, commands and raw results. |

## 4. Evidence → gap → RQ → requirement → validation

### G1
**Evidence:** component-level latency/overhead is reported inconsistently and event loss/buffering is often absent.  
**Gap:** no common end-to-end measurement methodology.  
**RQ:** RQ2/RQ4/RQ5.  
**Requirement:** synchronized timestamps across event generation, buffering, feature extraction, inference, decision and enforcement.  
**Validation:** low/high event-rate tests reporting event loss, CPU, memory and end-to-end detection-to-mitigation latency.

### G2
**Evidence:** many studies use bounded attack/workload distributions; P034 demonstrates online adaptation.  
**Gap:** insufficient standardized robustness evaluation under distribution shift.  
**RQ:** RQ3/RQ5.  
**Requirement:** separated development and shifted evaluation distributions.  
**Validation:** precision/recall/F1/FPR/calibration degradation under shift.

### G3
**Evidence:** P012 and other studies demonstrate multiple placement patterns.  
**Gap:** insufficient common-protocol placement comparison.  
**RQ:** RQ1/RQ2/RQ4.  
**Requirement:** common workload, telemetry semantics and metrics.  
**Validation:** detection quality, CPU/memory, throughput, event loss and latency comparison.

### G4
**Evidence:** active eBPF/XDP/LSM/syscall/process enforcement exists.  
**Gap:** enforcement safety is less standardized than detection.  
**RQ:** RQ4/RQ5.  
**Requirement:** staged policy/risk decision and explicit safety controls.  
**Validation:** false-positive blocking, legitimate-operation impact, mitigation latency and recovery/rollback.

### G5
**Evidence:** reproducibility is frequently partial and eBPF results depend on environment details.  
**Gap:** uneven artifact-level reproducibility.  
**RQ:** RQ5.  
**Requirement:** pinned environment/configuration plus repeatable scripts and raw outputs.  
**Validation:** clean rerun and configuration-sensitivity check.

## 5. Central research problem

> **The literature demonstrates that eBPF can support telemetry, ML-based detection and kernel-level enforcement, but it does not yet provide a sufficiently common and end-to-end evaluation basis for comparing integrated runtime-security pipelines across efficiency, robustness, response latency, enforcement safety and reproducibility.**

This is deliberately an **evaluation/integration problem**, not a claim that the component technologies are absent.

## 6. Defensible novelty position

The evidence does not justify “first ever,” “first system,” “no previous work,” or “completely unexplored.”

A defensible project position is:

> **A controlled, reproducible evaluation framework and prototype comparison that places existing eBPF telemetry, ML placement and enforcement mechanisms under a common workload and measurement protocol, with explicit treatment of telemetry completeness, end-to-end response latency, robustness, enforcement safety and reproducibility.**

Potential contribution dimensions:
- methodological: common end-to-end measurement and controlled comparison;
- evaluation: capability–efficiency–robustness–safety assessment;
- technical: modular implementation enabling controlled placement/enforcement comparisons;
- reproducibility: pinned environments, workloads, attack scripts, raw measurements and repeatable procedures.

Experimental novelty must be established by CHAT 06–10, not assumed here.

## 7. Evidence-to-design bridge

| Literature finding | Gap | Requirement | Future validation |
|---|---|---|---|
| Component-level latency/overhead are inconsistent | G1 | Timestamp each pipeline stage and measure event loss | End-to-end latency/event-loss benchmark |
| Detection is often bounded by attack/workload distribution | G2 | Separate development and shifted evaluation distributions | Workload/temporal/unseen-attack test |
| Multiple ML placements exist | G3 | Common workload/telemetry/metrics across placements | Placement comparison/ablation |
| Enforcement exists but safety metrics vary | G4 | Staged enforcement and safety controls | Legitimate-operation/false-positive/recovery test |
| Reproducibility depends on environment artifacts | G5 | Pin and document environment and artifacts | Clean rerun/artifact audit |

## 8. Requirements passed to CHAT 06

1. **Telemetry:** quantify event rate/completeness for at least one runtime telemetry modality.
2. **Latency:** measure component and end-to-end latency with synchronized timestamps.
3. **Placement:** compare at least two feasible ML-placement strategies under common conditions.
4. **Robustness:** include a feasible distribution-shift condition.
5. **Enforcement safety:** use staged/controlled enforcement and measure legitimate-workload impact.
6. **Reproducibility:** pin/document environment, configurations, workloads, attacks, model version and raw results.
7. **Baseline:** include a no-ML/no-enforcement baseline and telemetry-only configuration.

These are requirements, **not the final architecture**.

## 9. Remaining uncertainty

- Cross-study comparison remains constrained by heterogeneous objectives, telemetry semantics, hardware and datasets.
- Some evidence is Supporting/Adjacent rather than direct cloud/container ML evidence.
- Exact architecture and feasible hardware/software choices remain open for CHAT 06.
- Robustness and enforcement evaluations may need narrowing to remain student-feasible.
- The corpus does not justify a universal best ML model or placement.
- The literature does not establish a causal benefit of multimodal telemetry; that must be tested if used.

## 10. Completion decision

**CHAT 05 — COMPLETE.** All six CHAT 04 candidates were evaluated; A/C were merged to avoid redundancy. Final gaps have study-level support, RQ mappings and logically derived requirements. The 40-study baseline remains unchanged.

**Next phase:** **CHAT 06 — Experimental Architecture + Testbed Specification**.


---

## CHAT 06 architecture handoff

**Status:** COMPLETE

The five validated gaps are now translated into the authoritative experimental specification at:

- `research/CHAT06_EXPERIMENTAL_ARCHITECTURE_AND_TESTBED.md`

The selected minimum architecture is a single-host Linux/container testbed with one primary syscall/process telemetry modality, BPF ring-buffer transport, a common feature pipeline, user-space Logistic Regression, a feasibility-gated fixed-point kernel-local Logistic Regression placement variant, and staged controlled enforcement.

Important scope controls:
- no GPU, Kafka, distributed cluster, continual-learning framework or multimodal telemetry in the primary experiment;
- Kubernetes is deferred rather than required for the first controlled test;
- kernel-local ML is a feasibility-gated variant, not a claimed guaranteed capability;
- enforcement is isolated, staged and reversible;
- no experimental result is implied by the architecture document.

**Next phase:** CHAT 07 — Prototype Implementation / Experimental Infrastructure.
