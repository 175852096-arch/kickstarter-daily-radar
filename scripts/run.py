import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for script in ["collect.py", "report.py"]:
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT)
    if p.returncode:
        raise SystemExit(p.returncode)
