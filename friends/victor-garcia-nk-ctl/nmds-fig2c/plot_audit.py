"""Check published Figure 2C directly, using its PDF vector marks and ticks."""
import json
from pathlib import Path
import csv
import numpy as np
import pymupdf
from scipy.optimize import isotonic_regression

root=Path(__file__).resolve().parent
page=pymupdf.open(root/'evidence/paper.pdf')[4]
points=[]
for drawing in page.get_drawings():
    r=drawing['rect']
    if (238<r.x0<374 and 147<r.y0<294 and drawing['type']=='fs'
            and len(drawing['items'])==4):
        points.append([(r.x0+r.x1)/2,(r.y0+r.y1)/2])
points=np.array(points)
assert points.shape==(23,2)
# All facets share axis scales; x ticks are printed at the bottom, y ticks
# at the left. Use centers of identical-width labels to avoid font offsets.
words=page.get_text('words')
x100=next(w for w in words if w[4]=='100' and w[0]>300 and w[1]>460)
x200=next(w for w in words if w[4]=='200' and w[0]>350 and w[1]>460)
y100=next(w for w in words if w[4]=='100' and w[0]<100 and w[1]<190)
y0=next(w for w in words if w[4]=='0' and w[0]<100 and 220<w[1]<240)
sx=((x200[0]+x200[2])-(x100[0]+x100[2]))/200
sy=((y0[1]+y0[3])-(y100[1]+y100[3]))/200
coordinates=points/np.array([sx,-sy])
profiles=np.loadtxt(root/'results/independent_profiles.csv',delimiter=',')
pairs=[(i,j) for i in range(23) for j in range(i+1,23)]
# Round back to exact tenths before ordering.
profiles=np.rint(profiles*10).astype(np.int64)
order=sorted(range(253),key=lambda k:int(np.sum((profiles[pairs[k][0]]-profiles[pairs[k][1]])**2)))
y=np.array([np.linalg.norm(coordinates[pairs[k][0]]-coordinates[pairs[k][1]]) for k in order])
fit=isotonic_regression(y).x
stress=100*np.linalg.norm(y-fit)/np.linalg.norm(y)
assert round(stress,1)==23.4
default=np.loadtxt('friends_new_victor_1104/results/rudorf_default_coords.csv',delimiter=',',skiprows=1)
# Vector marks occur in original sequence row order. Verify all 23 match,
# allowing translation and the tick-defined horizontal/vertical scaling.
pred=default*np.array([sx,-sy]); pred+=np.mean(points-pred,axis=0)
max_error=float(np.max(np.linalg.norm(pred-points,axis=1)))
assert max_error<0.01
result={'points':len(points),'x_pdf_units_per_data_unit':sx,'y_pdf_units_per_data_unit':sy,
        'published_vector_stress_percent':float(stress),
        'default_max_error_pdf_points':max_error,
        'note':'PDF rendering precision; independent axis tick scaling, row order corroborated against all default marks.'}
(root/'results/published_plot_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
