"""Independent referee, prepared for mscr; never run on the Mini.
No imports from the claim's search or verifier. Run from the job directory.
"""
import csv, hashlib, json, re, subprocess
from decimal import Decimal, localcontext
from pathlib import Path
from pypdf import PdfReader

root=Path(__file__).resolve().parent
source=root/'evidence'
text='\n'.join(page.extract_text() for page in PdfReader(source/'shah_s2.pdf').pages)
starts=list(re.finditer(r'(?m)^([A-Z])\s+([ACGU]{3})\s+',text))
rates={}
for k,m in enumerate(starts):
    segment=text[m.end(): starts[k+1].start() if k+1<len(starts) else len(text)]
    rate=re.search(r'\b(\d+\.\d{3})\b',segment)
    assert rate, (m.group(2),segment)
    codon=m.group(2).replace('U','T')
    assert codon not in rates
    rates[codon]=int(Decimal(rate.group(1))*1000)
assert len(rates)==61,len(rates)
with open(source/'sequences.csv',encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
profiles=[]
for row in rows:
    dna=row["Sequence 5' → 3'"].strip().upper()
    assert len(dna)%3==0
    codons=[dna[i:i+3] for i in range(0,len(dna),3)]
    profiles.append([rates[c] for c in codons])
assert len(profiles)==23
assert len(set(map(len,profiles)))==1
with open(root/'profiles_independent.csv','w',newline='') as f:
    csv.writer(f).writerows(profiles)
# R dist order: lower triangular, column first. Integer squared distances
# fix the mathematical rank; native floating-point rank must also agree.
pairs=[(i,j) for i in range(23) for j in range(i+1,23)]
squared=[sum((a-b)**2 for a,b in zip(profiles[i],profiles[j])) for i,j in pairs]
rank=sorted(range(len(pairs)),key=lambda k:squared[k])
assert min(squared)>0
subprocess.run(['Rscript',str(root/'standard_referee.R')],check=True,cwd=root)
r_rank=[int(x)-1 for x in (root/'native_order.txt').read_text().split()]
assert rank==r_rank,'Exact-vs-native tie order differs; investigate before certifying.'

def evaluate(path,precision):
    with open(path,newline='') as f: coordinates=list(csv.DictReader(f))
    assert len(coordinates)==23
    with localcontext() as ctx:
        ctx.prec=precision
        xy=[[Decimal(row[c]) for c in ['x','y']] for row in coordinates]
        distances=[sum((xy[i][c]-xy[j][c])**2 for c in range(2)).sqrt() for i,j in pairs]
        y=[distances[k] for k in rank]
        # Pool adjacent violators: least-squares monotone fit in MASS rank order.
        blocks=[]
        for value in y:
            blocks.append([value,1])
            while len(blocks)>1 and blocks[-2][0]*blocks[-1][1]>blocks[-1][0]*blocks[-2][1]:
                b=blocks.pop();a=blocks.pop();blocks.append([a[0]+b[0],a[1]+b[1]])
        fitted=[s/n for s,n in blocks for _ in range(n)]
        numerator=sum((a-b)**2 for a,b in zip(y,fitted))
        denominator=sum(a*a for a in y)
        return str(100*(numerator/denominator).sqrt()),len(blocks)
results={}
for label,file in [('submitted',source/'witness.csv'),('native_default',root/'native_default.csv')]:
    results[label]={str(p):evaluate(file,p) for p in [80,120]}
results.update(sequence_count=23,codons=len(profiles[0]),pair_count=len(pairs),
               unique_squared_distances=len(set(squared)),
               hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir() if p.is_file()},
               caveat='Decimal precision cross-check, not an interval certificate')
(root/'independent_result.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
