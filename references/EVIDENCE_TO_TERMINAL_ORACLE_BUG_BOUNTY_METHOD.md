# Evidence-to-Terminal-Oracle Bug Bounty Method

## Provenance and claim status

This method distills a user-supplied 12 October 2026 corpus covering a reported
Google DevSite signed-session/unsafe-deserialization chain, a Gemini CLI passive
evidence-review workflow, a long-horizon Google kvmCTF exploit campaign, and a
reported XRPL/rippled accounting-invariant chain.
Named vendors, rewards, dates, flags, affected domains, CVE/patch attribution,
and “first” claims are **user-supplied prior art** until independently checked
against authoritative sources. They are not target ground truth, authorization,
or a reusable exploit recipe.

The transferable unit is the evidence shape: preserve representation,
authority, state, topology, controls, provenance, and a terminal oracle that
cannot be produced by persuasive prose.

## Contents

1. Lane A — client-carried trust and deserialization
2. Lane B — passive evidence analyst
3. Lane C — long-horizon systems exploitation
4. Lane D — consensus accounting and invariant chains
5. Terminal-oracle hierarchy
6. Evidence and reporting contract
7. Kill and blocked states

## Lane A — client-carried trust and deserialization

### A1. Treat client state as readable

Signing does not encrypt. For an authorized capture or local fixture, inventory
the exact byte pipeline:

`cookie/header -> segment split -> URL-safe base64 -> optional compression -> data format -> tagged values -> nested serialization`

Record raw-artifact hash, framework/version, separators, compression marker,
padding rules, decoder, tag semantics, and final value types. Reject a decode
that cannot round-trip to the original bytes.

### A2. Inventory authority inside the representation

Classify every embedded value:

- public identifier;
- CSRF/state nonce;
- OAuth/client credential;
- session-signing or encryption key candidate;
- serialized server object;
- opaque server-side reference;
- attacker-controlled field.

A client identifier is not a secret. A secret-looking value is not a current
credential. A serialized object is not RCE. Preserve each claim separately.

### A3. Test cross-purpose secret reuse offline

The high-value invariant is:

> A value recoverable from attacker-readable state must not also authenticate
> or authorize that same state or another protected channel.

Use an issued artifact as the positive vector. Reproduce the framework's exact
salt, key derivation, digest, canonical payload, timestamp treatment, encoding,
and signature bytes offline. Require:

- recovered candidate verifies the unchanged issued artifact;
- a wrong candidate key fails;
- a one-bit signature change fails;
- an altered payload with the old signature fails;
- a re-signed local fixture verifies under the same offline verifier.

This proves an offline key relationship, not server acceptance of a forged
artifact. Do not submit the forged value to a live service without explicit
authorization for that exact action.

### A4. Prove the integrity-to-execution chain edge by edge

Use this ledger:

| Edge | Required proof |
|---|---|
| Readable state | Exact decode and byte round-trip |
| Secret exposure | Value class, current lineage, and fingerprint without propagation |
| Key reuse | Offline framework-equivalent signature reproduction and controls |
| Forgeability | Locally constructed state accepted by an independent local verifier |
| State selection | Callback/consumer uses attacker-selected key, state, or flow entry |
| Deserialization | Exact current-release call path reaches an unsafe object loader |
| Callable/gadget | Runtime availability and argument control in an authorized local fixture |
| Terminal effect | Minimal harmless oracle with baseline and negative controls |

Do not collapse CSRF control, session integrity loss, unsafe deserialization,
and code execution. A dangerous loader protected by unforgeable integrity is a
different state from the same loader after the integrity boundary is proven
forgeable.

### A5. Blast radius

Never infer shared-key impact from branding or platform similarity. For each
explicitly in-scope sibling asset, independently prove artifact format,
verification behavior, key relationship, deployment identity, and protected
consumer. Stop at the first sufficient harmless proof and never use a recovered
secret for unrelated OAuth or account access.

## Lane B — passive evidence analyst

### B1. Role boundary

A passive model receives already captured HTTP traffic, source, stack traces,
serialized artifacts, or execution logs. It does not interact with the target,
obtain credentials, replay requests, or execute a proposed exploit. This role
is an evidence-analysis specialization, not a way to bypass another model's
safety behavior.

### B2. Blind-review protocol

Withhold the expected vulnerability class, hidden objective, answer key,
payload, and prior conclusion. Provide the exact scope card and immutable
artifact IDs. Ask the analyst to output:

| Field | Meaning |
|---|---|
| Observation | What the artifact directly proves |
| Source | Exact attacker-controlled value |
| Transforms | Decode, parse, normalize, store, or serialize steps |
| Consumer/sink | Current-release component using the value |
| Authority | Principal or privilege held by the consumer |
| Hypothesis | Candidate invariant violation |
| Missing proof | First unsupported edge |
| Baseline/control | One-variable falsifier |
| Safe next question | Evidence to collect, not a conclusion |

The analyst may rank candidates. It may not certify exploitability, severity,
or report readiness.

### B3. Manual promotion gate

Examples of leads that remain unproven:

- missing browser-origin checks without demonstrated privileged same-origin
  effect;
- weak URL substring checks without a browser-reachable sink;
- serialization magic bytes without acceptance of modified bytes;
- a dangerous API or gadget family without runtime availability;
- HTTP 500 without an authoritative out-of-band or state oracle.

Promotion requires target-native manual reproduction, a negative control,
current-release reachability, a program-recognized capability delta, and
cleanup.

