# Cloud Security Posture Dashboard

A defensive, recruiter-facing multi-cloud security engineering project that normalizes synthetic AWS, Azure, and GCP posture findings, calculates explainable risk, validates remediation evidence, and produces engineering-oriented posture reports.

> **Portfolio role:** Cloud Security flagship. The project demonstrates provider-neutral security data engineering, contextual prioritization, remediation governance, and evidence-based validation without requiring cloud credentials or production access.

## Recruiter quick review

For a short technical review, follow this path:

1. `src/models.py` — normalized cloud finding model and fail-closed validation.
2. `src/risk_engine.py` — deterministic contextual prioritization.
3. `src/remediation.py` — evidence-based closure and revalidation logic.
4. `reports/example_assessment.md` — synthetic analyst-facing output.
5. `docs/control-validation-matrix.md` — mapping from risk condition to remediation evidence and revalidation.
6. `tests/` and `.github/workflows/ci.yml` — automated quality controls.

A more detailed review sequence is available in [`docs/recruiter-review.md`](docs/recruiter-review.md).

## Recruiter signal at a glance

| Capability | Evidence |
|---|---|
| Multi-cloud security engineering | Provider-neutral normalization across synthetic AWS, Azure, and GCP findings |
| Risk prioritization | Explainable 0–100 scoring using severity plus exposure, identity, asset and telemetry context |
| Security governance | Remediation validation separates technical closure from ticket state or risk acceptance |
| Defensive threat modeling | ATT&CK context is attached where useful without claiming compromise |
| Engineering quality | Immutable models, strict parsing, duplicate rejection, deterministic IDs, unit tests and CI |
| Risk communication | Executive and engineering-oriented Markdown reporting |

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
- `src/posture_summary.py` — posture aggregation for portfolio views.
- `src/remediation.py` — evidence-based remediation validation.
- `src/reporting.py` — portfolio metrics and Markdown reporting.
- `src/cli.py` — offline command-line assessment workflow.
- `data/synthetic_findings.json` — realistic fictional AWS/Azure/GCP findings.
- `data/remediation_evidence.json` — synthetic closure/validation evidence.
- `tests/` — unit tests for validation, scoring, reporting, and remediation logic.
- `docs/architecture.md` — technical design and trust boundaries.
- `docs/methodology.md` — assessment, remediation, and retest methodology.
- `docs/control-validation-matrix.md` — control-family remediation and evidence expectations.
- `docs/recruiter-review.md` — concise technical review path.
- `reports/example_assessment.md` — example recruiter-facing output.

## Risk model

The model starts with severity and adds bounded context for internet exposure, privileged identity impact, critical assets, known-exploited context, missing logging, and overdue remediation. Critical controls remain explicit findings; a numeric score never suppresses a hard security condition.

Priority bands:

- `critical >= 85`
- `high >= 65`
- `medium >= 40`
- `low < 40`

The score is a transparent prioritization aid, not a claim of exploitability or a substitute for provider-native context.

## Control families

The normalized model covers identity and access, public exposure, network segmentation, encryption, logging/monitoring, secrets management, workload security, and configuration governance.

The [`control validation matrix`](docs/control-validation-matrix.md) documents expected impact, remediation evidence, and revalidation conditions for each family.

## MITRE ATT&CK context

Mappings are defensive threat-model context only, not proof of compromise:

- **T1078 — Valid Accounts**
- **T1190 — Exploit Public-Facing Application**
- **T1552 — Unsecured Credentials**
- **T1562 — Impair Defenses**
- **T1040 — Network Sniffing**

Technique mappings are used only where they clarify the security consequence of a finding. Provider misconfiguration alone is not treated as evidence that an adversary performed the mapped behavior.

## Usage

```bash
python -m src.cli data/synthetic_findings.json --remediation data/remediation_evidence.json --output posture-report.md
python -m unittest discover -s tests -v
```

No cloud credentials, SDK access, tenant identifiers, or live enumeration are required.

## Remediation and revalidation workflow

1. Identify the authoritative cloud configuration and accountable owner.
2. Define the exact risk condition being remediated.
3. Correct the preventive or detective control through an approved change process.
4. Capture implementation evidence and the post-change control state.
5. Re-evaluate the normalized finding against the original condition.
6. Validate effectiveness with a defined verification method.
7. Close only when evidence demonstrates the risk condition is removed or reduced as intended.

An approved risk exception changes governance state but does not erase technical exposure. Expired or weakly evidenced exceptions should not qualify as normal technical closure.

## Design decisions

- Provider-neutral normalized schema for consistent triage across AWS, Azure, and GCP examples.
- Immutable models for reproducibility.
- Fail-closed parsing for malformed or duplicate evidence.
- Deterministic IDs and scoring for auditability.
- Synthetic data only; no live enumeration or mutation.
- Closure requires validation evidence rather than ticket status alone.
- ATT&CK mappings explain plausible security impact without asserting compromise.

## CI and verification

The repository includes `.github/workflows/ci.yml` to exercise the implementation automatically. A workflow file does **not** by itself prove that a particular commit is healthy. CI status should always be evaluated against the exact commit under review; historical successful runs are evidence for those historical commits only.

## Limitations

This is an offline engineering lab, not a CSPM replacement. It does not enumerate tenants, call cloud APIs, mutate resources, validate IAM reachability dynamically, prove exploitability, or model every provider-specific control semantic. Provider-specific details are intentionally simplified so the decision logic remains transparent and reviewable.

## Skills demonstrated

Cloud security posture management, security data normalization, contextual risk prioritization, IAM/public-exposure reasoning, defensive ATT&CK mapping, remediation governance, evidence-based revalidation, Python engineering, unit testing, reporting, and CI/CD security hygiene.

## Roadmap

- Policy-as-code adapters for OPA/Rego fixtures.
- Historical posture trend calculation.
- Control-framework mapping to CIS/NIST using versioned fixture metadata.
- SARIF/JSON report exporters.
- Synthetic IaC drift comparison.

## Safety and data handling

All resources, identities, account IDs, findings, and evidence are fictional. The project contains no credentials, production targeting, exploit payloads, employer/client data, or claims of deployment in a real organization.
