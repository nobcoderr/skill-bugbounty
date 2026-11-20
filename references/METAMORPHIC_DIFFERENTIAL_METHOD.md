# Metamorphic Differential Method

## Find semantic siblings

Inventory operations that claim the same protected meaning but differ in
protocol, handler, version, batching, cache, queue, importer, worker, recovery,
or compatibility implementation.

Build a matrix:

| Semantic operation | Entry path | Authn | Authz | Normalize | State guard | Quota | Consumer |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Do not assume symmetry from shared naming. Trace each path to its final effect.

## Define a metamorphic relation

Derive transformations from parsers and consumers present in the repository.
Examples of semantic axes include normalization order, equivalent encodings,
field aliases, version adapters, batch wrapping, cache presence, sync/async
delivery, and recovery routing.

For transformation `T`, define:

`security_effect(input) == security_effect(T(input))`

when both inputs denote the same principal, object, operation, authority,
amount, and state. If they are not semantically equivalent, discard the test.

## Compare controls and effects

Compare authentication, authorization, tenant/object identity, validation
order, canonicalization, state checks, limits, error/default behavior, and
final consumer identity. A missing call is insufficient; prove there is no
equivalent enforcement upstream or downstream.

Use three controls:

1. canonical baseline;
2. one-variable equivalent transform;
3. non-equivalent negative input that must remain denied or isolated.

Record authoritative protected effects rather than status codes alone.

## Falsify

KILL when shared middleware enforces the invariant, the paths have different
security semantics by design, normalization makes them identical before the
guard, attacker control is impossible, or the divergent result has no protected
impact.

Do not hardcode public payloads or transformation lists. Every transformation
must cite the target parser/adapter/consumer that makes it meaningful.
