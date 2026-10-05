# CHAT 06 — Experimental Architecture + Testbed Specification

**Date:** 5 October 2026  
**Status:** **COMPLETE**  
**Baseline:** **40 primary studies = 36 journal articles + 4 peer-reviewed conference papers = 90% journals**  
**Primary-study changes:** None. P021/P031 unchanged.

## 1. Purpose and design boundary

CHAT 06 translates the five validated CHAT 05 gaps into a technically feasible experimental specification.

This is a **design/specification phase only**. No prototype implementation, final experiment, measured result, or novelty claim is made here.

The architecture is deliberately an **evaluation/integration architecture** rather than a claim that any individual component is novel.

### Frozen research questions

- **RQ1:** What architectural patterns couple eBPF telemetry hooks (kprobes, tracepoints, BPF-LSM, TC/XDP) with ML inference pipelines?
- **RQ2:** How do systems trade telemetry granularity against CPU, memory, buffering/event loss, and scalability overhead?
- **RQ3:** Which ML methods are used, and what evidence exists concerning concept drift, container churn, and adversarial evasion?
- **RQ4:** What mechanisms support real-time kernel mitigation, and what is the detection-to-mitigation latency?
- **RQ5:** What datasets, cloud testbeds, attack scenarios, metrics, and reproducibility artifacts are used?

## 2. Design principles

1. **Minimum sufficient architecture:** do not add infrastructure unless it answers an RQ or validates G1–G5.
2. **Controlled comparison:** hold workload, telemetry semantics, features, train/test split and model family constant when comparing ML placement.
3. **One primary telemetry modality:** syscall/process runtime telemetry is sufficient for the first controlled study; network telemetry is not added merely for architectural complexity.
4. **Kernel-local ML is a test condition, not an assumption:** a small fixed-point linear classifier is the feasibility candidate. If verifier/load constraints prevent a safe implementation, the planned fallback is hybrid inference.
5. **Controlled enforcement only:** enforcement is staged and reversible.
6. **No autonomous production blocking:** the testbed is isolated and all mitigation actions are deliberately bounded.
7. **Measured event volume:** expected event rate is measured during a calibration run; it is not fabricated in advance.
8. **Reproducibility from day one:** exact kernel, compiler, container image digests, configurations, scripts, seeds and raw measurements are captured.

---

# 3. Gap → requirement derivation

| Gap | Requirement | Architecture consequence | Validation |
|---|---|---|---|
| G1 — end-to-end latency/telemetry completeness | Timestamp every pipeline stage and quantify event loss | Monotonic timestamps in BPF events plus user-space stage timestamps; explicit sequence IDs and buffer counters | Event-rate sweep; component and end-to-end latency; event-loss percentage |
| G2 — distribution-shift robustness | Separate development and evaluation distributions | Frozen development split plus shifted workload evaluation | In-distribution vs shifted F1/FPR/recall/calibration degradation |
| G3 — ML-placement comparison | Compare at least two placements under common conditions | User-space LR vs kernel-local fixed-point LR; hybrid fallback if required | Same features/model parameters/conditions; compare quality, latency and resource cost |
| G4 — safe enforcement | Stage observation, detection and mitigation | Observe → log → controlled mitigation state machine with allow-list and rollback | False-positive impact, mitigation latency, rollback success |
| G5 — reproducibility | Pin environment and artifact provenance | Environment manifest, image digests, model hash, seed registry, experiment manifest and raw outputs | Clean rerun and artifact audit |

No additional architecture component is justified unless it maps to this table.

---

# 4. Architecture alternatives

## Option A — Baseline / no ML / no enforcement

**Purpose:** establish workload behaviour without security instrumentation.

**RQ coverage:** RQ2, RQ5.

**Advantages**
- Lowest overhead.
- Provides the reference for instrumentation cost.
- Simple to reproduce.

**Disadvantages**
- Does not answer ML placement or mitigation questions.

**Decision:** **Required baseline**, not the complete architecture.

