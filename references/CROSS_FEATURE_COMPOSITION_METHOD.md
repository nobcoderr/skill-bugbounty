# Cross-Feature Composition Method

## Preserve weak primitives

Record a primitive even when it does not independently cross a protected
boundary. Examples of primitive roles include attacker-controlled metadata,
stored representation, delayed callback, secondary fetch, queue message,
identity alias, partial file effect, cache entry, or optional consumer.

Do not increase severity by listing unrelated primitives. A composition edge
exists only when the same current-release workflow transfers data, identity,
authority, or capability between them.

## Build the composition graph

For each primitive record:

| ID | Attacker control | Produced artifact/state | Persistence | Consumers | Authority delta |
|---|---|---|---|---|---|
| | | | | | |

Connect primitives through exact storage keys, object identities, queue
payloads, filenames, URLs, callbacks, serialized fields, feature flags,
renderers, importers, recovery paths, or privileged workers.

## Search compositions

Explore pairs first, then bounded triples. For every edge ask:

- does the downstream consumer trust provenance the producer does not provide;
- does persistence outlive validation or authority;
- does a worker reinterpret metadata with more privilege;
- does one feature make an otherwise unreachable consumer active;
- does a weak read/write/redirect/markup effect supply a capability another
  feature consumes;
- do multiple individually safe objects violate an aggregate invariant.

## Prove or kill each edge

Require exact source trace, same release/configuration, attacker-reachable
handoff, final consumer identity, authority transition, protected effect,
negative control, and cleanup.

Use these edge states:

- `UNTESTED`;
- `SOURCE_LINKED`;
- `RUNTIME_LINKED`;
- `COMPOSES`;
- `PROVEN_NO_PATH`;
- `NON_COMPOSABLE`.

If a candidate has composition edges, do not KILL it while any plausible edge
is `UNTESTED`, `SOURCE_LINKED`, or `RUNTIME_LINKED`. KILL only after all edges
are `PROVEN_NO_PATH` or `NON_COMPOSABLE`, or after a stronger independent gate
such as out-of-scope/current-release-unreachable is proven and recorded.

Never infer terminal impact from the names of the primitives. Prove every edge
on the same authoritative path.
