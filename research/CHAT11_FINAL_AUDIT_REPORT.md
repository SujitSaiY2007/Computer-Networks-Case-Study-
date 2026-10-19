# Chat 11 — Interim Final Experimental Audit Report

**Audit date:** 19 October 2026  
**Status:** PARTIAL — critical execution and bibliography checks remain blocked  
**Repository:** https://github.com/SujitSaiY2007/Computer-Networks-Case-Study-  
**Starting remote `main` HEAD:** `8576f5bb12515c28868e7e8cbdbc8b104efe0e1e`  
**Audit scope:** Remote repository inspection and source review through the connected GitHub integration.

## A. Executive summary

Chat 11 has established the starting remote `main` revision and inspected the active handoff, README, manuscript, claim-to-evidence map, matrix validator, descriptive-analysis script, experiment manifest, environment manifest, processed metric files, representative raw records, and literature-selection register.

This is not a completed experimental audit. The available session provides remote GitHub file and repository operations, but no checked-out repository or shell execution environment for running the Python scripts against the full raw dataset. Therefore, the validator, revised statistical analysis, processing scripts, plot regeneration, and native BPF tests have **not** been executed in this audit. The combined commit-status endpoint returned an empty status list; that is not evidence of a passing CI run.

**Submission-readiness decision: Outcome 3 — Not yet ready.** Critical validation, counter reconciliation, and bibliography verification remain incomplete. No raw JSON records were modified by this audit.

## B. Repository state

- Repository default branch: `main` (confirmed from remote repository metadata).
- Starting remote HEAD: `8576f5bb12515c28868e7e8cbdbc8b104efe0e1e`.
- Latest commit message: `docs(chat10): align master plan and handoff with audit queue`.
- Inspected manuscript: `paper/MAIN_MANUSCRIPT.md`.
- Inspected claim map: `research/CHAT10_CLAIM_TO_EVIDENCE_MAP.md`.
- Inspected scripts: `experiments/scripts/validate_matrix.py`, `experiments/scripts/statistical_analysis.py`, `experiments/scripts/process_results.py`, `experiments/scripts/compute_stats.py`, and `experiments/scripts/generate_plots.py`.
- Inspected manifests: `experiments/manifests/experiment_matrix_manifest.json` and `experiments/manifests/env_manifest.json`.
- Inspected processed files: `summary_metrics.json`, `detection_performance.csv`, `summary_by_configuration.csv`, and `latency_breakdown.csv`.
- Representative records inspected: `run_C_A1_rep0.json`, `run_D_A1_rep0.json`, and `run_E_A1_rep0.json`.
- No additional branch was created or used by this audit. The remote metadata confirms `main` is the default branch; local branch/worktree state cannot be inspected from this session.
- Raw records were not changed by this audit. A full before/after raw-file hash comparison was not possible.

## C. Validation commands and execution status

The following commands are required by the project protocol but **were not run** because this session has no local checkout/shell execution access:

| Command | Result | Reason |
|---|---|---|
| `python experiments/scripts/validate_matrix.py` | BLOCKED — not executed | No shell against a checked-out repository/raw dataset |
| `python experiments/scripts/statistical_analysis.py` | BLOCKED — not executed | Same environment limitation |
| `python experiments/scripts/process_results.py` | BLOCKED — not executed | Derived outputs cannot be safely regenerated remotely through file inspection alone |
| `python experiments/scripts/compute_stats.py` | BLOCKED — not executed | Same environment limitation |
| `python experiments/scripts/generate_plots.py` | BLOCKED — not executed | Figures were not regenerated |
| `./prototype/tests/run_unit_tests.sh` | BLOCKED — not executed | Native/project test environment unavailable |
| BPF feasibility/native checks | BLOCKED — not executed | Requires the documented Linux/BPF environment or an actual CI run |

GitHub combined commit status queried for the starting SHA returned an empty status list. This means no status entries were returned by that endpoint; it does **not** mean CI passed.

## D. Evidence and discrepancies found by static inspection

### D1. Matrix and validator

