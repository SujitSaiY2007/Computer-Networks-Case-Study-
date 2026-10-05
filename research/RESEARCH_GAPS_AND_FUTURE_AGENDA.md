# Evidence-Based Research Gaps and Future Agenda

## Project focus
**eBPF-Assisted Machine Learning for Cloud-Native Runtime Security: Telemetry Overhead, Kernel Enforcement, and Detection Trade-offs**

The gaps below are written as evidence-backed hypotheses for the literature review. They are not claims that “nothing exists.” Existing technologies already cover substantial portions of the pipeline; the gaps concern integration, evaluation consistency, robustness, safety and deployment evidence.

## 1. Gap: fragmented telemetry rather than a common multimodal representation

**Existing technologies:** eBPF syscall tracing, file-access tracing, flow/XDP telemetry, Tetragon, Falco, Tracee, kernel audit mechanisms, and hybrid host/network approaches.

**Evidence pattern:** Some studies focus on syscall sequences, some on network flows, some on file access, and a smaller subset combines host and network telemetry. Hybrid work shows that different modalities capture different behavioural information.

**Why it matters:** A model trained on one telemetry modality may miss attacks whose strongest evidence appears in another layer. At the same time, collecting every event increases CPU, memory, buffering and event-processing cost.

**Future direction:** Build a controlled multimodal telemetry pipeline in which syscall, file and network events can be activated at different granularities. Measure how detection changes as telemetry richness increases.

**Evaluation needed:** detection quality, event rate, CPU, memory, buffer occupancy/event loss and end-to-end latency.

---

## 2. Gap: ML detection is often attack-specific or dataset-specific

**Existing technologies:** Decision trees, Random Forest, SVM, AdaBoost/XGBoost, autoencoders, VAE/iForest, LSTM and other classifiers are already used with eBPF-derived data.

**Evidence pattern:** Many studies evaluate a small number of named attacks or a limited set of benign/malicious containers. High accuracy is often reported under the same workload distribution used for development/evaluation.

**Why it matters:** A high accuracy value on one dataset does not establish robustness under new workloads, new containers, concept drift or previously unseen attacks.

**Future direction:** Evaluate temporal and workload distribution shift. Separate training workloads from evaluation workloads and include unseen attack classes where the method permits it.

**Evaluation needed:** cross-workload accuracy, precision, recall, F1, false-positive rate, calibration, temporal robustness and degradation under distribution shift.

---

## 3. Gap: in-kernel ML versus user-space ML is not yet a settled design choice

**Existing technologies:** In-kernel eBPF/XDP inference, AF_XDP, user-space inference, hybrid eBPF capture + user-space ML, model quantization and tail-call based model decomposition.

**Evidence pattern:** In-kernel inference can reduce context switching/data movement but is constrained by verifier rules, instruction complexity, stack limits, supported arithmetic and maintainability. User-space inference permits richer models but can add transfer and inference latency.

**Why it matters:** The correct placement depends on model complexity, traffic/event rate and security objective.

**Future direction:** Implement at least two placements—(1) eBPF telemetry + user-space ML and (2) lightweight/quantized in-kernel inference—and compare them under identical workloads.

**Evaluation needed:** inference latency, throughput, CPU, memory, model size, event loss and detection quality.

---

## 4. Gap: telemetry overhead is not measured under a common benchmark

**Existing technologies:** eBPF tracing, perf/audit-style monitoring, Tetragon/Falco/Tracee and specialized eBPF security agents.

**Evidence pattern:** Studies report overhead using different workloads, event rates, hardware, numbers of containers and metrics. This makes direct comparison difficult.

**Why it matters:** “Low overhead” is not a universal property; overhead can change substantially with event frequency, hook type and workload intensity.

**Future direction:** Define a common benchmark matrix with baseline, low-telemetry, high-telemetry, ML-only and ML+enforcement configurations.

**Evaluation needed:** CPU utilization, memory, event throughput, dropped events, application latency, network throughput and detection latency.

---

## 5. Gap: detection is better studied than safe autonomous enforcement

**Existing technologies:** BPF-LSM, eBPF maps, XDP, Seccomp, KubeRosy, BPFGuard, Cordon, Optimus, KubeAegis and related policy systems.

**Evidence pattern:** Several systems demonstrate enforcement, but the evidence is less standardized around false-positive consequences, rollback, policy conflict, explainability and safe recovery.

**Why it matters:** A false positive in runtime security can terminate a legitimate workload or block a required syscall/network operation.

**Future direction:** Introduce a staged response policy: observe → score → alert → enforce. Add rollback or fail-open/fail-safe policy controls and measure detection-to-mitigation latency.

**Evaluation needed:** false positives, blocked legitimate operations, mitigation latency, recovery time, policy conflicts and failure behaviour.

---

## 6. Gap: adversarial robustness of eBPF+ML security pipelines is under-evaluated

**Existing technologies:** ML classifiers and anomaly detectors are increasingly combined with eBPF telemetry, but the security of the model/feature pipeline is not always tested against deliberate evasion.

**Why it matters:** An attacker who knows which telemetry is monitored may attempt to modify behaviour so that the model remains below its detection threshold.

**Future direction:** Test evasion against feature-level and behaviour-level perturbations while preserving legitimate workload functionality.

**Evaluation needed:** attack success rate, detection degradation, false positives, robustness across model updates and overhead of defensive measures.

---

