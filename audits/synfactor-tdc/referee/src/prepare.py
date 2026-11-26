import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split
from chem import Chem, MurckoScaffold, cuts, standard, join

def split(rows, binary):
    groups = defaultdict(list)
    for i,r in enumerate(rows):
        groups[r['scaffold']].append(i)
    tr,va,te = [],[],[]
    for name,ids in sorted(groups.items(),key=lambda p:(-len(p[1]),p[0])):
        dest = tr if len(tr)+len(ids)<=.7*len(rows) else va if len(tr)+len(va)+len(ids)<=.8*len(rows) else te
        dest.extend(ids)
    sc = [tr,va,te]
    sets = [{rows[i]['scaffold'] for i in ids} for ids in sc]
    assert not any(sets[i]&sets[j] for i,j in [(0,1),(0,2),(1,2)])
    idx = np.arange(len(rows))
    y = np.array([r['y'] for r in rows])
    tr,temp = train_test_split(idx,test_size=.3,random_state=42,stratify=y if binary else None)
    va,te = train_test_split(temp,test_size=2/3,random_state=42,stratify=y[temp] if binary else None)
    return {'scaffold':sc,'random':[a.tolist() for a in (tr,va,te)]}

def main(key, entry):
    path = Path('data')/entry['filename']
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == entry['sha256'] and digest in Path('SEALED.md').read_text() and path.stat().st_size==entry['bytes']
    binary = entry['task']=='classification'
    stats = Counter()
    grouped = defaultdict(list)
    for row in csv.DictReader(path.open(),delimiter='\t'):
        stats['raw']+=1
        s = standard(row['Drug'])
        if s is None:
            stats['invalid']+=1
            continue
        y = float(row['Y'])
        assert np.isfinite(y) and (not binary or y in (0.,1.))
        grouped[s].append(y)
    rows=[]
    for s,labels in sorted(grouped.items()):
        if binary and len(set(labels))>1:
            stats['conflict_keys']+=1
            stats['conflict_rows']+=len(labels)
            continue
        stats['merged']+=len(labels)-1
        m = Chem.MolFromSmiles(s)
        options = cuts(m)
        parts = options[0][2:] if options else None
        if parts:
            stats['decomp']+=1
            ties=[o for o in options if o[:2]==options[0][:2]]
            stats['balanced_ties']+=len(ties)>1
            stats['tie_cap_changes']+=any([o[2][1],o[3][1]]!=[parts[0][1],parts[1][1]] for o in ties)
            try:
                restored=join(parts[0][2],parts[1][2])
            except (RuntimeError,ValueError):
                restored=None
            stats['roundtrip_mismatch']+=s!=restored
        rows.append(dict(s=s,y=float(np.mean(labels)),p=parts,scaffold=MurckoScaffold.MurckoScaffoldSmiles(mol=m,includeChirality=False)))
    dec=[r for r in rows if r['p']]
    stats['clean']=len(rows)
    assert len(rows)+stats['merged']+stats['conflict_rows']+stats['invalid']==stats['raw']
    out = dict(binary=binary,rows=rows,stats=dict(stats),sha256=digest,splits=split(dec,binary),clean_splits=split(rows,binary))
    Path('audit',key+'.json').write_text(json.dumps(out,separators=(',',':')))
    print(key, dict(stats), flush=True)

if __name__=='__main__':
    for key,entry in json.loads(Path('data/manifest.json').read_text()).items():
        main(key,entry)
