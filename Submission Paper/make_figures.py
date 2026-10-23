import json, glob, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D

RAW = "/home/claude/s5/experiments/raw/*.json"
MODEL = "/home/claude/s5/experiments/calibration/lr_model_frozen.json"
OUT = "figures/"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7, "axes.titlesize": 7.5,
    "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "legend.fontsize": 6.3, "axes.linewidth": 0.6, "pdf.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})
CFG = {"A": "#7F7F7F", "B": "#0072B2", "C": "#E69F00", "D": "#009E73", "E": "#CC79A7"}
WL = ["B1", "B2", "B3", "B4", "A1", "A2", "A3"]
WLC = {"B1": "#56B4E9", "B2": "#0072B2", "B3": "#009E73", "B4": "#7B5EA7",
       "A1": "#D55E00", "A2": "#E69F00", "A3": "#C2185B"}
WLN = {"B1": "B1 idle", "B2": "B2 file processing", "B3": "B3 process churn",
       "B4": "B4 client-server", "A1": "A1 drop and execute",
       "A2": "A2 file sweep", "A3": "A3 connection burst"}

R = [json.load(open(f)) for f in glob.glob(RAW)]
assert len(R) == 350
def sel(c=None, w=None):
    return [r for r in R if (c is None or r["config_id"] == c) and (w is None or r["workload_id"] == w)]
ops = lambda r: r["resources"]["ops_per_second"]

# ---------------------------------------------------------------- Fig 1
def box(ax, x, y, w, h, text, fc, ec, fs=6.4, bold=False, tc="black"):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=0.9",
                       fc=fc, ec=ec, lw=0.9)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=tc, linespacing=1.25)

def arrow(ax, p, q, color="#333333", ls="-", lw=1.1, rad=0.0, label=None, lx=0, ly=0, lc=None, fs=5.8):
    a = FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=7, color=color, lw=lw,
                        linestyle=ls, connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)
    if label:
        ax.text((p[0] + q[0]) / 2 + lx, (p[1] + q[1]) / 2 + ly, label, fontsize=fs,
                ha="center", va="center", color=lc or color, style="italic")

fig, ax = plt.subplots(figsize=(7.16, 3.7))
ax.set_xlim(0, 100); ax.set_ylim(0, 50); ax.axis("off")
ax.add_patch(Rectangle((0.5, 17), 18.5, 31.5, fc="#DCEEFB", ec="#2B7BB9", lw=1.0))
ax.text(9.75, 46.6, "Docker container", ha="center", fontsize=7, fontweight="bold", color="#1B5C8C")
ax.text(9.75, 44.3, "own cgroup v2", ha="center", fontsize=6, color="#1B5C8C")
ax.add_patch(Rectangle((21.5, 17), 42, 31.5, fc="#E6F4EA", ec="#2E8B57", lw=1.0))
ax.text(42.5, 46.6, "Linux kernel", ha="center", fontsize=7, fontweight="bold", color="#1E6B43")
ax.add_patch(Rectangle((66, 17), 33.5, 31.5, fc="#FFF1DC", ec="#D98A00", lw=1.0))
ax.text(82.75, 46.6, "User space (host)", ha="center", fontsize=7, fontweight="bold", color="#A86800")

box(ax, 2.2, 24, 15, 15, "Workload\n\nB1 to B4 benign\nA1 to A3\nanomalous\n\n2 s per run", "#FFFFFF", "#2B7BB9", fs=5.9)
box(ax, 23.5, 37.2, 17.5, 7, "Syscall tracepoints\nexecve, openat, connect,\nunlink, unlinkat", "#FFFFFF", "#2E8B57", fs=5.5)
box(ax, 23.5, 20.5, 17.5, 13.5, "eBPF probe\n\ncgroup and anchor filter\ncounters, sequence no.\n56-byte record", "#FFFFFF", "#2E8B57", fs=5.5)
box(ax, 45.5, 33, 15.5, 8.5, "Ring buffer, 4 MiB\nevents and alerts", "#FFFFFF", "#2E8B57", fs=5.6)
box(ax, 45.5, 19.2, 15.5, 11.6, "In-kernel classifier\n(Config D)\n5 window counts\nQ16.16 logit \u2265 0\n\u2192 alert record", "#CDEFD9", "#009E73", fs=5.5)
box(ax, 67.8, 36, 14, 8, "Consumer (libbpf)\ndrain, JSON lines,\ntransfer latency", "#FFFFFF", "#D98A00", fs=5.5)
box(ax, 84.6, 36, 13.4, 8, "Staged policy\nObserve, Detect-Log,\nMitigate, Rollback", "#FFFFFF", "#D98A00", fs=5.0)
box(ax, 67.8, 21, 14, 11, "Features\n1 s windows\n5 counts", "#FFFFFF", "#D98A00", fs=5.8)
box(ax, 85, 21, 12.6, 11, "Float classifier\n(Configs C, E)\nlogistic\nregression", "#FDE9C4", "#E69F00", fs=5.5)

