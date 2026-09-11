from __future__ import annotations

import json
from pathlib import Path
from .models import Finding


def load_findings(path: str | Path) -> list[Finding]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("root document must be a list")
    findings = [Finding.from_dict(item) for item in raw]
    ids = [f.finding_id for f in findings]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate finding_id detected")
    return findings
