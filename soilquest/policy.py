"""Policies see posterior, coordinates, obstacles and observed records only."""
from collections import deque
import numpy as np
POLICIES=['random','grid','uncertainty','balanced']

def routes(start,blocked,n):
    parent={start:None}; queue=deque([start])
    while queue:
        node=queue.popleft(); y,x=divmod(node,n)
        for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
            q=yy*n+xx
            if 0<=yy<n and 0<=xx<n and not blocked[q] and q not in parent: parent[q]=node; queue.append(q)
    paths={}
    for q in parent:
        p=[]; cur=q
        while cur is not None:p.append(cur);cur=parent[cur]
        paths[q]=p[::-1]
    return paths

def choose(policy,coords,blocked,n,records,mean,std,remaining,seed):
    if policy not in POLICIES:raise ValueError('unknown policy')
    start=records[-1]['index'] if records else 0; paths=routes(start,blocked,n); visited={r['index'] for r in records}
    candidates=[i for i,p in paths.items() if i not in visited and (len(p)-1)*100/(n-1)<=remaining+1e-8]
    if not candidates:return None
    if policy=='random': scores=np.random.default_rng(seed+len(records)*7919).random(len(candidates));reason='Seeded random reachable site'
    elif policy=='grid':
        # Fixed regular lattice, traversed in alternating rows. No posterior or labels.
        ticks=np.linspace(0,n-1,5,dtype=int).tolist(); order=[]
        for row,y in enumerate(ticks):
            for x in (ticks if row%2==0 else ticks[::-1]):
                i=y*n+x
                if not blocked[i]:order.append(i)
        ranks={i:j for j,i in enumerate(order)}
        scores=np.array([-ranks.get(i,len(order)+i) for i in candidates]);reason='Next reachable site in a fixed 5 × 5 regular sampling lattice'
    elif policy=='uncertainty':scores=std[candidates];reason='Largest posterior standard deviation among reachable sites'
    else:
        dist=np.array([(len(paths[i])-1)*100/(n-1) for i in candidates]);scores=(std[candidates]+.35*np.maximum(0,mean[candidates]-45))/(1+dist/70);reason='Uncertainty plus predicted hotspot value, discounted by travel cost'
    index=candidates[int(np.argmax(scores))]; path=paths[index]
    return index,path,(len(path)-1)*100/(n-1),reason
