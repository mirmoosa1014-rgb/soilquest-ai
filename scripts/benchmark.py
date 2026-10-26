import sys,json,csv,argparse,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from soilquest.simulation import run
from soilquest.policy import POLICIES
root=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--quick',action='store_true');args=p.parse_args();rows=[];start=time.time()
for family in ['narrow','directional']:
 for seed in ([41] if args.quick else [41,42,43,44]):
  for budget in ([12] if args.quick else [8,16,24]):
   for policy in POLICIES:
    r=run(seed,family,policy,budget);rows.append({'family':family,'seed':seed,'budget':budget,'policy':policy,**r['metrics']})
with (root/'results/benchmark.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(root/'results/demo.json').write_text(json.dumps(run(41,'narrow','balanced',20)))
(root/'results/benchmark-meta.json').write_text(json.dumps({'episodes':len(rows),'seconds':time.time()-start,'mode':'quick' if args.quick else 'full','threshold_mgkg':50,'travel_budget_m':650,'seeds':[41] if args.quick else [41,42,43,44]},indent=2));print(f'{len(rows)} episodes in {time.time()-start:.2f}s')
