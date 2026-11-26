"""Teacher, assembly and ID control. This process never imports PyTorch."""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import lightgbm as lgb
import numpy as np
from scipy.sparse import csr_matrix, eye
from scipy.sparse.linalg import spsolve
from sklearn.metrics import average_precision_score, mean_absolute_error, roc_auc_score, root_mean_squared_error
from scipy.stats import spearmanr

from chem import features, join, standard, Chem

def fit(x,y,split,binary):
    tr,va,_ = split
    cls = lgb.LGBMClassifier if binary else lgb.LGBMRegressor
    metric = 'binary_logloss' if binary else 'rmse'
    model = cls(n_estimators=2000,learning_rate=.03,num_leaves=31,min_child_samples=20,
                subsample=.8,subsample_freq=1,colsample_bytree=.5,reg_lambda=1.,
                random_state=42,n_jobs=4,verbosity=-1,metric=metric)
    model.fit(x[tr], y[tr], eval_set=[(x[va],y[va])],eval_metric=metric,
              callbacks=[lgb.early_stopping(50,verbose=False)])
    return model

def assemble(rows,clean,split):
    tr,va,te = split
    train = [rows[i]['p'] for i in tr]
    groups = defaultdict(lambda:[set(),set()])
    counts = Counter()
    for a,b in train:
        key = (a[0],b[0])
        counts[key]+=1
        groups[key][0].add(tuple(a))
        groups[key][1].add(tuple(b))
    keys=sorted(groups)
    slots=[[sorted(x) for x in groups[k]] for k in keys]
    weights=np.array([counts[k] for k in keys],dtype=float)
    rng=np.random.default_rng(42)
    ban={r['s'] for r in clean}
    cap = min(20000,5*len(tr))
    # Cache failures and duplicates at the dummy-identity level.
    tried=set()
    products={}
    trace=Counter()
    for _ in range(100*cap):
        if len(products)==cap:
            break
        k=rng.choice(len(keys),p=weights/weights.sum())
        a,b=[slot[rng.integers(len(slot))] for slot in slots[k]]
        trace['draws']+=1
        if (a,b) in tried:
            continue
        tried.add((a,b))
        try:
            s=join(a[2],b[2])
            s=standard(s)
        except (RuntimeError,ValueError):
            s=None
        if s is None:
            trace['invalid_product']+=1
        elif s in ban:
            trace['blocked_original']+=1
        elif s not in products:
            products[s]=(a,b)
    # Independently verify final membership and origin, including held-out products
    # with the same connectivity and different stereochemistry (diagnostic only).
    permitted=[{tuple(pair[j]) for pair in train} for j in (0,1)]
    assert all(a in permitted[0] and b in permitted[1] and (a[0],b[0]) in groups for a,b in products.values())
    for ix in split:
        assert not set(products).intersection(rows[i]['s'] for i in ix)
    assert len(products)==len(set(products)) and not set(products)&ban
    def flat(s):
        return Chem.MolToSmiles(Chem.MolFromSmiles(s),isomericSmiles=False)
    held={flat(rows[i]['s']) for i in va+te}
    trace.update(dict(exact_overlap=0, synthetic=len(products), requested=cap,
                      stereo_agnostic_holdout_hits=sum(flat(s) in held for s in products)))
    return products,dict(trace)

def ridge(ids,y,tr,va):
    n=len(ids)
    # Disjoint slot columns; add the penalized intercept exactly as compare.py.
    _,a=np.unique(ids[:,0],return_inverse=True)
    _,b=np.unique(ids[:,1],return_inverse=True)
    b+=a.max()+1
    inter=b.max()+1
    cols=np.c_[a,b,np.full(n,inter)].ravel()
    X=csr_matrix((np.ones(3*n),(np.repeat(np.arange(n),3),cols)),shape=(n,inter+1))
    mean,sd=y[tr].mean(),max(y[tr].std(),1e-6)
    gram=(X[tr].T@X[tr]).tocsc()
    rhs=X[tr].T@((y[tr]-mean)/sd)
    best=np.inf
    for penalty in (1e-6,.001,.1,1.,10.):
        w=spsolve(gram+penalty*eye(gram.shape[0],format='csc'),rhs)
        pred=(X@w)*sd+mean
        loss=np.mean(((pred[va]-y[va])/sd)**2)
        if loss<best:
            best,result,chosen=loss,pred,penalty
    return result,chosen

def matrix(strings):
    return np.stack([features(s) for s in strings])

def main(key):
    d=json.loads(Path('audit',key+'.json').read_text())
    clean=d['rows']
    binary=d['binary']
    dec_idx=[i for i,r in enumerate(clean) if r['p']]
    rows=[clean[i] for i in dec_idx]
    xc=matrix([r['s'] for r in clean])
    yc=np.array([r['y'] for r in clean])
    xd=xc[dec_idx]
    y=yc[dec_idx]
    caps=sorted({p[1] for r in rows for p in r['p']})
    index={s:i for i,s in enumerate(caps)}
    x=matrix(caps)
    base_ids=np.array([[index[p[1]] for p in r['p']] for r in rows],dtype='i8')
    np.save(Path('audit',key+'-features.npy'),x)
    for name,split in d['splits'].items():
        prefix=Path('audit',key+'-'+name)
        tr,va,te=split
        model=fit(xd,y,split,binary)
        def score(x):
            return model.booster_.predict(x,raw_score=True,num_threads=4)
        margins=score(xd)
        products,trace=assemble(rows, clean,split)
        strings=list(products)
        synth_score=np.concatenate([score(matrix(strings[j:j+512])) for j in range(0,len(strings),512)])
        synth_ids=np.array([[index[a[1]],index[b[1]]] for a,b in products.values()])
        ids=np.vstack([base_ids,synth_ids])
        seen=[np.isin(base_ids[te,j],base_ids[tr,j]) for j in range(2)]
        hit=seen[0].astype(int)+seen[1].astype(int)
        both_any=np.isin(base_ids[te],base_ids[tr]).all(axis=1)
        direct,lam1=ridge(base_ids,y,tr,va)
        distilled,lam2=ridge(base_ids,margins,tr,va)
        np.savez(str(prefix)+'-inputs.npz',ids=ids,tr=tr,va=va,te=te,
                 yfit=y[tr],yval=y[va],teacher=np.r_[margins,synth_score],binary=binary)
        np.savez(str(prefix)+'-eval.npz',truth=y[te],teacher=margins[te],ID_D=direct[te],
                 ID_T=distilled[te],hit=hit)
        cs=d['clean_splits'][name]
        full=fit(xc,yc,cs,binary)
        yy=yc[cs[2]]
        pp=full.booster_.predict(xc[cs[2]],raw_score=True,num_threads=4)
        np.savez(str(prefix)+'-clean.npz',truth=yy,pred=pp)
        trace.update(dict(both_seen=int((hit==2).sum()),one_seen=int((hit==1).sum()),
                          neither_seen=int((hit==0).sum()),both_any=int(both_any.sum()),
                          split_sizes=list(map(len,split)),id_lambda=[lam1,lam2],
                          teacher_best_iteration=model.best_iteration_,clean_best_iteration=full.best_iteration_,
                          clean_test_n=len(yy)))
        Path(str(prefix)+'-audit.json').write_text(json.dumps(trace,indent=2))
        print(key,name,'teacher/controls ready',flush=True)

if __name__=='__main__':
    main(sys.argv[1])
