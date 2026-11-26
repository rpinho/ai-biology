"""Sequential process isolation; restartable at individual fits."""
import subprocess
import sys
from pathlib import Path
for key in ('herg','lipophilicity_astrazeneca','solubility_aqsoldb','cyp3a4_veith'):
    if not Path('audit',key+'-random-audit.json').exists():
        subprocess.run([sys.executable,'src/teacher.py',key],check=True)
    for name in ('scaffold','random'):
        subprocess.run([sys.executable,'src/neural.py',key,name],check=True)
        with open('STATUS.md','a') as f:
            print(f'Completed {key} {name} model fits.',file=f)
