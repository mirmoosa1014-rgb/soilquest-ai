import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from soilquest.field import generate
from soilquest.model import predict
out=Path(__file__).resolve().parents[1];scores=[]
for length in [10,18,28]:
 params={'length_m':length,'mean':18,'amplitude':45,'noise_mgkg':3}
 errors=[]
 for family in ['smooth','multiple','background']:
  for seed in range(6):
   f=generate(seed,family);rng=np.random.default_rng(seed+200);idx=rng.choice(np.where(~f['obstacles'])[0],16,replace=False);records=[{'index':int(i),'value':float(f['truth'][i]+rng.normal(0,3))} for i in idx];mean,_=predict(f['coords'],records,params);mask=~f['obstacles'];mask[idx]=False;errors.append(float(np.mean((mean[mask]-f['truth'][mask])**2)))
 scores.append((float(np.mean(errors)),params))
score,params=min(scores,key=lambda x:x[0]);params.update({'training_families':['smooth','multiple','background'],'training_seeds':list(range(6)),'heldout_families':['narrow','directional'],'feature_schema':['x_m','y_m','observed_concentration_mgkg'],'training_mse':score,'candidate_length_scores':[{'length_m':p['length_m'],'mse':s} for s,p in scores]});(out/'models/hyperparameters.json').write_text(json.dumps(params,indent=2));print(json.dumps(params,indent=2))
