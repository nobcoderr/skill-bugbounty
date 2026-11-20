# Severity Escalation and Lock Method

The first demonstrated impact sets a provisional floor, not the final severity.
The objective is to find the maximum proven severity and evidence-backed impact available from the
same attacker state and authorized environment without inflating hypothetical
chains.

## Ladder

For a validated candidate:

1. Record direct primitive severity and program impact independently.
2. Compute the exact post-exploit capability delta.
3. Enumerate protected surfaces newly reachable because of that delta.
4. For each surface, state the prerequisite for the next primitive.
5. Test only edges where the post-state satisfies that prerequisite.
6. Prove identity, environment, privilege, and state continuity.
7. Re-run the program-impact gate on every demonstrated higher-impact state.
8. Repeat toward the next tier until a lock condition is met.

Use the ordinary program's severity taxonomy. `Low -> Medium -> High ->
Critical` is a search order, not an entitlement to promotion; a direct jump is
valid only when its full chain is proven.

## Escalation axes

Prioritize target-native transitions such as:

- metadata or enumeration -> protected data read;
- limited read -> secret, token, address, or pointer disclosure;
- limited write -> trusted metadata, executable path, policy, or identity
  control;
- object access -> cross-tenant action or impersonation;
- renderer/process execution -> sandbox or process-boundary escape;
- memory primitive -> controlled read/write -> boundary escape;
- SSRF -> metadata/workload identity -> protected cloud action;
- workflow/plugin/config influence -> privileged loader or execution consumer;
- availability primitive -> realistic sustained service or financial impact.

These are search dimensions only. Each edge needs target-specific evidence.

## Lock conditions

Set `SEVERITY_LOCKED=YES` only with one of:

- `LOCK_TERMINAL_IMPACT_PROVEN`: the highest permitted target-native state was
  demonstrated safely;
- `LOCK_NO_CAPABILITY_EXPANDING_EDGE`: every realistic newly reachable surface
  was tested or falsified with recorded evidence;
- `LOCK_PROGRAM_CEILING`: the program cannot recognize a higher tier for the
  asset or impact;
- `LOCK_SCOPE_OR_SAFETY_BOUNDARY`: the next proof is prohibited or would exceed
  minimum harmless validation;
- `LOCK_ENVIRONMENT_BLOCKED`: decisive production/runtime evidence is
  unavailable; lock the maximum proven tier and preserve the blocked edge.

No lock is allowed merely because the current label “looks right,” time was
spent, several agents agree, or a hypothetical Critical narrative exists.

## Required output

```text
INITIAL_SEVERITY=
CURRENT_MAX_PROVEN_SEVERITY=
SEVERITY_STATUS=<PROVISIONAL|ESCALATION_ACTIVE|LOCKED>
POST_STATE_CAPABILITIES=
NEWLY_REACHABLE_SURFACES=
ESCALATION_EDGES_TESTED=
HIGHER_EDGES_PROVEN=
HIGHER_EDGES_FALSIFIED=
HIGHER_EDGES_BLOCKED=
PROGRAM_IMPACT_GATE=
SEVERITY_LOCKED=<YES|NO>
SEVERITY_LOCK_REASON=
FINAL_MAX_PROVEN_SEVERITY=
```

Severity may be lowered when controls falsify impact. It may be raised only by
demonstrated protected effect and authoritative read-back.
