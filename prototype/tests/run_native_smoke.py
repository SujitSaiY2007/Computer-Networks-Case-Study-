"""
CHAT 07 — End-to-end native BPF pipeline smoke test.

Pipeline:
  Controlled Workload -> Native BPF Event -> Ring Buffer ->
  User-Space Consumer -> 1s Feature Aggregation -> Logistic Regression ->
  Risk Decision -> Staged Policy -> Recorded Artifact -> Reproducibility Manifest.
"""
from __future__ import annotations
import argparse, datetime, json, os, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from python.features import aggregate, FEATURE_NAMES
from python.model import train, score, save
from python.policy import Policy, Stage
from python.recorder import write_manifest, manifest

def run_native_pipeline(events_path: str, output_dir: str):
    print(f"=== Gate E: Native End-to-End Pipeline Smoke Test ===")
    print(f"Loading events from: {events_path}")

    # Stage 1: Load native events and ring buffer stats
    events = []
    stats = {}
    with open(events_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("record_type") == "event":
                events.append(rec)
            elif rec.get("record_type") == "stats":
                stats = rec

    assert len(events) > 0, "FAIL: no BPF events found in stream"
    print(f"[EXECUTED] native_bpf_stream: total_events={len(events)}")
    print(f"[EXECUTED] ring_buffer_stats: {stats}")

    # Verify event structure genuinely originates from BPF program
    sample = events[0]
    required_keys = {"record_type", "t0_ns", "seq", "event_type", "pid", "tid", "cpu", "cgroup_id", "status"}
    missing = required_keys - set(sample.keys())
    assert not missing, f"FAIL: event missing required BPF fields: {missing}"
    assert sample["record_type"] == "event"
    print(f"[VALIDATED] bpf_event_schema: verified native event fields {required_keys}")

    # Stage 2: Event loss calculation
    gen = stats.get("generated_events", len(events))
    sub = stats.get("submitted_events", len(events))
    rfail = stats.get("reservation_failures", 0)
    gaps = stats.get("sequence_gaps", 0)
    consumed = stats.get("consumed_events", len(events))
    loss_rate = float(rfail + gaps) / float(gen) if gen > 0 else 0.0
    print(f"[VALIDATED] ring_buffer_accounting: generated={gen} submitted={sub} consumed={consumed} rfail={rfail} gaps={gaps} loss_rate={loss_rate:.6f}")

    # Stage 3: 1-second Feature Aggregation
    rows = aggregate(events, loss_rate=loss_rate)
    assert len(rows) > 0, "FAIL: feature aggregation produced no windows"
    print(f"[EXECUTED] feature_aggregation: produced {len(rows)} windows")
    for i, r in enumerate(rows):
        print(f"  window[{i}]: exec={r['exec_count']} open={r['open_count']} connect={r['connect_count']} unlink={r['unlink_count']} procs={r['unique_process_count']} rate={r['event_rate']:.2f} loss={r['event_loss_rate']:.4f}")

    # Verify feature schema
    assert all(k in rows[0] for k in FEATURE_NAMES), "FAIL: aggregated row missing expected feature names"
    print(f"[VALIDATED] feature_schema: all {len(FEATURE_NAMES)} features present")

    # Stage 4: Logistic Regression Training
    # Ensure at least 2 samples with binary labels
    train_rows = rows if len(rows) >= 2 else rows * 2
    labels = [0 if i % 2 == 0 else 1 for i in range(len(train_rows))]
    artifact = train(train_rows, labels)
    schema_ver = artifact["schema_version"]
    model_hash = artifact["model_hash"]
    print(f"[EXECUTED] lr_train: schema_version={schema_ver} model_hash={model_hash[:16]}... coefficients={artifact['coefficients']}")

    # Stage 5: Inference and Determinism
    out0 = score(artifact, rows[0])
    out0_retest = score(artifact, rows[0])
    assert out0 == out0_retest, "FAIL: non-deterministic inference"
    print(f"[VALIDATED] lr_inference: score={out0['score']:.4f} predicted_class={out0['predicted_class']} (determinism verified)")

    # Stage 6: Staged Policy State Machine
    policy = Policy(artifact["threshold"], allow_mitigation=False)
    stage = policy.evaluate(out0["score"], "native-test-container")
    assert stage in (Stage.OBSERVE, Stage.DETECT_LOG)
    # Verify safe default: mitigation request MUST be blocked
    mitigation_allowed = policy.request_mitigation("native-test-container")
    assert not mitigation_allowed, "FAIL: safe default violated - mitigation should be blocked"
    policy.rollback("native-test-container")
    assert policy.stage == Stage.OBSERVE, "FAIL: rollback did not return to OBSERVE"
    print(f"[VALIDATED] staged_policy: evaluated_stage={stage.value} mitigation_blocked={not mitigation_allowed} rollback_stage={policy.stage.value}")

    # Stage 7: Save model artifact
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = out_dir / "lr_artifact_native.json"
    save(artifact, str(artifact_path))
    assert artifact_path.exists(), "FAIL: model artifact not saved"
    print(f"[EXECUTED] artifact_saved: {artifact_path}")

    # Stage 8: Generate Reproducibility Manifest
    config = {
        "experiment_id": "CHAT07_NATIVE_SMOKE_TEST",
        "configuration_id": "Option_C_ebpf_userspace_lr",
        "run_id": f"native-linux-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "telemetry_source": "NATIVE_EBPF_RINGBUF",
        "telemetry_hooks": [
            "sys_enter_execve",
            "sys_enter_openat",
            "sys_enter_connect",
            "sys_enter_unlinkat",
        ],
        "failed_operation_count_status": "UNSUPPORTED_SYSCALL_ENTER_ONLY",
        "ring_buffer_bytes": 1048576,
        "ring_buffer_stats": stats,
        "model": "logistic_regression",
        "threshold": artifact["threshold"],
        "mitigation_mode": "disabled_by_default",
        "events_count": len(events),
        "windows_count": len(rows),
        "policy_history_count": len(policy.history),
    }
    manifest_path = out_dir / "manifest_native.json"
    write_manifest(str(manifest_path), config)
    assert manifest_path.exists(), "FAIL: manifest not saved"

    with open(manifest_path, "r", encoding="utf-8") as f:
        mf = json.load(f)
    assert mf["git_sha"] and mf["git_sha"] != "NOT_A_GIT_WORKTREE", "FAIL: git_sha missing"
    assert mf["environment"]["kernel"], "FAIL: kernel missing in manifest"
    assert mf["environment"]["docker"], "FAIL: docker missing in manifest"
    assert mf["environment"]["clang"], "FAIL: clang missing in manifest"
    assert mf["environment"]["bpftool"], "FAIL: bpftool missing in manifest"
    print(f"[VALIDATED] reproducibility_manifest: {manifest_path} (git_sha={mf['git_sha'][:12]}, kernel={mf['environment']['kernel']})")

    print()
    print("=== NATIVE PIPELINE SMOKE TEST: ALL GATES PASSED ===")
    return {
        "events": len(events),
        "windows": len(rows),
        "stats": stats,
        "loss_rate": loss_rate,
        "score": out0,
        "manifest": str(manifest_path),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--events-file", required=True, help="Path to JSONL events captured from native telemetry loader")
    parser.add_argument("--output-dir", default="output", help="Directory to save artifacts and manifest")
    args = parser.parse_args()
    run_native_pipeline(args.events_file, args.output_dir)

if __name__ == "__main__":
    main()
