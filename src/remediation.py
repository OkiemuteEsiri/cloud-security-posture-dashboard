from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RemediationDecision:
    finding_id: str
    state: str
    missing_evidence: tuple[str, ...]


def validate_record(raw: dict) -> RemediationDecision:
    finding_id = str(raw.get("finding_id", "")).strip()
    if not finding_id:
        raise ValueError("remediation record requires finding_id")
    required = {
        "owner": raw.get("owner"),
        "change_reference": raw.get("change_reference"),
        "post_change_state": raw.get("post_change_state"),
        "validation_method": raw.get("validation_method"),
        "validation_result": raw.get("validation_result"),
    }
    missing = tuple(sorted(key for key, value in required.items() if not str(value or "").strip()))
    if missing:
        return RemediationDecision(finding_id, "needs_evidence", missing)
    result = str(raw["validation_result"]).lower()
    if result not in {"effective", "ineffective", "pending"}:
        raise ValueError("validation_result must be effective, ineffective, or pending")
    state = "validated" if result == "effective" else "invalid_closure" if result == "ineffective" else "ready_for_validation"
    return RemediationDecision(finding_id, state, ())


def load_remediation(path: str | Path) -> list[RemediationDecision]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("remediation root must be a list")
    decisions = [validate_record(item) for item in raw]
    ids = [d.finding_id for d in decisions]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate remediation finding_id detected")
    return decisions
