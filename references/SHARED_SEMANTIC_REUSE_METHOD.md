# Shared Semantic Reuse Method

## Purpose

Find a component, parser, validator, normalizer, cache, serializer, or policy
helper reused across domains whose security rules are not actually equivalent.

## Build the reuse graph

Map:

`shared component -> domain A consumers -> domain B consumers -> domain-specific rules`

Derive domain pairs from the target. Useful comparison axes include:

- encode versus decode;
- serialize versus deserialize;
- import versus export;
- read versus write;
- producer versus consumer;
- foreground versus background;
- synchronous versus asynchronous;
- validation versus execution;
- cache population versus cache retrieval;
- privileged versus ordinary caller context.

Do not assume that a listed pair exists or is vulnerable. Require call-graph,
configuration, type, or runtime evidence that the same semantic machinery is
actually reused.

## Test the domain rule

For each reuse edge ask:

1. Which rule is valid in domain A?
2. Is that rule valid, forbidden, or differently scoped in domain B?
3. Which identity, authority, representation, state, or resource bound changes?
4. Does the shared component know which domain it is serving?
5. Do wrappers restore the missing domain-specific control?

Generate one clean, target-derived differential and one safe sibling. A
difference is a hypothesis until the exact consumer and protected effect are
proven.

## Feed the cascade safely

If reuse explains an anomaly, derive detection strategies for sibling consumers
and different protected effects. Pass only the abstract semantic mismatch into
the cascade; never pass a known payload or let the child inherit proof.
