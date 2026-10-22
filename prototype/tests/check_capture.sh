#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

CGROUP_DIR="/sys/fs/cgroup/cncs_test"
FIFO="/tmp/capture_fifo.$$"
rm -f /tmp/capture.jsonl /tmp/loader.err "$FIFO"
mkfifo "$FIFO"

cleanup() {
    sudo kill -TERM $LOADER_PID 2>/dev/null || true
    rm -f "$FIFO"
    sudo rmdir "$CGROUP_DIR" 2>/dev/null || true
}
trap cleanup EXIT

# 1. Create test cgroup
sudo mkdir -p "$CGROUP_DIR"

# 2. Start loader with FIFO as stdin
sudo prototype/bpf/telemetry_loader prototype/bpf/telemetry.bpf.o --cgroup "$CGROUP_DIR" --max-seconds 10 < "$FIFO" > /tmp/capture.jsonl 2> /tmp/loader.err &
LOADER_PID=$!

# Keep FIFO open
exec 3> "$FIFO"

# 3. Wait until loader prints {"r":"ready"} on stdout
TIMEOUT=100
ELAPSED=0
while ! grep -q '"ready"' /tmp/capture.jsonl 2>/dev/null; do
    if ! kill -0 $LOADER_PID 2>/dev/null; then
        echo "Loader exited unexpectedly:" >&2
        cat /tmp/loader.err >&2
        exit 1
    fi
    sleep 0.05
    ELAPSED=$((ELAPSED + 1))
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "Timed out waiting for ready" >&2
        exit 1
    fi
done

# 4. Send GO <anchor_ns> (CLOCK_MONOTONIC ns)
ANCHOR=$(python3 -c "import time; print(time.monotonic_ns())")
echo "GO $ANCHOR" >&3

# 5. Wait until loader prints {"r":"armed"} on stdout
ELAPSED=0
while ! grep -q '"armed"' /tmp/capture.jsonl 2>/dev/null; do
    if ! kill -0 $LOADER_PID 2>/dev/null; then
        echo "Loader exited unexpectedly:" >&2
        cat /tmp/loader.err >&2
        exit 1
    fi
    sleep 0.05
    ELAPSED=$((ELAPSED + 1))
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "Timed out waiting for armed" >&2
        exit 1
    fi
done

# 6. Run 100 /bin/true execs inside test cgroup from a subshell
bash -c "echo \$\$ | sudo tee $CGROUP_DIR/cgroup.procs > /dev/null && for i in \$(seq 1 100); do /bin/true; done"

# 7. Brief pause for events to flush to ring buffer and loader, then stop loader
sleep 0.2
sudo kill -TERM $LOADER_PID 2>/dev/null || true
exec 3>&-
wait $LOADER_PID 2>/dev/null || true

# 8. Remove test cgroup directory
sudo rmdir "$CGROUP_DIR" 2>/dev/null || true

# Count lines with "ty":1 (exec event type) and print stats line
EXECVE_COUNT=$(grep -c '"ty":1' /tmp/capture.jsonl || true)
echo "execve count: $EXECVE_COUNT"
STATS_LINE=$(grep '"r":"stats"' /tmp/capture.jsonl || true)
echo "stats: $STATS_LINE"

if [ "$EXECVE_COUNT" -ge 100 ]; then
    echo "PASS"
    exit 0
else
    echo "FAIL"
    exit 1
fi
