# Schema-Driven API Campaign Method

## Purpose

Turn a large machine-readable API surface into bounded, typed, reviewable work.
This method improves completeness; it does not authorize broad testing and does
not make schema contents trustworthy.

## 1. Snapshot and normalize

Capture the authorized schema artifact and its retrieval context:

- artifact type and canonical source;
- retrieval time and authorization basis;
- target/version/visibility context;
- whole-document digest;
- normalization tool version.

Normalize every method into a stable identifier. Keep host, version, verb,
path/query path, typed request shape, response shape, auth modes, resource IDs,
and definition hash. A changed definition hash invalidates stale probe plans.

For GraphQL, represent a method as a query path rather than pretending every
field is an endpoint. Traverse from query/mutation roots and stop when a field:

- takes arguments;
- returns a scalar or enum;
- crosses a target-native converted RPC/protobuf object boundary.

Prune unrelated types only in the per-group view. Preserve the complete sealed
schema separately so pruning cannot hide dependencies.

## 2. Group by boundary

Group methods using:

- resource family and parent-child relationship;
- ownership namespace: user, account, org, project, tenant;
- action class: list/get/create/update/delete/admin/execute;
- common authorization middleware or backend;
- identifier flow between methods.

Groups are context controls, not independent silos. Pass forward only verified
facts: owned resource IDs, accepted enum values, confirmed method relationships,
and definition hashes. Do not pass forward candidate conclusions.

## 3. Coverage ledger

Each method has exactly one current state:

- `UNTESTED`
- `PLANNED`
- `TESTED`
- `BLOCKED_WITH_REASON`
- `NOT_APPLICABLE_WITH_SCOPE_EVIDENCE`
- `STALE_SCHEMA_RECOMPILE_REQUIRED`

A completion gate may require every in-scope method to leave `UNTESTED`, but it
must not force unsafe, out-of-scope, destructive, or credential-dependent
probes. Such methods are explicitly blocked with evidence.

## 4. Reduce model error surface

Give the model only fields it needs to choose:

- stable method ID;
- typed request parameters/body;
- owned identity label;
- owned resource label;
- declared probe intent.

The harness resolves immutable transport facts. Reject unknown methods,
invalid types, paths outside the schema, unauthorized identities, and resource
IDs outside the owned fixture registry before network execution.

## 5. Differential probes

Prefer a role-object-action matrix and one-variable controls:

| Operation | Identity | Object | Expected |
|---|---|---|---|
| baseline | owner A | object A | allowed |
| cross-owned control | user B | object A | denied |
| self sibling | user B | object B | allowed |
| nonexistent control | user B | nonexistent object | neutral denial |

All identities and objects remain researcher-owned. Exact program policy may
require an even narrower matrix.

## 6. Multi-variant execution

If a service legitimately varies by program-issued test credential, visibility
label, region, or version, execute the same typed request across the explicitly
approved variants. Preserve each variant record and group identical responses
by body hash for review efficiency. A grouped response never erases which
variant produced it.

Do not scrape or repurpose keys from applications, binaries, traffic, or public
artifacts. A discovered credential is routed to the credential exposure gate,
not silently added to the test pool.

## 7. Finish condition

Coverage finishes when every permitted method is accounted for. Research
finishes only after all candidates are replayed and judged, mutations are
cleaned, and unresolved methods are labeled rather than guessed.
