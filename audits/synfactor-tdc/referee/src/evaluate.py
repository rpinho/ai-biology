import json
import subprocess
import sys
from pathlib import Path

def run(*args):
    subprocess.run([sys.executable,*args],check=True)
for kind in ('ridge','pair','cp'):
    run('src/verify_controls.py',kind)
run('src/crosscheck.py')
run('src/leakage.py')
for key in ('herg','lipophilicity_astrazeneca','solubility_aqsoldb','cyp3a4_veith'):
    for name in ('scaffold','random'):
        if not Path('audit',key+'-'+name+'-stats.json').exists():
            run('src/statistics_audit.py',key,name)
        with open('STATUS.md','a') as f:
            print(f'Verified resampling harvest for {key} {name}.',file=f)
