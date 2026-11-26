"""Run one subprocess group, monitor job group RSS without logging command lines."""
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
assert Path.cwd() == root
deadline = float(os.environ.get("AUDIT_DEADLINE", datetime(2026,11,25,21,24,tzinfo=timezone.utc).timestamp()))
env = dict(os.environ, TMPDIR=str(root/".tmp"), XDG_CACHE_HOME=str(root/".cache"),
           MPLCONFIGDIR=str(root/".cache"), OMP_NUM_THREADS="4", OPENBLAS_NUM_THREADS="1",
           VECLIB_MAXIMUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONHASHSEED="0")
if time.time() >= deadline:
    sys.exit("deadline reached")
p = subprocess.Popen(sys.argv[1:], start_new_session=True, env=env)
peak = 0
def stop(*args):
    raise SystemExit(130)
signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
try:
    while p.poll() is None:
        listing = subprocess.check_output(["ps","-axo","pgid=,rss="], text=True)
        rss = sum(int(r)*1024 for g,r in (row.split() for row in listing.splitlines()) if int(g)==p.pid)
        peak = max(peak, rss)
        if rss >= 5_850_000_000 or time.time() >= deadline:
            sys.exit("resource stop")
        time.sleep(1)
finally:
    try:
        os.killpg(p.pid, signal.SIGTERM)
        time.sleep(0.3)
        os.killpg(p.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    p.wait()
    with open("audit/resources.tsv","a") as f:
        print(datetime.now(timezone.utc).isoformat(), sys.argv[2:], peak, p.returncode, sep="\t", file=f)
sys.exit(p.returncode)
