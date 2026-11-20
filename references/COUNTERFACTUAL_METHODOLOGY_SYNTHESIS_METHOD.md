# Counterfactual Methodology Synthesis Method

`COUNTERFACTUAL_METHODOLOGY_SYNTHESIS:v1`

## Purpose

This method creates a materially different way to interrogate an authorized
target after a bounded campaign has honestly ended in `NO VALID FINDING`. It is
not a promise that another vulnerability exists. Its purpose is to escape a
locally exhausted search strategy without recycling its payloads, desired bug
class, or unsupported impact.

Activate only when the prior campaign is closed, the target remains explicitly
authorized and current, and at least one target-native semantic or architectural
axis remains unexplored. Missing authorization, an excluded impact class, a
non-production-only target, or an exhausted budget remains a stop condition.

## 1. Freeze the exhausted method

Create a `prior_method_exclusion_digest` containing:

- inspected entrypoints, consumers, sinks, and state transitions;
- payload and representation families already tried;
- assumptions and protected invariants already tested;
- negative controls and falsifiers already executed;
- KILL, BLOCKED, duplicate, by-design, and reachability decisions; and
- the exact evidence that produced `NO VALID FINDING`.

The digest is a negative constraint. Do not treat the previous expected bug
class or payload vocabulary as inspiration for the new method.

## 2. Build a target fact deck

Record atomic facts from current source, tests, types, runtime, documentation,
release artifacts, and architecture. Each fact has a source anchor and one of:

- actor or authority;
- object ownership or identity;
- representation or normalization stage;
- state phase, order, rollback, retry, or revocation epoch;
- lifetime, cache, lease, or persistence boundary;
- direct, queued, worker, proxy, compatibility, or recovery topology;
- single, batch, aggregate, partial, or empty cardinality;
- primary, secondary, delayed, or privileged consumer;
- error, nil, default, fallback, rollback, or recovery semantics; or
- composition edge between independently reachable features.

Every new method must cite at least two facts. Generic vulnerability knowledge
does not satisfy this requirement.

## 3. Generate counterfactual operators

Use the grammar:

`What if A becomes B while protected invariant P should remain true?`

Useful target-native operators include:

1. `ACTOR_SUBSTITUTION`: owner to peer, user to worker, caller to callback.
2. `OWNERSHIP_REBIND`: stable ID to alias, parent to child, resource to clone.
3. `REPRESENTATION_SHIFT`: raw to canonical, signed to decoded, path to object.
4. `ORDER_INVERSION`: validate then mutate to mutate then consume.
5. `LIFETIME_EXTENSION`: request to retry, issuance to revocation, cache to epoch.
6. `TOPOLOGY_SUBSTITUTION`: direct to queue, proxy, compatibility, or recovery.
7. `CARDINALITY_SHIFT`: one to batch, aggregate, partial success, or empty set.
8. `CONSUMER_SUBSTITUTION`: safe display to privileged parser, worker, or sink.
9. `FAILURE_SEMANTICS`: reject to fallback, partial commit, retry, or fail-open.
10. `FEATURE_COMPOSITION`: harmless primitive A to separately reachable B.

Prefer one architecture-level change or two material semantic axes. Change only
one variable in the eventual experiment, but the method itself must differ from
the exhausted search in what relation it measures.

## 4. Independence and distance check

Classify as `MUTATION_ONLY` when the proposal changes only payload spelling,
filename, endpoint alias, encoding decoration, numeric constant, vulnerability
label, or test harness while preserving the same actor, consumer, invariant,
oracle, and falsifier.

A method is materially independent only when it:

- changes an architecture-level relation, or at least two semantic axes;
- introduces a new authoritative consumer, oracle, or decisive falsifier;
- has target-native fact anchors not used merely as synonyms; and
- can fail for a reason distinct from the previous method.

Known/public pattern replay is not methodological novelty. Use prior art as a
duplicate and overfitting falsifier after the proof gate, not as a payload seed.

## 5. Method card

Each method card contains:

| Field | Required content |
|---|---|
| `method_id` / `parent_method_id` | Unique identity and exhausted parent |
| `fact_anchors` | At least two exact target-native anchors |
| `changed_axes` | Material semantic or architecture axes |
| `protected_invariant` | One falsifiable security statement |
| `counterfactual_question` | Explicit A to B question |
| `attacker_variable` | What the authorized attacker controls |
| `authority_consumer` | Component making the security decision/effect |
| `oracle` | Deterministic, authoritative pass/fail observation |
| `baseline` | Normal case under identical authority |
| `safe_sibling` | Closest one-variable non-triggering case |
| `negative_control` | Case proving the harness is not the effect |
| `falsifier` | Cheapest decisive reason to kill the method |
| `release_reachability` | Current shipped/production path evidence |
| `impact_plan` | Capability delta and program-recognized boundary |
| `safety` | Harmless proof, owned data, scope, cleanup |
| `stop_condition` | Fixed request/time/attempt limit and abort trigger |
| `independence_explanation` | Why this is not method or payload churn |

## 6. Bounded two-cycle procedure

For each post-no-finding cycle:

1. Refresh scope, release, exclusions, and the fact deck.
2. Generate at most three method cards across different operators.
3. Reject `PATTERN_REPLAY`, `MUTATION_ONLY`, and cards missing proof design.
4. Rank survivors by distance from the exhausted method, impact plausibility,
   current reachability, and cheapest harmless falsifier.
5. Evaluate only the highest-value authorized card first.
6. Record every result without inheriting proof between methods.
7. Reroute if a new actor, representation, consumer, topology, or impact fact
   appears.

Run no more than two post-`NO VALID FINDING` cycles and no more than three cards
per cycle. Do not invent a third cycle merely to avoid an honest stop.

## 7. Evaluation states

- `DEFERRED_CURRENT_METHOD_ACTIVE`: prior methodology still has live candidates.
- `METHOD_READY_FOR_SAFE_EVALUATION`: complete, independent method card.
- `METHOD_REJECTED`: missing target facts, oracle, controls, or falsifier.
- `MUTATION_ONLY`: cosmetic change to the exhausted method.
- `BLOCKED_BY_SCOPE`: target or proposed proof is not currently authorized.
- `METHOD_GENERATED_NO_VALID_FINDING`: the new method was tested and falsified.
- `NO_MATERIAL_NEW_METHODOLOGY`: no independent method survived synthesis.
- `STOP_BUDGET_EXHAUSTED`: the two-cycle limit has been reached.
- `VALID_FINDING_GENERATED`: a method produced a candidate that passed every
  ordinary finding gate, including `STRONG + MANUALLY_CONFIRMED`.

## 8. Valid-finding gate

`VALID_FINDING_GENERATED` requires all of:

- attacker control and complete source-to-sink trace;
- harmless runtime invariant violation;
- baseline, safe sibling, and negative control;
- harness-independent reproduction;
- authoritative state or effect read-back;
- current shipped or production reachability;
- nonzero program-recognized capability delta;
- prior-art and duplicate clearance; and
- manual confirmation.

If any item is missing, preserve the exact missing proof and do not claim that
the methodology found a valid vulnerability.

## 9. Safety and interpretation

Method synthesis is read-only design work. It never authorizes live recon,
scanning, fuzzing, state-changing requests, exploit execution, destructive
proof, credential access, stealth, persistence, or third-party targeting.

Regression cases demonstrate only that the decision rules reject obvious false
novelty and preserve evidence gates. They do not prove generalization, zero-day
discovery ability, or that every eligible target contains a vulnerability.

