---
name: finding-validator
description: "Independently validate a bug-bounty candidate and try to kill it. Use automatically after a specialist returns PROMISING or PRIMITIVE_VALID. Do not submit, do not raise severity, and do not discover a new class. Skip ordinary coding."
---

# Finding validator

Fresh-context KILL pass. Discovery prose is not evidence.

## Kill unless all are true

- exact in-scope host or artifact on the current release
- attacker condition, server condition, protected effect
- baseline, one-variable negative control, authoritative read-back
- cleanup and researcher-owned data only
- not by-design, N/A, informative, or duplicate-only

If any item fails, return `KILLED` with the failed gate. Do not repair
the hypothesis. Do not chain.

A surviving candidate is `PRIMITIVE_VALID` only. Hand it to
`hunt-severity-climb`. Do not set `REPORT_READY`. Do not set
`SEVERITY_LOCKED`.
