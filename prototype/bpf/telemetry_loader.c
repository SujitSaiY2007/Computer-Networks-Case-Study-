#define _GNU_SOURCE
#include <errno.h>
#include <inttypes.h>
#include <linux/bpf.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <time.h>
#include <unistd.h>

struct bpf_object;
struct bpf_program;
struct bpf_link;
struct bpf_map;
struct ring_buffer;

struct bpf_object *bpf_object__open_file(const char *, const void *);
int bpf_object__load(struct bpf_object *);
struct bpf_program *bpf_object__find_program_by_name(const struct bpf_object *, const char *);
struct bpf_link *bpf_program__attach_tracepoint(const struct bpf_program *, const char *, const char *);
struct bpf_map *bpf_object__find_map_by_name(const struct bpf_object *, const char *);
int bpf_map__fd(const struct bpf_map *);
long libbpf_get_error(const void *);
void bpf_object__close(struct bpf_object *);
long bpf_link__destroy(struct bpf_link *);
struct ring_buffer *ring_buffer__new(int, int (*)(void *, void *, size_t), void *, const void *);
int ring_buffer__poll(struct ring_buffer *, int);
int ring_buffer__consume(struct ring_buffer *);
void ring_buffer__free(struct ring_buffer *);

static volatile sig_atomic_t stop;
static uint64_t consumed;
static uint64_t min_seq;
static uint64_t max_seq;

struct telemetry_counters { uint64_t generated; uint64_t submitted; uint64_t reservation_failures; };

struct event {
    uint64_t t0_ns;
    uint64_t seq;
    uint32_t event_type;
    uint32_t pid;
    uint32_t tid;
    uint32_t cpu;
    uint64_t cgroup_id;
    int32_t status;
    uint32_t reserved;
};

static void on_signal(int sig) { (void)sig; stop = 1; }

