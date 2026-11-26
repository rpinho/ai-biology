"""Paired molecule-level uncertainty; batched implementation with tie handling."""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.stats import rankdata

def corr(a,b):
    a=a-a.mean(axis=-1,keepdims=True)
    b=b-b.mean(axis=-1,keepdims=True)
    den=np.sqrt((a*a).sum(axis=-1)*(b*b).sum(axis=-1))
    return np.divide((a*b).sum(axis=-1),den,out=np.full_like(den,np.nan),where=den>0)

def metrics(y,p,binary):
    y,p=np.broadcast_arrays(y,p)
    if not binary:
        return dict(rho=corr(rankdata(y,axis=-1),rankdata(p,axis=-1)),
                    RMSE=np.sqrt(((p-y)**2).mean(-1)),MAE=np.abs(p-y).mean(-1))
    n=p.shape[-1]
    order=np.argsort(-p,axis=-1)
    py=np.take_along_axis(y,order,axis=-1)
    ps=np.take_along_axis(p,order,axis=-1)
    tp=np.cumsum(py,axis=-1)
    pos=tp[:,-1]
    neg=n-pos
    # All examples with identical scores enter the curve simultaneously.
    idx=np.arange(1,n+1)
    ends=np.c_[ps[:,:-1]!=ps[:,1:],np.ones((len(ps),1),dtype=bool)]
    boundary=np.minimum.accumulate(np.where(ends,idx,n)[:,::-1],axis=1)[:,::-1]
    start=np.maximum.accumulate(np.where(np.c_[np.ones((len(ps),1),bool),ends[:,:-1]],idx,1),axis=1)
    # Midrank in descending score order. Average precision uses right-edge precision.
    ranks=n+1-(boundary+start)/2
    with np.errstate(divide='ignore',invalid='ignore'):
        auc=((py*ranks).sum(-1)-pos*(pos+1)/2)/(pos*neg)
        ap=(py*np.take_along_axis(tp,boundary-1,axis=-1)/boundary).sum(-1)/pos
    return dict(AUROC=auc,AUPRC=ap)

def align(x):
    s=x.std()
    return (x-x.mean())/(s if s>0 else 1.)

def box(arr):
    vals=np.asarray(arr)
    vals=vals[np.isfinite(vals)]
    return [float(x) for x in np.quantile(vals,[.025,.975])] if len(vals) else None

def plain(x):
    x=float(x)
    return x if np.isfinite(x) else None

def bootstrap(y,models,binary,checks,fidelity):
    point={k:{m:plain(v[0]) for m,v in metrics(y[None,:],p[None,:],binary).items()} for k,p in models.items()}
    for k in fidelity:
        point[k]['teacher_rho']=plain(corr(rankdata(models[k]),rankdata(models['teacher'])))
        point[k]['teacher_r']=plain(corr(models[k],models['teacher']))
    data={k:{m:[] for m in row} for k,row in point.items()}
    rng=np.random.default_rng(20261124)
    for offset in range(0,2000,40):
        idx=rng.integers(len(y),size=(min(40,2000-offset),len(y)))
        yy=y[idx]
        for k,p in models.items():
            pp=p[idx]
            vals=metrics(yy,pp,binary)
            if k in fidelity:
                target=models['teacher'][idx]
                vals['teacher_rho']=corr(rankdata(pp,axis=1),rankdata(target,axis=1))
                vals['teacher_r']=corr(pp,target)
            for m,val in vals.items():
                data[k][m].append(val)
    data={k:{m:np.concatenate(v) for m,v in row.items()} for k,row in data.items()}
    points={k:{m:dict(value=v,CI=box(data[k][m]),valid_boot=int(np.isfinite(data[k][m]).sum())) for m,v in row.items()} for k,row in point.items()}
    diffs={}
    for a,b in checks:
        row={}
        for m in metrics(y[None,:],models[a][None,:],binary):
            if point[a][m] is None or point[b][m] is None:
                row[m]=dict(delta=None,CI=None,p=None)
            else:
                row[m]=dict(delta=point[a][m]-point[b][m],CI=box(data[a][m]-data[b][m]))
        permutation(y,models[a],models[b],binary,row)
        diffs[a+'-'+b]=row
    return dict(points=points,diffs=diffs)

