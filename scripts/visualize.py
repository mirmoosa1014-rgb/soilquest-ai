import os,sys,json,csv
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/soilquest-mpl')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,PillowWriter
from soilquest.simulation import run
root=Path(__file__).resolve().parents[1];rows=list(csv.DictReader((root/'results/benchmark.csv').open()));policies=['random','grid','uncertainty','balanced'];colors=['#72bdd0','#c6cbd2','#faaf60','#c8f25d'];plt.rcParams.update({'figure.facecolor':'#091a20','axes.facecolor':'#10272c','axes.edgecolor':'#47635d','text.color':'#e1eee7','axes.labelcolor':'#a7c4b7','xtick.color':'#a7c4b7','ytick.color':'#a7c4b7','grid.color':'#29433d','font.size':10,'axes.titleweight':'bold','savefig.facecolor':'#091a20'})
fig=plt.figure(figsize=(15,10),layout='constrained');gs=fig.add_gridspec(2,3);demo=run(41,'narrow','balanced',20);n=demo['n'];
for col,key,title in [(0,'truth','Hidden truth · evaluator only'),(1,'posterior','20-sample GP reconstruction'),(2,'uncertainty','Posterior uncertainty')]:
 ax=fig.add_subplot(gs[0,col]);v=np.array(demo[key]).reshape(n,n);im=ax.imshow(v,origin='lower',extent=[0,100,0,100],vmin=0,vmax=45 if key=='uncertainty' else 130,cmap='viridis');ax.set(title=title,xlabel='East (m)',ylabel='North (m)');fig.colorbar(im,ax=ax,shrink=.7,label='σ (mg/kg)' if key=='uncertainty' else 'Synthetic mg/kg');coords=np.array(demo['coords']);ids=[r['index'] for r in demo['records']];ax.plot(coords[demo['route'],0],coords[demo['route'],1],color='white',lw=.7,alpha=.6);ax.scatter(coords[ids,0],coords[ids,1],s=16,facecolors='none',edgecolors='white');
 if col==0:ax.annotate('Missed narrow hotspot',xy=np.array(demo['coords'])[np.argmax(demo['truth'])],xytext=(3,88),color='white',arrowprops={'arrowstyle':'->','color':'white'},fontsize=9)
ax=fig.add_subplot(gs[1,0])
for p,c in zip(policies,colors):
 means=[];dev=[]
 for b in [8,16,24]:
  v=np.array([float(r['rmse']) for r in rows if r['policy']==p and int(r['budget'])==b]);means.append(v.mean());dev.append(v.std())
 means=np.array(means);dev=np.array(dev);ax.plot([8,16,24],means,'o-',label=p,color=c);ax.fill_between([8,16,24],means-dev,means+dev,color=c,alpha=.12)
ax.set(title='Accuracy versus sample ceiling',xlabel='Maximum sample count (travel ≤ 650 m)',ylabel='Unobserved-cell RMSE (mg/kg)');ax.grid(alpha=.4);ax.legend(fontsize=8);ax.text(.02,.03,'Bands: ±1 SD across 8 held-out fields',transform=ax.transAxes,fontsize=8)
ax=fig.add_subplot(gs[1,1]);cov=[];rec=[]
for p in policies:
 vals=[r for r in rows if r['policy']==p and r['budget']=='24'];cov.append(np.mean([float(r['coverage95']) for r in vals]));rec.append(np.mean([float(r['hotspot_recall']) for r in vals if r['hotspot_recall']]))
x=np.arange(4);ax.bar(x-.18,cov,.34,label='95% interval coverage',color='#72bdd0');ax.bar(x+.18,rec,.34,label='Hotspot recall ≥50 mg/kg',color='#c8f25d');ax.axhline(.95,color='white',ls=':',lw=1);ax.set(xticks=x,xticklabels=policies,ylim=(0,1.08),title='Coverage can hide missed hotspots',ylabel='Fraction on held-out fields');ax.tick_params(axis='x',rotation=15);ax.legend(fontsize=8,loc='lower right')
ax=fig.add_subplot(gs[1,2])
for p,c in zip(policies,colors):
 vals=[r for r in rows if r['policy']==p and r['budget']=='24'];ax.scatter([float(r['travel_m']) for r in vals],[float(r['rmse']) for r in vals],label=p,color=c,s=30,alpha=.8)
ax.set(title='Travel / error tradeoff',xlabel='Actual travel (m)',ylabel='Unobserved-cell RMSE (mg/kg)');ax.grid(alpha=.4);fig.suptitle('SOILQUEST AI  /  ADAPTIVE ENVIRONMENTAL SAMPLING\n96 paired episodes · synthetic held-out narrow and directional fields · seeds 41–44',fontsize=17,fontweight='bold');fig.savefig(root/'docs/images/research-overview.png',dpi=150);plt.close(fig)
fig=plt.figure(figsize=(12,6));ax=fig.add_subplot(111,projection='3d');co=np.array(demo['coords']);ax.plot_surface(co[:,0].reshape(n,n),co[:,1].reshape(n,n),np.array(demo['posterior']).reshape(n,n),cmap='viridis',vmin=0,vmax=130,linewidth=.2,edgecolor='#132e32');ax.set(xlabel='East (m)',ylabel='North (m)',zlabel='Synthetic mg/kg',title='Posterior concentration surface · 20 acquired samples');fig.savefig(root/'docs/images/posterior-3d.png',dpi=150,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(6,6),layout='constrained');image=ax.imshow(np.array(demo['posterior']).reshape(n,n),origin='lower',vmin=0,vmax=130,cmap='viridis');ax.set_xticks([]);ax.set_yticks([]);title=ax.set_title('');
def update(b):
 r=run(41,'narrow','balanced',int(b));image.set_data(np.array(r['posterior']).reshape(n,n));title.set_text(f'Synthetic survey · {r["metrics"]["samples"]} samples · RMSE {r["metrics"]["rmse"]:.1f} mg/kg');return image,title
FuncAnimation(fig,update,frames=range(1,25),interval=180).save(root/'docs/images/survey-replay.gif',writer=PillowWriter(fps=5));plt.close(fig)
summary={p:{k:float(np.mean([float(r[k]) for r in rows if r['policy']==p and r['budget']=='24' and r[k]])) for k in ['rmse','mae','coverage95','hotspot_recall','travel_m','samples']} for p in policies};(root/'results/summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
