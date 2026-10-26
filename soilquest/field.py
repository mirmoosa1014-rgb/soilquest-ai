"""Synthetic stochastic spatial generator; no physical PDE is claimed."""
import numpy as np
FAMILIES={'train':['smooth','multiple','background'],'test':['narrow','directional']}

def generate(seed=41,family='narrow',n=18):
    if family not in sum(FAMILIES.values(),[]): raise ValueError('unknown field family')
    if not 10<=n<=24: raise ValueError('grid size must be 10..24')
    rng=np.random.default_rng(seed); x,y=np.meshgrid(np.linspace(0,100,n),np.linspace(0,100,n)); z=np.full_like(x,12.)
    count=3 if family=='multiple' else 1
    for _ in range(count):
        cx,cy=rng.uniform(20,80,2); width=5 if family=='narrow' else 19
        sx,sy=(30,8) if family=='directional' else (width,width)
        z+=rng.uniform(65,115)*np.exp(-.5*((x-cx)**2/sx**2+(y-cy)**2/sy**2))
    if family=='background': z=12+9*np.sin(x/40)+4*np.cos(y/30)
    z+=2*np.sin((x+y)/22)
    obstacles=np.zeros((n,n),bool); obstacles[3:n-4,n//2]=True; obstacles[n//2,n//2]=False
    return {'coords':np.column_stack([x.ravel(),y.ravel()]),'truth':np.maximum(0,z.ravel()),'obstacles':obstacles.ravel(),'n':n,'seed':seed,'family':family}

class Sampler:
    def __init__(self,field): self._field=field; self.records=[]
    def sample(self,index):
        if not isinstance(index,(int,np.integer)) or not 0<=index<len(self._field['truth']): raise ValueError('invalid sample cell')
        if index in [r['index'] for r in self.records]: raise ValueError('duplicate sample')
        if self._field['obstacles'][index]: raise ValueError('blocked cell')
        # Cell-indexed noise gives identical potential measurements to all policies.
        noise=np.random.default_rng(self._field['seed']*1000+index).normal(0,3)
        record={'index':int(index),'value':float(max(0,self._field['truth'][index]+noise))}; self.records.append(record); return record
