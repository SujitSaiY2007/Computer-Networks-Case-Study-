#include <linux/types.h>
#include "bpf_helpers_min.h"

char LICENSE[] SEC("license") = "GPL";

enum event_type {
    EVENT_EXEC = 1,
    EVENT_OPEN = 2,
    EVENT_CONNECT = 3,
    EVENT_UNLINK = 4,
};

struct telemetry_event {
    __u64 t0_ns;
    __u64 seq;
    __u32 event_type;
    __u32 pid;
    __u32 tid;
    __u32 cpu;
    __u64 cgroup_id;
    __s32 status;
    __u32 reserved;
};

struct telemetry_counters {
    __u64 generated;
    __u64 submitted;
    __u64 reservation_failures;
};

struct {
    __uint(type, 27); /* BPF_MAP_TYPE_RINGBUF */
    __uint(max_entries, 1 << 20);
} events SEC(".maps");

struct {
    __uint(type, 2); /* BPF_MAP_TYPE_ARRAY */
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct telemetry_counters);
} counters SEC(".maps");

static __always_inline int emit_event(__u32 type)
{
    __u32 key = 0;
    struct telemetry_counters *c = bpf_map_lookup_elem(&counters, &key);
    struct telemetry_event *e;
    __u64 id = bpf_get_current_pid_tgid();
    __u64 cg = bpf_get_current_cgroup_id();
    if (c) __sync_fetch_and_add(&c->generated, 1);

    e = bpf_ringbuf_reserve(&events, sizeof(*e), 0);
    if (!e) {
        if (c) __sync_fetch_and_add(&c->reservation_failures, 1);
        return 0;
    }

    e->t0_ns = bpf_ktime_get_ns();
    e->seq = c ? __sync_fetch_and_add(&c->submitted, 1) + 1 : e->t0_ns ^ id;
    e->event_type = type;
    e->pid = (__u32)(id >> 32);
    e->tid = (__u32)id;
    e->cpu = bpf_get_smp_processor_id();
    e->cgroup_id = cg;
    e->status = 0;
    e->reserved = 0;
    bpf_ringbuf_submit(e, 0);
    return 0;
}

SEC("tracepoint/syscalls/sys_enter_execve")
int handle_exec(void *ctx) { (void)ctx; return emit_event(EVENT_EXEC); }

SEC("tracepoint/syscalls/sys_enter_openat")
int handle_open(void *ctx) { (void)ctx; return emit_event(EVENT_OPEN); }

SEC("tracepoint/syscalls/sys_enter_connect")
int handle_connect(void *ctx) { (void)ctx; return emit_event(EVENT_CONNECT); }

SEC("tracepoint/syscalls/sys_enter_unlinkat")
int handle_unlink(void *ctx) { (void)ctx; return emit_event(EVENT_UNLINK); }
