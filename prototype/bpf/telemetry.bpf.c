// SPDX-License-Identifier: GPL-2.0
/*
 * Syscall telemetry probe with optional in-kernel Q16.16 linear classifier.
 *
 * Events are recorded only when (a) user space has armed the probe by
 * writing a non-zero anchor time, (b) the calling task belongs to the
 * target cgroup v2, and (c) the event time is at or after the anchor.
 *
 * When cfg.infer is set, every recorded event also updates running
 * counts for the current window (window index = (t - anchor) / window_ns)
 * and evaluates logit = b + sum(w[i] * count[i]) in Q16.16 fixed point.
 * The first time the logit reaches 0 (p >= 0.5) in a window, an ALERT
 * record is pushed to the same ring buffer.
 *
 * The state update is not atomic across CPUs. It is exact on one CPU and
 * approximate under concurrent events on several CPUs.
 */
#include <linux/types.h>
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

char LICENSE[] SEC("license") = "GPL";

#define NF 5            /* exec, open, connect, unlink, unique_pids */
#define EV_EXEC 1
#define EV_OPEN 2
#define EV_CONNECT 3
#define EV_UNLINK 4
#define EV_ALERT 100

struct cfg {
    __u64 target_cgid;
    __u64 anchor_ns;     /* 0 = not armed */
    __u64 window_ns;
    __u64 infer;         /* 1 = run in-kernel classifier */
    __s64 w_q16[NF];
    __s64 b_q16;
};

struct state {
    __u64 widx_plus1;    /* current window index + 1 (0 = none yet) */
    __u64 alerted_plus1; /* window index + 1 of last alert */
    __u64 cnt[NF];
};

struct counters {
    __u64 generated;
    __u64 submitted;
    __u64 reservation_failures;
    __u64 alerts;
};

struct event {
    __u64 t0_ns;     /* kernel time of the syscall entry */
    __u64 t_dec_ns;  /* ALERT only: kernel time after the decision */
    __u64 seq;
    __u64 widx;
    __s64 aux;       /* ALERT only: logit in Q16.16 */
    __u32 type;
    __u32 pid;
    __u32 tid;
    __u32 cpu;
};

struct { __uint(type, BPF_MAP_TYPE_RINGBUF); __uint(max_entries, 1 << 22); } events SEC(".maps");
struct { __uint(type, BPF_MAP_TYPE_ARRAY); __uint(max_entries, 1); __type(key, __u32); __type(value, struct cfg); } cfg_map SEC(".maps");
struct { __uint(type, BPF_MAP_TYPE_ARRAY); __uint(max_entries, 1); __type(key, __u32); __type(value, struct state); } state_map SEC(".maps");
struct { __uint(type, BPF_MAP_TYPE_ARRAY); __uint(max_entries, 1); __type(key, __u32); __type(value, struct counters); } counters SEC(".maps");
struct { __uint(type, BPF_MAP_TYPE_LRU_HASH); __uint(max_entries, 8192); __type(key, __u32); __type(value, __u64); } pid_win SEC(".maps");

static __always_inline void infer(struct cfg *cf, struct counters *c, __u64 t, __u32 type, __u32 pid)
{
    __u32 k = 0;
    struct state *st = bpf_map_lookup_elem(&state_map, &k);
    if (!st || cf->window_ns == 0)
        return;

    __u64 w1 = (t - cf->anchor_ns) / cf->window_ns + 1;
    if (st->widx_plus1 != w1) {
        st->widx_plus1 = w1;
        st->cnt[0] = 0; st->cnt[1] = 0; st->cnt[2] = 0; st->cnt[3] = 0; st->cnt[4] = 0;
    }
    switch (type) {
    case EV_EXEC: st->cnt[0]++; break;
    case EV_OPEN: st->cnt[1]++; break;
    case EV_CONNECT: st->cnt[2]++; break;
    case EV_UNLINK: st->cnt[3]++; break;
    }
    __u64 *seen = bpf_map_lookup_elem(&pid_win, &pid);
    if (!seen || *seen != w1) {
        bpf_map_update_elem(&pid_win, &pid, &w1, BPF_ANY);
        st->cnt[4]++;
    }

    __s64 logit = cf->b_q16;
    logit += cf->w_q16[0] * (__s64)st->cnt[0];
    logit += cf->w_q16[1] * (__s64)st->cnt[1];
    logit += cf->w_q16[2] * (__s64)st->cnt[2];
    logit += cf->w_q16[3] * (__s64)st->cnt[3];
    logit += cf->w_q16[4] * (__s64)st->cnt[4];

    if (logit >= 0 && st->alerted_plus1 != w1) {
        st->alerted_plus1 = w1;
        __sync_fetch_and_add(&c->alerts, 1);
        struct event *a = bpf_ringbuf_reserve(&events, sizeof(*a), 0);
        if (!a) {
            __sync_fetch_and_add(&c->reservation_failures, 1);
            return;
        }
        a->t0_ns = t;
        a->t_dec_ns = bpf_ktime_get_ns();
        a->seq = 0;
        a->widx = w1 - 1;
        a->aux = logit;
        a->type = EV_ALERT;
        a->pid = pid;
        a->tid = 0;
        a->cpu = bpf_get_smp_processor_id();
        bpf_ringbuf_submit(a, 0);
    }
}

static __always_inline int emit_event(__u32 type)
{
    __u32 k = 0;
    struct cfg *cf = bpf_map_lookup_elem(&cfg_map, &k);
    if (!cf || cf->anchor_ns == 0)
        return 0;
    if (bpf_get_current_cgroup_id() != cf->target_cgid)
        return 0;
    __u64 t = bpf_ktime_get_ns();
    if (t < cf->anchor_ns)
        return 0;

    struct counters *c = bpf_map_lookup_elem(&counters, &k);
    if (!c)
        return 0;
    __sync_fetch_and_add(&c->generated, 1);

    __u64 id = bpf_get_current_pid_tgid();
    __u32 pid = (__u32)(id >> 32);
    struct event *e = bpf_ringbuf_reserve(&events, sizeof(*e), 0);
    if (!e) {
        __sync_fetch_and_add(&c->reservation_failures, 1);
    } else {
        e->t0_ns = t;
        e->t_dec_ns = 0;
        e->seq = __sync_fetch_and_add(&c->submitted, 1) + 1;
        e->widx = cf->window_ns ? (t - cf->anchor_ns) / cf->window_ns : 0;
        e->aux = 0;
        e->type = type;
        e->pid = pid;
        e->tid = (__u32)id;
        e->cpu = bpf_get_smp_processor_id();
        bpf_ringbuf_submit(e, 0);
    }
    if (cf->infer)
        infer(cf, c, t, type, pid);
    return 0;
}

SEC("tracepoint/syscalls/sys_enter_execve")
int handle_exec(void *ctx) { return emit_event(EV_EXEC); }

SEC("tracepoint/syscalls/sys_enter_openat")
int handle_open(void *ctx) { return emit_event(EV_OPEN); }

SEC("tracepoint/syscalls/sys_enter_connect")
int handle_connect(void *ctx) { return emit_event(EV_CONNECT); }

SEC("tracepoint/syscalls/sys_enter_unlink")
int handle_unlink(void *ctx) { return emit_event(EV_UNLINK); }

SEC("tracepoint/syscalls/sys_enter_unlinkat")
int handle_unlinkat(void *ctx) { return emit_event(EV_UNLINK); }
