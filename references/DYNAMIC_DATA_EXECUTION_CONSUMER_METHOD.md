# Dynamic Data to Execution Consumer Method

`DYNAMIC_DATA_EXECUTION_CONSUMER:v1`

## Purpose

Use this method when attacker-controlled structured data can acquire control
semantics before a protocol serializer, cache, model, background worker,
interpreter, renderer, or process API consumes it.

The method generalizes three public, fixed GitLab lineages:

1. recursive API-resource objects whose attacker-selected property names can
   shadow language methods used by a downstream wire serializer;
2. import metadata that survives broad attribute transformation, becomes
   persistent execution-adjacent state, and later reaches a shell-bearing
   worker; and
3. an optional runtime dependency whose presence silently enables an
   interpreter extension with an ineffective sandbox.

These cases are prior art and regression material. They are not new findings,
payload templates, or authorization to test live imports, Redis, sessions,
renderers, workers, or third-party services.

## Public and fixed prior art

| Historical lineage | Reusable invariant | Novelty status |
|---|---|---|
| HackerOne `#1679624` / GitLab issue `#371884`, fixed in GitLab 15.3.2 | A data object must not control language methods such as string conversion or byte length when a protocol client frames bytes. The length and payload must derive from one immutable primitive byte buffer. | `PUBLIC / FIXED / DUPLICATE` |
| HackerOne `#1609965` / GitLab issue `#366088` / `CVE-2022-2185`, fixed in GitLab 15.1.1 | Remote import metadata must be projected through an allowlist before model construction, persistence, queueing, and process use. A path value must never be interpolated into a shell command string. | `PUBLIC / FIXED / DUPLICATE` |
| HackerOne `#1401444` / GitLab issue `#345892` / merge request `!76174`, fixed in GitLab 14.7 | Optional dependency presence is not an authorization decision. It must not silently enable an interpreter or unsafe extension; explicit configuration and a defensible capability boundary are required. | `PUBLIC / FIXED / DUPLICATE` |

The earlier GitHub-import `CVE-2022-2884` family is relevant prior art for
patch-variant review. A fix at one data-to-protocol call site does not prove that
every sibling consumer normalizes the dynamic object.

## Unified theorem

Use this chain grammar:

`attacker-controlled structured input -> dynamic/object representation -> method, attribute, or feature-control surface -> persistence/protocol/worker transition -> authority-bearing consumer -> intermediate protected effect -> separately proven terminal impact`

The protected invariant is:

> Untrusted data must remain data. It must not select language methods, wire
> framing, model attributes, feature activation, interpreter availability, or
> executable grammar merely because a library converted it into a richer
> object or because an optional dependency is present.

Before `KILL`, prove all applicable parts:

1. the untrusted representation is converted to a primitive data-only form;
2. the protocol length and exact transmitted bytes derive from the same
   immutable buffer;
3. only explicitly permitted model attributes survive every transformer and
   are revalidated before persistence and queue consumption;
4. process invocation preserves argv/data separation and does not invoke a
   shell parser over attacker-controlled text;
5. optional interpreter/extension activation is explicit, fail-closed, and
   independent of ambient dependency availability;
6. the sandbox or capability boundary covers nested loaders, globals, host
   objects, callbacks, and I/O/process facilities; and
7. every claimed terminal edge is independently evidenced.

Incomplete evidence stays `HYPOTHESIS / NEEDS_EXECUTION_CONSUMER_PROOF`.

## Family A — Dynamic object methods become protocol control

### High-value shape

`remote JSON/map -> recursive resource/object wrapper -> attacker-named methods -> serializer calls coercion/length/hash methods -> framing disagreement -> injected protocol operation`

### Method-surface inventory

Do not search only for one historical method name. Inventory every method a
downstream component invokes implicitly or explicitly:

| Surface | Examples to inspect | Security question |
|---|---|---|
| Text conversion | string conversion, interpolation, format hooks | Can attacker data replace the conversion method or its return type? |
| Length/framing | byte length, character length, size, iterator count | Is the declared length computed from the same immutable bytes that are sent? |
| Collection identity | hash, equality, key conversion, symbol conversion | Can attacker-controlled semantics alter cache keys or memoization? |
| Serialization hooks | JSON/YAML/Marshal-style conversion, encode/decode callbacks | Does a rich object select executable or protocol behavior? |
| Dynamic dispatch | missing-method hooks, property accessors, proxies | Can a remote field name collide with inherited or built-in methods? |

Record recursively nested objects. A top-level primitive does not prove nested
fields are primitive.

### Mandatory wire-framing matrix

| Stage | Object/value type | Conversion method | Length source | Bytes source | Mutable between steps? | Evidence |
|---|---|---|---|---|---|---|
| API response parse | | | | | | |
| domain/import object | | | | | | |
| cache/protocol argument | | | | | | |
| serialized frame | | | | | | |
| socket/mock capture | | | | | | |

