"""Read Figure 2's actual vector circles and labeled axis grid from the PDF.
Tests the original configuration rather than relying on the caption alone.
"""
import csv
import json
from pathlib import Path
import numpy as np
import pymupdf

doc = pymupdf.open('evidence/paper.pdf')
page = doc[4]
drawings = page.get_drawings()
points = []
for d in drawings:
    r = d['rect']
    if d['type']=='fs' and len(d['items'])==4 and 98<r.x0<230 and 314<r.y0<460:
        points.append(((r.x0+r.x1)/2,(r.y0+r.y1)/2))
assert len(points)==23
# Actual major ticks from the plot. Labels checked against page.get_text words:
# x=-100,0,100,200; y=-50,0,50,100. Use ticks, not font bounding boxes.
xticks=[]; yticks=[]
for d in drawings:
    r=d['rect']
    if d['type']=='s' and len(d['items'])==1 and d['width']>.9:
        if 114<r.x0<231 and r.x0==r.x1 and 461<r.y0<462 and r.y1<465:
            xticks.append(r.x0)
        if 95<r.x0<96 and r.x1<99 and r.y0==r.y1 and 340<r.y0<433:
            yticks.append(r.y0)
assert len(xticks)==4 and len(yticks)==4
xscale,xzero=np.polyfit([-100,0,100,200],sorted(xticks),1)
yscale,yzero=np.polyfit([-50,0,50,100],sorted(yticks,reverse=True),1)
xy=(np.array(points)-[xzero,yzero])/[xscale,yscale]
with open('pdf_points.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['x','y']); w.writerows(xy)
native=np.genfromtxt('native_default.csv',delimiter=',',skip_header=1)
errors=np.abs(xy-native)
profiles=np.genfromtxt('profiles_independent.csv',delimiter=',')
pairs=[(i,j) for i in range(23) for j in range(i+1,23)]
order=sorted(range(253),key=lambda k:sum((profiles[pairs[k][0]]-profiles[pairs[k][1]])**2))
y=np.array([np.linalg.norm(xy[i]-xy[j]) for i,j in pairs])[order]
blocks=[]
for v in y:
    blocks.append((v,1))
    while len(blocks)>1 and blocks[-2][0]*blocks[-1][1]>blocks[-1][0]*blocks[-2][1]:
        b,n=blocks.pop(); a,m=blocks.pop(); blocks.append((a+b,m+n))
fit=np.array([a/n for a,n in blocks for _ in range(n)])
stress=100*np.sqrt(sum((y-fit)**2)/sum(y*y))
assert errors.max()<.02
assert round(stress,1)==34.8
out={'pdf_stress_approx':float(stress),'max_native_coordinate_error':float(errors.max()),
     'points':23,'x_tick_scale':float(xscale),'y_tick_scale':float(yscale),
     'note':'Drawing order matches released sequence order; axis-calibrated PDF rounding causes small errors.'}
Path('results/pdf_plot_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
