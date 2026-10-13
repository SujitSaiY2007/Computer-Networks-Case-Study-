from __future__ import annotations
import json, platform, subprocess, sys, hashlib
from pathlib import Path


def git_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "NOT_A_GIT_WORKTREE"


def _cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, text=True, stderr=subprocess.STDOUT
        ).strip()[:500]
    except Exception:
        return "UNAVAILABLE"


def _deps():
    out = {}
    for name in ("numpy", "sklearn"):
        try:
            m = __import__(name)
            out[name] = getattr(m, "__version__", "unknown")
        except Exception:
            out[name] = "missing"
    return out


def manifest(config: dict) -> dict:
    return {
        "experiment_id": config["experiment_id"],
        "configuration_id": config["configuration_id"],
        "run_id": config["run_id"],
        "timestamp_utc": config["timestamp_utc"],
        "git_sha": git_sha(),
        "environment": {
            "os": platform.platform(),
            "kernel": platform.release(),
            "architecture": platform.machine(),
            "cpu_count": __import__("os").cpu_count(),
            "python": sys.version.split()[0],
            "docker": _cmd(["docker", "--version"]),
            "libbpf": _cmd(["bash", "-lc", "ldconfig -p | grep libbpf | head -1"]),
            "bpftool": _cmd(["bpftool", "version"]),
            "clang": _cmd(["clang", "--version"]),
            "python_dependencies": _deps(),
        },
        "configuration": config,
    }


def write_manifest(path, config):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(manifest(config), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )