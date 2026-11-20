# Dynamic Filter and Query-Evaluator RCE Method

## Contents

1. Historical prior art
2. Reusable chain model
3. Audit workflow
4. Source and dependency search
5. Authentication, liveness, and output channels
6. Safe proof and controls
7. Impact validation
8. Patch and variant analysis
9. Remediation and regression tests
10. KILL rules

## Historical prior art

The canonical public case for this method is Taskcluster
`GHSA-ccv5-c45x-2q38` / `CVE-2026-11892`. The official advisory describes a
free-form GraphQL `filter: JSON` value reaching `sift` 17.1.3, whose string
`$where` operator could compile a predicate with `new Function` when
`process.env.CSP_ENABLED` was not enabled. The exposure was unauthenticated where a deployment's
anonymous role could call an affected resolver. The advisory records versions
before 100.3.0 as affected and 100.3.0 as patched.

The upstream fix, Taskcluster PR #8718, removed `sift`, deleted or replaced the
open filter arguments, and used typed `searchTerm: String` inputs for the small
substring-search behavior the UI actually needed. Treat that invariant-restoring
change as stronger than blacklisting one operator.

Primary lineage:

- Advisory: https://github.com/taskcluster/taskcluster/security/advisories/GHSA-ccv5-c45x-2q38
- Fix: https://github.com/taskcluster/taskcluster/pull/8718
- Merge commit: `a1b0154b8235937657c2ded127f193b564e2334b`
- Fixed release: `100.3.0`

This exact root cause and fixed path are prior art. A future candidate must show
a distinct current endpoint, evaluator, sibling implementation, incomplete
patch, or reintroduction—not merely reproduce the public case.

## Reusable chain model

Use this grammar:

`API input -> open control object -> generic query DSL -> executable operator -> dynamic compiler/interpreter -> predicate invocation -> runtime authority -> protected impact`

The core defect is **control/data confusion**. The application intends to expose
data-only search semantics but delegates an attacker-controlled object to an
interpreter whose full operator set includes code execution.

Separate these boundaries:

| Layer | Evidence question |
|---|---|
| Schema | Can the caller supply arbitrary nested keys, values, arrays, or objects? |
| Transport | Does GraphQL/REST coercion preserve the dangerous representation? |
| Application | Is the raw object passed through, merged, normalized, or allowlisted? |
| Dependency | Which exact operators exist by default in the installed version? |
| Runtime | Which environment flags, module modes, or CSP settings change behavior? |
| Authorization | Which principal reaches each resolver and upstream loader operation? |
| Liveness | What guarantees at least one element invokes the predicate? |
| Output | How can a benign marker distinguish execution from parsing? |
| Authority | What process, service account, filesystem, network, or credential boundary is crossed? |

## Audit workflow

### 1. Pin reality and scope

Record the repository, commit/tag, released package, deployed version, endpoint,
allowed testing mode, anonymous-role configuration, dependency lock entry,
runtime version, feature flags, and process identity. KILL an archived or fixed
path before deeper work.

### 2. Enumerate open filter surfaces

Look for:

- GraphQL `JSON`, `JSONObject`, `Any`, custom scalar, or map-like arguments
  named `filter`, `query`, `where`, `match`, `selector`, `criteria`, or `search`;
- REST bodies/query parameters forwarded as filter/query objects;
- resolver or loader parameters whose static type is broader than the UI's real
  search use case;
- generic filtering utilities reused by many list endpoints;
- WebSocket/subscription, batch, admin, compatibility, or alternate API paths.

Do not flag an open scalar by itself. Trace its exact consumer.

### 3. Trace to the evaluator

Follow:

`schema/controller -> resolver -> loader/service -> wrapper -> dependency API -> operator dispatch -> dynamic sink -> invocation`

Read callers, callees, generated schema, UI queries, tests, lockfiles, and the
installed dependency source together. Determine whether options restrict the
default operator set or whether the library receives the raw object.

### 4. Inventory code-bearing semantics

Search for operator handlers and callbacks that use:

- `new Function`, `Function`, `eval`, VM/context execution, expression
  compilation, template compilation, dynamic import/require, reflection, or
  caller-supplied predicates;
- `$where`, `$function`, script/expression/callback keys, nested logical
  operators, or aliases that can reach the same handler;
- custom operation registration, operation merging, prototype traversal,
  getters, or recursively interpreted keys.

The presence of `new Function` in a dependency is C0-C2 evidence. Prove the
attacker-selected operator reaches it in the installed version and real config.

### 5. Reconstruct the principal path

Distinguish:

1. missing credentials accepted by middleware;
2. the principal placed in request context;
3. resolver-level authorization;
4. loader calls to upstream services;
5. anonymous/default role scopes;
6. object or field authorization after filtering.

Middleware calling the next handler without credentials is not automatically an
authorization bypass. Conversely, authentication on the outer API is not a fix
for exposing executable filter semantics to low-privileged users.

### 6. Prove liveness separately

Predicate evaluators often run only when a collection contains data. Record:

