---
name: hunt-severity-climb
description: "When a bug is valid at Low, Medium, or High, do not submit and do not stop. Climb the same attacker state toward Critical, then lock the maximum proven tier. Use automatically on every validated candidate during bug bounty."
---

# Hunt severity climb

A valid Low, Medium, or High is a floor. It is not a submission and not a
reason to stop.

Read `/home/kali/skill/references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md`
and spawn `exploit-chain-research-orchestrator/agents/severity-escalation-agent.md`.
Use `adaptive-plan-check-loop` when an edge fails: retry with a different
technique, then a different target-native edge.

## Rules

- Freeze the direct proof before chaining.
- Test only surfaces the new capability actually unlocks.
- Harmless owned-account canaries only. No credential theft, third-party
  data, persistence, DoS, or mainnet fund movement.
- Critical is a search direction, not a required outcome.
- Hypothetical, blocked, or unsafe edges do not raise the label.

Keep `REPORT_READY=NO` while `SEVERITY_LOCKED=NO`. After lock, keep the
maximum proven tier even if it stays Low, Medium, or High. Only then may
the parent run `security-review`.
