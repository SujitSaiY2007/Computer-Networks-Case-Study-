from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable
import json

EVENT_NAMES={1:"exec_count",2:"open_count",3:"connect_count",4:"unlink_count"}
FEATURE_NAMES=["exec_count","open_count","connect_count","unlink_count","unique_process_count","failed_operation_count","event_count","event_rate","event_loss_rate"]

@dataclass
class Window:
    start_ns:int
    end_ns:int
    counts:dict[str,int]
    pids:set[int]
    failed:int=0

    def vector(self, loss_rate:float=0.0)->dict[str,float]:
        d={k:float(self.counts.get(k,0)) for k in EVENT_NAMES.values()}
        d["unique_process_count"]=float(len(self.pids))
        d["failed_operation_count"]=float(self.failed)
        d["event_count"]=float(sum(self.counts.values()))
        duration=max((self.end_ns-self.start_ns)/1e9,1e-9)
        d["event_rate"]=d["event_count"]/duration
        d["event_loss_rate"]=float(loss_rate)
        return d

def aggregate(events:Iterable[dict],window_ns:int=1_000_000_000,loss_rate:float=0.0):
    windows={}
    for e in events:
        t=int(e["t0_ns"])
        start=(t//window_ns)*window_ns
        w=windows.get(start)
        if w is None:
            w=Window(start,start+window_ns,defaultdict(int),set())
            windows[start]=w
        name=EVENT_NAMES.get(int(e["event_type"]))
        if name:
            w.counts[name]+=1
        w.pids.add(int(e["pid"]))
        if int(e.get("status",0))<0:
            w.failed+=1
    return [w.vector(loss_rate) | {"window_start_ns":w.start_ns,"window_end_ns":w.end_ns} for w in sorted(windows.values(),key=lambda x:x.start_ns)]

def load_jsonl(path:str):
    with open(path,encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r=json.loads(line)
                if r.get("record_type")=="event":
                    yield r
