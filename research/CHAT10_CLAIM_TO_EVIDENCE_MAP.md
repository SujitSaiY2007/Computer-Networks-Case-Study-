# Chat 10 — Claim-to-Evidence Map and Final Audit Queue

**Main SHA inspected:** c55bfeec9a146a08c5a544d81a763021d9258ebb  
**Status:** Drafted for Chat 11 audit; repository validation commands were not executed during this authoring pass.

## Claim-to-evidence map

| Manuscript claim | Evidence location | Evidence class | Caveat |
|---|---|---|---|
| 350 records, 35 cells, 10 records per cell | experiments/raw/run_*.json; experiments/scripts/validate_matrix.py; experiments/manifests/experiment_matrix_manifest.json | Matrix structure/raw records | Run validator before submission |
| Mean durations approximately A 0.8199 s, B 0.8214 s, C 0.8204 s, D 0.8211 s, E 0.8204 s | experiments/processed/summary_metrics.json, seven workload cell means per configuration | Derived descriptive summary | Confirm processing convention by regenerating outputs |
| Reported mean slowdown A 0.00%, B 0.19%, C 0.09%, D 0.16%, E 0.06% | experiments/processed/summary_metrics.json | Derived descriptive summary | Specific workloads and WSL2 environment only |
| Mean host-process RSS A 93.18 MB, B 93.53 MB, C/D 93.63 MB, E 93.73 MB | experiments/processed/summary_metrics.json; experiments/processed/summary_by_configuration.csv | Process-level resource observation | Not pure kernel memory overhead |
| 16,001 generated events and 15,999 submitted events | README.md; status and Chat 09 integrity report; experiments/raw/run_*.json telemetry fields | Counter totals | Two-event discrepancy remains unresolved |
| Zero reservation failures and sequence gaps | experiments/scripts/validate_matrix.py; experiments/raw/run_*.json | Counter-derived indicator | Does not prove reconciled end-to-end zero loss |
| A1: 7 TP, 3 FN; precision 1.00, recall 0.70, F1 about 0.824 | experiments/processed/detection_performance.csv; summary_metrics.json; raw records | Classification counts | Specific model/workload only |
| B3: 5/10 to 8/10 false positives; 50–80% FPR | experiments/processed/detection_performance.csv; raw records | Classification counts | Major operational limitation |
| A2 misses in C/D and 2/10 detected in E | experiments/processed/detection_performance.csv | Classification counts | Verify metrics during final audit |
| A3 recall zero in C/D/E | experiments/processed/detection_performance.csv; raw records | Classification counts | Held-out connection-burst workload only |
| 169.20 μs vs 4.19 μs average inference timing | experiments/processed/summary_by_configuration.csv; summary_metrics.json; experiments/scripts/run_experiments.py | Software benchmark | Python float/scikit-learn vs Python Q16.16; not kernel-vs-user-space |
| Approx. 40.4× mean ratio | Same as above | Derived ratio | Not in-kernel speedup |
| C detection delay about 1.567 ms and D about 0.085 ms | experiments/scripts/run_experiments.py; raw latency fields | Formula-derived estimate | Assumed constants; not one continuous clock interval |
| Mitigation about 1.17 ms and rollback about 15 μs | run_experiments.py; latency_breakdown.csv; raw records | Simulation | Python policy transitions and synthetic sleep; no cgroup freeze/firewall actuation |
| Gate G verifier feasibility | prototype/bpf/kernel_lr_feasibility.bpf.c; prototype/tests/test_kernel_lr_feasibility.py; research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md | Feasibility test | Not proof of live matrix inference in kernel |
| WSL2 kernel 6.6.87.2 deviation | experiments/manifests/env_manifest.json; research/CHAT07_IMPLEMENTATION_AND_VALIDATION.md | Environment record | Disclose against originally intended 6.8-series kernel |
| Literature count 40 primary + 10 supporting = 50 references | review2/REVIEW2_50_PAPER_LITERATURE_TABLE.md; research/REVIEW2_PAPER_SELECTION_AND_AUDIT.md | Approved literature record | Keep counts distinct |

## Statistical-method correction

The previous experiments/scripts/statistical_analysis.py paired C and D by workload ID and repetition index and ran paired tests. It also ran a pooled one-way ANOVA on durations and interpreted non-significance as confirming negligible overhead. The manuscript does not retain these inferential claims because matching labels alone do not prove a paired design, separate sequential executions can have run-order effects, formula-derived latency includes assumed constants, and a non-significant ANOVA is not an equivalence test.

The replacement analysis script is intended to provide workload-stratified descriptive summaries and counter reconciliation without unsupported confirmatory p-values. It has not been executed in this authoring pass. Chat 11 must run it and verify its outputs against immutable raw records.

## Mandatory Chat 11 checks

- Run python experiments/scripts/validate_matrix.py.
- Run the revised experiments/scripts/statistical_analysis.py.
- Regenerate summaries with the established processing command documented in experiments/README.md and compare them with committed outputs without changing raw JSON.
- Reconcile generated/submitted/consumed event counts and document every counter definition; otherwise retain the unresolved caveat.
- Verify all 350 records, 35 cells, ten records per cell, warnings, and exclusions.
- Ensure no stale 77,598-event claim remains in manuscript text.
- Complete every abbreviated reference from the approved register; verify author list, title, venue, year, DOI/official URL.
- Check one-to-one citation/reference consistency.
- Verify branch main, capture full local and remote HEAD SHAs, inspect the diff, and report actual validation outcomes.
- Do not claim a UI/dashboard exists, production readiness, live OS enforcement, zero end-to-end loss, or measured in-kernel speedup.
