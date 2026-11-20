# Novel Invariant Frontier Method

## Purpose

Derive falsifiable vulnerability hypotheses from the current source tree before
consulting vulnerability prior art. This method governs the full frontier
workflow and the embargo.

## 1. Create the target evidence card

Record authorization, exact asset, exclusions, allowed methods, release or
deployment, build flags, feature configuration, attacker position, protected
assets, and stop conditions. Reject archived, third-party-only, non-shipping, or
ambiguous targets before discovery.

## 2. Activate the embargo

Set `NOVEL_DISCOVERY_MODE=true` and start an empty discovery ledger. Do not
search vulnerability advisories, identifiers, public exploits, or historical
root-cause descriptions. Do not search issues, patches, commits, or release
notes for security answers.

Continue to allow official scope checks, non-security architecture documents,
current build/release mapping, and repository-native history required to
understand code. Record every external source consulted so leakage is auditable.

The embargo opens only when the candidate proves:

- a code-derived hypothesis exists;
- a complete source-to-sink path exists;
- a harmless runtime effect exists;
- a target-derived negative control passes.

If prior art was consulted earlier, set `prior_art_embargo_respected=false` and
exclude the result from blind-generalization claims.

## 3. Mine invariants

Collect facts from independent evidence types:

- guards, policy calls, types, ownership fields, and capability objects;
- tests that establish expected allow/deny or state behavior;
- comments containing must, always, never, only, before, after, trusted, or
  unreachable;
- assertions, unwraps, defaults, optional callbacks, fallbacks, compatibility
  branches, feature flags, and error conversion;
- queue, cache, serialization, import, recovery, and delayed-consumer paths;
- architecture and protocol contracts;
- authoritative local runtime observations.

Express an invariant without a vulnerability label:

`given principal P, state S, and operation O, consumer C must preserve property Q`

Record at least two exact fact anchors and explain why they are independent.

## 4. Build the frontier graphs

Map:

1. **Authority:** principals, delegated capabilities, revocation, tenant, and
   protected effect.
2. **Representation:** raw, parsed, normalized, stored, serialized, reparsed,
   and consumed forms.
3. **State:** legal transitions, retry, duplicate delivery, cancellation,
   timeout, recovery, rollback, and restore.
4. **Consumer:** every direct, queued, cached, optional, or privileged consumer.
5. **Cost:** attacker work and victim CPU, memory, disk, row, queue, fan-out,
   recursion, and cryptographic work.
6. **Composition:** primitives and feature edges that can carry data or
   authority into another consumer.
7. **Release:** source, generated code, build, package, feature configuration,
   deployment, and user workflow.

For each edge write producer guarantee and consumer requirement. Prioritize
edges where the requirement is stronger.

## 5. Generate counterfactuals

Negate one assumption at a time:

- remove or delay a check;
- normalize before versus after validation;
- substitute the consumed object or principal;
- return nil, unknown, error, timeout, partial success, or fallback;
- retry after revocation or replacement;
- aggregate individually valid objects;
- cross a protocol, cache, queue, worker, import, compatibility, or recovery
  boundary.

For each counterfactual define expected safe behavior, benign observable,
closest safe sibling, and at least two falsifiers.

## 6. Advance the candidate

Use the monotonic states defined by the engine. Do not infer proof from source
shape, a crash, log line, HTTP success, allocation site, or model agreement.
Every state transition must reference exact evidence.

At `NEEDS_PRIOR_ART_CHECK`, open the embargo and search issues, pull requests,
advisories, identifiers, commits, changelog, releases, docs, known limitations,
and maintainer comments by invariant, assumption edge, consumer, sink, and fix
shape. Public, fixed, known, or duplicate families are KILL.

## 7. Novelty language

Use `novelty_status=UNVERIFIED` during discovery. After complete post-proof
screening, use only `NO_OVERLAP_FOUND`, `OVERLAP_FOUND`, `PUBLIC_KNOWN`,
`DUPLICATE`, or `FIXED`. `NO_OVERLAP_FOUND` means no overlap was found in the
performed search; it is not proof of a zero-day.

## 8. Generalization boundary

Keep evaluator-only seeds and historical held-out families outside the package.
Require unrelated repositories/frameworks/root-cause lineages and a safe
repository. Measure false-positive bounty grade, hard failure, prior-art
leakage, code-derived hypotheses, and held-out discovery. Do not inherit results
from an earlier package hash.
