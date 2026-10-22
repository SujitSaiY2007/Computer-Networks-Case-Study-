"""Integration tests for the BPF probe and loader. Need root, cgroup v2,
syscall tracepoints and a built prototype/bpf. Skipped otherwise."""
import json
import os
import subprocess
import time
import unittest
from pathlib import Path

BPF = Path(__file__).resolve().parents[1] / "bpf"
LOADER, OBJ = BPF / "telemetry_loader", BPF / "telemetry.bpf.o"
def _default_cg_root() -> str:
    """cgroup v2 root: /sys/fs/cgroup on pure v2 hosts, /sys/fs/cgroup/unified on hybrid hosts."""
    if os.path.exists("/sys/fs/cgroup/cgroup.controllers"):
        return "/sys/fs/cgroup/ebpfexp"
    return "/sys/fs/cgroup/unified/ebpfexp"


CG_ROOT = Path(os.environ.get("EBPF_CGROUP_ROOT", _default_cg_root()))
TP = Path("/sys/kernel/tracing/events/syscalls/sys_enter_execve")


def available():
    return os.geteuid() == 0 and LOADER.exists() and OBJ.exists() and TP.exists() and CG_ROOT.parent.exists()


@unittest.skipUnless(available(), "needs root, built loader, syscall tracepoints and cgroup v2")
class LoaderTests(unittest.TestCase):
    def setUp(self):
        CG_ROOT.mkdir(parents=True, exist_ok=True)
        self.cg = CG_ROOT / f"test_{os.getpid()}_{time.monotonic_ns()}"
        self.cg.mkdir()

    def tearDown(self):
        self.cg.rmdir()

    def start(self, extra=()):
        p = subprocess.Popen([str(LOADER), str(OBJ), "--cgroup", str(self.cg), *extra],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
        self.assertEqual(json.loads(p.stdout.readline())["r"], "ready")
        p.stdin.write(f"GO {time.monotonic_ns()}\n")
        p.stdin.flush()
        self.assertEqual(json.loads(p.stdout.readline())["r"], "armed")
        return p

    def stop(self, p):
        p.terminate()
        p.stdin.close()
        lines = [json.loads(line) for line in p.stdout.read().splitlines()]
        p.wait(10)
        p.stdout.close()
        return lines, lines[-1]

    def in_cgroup(self, cmd):
        def join():
            (self.cg / "cgroup.procs").write_text(str(os.getpid()))
        subprocess.run(["sh", "-c", cmd], preexec_fn=join, check=True)

    def test_loader_stays_alive_under_event_load(self):
        """Old bug: the loop counted poll wake-ups, so under load the loader exited in ~0.1 s."""
        p = self.start()
        t0 = time.monotonic()
        while time.monotonic() - t0 < 2.0:
            self.in_cgroup("for i in $(seq 50); do /bin/true; done")
        lines, st = self.stop(p)
        execs = sum(1 for r in lines if r.get("r") == "e" and r["ty"] == 1)
        self.assertEqual(st["stopped_by"], "signal")
        self.assertGreaterEqual(st["lifetime_s"], 2.0)
        self.assertGreater(execs, 200)
        self.assertEqual(st["generated"], st["consumed"])

    def test_cgroup_filter(self):
        p = self.start()
        self.in_cgroup("for i in $(seq 20); do /bin/true; done")
        subprocess.run(["sh", "-c", "for i in $(seq 200); do /bin/true; done"], check=True)
        lines, st = self.stop(p)
        execs = sum(1 for r in lines if r.get("r") == "e" and r["ty"] == 1)
        self.assertGreaterEqual(execs, 20)
        self.assertLess(execs, 40)

    def test_in_kernel_alert_at_exact_threshold(self):
        """w_exec = 1.0, b = -50.0: logit reaches exactly 0 on the 50th exec of the window."""
        q = 65536
        p = self.start(["--infer", "--w", f"{q},0,0,0,0", "--b", str(-50 * q)])
        self.in_cgroup("for i in $(seq 100); do /bin/true; done")
        lines, st = self.stop(p)
        alerts = [r for r in lines if r.get("r") == "a"]
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["logit_q16"], 0)
        self.assertGreaterEqual(alerts[0]["td"], alerts[0]["t0"])
        self.assertEqual(st["alerts_kernel"], 1)


if __name__ == "__main__":
    unittest.main()