---

## Option B — eBPF telemetry only

**Purpose:** quantify telemetry cost and event completeness independently of ML.

**RQ coverage:** RQ1, RQ2, RQ5.

**Advantages**
- Isolates eBPF instrumentation overhead.
- Directly supports G1.
- Provides a clean baseline for ML overhead.

**Disadvantages**
- No detection decision or enforcement.

**Decision:** **Required experimental configuration.**

---

## Option C — eBPF + user-space ML

**Purpose:** primary practical ML pipeline.

**RQ coverage:** RQ1–RQ5, especially RQ2/RQ3/RQ4.

**Architecture:** eBPF tracepoints → ring buffer → feature aggregation → ML inference in user space → decision.

**Advantages**
- Lowest implementation risk among ML variants.
- Rich model/library support.
- Clear measurement boundary between kernel telemetry and user-space processing.

**Disadvantages**
- Kernel/user-space data transfer contributes latency and buffering overhead.

**Decision:** **Required primary ML configuration.**

---

## Option D — eBPF + lightweight kernel-local ML

**Purpose:** isolate the cost/benefit of moving a deliberately small inference function into the kernel.

**Candidate model:** logistic/linear classifier represented with integer/fixed-point coefficients and bounded arithmetic.

**Advantages**
- Same mathematical model family can be compared against user-space inference.
- Removes a kernel→user-space inference transfer for the decision path.
- Directly addresses RQ1/RQ2/RQ4.

**Disadvantages**
- eBPF verifier and instruction/resource constraints limit model complexity.
- Floating-point/general ML frameworks are inappropriate for the kernel-local path.
- Deployment is kernel-version/configuration sensitive.
- More engineering effort and greater failure risk.

**Decision:** **Retained as an explicitly feasibility-gated variant.** If the fixed-point classifier cannot be loaded and validated safely on the pinned testbed, it is not forced. The fallback is Option C plus a hybrid placement experiment.

---

## Option E — eBPF + ML + controlled enforcement

**Purpose:** evaluate the complete detection-to-mitigation path.

**RQ coverage:** RQ2, RQ4, RQ5.

**Architecture:** telemetry → features → ML → risk decision → staged policy → bounded kernel enforcement.

**Advantages**
- Directly validates G1 and G4.
- Measures the complete response path.

**Disadvantages**
- Higher safety and implementation complexity.
- False positives can affect legitimate workloads.

**Decision:** **Required final evaluation configuration, but enforcement remains staged and isolated.**

---

# 5. Selected architecture

## Selected minimum architecture

**Host Linux kernel**
→ **container workloads**
→ **eBPF syscall/process telemetry**
→ **bounded ring-buffer transport**
→ **user-space feature aggregator**
→ **shared feature vector**
→ **Placement V1: user-space Logistic Regression**
**or**
**Placement V2: kernel-local fixed-point linear classifier, if feasible**
→ **common risk threshold**
→ **observe/log**
→ **controlled mitigation**
→ **rollback/recovery**
→ **experiment recorder**

### Why this is the minimum sufficient architecture

It directly covers:

- **G1:** complete event-to-decision-to-mitigation timing and event-loss accounting;
- **G2:** shifted workload evaluation;
- **G3:** controlled placement comparison;
- **G4:** staged enforcement safety;
- **G5:** reproducible environment and artifact capture.

It deliberately excludes a GPU, distributed cluster, Kafka, service mesh, federated learning, continual-learning framework, multimodal telemetry and autonomous policy engine because none is required to answer the frozen RQs in the first controlled experiment.

---

# 6. Testbed specification

## 6.1 Hardware

### Minimum
- One x86-64 Linux machine.
- **4 physical CPU cores / 8 logical threads or better.**
- **16 GB RAM minimum; 32 GB preferred.**
- At least 50 GB free SSD space.
- Hardware virtualization support if a VM fallback is needed.

### GPU
**Not required.**

The selected models are lightweight classical ML models and the experiment is primarily CPU/kernel instrumentation limited.

### Multiple machines
**Not required for the primary experiment.**

A second machine is optional only for a later external-validity/network-load extension.

### Containers / VM
Native Linux containers are preferred for the primary experiment. A VM is an acceptable fallback when host privileges or kernel isolation make native execution impractical.

### Network
No external attack target is required. Any network anomaly workload uses an isolated local test sink or container network.

---

## 6.2 Operating system and kernel

**Preferred OS:** Ubuntu 24.04 LTS, x86-64.

**Pinned kernel:** use the Ubuntu 24.04 GA 6.8 kernel line for the reproducibility baseline, with the exact installed package version recorded in the experiment manifest. Do not silently upgrade the kernel between experimental runs.

The exact kernel package version must be captured with uname -a and package-manager metadata.

A newer supported kernel may be evaluated later as a portability experiment, but it must not replace the pinned baseline.

---

## 6.3 Container runtime

**Primary:** Docker Engine + Docker Compose.

Rationale:
- simpler than a nested Kubernetes/kind setup;
- directly provides isolated container workloads;
- exposes container lifecycle and cgroup behaviour needed for churn experiments;
- avoids introducing a second orchestration layer whose overhead would confound the first study.

**Kubernetes:** deferred to a later extension. It is not required for the primary controlled experiment.

---

## 6.4 eBPF tooling

Primary tooling:

- Linux kernel BPF subsystem;
- **libbpf**;
- **bpftool**;
- Clang/LLVM for BPF object compilation;
- C for the BPF program and loader;
- Python for orchestration, feature processing, ML training and experiment analysis.

libbpf is preferred over a higher-level framework because it exposes the kernel/user-space boundary explicitly and keeps the measurement path small.

---

# 7. Telemetry design

## 7.1 Primary modality

**Process/syscall runtime telemetry.**

This is one telemetry modality even though several event types are sampled.

### Candidate hooks

1. tracepoint/syscalls/sys_enter_execve
2. tracepoint/syscalls/sys_enter_openat
3. tracepoint/syscalls/sys_enter_connect
4. optional tracepoint/syscalls/sys_enter_unlinkat

The final minimal event set should be reduced during calibration if one event type adds little experimental value.

### Container identity

Use cgroup/process identity captured at the telemetry boundary and map events to the experiment's container identifier in user space.

Linux cgroup v2 is used as the resource/identity boundary where available.

## 7.2 Event fields

Each event should contain only fields required for the experiment:

- monotonic event timestamp;
- event sequence number;
- event type;
- PID/TID;
- cgroup identifier;
- return/status information where available;
- compact operation-specific numeric fields;
- experiment/run identifier if practical.

Avoid raw command lines, full file paths or payloads unless explicitly needed; minimizing telemetry also reduces privacy and processing overhead.

## 7.3 Timestamping

Use a monotonic clock domain.

Required timestamps:

- **T0:** event generated in BPF;
- **T1:** event consumed from ring buffer;
- **T2:** feature-window update completed;
- **T3:** inference start;
- **T4:** inference completed;
- **T5:** decision produced;
- **T6:** enforcement action requested;
- **T7:** mitigation outcome observed.

Derived metrics:

- telemetry transfer = T1 − T0;
- feature latency = T2 − T1;
- inference latency = T4 − T3;
- decision latency = T5 − T4;
- enforcement latency = T7 − T6;
- end-to-end detection latency = T5 − T0;
- detection-to-mitigation latency = T7 − T0.

Clock synchronization between separate machines is therefore unnecessary for the primary testbed.

## 7.4 Buffering

Use **BPF ring buffer** as the primary transport.

Required measurements:

- total generated events;
- successfully submitted events;
- consumed events;
- reservation failures;
- sequence gaps;
- buffer occupancy samples.

The ring buffer is appropriate because the Linux documentation explicitly supports shared multi-CPU buffering and reports reservation failure when insufficient space exists. It also provides APIs for observing available data and buffer size.

