# Thin-Slice Context Budget Method

## Objective

Keep model attention on the few facts that decide a vulnerability while
preserving enough scaffolding to prevent generic, unreachable findings.

The method does not reduce scope validation, evidence gates, prior-art rules,
or manual verification. It changes how much context is loaded at once.

## 1. Compress the threat model

Represent the current slice with:

```text
ATTACKER_START=
ATTACKER_CONTROL=
UNAVAILABLE_CAPABILITIES=
PROTECTED_PROPERTY=
TRUST_BOUNDARY=
ENTRYPOINTS=
CROWN_JEWEL_CONSUMERS=
INVARIANTS=
RELEASE=
```

This should normally fit on one page. If it becomes a catalog of every CWE,
dependency, style rule, and hypothetical threat, split it again.

## 2. Select a thin slice

A slice follows one real security boundary or enforcement mechanism, such as:

- credential privilege separation;
- algorithm/key selection;
- signature state and secret rotation;
- syscall or protocol enforcement coverage;
- parser framing and message multiplicity;
- name-to-address policy binding;
- untrusted rendering inside an authority-bearing origin;
- cache identity and authorization context.

Choose code by entrypoint and consumer reachability, not directory size alone.
Include callers, callees, shared helpers, tests, configuration, and relevant
sibling implementations even if they cross folders.

## 3. Context allocation

Use the following only as a default heuristic, not a rigid quota:

- stable scaffold: roughly 10% or less;
- focused target exploration: roughly 60–80%;
- verification and reduction: roughly 20–30%.

Adjust when the target is unusually small or verification is expensive. The
invariant is that persistent policy text must not crowd out target evidence or
verification.

The router still evaluates every installed skill. It loads detailed conditional
skill bodies only when current evidence activates them. Store registries and
evidence outside the prompt, then inject only the current slice and pointers.

## 4. Editable threat model

Update the slice only with:

- verified architecture or call-flow facts;
- source-supported invariants;
- demonstrated attacker capabilities;
- killed assumptions and their evidence;
- newly reachable consumers.

Do not add model speculation as fact. Candidate prose remains in a separate
ledger until verified.

## 5. Prior art modes

### Normal mode

Past advisories and accepted CVEs may reveal the product's historical threat
model and recurring enforcement boundaries. Use them to prioritize a slice,
then independently trace current code and screen duplicates. Do not replay a
known bug or assume the same root remains.

### Novel discovery mode

Preserve the prior-art embargo. Build the thin slice from documentation,
interfaces, tests, types, comments, architecture, and observed runtime behavior.
Load vulnerability history only after target-native source/runtime/control proof
opens the gate.

## 6. Invariant decomposition

For each invariant:

1. state the exact protected property;
2. enumerate assumptions about input, caller, state, configuration, order, and
   environment;
3. identify which assumptions the attacker could control;
4. trace each to the authoritative consumer;
5. seek one concrete witness;
6. actively seek the closest source-supported falsifier.

Examples of useful comparisons include privileged versus restricted credential
handlers, explicit algorithm versus fallback selection, one versus multiple
rotated secrets, covered versus uncovered enforcement primitives, and cached
responses across auth contexts. These are method shapes, not claims about a new
target.

## 7. Search pressure without deception

Adversarial framing can improve exploration, but fabricated certainty poisons
evaluation. Use:

```text
Assume for this search pass that one stated invariant may fail. Find a concrete
witness or return NO_WITNESS. A separate pass will attempt to disprove it.
```

Do not say “there are definitely three bugs,” “I already found one,” or provide
hidden ground truth unless those statements are true and necessary. False
anchors bias candidate generation, invalidate blind evaluation, and conflict
with the package's `AGENT_REALITY_DECEPTION=FORBIDDEN` invariant.

## 8. Concrete proof, not exploit theater

Ask for the minimum test that would discriminate secure from insecure behavior:

- unit or integration regression;
- static invariant query;
- debug assertion;
- sanitizer build or reduced crash harness;
- local protocol/property test;
- safe owned-fixture request.

An operational payload is not required when a local deterministic witness proves
the boundary. Failure to construct a witness lowers confidence rather than
proving safety.

## 9. Bounded tail search

After first-pass findings:

- freeze already-covered roots;
- ask for a different assumption, representation, state order, or consumer;
- require new source evidence before another round;
- stop after two zero-gain rounds or when remaining work repeats names/payloads.

This prevents endless “what else?” prompting from turning into hallucination.

## 10. Slice handoff

Pass forward only:

- scope/release digest;
- verified facts;
- invariant and exact evidence pointers;
- killed assumptions;
- unresolved discriminators;
- candidate IDs and verifier status;
- newly reachable slice, if any.

Do not pass the entire conversation, motivational framing, or unsupported impact
narrative. Reconstruct evidence from source and test artifacts.

## Acceptance

A slice succeeds if it yields either a reproducible candidate or a bounded
`NO_WITNESS`/`EXHAUSTED` result with meaningful coverage. Candidate count is not
the metric. Useful metrics are invariant coverage, exact trace coverage,
verifier completion, false-positive rate, context consumed, and marginal new
evidence.
