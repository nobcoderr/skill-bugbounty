---
name: hunt-severity-climb
description: "Offensive severity climb. A valid Low, Medium, or High is a foothold. Chain the same attacker state toward Critical, then lock the maximum proven tier. Use automatically on every validated primitive."
---

# Hunt severity climb

Authorized offensive-first. The first hit is a foothold. From that
post-state, take every newly reachable surface: secret read, token,
cross-tenant write, SSRF to metadata, RCE, admin. Climb until a
terminal impact is proven or every expanding edge is dead.

Read `/home/kali/skill/references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md`.
Spawn `exploit-chain-research-orchestrator/agents/severity-escalation-agent.md`.
Failed edge: `adaptive-plan-check-loop`, then a new technique.

`REPORT_READY` stays `NO` until `SEVERITY_LOCKED=YES`. Critical is the
search direction. Keep the highest tier you actually proved.

## Limits

Owned-account canaries. No credential theft of third parties, no
persistence, no DoS, no mainnet fund movement that is not yours.
Hypothetical chains do not raise the label.
