import numpy as np
from .field import generate,Sampler
from .model import predict
from .policy import choose,POLICIES

def run(seed=41,family='narrow',policy='balanced',budget=20,travel_budget=650,n=18):
    if policy not in POLICIES:raise ValueError('unknown policy')
    if not isinstance(seed,int) or not 0<=seed<=100000:raise ValueError('seed must be 0..100000')
    if not 1<=budget<=40 or not 0<=travel_budget<=2000:raise ValueError('invalid budget')
    field=generate(seed,family,n); coords=field['coords']; sampler=Sampler(field); audit=[]; route=[0]; distance=0.;sampler.sample(0)
    while len(sampler.records)<budget:
        mean,std=predict(coords,sampler.records)
        decision=choose(policy,coords,field['obstacles'],n,sampler.records,mean,std,travel_budget-distance,seed)
        if decision is None:break
        index,path,cost,reason=decision
        audit.append({'step':len(sampler.records),'observations_before':list(sampler.records),'selected':index,'posterior_mean':float(mean[index]),'posterior_std':float(std[index]),'travel_m':cost,'remaining_travel_m':travel_budget-distance,'rationale':reason})
        sampler.sample(index); route+=path[1:];distance+=cost
    mean,std=predict(coords,sampler.records); mask=~field['obstacles'].copy();mask[[r['index'] for r in sampler.records]]=False
    truth=field['truth']; error=mean[mask]-truth[mask]; positive=truth[mask]>=50;pred=mean[mask]>=50;tp=int(np.sum(positive&pred)); actual=int(positive.sum()); reported=int(pred.sum())
    metrics={'rmse':float(np.sqrt(np.mean(error**2))),'mae':float(np.mean(abs(error))),'coverage95':float(np.mean(abs(error)<=1.96*std[mask])),'hotspot_precision':tp/reported if reported else None,'hotspot_recall':tp/actual if actual else None,'travel_m':float(distance),'samples':len(sampler.records),'max_missed_mgkg':float(np.max(truth[mask][positive&~pred])) if np.any(positive&~pred) else 0.}
    next_choice=choose(policy,coords,field['obstacles'],n,sampler.records,mean,std,travel_budget-distance,seed)
    return {'seed':seed,'family':family,'policy':policy,'n':n,'coords':coords.tolist(),'truth':truth.tolist(),'posterior':mean.tolist(),'uncertainty':std.tolist(),'obstacles':field['obstacles'].tolist(),'records':sampler.records,'route':route,'audit':audit,'metrics':metrics,'next':({'index':int(next_choice[0]),'reason':next_choice[3]} if next_choice else None),'synthetic':True,'units':{'coordinates':'m','concentration':'mg/kg (synthetic)'},'sample_budget':budget,'travel_budget_m':travel_budget}