arrow(ax, (17.6, 33), (23.2, 40.3), lw=1.1)
ax.text(19.3, 38.4, "syscalls", fontsize=5.4, style="italic", ha="center", va="center", color="#333333",
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85), zorder=6)
arrow(ax, (32.25, 37.1), (32.25, 34.3))
arrow(ax, (41.3, 29), (45.2, 26), color="#009E73")
arrow(ax, (41.3, 33.2), (45.2, 36.4))
arrow(ax, (53.25, 31.1), (53.25, 32.8), color="#009E73", ls="--")
arrow(ax, (61.3, 38), (67.6, 40))
arrow(ax, (82.0, 40), (84.3, 40))
arrow(ax, (74.8, 35.8), (74.8, 32.3))
arrow(ax, (82.0, 26.5), (84.7, 26.5))
arrow(ax, (91.3, 32.3), (91.3, 35.7))
ax.plot([97.9, 98.9, 98.9, 9.75, 9.75], [40, 40, 13.2, 13.2, 22], color="#8E3B8E", lw=1.3, solid_capstyle="round")
arrow(ax, (9.75, 20.5), (9.75, 23.4), color="#8E3B8E", lw=1.3)
ax.text(54, 14.3, "Config E: write 1 to cgroup.freeze, wait for \u201cfrozen 1\u201d, then write 0 (thaw)", fontsize=6.0,
        color="#8E3B8E", ha="center", fontweight="bold")

ax.text(0.5, 9.6, "Configurations", fontsize=6.8, fontweight="bold", ha="left")
chips = [("A", "baseline,\nno probe"), ("B", "+ telemetry"), ("C", "+ float classifier\nin user space"),
         ("D", "+ Q16.16 classifier\ninside the probe"), ("E", "C + cgroup freeze\nand thaw")]
for i, (k, t) in enumerate(chips):
    x0 = 0.5 + i * 19.9
    ax.add_patch(FancyBboxPatch((x0, 0.8), 19.0, 7.4, boxstyle="round,pad=0.2,rounding_size=0.8",
                                fc=CFG[k], ec="none", alpha=0.92))
    ax.text(x0 + 1.6, 4.5, k, color="white", fontsize=10, fontweight="bold", va="center")
    ax.text(x0 + 4.4, 4.5, t, color="white", fontsize=5.6, va="center", linespacing=1.2)
