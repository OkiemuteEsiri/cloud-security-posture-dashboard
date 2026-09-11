# Cloud Security Posture Dashboard

A recruiter-facing, defensive multi-cloud security engineering project that normalizes synthetic AWS, Azure, and GCP posture findings, calculates explainable risk, validates remediation evidence, and produces engineering-oriented posture reports.

## Problem statement
Cloud security data is fragmented across providers and control families. Raw finding counts often hide the difference between internet exposure, privileged identity risk, missing telemetry, encryption gaps, and low-impact hygiene issues. This project demonstrates a provider-neutral control model that turns synthetic posture evidence into prioritized, reproducible remediation decisions.

## Architecture

```text
Synthetic AWS/Azure/GCP findings
          |
          v
 fail-closed ingestion
          |
          v
 normalized Finding model
          |
          +--> risk engine --> priority / score / ATT&CK context
          |
          +--> metrics engine --> provider/control/severity posture
          |
          +--> remediation validator --> closure evidence state
          |
          v
 Markdown executive + engineering report
```

## Repository structure
- `src/models.py` — immutable domain models and validation.
- `src/ingest.py` — fail-closed JSON ingestion and duplicate rejection.
- `src/risk_engine.py` — deterministic contextual scoring and prioritization.
- `src/remediation.py` — evidence-based remediation validation.
- `src/reporting.py` — portfolio metrics and Markdown reporting.
- `src/cli.py` — offline command-line assessment workflow.
- `data/synthetic_findings.json` — realistic fictional AWS/Azure/GCP findings.
- `data/remediation_evidence.json` — synthetic closure/validation evidence.
- `tests/` — unit tests for validation, scoring, reporting, and remediation logic.
- `docs/architecture.md` — technical design and trust boundaries.
- `docs/methodology.md` — assessment, remediation, and retest methodology.
- `reports/example_assessment.md` — example recruiter-facing output.

## Risk model
The model starts with severity and adds bounded context for internet exposure, privileged identity impact, critical assets, known-exploited context, missing logging, and overdue remediation. Critical controls remain explicit findings; a numeric score never suppresses a hard security condition.

Priority bands: `critical >= 85`, `high >= 65`, `medium >= 40`, otherwise `low`.

## Control families
Identity & access, public exposure, network segmentation, encryption, logging/monitoring, secrets management, workload security, and configuration governance.

## MITRE ATT&CK context
Mappings are threat-model context only, not proof of compromise:
- T1078 — Valid Accounts
- T1190 — Exploit Public-Facing Application
- T1552 — Unsecured Credentials
- T1562 — Impair Defenses
- T1040 — Network Sniffing

## Usage
```bash
python -m src.cli data/synthetic_findings.json --remediation data/remediation_evidence.json --output posture-report.md
python -m unittest discover -s tests -v
```
No cloud credentials or SDK access are required.

## Remediation workflow
1. Identify the authoritative cloud configuration and accountable owner.
2. Correct the preventive or detective control in the approved change process.
3. Capture change evidence and the post-change control state.
4. Re-evaluate the normalized finding.
5. Validate effectiveness with a defined verification method.
6. Close only when evidence demonstrates the risk condition is removed or explicitly accepted.

## Design decisions
- Provider-neutral normalized schema.
- Immutable models for reproducibility.
- Fail-closed parsing for malformed or duplicate evidence.
- Deterministic IDs and scoring for auditability.
- Synthetic data only; no live enumeration or mutation.
- Closure requires validation evidence rather than ticket status alone.

## Limitations
This is an offline engineering lab, not a CSPM replacement. It does not enumerate tenants, call cloud APIs, mutate resources, verify IAM reachability dynamically, or prove exploitability. Provider-specific semantics are intentionally simplified for transparent portfolio demonstration.

## Skills demonstrated
Cloud security posture management, security data normalization, contextual risk prioritization, IAM/public-exposure reasoning, defensive ATT&CK mapping, remediation governance, Python engineering, unit testing, reporting, and CI/CD security hygiene.

## Roadmap
- Policy-as-code adapters for OPA/Rego fixtures.
- Historical posture trend calculation.
- Control-framework mapping to CIS/NIST using versioned fixture metadata.
- SARIF/JSON report exporters.
- Synthetic IaC drift comparison.

## Safety
All resources, identities, account IDs, findings, and evidence are fictional. The project contains no credentials, production targeting, exploit payloads, or employer/client data.
