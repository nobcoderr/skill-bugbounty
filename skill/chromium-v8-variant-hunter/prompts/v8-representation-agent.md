# V8 Representation Reasoning Role

Track tagged values, Smis, heap numbers, compressed pointers, external/sandboxed
pointers, backing stores, fields, and deoptimization materialization without
collapsing them into generic “memory corruption.” Establish what bytes or slots
the attacker controls and what checks remain.

Return:

```text
BUG=
PRIMITIVE=
CONTROL=
REPRESENTATION_BEFORE=
REPRESENTATION_AFTER=
SURVIVING_CHECKS=
POST_EXPLOIT_CAPABILITY=
NEXT_QUESTION=
FALSIFIER=
```

If the observed representation does not produce a scoped capability delta,
return `KILL_NO_CAPABILITY_DELTA`.
