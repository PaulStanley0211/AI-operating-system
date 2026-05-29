import sys
from pathlib import Path

# Put the repo root on sys.path so `import actions.triage.*` works in tests.
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
