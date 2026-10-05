from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from .features import FEATURE_NAMES

def _ordered(rows):
    return np.asarray([[float(r[n]) for n in FEATURE_NAMES] for r in rows],dtype=float)

def train(rows, labels, threshold=0.5):
    scaler=StandardScaler()
    X=scaler.fit_transform(_ordered(rows))
    clf=LogisticRegression(random_state=0,solver="liblinear")
    clf.fit(X,labels)
    artifact={
      "schema_version":1,
      "feature_names":FEATURE_NAMES,
      "mean":scaler.mean_.tolist(),
      "scale":scaler.scale_.tolist(),
      "coefficients":clf.coef_[0].tolist(),
      "intercept":float(clf.intercept_[0]),
      "threshold":float(threshold),
      "model_family":"logistic_regression",
    }
    artifact["model_hash"]=hashlib.sha256(json.dumps(artifact,sort_keys=True).encode()).hexdigest()
    return artifact

def score(artifact,row):
    if artifact["feature_names"]!=FEATURE_NAMES:
        raise ValueError("incompatible feature schema")
    x=np.asarray([float(row[n]) for n in FEATURE_NAMES])
    mean=np.asarray(artifact["mean"]); scale=np.asarray(artifact["scale"])
    z=(x-mean)/scale
    logit=float(np.dot(np.asarray(artifact["coefficients"]),z)+artifact["intercept"])
    prob=float(1/(1+np.exp(-logit)))
    return {"score":prob,"predicted_class":int(prob>=artifact["threshold"])}

def save(artifact,path):
    Path(path).write_text(json.dumps(artifact,indent=2,sort_keys=True)+"\n",encoding="utf-8")
