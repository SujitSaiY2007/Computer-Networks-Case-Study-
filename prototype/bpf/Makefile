CLANG ?= clang
CC ?= cc
BPF_CFLAGS := -O2 -g -target bpf -D__TARGET_ARCH_x86 -I.
USER_CFLAGS := -O2 -g -std=c11 -Wall -Wextra

all: telemetry.bpf.o telemetry_loader

telemetry.bpf.o: telemetry.bpf.c bpf_helpers_min.h
	$(CLANG) $(BPF_CFLAGS) -c $< -o $@

telemetry_loader: telemetry_loader.c
	$(CC) $(USER_CFLAGS) $< -o $@ -lbpf -lelf -lz

clean:
	rm -f telemetry.bpf.o telemetry_loader
