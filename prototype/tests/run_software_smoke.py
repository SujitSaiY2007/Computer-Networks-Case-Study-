"""
CHAT 07 — End-to-end software-side pipeline smoke test.

Event source: SIMULATED synthetic fixture.
This test validates the full software pipeline:
  synthetic events -> feature aggregation -> LR training/inference ->
  policy decision -> recording -> reproducibility manifest.

Native BPF execution requires a Linux host with the CHAT 06 toolchain.
"""
from __future__ import annotations
import sys, json, datetime, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from python.features import aggregate, FEATURE_NAMES
from python.model import train, score, save
from python.policy import Policy, Stage
from python.recorder import write_manifest

# ---- STAGE 1: Synthetic event stream (SIMULATED, not native BPF) ----
base_ns = 1_000_000_000
events = []
for i in range(12):
    t = base_ns + i * 100_000_000
    etype = (i % 4) + 1
    events.append({
        "record_type": "event",
        "t0_ns": t,
        "event_type": etype,
        "pid": 100 + (i % 3),
        "tid": 200 + i,
        "cpu": 0,
        "cgroup_id": 12345,
        "status": 0,
        "seq": i + 1,
    })
for i in range(6):
    t = 2_000_000_000 + i * 100_000_000
    etype = (i % 3) + 1
    events.append({
        "record_type": "event",
        "t0_ns": t,
        "event_type": etype,
        "pid": 200 + (i % 2),
        "tid": 300 + i,
        "cpu": 1,
        "cgroup_id": 12345,
        "status": 0,
        "seq": 13 + i,
    })

print(f"[SIMULATED] event_source=synthetic_fixture events={len(events)}")

# ---- STAGE 2: Feature Aggregation ----
rows = aggregate(events)
assert len(rows) == 2, f"Expected 2 windows, got {len(rows)}"
print(f"[EXECUTED] feature_aggregation windows={len(rows)}")
for i, r in enumerate(rows):
    exec_c = r["exec_count"]
    open_c = r["open_count"]
    conn_c = r["connect_count"]
    unlink_c = r["unlink_count"]
    rate = r["event_rate"]
    loss = r["event_loss_rate"]
    print(f"  window[{i}]: exec={exec_c} open={open_c} connect={conn_c} unlink={unlink_c} rate={rate:.2f} loss={loss}")

# ---- STAGE 3: LR Training ----
labels = [0, 1]
artifact = train(rows, labels)
schema_ver = artifact["schema_version"]
model_hash = artifact["model_hash"][:16]
print(f"[EXECUTED] lr_train schema_version={schema_ver} model_hash={model_hash}...")

# ---- STAGE 4: Inference ----
out0 = score(artifact, rows[0])
out1 = score(artifact, rows[1])
print(f"[EXECUTED] lr_score window[0]={out0}")
print(f"[EXECUTED] lr_score window[1]={out1}")

# ---- STAGE 5: Policy Decision ----
policy = Policy(artifact["threshold"], allow_mitigation=False)
stage0 = policy.evaluate(out0["score"], "test-resource")
stage1 = policy.evaluate(out1["score"], "test-resource")
# Verify safe default: mitigation must be blocked
assert not policy.request_mitigation("test-resource"), "FAIL: mitigation should be blocked in safe mode"
policy.rollback("test-resource")
assert policy.stage == Stage.OBSERVE, "FAIL: rollback should return to OBSERVE"
print(f"[VALIDATED] policy stage0={stage0.value} stage1={stage1.value} mitigation=blocked rollback=OBSERVE")

# ---- STAGE 6: Feature Schema Validation ----
assert artifact["feature_names"] == FEATURE_NAMES, "FAIL: schema mismatch"
print(f"[VALIDATED] feature_schema names={FEATURE_NAMES}")

# ---- STAGE 7: Determinism check ----
out0_b = score(artifact, rows[0])
assert out0 == out0_b, "FAIL: non-deterministic inference"
print("[VALIDATED] determinism: score is reproducible")

# ---- STAGE 8: Save artifact ----
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROTOTYPE_DIR = os.path.dirname(TESTS_DIR)
OUTPUT_DIR = os.path.join(PROTOTYPE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

artifact_path = os.path.join(OUTPUT_DIR, "lr_artifact_smoke.json")
save(artifact, artifact_path)
print(f"[EXECUTED] artifact saved to {artifact_path}")

# ---- STAGE 9: Reproducibility Manifest ----
config = {
    "experiment_id": "CHAT07_SMOKE_TEST",
    "configuration_id": "baseline-user-space-lr",
    "run_id": "windows-smoke-2026-10-13",
    "timestamp_utc": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "feature_window_ns": 1_000_000_000,
    "telemetry_hooks": [
        "sys_enter_execve",
        "sys_enter_openat",
        "sys_enter_connect",
        "sys_enter_unlinkat",
    ],
    "ring_buffer_bytes": 1_048_576,
    "model": "logistic_regression",
    "threshold": 0.5,
    "mitigation_mode": "disabled_by_default",
    "seed": 0,
    "event_source": "SIMULATED_FIXTURE",
    "event_count": len(events),
    "windows_produced": len(rows),
    "policy_history_count": len(policy.history),
}
manifest_path = os.path.join(OUTPUT_DIR, "manifest_smoke.json")
write_manifest(manifest_path, config)
print(f"[EXECUTED] manifest written to {manifest_path}")

# Validate manifest contents
with open(manifest_path, encoding="utf-8") as f:
    mf = json.load(f)
assert mf["git_sha"] and mf["git_sha"] != "NOT_A_GIT_WORKTREE", "WARN: git sha not captured"
assert mf["environment"]["python"]
assert mf["configuration"]["event_source"] == "SIMULATED_FIXTURE"
print(f"[VALIDATED] manifest git_sha={mf['git_sha'][:16]}... python={mf['environment']['python']}")

print()
print("=== SOFTWARE-SIDE PIPELINE: SMOKE_PASS ===")
print("NOTE: Event source is SIMULATED. Native BPF execution requires Linux host.")