## 7.5 Event-loss definition

For each run:

event_loss_rate = 1 - (consumed_events / generated_events)

Also record the reason when distinguishable:

- ring-buffer reservation failure;
- consumer lag;
- sequence gap;
- user-space processing failure.

Do not treat a missing event as an ML false negative; telemetry loss is a separate measurement layer.

---

# 8. Feature pipeline

## 8.1 Processing chain

**Raw event → container mapping → fixed window aggregation → normalization → feature vector → model**

## 8.2 Window

Primary window: **1 second tumbling window**.

Sensitivity experiment: **250 ms and 2 s** windows only if the primary results show a meaningful window-size dependency.

## 8.3 Candidate features

For each container/window:

1. exec_count
2. open_count
3. connect_count
4. unlink_count
5. unique_process_count where reliably available
6. failed_operation_count
7. event_count
8. event_rate
9. event_loss_rate
10. optional short-window burst indicator

The final feature set is frozen **after calibration**, not selected by looking at test labels.

## 8.4 Normalization

For Logistic Regression:
- fit normalization parameters on the development set only;
- store mean/scale parameters with the model artifact;
- apply the same transformation to validation, test and shifted-distribution data.

For kernel-local fixed-point inference:
- quantize the already-fitted normalization and model coefficients into a documented integer representation;
- use bounded arithmetic;
- record scale factors and quantization error.

## 8.5 Leakage prevention

The following are prohibited:
- fitting normalization on the full dataset;
- selecting features using evaluation labels;
- tuning the decision threshold on the final test set;
- mixing future shifted-distribution observations into development training;
- using attack labels as runtime features.

---

# 9. ML design

## 9.1 Candidate models

| Model | Role | Reason |
|---|---|---|
| Logistic Regression | Primary | Small, interpretable, low-cost and straightforward to reproduce |
| Random Forest | Secondary candidate | Strong classical baseline and represented in the literature |
| Gradient boosting | Optional | Consider only if LR/RF fail to provide sufficient detection quality |
| Small neural network | Deferred | Not justified unless simpler models are inadequate |

Deep learning is **not** assumed to be superior.

## 9.2 Selected primary model

**Logistic Regression** is the default model for the placement experiment.

Reason:
- same mathematical decision function can be implemented in user space and as bounded fixed-point arithmetic in eBPF;
- model size is small;
- inference cost is measurable;
- avoids conflating model complexity with placement.

Random Forest may be evaluated as a secondary model only after the primary placement protocol is working.

## 9.3 Placement variants

### V1 — User-space

BPF telemetry → ring buffer → user-space feature aggregation → LR inference → decision.

### V2 — Kernel-local

BPF telemetry → bounded feature accumulation → fixed-point linear score → threshold decision.

To preserve comparability, the kernel-local classifier uses the same trained LR coefficients after documented quantization.

### Fallback — Hybrid

If V2 cannot be safely loaded or its quantization/feature semantics cannot be made equivalent, use:

BPF telemetry/partial feature aggregation → user-space inference.

The fallback must be documented as a feasibility boundary, not hidden.

---

# 10. Decision and enforcement

## 10.1 Decision output

Every inference produces:
- run ID;
- container ID;
- timestamp;
- model/placement ID;
- score;
- threshold;
- predicted class;
- action state.

## 10.2 Threshold

The threshold is selected using the development/validation data and frozen before the final evaluation.

A secondary threshold-sensitivity analysis may use:
- conservative threshold;
- selected threshold;
- permissive threshold.

The final test set must not be used to choose the primary threshold.

## 10.3 Enforcement state machine

### Stage 0 — Observe only

Telemetry and inference operate, but no blocking action occurs.

### Stage 1 — Detect + log

A high-risk decision is recorded with no workload modification.

### Stage 2 — Controlled mitigation

Only a pre-approved test action is allowed, for example:
- isolate the test container from the isolated test network;
- deny a narrowly defined test operation at a BPF LSM hook;
- terminate/restart the intentionally disposable test workload through the experiment controller.

