# Authorization Invariant and KILL Challenge

Use this method whenever a candidate involves authentication, authorization,
tenant/object scope, a policy callback/provider, optional middleware, or a
protected operation whose target identity can come from more than one input.

## 1. State the invariant before judging intent

Write one sentence that names the protected operation and the condition that
must remain true. Examples:

- a protected handler must not become reachable merely because an
  authentication callback/provider is absent;
- the resource mutated must be the same resource that was resolved and
  authorized;
- an error, unknown decision, empty policy, or missing dependency must not be
  converted into authorization success.

Do not use `looks intentional`, a named no-op helper, optional configuration,
or a successful unit test as a substitute for this invariant.

## 2. Build the enforcement topology

Record:

1. the operation that requires protection;
2. the component responsible for enforcing it;
3. who supplies or initializes that component;
4. every defaulting/fallback wrapper between configuration and enforcement;
5. the final handler/query/mutation reached after the decision;
6. the authoritative security-sensitive state read or changed.

Trace both directions:

`untrusted caller -> configuration/default -> auth control -> decision -> protected operation`

`protected operation <- dispatcher <- policy result <- callback/provider <- initialization`

## 3. Evaluate absence and failure semantics

Do not review only the normal configured state. Evaluate this matrix on the
real shipped path:

| Control state | Decision returned | Protected operation dispatched? | Invariant preserved? |
|---|---|---|---|
| configured and valid | | | |
| absent / omitted | | | |
| nil / null | | | |
| empty policy or empty provider set | | | |
| explicit success-returning no-op | | | |
| implicit fallback to success/no-op | | | |
| unknown / indeterminate | | | |
| error / exception / timeout | | | |

Distinguish explicit caller opt-in from implicit framework defaulting. A public
operation intentionally configured with an explicit no-op is not equivalent to
a protected operation whose omitted callback is silently replaced with a
success-returning function.

## 4. Bind authorization to the consumed resource

Inventory every security-relevant identifier and representation:

| Source | Identifier/representation | Used for resolution? | Used for authorization? | Used by sink? |
|---|---|---|---|---|
| route/path | | | | |
| query | | | | |
| form/JSON body | | | | |
| session/context | | | | |
| loaded database object | | | | |
| queue/worker payload | | | | |

If authorization uses Resource A while the sink consumes Resource B, retain a
candidate until a downstream control proves that A and B must be identical or
the cross-resource effect is impossible. CSRF, type, and action checks do not
repair a target-resource mismatch.

## 5. Mandatory KILL challenge

Before assigning `KILL` to an authentication or authorization candidate,
provide evidence for all five steps:

1. state the expected security invariant;
2. identify the enforcing component on the release-reachable path;
3. demonstrate that enforcement remains effective under absent, nil, empty,
   default, success, unknown, and error states that the API permits;
4. trace the exact protected operation end to end, including the resource
   identity authorized and the identity consumed by the sink;
5. prove either that the behavior is documented/architecturally intentional
   **and** preserves the invariant, or that no attacker-controlled privilege,
   tenant, object, confidentiality, or integrity transition is possible.

If any step is missing, do not promote the candidate and do not KILL it. Keep
it as `HYPOTHESIS / NEEDS_INVARIANT_PROOF` with the single missing evidence
question. This status is not report-ready and does not count as a finding.

`Intentional` is sufficient for KILL only when all of these are evidenced:

`documented or architecturally supported + invariant preserved + protected operation traced + no attacker-controlled authority transition`

## 6. Safe proof pattern

Use owned synthetic state and change one variable at a time:

1. configured valid-control baseline;
2. wrong credential or wrong resource negative control;
3. absent/nil/default state candidate;
4. explicit no-op safe sibling when the API supports one;
5. error/unknown state control;
6. authoritative handler/query/state read-back;
7. patched or fail-closed sibling when available;
8. cleanup and source-digest verification.

Do not infer impact from a decision value alone. Confirm whether the protected
handler or authoritative sink actually runs.

## 7. Required handoff fields

For every auth-related survivor or KILL decision, include:

- protected operation;
- enforcing component and initialization owner;
- absence/failure-state matrix;
- authorized resource identity and consumed resource identity;
- intent/documentation evidence;
- end-to-end dispatch/sink result;
- KILL blockers or complete KILL proof.

<!-- AUTHORIZATION_KILL_CHALLENGE:v1 -->
