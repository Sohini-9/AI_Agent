from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"


def load_json(file_name: str) -> Any:
    return json.loads((DATA_DIR / file_name).read_text(encoding="utf-8"))


def load_text(file_name: str) -> str:
    return (DATA_DIR / file_name).read_text(encoding="utf-8")


def write_report(file_name: str, content: str) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / file_name
    path.write_text(content, encoding="utf-8")
    return path

