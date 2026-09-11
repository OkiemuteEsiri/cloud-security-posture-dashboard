from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from .models import Assessment, Finding

BASE = {"critical": 70, "high": 52, "medium": 30, "low": 12}


def assess(finding: Finding, now: datetime | None = None) -> Assessment:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    score = BASE[finding.severity]
    reasons = [f"base:{finding.severity}"]
    modifiers = [
        (finding.internet_exposed, 14, "internet-exposed"),
        (finding.privileged_identity, 14, "privileged-identity"),
        (finding.critical_asset, 10, "critical-asset"),
        (finding.known_exploited_context, 12, "known-exploited-context"),
        (not finding.logging_enabled, 8, "logging-gap"),
        (finding.status == "open" and now > finding.due_at, 10, "overdue"),
    ]
    for condition, points, reason in modifiers:
        if condition:
            score += points
            reasons.append(reason)
    if finding.status == "remediated":
        score = max(0, score - 35)
        reasons.append("remediated-awaiting-or-with-validation")
    elif finding.status == "accepted":
        score = max(0, score - 10)
        reasons.append("risk-accepted")
    score = min(100, score)
    priority = "critical" if score >= 85 else "high" if score >= 65 else "medium" if score >= 40 else "low"
    material = "|".join([finding.finding_id, str(score), priority, *sorted(reasons)])
    decision_id = hashlib.sha256(material.encode()).hexdigest()[:16]
    return Assessment(finding.finding_id, score, priority, tuple(reasons), decision_id)


def assess_all(findings: list[Finding], now: datetime | None = None) -> list[Assessment]:
    return sorted((assess(f, now) for f in findings), key=lambda a: (-a.score, a.finding_id))
