from __future__ import annotations

import os
import sys
from pathlib import Path


os.environ["DEBUG"] = "false"
os.environ.setdefault("APP_ENV", "testing")

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