fig.savefig(OUT + "fig1_pipeline.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig(OUT + "fig1_pipeline.png", dpi=170, bbox_inches="tight", pad_inches=0.03)
plt.close(fig)

# ---------------------------------------------------------------- Fig 2
def stats(w):
    a = np.mean([ops(r) for r in sel("A", w)])
    out = {}
    for c in "BCDE":
        rs = sel(c, w)
        b = np.mean([ops(r) for r in rs])
        ev = np.mean([r["telemetry"]["workload_events"] / r["resources"]["workload_duration_seconds"] for r in rs])
        out[c] = (ev, (1 - b / a) * 100)
    return out

fig, ax = plt.subplots(figsize=(3.5, 2.85))
xs = np.linspace(0, 52000, 100)
ax.fill_between(xs, 12e-6 * xs * 100, 15e-6 * xs * 100, color="#9ED9C5", alpha=0.65, lw=0,
                label="12 to 15 \u00b5s per event")
ax.plot(xs, 13.5e-6 * xs * 100, color="#009E73", lw=0.8)
for w in ["B2", "B3", "B4", "A1", "A2", "A3"]:
    s = stats(w)
    for c in "CDE":
        ax.scatter(s[c][0], s[c][1], s=14, color=WLC[w], alpha=0.35, marker={"C": "s", "D": "^", "E": "D"}[c],
                   lw=0, zorder=3)
    ax.scatter(s["B"][0], s["B"][1], s=46, color=WLC[w], edgecolor="black", lw=0.6, zorder=4, label=WLN[w])
ax.annotate("A3: about 25 \u00b5s\nper event", xy=(stats("A3")["B"][0], stats("A3")["B"][1]),
            xytext=(1200, 43), fontsize=6, color="#C2185B", arrowprops=dict(arrowstyle="-", color="#C2185B", lw=0.6))
ax.annotate("B4: 180 events/s,\nno measurable loss", xy=(180, 0.5), xytext=(1200, 18.5), fontsize=6, color="#7B5EA7",
            arrowprops=dict(arrowstyle="-", color="#7B5EA7", lw=0.6))
ax.set_xlabel("Recorded events per second (configuration B)")
ax.set_ylabel("Throughput loss vs. configuration A (%)")
ax.set_xlim(0, 52000); ax.set_ylim(-3, 68)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v/1000)}k" if v else "0"))
ax.grid(alpha=0.25, lw=0.4)
h, l = ax.get_legend_handles_labels()
mk = [Line2D([], [], marker=m, ls="", color="#555555", alpha=0.6, ms=3.5, label=f"Config {c}") for c, m in
      (("C", "s"), ("D", "^"), ("E", "D"))]
ax.legend(h + mk, l + [m.get_label() for m in mk], loc="lower right", frameon=True, framealpha=0.95, ncol=1,
          fontsize=5.4, borderpad=0.4, labelspacing=0.28, handletextpad=0.4)
