# Cross-Boundary Composition Method

<!-- CROSS_BOUNDARY_COMPOSITION_METHOD:v1 -->

## Purpose and evidence status

Use this reference only for explicitly authorized security research. It turns
the user-supplied public write-ups into reusable audit methods for six related
classes of boundary failure:

1. shared workflow context overwriting server-trusted identity;
2. managed-runtime interop and serializer coercion reaching execution;
3. JWT verifier drift and asymmetric-to-symmetric algorithm confusion;
4. multi-hop Active Directory ACL and delegation chains;
5. layered mobile request-signing and encryption reconstruction; and
6. AI/NL-to-SQL data authorization and result fan-out.

The 8x8 report IDs below are public prior art and exact-root novelty burns:

- HackerOne `#3858504`, Automation Builder workflow-output context poisoning;
- HackerOne `#3861550`, Jint-to-Newtonsoft serializer coercion and
  `TypeNameHandling` RCE; and
- HackerOne `#3800870`, RS256-to-HS256 JWT algorithm confusion.

The supplied Active Directory article uses a fictionalized `evil.corp` lab,
and the supplied TikTok and AI analytics articles did not include a source URL
or verifiable target. Treat all claims as user-supplied research seeds until
independently tied to authoritative documentation, exact artifacts, versions,
and runtime evidence. Never replay these operational paths against 8x8,
TikTok, an unidentified analytics service, a public AD environment, or any
third party. Historical resemblance creates a hypothesis or duplicate check,
not proof of a live vulnerability.

## Activation map

Load only the lane supported by target evidence:

| Evidence | Primary lane | Additional specialists |
|---|---|---|
| User-controlled output keys share storage with server identity or credentials | Shared-context identity collision | Auth, API/business logic, parser/state, source/runtime |
| A template or script engine receives live CLR objects, `JObject`, `JToken`, or serializer-like values | Interop coercion and serializer construction | .NET, JavaScript, source, patch-diff, modern RCE |
| Multiple API generations or services verify the same JWT differently | JWT verifier drift | Auth, crypto/signature, API, relevant runtimes |
| AD ACLs connect users, groups, machine objects, delegation, key credentials, or GPOs | AD ACL chain reconstruction | Windows internals, red-team planning only when explicitly requested |
| A mobile/native client applies several request-integrity, attestation, signing, or encryption layers | Mobile request-signing reconstruction | Mobile, reverse engineering, crypto/signature, native runtime |
| An AI or natural-language query endpoint accepts dataset/space identifiers and executes database tools | AI-to-data authorization and result fan-out | AI, auth, API/business logic, SQL/database, source/runtime |

A generic word such as `workflow`, `token`, `mobile`, `Windows`, or `serializer`
is insufficient. Require a second signal identifying the representation,
runtime, trust boundary, or authority-bearing consumer.

## Common operating model

For every lane, build two linked ledgers:

- **Representation ledger:** exact attacker-controlled bytes, keys, objects,
  claims, ACL edges, headers, or state; every validation, conversion, merge,
  overload selection, serialization, lookup, and fallback; and the final value
  consumed.
- **Authority ledger:** authenticated starting principal, tenant/account,
  credential or key, process or service identity, directory object, device
  identity, protected recipient/action, and resulting authority.

Hold attacker authority constant. A candidate survives only when the same
current path proves:

`controlled representation -> admitted transform -> authority-bearing consumer -> unauthorized protected action -> authoritative read-back`

Prefer the one-variable `S/C/P` control triad where it fits:

- `S` — self/baseline operation under the researcher's ordinary authority;
- `C` — cross-boundary control without the suspected primitive; and
- `P` — the same cross-boundary request with only the suspected primitive
  changed.

The `C/P` pair is strongest when target, destination, state, timing, and all
other inputs are identical. A success status alone is not evidence: require a
failure/success differential plus authoritative state, ownership, billing,
identity, or execution read-back. Use only researcher-owned accounts, devices,
domains, infrastructure, and harmless canaries.

## Lane A — Shared-context identity collision

### Invariant

User-controlled workflow data must not overwrite server-trusted identity,
tenant, credential-selector, billing, authorization, or provenance fields. A
single dictionary is not automatically vulnerable; the finding requires a
later privileged consumer that trusts the collided key.

### Audit procedure

1. Enumerate each context namespace and label every key by writer and trust:
   trigger/authentication, engine, user step, connector, retry/resume path, or
   imported state.
2. Compare name validation symmetrically across inputs, outputs, variables,
   imports, templates, retries, and resume/deserialization paths. Record
   whether validators inspect values, keys, both, or neither.
3. Identify reserved fields even when the documentation does not name them.
   Work backward from credential, tenant, sender, billing, ownership, and
   policy consumers to every context lookup.
