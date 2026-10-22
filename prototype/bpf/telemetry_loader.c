// SPDX-License-Identifier: GPL-2.0
/*
 * Loads telemetry.bpf.o, attaches the four syscall tracepoints and streams
 * records to stdout as JSON lines.
 *
 * Protocol:
 *   1. prints {"r":"ready"} after load and attach
 *   2. waits for one stdin line: "GO <anchor_ns>" (CLOCK_MONOTONIC ns)
 *   3. arms the probe, prints {"r":"armed"} and streams events
 *   4. on SIGTERM/SIGINT or after --max-seconds: drains the ring buffer,
 *      prints {"r":"stats",...} and exits 0
 *
 * Usage:
 *   telemetry_loader telemetry.bpf.o --cgroup /sys/fs/cgroup/unified/x
 *       [--window-ms 1000] [--max-seconds 60]
 *       [--infer --w w0,w1,w2,w3,w4 --b b]   (Q16.16 integers)
 */
#define _GNU_SOURCE
#include <errno.h>
#include <inttypes.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
#include <bpf/bpf.h>
#include <bpf/libbpf.h>

#define NF 5
struct cfg { uint64_t target_cgid, anchor_ns, window_ns, infer; int64_t w_q16[NF]; int64_t b_q16; };
struct counters { uint64_t generated, submitted, reservation_failures, alerts; };
struct event { uint64_t t0_ns, t_dec_ns, seq, widx; int64_t aux; uint32_t type, pid, tid, cpu; };

static volatile sig_atomic_t stop;
static uint64_t consumed, alerts_seen, min_seq, max_seq;

static void on_signal(int s) { (void)s; stop = 1; }

