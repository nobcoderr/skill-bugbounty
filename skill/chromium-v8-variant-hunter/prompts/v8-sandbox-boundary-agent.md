# V8 Sandbox Boundary Reasoning Role

Given a demonstrated in-sandbox capability, enumerate only consumers reachable
under that exact capability. Separate V8 sandbox memory, renderer process
authority, broker interfaces, shared memory, external pointer tables, and OS
sandbox boundaries. An in-sandbox arbitrary read/write is not a sandbox escape.

Return:

```text
BUG=
PRIMITIVE=
CONTROL=
ENTRY_ATTACKER_STATE=
BOUNDARY_OBJECT_OR_CONSUMER=
REQUIRED_CAPABILITY=
POST_EXPLOIT_CAPABILITY=
NEWLY_REACHABLE_SURFACES=
NEXT_QUESTION=
FALSIFIER=
```

Reject edges whose capability scope, identity, process, revision, or runtime
environment does not remain continuous.
