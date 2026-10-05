#!/usr/bin/env bash
set -euo pipefail

fail=0
req_cmds=(uname awk grep sed python3 cc clang bpftool docker)
for c in "${req_cmds[@]}"; do
  if ! command -v "$c" >/dev/null 2>&1; then
    echo "MISSING_COMMAND=$c"
    fail=1
  fi
done

echo "=== environment ==="
echo "timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "os=$(grep '^PRETTY_NAME=' /etc/os-release | cut -d= -f2- || true)"
echo "kernel=$(uname -r)"
echo "kernel_full=$(uname -a)"
echo "arch=$(uname -m)"
echo "cpu=$(nproc)"
echo "ram_kb=$(awk '/MemTotal/ {print $2}' /proc/meminfo)"
echo "docker=$(docker --version 2>/dev/null || true)"
echo "clang=$(clang --version 2>/dev/null | head -1 || true)"
echo "bpftool=$(bpftool version 2>/dev/null | head -1 || true)"
echo "python=$(python3 --version 2>/dev/null || true)"
echo "git_sha=$(git rev-parse HEAD 2>/dev/null || echo NOT_A_GIT_WORKTREE)"

if [[ -r /sys/kernel/btf/vmlinux ]]; then
  echo "btf_vmlinux=available"
else
  echo "btf_vmlinux=missing"
  fail=1
fi

if [[ -e /sys/fs/cgroup/cgroup.controllers ]]; then
  echo "cgroup_v2=available"
else
  echo "cgroup_v2=missing"
  fail=1
fi

if [[ -e /sys/kernel/debug/tracing ]]; then
  echo "tracefs=available"
else
  echo "tracefs=missing"
fi

if [[ -e /proc/sys/kernel/unprivileged_bpf_disabled ]]; then
  echo "unprivileged_bpf_disabled=$(cat /proc/sys/kernel/unprivileged_bpf_disabled)"
fi

if [[ "$EUID" -ne 0 ]]; then
  echo "privilege=non-root; CAP_BPF/CAP_PERFMON/CAP_SYS_ADMIN must be available as appropriate"
else
  echo "privilege=root"
fi

python3 - <<'PY'
import importlib.util
for name in ("numpy", "sklearn"):
    print(f"python_dep_{name}=" + ("available" if importlib.util.find_spec(name) else "missing"))
PY

if [[ "$fail" -ne 0 ]]; then
  echo "PREFLIGHT=FAIL"
  echo "Resolve the missing capabilities/tooling; do not silently substitute another environment."
  exit 2
fi

echo "PREFLIGHT=PASS"