The action must never target the host or unrelated processes.

### Rollback

Every mitigation must have a deterministic recovery procedure.

Record:
- mitigation requested;
- mitigation completed;
- rollback requested;
- rollback completed;
- recovery time;
- failure reason.

---

# 11. Benign workloads

The workload suite must be deterministic enough to repeat but varied enough to avoid training on one fixed trace.

## B1 — Idle/service baseline
- Long-running simple service.
- Low event volume.
- Used for baseline overhead.

## B2 — Normal file-processing workload
- Repeated reads/writes of synthetic test files.
- Controlled file sizes and repetition counts.

## B3 — Process-churn workload
- Bounded creation and termination of worker processes.
- Useful for container churn and syscall-rate variation.

## B4 — Normal client/server workload
- Local container-to-container requests against a test service.
- Fixed request-rate levels.

Each workload has:
- fixed duration;
- configuration file;
- deterministic seed where randomness exists;
- expected ground-truth label;
- workload hash/version.

---

# 12. Anomaly / attack scenarios

The primary experiment uses **safe, isolated, reproducible anomaly scenarios**, not uncontrolled real-world attacks.

## A1 — Abnormal process-execution burst

A disposable test container launches an unusually high but bounded number of short-lived processes.

**Expected telemetry:** elevated exec_count, process churn and event rate.

**Ground truth:** controller-defined anomaly interval.

## A2 — Abnormal file-access pattern

A disposable test workload repeatedly accesses a controlled set of synthetic files at an abnormal rate/pattern.

**Expected telemetry:** elevated file-operation counts and burstiness.

## A3 — Connection burst to local test sink

The workload creates a bounded burst of connections to an isolated local/container sink.

**Expected telemetry:** elevated connect_count and event rate.

## A4 — Optional combined anomaly

A1 + A2 or A1 + A3 at controlled timing.

Use only if the primary single-anomaly results are stable.

### Training/evaluation allocation

Development:
- benign B1–B4;
- A1/A2 at selected intensities.

Evaluation:
- held-out benign traces;
- held-out intensity levels;
- shifted workload mix;
- A3 as an unseen anomaly if the development experiment remains stable.

No evaluation labels are used for model fitting.

---

# 13. Distribution-shift experiment

## Primary shift

**Workload-intensity / temporal shift.**

### Development distribution D

- fixed mixture of B1–B4;
- A1/A2 at development intensities;
- training and validation traces collected separately.

### In-distribution test ID

Same workload families and intensity range, but from different runs/seeds.

### Shifted test S

Change at least one of:
- workload mixture;
- event intensity;
- temporal ordering;
- container churn rate.

The shift configuration is declared before evaluation.

### Optional stronger shift

Use A3 as an unseen anomaly type.

### Robustness metrics

Report:
- precision;
- recall;
- F1;
- FPR;
- FNR;
- calibration error if probability outputs are retained;
- absolute and relative degradation from ID → S.

Primary robustness statement:

degradation = metric_ID - metric_shifted

Do not claim generalization beyond the tested shift.

---

# 14. Experimental configurations

| ID | Telemetry | ML | Enforcement | Purpose |
|---|---|---|---|---|
| C0 | None | None | None | Bare workload baseline |
| C1 | eBPF | None | None | Telemetry overhead/completeness |
| C2 | eBPF | User-space LR | None | Practical ML detection |
| C3 | eBPF | Kernel-local LR | None | Placement comparison, if feasible |
| C4 | eBPF | User-space LR | Observe/log | Detection + decision path |
| C5 | eBPF | User-space LR | Controlled | End-to-end mitigation |
| C6 | eBPF | Kernel-local LR | Controlled | Full kernel-local path, only if V2 passes feasibility gate |

C3/C6 are omitted from the final comparison if the kernel-local feasibility gate fails.

---

# 15. Measurement framework

