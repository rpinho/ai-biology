"""Secondary equal-size salt-fragment tie check. Preserve all primary artifacts."""
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
from collections import defaultdict

import numpy as np
from chem import Chem, MurckoScaffold, cuts, smiles
from prepare import split

ROOT=Path(__file__).resolve().parents[1]

def run():
    sub=ROOT/'audit/salt-sensitivity'
    (sub/'audit').mkdir(parents=True,exist_ok=True)
    summary={}
    for key,entry in json.loads(Path('data/manifest.json').read_text()).items():
        grouped=defaultdict(list)
        for r in csv.DictReader(Path('data',entry['filename']).open(),delimiter='\t'):
            m=Chem.MolFromSmiles(r['Drug'])
            if m is None:
                continue
            pieces=Chem.GetMolFrags(m,asMols=True,sanitizeFrags=True)
            s=min((-p.GetNumHeavyAtoms(),smiles(p)) for p in pieces)[1]
            grouped[s].append(float(r['Y']))
        d=json.loads(Path('audit',key+'.json').read_text())
        originals={r['s']:r for r in d['rows']}
        rows=[]
        for s,ys in sorted(grouped.items()):
            if d['binary'] and len(set(ys))>1:
                continue
            if s in originals:
                r=dict(originals[s])
            else:
                m=Chem.MolFromSmiles(s)
                options=cuts(m)
                r=dict(s=s,scaffold=MurckoScaffold.MurckoScaffoldSmiles(mol=m,includeChirality=False),p=options[0][2:] if options else None)
            r['y']=float(np.mean(ys))
            rows.append(r)
        decomp=[r for r in rows if r['p']]
        splits=split(decomp,d['binary'])
        summ=dict(clean=len(rows),decomp=len(decomp))
        for name,(tr,va,te) in splits.items():
            seen=[{decomp[i]['p'][j][1] for i in tr} for j in (0,1)]
            both=sum(all(decomp[i]['p'][j][1] in seen[j] for j in (0,1)) for i in te)
            summ[name]=dict(both=both,n=len(te))
        summary[key]=summ
        if key=='solubility_aqsoldb':
            obj=dict(rows=rows,binary=False,splits={'scaffold':splits['scaffold']},clean_splits=split(rows,False))
            (sub/'audit'/f'{key}.json').write_text(json.dumps(obj,separators=(',',':')))
    (sub/'counts.json').write_text(json.dumps(summary,indent=2))
    key='solubility_aqsoldb'
    for script,args in [('teacher',[key]),('neural',[key,'scaffold']),('statistics_audit',[key,'scaffold'])]:
        subprocess.run([sys.executable,str(ROOT/'src'/f'{script}.py'),*args],check=True,cwd=sub)
if __name__=='__main__':
    run()
