import json
from pathlib import Path
from control_runs import run
cases=[
 ('recovery-after-extreme-immune-transient',0.2,1,1e9,2,10,200000),
 ('slow-boundary-approach-U=a',0.514,0.002,100,1,0,1000000),
 ('degenerate-boundary-U=a-Vcrit',0.514,10922486893/12500000000000,100,1,0,1000000),
]
out=[]
for case in cases:
    result=run(case,max_step=100);out.append(result);print(json.dumps(result),flush=True)
Path('extended_controls.json').write_text(json.dumps(out,indent=2))
print('EXTENDED CONTROLS DONE; finite diagnostics, not a proof')
