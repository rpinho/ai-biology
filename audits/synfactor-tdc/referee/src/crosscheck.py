"""Independent raw-label, identity, split, control and statistic cross-checks."""
import csv
import hashlib
import json
import sys
from pathlib import Path
from collections import Counter,defaultdict

import numpy as np
from rdkit import Chem
from scipy import stats
from sklearn.metrics import roc_auc_score,average_precision_score
from chem import cuts,join
from statistics_audit import metrics,align,bootstrap

def checks(key,entry):
    path=Path('data')/entry['filename']
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest==entry['sha256'] and digest in next(l for l in Path('SEALED.md').read_text().splitlines() if entry['filename'].split('.')[0] in l and entry['url'] in l)
    raw=list(csv.DictReader(path.open(),delimiter='\t'))
    records=json.loads(Path('audit',key+'.json').read_text())
    binary=records['binary']
    stored={r['s']:r['y'] for r in records['rows']}
    groups=defaultdict(list)
    reverse_tie_groups=defaultdict(list)
    literal_groups=defaultdict(list)
    invalid=0
    single_diffs=0
    for r in raw:
        m=Chem.MolFromSmiles(r['Drug'])
        if m is None:
            invalid+=1
            continue
        frags=Chem.GetMolFrags(m,asMols=True,sanitizeFrags=True)
        best=max(f.GetNumHeavyAtoms() for f in frags)
        choices=sorted(Chem.MolToSmiles(f) for f in frags if f.GetNumHeavyAtoms()==best)
        y=float(r['Y'])
        groups[choices[-1]].append(y)
        reverse_tie_groups[choices[0]].append(y)
        literal=Chem.MolToSmiles(m) if len(frags)==1 else choices[-1]
        single_diffs+=literal!=choices[-1]
        literal_groups[literal].append(y)
    def reduce(g):
        return {s:sum(v)/len(v) for s,v in g.items() if not binary or len(set(v))==1}
    rebuilt=reduce(groups)
    assert rebuilt.keys()==stored.keys()
    delta=max(abs(v-stored[s]) for s,v in rebuilt.items())
    assert delta<1e-12
    dec=[r for r in records['rows'] if r['p']]
    ties=Counter()
    mismatch=Counter()
    examples=[]
    alternative=[]
    for r in dec:
        m=Chem.MolFromSmiles(r['s'])
        allcuts=cuts(m)
        same=[o for o in allcuts if o[:2]==allcuts[0][:2]]
        alt=same[-1][2:]
        alternative.append([p[1] for p in alt])
        if len(same)>1:
            # Enumerate cuts from reversed atom order without recanonicalizing the input.
            reordered=Chem.RenumberAtoms(m,list(reversed(range(m.GetNumAtoms()))))
            ties['reordered_checked']+=1
            ties['reordered_winner_changes']+=allcuts[0]!=cuts(reordered)[0]
        a,b=r['p']
        assembled=join(a[2],b[2])
        if assembled!=r['s']:
            reround=Chem.MolToSmiles(Chem.MolFromSmiles(assembled))
            mismatch['different_strings']+=1
            mismatch['same_after_reparse']+=reround==Chem.MolToSmiles(m)
            mi=Chem.MolFromSmiles(assembled)
            mismatch['same_nonisomeric']+=Chem.MolToSmiles(mi,isomericSmiles=False)==Chem.MolToSmiles(m,isomericSmiles=False)
            if len(examples)<2:
                examples.append([r['s'],assembled])
    overlaps={}
    for name,(tr,va,te) in records['splits'].items():
        exp=set(tr)|set(va)|set(te)
        assert len(exp)==len(tr)+len(va)+len(te)==len(dec)
        ids=sorted(exp)
        assert ids==list(range(len(dec)))
        slots=[{alternative[i][s] for i in tr} for s in (0,1)]
        overlaps[name]=sum(all(alternative[i][j] in slots[j] for j in (0,1)) for i in te)
    # Count decomposability under the opposite largest-fragment lexical tie,
    # including any identities that differ from the primary cleaned set.
    from sklearn.model_selection import train_test_split
    valid_dec={r['s'] for r in dec}
    first=[s for s in groups if s in valid_dec]
    yy=[stored[s] for s in first]
    _,temp=train_test_split(first,test_size=.3,random_state=42,stratify=yy if binary else None)
    _,alt_test=train_test_split(temp,test_size=2/3,random_state=42,stratify=[stored[s] for s in temp] if binary else None)
    primary_test={dec[i]['s'] for i in records['splits']['random'][2]}
    alt_keys=set(reduce(reverse_tie_groups))
    decomp_keys={r['s'] for r in dec}
    alt_dec=len(decomp_keys&alt_keys)+sum(bool(cuts(Chem.MolFromSmiles(s))) for s in alt_keys-set(stored))
    return dict(sha256=digest,raw=len(raw),invalid=invalid,raw_value_counts=dict(Counter(r['Y'] for r in raw)) if binary else None,
                raw_y_range=[min(float(r['Y']) for r in raw),max(float(r['Y']) for r in raw)],
                verified_clean_labels=len(stored),max_label_abs_error=delta,
                clean_lex_first_largest_tie=len(alt_keys),decomp_lex_first_largest_tie=alt_dec,literal_single_fragment_clean=len(reduce(literal_groups)),
                single_fragment_direct_smiles_changes=single_diffs,random_raw_order_test_intersection=len(primary_test.intersection(alt_test)),
                atom_reversal=dict(ties),reverse_tie_both_seen=overlaps,roundtrip=dict(mismatch),examples=examples)

