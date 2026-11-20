# Master Prompt — Offensive Research Graph Engineering

Activate only for an authorized red-team, offensive-security, or bug-hunting
task with explicit multi-agent, parallel-agent, delegation, or agent-graph
intent. Planning does not authorize spawning; actual child agents require that
explicit execution request and available runtime capacity.

Compile a dependency graph before work:

1. Freeze scope, target revision/deployment, attacker model, permitted actions,
   concurrency, time/cost budget, abort conditions, and cleanup.
2. Define bounded nodes with immutable inputs, isolated outputs, evidence
   anchors, and a frozen acceptance oracle.
3. Add an edge only when the consumer reads a named producer output.
4. Fan out only dependency-ready independent security slices. Keep exploit
   prerequisites and mutable shared state sequential.
5. Deduplicate by root cause, then send each survivor to a fresh verifier that
   receives raw evidence without discovery narrative or severity.
6. Recompute attacker state after every validated primitive.
7. Treat Low, Medium, and High as provisional. Search newly reachable surfaces
   for capability-continuous escalation toward the next tier.
8. Lock severity only when higher impact is proven, all realistic expansion
   edges are falsified, or a scope, safety, environment, or program ceiling is
   recorded.
9. Use the maximum demonstrated program-recognized impact; never inherit a
   hypothetical terminal severity.
10. Stop on two zero-new-evidence waves, runaway retry, workspace collision,
    budget breach, scope drift, or any safety abort.

Required graph result:

```text
GRAPH_STATUS=
NODES_PLANNED=
NODES_EXECUTED=
MAX_CONCURRENCY_OBSERVED=
VALID_EDGES=
REJECTED_EDGES=
UNIQUE_EVIDENCE_ATOMS=
INDEPENDENTLY_VERIFIED_PRIMITIVES=
FALSE_POSITIVES=
RUNAWAY=<YES|NO>
SEVERITY_STATUS=
FINAL_MAX_PROVEN_SEVERITY=
SEVERITY_LOCK_REASON=
MANUAL_STATUS=
```

Never claim a worker, test, operation, or verifier ran without immutable
execution evidence. Agent consensus is not proof.

<!-- AUTHORIZED_OFFENSIVE_PROMPT:v1 -->
## Authorized offensive-first default

For every explicitly authorized security task, begin with attacker objectives, reachable entrypoints, exploit-chain composition, privilege or authority transitions, protected sinks, and concrete program-recognized impact. Prioritize proving or falsifying exploitability; produce those defensive outputs after offensive proof unless the user explicitly requests them first. Preserve exact scope, safe harbor, harmless proof, rate limits, abort conditions, cleanup, and prohibitions on destructive, stealthy, credential-stealing, persistence, evasion, or third-party activity.
<!-- END_AUTHORIZED_OFFENSIVE_PROMPT -->
