# Recruiter Review Guide

This guide provides a short technical path through the Cloud Security Posture Dashboard without requiring a reviewer to inspect every file.

## Five-minute review path

1. Read `README.md` for the problem statement, architecture, risk model, safety boundaries, and usage.
2. Review `src/models.py` to see the normalized provider-neutral finding model and input validation.
3. Review `src/risk_engine.py` for deterministic contextual prioritization across severity, exposure, identity, asset criticality, logging, exploit context, and remediation age.
4. Review `src/remediation.py` for evidence-based closure and revalidation logic.
5. Review `reports/example_assessment.md` for the analyst-facing output produced from synthetic AWS, Azure, and GCP evidence.
6. Review `tests/` and `.github/workflows/ci.yml` for automated quality controls.

## Capability-to-evidence map

| Capability | Evidence in this repository |
|---|---|
| Multi-cloud security normalization | Provider-neutral models plus synthetic AWS, Azure, and GCP findings |
| Risk-based prioritization | Deterministic 0-100 contextual scoring and priority bands |
| Identity and exposure reasoning | Privileged-identity, public-exposure, critical-asset, and logging context |
| Remediation governance | Closure requires change evidence, post-change state, and validation outcome |
| Security reporting | Executive and engineering-oriented Markdown assessment output |
| Defensive threat modeling | MITRE ATT&CK context used to explain risk, not to claim compromise |
| Engineering quality | Unit tests, fail-closed parsing, duplicate rejection, deterministic identifiers, CI workflow |

## What the project demonstrates

The project is designed to answer practical security-engineering questions:

- How can findings from different cloud providers be normalized without losing important risk context?
- Which findings should be remediated first when raw severity alone is insufficient?
- How should privileged identity, internet exposure, critical assets, missing telemetry, and remediation age change priority?
- What evidence should be required before a cloud-security finding is considered remediated?
- How can executive posture reporting remain traceable to engineering evidence?

## Review boundaries

This repository is intentionally offline. It does not enumerate cloud tenants, call provider APIs, modify resources, validate live IAM reachability, or perform exploitation. All account IDs, resources, identities, findings, and remediation evidence are synthetic.

The project demonstrates security-engineering design and reasoning rather than claiming production deployment or access to any employer/client environment.

## CI interpretation

The presence of `.github/workflows/ci.yml` is not itself evidence of a passing build. Reviewers should evaluate the GitHub Actions result associated with the exact commit being reviewed. Historical green runs are useful evidence but do not automatically transfer to later commits.