## Detection
- accuracy;
- precision;
- recall;
- F1;
- FPR;
- FNR;
- confusion matrix.

## Runtime cost
- CPU utilization;
- memory usage;
- event rate;
- throughput;
- buffer occupancy;
- event loss.

## Latency
- T1−T0 telemetry transfer;
- T2−T1 feature processing;
- T4−T3 inference;
- T5−T4 decision;
- T7−T6 enforcement;
- T5−T0 end-to-end detection;
- T7−T0 detection-to-mitigation.

## Safety
- false-positive count;
- legitimate operations affected;
- legitimate workload degradation;
- mitigation success rate;
- rollback success rate;
- recovery time;
- enforcement failure behaviour.

## Model/deployment
- model size;
- coefficient count;
- inference CPU time;
- model load time;
- training time;
- quantization error for kernel-local variant.

---

# 16. Calibration and event-rate protocol

Before final experiments:

1. Run C0 with each benign workload.
2. Run C1 with the same workloads.
3. Measure event-generation distribution.
4. Sweep workload intensity to at least three empirically observed levels.
5. Choose low/medium/high event-rate bands from measured quantiles rather than arbitrary event counts.
6. Size the ring buffer so that the normal condition is measurable without immediate overflow.
7. Repeat selected high-rate conditions specifically to induce measurable stress.
8. Record event loss rather than treating loss as an implementation bug to hide.

This separates **instrumentation behaviour** from **model behaviour**.

---

# 17. Statistical plan

## Repetitions

Use **10 independent repetitions per primary condition** after the calibration stage.

Use deterministic seeds for workload generation where applicable; the seed list is stored in the experiment manifest.

## Aggregation

For each condition report:
- median;
- interquartile range;
- mean and standard deviation where informative;
- 95% confidence interval.

Latency distributions should not be summarized by mean alone. Report median and high percentiles such as p95 and p99.

## Comparisons

Primary comparisons are paired by workload/run configuration.

- If paired differences satisfy the assumptions for a parametric comparison, a paired t-test may be used.
- Otherwise use the Wilcoxon signed-rank test.
- For more than two repeated conditions, use an appropriate repeated-measures method after checking assumptions; otherwise use a non-parametric alternative.
- Report effect sizes alongside p-values.
- Correct for multiple comparisons when multiple pairwise hypotheses are tested.

The statistical test is selected **after inspecting assumptions**, not prescribed in advance merely because it is conventional.

## Outliers

Do not delete outliers solely because they weaken a result.

Record:
- raw value;
- reason for any technically invalid run;
- whether exclusion was pre-specified;
- sensitivity analysis where practical.

---

# 18. Ablation plan

Only ablations tied to causal questions are retained.

| Ablation | Causal question |
|---|---|
| C0 vs C1 | What is the cost of eBPF telemetry itself? |
| C1 vs C2 | What is the incremental cost of user-space ML? |
| C2 vs C3 | What changes when inference placement moves kernel-local? |
| C2 vs C4 | What is the cost of enabling the decision path? |
| C4 vs C5 | What is the additional latency/safety cost of controlled enforcement? |
| Low vs high event rate | How does telemetry pressure affect loss and latency? |
| ID vs shifted test | How sensitive is detection to distribution shift? |
| Optional window-size test | Does feature-window granularity materially alter the trade-off? |

No ablation is added merely to increase the experiment count.

---

# 19. Reproducibility artifact specification

Record/version:

### Environment
- OS release;
- exact kernel package/version;
- architecture;
- CPU/RAM;
- Docker version;
- container image digest;
- libbpf version/source revision;
- bpftool version;
- Clang/LLVM version;
- Python version;
- Python dependency lock file.

### Source
- Git commit SHA;
- BPF source;
- user-space loader;
- feature code;
- model-training code;
- enforcement policy;
- workload scripts;
- anomaly scripts.

### Configuration
- telemetry hooks;
- ring-buffer size;
- feature window;
- normalization parameters;
- model coefficients;
- quantization scale;
- threshold;
- workload configuration;
- seed list.

