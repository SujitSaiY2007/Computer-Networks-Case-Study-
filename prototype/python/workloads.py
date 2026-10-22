from __future__ import annotations
import argparse,os,socket,subprocess,time,tempfile
from pathlib import Path

def idle(duration): time.sleep(duration)
def file_processing(duration,seed=0):
    root=Path(tempfile.mkdtemp(prefix="chat07-files-"))
    try:
        end=time.monotonic()+duration; i=0
        while time.monotonic()<end:
            p=root/f"f-{seed}-{i%32}.dat"; p.write_bytes(b"chat07"*128); _=p.read_bytes()
            if i%4==0: p.unlink(missing_ok=True)
            i+=1
    finally:
        for p in root.glob("*"): p.unlink(missing_ok=True)
        root.rmdir()
def process_churn(duration):
    end=time.monotonic()+duration
    while time.monotonic()<end:
        p=subprocess.Popen(["true"]); p.wait()
def local_client_server(duration,port=39077):
    import threading
    end=time.monotonic()+duration
    srv=socket.socket(); srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    try:
        srv.bind(("127.0.0.1",port)); srv.listen(16); srv.settimeout(.1)
    except OSError:
        pass
    def client_worker():
        while time.monotonic()<end:
            try:
                c=socket.create_connection(("127.0.0.1",port),timeout=.05)
                c.sendall(b"ping"); _=c.recv(16); c.close()
                time.sleep(0.01)
            except OSError:
                time.sleep(0.01)
    cw=threading.Thread(target=client_worker,daemon=True); cw.start()
    try:
        while time.monotonic()<end:
            try:
                c,_=srv.accept(); c.recv(64); c.sendall(b"ok"); c.close()
            except (TimeoutError, OSError): pass
    finally:
        try: srv.close()
        except OSError: pass
        cw.join(timeout=0.1)
def exec_burst(duration,count=100):
    end=time.monotonic()+duration
    while time.monotonic()<end:
        for _ in range(count): subprocess.run(["true"],check=True)
def abnormal_file_access(duration): file_processing(duration,seed=991)
def local_connection_burst(duration,port=39078):
    import threading
    end=time.monotonic()+duration
    srv=socket.socket(); srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    try:
        srv.bind(("127.0.0.1",port)); srv.listen(64); srv.settimeout(.1)
    except OSError:
        srv=None
    def sink_worker():
        if not srv: return
        while time.monotonic()<end:
            try:
                c,_=srv.accept(); c.close()
            except (TimeoutError, OSError): pass
    if srv:
        sw=threading.Thread(target=sink_worker,daemon=True); sw.start()
    try:
        while time.monotonic()<end:
            try:
                s=socket.create_connection(("127.0.0.1",port),timeout=.05); s.sendall(b"x"); s.close()
            except OSError: pass
    finally:
        if srv:
            try: srv.close()
            except OSError: pass
WORKLOADS={"B1":idle,"B2":file_processing,"B3":process_churn,"B4":local_client_server,"A1":exec_burst,"A2":abnormal_file_access,"A3":local_connection_burst}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("workload",choices=sorted(WORKLOADS)); ap.add_argument("--duration",type=float,default=10); ap.add_argument("--seed",type=int,default=0)
    args=ap.parse_args(); fn=WORKLOADS[args.workload]
    t0=time.monotonic()
    if args.workload=="B2": fn(args.duration,args.seed)
    else: fn(args.duration)
    t1=time.monotonic()
    measured_duration_s=t1-t0
    print({"workload_id":args.workload,"duration":args.duration,"seed":args.seed,"pid":os.getpid(),"measured_duration_s":measured_duration_s})
if __name__=="__main__": main()