def permutation(y,a,b,binary,row):
    aligned_a,aligned_b=align(a),align(b)
    rng=np.random.default_rng(20261124)
    counts=dict.fromkeys(row,0)
    for offset in range(0,10000,64):
        mask=rng.random((min(64,10000-offset),len(y)))<.5
        def exchange(a,b):
            return np.where(mask,a,b),np.where(mask,b,a)
        x,z=exchange(aligned_a,aligned_b)
        if binary:
            ma,mb=metrics(y,x,True),metrics(y,z,True)
            diff={m:ma[m]-mb[m] for m in ma}
        else:
            ry=rankdata(y)
            diff={'rho':corr(ry,rankdata(x,axis=1))-corr(ry,rankdata(z,axis=1))}
            x,z=exchange(a,b)
            diff['RMSE']=np.sqrt(np.mean((x-y)**2,axis=1))-np.sqrt(np.mean((z-y)**2,axis=1))
            diff['MAE']=np.mean(abs(x-y),axis=1)-np.mean(abs(z-y),axis=1)
        for m,d in diff.items():
            if row[m]['delta'] is not None:
                counts[m]+=np.count_nonzero(np.abs(d)>=abs(row[m]['delta'])-1e-14)
    for m,c in counts.items():
        if row[m]['delta'] is not None:
            row[m]['p']=(1+int(c))/10001

def eval_cell(key,name):
    prefix='audit/'+key+'-'+name
    d=np.load(prefix+'-eval.npz')
    p={k:d[k].astype(float) for k in ['teacher','ID_D','ID_T']}
    y=d['truth']
    binary=key in ('herg','cyp3a4_veith')
    seeds={}
    for mode in ('D','T','C'):
        for kind in ('A','CP'):
            k=f'{kind}_{mode}'
            pp=np.stack([np.load(f'{prefix}-{k}-{s}.npz')['pred'] for s in (42,43,44)]).astype(float)
            assert pp.shape==(3,len(y)) and np.isfinite(pp).all()
            seeds[k]=pp
            p[k]=pp.mean(0)
    checks=[('CP_D','A_D'),('CP_D','ID_D'),('CP_T','A_T'),('CP_C','A_C'),('CP_C','teacher')]
    result={}
    for group,mask in [('all',np.ones(len(y),bool)),('both_seen',d['hit']==2),('unseen_any',d['hit']!=2)]:
        yy=y[mask]
        entry={'n':len(yy),'classes':np.bincount(yy.astype(int),minlength=2).tolist() if binary else None}
        result[group]=entry
        if len(yy)<20 or (binary and min(entry['classes'])<2):
            entry['status']='N/A'
            continue
        selected={k:v[mask] for k,v in p.items()}
        entry.update(bootstrap(yy,selected,binary,checks,['CP_C','A_C','CP_T','A_T','ID_T']))
        entry['seeds']={}
        for k,pp in seeds.items():
            vals=metrics(yy,pp[:,mask],binary)
            if k.endswith(('_T','_C')):
                target=selected['teacher']
                vals['teacher_rho']=corr(rankdata(pp[:,mask],axis=1),rankdata(target))
                vals['teacher_r']=corr(pp[:,mask],target)
            entry['seeds'][k]={m:dict(values=[plain(v) for v in vs],mean=plain(np.mean(vs)),sd=plain(np.std(vs,ddof=1))) for m,vs in vals.items()}
        # Paired same-seed differences explicitly expose sign changes.
        entry['matched_seed_deltas']={}
        for mode in ('D','T','C'):
            a=metrics(yy,seeds['CP_'+mode][:,mask],binary)
            b=metrics(yy,seeds['A_'+mode][:,mask],binary)
            entry['matched_seed_deltas'][mode]={m:(a[m]-b[m]).tolist() for m in a}
        print(key,name,group,'evaluated',flush=True)
    cl=np.load(prefix+'-clean.npz')
    result['clean_teacher']={m:plain(v[0]) for m,v in metrics(cl['truth'][None,:],cl['pred'][None,:],binary).items()}
    out=Path(prefix+'-stats.json')
    tmp=out.with_suffix('.tmp')
    tmp.write_text(json.dumps(result,allow_nan=False,separators=(',',':')))
    tmp.replace(out)

if __name__=='__main__':
    eval_cell(*sys.argv[1:])
