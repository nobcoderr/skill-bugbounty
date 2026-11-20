---
name: hunt-director
description: "Direct an authorized bug-bounty hunt. Assign one falsifiable lane per specialist, keep scope, and refuse REPORT_READY. Use as soon as the task is bug bounty, a named program, or an in-scope hunt. Do not wait to be named. Skip ordinary coding."
---

# Hunt director

The director does not hunt. It names the in-scope system, the attacker
position, and the lanes. `hunt-orchestrator` runs those lanes. The parent
owns `REPORT_READY`.

Do not wait for the user to say director, pengarah, or orchestrator. If
the task is ordinary coding, leave this skill unused.

## Open without being asked

1. `valid-bug-hunt`
2. `target-system-model`
3. `hunt-orchestrator`
4. `adaptive-plan-check-loop`
5. `capability-gap-skill-builder` when a needed skill is missing
6. `hunt-severity-climb` as soon as any candidate is technically valid

## Assign lanes

Give each specialist one independent question: entry, protected effect,
and the observation that kills it. Default swarm when the surface exists:

- `hunt-reentrancy` for callbacks, tokens with hooks, external calls, or
  contracts
- `hunt-logic-vulnerability` for workflows, money, entitlement, or state
  machines
- class `hunt-*` skills for every other reachable class
- `finding-validator` for every surviving candidate
- `security-review` only after `SEVERITY_LOCKED=YES`

Do not load every `hunt-*` body before the surface exists. A class the
system cannot reach stays unused. If the needed specialist is absent,
follow `capability-gap-skill-builder` once, then resume.

## Output

```text
PROGRAM=
SCOPE=
ATTACKER_POSITION=
LANES=
DEFERRED=
NOT_APPLICABLE=
MISSING_SKILL=
NEXT_ORCHESTRATOR_WAVE=
```

Do not test. Do not submit. Do not raise or lock severity.
