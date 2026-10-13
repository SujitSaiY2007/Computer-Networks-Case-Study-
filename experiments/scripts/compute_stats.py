#!/usr/bin/env python3
import json, glob
import numpy as np

files = glob.glob('experiments/raw/run_*.json')
print('Total files:', len(files))

cfg_cpu = {c: [] for c in 'ABCDE'}
cfg_rss = {c: [] for c in 'ABCDE'}
cfg_loss = {c: [] for c in 'BCDE'}
inf_c = []
inf_d = []
det_c = []
det_d = []
det_e = []
mit_e = []
dtm_e = []

for f in sorted(files):
    with open(f) as fp:
        d = json.load(fp)
    c = d['config_id']
    cfg_cpu[c].append(d['resources']['cpu_utilization_pct'])
    cfg_rss[c].append(d['resources']['rss_peak_mb'])
    if c in cfg_loss:
        cfg_loss[c].append(d['telemetry']['loss_rate'])
    if c == 'C' and d['latency']['inference_latency_us'] > 0:
        inf_c.append(d['latency']['inference_latency_us'])
        det_c.append(d['latency']['detection_latency_ms'])
    elif c == 'D' and d['latency']['inference_latency_us'] > 0:
        inf_d.append(d['latency']['inference_latency_us'])
        det_d.append(d['latency']['detection_latency_ms'])
    elif c == 'E' and d['latency']['inference_latency_us'] > 0:
        det_e.append(d['latency']['detection_latency_ms'])
        if d['latency']['mitigation_latency_ms'] is not None:
            mit_e.append(d['latency']['mitigation_latency_ms'])
            dtm_e.append(d['latency']['detection_to_mitigation_ms'])

print('CPU (%):')
for k, v in cfg_cpu.items():
    print(f"  Config {k}: mean={np.mean(v):.2f} std={np.std(v):.2f} p50={np.median(v):.2f} p95={np.percentile(v, 95):.2f}")

print('\nRSS (MB):')
for k, v in cfg_rss.items():
    print(f"  Config {k}: mean={np.mean(v):.2f} std={np.std(v):.2f} p50={np.median(v):.2f} p95={np.percentile(v, 95):.2f}")

print('\nLoss max (%):', {k: max(v)*100 for k, v in cfg_loss.items()})

print('\nInference Latency (us):')
print(f"  Config C (User-space Float): mean={np.mean(inf_c):.2f} std={np.std(inf_c):.2f} median={np.median(inf_c):.2f} IQR={np.percentile(inf_c, 75) - np.percentile(inf_c, 25):.2f} p95={np.percentile(inf_c, 95):.2f}")
print(f"  Config D (Kernel Fixed-Pt): mean={np.mean(inf_d):.2f} std={np.std(inf_d):.2f} median={np.median(inf_d):.2f} IQR={np.percentile(inf_d, 75) - np.percentile(inf_d, 25):.2f} p95={np.percentile(inf_d, 95):.2f}")
speedup = np.mean(inf_c) / np.mean(inf_d)
print(f"  Mean Ratio (C/D): {speedup:.2f}x")

print('\nDetection Latency (ms):')
print(f"  Config C: mean={np.mean(det_c):.3f} std={np.std(det_c):.3f} median={np.median(det_c):.3f}")
print(f"  Config D: mean={np.mean(det_d):.3f} std={np.std(det_d):.3f} median={np.median(det_d):.3f}")
print(f"  Config E: mean={np.mean(det_e):.3f} std={np.std(det_e):.3f} median={np.median(det_e):.3f}")

print('\nMitigation Latency Config E (ms):')
print(f"  Mitigation (T7-T6): mean={np.mean(mit_e):.3f} std={np.std(mit_e):.3f} median={np.median(mit_e):.3f} count={len(mit_e)}")
print(f"  Detection-to-Mitigation (T7-T0): mean={np.mean(dtm_e):.3f} std={np.std(dtm_e):.3f} median={np.median(dtm_e):.3f}")
