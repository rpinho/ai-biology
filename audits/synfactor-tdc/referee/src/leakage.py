"""Replay the product stream, bind it to fit inputs, and check stronger identities."""
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold
from teacher import assemble

def run(key,split):
    d=json.loads(Path('audit',key+'.json').read_text())
    clean=d['rows']
    dec=[r for r in clean if r['p']]
    indices=d['splits'][split]
    tr,va,te=indices
    pfx='audit/'+key+'-'+split
    products,trace=assemble(dec,clean,indices)
    cap_index={s:i for i,s in enumerate(sorted({p[1] for r in dec for p in r['p']}))}
    ids=np.load(pfx+'-inputs.npz')['ids'][len(dec):]
    assert all(tuple(ids[i])==(cap_index[a[1]],cap_index[b[1]]) for i,(a,b) in enumerate(products.values()))
    primary=json.loads(Path(pfx+'-audit.json').read_text())
    assert all(v==primary[k] for k,v in trace.items())
    sources=[{tuple(dec[i]['p'][j]) for i in tr} for j in (0,1)]
    types={(dec[i]['p'][0][0],dec[i]['p'][1][0]) for i in tr}
    for a,b in products.values():
        assert a in sources[0] and b in sources[1] and (a[0],b[0]) in types
    def recanon(s):
        return Chem.MolToSmiles(Chem.MolFromSmiles(s),canonical=True,isomericSmiles=True)
    held_ids=[{recanon(dec[i]['s']) for i in ix} for ix in indices]
    held_scaf=[{dec[i]['scaffold'] for i in ix} for ix in indices]
    stats=Counter()
    matched_scaffolds=set()
    digest=hashlib.sha256()
    for s,(a,b) in products.items():
        digest.update((json.dumps((s,a,b),separators=(',',':'))+'\n').encode())
        m=Chem.MolFromSmiles(s)
        sc=MurckoScaffold.MurckoScaffoldSmiles(mol=m,includeChirality=False)
        ss=Chem.MolToSmiles(m)
        for j,n in enumerate(('train','val','test')):
            stats['recanonicalized_overlap_'+n]+=ss in held_ids[j]
            stats['scaffold_overlap_products_'+n]+=sc in held_scaf[j]
        if sc in held_scaf[2]:
            matched_scaffolds.add(sc)
    return {**stats,'unique_test_scaffolds_in_synthetic':len(matched_scaffolds),
            'test_scaffolds':len(held_scaf[2]),'ordered_product_source_sha256':digest.hexdigest()}
if __name__=='__main__':
    out={}
    for key in json.loads(Path('data/manifest.json').read_text()):
        for split in ('scaffold','random'):
            out[key+' '+split]=run(key,split)
    Path('audit/leakage.json').write_text(json.dumps(out,indent=2))
