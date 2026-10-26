"""Small Gaussian process: fitted only to acquired measurements."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import cho_factor,cho_solve
MODEL=Path(__file__).resolve().parents[1]/'models/hyperparameters.json'

def predict(coords,records,params=None):
    if params is None: params=json.loads(MODEL.read_text())
    if not records:return np.full(len(coords),params['mean']),np.full(len(coords),params['amplitude'])
    indices=[r['index'] for r in records]; points=coords[indices]; values=np.array([r['value'] for r in records]); length=params['length_m']; amp=params['amplitude']
    def kernel(a,b):return amp**2*np.exp(-np.sum((a[:,None]-b[None,:])**2,axis=2)/(2*length**2))
    cov=kernel(points,points)+np.eye(len(points))*params['noise_mgkg']**2
    fac=cho_factor(cov); k=kernel(coords,points)
    mean=params['mean']+k@cho_solve(fac,values-params['mean'])
    var=amp**2-np.einsum('ij,ji->i',k,cho_solve(fac,k.T))
    return np.maximum(0,mean),np.sqrt(np.maximum(var,1e-8))