def stat_control():
    rng=np.random.default_rng(610)
    worst=0.
    num=0
    for _ in range(12):
        y=rng.integers(0,2,(4,34)).astype(float)
        p=rng.integers(-2,5,y.shape).astype(float)
        regs=metrics(y,p,False)
        cls=metrics(y,p,True)
        for i in range(len(y)):
            for actual,expected in [(cls['AUROC'][i],roc_auc_score(y[i],p[i])),
                (cls['AUPRC'][i],average_precision_score(y[i],p[i])),
                (regs['rho'][i],stats.spearmanr(y[i],p[i]).statistic),
                (regs['RMSE'][i],np.linalg.norm(y[i]-p[i])/np.sqrt(p.shape[1])),
                (regs['MAE'][i],np.abs(y[i]-p[i]).mean())]:
                worst=max(worst,abs(actual-expected))
                num+=1
    assert worst<1e-12
    # A small tied example permits an independent exhaustive scalar lookup for
    # all swap configurations. Reweight it with the prescribed Monte Carlo draws.
    y=np.array([0.,1.,1.,0.,1.,0.])
    a=np.array([2.,2.,6.,2.,3.,1.])
    b=np.array([.2,.8,.6,.4,.1,.8])
    calls=0
    swap_err=0.
    boot_err=0.
    for binary in (True,False):
        result=bootstrap(y,{'a':a,'b':b},binary,[('a','b')],[])
        diff=result['diffs']['a-b']
        rng2=np.random.default_rng(20261124)
        mask=rng2.random((10000,len(y)))<.5
        bit=(1<<np.arange(len(y)))
        freq=np.bincount(mask@bit,minlength=2**len(y))
        ref={'AUROC':roc_auc_score,'AUPRC':average_precision_score} if binary else {
            'rho':lambda y,p:stats.spearmanr(y,p).statistic,'RMSE':lambda y,p:np.sqrt(np.mean((y-p)**2)),
            'MAE':lambda y,p:np.mean(abs(y-p))}
        idx=np.random.default_rng(20261124).integers(len(y),size=(2000,len(y)))
        for m,fn in ref.items():
            obs=fn(y,a)-fn(y,b)
            aa,bb=(align(a),align(b)) if m in ('AUROC','AUPRC','rho') else (a,b)
            count=0
            for pattern,mult in enumerate(freq):
                sel=(pattern&bit)!=0
                delta=fn(y,np.where(sel,aa,bb))-fn(y,np.where(sel,bb,aa))
                count+=mult*(abs(delta)>=abs(obs)-1e-14)
            swap_err=max(swap_err,abs((1+count)/10001-diff[m]['p']))
            if m=='RMSE':
                res=np.array([fn(y[i],a[i])-fn(y[i],b[i]) for i in idx])
                boot_err=float(np.max(np.abs(np.quantile(res,[.025,.975])-diff[m]['CI'])))
            calls+=1
    assert max(swap_err,boot_err)<1e-12
    return dict(metric_cases=num,max_abs_error=float(worst),permutation_metrics=calls,
                max_p_error=swap_err,paired_RMSE_interval_error=boot_err)


if __name__=='__main__':
    out={'statistics':stat_control()}
    for k,e in json.loads(Path('data/manifest.json').read_text()).items():
        out[k]=checks(k,e)
    Path('audit/crosscheck.json').write_text(json.dumps(out,allow_nan=False,indent=2))