- which upstream call populates the collection;
- whether an owned input deterministically yields one benign element;
- pagination, caching, error, and empty-result behavior;
- whether the evaluator runs once per element or during query construction.

Use an owned, deterministic element. Do not rely on another user's role, hook,
task, secret, or object.

### 7. Map the output channel

Prefer a harmless computed marker. Possible evidence channels include a returned
boolean/value, a deliberately thrown marker handled by the normal error
formatter, a local test callback, an instrumented evaluator invocation, or a
temporary marker in an isolated fixture.

Error reflection is only an output channel. It becomes security evidence after
server-side computation has been independently established.

## Source and dependency search

Use searches as hypothesis generators:

- schema: `filter.*JSON`, `where.*JSON`, custom JSON scalars, map/object inputs;
- forwarding: `sift(filter)`, `matches(query)`, `compile(filter)`,
  `array.filter(evaluator(...))`, or raw request objects passed to query helpers;
- sinks: `new Function`, `eval`, `vm.`, expression/template compilers, dynamic
  predicate builders;
- operations: `$where`, `$function`, script/expression/callback handlers;
- configuration: `CSP_ENABLED`, other CSP/safe-mode toggles, operation allowlists, environment
  defaults, and custom operator registration;
- package graph: direct/transitive dependency, lockfile version, bundled copy,
  vendored code, and release artifact.

Search semantic siblings, not only the same library name. The reusable class is
an untrusted control object reaching a code-capable interpreter.

## Safe proof and controls

Do not begin with shell commands, environment dumps, secrets, network callbacks,
or third-party data. Escalate only in an explicitly authorized disposable lab.

Use this sequence:

1. **Baseline:** the same resolver and owned data work with an ordinary typed
   search/filter.
2. **Reachability control:** malformed or disallowed operator is rejected before
   the evaluator when the protection is present.
3. **Liveness control:** show the marker does not fire for an empty collection
   and does fire for one owned benign element.
4. **Runtime control:** compare the vulnerable configuration with a restricted
   operator set or the documented mitigation.
5. **Computed canary:** prove server-side evaluation using a unique harmless
   calculation or instrumented callback.
6. **Context proof:** in a local disposable instance, prove the callback runs in
   the application process without spawning a shell or reading secrets.
7. **Cleanup:** remove fixtures, temporary markers, accounts, and logs containing
   sensitive values.

Record request/response or test traces, exact version, timestamps, baseline,
positive proof, negative controls, and why alternate explanations fail.

## Impact validation

Map process authority without harvesting it:

- OS/container identity and sandbox boundaries;
- writable directories and automatic consumers;
- outbound/internal-network policy;
- database, queue, storage, OAuth, signing, or encryption capabilities;
- workload/service-account scopes;
- whether secrets are static, scoped, expiring, rotated, or independently usable.

Code execution in the application process is already a protected execution
boundary. Do not require dumping real environment values to prove it. If a
credential bridge is essential to a higher impact claim, validate only an owned,
non-sensitive capability with explicit authorization, least privilege, negative
control, no secret disclosure, and cleanup.

## Patch and variant analysis

For a public fix, compare:

- every schema field that accepted the open filter;
- resolver, loader, utility, and direct dependency call sites;
- REST, GraphQL, subscription, batch, internal, admin, and compatibility paths;
- typed replacement semantics versus a token blacklist;
- removal from source, package manifests, lockfiles, bundles, and release images;
- anonymous and authenticated principals;
- nested operator aliases and alternate evaluator libraries;
- older clients or generated schemas that can still send removed fields;
- regression tests for both empty and non-empty data.

A sound fix narrows the API to the actual product requirement and removes the
general interpreter. An environment flag or a `$where` blacklist is mitigation,
not a complete invariant repair.

## Remediation and regression tests

Prefer, in order:

1. Remove the generic evaluator from the untrusted path.
2. Replace open JSON with typed fields implementing only required comparisons.
3. If a query DSL is unavoidable, build a recursive allowlist of fields and
   data-only operators; reject unknown `$`-prefixed keys, accessors, prototypes,
   and executable callbacks before dependency code.
4. Authorize the final parsed query and resulting object set.
5. Run the service with least privilege, network restrictions, and secrets that
   are scoped and rotatable.
6. Treat runtime/CSP flags as defense in depth.

Add tests that:

- reject the code-bearing operator at every former endpoint and nesting level;
- instrument dynamic compiler APIs and assert they are never invoked by request
  data;
- cover anonymous, low-privileged, and authorized principals;
- cover empty and deterministic non-empty collections;
- verify the typed replacement provides only intended search semantics;
- verify the dependency is absent from manifests, lockfiles, bundles, and
  release artifacts when removal is the fix.

## KILL rules

Mark `KILL` when the candidate is public/fixed/duplicate, lacks a current
release path, never reaches a code-capable operator, depends on a disabled
non-default configuration absent from deployment, cannot invoke the predicate,
is blocked for the attacker principal, or proves only an error/sink without
execution and protected impact.

Do not rescue a burned lineage by changing the title from GraphQL injection to
dependency RCE, anonymous access, secret exposure, or CI compromise. Preserve
the exact root cause and public prior-art family.