4. Trace merge order and collision semantics: reject, first-writer-wins,
   last-writer-wins, shallow/deep merge, case folding, normalization, and
   persistence across steps.
5. Trace resolver behavior beyond the direct lookup. Record composite-key
   failures, default-key fallback, cache lookup, tenant inference, retry, and
   whether ownership is rechecked at the final send/action sink.
6. Run a harmless `S/C/P` triad with two researcher-owned tenants when live
   testing is explicitly authorized. Stop after the minimum protected effect.
   Billing evidence, if permitted, must use a funded researcher-owned account,
   a minimum-cost action, before/after balance, stable reread, and cleanup.

### Evidence and falsifiers

Do not infer a credential swap from any one of these alone: workflow
`Complete`, a context echo, a mismatched key ID, queue acceptance, missing UI
logs, or an error string. Require the cross-boundary control to fail and the
otherwise identical poisoned case to succeed, then bind the result to the
protected tenant/action through an authoritative read-back.

Use `KILL_NO_AUTHORITY_CONSUMER` when the overwritten key is display-only or
revalidated before use. Use `KILL_EQUAL_AUTHORITY` when the attacker already
has an equivalent supported way to select the same credential or tenant. The
public 8x8 root is `KILL_KNOWN_OR_DUPLICATE` unless a current distinct product,
consumer, or incomplete fix is proven.

## Lane B — Interop coercion and serializer construction

### Invariant

Untrusted script/template data must not gain host authority because a bridge
exposes live runtime objects, selects an unsafe overload, or helpfully coerces
a dictionary into a security-sensitive configuration object.

### Enumerate actual runtime members

Do not deduce the reachable host surface only from documented sandbox flags.
For every injected value, record its concrete runtime type, wrapper type,
properties, indexers, methods, overloads, return types, extension methods,
enumerators/readers, callbacks, getters, setters, conversions, and objects
reachable from each return value. Distinguish plain script values from live CLR
objects such as `JObject`, `JToken`, `JsonReader`, tasks, exceptions, and
application step instances.

Build a conversion matrix for each callable boundary:

| Supplied value | Candidate overload | Conversion attempted | Constructed/configured type | Security-sensitive properties | Result |
|---|---|---|---|---|---|

Include generic/non-generic overload selection, dictionary-to-object
construction, numeric-to-enum coercion, instance/static dispatch, implicit
string conversion, indexer lookup, and serializer reuse. A parse that treats
`$type` as inert does not prove a later re-deserialization path will also treat
it as inert.

### Narrow-fix variant sweep

A narrow gadget fix is a new architecture lead, not closure. After confirming
the patched member and its accessor are blocked, freeze that root as known and
change reasoning axes rather than mutating member names:

- reflection and type acquisition;
- serialization/deserialization and attacker-configurable binders;
- overload selection and argument coercion;
- callbacks, getters, formatters, and late lifecycle hooks;
- live-object mutation after save-time validation;
- runtime values fetched after validation; and
- object construction that creates execution-capable host types.

Reproduce only in an isolated version-matched lab with inert effects. Do not
copy public commands, gadget payloads, file reads, process launch, or reverse
shells into a live target. A save-time validator bypass, a reachable CLR
object, or an unsafe serializer setting is an intermediate primitive; terminal
RCE requires the same current deployed path, a harmless execution marker, a
negative control, and authoritative read-back.

The public 8x8 interop and `TypeNameHandling` roots are prior art. A reportable
variant needs a distinct reachable conversion/consumer or a proven incomplete
fix, not a renamed reflection gadget.

## Lane C — Legacy/current JWT verifier drift

### Invariant

The verifier, not the attacker-controlled JWT header, must determine the
accepted algorithm and key type. All services accepting the same token family
must enforce compatible issuer, audience, key, claim, lifetime, revocation,
and operation-specific authorization rules.

### Verifier matrix

Build a matrix across API versions, gateways, legacy/new services, read/write
paths, regions, mobile/web entrypoints, and SSO surfaces:

| Verifier | Accepted algorithms | Expected key type | Issuer/audience | Claim source of truth | Read result | Write result | Error fingerprint |
|---|---|---|---|---|---|---|---|

Pin `alg` and key type server-side. Test algorithm rejection separately from
claim authorization. A fat token containing identity, tenant, access level, or
roles raises impact only if a vulnerable verifier trusts those claims without
an authoritative server-side binding.

Recoverability or publication of an RSA public key is not a vulnerability.
GCD recovery from researcher-owned RS256 signatures is relevant only as a
public-key provenance technique; the security failure exists only if a
verifier accepts an HMAC token using asymmetric public-key bytes as the HMAC
secret. Do not include reusable token-forging code in live-target work.