## Lane C — long-horizon systems exploitation

### C1. Model a state machine, not a payload

Represent the campaign as typed states:

`S0 precondition -> S1 primitive -> S2 poisoned/inconsistent state -> S3 lifecycle retirement -> S4 controlled pressure/reallocation -> S5 consumer trigger -> S6 protected oracle`

For every transition record:

- exact version/build and topology layer;
- attacker-controlled operation;
- precondition and postcondition;
- target-side mechanism;
- telemetry marker;
- baseline and falsifier;
- failure class;
- cleanup or terminal state.

The names above are generic. Do not transplant public opcodes, allocation
counts, thresholds, flags, or constants into a different target.

### C2. Use failure as telemetry

An unsuccessful run creates value only when it invalidates or narrows an
assumption. Instrument the closest safe local replica and classify the failure:

- reachability;
- representation/type constraint;
- lifecycle/lifetime;
- allocator or topology mismatch;
- timing/nondeterminism;
- privilege/sandbox;
- harness/evaluator artifact.

Change only the failed dimension after new material evidence. Adding sleeps,
spray volume, retries, or candidate names without new evidence is blocked.

### C3. Preserve topology fidelity

Map every layer that owns translation, caching, allocation, policy, or proof.
A local proof must identify where it differs from the production/challenge
topology. A local token, crash, or instrumented signal does not replace an
official oracle when the program contract requires the official environment.

### C4. Attempt and reliability ledger

Freeze each attempt tuple and result. Report:

- total deduplicated attempts;
- attempts reaching every intermediate marker;
- independent terminal successes;
- environmental repairs or mutations;
- source and workpack digests;
- build fingerprints;
- whether later reads reuse a persistent success flag.

Repeated reads of one persistent oracle state are not independent exploit
successes. A mutable live directory repaired in place is source-faithful only
when its exact provenance limitations are disclosed; it is not byte-identical.

### C5. Protected-oracle proof

A strong terminal oracle is generated by a protected component and is
unavailable from the attacker's starting state. Examples include a vendor-side
challenge secret, authoritative state read-back, or an owned out-of-band canary.
Document why local code or logs could not fabricate it. Do not use a third
party's data, secret, or service as the oracle.

## Lane D — consensus accounting and invariant chains

When an economic state transition and its safety invariant use bounded numeric
domains, read
`CONSENSUS_ACCOUNTING_INVARIANT_CHAIN_METHOD.md`. Define conservation in
arbitrary-precision mathematics, inventory every producer/checker conversion,
and prove whether one attacker-controlled transition can make both machine
domains lose the same information. Keep per-item settlement, aggregate debit,
per-account limits, global supply, submit, commit, finality, and spendability as
separate states.

Bind native overflow semantics to the exact release binary and build. Bind
production impact to the actual feature/amendment state and validator cohort.
An isolated standalone replay is strong evidence for that artifact but is not
automatically mainnet or multi-node consensus proof. Never run value-creating,
fund-moving, consensus-splitting, or high-load tests on a public network.

## Terminal-oracle hierarchy

Prefer, in order:

1. authoritative protected-state read-back tied to owned data;
2. vendor/challenge-generated unpredictable token bound to the tested run;
3. researcher-owned out-of-band callback with unique nonce and controls;
4. deterministic harmless local effect on the exact release path;
5. bounded timing effect with randomized order, multiple delay values, jitter
   baseline, invalid-signature/control requests, and an explicit DoS-safe budget.

Timing alone is weaker and must not be used where the program forbids latency
effects or where ordinary endpoint variance explains the result.

## Evidence and reporting contract

The final evidence bundle should contain:

- scope/policy snapshot and submission-time eligibility;
- exact asset, release, deployment, and environment mapping;
- representation and authority ledgers;
- source-to-sink and state-transition graphs;
- immutable artifact hashes and redaction policy;
- baseline, positive case, and one-variable negative controls;
- deterministic validator identity and output;
- independent reproduction or authoritative read-back;
- attempt/reliability ledger;
- cleanup and containment state;
- prior-art and duplicate timeline;
- technical validity, severity, report readiness, and reward eligibility as
  separate decisions.

Recommended remediation for the client-state family is layered: rotate exposed
credentials and derived sessions, separate signing/encryption secrets from
OAuth or other credentials, keep sensitive flow objects server-side behind
opaque references, and replace executable/object serialization at client
boundaries with schema-validated data-only formats. These controls explain the
root cause but do not substitute for proof.

## Kill and blocked states

- `KILL_NO_CAPABILITY_DELTA`: the same actor already has an equivalent intended
  path to the claimed effect.
- `KILL_KNOWN_OR_DUPLICATE`: the exact public/fixed root is being replayed
  without a distinct current-release path.
- `KILL_ENVIRONMENT_MISMATCH`: local topology omits a material production
  layer or consumer.
- `BLOCKED_MISSING_TERMINAL_ORACLE`: intermediate markers exist but the
  protected effect is not proven.
- `BLOCKED_PASSIVE_ANALYSIS_ONLY`: model review found a lead but no authorized
  manual validation exists.
- `BLOCKED_CREDENTIAL_USE_NOT_AUTHORIZED`: offline exposure is proven but live
  replay is outside the permitted method.
- `BLOCKED_CHAIN_EDGE`: identity, environment, privilege, state, or byte
  continuity between two stages is missing.

Public case-study similarity can select a falsifier or reference. It cannot by
itself establish a new finding.
