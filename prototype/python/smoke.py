from __future__ import annotations
import argparse,json
from .features import aggregate,FEATURE_NAMES
from .model import train,score
from .policy import Policy,Stage

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--events",required=True)
    args=ap.parse_args()
    events=[]
    with open(args.events,encoding="utf-8") as f:
        for line in f:
            r=json.loads(line)
            if r.get("record_type")=="event": events.append(r)
    rows=aggregate(events)
    if not rows:
        raise SystemExit("SMOKE_FAIL: no events")
    # Deterministic infrastructure test: duplicate feature rows with explicit labels.
    labels=[0 if i%2==0 else 1 for i in range(len(rows))]
    if len(rows)<2:
        rows=rows*2; labels=[0,1]
    artifact=train(rows,labels)
    out=score(artifact,rows[0])
    policy=Policy(artifact["threshold"],allow_mitigation=False)
    stage=policy.evaluate(out["score"],"disposable-test-resource")
    assert stage in (Stage.OBSERVE,Stage.DETECT_LOG)
    assert artifact["feature_names"]==FEATURE_NAMES
    print("SMOKE_PASS")
    print(json.dumps({"rows":len(rows),"prediction":out,"policy_stage":stage.value},sort_keys=True))
if __name__=="__main__": main()