Use two researcher-owned tenants and the minimum read-only identity endpoint
when explicitly authorized. Prove the response contains server-side data from
the second owned identity rather than merely echoing forged claims. Map write
authorization independently; a read impersonation must not inherit write or
account-takeover impact. Compare every sibling verifier and record where
algorithm pinning already works.

The public 8x8 `#3800870` path is a known root. KILL when all relevant
verifiers pin algorithms/key types, the token is rejected before claims are
used, or the observed result is only payload echo.

## Lane D — Active Directory ACL chain reconstruction

### Invariant

Delegated directory rights must not compose into authority over a higher-value
principal, policy object, or domain-wide execution consumer beyond the intended
administrative boundary.

For each graph edge record:

| Current principal | Target object | Exact ACE/right | Writable attribute or operation | Primitive | Blocker | Alternate primitive | Next principal/authority |
|---|---|---|---|---|---|---|---|

Confirm BloodHound or graph output against the authoritative DACL and deny ACEs.
Distinguish `GenericAll`, `GenericWrite`, scoped property rights, validated
writes, group membership, object owner, and inherited rights. A graph edge is
a hypothesis until the exact object and attribute permission are confirmed.

Model machine accounts and special objects precisely. A Failover Cluster Name
Object is not interchangeable with a physical node account; SPN, UPN,
delegation, and S4U behavior can differ. If one primitive is blocked, do not
declare the edge dead until other operations granted by the same confirmed ACE
are evaluated, but keep each alternate primitive independently evidenced.

For delegation and key-credential paths, separate attribute write, KDC
acceptance, issued credential, recovered principal authority, and next ACL
edge. For GPO paths, separate control of the directory GPC, control or redirect
of the file-system GPT, client read reachability, policy refresh, execution
context, and domain impact. A writable share or modified attribute alone is not
Domain Admin.

Run only in an explicitly owned, isolated AD lab or authorized pentest with a
written allowlist, maintenance/abort plan, snapshots, and cleanup of machine
accounts, delegation descriptors, key credentials, GPO attributes/files, and
group membership. Never operationalize the supplied domain-escalation command
sequence. The fictionalized `evil.corp` chain is a methodology seed, not proof
about any real environment.

## Lane E — Layered mobile request-signing reconstruction

### Invariant

Every layer must be assigned its real security property. Reproducing an
obfuscation or integrity header does not prove possession of a device-bound
private key, server-side authorization, anti-abuse state, or an accepted
protected operation.

Create a layer ledger:

| Layer/header/body | Primitive fingerprint | Exact covered bytes | Key/nonce source | Freshness coupling | Server failure oracle | Security property |
|---|---|---|---|---|---|---|

Use permitted local application artifacts, captured traffic from a
researcher-owned device/account, and version-pinned native-library hashes.
Confirm algorithms from constants plus input/output pairs or traced calls; a
familiar constant or output length alone is not proof. Trace one request byte
for byte through canonicalization, hashing, encryption, signing, encoding, and
transport.

Look for shared derivation seeds and shared timestamps because one recovered
dependency may collapse several apparent layers. Still classify separately:

- reversible obfuscation and freshness encoding;
- keyed request-integrity or device metadata checks;
- body confidentiality;
- asymmetric device-bound signing; and
- behavioral/session/server state.

A successfully regenerated timestamp, hash chain, cipher block, or encrypted
body is mechanism evidence only. It does not bypass an ECDSA/private-key layer
or behavioral authorization. Require the final server acceptance oracle and a
protected capability delta before calling the result a vulnerability.

Do not automate production API impersonation, evade platform controls, extract
third-party device keys, or replay traffic from other users. The user-supplied
TikTok layer names and algorithm claims are research hypotheses until verified
against the exact authorized artifact and version.

## Lane F — AI-to-data authorization and result fan-out

### Invariant

An AI planner may choose query shape, but it must never decide data authority.
Every database execution, memory retrieval, event-stream disclosure, and
export must bind the authenticated subject to the canonical dataset, space,
tenant, row policy, and output object at the final server-side consumer.
Listing a user's accessible datasets is discovery, not enforcement. This lane
is normally object-level authorization failure, tenant isolation failure, or a
confused deputy—not SQL injection—when the generated SQL is an intended part
of the product.

### Authority and fan-out trace

Trace the full path without collapsing intermediate disclosures:

`authenticated subject -> entitlement set -> request selector/alias -> canonical dataset or space -> SQL-rule/schema retrieval -> model/tool plan -> database principal and row policy -> query execution -> preview/event stream -> similar-query memory -> signed full-result export`

Build a selector matrix for every way the resource can be named: path ID, body
dataset ID, space ID, feature flag, chat/thread state, tool argument, stored
conversation value, export object, and retry/background-job state. For each
selector record normalization, canonical resolution, the authorization call,
the exact resource passed to that call, the resource consumed by the database,
and the resource bound into the result/export. Test aliases and conflicting
selectors because a check on one identifier does not authorize a sibling path.

