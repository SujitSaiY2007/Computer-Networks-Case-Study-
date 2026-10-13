#include <linux/types.h>
#include "bpf_helpers_min.h"

char LICENSE[] SEC("license") = "GPL";

/*
 * Gate G: Fixed-point Kernel-local Logistic Regression Feasibility Probe
 *
 * Floating-point arithmetic is forbidden in eBPF.
 * Representation: Fixed-point Q16.16 (scaled by 65536).
 * Features (9):
 *   0: exec_count
 *   1: open_count
 *   2: connect_count
 *   3: unlink_count
 *   4: unique_process_count
 *   5: failed_operation_count
 *   6: event_count
 *   7: event_rate (events/sec in Q16.16)
 *   8: event_loss_rate (ratio in Q16.16, e.g. 0.05 * 65536)
 */

#define SCALE_FP 65536LL
#define NUM_FEATURES 9

struct model_params {
    __s64 weights[NUM_FEATURES]; /* Q16.16 fixed-point */
    __s64 intercept;             /* Q16.16 fixed-point */
    __s64 threshold_logit;       /* logit corresponding to threshold (0 for p=0.5) */
};

struct {
    __uint(type, 2); /* BPF_MAP_TYPE_ARRAY */
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct model_params);
} model_map SEC(".maps");

struct inference_result {
    __s64 logit_q16;
    __u32 predicted_class;
};

struct {
    __uint(type, 2); /* BPF_MAP_TYPE_ARRAY */
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct inference_result);
} result_map SEC(".maps");

static __always_inline int predict_fixed_point(const __s64 *features, struct inference_result *res)
{
    __u32 key = 0;
    struct model_params *mp = bpf_map_lookup_elem(&model_map, &key);
    if (!mp)
        return -1;

    __s64 dot = mp->intercept;
    #pragma unroll
    for (int i = 0; i < NUM_FEATURES; ++i) {
        /* features[i] in integer, weights[i] in Q16.16 -> sum stays in Q16.16 */
        dot += mp->weights[i] * features[i];
    }

    res->logit_q16 = dot;
    res->predicted_class = (dot >= mp->threshold_logit) ? 1 : 0;
    return 0;
}

SEC("tracepoint/syscalls/sys_enter_execve")
int test_kernel_lr(void *ctx)
{
    (void)ctx;
    __s64 test_features[NUM_FEATURES] = {
        10,  /* exec */
        50,  /* open */
        2,   /* connect */
        5,   /* unlink */
        4,   /* procs */
        0,   /* failed */
        67,  /* events */
        67 * SCALE_FP, /* rate */
        0    /* loss */
    };

    __u32 rkey = 0;
    struct inference_result *r = bpf_map_lookup_elem(&result_map, &rkey);
    if (!r)
        return 0;

    predict_fixed_point(test_features, r);
    return 0;
}
