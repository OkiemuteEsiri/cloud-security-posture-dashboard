# Cloud Security Posture Dashboard

A defensive cloud-security engineering project for summarizing configuration risk, identity exposure, logging coverage, encryption posture, and remediation status across synthetic cloud assets.

## Objectives

- Normalize cloud-security findings into a common schema.
- Highlight high-risk misconfigurations and privileged identity exposure.
- Track remediation ownership and aging.
- Distinguish preventive controls from detective controls.
- Present posture metrics in a way that supports engineering decisions rather than vanity reporting.

## Repository structure

- `data/sample_findings.csv` — synthetic cloud findings
- `src/posture_summary.py` — simple posture aggregation logic
- `docs/control-model.md` — control categories and interpretation guidance

## Example control areas

Identity and access, public exposure, encryption, logging, key management, network segmentation, secrets handling, container security, and configuration drift.

## Safety
This project uses synthetic findings only. It does not contain cloud credentials, tenant identifiers, production account data, or provider secrets.