The safe invariant is not merely “call string conversion.” The implementation
must first materialize one primitive byte buffer, compute its length from that
buffer, and transmit that same buffer without consulting attacker-influenced
methods again.

### Impact separation

Keep these edges independent:

1. remote field controls a method surface;
2. method surface changes framing bytes;
3. an extra protocol operation is accepted;
4. a protected key/object/state can be modified;
5. an application consumer reads that state;
6. a deserializer actually processes the attacker-selected representation;
7. a compatible gadget or protected action exists in the shipped runtime;
8. a harmless terminal marker proves the final execution context.

A source trace to a protocol serializer is not command injection. A captured
framing discrepancy is not a session write. A protected cache mutation is not
deserialization. Deserialization is not automatically code execution.

## Family B — Import metadata becomes delayed execution state

### High-value shape

`remote import metadata -> denylist/broad transformation -> model/service mass assignment -> stored execution-adjacent attribute -> queue/retry/template transition -> shell-bearing helper -> worker-process effect`

### Attribute-provenance table

| Attribute | Remote source | Transformer action | Model setter/callback | Persisted value | Queue/job field | Final consumer | Allowed by design? |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Audit both direct assignment and indirect path selection:

- template, sample, migration, overwrite, compatibility, or retry branches;
- type/source fields that change which importer runs;
- controller versus API enforcement of source types and feature flags;
- default-off features reachable through alternate routes or direct values;
- time-delayed consumers after retry exhaustion or missing-file fallbacks;
- model callbacks and services that rewrite one field while preserving another.

A denylist of obviously dangerous names is not equivalent to a minimal
allowlist of business fields. Revalidate at the authoritative service/model and
again before an execution-bearing worker consumes stored state.

### Command-consumer invariant

Use a process API with an explicit executable and argv array, or pipe data to a
fixed process through stdin. Do not assemble a command string containing an
untrusted path, URL, archive name, import source, project attribute, or option.

Inspect wrappers rather than trusting API names. Determine whether the runtime
invokes a shell for string arguments, how options are separated, which working
directory/environment is inherited, and whether an option-like value can alter
the fixed command.

### Asynchronous reachability

Prove:

1. the exact entry route accepts the remote metadata;
2. the attacker's starting role may create the import object;
3. the value survives transformation and authoritative persistence;
4. the relevant job is scheduled in the affected configuration;
5. retries, feature gates, and missing-file behavior reach the consumer;
6. the worker uses the stored attacker value;
7. the harmless effect occurs under the worker identity; and
8. cleanup restores and removes only researcher-owned state.

An enabled UI flag is not the only gate. Compare controllers, API versions,
source-type parameters, direct endpoints, workers, and default configuration.

## Family C — Optional dependency silently enables an interpreter

### High-value shape

`attacker-authored content -> renderer/parser -> optional extension auto-loads when dependency resolves -> nominal sandbox -> nested loader/global/host capability escapes -> interpreter or process effect`

### Activation matrix

| State | Dependency/package present | Explicit feature config | Extension registered | Untrusted content reaches it | Protected effect | Verdict evidence |
|---|---|---|---|---|---|---|
| Shipped default | | | | | | |
| Supported optional install | | | | | | |
| Source/shared-runtime install | | | | | | |
| Dependency absent | | | | | | |
| Explicitly disabled | | | | | | |
| Patched release | | | | | | |

Dependency resolution must not serve as a security policy. Require explicit
configuration owned by an authorized administrator, a safe default, and a
clear capability boundary.

### Sandbox completeness review

Inventory:

- dynamic loaders, compilation, evaluation, includes, and nested interpreters;
- global environment and realm selection;
- mutable intrinsics, prototypes, modules, callbacks, and shared state;
- host objects, filesystem, network, environment, process, and FFI access;
- error/fallback behavior and callbacks created outside the sandbox;
- runtime and dependency version assumptions.

Do not call a path release-reachable merely because a package can be manually
installed. Record whether the dependency is in the official artifact, lockfile,
supported optional configuration, shared runtime, or only a hypothetical local
customization. A configuration-dependent vulnerability may still be valid, but
its affected population and severity must be bounded to the proven state.

## Mandatory execution-consumer KILL challenge

Before KILLing a candidate in any of these families, answer:

1. What exact attacker-controlled representation enters?
2. Does it become a dynamic object, model attribute, stored job value, or
   extension/interpreter input?
3. Which method names, coercions, attributes, feature states, or dependency
   states can influence control semantics?
4. Is data normalized to a primitive before the protocol/interpreter/process
   boundary?
5. Do framing length and transmitted bytes derive from the same immutable
   buffer?
6. Does a strict allowlist close every alternate transformer, service, model,
   queue, retry, and worker path?
7. Is optional execution functionality explicitly enabled and fail-closed?
8. Which exact authority-bearing consumer runs, under what identity?
9. What intermediate effect is proven, and what terminal edge is still only an
   assumption?
10. Do baseline, closest one-variable sibling, negative control, patched
    control, authoritative read-back, and cleanup agree?

