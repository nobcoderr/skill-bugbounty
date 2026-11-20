# Derived-Metadata Equivalence Variant Method

## Purpose

Find current Chromium/V8 bugs where an optimizer, parser, cache, or recovery
pipeline collapses states that are operationally different. The seed is a
public fixed root; success requires a new exact root and current release proof.

## Root card

Freeze these fields before searching siblings:

```text
PUBLIC_ROOT=
VULNERABLE_REVISION=
FIXED_REVISION=
INTRODUCING_REVISION=
COMPARED_OBJECT=
DERIVED_OR_EXTERNAL_FACT=
OMITTED_IDENTITY_FACT=
EQUIVALENCE_MECHANISM=
PROTECTED_CONSUMER=
INVALIDATION_OR_DEOPT_EVENT=
WRONG_INTERPRETATION=
SECURITY_CONSEQUENCE=
FIX_REQUIREMENT=
```

For CVE-2026-6307, the historical root is the omitted JS-to-Wasm signature in
frame-state equality. The V8 fix explicitly adds the signature comparison and
prevents base-class copying. Any same-root recurrence is prior art, not novelty.

## Completeness inventory

For the relevant object or metadata family, inventory:

- base fields, derived fields, side tables, tagged unions, discriminators, and
  feature-dependent fields;
- `operator==`, `Equals`, hash functions, cache/interner keys, set/map
  comparators, canonicalization, serialization, cloning, copying, slicing,
  zone allocation, and invalidation;
- all constructors and factories that can create the compared state;
- all consumers that trust the equivalence decision.

Build this matrix:

| State fact | Stored where | Equality | Hash/key | Copy/clone | Consumer | Security meaning |
|---|---|---|---|---|---|---|
| type/discriminator | base/derived/side table | yes/no | yes/no | preserved/lost | pass | reconstruction branch |
| representation | ... | ... | ... | ... | ... | tagged vs unboxed |
| signature/schema | ... | ... | ... | ... | ... | ABI/materialization |
| effect/lifetime | ... | ... | ... | ... | ... | reordering/invalidation |

Do not infer a flaw solely because the hash omits a field. Prove that the full
equality/key path also accepts two states that the protected consumer must
distinguish.

## Differential pair

Construct two states `A` and `B` such that:

```text
base_identity(A) == base_identity(B)
security_fact(A) != security_fact(B)
equivalence(A, B) == true
consumer(A) != consumer(B)
```

Hold everything except the candidate field constant. Record a safe sibling in
which either the field matches or the states remain distinct. The first oracle
should be a wrong value, wrong type, stale metadata, incorrect node replacement,
or trace-visible merge—not a weaponized payload.

## Search order

1. The exact patched abstraction: neighboring derived types and feature gates.
2. Other identity operations on the same type: hash, cache key, copy, clone,
   serialization, interning, and invalidation.
3. Call sites constructing the same metadata through alternate factories.
4. Equivalent recovery metadata in Maglev, TurboFan, Turboshaft, Wasm, builtins,
   inline caches, and parser lazy-reparse state.
5. Cross-tier handoffs where one tier records richer facts than the next.
6. Architecture- or configuration-specific fields that alter ABI,
   representation, register class, pointer width, or sandbox interpretation.

## Consumer proof

Trace all five edges:

```text
attacker-controlled program shape
 -> two distinct internal states
 -> incorrect equality/key/cache decision
 -> protected optimizer/parser/recovery consumer
 -> observable divergence
```

For compiler metadata, separately prove:

- both states coexist in one compilation or cache domain;
- the relevant pass can compare or reuse them;
- one state actually replaces or aliases the other;
- the retained metadata survives lowering/code generation;
- a reachable event consumes it after assumptions change.

## Falsifiers

Kill the lane when any of these holds:

- a type discriminator, unique identity, or complete equality check distinguishes
  the states before reuse;
- the omitted field cannot affect the consumer;
- downstream code recomputes or validates the fact authoritatively;
- the state pair cannot coexist in the same optimization/cache domain;
- the only effect requires target modification, a debug-only intrinsic, an
  experimental V8 flag, Canary/trunk churn, or a non-shipped configuration;
- current source already contains the effective guard;
- public material describes the same primitive and fix requirement;
- the runtime outcome is only an expected CHECK, DCHECK, safe deopt, or zero
  capability delta.

## Proof ladder

Advance one stage at a time:

1. `SOURCE_IDENTITY_GAP`
2. `REACHABLE_STATE_PAIR`
3. `TRACE_CONFIRMED_REUSE`
4. `BENIGN_WRONG_VALUE_OR_TYPE`
5. `MEMORY_SAFETY_SIGNAL` with symbolized evidence
6. `CURRENT_RELEASE_REPRODUCTION`
7. `PROGRAM_IMPACT_DELTA`
8. `STRONG + MANUALLY_CONFIRMED`

Stop at the first unproven edge. A historical vulnerable build is suitable for
learning and regression, but cannot satisfy stages 6-8.

## Variant ledger

For every lane record:

```text
VARIANT_ID=
SOURCE_REVISION=
ROOT_DIFFERENCE_FROM_PUBLIC_SEED=
STATE_A=
STATE_B=
EQUIVALENCE_SITE=
CONSUMER=
ORACLE=
NEGATIVE_CONTROL=
PATCHED_CONTROL=
FLAGS_AND_FEATURE_STATE=
CHROME_RELEASE_REACHABILITY=
PRIOR_ART_RESULT=
CAPABILITY_DELTA=
MANUAL_REPRODUCTION=
VERDICT=
FALSIFIER_OR_NEXT_PROOF=
```

Deduplicate by semantic root, not filename, payload, compiler tier, or crash
address.
