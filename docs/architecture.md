# Architecture

## Objective
Provide a reproducible offline reference architecture for normalizing and prioritizing heterogeneous cloud posture evidence without requiring real cloud access.

## Components
1. **Ingestion boundary** — accepts JSON fixture evidence only and rejects malformed roots, unsupported providers/control families, timezone-naive timestamps, and duplicate finding IDs.
2. **Normalized model** — creates immutable provider-neutral `Finding` objects.
3. **Risk engine** — combines severity with bounded environmental context; output is deterministic for a fixed timestamp.
4. **Metrics/reporting** — aggregates provider, control-family, exposure, logging, and priority posture.
5. **Remediation validator** — separates change completion from proven effectiveness.
6. **CLI** — composes the modules without network access.

## Trust boundaries
Input files are untrusted until parsed. Provider names, severity, control family, status, identifiers, ownership and timestamps are validated before scoring. Reports never infer compromise from configuration posture.

## Security properties
- Fail closed on malformed/duplicate records.
- No secrets, cloud SDKs, or outbound requests.
- Immutable normalized evidence.
- Deterministic assessment IDs.
- Explicit hard findings preserved alongside risk scores.
- Remediation closure requires validation evidence.

## Data flow
`JSON -> validate -> normalize -> score -> aggregate -> remediation correlation -> Markdown report`

## Production evolution
A production implementation would add provider-specific collectors behind read-only identities, schema versioning, signed evidence snapshots, policy version pinning, durable history, RBAC, audit logging, and independently governed exception handling.