`Looks like ordinary data`, `the feature is optional`, `the flag is normally
off`, `the dependency is not bundled`, `the API coerces to a string`, or `the
process call is wrapped` is not enough without the corresponding end-to-end
evidence.

## Safe proof ladder

- **E0 — resemblance:** dynamic methods, mass assignment, string command, or
  optional interpreter exists in source.
- **E1 — attacker control:** realistic attacker input reaches the released
  entrypoint and exact representation.
- **E2 — control semantics:** a method/attribute/feature/dependency state is
  shown to alter the downstream interpretation.
- **E3 — intermediate boundary:** a mock wire capture, stored-state read-back,
  or sandbox capability canary proves the first protected effect.
- **E4 — authority-bearing consumer:** the real protocol client, worker, or
  renderer consumes it under the claimed identity.
- **E5 — terminal edge:** a separate harmless canary proves the terminal
  deserializer/interpreter/process effect.
- **E6 — controls:** baseline, closest sibling, negative control, patched
  control, and authoritative read-back all match the hypothesis.
- **E7 — release and novelty:** affected artifact/configuration, prior art,
  cleanup, reproducibility, and current distinct lineage are complete.

Do not label RCE below E5. An intermediate integrity primitive may be retained
at its proven impact level, but it cannot inherit the terminal claim.

## Safe verification rules

- Prefer pure unit tests, a mock serializer/socket capture, fake queue, and
  temporary researcher-owned state.
- Use only inert fixed markers in an isolated local fixture when execution
  context must be proven.
- Keep network access loopback-only and concurrency one unless the authorized
  task requires otherwise.
- Never write an operational Redis/session injection payload, deserialization
  gadget, shell command, reverse shell, persistence mechanism, or public import
  into package regression fixtures.
- Never install optional runtime dependencies into a real target to create the
  prerequisite being claimed.
- Stop on third-party data, service instability, unexpected privileged state,
  or scope drift.

## Closest one-variable controls

Use the control closest to the suspected broken invariant:

- dynamic wrapper versus the same value flattened to a primitive;
- mismatched framing sources versus one immutable byte buffer;
- broad project attributes versus a strict business-field allowlist;
- shell-bearing string versus fixed executable and argv/data separation;
- feature-gated UI versus the same direct/API source type;
- optional dependency present versus absent;
- ambient auto-enable versus explicit disabled state;
- unsafe nested loader versus the same interpreter with loader/host capability
  removed;
- vulnerable release versus the fixed release.

Change one variable at a time and capture the authoritative state, not only an
exception or HTTP status.

## Immediate invalidation rules

KILL when complete evidence proves any applicable condition:

- attacker input is flattened to a data-only primitive before any method or
  protocol consumer;
- one immutable byte buffer supplies both frame length and transmitted bytes;
- strict attribute allowlists and authoritative service/model checks prevent
  execution-adjacent state from being stored;
- the process API receives a fixed executable and argv/data values without a
  shell or option confusion;
- the alternate route/source type is rejected before object creation;
- the optional dependency is absent from every relevant released/supported
  configuration and no current eligible deployment path exists;
- interpreter functionality requires explicit trusted enablement, is disabled
  by default, and remains unreachable from the attacker role;
- a real capability-secure sandbox blocks the required loader/host effect;
- only the already public/fixed GitLab lineage is present;
- the terminal claim depends on an unproven state consumer, gadget, runtime, or
  invented edge.

If evidence is incomplete, use `NEEDS_EXECUTION_CONSUMER_PROOF`, not KILL.

## Fix directions

- recursively convert remote resources to schema-validated data-only
  primitives before business or protocol use;
- reserve or reject property names that collide with runtime methods, but do
  not rely on a finite name blacklist as the primary boundary;
- serialize once to immutable bytes and derive framing metadata from those
  exact bytes;
- use minimal positive attribute allowlists at every import boundary;
- revalidate stored state before asynchronous execution-bearing use;
- use fixed executable plus argv/stdin, never a shell command string;
- enforce feature/source-type policy at every controller/API entry and at the
  authoritative service;
- require explicit administrator configuration for interpreter extensions;
- remove unsafe interpreter features or isolate them in a capability-secure
  process with no host I/O/process authority;
- regression-test nested dynamic objects, method-name collisions, alternate
  routes, retries, dependency-present/absent states, and fixed releases.

## Required handoff

- Verdict and manual status
- Public-prior-art or distinct-current-lineage result
- Attacker and server conditions
- Exact structured input and representation transitions
- Dynamic method/attribute/feature/dependency surface
- Primitive normalization and framing identity
- Persistence/queue/worker trace
- Execution consumer and process authority
- Intermediate effect versus terminal impact edge
- Baseline, closest sibling, negative and patched controls
- Authoritative read-back and cleanup
- `kill_permitted` plus blockers

Only `STRONG + MANUALLY_CONFIRMED` is report-ready. The exact historical cases
above remain `KILL / PUBLIC / FIXED / DUPLICATE` for novelty.

