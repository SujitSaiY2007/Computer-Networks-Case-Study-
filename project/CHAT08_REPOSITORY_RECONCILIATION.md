# Chat 08 Repository Reconciliation and Chat 09 Entry Gate

**Date:** 13 October 2026  
**Repository:** `SujitSaiY2007/Computer-Networks-Case-Study-`  
**Canonical branch from this point forward:** `main`

## Why this record exists

A Chat 08 final summary supplied in the conversation reports 350 runs across 35 configuration/workload cells, processed CSVs and figures, and commit abbreviation `5732f2f`. During direct GitHub inspection, the repository's recent commit search returned the older Chat 07 merge as the latest commit; the supplied SHA abbreviation did not resolve; and the reported Chat 08 report and processed CSVs could not be retrieved from `main`. The currently visible handoff and README also still describe Chat 08 as next. This is a mismatch between the conversation summary and the remotely visible repository state.

**Interpretation:** this is a synchronization/provenance discrepancy. It does not prove the experiment work never existed or that local files are lost. It does mean that ChatGPT cannot honestly claim the Chat 08 implementation/results are committed and independently verified on GitHub yet.

## Authoritative decisions

1. All future project work is done directly on `main`; no feature branches for new work.
2. Preserve `feat/chat07-native-validation` and all historical branches/files. Do not delete, force-push, reset, rebase, or rewrite history.
3. Do not rerun all 350 experiments until local repository and AG workspace have been inspected.
4. Raw run files are immutable evidence. Never synthesize missing JSON or alter raw records to match a claimed count.
5. A reported summary is not accepted as verified evidence until scripts, raw records, manifests, report, and full commit SHA are present and inspectable on GitHub.
6. Frozen literature counts remain 40 primary studies (36 journals + 4 peer-reviewed conferences) and 50 Review 2 references (40 primary + 10 supporting/background). Review 1 and Review 2 are complete.

## AG/Antigravity recovery checklist

Run from the existing project checkout and report actual output before changing anything:

```bash
git status --short --branch
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git log --oneline --decorate --all -30
git reflog --all --date=iso -30
git branch -avv
git ls-remote origin refs/heads/main
find experiments -maxdepth 4 -type f -print 2>/dev/null | sort
find . -type f \( -name 'run_*.json' -o -name '*CHAT08*' -o -name '*summary*.csv' -o -name '*latency*.csv' \) -print 2>/dev/null | sort
git status --short --ignored experiments
```

Also inspect the AG workspace and local-only branches/commits. Do not print secrets or unrelated private file contents. Determine whether the claimed 350-run data is tracked, untracked, ignored, in another local branch, or absent. Identify the full 40-character commit SHA corresponding to the claimed short SHA if one exists.

If valid artifacts exist locally, verify run coverage and provenance before staging. Compare the expected 5 configurations × 7 workloads × 10 repetitions (35 cells, 350 runs) against actual raw files; record any design-specific exclusions, failed runs, duplicate/missing IDs, seed mismatches, or schema problems. Re-run processing scripts from raw JSON and compare outputs; check timing definitions, event-loss denominators, model split/calibration separation, confusion matrices and metric averaging, mitigation/rollback denominators, and plots. Do not silently correct inconsistencies: document them and preserve original raw data. Then commit all appropriate files directly to `main`, push normally, and verify remote HEAD and exact file URLs.

If local artifacts are not found, report the searches performed and the exact missing artifacts. Recover only from a verified source/backup. Do not fabricate the matrix or mark Chat 08 complete merely from its narrative summary.

## Chat 09 acceptance criteria

Chat 09 empirical synthesis may begin only after the recovery gate passes. It must:

- Recompute metrics from immutable raw records using versioned scripts.
- Audit all applicable A–E × B1–B4/A1–A3 cells, run counts, seeds, exclusions, and denominators.
- Report central tendency and variability; use confidence intervals/effect sizes only when statistically appropriate and explain the unit of analysis.
- Validate claims of <0.20% slowdown, +0.35–0.55 MB RSS, zero telemetry loss, 169.20 μs versus 4.24 μs inference, 1.57 ms versus 0.085 ms detection, 1.16 ms containment, 2.61 ms total response, 0.016 ms rollback, F1 0.824, B3 FPR 50–80%, A3 recall 0%, and zero benign-operation impact. Treat every number as a hypothesis to verify, not a fact to force the data to match.
- Check whether the approximately 40× ratio is supported by comparable timing boundaries and distributions; don't infer universal superiority from mean-only comparisons.
- Distinguish an observed false-alarm result on B3 from a general claim of concept drift. Explain A3 as failure on the specified held-out workload, not proof of all zero-day evasion.
- Connect verified findings to frozen research questions and literature evidence, keeping direct measurements, cited-study claims, synthesis, and interpretation distinct.
- Update experiment report, reproducible tables/figures, README, handoff, status correction, and master plan; commit and verify on `main`.

## Role split

**AG/Antigravity:** inspect local machine/repository state; recover existing work; execute shell/Git commands; validate files and scripts; regenerate derived outputs from raw data; commit/push directly to `main`; return exact command output, full SHAs, changed paths, and validation results.

**ChatGPT:** direct the audit; inspect source/report/data where accessible; challenge statistical assumptions and unsupported claims; review the reproduced outputs; synthesize the results section, limitations, literature connection, and manuscript-ready text; ensure handoff and provenance consistency. ChatGPT must not claim it executed local commands or saw files it could not access.

## Start-of-chat and end-of-chat provenance ledger

Every future chat must record:

- Canonical branch: `main`
- Full local HEAD SHA
- Full remote `origin/main` SHA
- Working-tree status (clean/dirty)
- Last commit message
- Exact artifact paths and GitHub URLs
- Validation commands and their actual exit/results
- Any unresolved mismatch and the next action

If local and remote HEAD differ, stop and reconcile before editing. A task is complete only when the deliverables are committed, pushed, and verified at the exact remote SHA.
