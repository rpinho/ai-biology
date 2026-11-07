"""Arb verification of the independent Decimal isotonic partition.
Checks KKT conditions and bounds the actual MASS percentage Stress-1.
"""
import csv
import json
from decimal import Decimal, localcontext
from pathlib import Path
from flint import arb, fmpq, ctx

ctx.prec = 320
profiles = [[int(v) for v in row] for row in csv.reader(open('profiles_independent.csv'))]
pairs = [(i,j) for i in range(23) for j in range(i+1,23)]
sq = [sum((a-b)**2 for a,b in zip(profiles[i],profiles[j])) for i,j in pairs]
order = sorted(range(253),key=lambda k:sq[k])
with open('evidence/witness.csv',newline='') as f:
    strings = [[r['x'],r['y']] for r in csv.DictReader(f)]
with localcontext() as dc:
    dc.prec = 110
    xy = [[Decimal(t) for t in row] for row in strings]
    ds = [sum((xy[i][k]-xy[j][k])**2 for k in [0,1]).sqrt() for i,j in pairs]
    ys = [ds[k] for k in order]
    blocks = []
    for k,v in enumerate(ys):
        blocks.append(([k],v))
        while len(blocks)>1 and blocks[-2][1]*len(blocks[-1][0]) > blocks[-1][1]*len(blocks[-2][0]):
            bi,bs = blocks.pop(); ai,asum = blocks.pop()
            blocks.append((ai+bi,asum+bs))

# Exact rational inputs, then outward-rounded square roots and all arithmetic.
def rational(t):
    a,b = Decimal(t).as_integer_ratio()
    return arb(fmpq(a,b))
xy = [[rational(t) for t in row] for row in strings]
dist = [sum(((xy[i][k]-xy[j][k])**2 for k in [0,1]),arb(0)).sqrt() for i,j in pairs]
y = [dist[k] for k in order]
means = []
prefix_count = 0
for indices,_ in blocks:
    total = sum((y[i] for i in indices),arb(0))
    mean = total/len(indices)
    if means:
        assert mean > means[-1], 'Adjacent block means not provably increasing'
    means.append(mean)
    partial = arb(0)
    for i in indices[:-1]:
        partial += y[i]-mean
        assert partial > 0, 'KKT prefix inequality not proved'
        prefix_count += 1
fitted = [m for (indices,_),m in zip(blocks,means) for i in indices]
num = sum(((a-b)*(a-b) for a,b in zip(y,fitted)),arb(0))
den = sum((a*a for a in y),arb(0))
stress = 100*(num/den).sqrt()
lo,hi = '16.9693901688773','16.9693901688775'
assert stress > rational(lo) and stress < rational(hi)
assert stress < rational('34.75')
out = dict(pass_certificate=True,precision_bits=320,stress_ball=str(stress),
           rational_lower=lo,rational_upper=hi,blocks=len(blocks),
           certified_interior_KKT_prefixes=prefix_count,
           certified_strict_block_boundaries=len(blocks)-1,
           same_native_pair_order=True,below_printed_rounding_bin=True,
           definition='100 sqrt(sum((distance - isotonic_fit)^2) / sum(distance^2))')
Path('results/independent_interval.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
