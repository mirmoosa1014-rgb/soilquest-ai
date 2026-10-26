import json,inspect
from pathlib import Path
import numpy as np
import pytest
from fastapi.testclient import TestClient
from soilquest.api import app
from soilquest.field import generate,Sampler,FAMILIES
from soilquest.model import predict
from soilquest.policy import choose,routes,POLICIES
from soilquest.simulation import run

def test_field_determinism_positivity_and_holdout():
 assert set(FAMILIES['train']).isdisjoint(FAMILIES['test'])
 for family in sum(FAMILIES.values(),[]):
  a=generate(3,family);b=generate(3,family);assert np.array_equal(a['truth'],b['truth']);assert np.min(a['truth'])>=0
 model=json.loads(Path('models/hyperparameters.json').read_text());assert model['training_families']==FAMILIES['train'];assert not set(model['training_seeds'])&{41,42,43,44}

def test_sampler_boundary_and_noise():
 f=generate();a=Sampler(f);b=Sampler(f);assert a.sample(0)==b.sample(0)
 with pytest.raises(ValueError):a.sample(0)
 with pytest.raises(ValueError):a.sample(int(np.where(f['obstacles'])[0][0]))

def test_model_has_no_truth_and_only_observed_values():
 assert 'truth' not in inspect.signature(predict).parameters
 f=generate();s=Sampler(f);s.sample(0);m,sd=predict(f['coords'],s.records)
 f['truth'][:]=9999;m2,sd2=predict(f['coords'],s.records)
 assert np.array_equal(m,m2);assert np.array_equal(sd,sd2)
 assert sd[0]<sd[-1];assert np.all(np.isfinite(m));assert np.all(sd>=0)
 empty,unc=predict(f['coords'],[]);assert np.all(empty==18);assert np.all(unc==45)

@pytest.mark.parametrize('policy',POLICIES)
def test_budget_no_duplicate_paths_audit_replay(policy):
 r=run(41,'narrow',policy,24);assert r==run(41,'narrow',policy,24)
 idx=[a['index'] for a in r['records']];assert idx[0]==0;assert len(idx)==len(set(idx))<=24
 assert r['metrics']['travel_m']<=650+1e-6
 assert abs((len(r['route'])-1)*100/(r['n']-1)-r['metrics']['travel_m'])<1e-6
 assert all(not r['obstacles'][i] for i in r['route'])
 for a,b in zip(r['route'],r['route'][1:]):
  ay,ax=divmod(a,r['n']);by,bx=divmod(b,r['n']);assert abs(ax-bx)+abs(ay-by)==1
 for i,a in enumerate(r['audit']):assert len(a['observations_before'])==i+1;assert a['selected'] not in [x['index'] for x in a['observations_before']]
 assert 0<=r['metrics']['coverage95']<=1

def test_zero_travel_budget():
 r=run(travel_budget=0);assert r['metrics']['samples']==1;assert r['metrics']['travel_m']==0

def test_policies_receive_no_truth():
 assert 'truth' not in inspect.signature(choose).parameters
 assert set(inspect.signature(choose).parameters)=={'policy','coords','blocked','n','records','mean','std','remaining','seed'}

def test_api_valid_invalid():
 c=TestClient(app);assert c.get('/api/health').json()['ok']
 assert c.get('/api/survey?budget=3').json()['metrics']['samples']==3
 for q in ['budget=10000','seed=-1','travel=3000']:assert c.get('/api/survey?'+q).status_code==422
 assert c.get('/api/survey?family=unknown').status_code==400
 assert c.get('/api/survey?policy=oracle').status_code==400

def test_shared_first_observation():
 first=[run(policy=p,budget=2)['records'][0] for p in POLICIES];assert all(r==first[0] for r in first)

def test_regular_grid_baseline():
 f=generate();r=Sampler(f).sample(0);mean,std=predict(f['coords'],[r]);i,_,_,_=choose('grid',f['coords'],f['obstacles'],18,[r],mean,std,650,41);assert i==4