### Results
- raw event logs;
- raw timing records;
- CPU/memory measurements;
- model outputs;
- processed CSV/Parquet files;
- plots/tables;
- run metadata;
- failed-run log.

Every result file must be linked to:
experiment_id + git_sha + environment_id + seed + configuration_id.

---

# 20. Feasibility gates

## Gate F1 — eBPF telemetry
Pass only if:
- program loads successfully;
- required hooks are available;
- event schema is stable;
- event sequence accounting works.

## Gate F2 — user-space ML
Pass only if:
- feature extraction is deterministic;
- train/test separation is demonstrable;
- inference result is reproducible for identical input.

## Gate F3 — kernel-local ML
Pass only if:
- fixed-point classifier loads under the pinned kernel;
- verifier accepts it;
- bounded execution is demonstrated;
- output agrees with the reference implementation within the predeclared quantization tolerance;
- no unsafe host-targeting behaviour exists.

If F3 fails, **do not weaken the safety requirement just to keep Option D**. Use the hybrid fallback.

## Gate F4 — controlled enforcement
Pass only if:
- Stage 0 and Stage 1 work without workload modification;
- Stage 2 affects only disposable test resources;
- rollback succeeds;
- failure defaults to observation rather than irreversible blocking.

## Gate F5 — reproducibility
Pass only if:
- environment manifest is complete;
- exact source commit is recorded;
- seed/configuration mapping is complete;
- raw outputs can be associated with a run.

---

# 21. Feasibility and risk analysis

| Risk | Probability | Impact | Mitigation | Fallback |
|---|---|---|---|---|
| Kernel/eBPF feature mismatch | Medium | High | Pin kernel; preflight capability checks | Use supported hook subset |
| Verifier rejects kernel-local classifier | Medium–High | High | Keep model tiny; bounded fixed-point arithmetic | Hybrid/user-space placement |
| Ring-buffer overflow | Medium | Medium | Measure event rate; tune buffer; stress deliberately | Reduce telemetry fields or use controlled sampling, documented |
| Excessive telemetry overhead | Medium | High | Minimal fields; calibration; rate sweep | Narrow event set |
| Container identity ambiguity | Medium | Medium | cgroup/process mapping validation | Restrict experiment to dedicated containers |
| ML leakage | Medium | High | Frozen split; fit transforms on development data only | Rebuild dataset/split |
| False-positive enforcement | Medium | High | Observe/log stages; allow-list; disposable workloads | Disable Stage 2 and report detection-only |
| Non-repeatable workload | Medium | Medium | Seeded scripts and fixed configs | Reduce workload stochasticity |
| Host resource contention | Medium | Medium | Dedicated experiment window; record host state | Repeat on quieter host |
| Kernel update during study | Low–Medium | High | Pin exact package/version and record hash | Rebuild all results after environment change |
| Schedule overrun | Medium | Medium | Implement C0–C5 first; treat C3/C6 as optional gate | Finish user-space comparison + safety evaluation |

---

# 22. Traceability matrix

| Research Gap | RQ | Requirement | Architecture Component | Experiment | Metric | Expected Evidence |
|---|---|---|---|---|---|---|
| G1 | RQ2/RQ4/RQ5 | Complete timestamp chain + event completeness | BPF timestamps, ring buffer, stage recorder | Event-rate sweep, C0–C5 | event loss, CPU, buffer occupancy, T0–T7 latency | End-to-end latency/event-loss profile |
| G2 | RQ3/RQ5 | Separate development and shifted evaluation | Frozen split + shift generator | ID vs S | F1, recall, FPR, FNR, calibration, degradation | Robustness/degradation profile |
| G3 | RQ1/RQ2/RQ4 | Same features/model/workload across placements | V1 user-space LR + V2 kernel-local LR | C2 vs C3 | detection, inference latency, CPU, memory, event loss | Placement trade-off evidence |
| G4 | RQ4/RQ5 | Staged safe mitigation | policy state machine + BPF LSM/controlled action | C4 vs C5 | mitigation latency, legitimate impact, rollback success | Safety/response evidence |
| G5 | RQ5 | Versioned reproducibility artifacts | experiment manifest + pinned environment | clean rerun/artifact audit | rerun agreement, artifact completeness | Reproducibility evidence |

