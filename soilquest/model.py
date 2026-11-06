"""Small Gaussian process: fitted only to acquired measurements."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import cho_factor,cho_solve
MODEL=Path(__file__).resolve().parents[1]/'models/hyperparameters.json'

def predict(coords,records,params=None):
    if params is None: params=json.loads(MODEL.read_text())
    try:
        values=np.array([params[k] for k in ('length_m','mean','amplitude','noise_mgkg')],dtype=float)
        if values.shape!=(4,) or not np.isfinite(values).all() or values[0]<=0 or values[2]<=0 or values[3]<0:raise ValueError('invalid GP parameters')
    except (KeyError,TypeError,ValueError) as exc:raise ValueError('finite GP parameters with positive length/amplitude and nonnegative noise required') from exc
    params=dict(zip(('length_m','mean','amplitude','noise_mgkg'),values))
    indices=[]
    for record in records:
        index=record.get('index');value=record.get('value')
        if isinstance(index,(bool,np.bool_)) or not isinstance(index,(int,np.integer)) or not 0<=index<len(coords) or index in indices:raise ValueError('unique in-range integer observation indices required')
        if not isinstance(value,(int,float,np.integer,np.floating)) or isinstance(value,(bool,np.bool_)) or not np.isfinite(value):raise ValueError('finite numeric observations required')
        indices.append(index)
    if not records:return np.full(len(coords),params['mean']),np.full(len(coords),params['amplitude'])
    indices=[r['index'] for r in records]; points=coords[indices]; values=np.array([r['value'] for r in records]); length=params['length_m']; amp=params['amplitude']
    def kernel(a,b):return amp**2*np.exp(-np.sum((a[:,None]-b[None,:])**2,axis=2)/(2*length**2))
    cov=kernel(points,points)+np.eye(len(points))*params['noise_mgkg']**2
    fac=cho_factor(cov); k=kernel(coords,points)
    mean=params['mean']+k@cho_solve(fac,values-params['mean'])
    var=amp**2-np.einsum('ij,ji->i',k,cho_solve(fac,k.T))
    return np.maximum(0,mean),np.sqrt(np.maximum(var,1e-8))
