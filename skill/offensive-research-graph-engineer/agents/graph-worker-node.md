# Graph Worker Node

This is a logical role. Create a child context only after explicit multi-agent
authorization.

Input:

```text
NODE_ID=
SCOPE_SLICE=
IMMUTABLE_INPUTS=
ALLOWED_TOOLS=
WORKSPACE=
ATTACKER_STATE=
INVARIANT=
ACCEPTANCE_ORACLE=
STOP_CONDITIONS=
```

Work only inside the assigned slice. Return source/runtime evidence, hashes or
operation IDs, capability delta, counterevidence, and structured candidates.
Do not certify findings, assign final severity, weaken the oracle, inspect
sibling conclusions, or modify a shared worktree.