Keep these effects separate:

- unauthorized dataset query execution and authoritative result data;
- cross-user or cross-tenant similar-question/memory retrieval;
- tool instructions, system prompt, SQL rules, or schema disclosure;
- preview truncation versus a complete exported result; and
- signed object-storage URLs as bearer capabilities, including object binding,
  permission, expiry, audience, revocation, and row count.

Generic OpenAPI, Swagger/Redoc, public configuration, a client-distributed API
key, system prompt, or database schema may reduce discovery cost but is not a
protected-boundary impact by itself. A signed download URL amplifies an
unauthorized query only after ownership and data origin are proven; it is a
separate finding only when its own authorization or recipient binding crosses
a distinct boundary.

### Controlled proof matrix

Use two or three researcher-owned accounts/tenants and synthetic datasets with
unique canaries. First obtain the authenticated subject's authoritative
entitlement list. Then compare:

- `S` — query an entitled owned dataset and recover its canary;
- `C` — request a non-entitled owned dataset through the ordinary selector and
  require denial; and
- `P` — hold subject, question, model/tool configuration, and dataset constant,
  changing only the suspected selector or missing-check path.

Also test an invalid identifier, every supported selector alias, an empty
entitlement, and a downstream database/RLS denial where available. Prove data
origin with a researcher-planted canary or owner-side authoritative read-back,
not an AI summary, HTTP 200, streamed status, generated SQL, row count, or
plausible-looking output. Treat read and write authority independently.

For memory isolation, seed a harmless unique question in account B and prove
whether account A receives that exact canary without requesting or sharing it.
For exports, compare preview count with the owned result object, record only
non-secret URL metadata, and do not redistribute the bearer URL. Do not request
broad employee, contract, invoice, supplier, or financial enumerations. Abort
and minimize evidence immediately if any unexpected third-party PII or business
data appears; do not follow, download, correlate, or expand it.

### Evidence and falsifiers

KILL when the final query executor independently enforces the subject's
canonical dataset/tenant and row policy, when returned data belongs to an
intentionally shared resource, when only public schema/instructions are
disclosed, or when the model fabricated the apparent result. A client-side
entitlement screen is not enough to retain or kill the candidate: locate the
final enforcement point. Require current deployed reachability, exact program
eligibility, a nonzero capability delta, and one-variable owned-data controls.

The supplied “SQLi Without SQLi” article is an unverified methodology seed. It
must not be cited as proof that any named or inferred product is vulnerable,
and its reported third-party data shapes must never be reproduced during
testing.

## Cross-lane variant questions

After mapping the target natively, ask only evidence-supported questions:

- Does a user-data namespace overlap a trusted identity namespace?
- Does validation cover keys as well as values, and the same representation
  later consumed?
- Does fallback resolution change principal, tenant, credential, or billing?
- Does an interop bridge enumerate differently at runtime than its sandbox
  policy suggests?
- Can overload resolution or coercion construct a security-sensitive object?
- Did a fix remove one gadget while leaving the live host object or unsafe
  conversion boundary intact?
- Do old and new verifiers enforce the same algorithm, key type, claims, and
  operation-specific checks?
- Does a blocked AD primitive leave a different capability under the same
  confirmed ACE?
- Which mobile layers are reversible format checks, and which require an
  unavailable private key or server state?
- Is dataset authorization enforced at the query/export consumer, or only at a
  separate listing/UI endpoint?
- Do dataset/space aliases resolve to one canonical resource before policy,
  database execution, memory retrieval, and signed-export creation?

Reject name, payload, encoding, or endpoint-alias churn. Each variant needs a
target-native invariant, a new material consumer or authority edge, current
release/deployment reachability, a deterministic oracle, baseline, closest
safe sibling, negative control, falsifier, harmless proof, cleanup, and stop
condition.

## Required output

For the active lane, provide:

1. source status and exact prior-art/duplicate treatment;
2. target/scope evidence card;
3. representation and authority ledgers;
4. exact source-to-consumer and sink-to-source traces;
5. one-variable controls, authoritative read-back, and alternative
   explanations;
6. narrow-fix or sibling-verifier coverage where relevant;
7. program-impact capability delta and current reachability;
8. separate query, memory, schema/prompt, stream, and export judgments where
   the AI-to-data lane is active;
9. safety, abort, and cleanup plan; and
10. `STRONG`, `MEDIUM`, `WEAK`, `KILL`, or `NO VALID FINDING`, with manual
   status kept separate.

Only `STRONG + MANUALLY_CONFIRMED` may be report-ready. Public/fixed roots,
unverified article claims, mechanism-only reproductions, graph-only paths,
layer reimplementation without a protected effect, AI-generated results
without owned-data provenance, and chains with a missing authority-bearing
consumer remain non-reportable.
