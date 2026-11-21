---
name: hunt-director
description: "Offensive hunt director. Name attacker position, high-impact lanes, and which specialist fires first. Use automatically on bug bounty. Critical and chainable primitives first."
---

# Hunt director

Authorized offensive-first. Point the swarm at the highest-impact
reachable attacks. `hunt-orchestrator` fires the lanes. The parent owns
`REPORT_READY`.

## Order

Critical first: RCE, auth bypass, ATO, IDOR cross-tenant, SSRF to
cloud metadata, reentrancy with asset movement, then high, medium, low.

Open without being asked: `valid-bug-hunt`, `target-system-model`,
`hunt-scope-exhaustion`, `hunt-orchestrator`, `corpus-writeup-transfer`,
`nobcoder-writeup-transfer`, `payload-forge`, `payloadsallthethings`,
`adaptive-plan-check-loop`.
Use `oss-scanner` when the asset is GitHub source.

## Lanes

Each lane is an attack question: entry, privilege change, protected
effect.

- `hunt-reentrancy` on callbacks, hooks, external calls, contracts
- `hunt-logic-vulnerability` on money, entitlement, state machines
- every other reachable `hunt-*` class
- `corpus-writeup-transfer` to land paid writeup methods on this target
- `nobcoder-writeup-transfer` to land methods from `github.com/nobcoderr/writeup`
- `hunt-scope-exhaustion` so one empty asset never ends the hunt
- `payload-forge` to create and mutate bypass/SQL/XSS/SSTI payloads
- `payloadsallthethings` to land swisskyrepo methods on this host
- `oss-scanner` on GitHub/OSS assets
- `finding-validator` then `hunt-severity-climb` on survivors

Load a class only after the surface exists. If a specialist is missing,
build it with `capability-gap-skill-builder` and keep attacking.

```text
PROGRAM=
SCOPE=
ATTACKER_POSITION=
OBJECTIVE=
LANES=
NEXT_ORCHESTRATOR_WAVE=
```
