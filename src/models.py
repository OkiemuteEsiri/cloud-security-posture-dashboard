from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping

PROVIDERS = {"aws", "azure", "gcp"}
SEVERITIES = {"critical", "high", "medium", "low"}
CONTROL_FAMILIES = {"identity", "exposure", "network", "encryption", "logging", "secrets", "workload", "governance"}


def parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return dt.astimezone(timezone.utc)


@dataclass(frozen=True)
class Finding:
    finding_id: str
    provider: str
    account: str
    resource_id: str
    title: str
    severity: str
    control_family: str
    owner: str
    detected_at: datetime
    due_at: datetime
    internet_exposed: bool = False
    privileged_identity: bool = False
    critical_asset: bool = False
    known_exploited_context: bool = False
    logging_enabled: bool = True
    status: str = "open"
    attack_id: str | None = None

    @classmethod
    def from_dict(cls, raw: Mapping[str, object]) -> "Finding":
        required = {"finding_id", "provider", "account", "resource_id", "title", "severity", "control_family", "owner", "detected_at", "due_at"}
        missing = sorted(required - raw.keys())
        if missing:
            raise ValueError(f"missing required fields: {', '.join(missing)}")
        provider = str(raw["provider"]).lower()
        severity = str(raw["severity"]).lower()
        family = str(raw["control_family"]).lower()
        if provider not in PROVIDERS:
            raise ValueError(f"unsupported provider: {provider}")
        if severity not in SEVERITIES:
            raise ValueError(f"unsupported severity: {severity}")
        if family not in CONTROL_FAMILIES:
            raise ValueError(f"unsupported control family: {family}")
        status = str(raw.get("status", "open")).lower()
        if status not in {"open", "remediated", "accepted"}:
            raise ValueError(f"unsupported status: {status}")
        finding_id = str(raw["finding_id"]).strip()
        owner = str(raw["owner"]).strip()
        if not finding_id or not owner:
            raise ValueError("finding_id and owner must be non-empty")
        return cls(
            finding_id=finding_id,
            provider=provider,
            account=str(raw["account"]),
            resource_id=str(raw["resource_id"]),
            title=str(raw["title"]),
            severity=severity,
            control_family=family,
            owner=owner,
            detected_at=parse_time(str(raw["detected_at"])),
            due_at=parse_time(str(raw["due_at"])),
            internet_exposed=bool(raw.get("internet_exposed", False)),
            privileged_identity=bool(raw.get("privileged_identity", False)),
            critical_asset=bool(raw.get("critical_asset", False)),
            known_exploited_context=bool(raw.get("known_exploited_context", False)),
            logging_enabled=bool(raw.get("logging_enabled", True)),
            status=status,
            attack_id=str(raw["attack_id"]) if raw.get("attack_id") else None,
        )


@dataclass(frozen=True)
class Assessment:
    finding_id: str
    score: int
    priority: str
    reasons: tuple[str, ...]
    decision_id: str
