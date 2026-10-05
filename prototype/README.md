# CHAT 07 Prototype / Experimental Infrastructure

This directory implements the minimum infrastructure frozen by CHAT 06.

## Scope

Pipeline: container workload -> eBPF syscall/process telemetry -> BPF ring buffer -> user-space event stream -> 1 s feature aggregation -> Logistic Regression -> risk decision -> staged policy -> experiment recorder.

The kernel-local fixed-point classifier is a feasibility-gated extension and is not part of the primary path until the user-space path and telemetry accounting are validated.

## Host requirements

The pinned baseline is Ubuntu 24.04 LTS x86-64 with the exact installed 6.8-series kernel package recorded by preflight. Required tooling includes Docker Engine, libbpf/libbpf-dev, bpftool, Clang/LLVM with BPF target support, a C compiler, Python 3 and the dependencies in requirements.txt.

## Quick start

1. cd prototype
2. bash preflight.sh
3. make -C bpf
4. ./bpf/telemetry_loader ./bpf/telemetry.bpf.o --duration 10 > run/events.jsonl
5. python3 -m python.smoke --events run/events.jsonl

## Workloads

B1 idle/service baseline; B2 synthetic file processing; B3 bounded process churn; B4 local client/server. Safe bounded anomaly scenarios are A1 process-execution burst, A2 abnormal synthetic-file access and A3 local connection burst. Example: python3 -m python.workloads B2 --duration 10 --seed 7. No external target is used.

## Validation order

1. preflight
2. BPF build/load
3. ring-buffer accounting
4. container/cgroup identity
5. feature aggregation
6. reference LR inference
7. policy state machine
8. reproducibility manifest
9. complete smoke path
10. kernel-local fixed-point LR feasibility gate

Final experiment matrices are deliberately outside CHAT 07.
