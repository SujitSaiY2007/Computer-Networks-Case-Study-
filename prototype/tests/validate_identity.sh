#!/usr/bin/env bash
set -uo pipefail

cd "$(dirname "$0")/../.."

echo "=== Gate C: Workload and Identity Correlation ==="

# 1. Start a controlled active container workload performing openat and unlinkat
docker rm -f chat07_val_cnt 2>/dev/null || true
docker run -d --name chat07_val_cnt alpine sh -c "while true; do touch /tmp/f; rm -f /tmp/f; sleep 0.1; done"

# 2. Run identity_probe.py
python3 prototype/python/identity_probe.py --container chat07_val_cnt

# 3. Retrieve container PID and cgroup details
CPID=$(docker inspect -f '{{.State.Pid}}' chat07_val_cnt)
CG_REL=$(cat /proc/"$CPID"/cgroup | head -1 | cut -d: -f3)
CG_INODE=$(stat -c %i "/sys/fs/cgroup$CG_REL")

echo "HOST_PID=$CPID"
echo "CGROUP_PATH=$CG_REL"
echo "CGROUP_INODE=$CG_INODE"

# 4. Run telemetry loader for 3 seconds
EVFILE="/tmp/gate_c_events.jsonl"
rm -f "$EVFILE"
./prototype/bpf/telemetry_loader ./prototype/bpf/telemetry.bpf.o --duration 3 > "$EVFILE"

# 5. Check for events matching container cgroup or host PID
MATCH_COUNT=$(grep -c "\"cgroup_id\":$CG_INODE" "$EVFILE" || true)
echo "MATCHED_CONTAINER_EVENTS=$MATCH_COUNT"

if [ "$MATCH_COUNT" -gt 0 ]; then
  echo "--- Matched Container Event Sample ---"
  grep "\"cgroup_id\":$CG_INODE" "$EVFILE" | head -n 5
  echo "GATE_C=PASS"
else
  echo "Captured events total: $(wc -l < "$EVFILE")"
  echo "Sample events:"
  head -n 5 "$EVFILE" || true
  echo "GATE_C=FAIL (no events matched container cgroup $CG_INODE)"
fi

# Cleanup
docker rm -f chat07_val_cnt >/dev/null 2>&1 || true