---

# 23. Architecture decision

## Selected

**Single-host Linux + native containers + eBPF syscall/process telemetry + ring buffer + common feature pipeline + user-space Logistic Regression, with a feasibility-gated fixed-point kernel-local LR variant + staged controlled enforcement.**

## Why selected

1. It directly maps to all five validated gaps.
2. It uses one primary telemetry modality, reducing confounding.
3. Logistic Regression provides a mathematically comparable model across user-space and kernel-local placement.
4. Native containers avoid unnecessary nested Kubernetes infrastructure.
5. Controlled enforcement allows RQ4 without exposing the host to uncontrolled blocking.
6. The design produces measurable event-loss and end-to-end latency rather than only model accuracy.
7. The experiment is reproducible on a student-feasible single machine.
8. A failure of kernel-local inference does not invalidate the whole project because the fallback is explicit.

## Alternatives rejected or deferred

- **GPU:** no RQ requires it.
- **Kafka/message broker:** adds buffering and network infrastructure that would confound the first latency study.
- **Kubernetes/kind:** deferred because nested/containerized orchestration is not necessary for the primary controlled test.
- **Deep neural network:** not justified before classical baselines establish a need.
- **Multimodal telemetry:** not justified by CHAT 05; it should be an ablation/extension only if later evidence requires it.
- **Continual learning framework:** not required because G2 is a distribution-shift evaluation gap, not an absence-of-continual-learning gap.
- **Autonomous enforcement:** rejected for safety reasons.
- **Full in-kernel Random Forest/XGBoost:** rejected as the primary placement comparator because it would confound model family/representation and increase verifier/deployment complexity.

---

# 24. CHAT 06 completion decision

**CHAT 06 — COMPLETE.**

Completion criteria satisfied:
- G1–G5 requirements traced.
- Alternatives compared.
- Minimum architecture selected with explicit rejection/deferment reasons.
- Hardware/software testbed specified.
- Telemetry and buffering design specified.
- Feature pipeline specified.
- ML candidates and placement protocol specified.
- Benign workloads specified.
- Safe anomaly/attack scenarios specified.
- Distribution-shift experiment specified.
- Staged enforcement and rollback specified.
- Baselines and ablations specified.
- Metrics specified.
- Statistical plan specified.
- Reproducibility specification specified.
- Feasibility gates and risks specified.
- Complete traceability matrix provided.

**No prototype implementation or final experiment has been performed in CHAT 06.**

---

# 25. Evidence and external technical references used for feasibility

The architectural feasibility statements were checked against current upstream documentation rather than assumed from model knowledge.

- Linux BPF documentation: https://kernel.org/doc/html/latest/bpf/
- Linux eBPF verifier documentation: https://docs.kernel.org/bpf/verifier.html
- Linux libbpf documentation: https://docs.kernel.org/bpf/libbpf/index.html
- Linux BPF ring buffer documentation: https://origin.kernel.org/doc/html/latest/bpf/ringbuf.html
- Linux BPF LSM documentation: https://cdn.kernel.org/doc/html/latest/bpf/prog_lsm.html
- Linux cgroup v2 documentation: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
- Ubuntu kernel documentation: https://ubuntu.com/kernel

These sources establish the available BPF/libbpf, verifier, ring-buffer, BPF-LSM and cgroup mechanisms. They do **not** establish experimental performance results; those must come from CHAT 08–10 measurements.

## Next phase

**CHAT 07 — Prototype Implementation / Experimental Infrastructure**

CHAT 07 must implement only the architecture that passed the CHAT 06 gates. It must not silently expand scope.
