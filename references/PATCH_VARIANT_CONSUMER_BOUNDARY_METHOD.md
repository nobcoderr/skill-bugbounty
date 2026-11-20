# Patch-Variant and Consumer-Boundary Method

`PATCH_VARIANT_CONSUMER_BOUNDARY:v1`

Use this method for authorized review when a security decision is made on one
condition, representation, or protocol model but a later component consumes a
larger semantic domain. It covers three recurring families without treating
their historical payloads as signatures:

1. a narrow patch guards one failure mode while the same operation has other
   attacker-reachable errors;
2. a selector, validator, or sanitizer accepts representation A while a later
   parser, template, DOM, or worker consumes representation B;
3. a validator approves a URL or resource identifier without constraining the
   protocols and authority available to the downstream client.

The unit of analysis is the restored security invariant plus every consumer of
the resulting state. Public reports below are fixed prior art. Their exact
paths are `KILL / PUBLIC / FIXED / DUPLICATE`; use them only to derive general
questions for a distinct current target.

## Historical prior art and bounded lessons

### Cosmos SDK `x/group` EndBlocker error propagation

User-supplied public HackerOne report `#3018307` maps to the follow-on advisory
below. The report and both advisories are historical, public, and fixed.

Official advisories:

- [GHSA-x5vx-95h7-rv4p](https://github.com/cosmos/cosmos-sdk/security/advisories/GHSA-x5vx-95h7-rv4p)
  documented a malicious group proposal that caused division by zero and chain
  halt; it was fixed in v0.50.12 and v0.47.16.
- [GHSA-47ww-ff84-4jrg](https://github.com/cosmos/cosmos-sdk/security/advisories/GHSA-47ww-ff84-4jrg)
  documented a follow-on `x/group` EndBlocker error path that could also halt a
  chain; it was fixed in v0.50.13 and v0.47.17.

General lesson: a zero-denominator guard does not establish that decimal
division is total over the admitted input domain. Range, exponent, precision,
overflow, underflow, context, conversion, and serialization failures must be
enumerated. An ordinary validation error and an error escaping a consensus
lifecycle consumer have different impact.

### GitLab Kroki selector-to-consumer disagreement

User-supplied public HackerOne report `#1731349` maps to the fixed GitLab issue
family below.

GitLab assigned
[CVE-2023-0050](https://gitlab.com/gitlab-org/cves/-/blob/master/2023/CVE-2023-0050.json)
to a stored XSS through a crafted Kroki diagram and fixed the affected release
lines in 15.7.8, 15.8.4, and 15.9.2. The historical report showed a useful
class: one node/attribute made a selector eligible, while a different
node/attribute was consumed to build an HTML fragment.

General lesson: prove that the value validated for eligibility is the exact
value used at the sink. Constructing markup by string interpolation can turn a
representation mismatch into attribute injection. A Content Security Policy is
not proof that the primitive is harmless; shipped same-origin scripts and data
attributes must be evaluated as distinct, evidence-required gadget edges.

### GitLab BulkImports URL validation versus Git transport

User-supplied public HackerOne report `#1685822` maps to GitLab issue `#372165`.

GitLab issue
[#372165](https://gitlab.com/gitlab-org/gitlab/-/issues/372165) records the
historical `RepositoryPipeline` flaw fixed in 15.4.1: attacker-supplied
`httpUrlToRepo` passed URL validation without an explicit scheme allowlist and
was then consumed by Git, whose supported transports included a local-file
scheme. Predictable internal repository paths turned that protocol expansion
into cross-project source disclosure.

General lesson: a URL validator is not a capability boundary unless it limits
the exact protocol set, redirect behavior, authority, path semantics, and
credentials understood by the downstream client.

## Unified invariant

For every candidate, state this invariant before searching for a payload:

> The exact security-relevant value and operation admitted by the enforcing
> component must remain within the same semantic and authority domain at every
> later consumer, and every attacker-reachable failure at a critical lifecycle
> consumer must resolve safely.

Then build this chain:

`attacker input -> admission representation -> decision/check -> retained state -> consumer representation -> authority-bearing operation -> lifecycle/error propagation -> protected impact`

Never inherit proof across a missing edge.

## Method A — Patch-variant failure-domain sweep

### Recover the invariant, not the literal condition

For a security patch:

1. identify the reported failing operation;
2. write the complete precondition under which that operation is safe;
3. list every input producer and every stored-state producer;
4. enumerate all error results, panics, exceptions, non-finite values, and
   invalid serializations—not only the branch changed by the patch;
5. trace each result through every caller to its final lifecycle consumer;
6. compare equivalent operations, libraries, branches, versions, and vendored
   copies;
7. search public history for the root-cause family before retaining a variant.

### Numeric and precision domain matrix

When attacker-controlled numeric strings, weights, ratios, quotas, prices, or
voting power reach arithmetic, record:

| Property | Admission constraint | Operation constraint | Failure behavior | Critical consumer |
|---|---|---|---|---|
| zero/sign | | | | |
| magnitude | | | | |
| exponent/scale | | | | |
| precision/rounding | | | | |
| overflow/underflow | | | | |
| parse/coercion | | | | |
| aggregate/cancellation | | | | |
| serialization/storage | | | | |

Do not assume a library operation only fails for its most familiar case. Read
the exact library version, context, error flags, wrapper, and caller behavior.

### Lifecycle severity ladder

Separate these effects:

- `L0` input is rejected before persistent state;
- `L1` one request or transaction returns an error;
- `L2` a local worker/job fails and retries safely;
- `L3` invalid state is persisted but quarantined;
- `L4` a deterministic block hook/finalizer returns an error;
- `L5` validators/full nodes fail to apply the same block or make progress;
- `L6` a network or control plane halts until upgrade/state intervention.

Do not call a candidate a chain halt from a local arithmetic error alone. Prove
the actual transaction/state path, voting/timing conditions, lifecycle hook,
error propagation, node behavior, and patched control on an isolated local
network. Never test denial of service on public nodes or mainnet.

### Patch completeness controls

Use at minimum:

- baseline: ordinary admitted values complete normally;
- closest one-variable sibling: the reported literal failure is guarded while
  another operation-domain boundary is varied;
- positive local candidate: harmless state reaches the lifecycle consumer;
- patched control: the same state is rejected, normalized, bounded, or handled
  without halting progress;
- authoritative read-back: block height/state/event/error chain, not only a CLI
  message;
- cleanup: stop local nodes and remove only the disposable state directory.

## Method B — Eligible value versus consumed value

### Node-and-value identity table

For markup, ASTs, config trees, deserialized objects, selectors, and workers,
record:

| Stage | Object/node selected | Field/value checked | Field/value consumed | Parser/builder | Output context |
|---|---|---|---|---|---|
| eligibility | | | | | |
| transformation | | | | | |
| serialization | | | | | |
| browser/worker use | | | | | |

Ask explicitly:

- Can child A satisfy the selector while parent/sibling B supplies the sink
  value?
- Does fallback order (`parent || child`, header then body, route then form,
  cache then request) change the identity?
- Is the validated object retained, or are raw bytes/another node reparsed?
- Does string interpolation re-enter HTML, JavaScript, CSS, URL, shell, SQL, or
  template grammar?
- Does a later sanitizer operate on the same context and the same attributes?

`Selector matched` is not equivalent to `consumed value validated`.

### Browser and CSP gadget discipline

If the first effect is markup or attribute injection:

1. prove the stored/reflected rendering path and victim privilege;
2. distinguish DOM structure from script execution;
3. enumerate only shipped scripts that read the injected class/id/data/URL;
4. state every required click, hover, navigation, or reload;
5. prove same-origin data retrieval and executable interpretation separately;
6. repeat with CSP enabled and disabled if both are relevant;
7. bound impact to the actions the victim origin can actually perform.

Do not call a CSP violation a CSP bypass. Do not call a click-assisted gadget
zero-click. Do not compose unrelated gadgets from another release.

### Safer construction invariant

Fix direction should align eligibility and consumption, then preserve type:

- resolve one canonical node/value and validate that exact value;
- use an explicit format/attribute allowlist at the consumer;
- construct DOM nodes and attributes through typed APIs rather than parsing a
  string-built fragment;
- encode for the final output context, not an earlier semantic context;
- add a regression where only the non-selected parent/sibling field is hostile.

## Method C — Validator versus protocol consumer

### Protocol-capability matrix

For every URL or repository/package/import location, enumerate:

| Layer | Accepted schemes | Redirects | Local/private targets | Credentials | Filesystem/process authority |
|---|---|---|---|---|---|
| request/schema | | | | | |
| URL validator | | | | | |
| normalizer/rewriter | | | | | |
| HTTP/Git/cURL/package client | | | | | |
| async worker/runtime | | | | | |

An omitted scheme list is a hypothesis. Retain it only when the exact downstream
client accepts a stronger transport and reaches a protected resource under the
service account.

### Identity and authority chain

Trace:

`remote import metadata -> URL rewrite -> URL validation -> queue/worker -> downstream client -> resolved protocol/path -> service-account read -> imported artifact -> attacker-visible destination`

Check:

- credentials inserted before or after validation;
- hostname, userinfo, port, path, fragment, and encoding normalization;
- redirects and final-destination revalidation;
- alternate schemes, local transports, helpers, and protocol handlers;
- chroot/container/mount/storage-node boundaries;
- predictable IDs, hashed storage paths, object names, or tenant layouts;
- async retries, worker placement, and storage affinity.

Do not guess worker co-location from flaky success. Prove scheduling/storage
conditions or classify the server condition explicitly.

### Safe A/B proof

Use only researcher-owned fixtures:

- Account A owns a private source repository containing a harmless canary.
- Account B cannot read A through the normal product path.
- Baseline imports B's own remote repository through an intended scheme.
- Negative control uses a nonexistent local path or disallowed scheme.
- Positive local lab uses a disposable local repository path belonging to A.
- Authoritative read-back proves the canary appeared in B's imported project.
- Patched control rejects the transport before the downstream client starts.
- Cleanup deletes both temporary projects/repositories and records no third-
  party data.

Never enumerate production filesystem paths, clone third-party repositories, or
retry across public workers to obtain co-location.

## Cross-family KILL challenge

Before `KILL`, answer all of these with evidence:

1. What exact invariant does the guard/validator/selector claim to enforce?
2. Is the value checked identical to the value consumed?
3. Is the operation total over the admitted input domain?
4. What happens for absent, fallback, error, overflow, redirect, alternate-
   scheme, and async-consumer states?
5. Does failure occur before persistence or inside an authority-bearing
   lifecycle consumer?
6. Which downstream component has greater parser/protocol/process authority?
7. Is there an upstream or downstream hard control on the same released path?
8. Is the root cause public, fixed, duplicated, or only a historical regression?

If evidence is incomplete, keep `HYPOTHESIS / NEEDS_CONSUMER_PROOF`. This is
not a finding and not a valid KILL.

## Required evidence and verdict

For every survivor include:

- attacker condition and server/deployment condition;
- exact release/package and prior-art lineage;
- admitted versus consumed representation/value;
- operation error-domain or protocol-capability matrix;
- forward input-to-sink and backward sink-to-input trace;
- protected boundary and authoritative impact evidence;
- baseline, closest negative control, patched control, read-back, request/trial
  budget, abort conditions, and cleanup;
- invalidation factors and minimal invariant-restoring fix.

Only `STRONG + MANUALLY_CONFIRMED` is report-ready. Public/fixed examples remain
methodology and regression material. If nothing distinct survives, return
`NO VALID FINDING`.
