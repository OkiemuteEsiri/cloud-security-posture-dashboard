# Cloud Control Validation Matrix

This matrix separates **technical exposure**, **remediation action**, and **closure evidence** so that a ticket state or approved exception is not mistaken for removal of the underlying security condition.

| Control family | Representative risk condition | Security impact | Required remediation evidence | Revalidation condition | ATT&CK context |
|---|---|---|---|---|---|
| Identity & access | Excessive privilege or weak privileged-account governance | Unauthorized access can have a larger blast radius | Approved identity change, accountable owner, affected principal/resource, post-change privilege state | Effective privilege is reduced to the intended least-privilege state | T1078 Valid Accounts |
| Public exposure | Sensitive service or workload unintentionally internet reachable | Increased attack surface and remote exploitation opportunity | Network/resource configuration change and intended exposure statement | Resource is no longer publicly reachable unless exposure is explicitly required and controlled | T1190 Exploit Public-Facing Application |
| Secrets management | Secret material stored or exposed outside approved controls | Credential disclosure can enable unauthorized access | Secret rotation/revocation evidence and migration to approved storage | Previous secret is invalid and the workload uses the approved secret-management path | T1552 Unsecured Credentials |
| Logging / monitoring | Security-relevant activity is not captured or centrally available | Reduced ability to detect, investigate, and validate security events | Logging configuration change, destination evidence, and retention/coverage statement | Expected synthetic or approved validation event is observable in the intended telemetry path | T1562 Impair Defenses |
| Network segmentation | Unnecessary trust path between security zones or workloads | Compromise can traverse beyond the intended boundary | Rule/policy change with source, destination, protocol, owner, and business requirement | Previously unnecessary path is blocked while required connectivity remains functional | T1040 Network Sniffing (context where visibility/exposure is relevant) |
| Encryption | Sensitive data or transport lacks required protection | Confidentiality and integrity controls may be weakened | Encryption setting/key configuration change and scope evidence | Resource reports the required encryption state and permitted workloads remain functional | Defensive control context; no attack claim implied |
| Workload security | High-risk configuration weakens workload isolation or runtime protection | Increased compromise impact or control bypass opportunity | Configuration/policy change plus owner and affected workload evidence | Weak condition is absent and required workload behavior is preserved | Technique mapping depends on the specific finding |
| Configuration governance | Required preventive policy is missing, disabled, or bypassed | Misconfiguration can recur or spread across environments | Policy-as-code/guardrail change and ownership evidence | New noncompliant synthetic fixture is rejected or flagged by the preventive/detective control | Technique mapping depends on the governed control |

## Evidence quality levels

**Level 0 — Administrative only**  
Ticket marked complete, verbal confirmation, or change reference without technical evidence. This is insufficient for closure.

**Level 1 — Implementation evidence**  
A configuration or control change is documented, but effectiveness has not yet been independently checked. The finding remains pending validation.

**Level 2 — Technical validation**  
Post-change evidence demonstrates that the original risk condition is removed or reduced as intended. This is the minimum technical state for normal closure.

**Level 3 — Sustainable control validation**  
The technical fix is validated and a preventive/detective mechanism demonstrates that equivalent drift can be detected or prevented. This is the preferred state for recurring or systemic findings.

## Exception handling

An approved risk exception changes the **governance state**, not the technical exposure state. Exceptions should have an owner, rationale, approval reference, compensating controls where applicable, and an expiry/review date. Expired exceptions must not be treated as active closure evidence.

## Revalidation principles

- Validate against the original risk condition, not merely the implementation ticket.
- Preserve sufficient evidence to explain who changed what, why, and how effectiveness was checked.
- Re-test the narrow control without introducing unsafe production targeting.
- Use synthetic fixtures in this repository; provider APIs and real cloud credentials are intentionally out of scope.
- Re-open or retain the finding when validation is incomplete, contradictory, or shows the risk condition remains.