fig.savefig(OUT + "fig2_overhead_model.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig(OUT + "fig2_overhead_model.png", dpi=190, bbox_inches="tight", pad_inches=0.03)
plt.close(fig)

# ---------------------------------------------------------------- Fig 3
fig, ax = plt.subplots(figsize=(7.16, 2.55))
wls = ["B2", "B3", "B4", "A1", "A2", "A3"]
bw = 0.19
for j, c in enumerate("BCDE"):
    m, e = [], []
    for w in wls:
        a = np.mean([ops(r) for r in sel("A", w)])
        v = [ops(r) for r in sel(c, w)]
        m.append((np.mean(v) / a - 1) * 100); e.append(np.std(v, ddof=1) / a * 100)
    xs_ = np.arange(len(wls)) + (j - 1.5) * bw
    ax.bar(xs_, m, bw, yerr=e, color=CFG[c], capsize=1.5, error_kw=dict(lw=0.6, ecolor="#222222"),
           label={"B": "B telemetry only", "C": "C float classifier", "D": "D in-kernel classifier",
                  "E": "E float classifier + freeze"}[c], edgecolor="white", lw=0.3)
    for x_, m_ in zip(xs_, m):
        yy_ = 1.4 + (3.4 * (j % 2) if abs(m_) < 2 else 0)
        ax.text(x_, yy_, f"{m_:+.0f}" if abs(m_) >= 2 else f"{m_:+.1f}", ha="center", va="bottom", fontsize=5.3, color=CFG[c], fontweight="bold")
ax.axhline(0, color="black", lw=0.7)
ax.set_xticks(range(len(wls)))
ax.set_xticklabels([f"{WLN[w]}\n({round(np.mean([r['telemetry']['workload_events']/r['resources']['workload_duration_seconds'] for r in sel('B', w)])):,} events/s)" for w in wls])
ax.set_ylabel("Change in throughput vs. A (%)")
ax.set_ylim(-66, 10)
ax.grid(axis="y", alpha=0.25, lw=0.4)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=4, frameon=False)
fig.savefig(OUT + "fig3_throughput.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig(OUT + "fig3_throughput.png", dpi=170, bbox_inches="tight", pad_inches=0.03)
plt.close(fig)

# ---------------------------------------------------------------- Fig 4
def q(vals): v = np.array([x for x in vals if x is not None], float); return np.median(v), np.percentile(v, 95)
D = [r for r in sel("D") if r["prediction"] == 1]
Es = [r for r in sel("E") if r["enforcement"]["mitigation_triggered"]]
rows = [
    ("Probe: syscall to in-kernel decision", "D", q([r["latency"]["kernel_decision_us"] for r in D])),
    ("Alert: decision to consumer", "D", q([r["latency"]["alert_to_user_us"] for r in D])),
    ("Event transfer: probe to consumer", "B", q([r["telemetry"]["telemetry_transfer_latency_us"] for r in R if r["config_id"] != "A"])),
    ("Float inference, one window (Python)", "C", q([r["latency"]["inference_latency_us"] for r in sel("C")])),
    ("Feature aggregation, whole run (Python)", "C", q([r["latency"]["feature_aggregation_us"] for r in R if r["config_id"] in "CE"])),
    ("cgroup freeze: request to frozen", "E", q([r["enforcement"]["mitigation_latency_ms"] * 1000 for r in Es])),
    ("cgroup thaw: request to thawed", "E", q([r["enforcement"]["rollback_time_ms"] * 1000 for r in Es])),
]
fig, ax = plt.subplots(figsize=(7.16, 2.55))
yy = np.arange(len(rows))[::-1]
for y, (name, c, (med, p95)) in zip(yy, rows):
    ax.barh(y, med, color=CFG[c], height=0.62, edgecolor="white", lw=0.4)
    ax.plot([med, p95], [y, y], color="#222222", lw=0.8)
    ax.plot([p95, p95], [y - 0.14, y + 0.14], color="#222222", lw=0.8)
    lab = f"{med:,.1f} \u00b5s" if med < 1000 else f"{med/1000:,.1f} ms"
    ax.text(med * 0.93, y, lab, ha="right", va="center", fontsize=6.2, color="white", fontweight="bold")
ax.set_xscale("log"); ax.set_xlim(1, 1.5e5)
ax.set_yticks(yy); ax.set_yticklabels([r[0] for r in rows])
ax.set_xlabel("Latency, log scale (bar = median, whisker = 95th percentile)")
ax.grid(axis="x", alpha=0.25, lw=0.4)
ax.legend(handles=[Rectangle((0, 0), 1, 1, color=CFG[k]) for k in "DBCE"],
          labels=["Config D (in kernel)", "Configs B to E (transport)", "Config C (user space)", "Config E (containment)"],
          loc="lower right", frameon=True, framealpha=0.95)
fig.savefig(OUT + "fig4_latency.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig(OUT + "fig4_latency.png", dpi=170, bbox_inches="tight", pad_inches=0.03)
plt.close(fig)

# ---------------------------------------------------------------- Fig 5
m = json.load(open(MODEL))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.16, 2.6), gridspec_kw={"width_ratios": [1.55, 1]})
rng = np.random.default_rng(3)
for i, w in enumerate(WL):
    s = [r["score"] for r in sel("C", w)]
    a1.scatter(i + rng.uniform(-0.18, 0.18, len(s)), s, s=16, color=WLC[w], edgecolor="black", lw=0.3, zorder=3)
a1.axhline(0.5, color="#C62828", lw=1.0, ls="--")
a1.text(6.45, 0.52, "threshold 0.5", color="#C62828", fontsize=6, ha="right", va="bottom")
a1.axhspan(0.5, 1.02, color="#FDECEA", zorder=0); a1.axhspan(-0.02, 0.5, color="#EAF3FB", zorder=0)
a1.text(-0.42, 0.97, "flagged as anomalous", fontsize=6, color="#C62828", va="top")
a1.text(-0.42, 0.03, "not flagged", fontsize=6, color="#1B5C8C", va="bottom")
a1.annotate("held out:\nall 10 runs missed", xy=(6, 0.02), xytext=(4.45, 0.30), fontsize=6, color="#C2185B",
            arrowprops=dict(arrowstyle="->", color="#C2185B", lw=0.7))
a1.set_xticks(range(7)); a1.set_xticklabels(WL)
a1.set_ylabel("Classifier score (configuration C)"); a1.set_ylim(-0.02, 1.02); a1.set_xlim(-0.5, 6.5)
a1.set_title("(a) Score of every run", loc="left")
names = ["exec", "open", "connect", "unlink", "unique\nprocesses"]
co = m["coefficients"]
cols = ["#D55E00" if v > 0 else "#0072B2" for v in co]
b = a2.barh(range(5)[::-1], co, color=cols, edgecolor="white", height=0.62)
for y, v in zip(range(5)[::-1], co):
    a2.text(v + (0.05 if v > 0 else -0.05), y, f"{v:+.2f}", va="center", ha="left" if v > 0 else "right", fontsize=6.2)
