# Assessment and Remediation Methodology

## 1. Establish scope
Define providers, accounts/subscriptions/projects, business criticality, expected logging, ownership and approved control baseline. This lab uses fictional scope only.

## 2. Normalize evidence
Translate provider-specific posture evidence into a common schema. Reject incomplete or ambiguous records rather than silently defaulting security-significant fields.

## 3. Evaluate impact and exploitability context
Prioritize findings using severity plus contextual factors: public reachability, privileged identity impact, critical workload placement, exploited-vulnerability context, telemetry gaps and overdue remediation. Context improves triage but does not claim exploitability.

## 4. Map defensive threat context
Use ATT&CK only where the cloud weakness plausibly supports an adversary behavior. The mapping communicates security relevance; it is not incident attribution.

## 5. Remediate at the authoritative source
Correct IAM policy, network policy, logging configuration, key/secrets handling, storage exposure, or workload configuration through controlled engineering changes. Avoid console-only drift when infrastructure is managed as code.

## 6. Validate effectiveness
A closure record should contain an accountable owner, change reference, post-change state, validation method and validation result. Re-run the control evaluation after the change. An ineffective validation is an invalid closure.

## 7. Report residual risk
Report open, accepted, pending-validation and validated states separately. Track control-family and provider concentration rather than using only total counts.

## Limitations
The synthetic scoring model is intentionally transparent rather than statistically predictive. Production prioritization should incorporate authoritative business context, provider-native configuration semantics, attack-path reachability and current threat intelligence under governance.
