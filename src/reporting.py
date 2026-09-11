from __future__ import annotations

from collections import Counter
from .models import Assessment, Finding
from .remediation import RemediationDecision


def metrics(findings: list[Finding], assessments: list[Assessment]) -> dict:
    by_priority = Counter(a.priority for a in assessments)
    by_provider = Counter(f.provider for f in findings)
    by_family = Counter(f.control_family for f in findings)
    return {
        "total": len(findings),
        "open": sum(f.status == "open" for f in findings),
        "internet_exposed": sum(f.internet_exposed for f in findings),
        "logging_gaps": sum(not f.logging_enabled for f in findings),
        "by_priority": dict(sorted(by_priority.items())),
        "by_provider": dict(sorted(by_provider.items())),
        "by_control_family": dict(sorted(by_family.items())),
    }


def render_markdown(findings: list[Finding], assessments: list[Assessment], remediation: list[RemediationDecision] | None = None) -> str:
    m = metrics(findings, assessments)
    rem = {r.finding_id: r for r in (remediation or [])}
    lines = ["# Cloud Security Posture Assessment", "", "## Executive metrics", "", f"- Total findings: **{m['total']}**", f"- Open findings: **{m['open']}**", f"- Internet-exposed findings: **{m['internet_exposed']}**", f"- Logging gaps: **{m['logging_gaps']}**", f"- Priority distribution: `{m['by_priority']}`", f"- Provider distribution: `{m['by_provider']}`", "", "## Prioritized findings", "", "| ID | Provider | Control | Score | Priority | Remediation evidence |", "|---|---|---|---:|---|---|"]
    finding_map = {f.finding_id: f for f in findings}
    for a in assessments:
        f = finding_map[a.finding_id]
        state = rem[a.finding_id].state if a.finding_id in rem else "not-submitted"
        lines.append(f"| {f.finding_id} | {f.provider} | {f.control_family} | {a.score} | {a.priority} | {state} |")
    lines.extend(["", "## Interpretation", "", "Scores prioritize engineering attention; they do not prove exploitability or compromise. Closure requires authoritative configuration change plus effectiveness validation."])
    return "\n".join(lines) + "\n"
