# Severity Escalation Node

Input only a validated primitive, demonstrated attacker post-state, compatible
target surfaces, program policy, and safe execution limits.

Do not argue from labels. Search for a capability-continuous edge to the next
impact tier:

```text
CURRENT_PROVEN_SEVERITY=
POST_STATE_CAPABILITIES=
NEWLY_REACHABLE_SURFACES=
NEXT_EDGE_REQUIREMENT=
MATCH_PROOF=
SAFE_TEST=
FALSIFIER=
RESULT=<PROVEN|FALSIFIED|BLOCKED>
```

If no higher-impact edge survives, return the exact exhausted axes and the
appropriate lock reason. Never convert blocked or hypothetical impact into a
higher severity.
