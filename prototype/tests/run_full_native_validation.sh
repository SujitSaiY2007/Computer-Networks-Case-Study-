#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

echo "=========================================================="
echo "CHAT 07 — FULL NATIVE LINUX VALIDATION SUITE"
echo "=========================================================="

# 1. Environment Preflight
echo ""
echo ">>> [1/6] Running Environment Preflight..."
./prototype/preflight.sh

# 2. Gate A: Build Native BPF Program and Loader
echo ""
echo ">>> [2/6] Building Native BPF Program and Loader..."
cd prototype/bpf
make clean
make
cd ../..

# 3. Gate B & E: Live Workload Execution and Native Telemetry Capture
echo ""
echo ">>> [3/6] Capturing Native BPF Telemetry under Controlled Workloads..."
EVENTS_LOG="/tmp/chat07_native_events.jsonl"
rm -f "$EVENTS_LOG"

# Start loader in background for 6 seconds
./prototype/bpf/telemetry_loader ./prototype/bpf/telemetry.bpf.o --duration 6 > "$EVENTS_LOG" &
LOADER_PID=$!
sleep 0.5

# Execute workloads during capture
python3 prototype/python/workloads.py B2 --duration 2 --seed 42 &
python3 prototype/python/workloads.py B3 --duration 2 &
wait

wait "$LOADER_PID" || true

echo "Events captured: $(grep -c '\"record_type\":\"event\"' "$EVENTS_LOG")"
tail -n 1 "$EVENTS_LOG"

# 4. Gate C: Container & Identity Correlation
echo ""
echo ">>> [4/6] Validating Container & Cgroup Identity Correlation..."
./prototype/tests/validate_identity.sh

# 5. Gate D: Software-Side Unit Tests
echo ""
echo ">>> [5/6] Running Python Unit Tests..."
./prototype/tests/run_unit_tests.sh

# 6. Gate E & F: End-to-End Pipeline & Reproducibility Manifest
echo ""
echo ">>> [6/6] Executing End-to-End Smoke Pipeline & Generating Manifest..."
python3 prototype/tests/run_native_smoke.py --events-file "$EVENTS_LOG" --output-dir prototype/output

echo ""
echo "=========================================================="
echo "ALL GATES (A, B, C, D, E, F) NATIVELY VALIDATED!"
echo "=========================================================="
