# CHAT 07 Prototype / Experimental Infrastructure

This directory implements the minimum infrastructure frozen by CHAT 06.

## Scope

Pipeline:

container workload -> eBPF syscall/process telemetry -> BPF ring buffer -> user-space event stream -> 1 s feature aggregation -> Logistic Regression -> risk decision -> staged policy -> experiment recorder.

The kernel-local fixed-point classifier is intentionally a feasibility-gated extension and is not part of the primary path until the user-space path and telemetry accounting are validated.

## Host requirements

The pinned baseline is Ubuntu 24.04 LTS x86-64 with the exact installed 6.8-series kernel package recorded by the preflight script. Required tooling includes Docker Engine, libbpf/libbpf-dev, bpftool, Clang/LLVM with BPF target support, a C compiler, Python 3 and the Python dependencies in `requirements.txt`.

## Quick start

```bash
cd prototype
./preflight.sh
make -C bpf
./bin/telemetry_loader ./bpf/telemetry.bpf.o --duration 10 > run/events.jsonl
python3 -m python.smoke --events run/events.jsonl
```

The loader requires the privileges/capabilities reported by preflight. It attaches only to the declared syscall tracepoints and does not collect command lines, paths or payloads.

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
10. kernel-local fixed-point feasibility gate

Final experiment matrices are deliberately outside CHAT 07.
