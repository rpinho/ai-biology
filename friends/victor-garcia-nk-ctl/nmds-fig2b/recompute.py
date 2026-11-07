"""Independent reconstruction from primary PDFs and released sequences.
No claimant code is loaded. Native MASS defaults run before witness evaluation.
"""
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from decimal import Decimal, localcontext
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
E = ROOT / 'evidence'
text = '\n'.join(p.extract_text() for p in PdfReader(E/'shah_fresh.pdf').pages)
entries = list(re.finditer(r'(?m)^([A-Z])\s+([ACGU]{3})\s+', text))
rate = {}
for index, match in enumerate(entries):
    end = entries[index+1].start() if index+1 < len(entries) else len(text)
    values = re.findall(r'(?<![\d.])(\d+\.\d{3})(?!\d)', text[match.end():end])
    assert len(values) == 1, (match.group(2), values)
    rate[match.group(2).replace('U','T')] = int(Decimal(values[0])*1000)
assert len(rate) == 61
with (E/'sequences.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
profiles = []
for row in rows:
    seq = row["Sequence 5' → 3'"].strip().upper()
    assert len(seq) == 1164 and seq[-3:] in {'TAA','TGA','TAG'}
    # Stops are termination, not elongation; all 387 remaining codons have Rc.
    codons = [seq[i:i+3] for i in range(0,len(seq)-3,3)]
    assert len(codons) == 387 and all(c in rate for c in codons)
    profiles.append([rate[c] for c in codons])
assert len(profiles) == 23
with open('profiles_independent.csv','w',newline='') as f:
    csv.writer(f).writerows(profiles)
(ROOT/'rates_independent.json').write_text(json.dumps(rate,sort_keys=True,indent=2)+'\n')
pairs = [(i,j) for i in range(23) for j in range(i+1,23)]
sq = [sum((a-b)**2 for a,b in zip(profiles[i], profiles[j])) for i,j in pairs]
order = sorted(range(253), key=lambda k:sq[k])
assert min(sq) > 0
rh = ROOT/'runtime/R-expanded/R-fw.pkg/Payload/R.framework/Versions/4.6/Resources'
env = dict(os.environ, R_HOME=str(rh), DYLD_LIBRARY_PATH=str(rh/'lib'),
           R_LIBS_USER=str(ROOT/'runtime/Rlib'), TMPDIR=str(ROOT/'tmp'),
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')
run = subprocess.run([str(rh/'bin/exec/R'),'--vanilla','--slave','-f','standard_referee.R'],
                     env=env, capture_output=True,text=True)
(ROOT/'results/native_R.log').write_text(run.stdout+run.stderr)
assert run.returncode == 0, (run.returncode, run.stderr)
r_order = [int(s)-1 for s in Path('native_order.txt').read_text().split()]
assert r_order == order, 'Native and exact dissimilarity orders differ'

def evaluate(filename, digits):
    with localcontext() as ctx:
        ctx.prec = digits
        with open(filename,newline='') as f:
            xy = [[Decimal(r['x']),Decimal(r['y'])] for r in csv.DictReader(f)]
        assert len(xy) == 23
        y = [sum((xy[i][k]-xy[j][k])**2 for k in range(2)).sqrt() for i,j in pairs]
        y = [y[k] for k in order]
        blocks = []
        for v in y:
            blocks.append((v,1))
            while len(blocks)>1 and blocks[-2][0]*blocks[-1][1] > blocks[-1][0]*blocks[-2][1]:
                b,n = blocks.pop(); a,m = blocks.pop()
                blocks.append((a+b,m+n))
        fit = [a/n for a,n in blocks for _ in range(n)]
        stress = 100*(sum((a-b)**2 for a,b in zip(y,fit))/sum(a*a for a in y)).sqrt()
        return {'stress':str(stress),'blocks':len(blocks)}

result = {'sequences':23,'codons':387,'pairs':253,'unique_dissimilarities':len(set(sq)),
          'exact_and_native_order_agree':True,
          'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in [E/'paper.pdf',E/'shah_fresh.pdf',E/'sequences.csv',E/'witness.csv']}}
for label,filename in [('native_default','native_default.csv'),('witness',E/'witness.csv')]:
    result[label] = {str(d):evaluate(filename,d) for d in [70,110]}
Path('results/recomputed.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