The manifest specifies 5 configurations × 7 workloads × 10 repetitions = 350 records. Three representative raw records match the documented JSON nesting for identifiers, resources, telemetry, latency, classification, and enforcement. These samples do not prove full matrix completeness.

Static review of `validate_matrix.py` found:
- It prints an “AUDIT PASS” banner before validating the records.
- It checks the expected record count, tuple uniqueness, cell counts, ground-truth labels, and per-record classification breakdowns.
- It computes its reported loss indicator only from reservation failures plus sequence gaps divided by generated events; it does not reconcile generated, submitted, and consumed totals.
- It uses `assert` for some integrity checks and defaults missing classification/counter values to zero in places, so missing fields may not be reported as clearly as required by the audit protocol.
- It does not visibly compare the actual records against the manifest's full required-field/type specification.

These are code-review observations, not an executed validator result. The validator should be revised only after schema and raw-data checks can be run in an appropriate environment.

### D2. Descriptive analysis

The replacement `statistical_analysis.py` correctly avoids unsupported confirmatory tests and checks expected matrix tuples before summarizing. It reports per-cell duration means, medians, an IQR-like spread, RSS means, inference timing, and generated/submitted/consumed counter totals. It has not been executed.

The script's IQR helper uses selected order-statistic indices rather than a documented standard quartile convention. This should be explicitly defined and applied consistently before the values are described as IQR.

### D3. Processed-output mismatch

The committed `experiments/processed/summary_by_configuration.csv` reports Configuration D mean inference timing as **4.238 μs**. The manuscript abstract and claim-to-evidence map report **4.19 μs**. The committed table alone does not establish which figure is correct against raw observations. Regenerate from raw records and reconcile this discrepancy before publication. Do not silently choose one value.

The committed detection CSV supports these processed counts: A1 has 7 TP and 3 FN in each of C/D/E; B3 FPR is 80% for C, 50% for D, and 80% for E; A2 has 0/10 detections in C/D and 2/10 in E; A3 has 0/10 detections in C/D/E. These are inspected processed-file values, not independently recomputed full-dataset results.

### D4. Telemetry accounting

The project documents report 16,001 generated versus 15,999 submitted events, with zero reservation failures and sequence gaps. The new analysis script includes a consumed counter, but no execution output was obtained to establish its aggregate. The discrepancy remains **unresolved**. The existing validator's zero indicator is based on reservation failures and sequence gaps and cannot by itself establish end-to-end zero loss.

Safe manuscript wording pending reconciliation:

> Across the instrumented runs, the recorded counters report 16,001 generated events and 15,999 submitted events, with no recorded reservation failures or sequence gaps. The two-event discrepancy and the aggregate generated/submitted/consumed relationship remain unresolved; therefore, these records do not establish end-to-end zero event loss.

### D5. Architecture and environment

The manuscript and claim map distinguish Python floating-point/scikit-learn timing from Python Q16.16 arithmetic, formula-derived latency estimates from direct end-to-end measurements, and simulated policy-state changes from live OS enforcement. They also state that the 350-run matrix did not demonstrate a live kernel-local ML inference loop or a UI/dashboard. These distinctions are appropriate but have not been verified against all implementation code and test logs in this pass.

The environment manifest records Ubuntu 24.04.3 LTS under WSL2, kernel `6.6.87.2-microsoft-standard-WSL2`, Python 3.12.3, and a `git_sha` of `66512d8efdf5e16a8a8e9c3edd65534681b3bbfd`, with branch recorded as `feat/chat07-native-validation`. The manifest's own notes describe this as a Chat 07 runtime capture. Its provenance relative to the Chat 08 experiment timestamp must remain explicit; the manifest must not be represented as proving every listed tool was exercised by every matrix configuration.

## E. Bibliography audit

The manuscript reference list visibly contains abbreviated author fields such as “Her, et al.”, “Kim, et al.”, “Lu, et al.”, “Remya, et al.”, “Ryu, et al.”, “Soldani, et al.”, “Taguchi, et al.”, “Zehra, et al.”, and “Zhan, et al.” Several entries also omit volume, issue, page/article details, or DOI/official URLs. The manuscript itself labels the list a working subset and asks for verification.

