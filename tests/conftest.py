from __future__ import annotations

import sys
from pathlib import Path

def _project_root() -> Path:
    # tests/ -> project root
    return Path(__file__).resolve().parents[1]

ROOT = _project_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))