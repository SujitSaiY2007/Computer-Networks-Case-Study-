#ifndef CHAT07_BPF_HELPERS_MIN_H
#define CHAT07_BPF_HELPERS_MIN_H

#define SEC(name) __attribute__((section(name), used))
#define __uint(name, val) int (*name)[val]
#define __type(name, val) typeof(val) *name
#define __array(name, val) typeof(val) *name[]
#define __always_inline inline __attribute__((always_inline))
static void *(*bpf_map_lookup_elem)(void *map, const void *key) = (void *)1;
static unsigned int (*bpf_get_smp_processor_id)(void) = (void *)8;
#define __ulong(name, val) enum { ___bpf_concat(name, __LINE__) = val }

static void *(*bpf_ringbuf_reserve)(void *ringbuf, unsigned long size, unsigned long flags) = (void *)131;
static void (*bpf_ringbuf_submit)(void *data, unsigned long flags) = (void *)132;
static void (*bpf_ringbuf_discard)(void *data, unsigned long flags) = (void *)133;
static unsigned long long (*bpf_ktime_get_ns)(void) = (void *)5;
static unsigned long long (*bpf_get_current_pid_tgid)(void) = (void *)14;
static unsigned long long (*bpf_get_current_cgroup_id)(void) = (void *)80;

#endif