The approved Review 2 register distinguishes 40 primary studies from 10 supporting/background references (50 total). The count distinction is documented, but the manuscript's citations have **not** been individually verified against original publisher/proceedings records, retraction/correction status, or citation-to-claim support in this pass. No bibliography entry should be treated as fully verified yet.

## F. Required manuscript and documentation corrections

1. Reconcile Configuration D inference timing (4.19 μs in manuscript/map versus 4.238 μs in the committed configuration summary) by executing the raw-data pipeline.
2. Keep telemetry end-to-end loss unresolved until generated, submitted, and consumed totals are reconciled.
3. Expand and verify abbreviated author lists and publication metadata from official sources; verify every in-text citation and attributed claim.
4. Update stale status statements in README/experiment documentation that still describe Chat 10 as the next phase or Configuration D as directly measured kernel-local inference.
5. Correct the validator's premature PASS banner and strengthen required-field, counter, and manifest checks only after executing the test suite against the real data.
6. Document the chosen IQR/quartile convention in the descriptive-analysis script.
7. Regenerate processed outputs and figures and compare them with committed artifacts before claiming they are current.

No numerical manuscript edits were made because the required raw-data regeneration and validation could not be executed.

## G. Acceptance criteria

| ID | Status | Evidence / reason |
|---|---|---|
| A1 Repository state established | PARTIAL | Remote default branch and full starting SHA confirmed; local worktree/branch status unavailable |
| A2 Experimental matrix validated | BLOCKED | Validator not executed against all raw files |
| A3 Revised analysis executed | BLOCKED | Analysis script not executed |
| A4 Derived outputs reconciled | BLOCKED | Processing/figures not regenerated; D timing mismatch remains |
| A5 Telemetry accounting audited | PARTIAL | Counter definitions and code inspected; aggregate consumed count not obtained and discrepancy unresolved |
| A6 Detection metrics verified | PARTIAL | Processed CSV and representative raw records inspected; full raw recomputation not executed |
| A7 Architecture claims verified | PARTIAL | Manuscript and evidence map inspected; complete implementation/test-path verification not executed |
| A8 Bibliography audited | BLOCKED | Abbreviated entries identified; original-source verification incomplete |
| A9 Manuscript corrected | PARTIAL | Material inconsistency identified; no unverified numerical correction made |
| A10 Reproducibility assessed | PARTIAL | Manifests and scripts inspected; execution chain not reproduced |
| A11 Git state verified | PARTIAL | Starting remote SHA confirmed; this report's final commit/remote SHA must be verified after publication |
| A12 Handoff completed | PARTIAL | This report records interim state; next-phase instructions must retain blockers |

## H. Unresolved limitations and next steps

1. Obtain a shell/checkout or CI runner with the repository and its raw records. Keep the branch on `main`; do not create another branch.
2. Run the validator, analysis, processing, plot generation, and applicable tests; capture actual output and exit codes.
3. Reconcile all telemetry counters from raw records, including generated, submitted, and consumed counts.
4. Regenerate outputs, resolve the 4.19/4.238 μs discrepancy, and compare each generated artifact against committed files.
5. Verify all bibliography entries against official publication records and audit citation/reference consistency.
6. Fix justified code/documentation defects, inspect the complete diff, commit directly to `main`, and verify the final remote SHA.
7. Do not describe the manuscript as submission-ready until the critical criteria pass.

## I. Chat 12 handoff

Chat 12 may prepare a presentation of the **currently supported, explicitly qualified** findings and the unresolved audit state, but must not describe the work as fully validated or submission-ready. If the submission package requires validated results, prioritize the blocked Chat 11 execution and bibliography tasks first. Preserve raw records, historical artifacts, the existing branch history, and the main-branch-only workflow. Do not repeat the experiment matrix unless the audit demonstrates a specific reason and the project workflow authorizes it.
