from __future__ import annotations
import argparse,subprocess
def cgroup_paths(pid):
    with open(f"/proc/{pid}/cgroup",encoding="utf-8") as f: return [line.strip() for line in f if line.strip()]
def docker_pid(container):
    return int(subprocess.check_output(["docker","inspect","-f","{{.State.Pid}}",container],text=True).strip())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--container",required=True); args=ap.parse_args()
    pid=docker_pid(args.container); print(f"container={args.container}"); print(f"pid={pid}")
    for row in cgroup_paths(pid): print(f"cgroup={row}")
if __name__=="__main__": main()