static int sample_cb(void *ctx, void *data, size_t size)
{
    (void)ctx;
    if (size < sizeof(struct event))
        return 0;
    const struct event *e = (const struct event *)data;
    if (consumed == 0) {
        min_seq = e->seq;
        max_seq = e->seq;
    } else {
        if (e->seq < min_seq) min_seq = e->seq;
        if (e->seq > max_seq) max_seq = e->seq;
    }
    consumed++;

    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    uint64_t now_ns = (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
    uint64_t transfer_ns = (now_ns > e->t0_ns) ? (now_ns - e->t0_ns) : 0;

    printf("{\"record_type\":\"event\",\"t0_ns\":%" PRIu64 ",\"seq\":%" PRIu64 ",\"event_type\":%u,\"pid\":%u,\"tid\":%u,\"cpu\":%u,\"cgroup_id\":%" PRIu64 ",\"status\":%d,\"transfer_ns\":%" PRIu64 "}\n",
           e->t0_ns, e->seq, e->event_type, e->pid, e->tid, e->cpu, e->cgroup_id, e->status, transfer_ns);
    return 0;
}

static int map_lookup(int fd, uint32_t key, void *value)
{
    union bpf_attr attr;
    memset(&attr, 0, sizeof(attr));
    attr.map_fd = fd;
    attr.key = (uint64_t)(uintptr_t)&key;
    attr.value = (uint64_t)(uintptr_t)value;
    return syscall(__NR_bpf, BPF_MAP_LOOKUP_ELEM, &attr, sizeof(attr));
}

static void usage(const char *p)
{
    fprintf(stderr, "usage: %s <bpf-object> [--duration seconds]\n", p);
}

int main(int argc, char **argv)
{
    const char *obj_path = "./telemetry.bpf.o";
    int duration = 10;
    if (argc >= 2 && argv[1][0] != '-') obj_path = argv[1];
    for (int i = 1; i < argc; ++i) {
        if (!strcmp(argv[i], "--duration") && i + 1 < argc) duration = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--help")) { usage(argv[0]); return 0; }
    }

    signal(SIGINT, on_signal);
    signal(SIGTERM, on_signal);
    setlinebuf(stdout);

    struct bpf_object *obj = bpf_object__open_file(obj_path, NULL);
    long err = libbpf_get_error(obj);
    if (err) {
        fprintf(stderr, "OPEN_FAIL=%ld\n", err);
        return 2;
    }
    if (bpf_object__load(obj) != 0) {
        fprintf(stderr, "LOAD_FAIL: kernel rejected BPF object\n");
        bpf_object__close(obj);
        return 3;
    }

    const char *names[] = {"handle_exec","handle_open","handle_connect","handle_unlink"};
    const char *tp[] = {"sys_enter_execve","sys_enter_openat","sys_enter_connect","sys_enter_unlinkat"};
    struct bpf_link *links[4] = {0};
    for (int i = 0; i < 4; ++i) {
        struct bpf_program *p = bpf_object__find_program_by_name(obj, names[i]);
        if (!p) { fprintf(stderr, "PROGRAM_NOT_FOUND=%s\n", names[i]); return 4; }
        links[i] = bpf_program__attach_tracepoint(p, "syscalls", tp[i]);
        if (libbpf_get_error(links[i])) {
            fprintf(stderr, "ATTACH_FAIL=%s\n", tp[i]);
            return 5;
        }
    }

    struct bpf_map *map = bpf_object__find_map_by_name(obj, "events");
    if (!map) { fprintf(stderr, "RINGBUF_MAP_NOT_FOUND\n"); return 6; }

    int map_fd = bpf_map__fd(map);
    struct ring_buffer *rb = ring_buffer__new(map_fd, sample_cb, NULL, NULL);
    if (!rb) { fprintf(stderr, "RINGBUF_INIT_FAIL\n"); return 7; }

    fprintf(stderr, "TELEMETRY_RUNNING duration=%d\n", duration);
    struct timespec start_ts, now_ts;
    clock_gettime(CLOCK_MONOTONIC, &start_ts);
    while (!stop) {
        clock_gettime(CLOCK_MONOTONIC, &now_ts);
        int64_t elapsed_ms = ((int64_t)now_ts.tv_sec - (int64_t)start_ts.tv_sec) * 1000LL +
                             ((int64_t)now_ts.tv_nsec - (int64_t)start_ts.tv_nsec) / 1000000LL;
        if (elapsed_ms >= (int64_t)duration * 1000LL)
            break;
        int64_t remain_ms = (int64_t)duration * 1000LL - elapsed_ms;
        int timeout_ms = (remain_ms > 100) ? 100 : (int)remain_ms;
        int rc = ring_buffer__poll(rb, timeout_ms);
        if (rc < 0 && rc != -EINTR) {
            fprintf(stderr, "RINGBUF_POLL_FAIL=%d\n", rc);
            break;
        }
    }

    // At shutdown: destroy all 4 links first
    for (int i = 0; i < 4; ++i) {
        if (links[i]) {
            bpf_link__destroy(links[i]);
            links[i] = NULL;
        }
    }

    // Call ring_buffer__consume(rb) until it returns 0
    while (ring_buffer__consume(rb) > 0) {
    }

    // Read the counters map
    struct telemetry_counters c = {0};
    struct bpf_map *cmap = bpf_object__find_map_by_name(obj, "counters");
    if (cmap) {
        int cfd = bpf_map__fd(cmap);
        map_lookup(cfd, 0, &c);
    }

    uint64_t sequence_gaps = 0;
    if (consumed > 0 && max_seq >= min_seq) {
        uint64_t expected = (max_seq - min_seq + 1);
        if (expected > consumed)
            sequence_gaps = expected - consumed;
    }

    printf("{\"record_type\":\"stats\",\"generated_events\":%" PRIu64 ",\"submitted_events\":%" PRIu64 ",\"reservation_failures\":%" PRIu64 ",\"consumed_events\":%" PRIu64 ",\"sequence_gaps\":%" PRIu64 "}\n",
           c.generated, c.submitted, c.reservation_failures, consumed, sequence_gaps);

    ring_buffer__free(rb);
    bpf_object__close(obj);
    return 0;
}