## 7. Gap: eBPF's own security and verifier constraints need to be part of the security model

**Existing technologies:** eBPF verifier, LSM, hardware-assisted isolation, permission controls and research on eBPF attack surfaces.

**Evidence pattern:** eBPF is both a defensive mechanism and a privileged kernel programmability layer. Treating eBPF as automatically safe would ignore its own attack surface and verifier limitations.

**Why it matters:** A runtime-security architecture is not trustworthy if the security mechanism itself introduces an unmanaged privilege or isolation risk.

**Future direction:** Include a threat model for the eBPF subsystem and record verifier, privilege, kernel-version and program-loading assumptions in the evaluation.

**Evaluation needed:** verifier acceptance constraints, privilege boundaries, kernel-version portability, attack surface and failure behaviour.

---

## 8. Gap: portability across kernel versions and environments

**Existing technologies:** libbpf, BCC, CO-RE, tracepoints, kprobes, BPF-LSM, XDP and different container runtimes/CNIs.

**Evidence pattern:** A prototype may work on one Linux/kernel configuration but require changes elsewhere.

**Why it matters:** Cloud-native deployments are heterogeneous and upgraded frequently.

**Future direction:** Test the prototype across more than one kernel version or clearly document a pinned kernel/testbed and portability constraints.

**Evaluation needed:** deployment success, verifier compatibility, hook availability, performance variance and maintenance effort.

---

## 9. Gap: reproducibility is weaker than capability reporting

**Existing technologies:** Open-source runtime-security tools and some research prototypes provide code, while other studies provide only high-level architecture or limited configuration details.

**Why it matters:** Without code, traces, configurations and exact attack scenarios, independent researchers cannot reproduce overhead or detection claims.

**Future direction:** Publish the project's eBPF programs, ML training/inference code, container images, configurations, attack scripts and raw evaluation results where legally and ethically possible.

**Evaluation needed:** artifact completeness, repeatability of reported metrics and sensitivity to configuration changes.

---

## 10. Gap: no single evaluation framework connects capability, efficiency and safety

**Existing technologies:** Existing papers commonly emphasize one of detection accuracy, throughput, enforcement or monitoring overhead.

**Why it matters:** A security mechanism can have excellent detection accuracy but unacceptable CPU cost or unsafe false-positive behaviour.

**Future direction:** Use a unified evaluation framework with five dimensions:

1. **Capability** — Can attacks be detected?
2. **Reliability** — Does performance remain stable across runs/workloads?
3. **Robustness** — Does detection survive workload/attack distribution shift?
4. **Safety** — Can enforcement cause unacceptable legitimate-workload failures?
5. **Efficiency** — What are CPU, memory, event-processing and latency costs?

This directly supports the project's intended contribution and avoids reducing the review to an accuracy leaderboard.

---

# Proposed solution direction for the project

The literature suggests that the most defensible project direction is a **controlled, modular prototype** rather than claiming a completely new security technology.

```text
Kubernetes / Container Workloads
            |
            v
     eBPF Telemetry Layer
   /         |          \
 syscalls   files       network
   \         |          /
            v
     Feature Extraction
            |
            v
       ML Detection
            |
      +-----+------+
      |            |
   benign      suspicious
                   |
                   v
          Policy / Risk Score
                   |
                   v
        Kernel Enforcement
          (BPF-LSM/XDP/etc.)
                   |
                   v
            Mitigation
```

## Recommended experimental comparisons

| Configuration | Purpose |
|---|---|
| Baseline container | Establish application/network cost without security monitoring |
| eBPF telemetry only | Measure pure observability overhead |
| eBPF + user-space ML | Measure practical hybrid detection |
| eBPF + lightweight in-kernel ML | Study placement/latency trade-off |
| eBPF + ML + enforcement | Measure detection-to-mitigation behaviour |
| Low vs high telemetry | Quantify telemetry richness versus overhead |

## Recommended metrics

**Detection:** precision, recall, F1, false-positive rate, attack detection rate.  
**Performance:** CPU, memory, throughput, application latency.  
**Telemetry:** events/sec, buffer occupancy, dropped events.  
**Response:** inference latency, detection latency, detection-to-mitigation latency.  
**Safety:** legitimate operations blocked, recovery/rollback behaviour.  
**Reproducibility:** code/data/configuration/artifact availability.

## Priority order for future work

1. Standardized telemetry + performance benchmark.
2. Hybrid host/network ML detection.
3. Distribution-shift and unseen-attack evaluation.
4. Safe staged kernel enforcement.
5. In-kernel versus user-space ML placement comparison.
6. Adversarial robustness.
7. Portability and reproducibility.

This priority order should be refined after the final full-text extraction matrix is completed; it is not yet a final conclusion.


## CHAT 04 preliminary synthesis pointer — 5 October 2026

CHAT 04 completed the cross-paper synthesis. The following observations are explicitly **preliminary / candidate observations**, not frozen final gaps: fragmented end-to-end latency measurement; narrower robustness/drift evidence than within-scenario detection evidence; under-standardized event-loss/buffering measurement; less standardized safe-enforcement evaluation; heterogeneous ML-placement comparisons; and reproducibility dependencies on kernel/runtime/configuration artifacts.

The authoritative synthesis is `research/CHAT04_CRITICAL_SYNTHESIS.md`. CHAT 05 must validate, consolidate, reject or refine these observations before any final research-gap claim is adopted.
