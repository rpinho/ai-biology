"""Independent fixed-witness audit; no producer/referee modules are used."""
import csv
import hashlib
import json
import re
from pathlib import Path
from fractions import Fraction

import numpy as np
from scipy.optimize import isotonic_regression
from pypdf import PdfReader
from flint import arb, ctx

HERE = Path(__file__).resolve().parent
SRC = HERE / 'evidence'
PRODUCER = HERE.parent.parent.parent / 'friends_new_victor_1104'
ctx.prec = 384

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

# Read the original supplementary PDF, first rate column, in exact tenths.
rate_text = '\n'.join(p.extract_text() for p in PdfReader(SRC/'rudorf_s2.pdf').pages)
rates = {}
for line in rate_text.splitlines():
    m = re.fullmatch(r'([ACGU]{3})\s+(\d+\.\d)\s+\d+\.\d\s+\d+\.\d\s+\d+\.\d', line.strip())
    if m:
        rates[m[1].replace('U','T')] = int(Fraction(m[2])*10)
assert len(rates) == 61
rows = list(csv.DictReader((SRC/'sequences.csv').open(encoding='utf-8-sig')))
assert len(rows) == 23
profiles = []
for row in rows:
    sequence = row["Sequence 5' → 3'"].strip().upper()
    assert len(sequence) % 3 == 0
    codons = [sequence[k:k+3] for k in range(0,len(sequence),3)]
    assert codons[-1] in {'TAA','TAG','TGA'}
    assert all(c in rates for c in codons[:-1])
    profiles.append([rates[c] for c in codons[:-1]])
assert {len(p) for p in profiles} == {387}
labels = [r['Construct name'] for r in rows]
# Candidate file has no labels: explicitly check its accompanying row manifest.
assert labels == json.loads((PRODUCER/'results/sequence_labels.json').read_text())
pairs = [(i,j) for i in range(23) for j in range(i+1,23)]
sq_input = [sum((a-b)**2 for a,b in zip(profiles[i],profiles[j])) for i,j in pairs]
assert min(sq_input)>0
order = sorted(range(253), key=lambda k:sq_input[k])
ordered_q = [sq_input[k] for k in order]

def ball(q):
    q = Fraction(q)
    return arb(q.numerator)/arb(q.denominator)

def pava(y, weights=None):
    blocks=[]
    for k,value in enumerate(y):
        w = 1 if weights is None else weights[k]
        blocks.append([k,k+1,float(value)*w,w])
        while len(blocks)>1 and blocks[-2][2]/blocks[-2][3] > blocks[-1][2]/blocks[-1][3]:
            right=blocks.pop(); left=blocks.pop()
            blocks.append([left[0],right[1],left[2]+right[2],left[3]+right[3]])
    fit=np.empty(len(y))
    for a,b,s,w in blocks:
        fit[a:b]=s/w
    return fit,blocks

def evaluate(path):
    coords = list(csv.reader(path.open()))[1:]
    assert len(coords)==23 and all(len(r)==2 for r in coords)
    xy = [[Fraction(v) for v in row] for row in coords]
    sq = [sum((xy[i][d]-xy[j][d])**2 for d in range(2)) for i,j in pairs]
    y = np.array([float(sq[k])**0.5 for k in order])
    fit,blocks = pava(y)
    assert np.max(np.abs(fit-isotonic_regression(y).x))<1e-10
    stress = 100*np.sqrt(np.sum((y-fit)**2)/np.sum(y*y))
    # Independently recompute distances and feasible disparities with Arb.
    distances = [ball(sq[k]).sqrt() for k in order]
    means = [sum(distances[a:b],arb(0))/(b-a) for a,b,_,_ in blocks]
    assert all(means[k]<means[k+1] for k in range(len(means)-1))
    residual = arb(0)
    kkt = True
    for (a,b,_,_), mean in zip(blocks,means):
        prefix=arb(0)
        for k in range(a,b):
            delta=distances[k]-mean
            residual+=delta*delta
            prefix+=delta
            if k<b-1 and not prefix>=0:
                kkt=False
    cert = 100*(residual/sum((ball(v) for v in sq),arb(0))).sqrt()
    assert cert<arb('23.35')
    # Sensitivity to the stricter alternative requiring equal fitted values
    # for exactly equal input dissimilarities (MASS uses stable rank order).
    groups=[]
    for k,q in enumerate(ordered_q):
        if groups and groups[-1][0]==q: groups[-1][2]=k+1
        else: groups.append([q,k,k+1])
    tied_y=[float(np.mean(y[a:b])) for _,a,b in groups]
    tied_fit,_=pava(tied_y,[b-a for _,a,b in groups])
    tied_full=np.empty(253)
    for val,(_,a,b) in zip(tied_fit,groups): tied_full[a:b]=val
    return {'file':str(path.relative_to(PRODUCER)) if path.is_relative_to(PRODUCER) else str(path.relative_to(HERE)),
            'sha256':sha(path),'stress_percent_float':float(stress),
            'stress_percent_arb':str(cert),'below_23_35_certified':bool(cert<arb('23.35')),
            'pava_blocks':len(blocks),'optimality_KKT_certified':kkt,
            'equal_input_ties_stress_percent':float(100*np.linalg.norm(y-tied_full)/np.linalg.norm(y))}

result={'sources':{str(p.relative_to(HERE)):sha(p) for p in [SRC/'paper.pdf',SRC/'rudorf_s2.pdf',SRC/'sequences.csv']},
        'n':23,'codon_positions':387,'pairs':253,'dimensions':2,
        'input_tie_count':253-len(set(sq_input)), 'labels':labels,
        'rates_in_tenths':rates,
        'candidate':evaluate(HERE/'results/rudorf_best_coords.csv')}
# Default coordinates are data, not trusted solver output; evaluate separately.
default_path=PRODUCER/'results/rudorf_default_coords.csv'
# The generic routine above asserts improvement, so evaluate default using a
# separate float-only path, without treating it as a new certified candidate.
default=np.loadtxt(default_path,delimiter=',',skiprows=1)
y=np.array([np.linalg.norm(default[pairs[k][0]]-default[pairs[k][1]]) for k in order])
f,_=pava(y)
result['supplied_default_stress_percent']=float(100*np.linalg.norm(y-f)/np.linalg.norm(y))
np.savetxt(HERE/'results/independent_profiles.csv',np.array(profiles)/10,delimiter=',')
(HERE/'results/independent_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
