"""Audit supplied model semantics, the ID solver, and label-free pair collisions."""
import inspect
import json
from pathlib import Path
import sys
import numpy as np

def ridge_check():
    # Extract just the upstream standalone ridge function so Torch remains isolated.
    import ast
    import teacher
    source=Path('synfactor/experiments/compare.py').read_text()
    node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='additive_fit')
    ns={'np':np}
    exec(ast.get_source_segment(source,node),ns)
    rng=np.random.default_rng(535)
    ids=rng.integers(0,8,(100,2))
    ids[-5:]=99
    rows=np.column_stack([ids[:,0],ids[:,1]+100,np.full(len(ids),-1)])
    y=rng.normal(size=len(ids))
    split=np.array(['train']*70+['validation']*14+['test']*16)
    ref,rec=ns['additive_fit'](y[:,None],rows,split)
    actual,lam=teacher.ridge(ids,y,np.flatnonzero(split=='train'),np.flatnonzero(split=='validation'))
    err=float(np.max(np.abs(ref[:,0]-actual)))
    assert lam==rec['ridge_penalty'] and err<1e-10
    return dict(rows=len(y),unseen_only_rows=5,max_absolute_error=err,lambda_selected=lam)

def pair_checks():
    out={}
    for path in sorted(Path('audit').glob('*-inputs.npz')):
        d=np.load(path)
        ids,tr,va,te=[d[k] for k in ('ids','tr','va','te')]
        n=len(tr)+len(va)+len(te)
        synth=ids[n:]
        assert len(synth)==min(20000,5*len(tr))
        train=[set(ids[tr,j]) for j in range(2)]
        assert all(set(synth[:,j])<=train[j] for j in (0,1))
        synthset=set(map(tuple,synth))
        result={}
        for k,idx in [('train',tr),('validation',va),('test',te)]:
            result[k+'_cap_tuple_seen_in_synthetic']=sum(tuple(r) in synthset for r in ids[idx])
        result['unique_synthetic_cap_tuples']=len(synthset)
        result['synthetic_count']=len(synth)
        out[path.stem]=result
    assert len(out)==8
    return out

def cp_check():
    import torch
    from neural import SynFactor,NeuralAdditive
    torch.manual_seed(251)
    cp=SynFactor(2058,rank=16).eval()
    add=NeuralAdditive().eval()
    x=torch.randn((16,3,2058))
    mask=torch.tensor([[True,True,False]]).expand(16,-1)
    with torch.no_grad():
        pred=cp(x,mask)
        expect=(cp.factor(x[:,0],0)*cp.factor(x[:,1],1)).sum(-1)/4
        alt=x.clone()
        alt[:,2]=alt[:,2]*17
        ch=float((cp(alt,mask)-pred).abs().max())
        pe=float((expect-pred).abs().max())
        assert ch==0 and pe<1e-7
        def interaction(net):
            vals=[]
            for i,j in [(0,0),(0,1),(1,0),(1,1)]:
                batch=x.clone()
                batch[:,0]=x.roll(i,0)[:,0]
                batch[:,1]=x.roll(j,0)[:,1]
                vals.append(net(batch,mask))
            return float((vals[0]-vals[1]-vals[2]+vals[3]).abs().max())
        a,c=interaction(add),interaction(cp)
        assert a<1e-6 and c>1e-4
    return dict(mask_invariance_error=ch,CP_formula_error=pe,additive_interaction=a,CP_interaction=c,
                additive_parameters=sum(p.numel() for p in add.parameters()),
                CP_parameters=sum(p.numel() for p in cp.parameters()))
if __name__=='__main__':
    name=sys.argv[1]
    result={'ridge':ridge_check,'pair':pair_checks,'cp':cp_check}[name]()
    Path('audit',name+'-control.json').write_text(json.dumps(result,indent=2))
