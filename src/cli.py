from __future__ import annotations

import argparse
from pathlib import Path
from .ingest import load_findings
from .remediation import load_remediation
from .reporting import render_markdown
from .risk_engine import assess_all


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline synthetic multi-cloud posture assessor")
    parser.add_argument("findings")
    parser.add_argument("--remediation")
    parser.add_argument("--output")
    args = parser.parse_args()
    findings = load_findings(args.findings)
    assessments = assess_all(findings)
    remediation = load_remediation(args.remediation) if args.remediation else []
    report = render_markdown(findings, assessments, remediation)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