a2.axvline(0, color="black", lw=0.7)
a2.set_yticks(range(5)[::-1]); a2.set_yticklabels(names)
a2.set_xlim(-1.5, 1.35)
a2.set_xlabel("Standardized coefficient")
a2.set_title("(b) What the model learned", loc="left")
a2.annotate("connect is negative:\nonly benign B4 had\nconnections in\ntraining", xy=(co[2], 2), xytext=(0.08, 1.45),
            fontsize=5.6, color="#1B5C8C", arrowprops=dict(arrowstyle="->", color="#1B5C8C", lw=0.7))
a2.legend(handles=[Rectangle((0, 0), 1, 1, color="#D55E00"), Rectangle((0, 0), 1, 1, color="#0072B2")],
          labels=["raises score", "lowers score"], loc="upper right", frameon=True, fontsize=5.8, bbox_to_anchor=(1.0, 1.0))
fig.tight_layout(w_pad=1.5)
fig.savefig(OUT + "fig5_detection.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig(OUT + "fig5_detection.png", dpi=170, bbox_inches="tight", pad_inches=0.03)
plt.close(fig)

# ---------------------------------------------------------------- Fig 6
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.16, 2.5), gridspec_kw={"width_ratios": [1, 1.25]})
fz = [(r["enforcement"]["mitigation_latency_ms"], r["enforcement"]["rollback_time_ms"], r["workload_id"]) for r in Es]
for k, (lab, idx) in enumerate((("Freeze", 0), ("Thaw", 1))):
    for w, col in (("A1", WLC["A1"]), ("A2", WLC["A2"])):
        v = [x[idx] for x in fz if x[2] == w]
        a1.scatter(k + rng.uniform(-0.17, 0.17, len(v)), v, s=18, color=col, edgecolor="black", lw=0.3, label=WLN[w] if k == 0 else None, zorder=3)
    med = np.median([x[idx] for x in fz])
    a1.plot([k - 0.3, k + 0.3], [med, med], color="black", lw=1.2)
    a1.text(k + 0.33, med, f"median\n{med:.3f} ms", fontsize=5.8, va="center")
a1.set_xticks([0, 1]); a1.set_xticklabels(["Freeze\n(request to frozen)", "Thaw\n(request to thawed)"])
a1.set_xlim(-0.5, 1.9); a1.set_ylim(0, 0.45)
a1.set_ylabel("Latency (ms)")
a1.set_title("(a) Freeze and thaw of the 20 flagged runs", loc="left")
a1.legend(loc="upper right", frameon=True, fontsize=5.8)
a1.grid(axis="y", alpha=0.25, lw=0.4)
order = sorted(Es, key=lambda r: r["latency"]["detection_to_mitigation_ms"])
proc = [r["latency"]["processing_latency_ms"] for r in order]
frz = [r["enforcement"]["mitigation_latency_ms"] for r in order]
x = np.arange(len(order))
a2.bar(x, proc, color=CFG["C"], label="Feature aggregation and scoring (Python)", edgecolor="white", lw=0.3)
a2.bar(x, frz, bottom=proc, color=CFG["E"], label="Freeze (cgroup v2)", edgecolor="white", lw=0.3)
a2.set_xlabel("Flagged runs, sorted by total time"); a2.set_ylabel("Time to confirmed freeze (ms)")
a2.set_xticks([])
tot = [p + f for p, f in zip(proc, frz)]
share = np.median([f / t for f, t in zip(frz, tot)]) * 100
a2.text(0.5, max(tot) * 0.62, f"The freeze itself is a median\n{share:.2f}% of the total.", fontsize=6.2, color="#8E3B8E",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CC79A7", lw=0.6))
a2.set_title("(b) Where the time goes before containment", loc="left")
a2.legend(loc="upper left", frameon=True, fontsize=5.8)
fig.tight_layout(w_pad=1.5)
fig.savefig(OUT + "fig6_containment.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig(OUT + "fig6_containment.png", dpi=170, bbox_inches="tight", pad_inches=0.03)
plt.close(fig)
print("share median freeze %", share, "n", len(Es))
