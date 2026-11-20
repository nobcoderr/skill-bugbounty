---
name: hunt-orchestrator
description: "Coordinate parallel bug-bounty specialists, collect their results, and evaluate them. Spawn reentrancy, logic, class, and validator agents without being asked. Use during an authorized hunt after hunt-director assigns lanes. Skip ordinary coding."
---

# Hunt orchestrator

Run the director's lanes. One specialist, one question. The parent still
owns scope, severity lock, and `REPORT_READY`.

Do not wait for the user to name this skill, an agent, or a class.

## Spawn without being asked

Use Cursor `Task` with `generalPurpose` and `run_in_background` false
unless the parent asked for background. Give each child the exact host,
scope, question, and kill observation. Do not give it `REPORT_READY`.

Default parallel set when those surfaces exist:

- `hunt-reentrancy/agents/reentrancy-hunter.md`
- `hunt-logic-vulnerability/agents/logic-hunter.md`
- one `vuln-variant-coverage/agents/variant-hypothesis-tester.md` card
  per other reachable class
- `finding-validator/agents/finding-validator.md` for each survivor

If a step fails, follow `adaptive-plan-check-loop`: diagnose, then retry
with a materially different technique. Do not repeat the same request.

If a needed skill or agent is missing, follow
`capability-gap-skill-builder` once, then continue the original lane.

## Evaluate

For each child return, keep only evidence that names attacker condition,
server condition, and a protected effect. Mark the rest `KILLED`.

A valid Low, Medium, or High is not finished. Hand it to
`hunt-severity-climb` before any submit-or-stop decision.

## Output

```text
WAVE=
SPAWNED=
SURVIVORS=
KILLED=
BLOCKED=
RETRY_WAVES=
ESCALATION_HANDOFF=
```