static uint64_t now_ns(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

static int on_record(void *ctx, void *data, size_t size)
{
    (void)ctx;
    if (size < sizeof(struct event))
        return 0;
    const struct event *e = data;
    uint64_t tr = now_ns();
    if (e->type == 100) {
        alerts_seen++;
        printf("{\"r\":\"a\",\"t0\":%" PRIu64 ",\"td\":%" PRIu64 ",\"tr\":%" PRIu64 ",\"w\":%" PRIu64 ",\"logit_q16\":%" PRId64 "}\n",
               e->t0_ns, e->t_dec_ns, tr, e->widx, e->aux);
        return 0;
    }
    if (consumed == 0 || e->seq < min_seq)
        min_seq = e->seq;
    if (e->seq > max_seq)
        max_seq = e->seq;
    consumed++;
    printf("{\"r\":\"e\",\"t0\":%" PRIu64 ",\"tr\":%" PRIu64 ",\"seq\":%" PRIu64 ",\"ty\":%u,\"pid\":%u,\"w\":%" PRIu64 "}\n",
           e->t0_ns, tr, e->seq, e->type, e->pid, e->widx);
    return 0;
}

static int parse_list(const char *s, int64_t *out, int n)
{
    char *dup = strdup(s), *tok, *save = NULL;
    int i = 0;
    for (tok = strtok_r(dup, ",", &save); tok && i < n; tok = strtok_r(NULL, ",", &save))
        out[i++] = strtoll(tok, NULL, 10);
    free(dup);
    return i == n ? 0 : -1;
}

int main(int argc, char **argv)
{
    const char *obj_path = NULL, *cg_path = NULL;
    int window_ms = 1000, max_s = 60, infer = 0;
    int64_t w[NF] = {0}, b = 0;

    for (int i = 1; i < argc; ++i) {
        if (!strcmp(argv[i], "--cgroup") && i + 1 < argc) cg_path = argv[++i];
        else if (!strcmp(argv[i], "--window-ms") && i + 1 < argc) window_ms = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--max-seconds") && i + 1 < argc) max_s = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--infer")) infer = 1;
        else if (!strcmp(argv[i], "--w") && i + 1 < argc) {
            if (parse_list(argv[++i], w, NF)) { fprintf(stderr, "BAD_WEIGHTS\n"); return 1; }
        }
        else if (!strcmp(argv[i], "--b") && i + 1 < argc) b = strtoll(argv[++i], NULL, 10);
        else if (argv[i][0] != '-' && !obj_path) obj_path = argv[i];
        else { fprintf(stderr, "BAD_ARG=%s\n", argv[i]); return 1; }
    }
    if (!obj_path || !cg_path) {
        fprintf(stderr, "usage: %s <obj> --cgroup <cgroup2 dir> [--window-ms N] [--max-seconds N] [--infer --w a,b,c,d,e --b x]\n", argv[0]);
        return 1;
    }

    struct stat sb;
    if (stat(cg_path, &sb) != 0) { fprintf(stderr, "CGROUP_STAT_FAIL=%s\n", cg_path); return 1; }

    signal(SIGINT, on_signal);
    signal(SIGTERM, on_signal);
    setvbuf(stdout, NULL, _IOFBF, 1 << 16);

    struct bpf_object *obj = bpf_object__open_file(obj_path, NULL);
    if (!obj || libbpf_get_error(obj)) { fprintf(stderr, "OPEN_FAIL\n"); return 2; }
    if (bpf_object__load(obj)) { fprintf(stderr, "LOAD_FAIL\n"); return 3; }

    const char *names[5] = {"handle_exec", "handle_open", "handle_connect", "handle_unlink", "handle_unlinkat"};
    struct bpf_program *progs[5];
    struct bpf_link *links[5];
    for (int i = 0; i < 5; ++i) {
        progs[i] = bpf_object__find_program_by_name(obj, names[i]);
        links[i] = progs[i] ? bpf_program__attach(progs[i]) : NULL;
        if (!links[i]) { fprintf(stderr, "ATTACH_FAIL=%s\n", names[i]); return 5; }
    }

    int cfg_fd = bpf_map__fd(bpf_object__find_map_by_name(obj, "cfg_map"));
    int cnt_fd = bpf_map__fd(bpf_object__find_map_by_name(obj, "counters"));
    int ev_fd = bpf_map__fd(bpf_object__find_map_by_name(obj, "events"));
    uint32_t key = 0;
    struct cfg cf = {0};
    cf.target_cgid = (uint64_t)sb.st_ino;
    cf.window_ns = (uint64_t)window_ms * 1000000ull;
    cf.infer = (uint64_t)infer;
    for (int i = 0; i < NF; ++i) cf.w_q16[i] = w[i];
    cf.b_q16 = b;
    if (bpf_map_update_elem(cfg_fd, &key, &cf, BPF_ANY)) { fprintf(stderr, "CFG_WRITE_FAIL\n"); return 6; }

    struct ring_buffer *rb = ring_buffer__new(ev_fd, on_record, NULL, NULL);
    if (!rb) { fprintf(stderr, "RINGBUF_INIT_FAIL\n"); return 7; }

    uint64_t t_start = now_ns();
    printf("{\"r\":\"ready\",\"cgid\":%" PRIu64 "}\n", cf.target_cgid);
    fflush(stdout);

    char line[128];
    if (!fgets(line, sizeof(line), stdin) || strncmp(line, "GO ", 3) != 0) { fprintf(stderr, "NO_GO\n"); return 8; }
    cf.anchor_ns = strtoull(line + 3, NULL, 10);
    if (bpf_map_update_elem(cfg_fd, &key, &cf, BPF_ANY)) { fprintf(stderr, "ARM_FAIL\n"); return 6; }
    printf("{\"r\":\"armed\",\"anchor\":%" PRIu64 "}\n", cf.anchor_ns);
    fflush(stdout);

    /* Time-based loop: ring_buffer__poll returns on every wake-up, so the
       exit condition must be wall-clock time, never an iteration count. */
    uint64_t deadline = now_ns() + (uint64_t)max_s * 1000000000ull;
    while (!stop && now_ns() < deadline) {
        int rc = ring_buffer__poll(rb, 50);
        if (rc < 0 && rc != -EINTR) { fprintf(stderr, "POLL_FAIL=%d\n", rc); break; }
        fflush(stdout);
    }

    /* Disarm, then drain whatever is still in the ring buffer. */
    cf.anchor_ns = 0;
    bpf_map_update_elem(cfg_fd, &key, &cf, BPF_ANY);
    while (ring_buffer__consume(rb) > 0) {}

    struct counters c = {0};
    bpf_map_lookup_elem(cnt_fd, &key, &c);
    uint64_t gaps = 0;
    if (consumed > 0 && max_seq >= min_seq) {
        uint64_t span = max_seq - min_seq + 1;
        if (span > consumed)
            gaps = span - consumed;
    }
    printf("{\"r\":\"stats\",\"generated\":%" PRIu64 ",\"submitted\":%" PRIu64 ",\"consumed\":%" PRIu64
           ",\"reservation_failures\":%" PRIu64 ",\"sequence_gaps\":%" PRIu64 ",\"alerts_kernel\":%" PRIu64
           ",\"alerts_seen\":%" PRIu64 ",\"stopped_by\":\"%s\",\"lifetime_s\":%.6f,\"progs\":{",
           c.generated, c.submitted, consumed, c.reservation_failures, gaps, c.alerts, alerts_seen,
           stop ? "signal" : "deadline", (now_ns() - t_start) / 1e9);
    for (int i = 0; i < 5; ++i) {
        struct bpf_prog_info info;
        uint32_t len = sizeof(info);
        memset(&info, 0, sizeof(info));
        bpf_prog_get_info_by_fd(bpf_program__fd(progs[i]), &info, &len);
        printf("%s\"%s\":{\"run_cnt\":%llu,\"run_time_ns\":%llu,\"recursion_misses\":%llu}", i ? "," : "", names[i],
               (unsigned long long)info.run_cnt, (unsigned long long)info.run_time_ns,
               (unsigned long long)info.recursion_misses);
    }
    printf("}}\n");
    fflush(stdout);

    ring_buffer__free(rb);
    for (int i = 0; i < 5; ++i) bpf_link__destroy(links[i]);
    bpf_object__close(obj);
    return 0;
}
