#!/usr/bin/env bash
# Build the probe and run all tests including the live kernel tests. Needs root.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "$(id -u)" -ne 0 ]; then echo "run as root"; exit 1; fi
mountpoint -q /sys/kernel/tracing || mount -t tracefs nodev /sys/kernel/tracing
make -C bpf clean
make -C bpf
python3 -m unittest discover -s tests -p 'test_*.py' -v
