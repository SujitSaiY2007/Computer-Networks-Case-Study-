#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

rm -f /tmp/capture.jsonl /tmp/loader.err

sudo prototype/bpf/telemetry_loader prototype/bpf/telemetry.bpf.o --duration 6 > /tmp/capture.jsonl 2> /tmp/loader.err &
LOADER_PID=$!

# Wait until the loader prints TELEMETRY_RUNNING on stderr (not a fixed sleep)
TIMEOUT=5
ELAPSED=0
while ! grep -q "TELEMETRY_RUNNING" /tmp/loader.err 2>/dev/null; do
    if ! kill -0 $LOADER_PID 2>/dev/null; then
        echo "Loader exited unexpectedly:" >&2
        cat /tmp/loader.err >&2
        exit 1
    fi
    sleep 0.05
    ELAPSED=$((ELAPSED + 1))
    if [ $ELAPSED -ge 100 ]; then
        echo "Timed out waiting for TELEMETRY_RUNNING" >&2
        kill $LOADER_PID 2>/dev/null || true
        exit 1
    fi
done

# Run 100 execs
for i in $(seq 1 100); do
    /bin/true
done

# Wait for loader to exit
wait $LOADER_PID 2>/dev/null || true

# Count lines with "event_type":1 and print count plus stats line
EXECVE_COUNT=$(grep -c '"event_type":1' /tmp/capture.jsonl || true)
echo "execve count: $EXECVE_COUNT"
STATS_LINE=$(grep '"record_type":"stats"' /tmp/capture.jsonl || true)
echo "stats: $STATS_LINE"

if [ "$EXECVE_COUNT" -ge 100 ]; then
    echo "PASS"
    exit 0
else
    echo "FAIL"
    exit 1
fi
