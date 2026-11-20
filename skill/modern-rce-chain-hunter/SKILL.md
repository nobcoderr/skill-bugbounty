---
name: modern-rce-chain-hunter
description: "Expert authorized source-code and product-security workflow for discovering multi-stage RCE chains derived from modern public incidents: cross-service parser mismatch, validation/use desynchronization, cache/object poisoning, dynamic resolver abuse, sandbox context escape, filesystem semantic differential, arbitrary-write-to-privileged-consumer, browser-to-native chaining, and release-reachable memory corruption. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Expert Modern RCE Chain Hunter

Use this skill for **authorized, in-scope, release-reachable RCE research** across server applications, frameworks, APIs, desktop clients, developer tools, package ecosystems, privileged services, and native protocol parsers.

This skill turns public RCE history into **searchable invariants and safe verification plans**. It is not a payload library. Do not reproduce public exploits against third parties, do not generate reverse shells or persistence, and do not call pattern similarity a finding.

Mandatory companion material:

- `references/MODERN_RCE_CHAIN_ATLAS_2026.md`
- `references/EXPERT_SCOPE_REACHABILITY_CHECKLIST.md`
- `references/EXPERT_TEST_DESIGN_MATRIX.md`
- `references/EXECUTABLE_RCE_EVIDENCE_WORKSHEET.md`
- `references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md` when remote data can
  define dynamic methods/coercions, protocol framing, persistent import
  attributes, feature activation, or optional interpreter availability
- `skill/dynamic-filter-evaluator-rce-hunter/SKILL.md` and its
  `references/dynamic-filter-evaluator-rce-method.md` when an API filter or
  query DSL can select executable operator semantics
- `skill/cross-language-script-injection-hunter/SKILL.md` and its method when
  one runtime interpolates untrusted values into generated source executed by
  another runtime
- `skill/patch-diff-root-cause-analyzer/SKILL.md`
- the runtime-specific language skill for the target

## Hard operating contract

Retain a candidate only when every relevant gate survives:

1. **Scope and authorization:** the exact product, component, version, vulnerability class, testing method, and account capability are allowed.
2. **Release reality:** the path is present in the stable/released/deployed artifact and reachable in realistic configuration.
3. **Attacker capability:** identify what the attacker can actually supply, mutate, host, upload, push, configure, or cause the victim to open.
4. **Representation identity:** prove what bytes/object/path/route were validated, and whether the same representation is later used.
5. **Boundary:** identify the trust, privilege, sandbox, tenant, integrity, or execution boundary crossed.
6. **Primitive:** prove a controlled execution primitive or the exact preceding primitive required by the program. A dangerous sink, error, or crash alone is not RCE.
7. **Safe evidence:** use researcher-owned infrastructure, benign markers, baseline, negative control, state before/after, and cleanup.
8. **Runtime matrix:** state OS, runtime, loader/classloader, module mode, allocator, server model, privilege, feature flags, and mitigations required by the chain.
9. **Prior art:** search advisories, issues, PRs, commits, release notes, changelog, vendor docs, public security research, and duplicate root-cause families.
10. **Aggressive falsification:** seek upstream/downstream checks, trusted-by-design assumptions, equal-privilege prerequisites, default-off features, non-production paths, and mitigation blockers.

If scope, release reachability, primitive, boundary, or novelty fails, mark **KILL**.

## RCE chain theorem

A valid modern RCE normally has more than one stage:

`attacker capability -> controllable representation -> missing/misplaced invariant -> primitive -> trusted consumer or privilege transition -> execution context -> concrete impact`

For every candidate, explicitly separate:

- **trigger:** how attacker data enters;
- **confusion:** where components disagree or validation applies to the wrong object;
- **primitive:** SQLi, object fabrication, arbitrary write, dynamic resolution, unsafe eval, XSS, memory corruption, or privileged API access;
- **gadget/consumer:** hook loader, cache hydration, build engine, browser/native bridge, scheduler, web root, classloader, log rotation, protocol handler, or cleanup callback;
- **execution:** harmless controlled effect in the victim/trusted context;
- **impact:** the protected boundary actually crossed.

Do not collapse the entire chain into “input reaches exec.”

## Priority pattern families

### 1. Cross-service metadata or delimiter injection

Look for user-controlled values embedded into an internal header, RPC metadata blob, environment block, hook configuration, or delimiter-separated record. Compare producer and consumer rules for escaping, duplicate fields, unknown fields, first/last-wins behavior, type coercion, and key normalization.

High-value shape:

`user field -> serializer without unambiguous encoding -> internal parser -> duplicate/synthetic privileged key -> hook/path/command option override`

### 2. Validation/use desynchronization

Look for parallel arrays, separately filtered lists, index maps, batched routes, request/result tuples, and loops that `continue` or drop one element without inserting a placeholder. Prove whether request N is validated against policy N but executed as handler N+1.

High-value shape:

`malformed earlier element -> list/index drift -> validation for object A -> execution of object B`

### 3. Primitive-to-state poisoning

Do not stop at read-only SQLi, object injection, or deserialization. Trace whether attacker-controlled query results are hydrated into trusted domain objects, cached, written back, used by authorization, or passed through lifecycle callbacks.

High-value shape:

`query/control primitive -> fabricated trusted object -> cache/session/state -> privileged writeback/gadget -> role/code execution`

### 4. Caller override of trusted stored definition

Compare public/shared/template/build endpoints that should execute server-owned definitions with parameters that allow callers to supply replacement graphs, components, templates, code, workflow steps, or serialized objects.

High-value shape:

`public object ID + attacker replacement definition -> trusted build/evaluation path -> exec/import/template callback`

### 5. Dynamic resolver and living-off-the-land gadget

Trace attacker control over module path, class name, package, export symbol, template helper, script include, plugin identifier, protocol handler, or reflection target. A checksum of attacker input is not an allowlist.

High-value shape:

`deserialized resolver descriptor -> dynamic import/require/class load -> callable export/initializer -> execution`

Require a runtime-specific reachability matrix; do not assume a gadget works in all module modes or loaders.

### 6. Sandbox or realm/context transition

Search for helpers that evaluate code in a different realm, security domain, classloader, global object, script include, callback, or prototype context. Track global mutation, function clobbering, constructor recovery, host object exposure, and callbacks created outside the sandbox.

High-value shape:

`sandboxed expression -> cross-context include/helper -> attacker-influenced global/callback -> unsandboxed function creation or privileged host operation`

### 7. Filesystem semantic differential

Model the target filesystem rather than only the development OS. Test path separators, alternate data streams, 8.3 aliases, reserved device names, case folding, trailing dots/spaces, Unicode normalization, symlinks, junctions, archive members, and configuration-key mistakes that silently disable protection.

High-value shape:

`repository/archive path valid on producer OS -> different decomposition on victim OS -> protected-directory write or traversal -> automatic hook/load`

### 8. Resource lookup before rejection

Inspect validators and deserializers that perform DNS, URL, JAR, classpath, schema, plugin, or resource lookup **before** deciding the type/object is prohibited. Side effects can create SSRF, downloaded artifacts, cache entries, open descriptors, or loader-visible state usable by a second request.

High-value shape:

`rejected type -> pre-rejection lookup side effect -> persistent/open resource -> second-stage resolver -> load/execute`

### 9. Arbitrary write to privileged consumer

After finding file write or path traversal, enumerate all consumers of the destination and suffix constraints. Search web roots, hook directories, plugin discovery, cron/task folders, config include globs, log rotation, package loaders, startup/repair/update paths, and service restarts.

High-value shape:

`low-priv input/fetch/archive -> controlled path/content -> privileged periodic/automatic parser -> command/script/module execution`

### 10. Browser or stored-XSS to privileged native/server API

When XSS exists in an administrative or desktop origin, enumerate same-origin APIs, CSRF/token access, local/native bridges, PowerShell/process endpoints, configuration writers, plugin uploaders, and web-root writers. Require realistic victim interaction and an allowed class.

High-value shape:

`attacker content -> trusted-origin script -> privileged API/token/native bridge -> controlled file/process capability`

For WordPress-like plugin upload, do not infer execution from archive upload,
successful extraction, plugin discovery, or activation state. Prove the exact
destination, served URL, web-server handler, filesystem permission, and direct
execution of an inert canary. Some deployments execute a directly requested
PHP file without plugin activation; others block direct PHP or file
modification. Load the XSS2Shell seven-boundary reference for
`CVE-2026-64638`-shaped paths and preserve active administrator interaction.

### 11. Attacker-selected backend rendered in trusted origin

Desktop/admin clients may accept a gateway/base URL and then render remote error text, auth challenges, or HTML inside a trusted origin. Track backend selection, TLS trust, response parsing, HTML sinks, local storage, and privileged API access.

### 12. OS protocol-handler execution

Audit Markdown/HTML/document links, custom URI schemes, `ShellExecute`, `Process.Start`, deep links, app installers, file associations, and registered handlers. An allowlist must cover the **resolved execution semantics**, not just string appearance.

### 13. Protocol lifecycle and cleanup memory corruption

For native servers and parsers, map state transitions and object ownership across reset, abort, retry, error, timeout, and cleanup callbacks. Search duplicate queue insertion, double cleanup registration, refcount imbalance, stale callback pointers, and allocator-specific reuse.

High-value shape:

`remote lifecycle sequence -> same object queued/freed twice -> controlled reuse/callback -> release-context impact`

A crash remains **WEAK** until a reliable primitive and in-scope impact are proven.

### 14. Low-privileged configuration as a code pipeline

Treat URLs, aliases, import sources, hook paths, templates, repository options, and administrative “configuration” fields as code-adjacent inputs when a root/service process later fetches or interprets them. Map the entire scheduled pipeline.

### 15. Open filter/query object to executable evaluator

Audit GraphQL JSON scalars, REST filter maps, and Mongo-like query DSLs that are
passed to generic predicate libraries. Prove the exact operator set, runtime
gate, eligible principal, deterministic non-empty input, predicate invocation,
and server execution context. Route the detailed workflow through
`dynamic-filter-evaluator-rce-hunter`; do not treat GraphQL, JSON, a dependency,
or `new Function` alone as RCE.

### 16. Cross-language generated-script injection

Audit Ruby heredocs, string templates, temporary scripts, browser-automation
wrappers, and other emit-then-execute flows. Trace the value through its
source-language validator into the exact target-language lexical context, the
complete emitted artifact, the interpreter invocation, and child-process
authority. Route the detailed workflow through
`cross-language-script-injection-hunter`.

High-value shape:

`attacker value -> semantic validator -> textual interpolation into generated source -> target parser treats data as syntax -> child runtime executes with application authority`

Do not equate URL/selector/path validation with target-language encoding, or a
route namespace with authorization. Prefer a typed data channel and static
source over manual quote escaping.

### 17. Dynamic data to protocol, worker, or interpreter control

Audit recursive resource wrappers that create methods from remote field names,
protocol clients that compute framing metadata through one method and bytes
through another, import pipelines that persist broad remote attributes before
an asynchronous process consumer, and optional dependencies that silently
enable interpreter-bearing extensions.

High-value shapes:

`remote object -> attacker-selected method/coercion -> protocol framing drift -> protected state -> separately proven terminal consumer`

`remote import metadata -> broad attribute projection -> persisted/queued path -> shell-bearing worker -> inert canary`

`untrusted content -> dependency-presence auto-enable -> nominal sandbox -> host/interpreter capability -> inert canary`

Load `references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md`. Do not inherit RCE
from a protocol injection, state mutation, dependency presence, or sandbox
theory. Prove every terminal edge independently and preserve configuration-
dependent reachability accurately.

<!-- DYNAMIC_DATA_EXECUTION_CONSUMER:v1 -->

Load `references/ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md` when a renderer
option selects a class/constructor/loader, upload markup activates a secondary
resource loader, or a filesystem object reaches a later execution consumer.
Use inert constructor/loader spies; do not start from commands. RCE remains
unproven until the terminal process/interpreter edge is independently observed.

<!-- ARCHIVE_RENDERER_FRAMEWORK_CONSUMER:v1 -->

## Mandatory two-way workflow

### Phase 0 — Scope, release, and prior-art gate

Record:

- program and eligible class;
- exact repo/component/package/product;
- stable version, commit/tag, build artifact, platform, architecture;
- production or default configuration evidence;
- attacker account/role and victim interaction;
- public advisory/fix/duplicate family;
- known exclusions and unsafe testing restrictions.

KILL before deep work if the real consumer cannot be proven.

### Phase 1 — Component interpretation map

For every transition, create a table:

| Stage | Component | Input representation | Decode/normalize rules | Duplicate/error behavior | Trust assumption | Output representation |
|---|---|---|---|---|---|---|

Include clients, proxies, serializers, databases, caches, workers, loaders, operating systems, and privileged consumers.

### Phase 2 — Forward trace from attacker inputs

Enumerate attacker-controlled:

- fields, headers, routes, batch entries, files, archives, repository objects;
- URLs, gateways, redirects, schemas, class/module/export names;
- flow/workflow/component definitions;
- low-privileged configuration and remote content;
- protocol state transitions, reset/abort timing, lengths, indexes, and ownership events.

Trace every transformation until the value is rejected, neutralized, stored, or reaches a sensitive primitive.

### Phase 3 — Backward trace from high-value consumers

Start from:

- `exec`, `eval`, template/script engines, reflection, dynamic imports, classloaders;
- process creation, protocol handlers, shell/interpreter wrappers;
- privileged file writes, web roots, hook/plugin/config directories;
- cache hydration, session/user/role construction, writeback callbacks;
- cleanup callbacks, frees, object pools, refcounts, function pointers;
- native/desktop bridges and administrative APIs.

Walk backward through all callers and policy assumptions until attacker control is proven or the lead dies.

### Phase 4 — Validation/use identity check

Answer explicitly:

- Which exact object, index, route, path, bytes, class, host, or definition was validated?
- Which exact object was executed, loaded, cached, or written?
- Can an error, filter, retry, redirect, normalization, hydration, or second request change identity between those points?
- Does authorization occur before or after canonicalization?
- Does the signature/hash cover the same representation and identity that the consumer uses?

### Phase 5 — Primitive augmentation

For a real primitive, enumerate only **local, in-scope, automatic** next consumers:

- SQL/control result -> object hydration/cache/writeback;
- XSS -> same-origin privileged API/native bridge;
- file write -> automatic loader/scheduler/config parser;
- SSRF/resource fetch -> cached/open artifact -> loader;
- dynamic import -> callable export/initializer;
- memory corruption -> object reuse/callback control.

Do not invent a gadget. Confirm it exists in the shipped dependency/runtime graph.

### Phase 6 — Runtime and mitigation matrix

Record at minimum:

| Dimension | Tested/observed value | Required for chain? | Alternative behavior | Evidence |
|---|---|---|---|---|
| OS/filesystem | | | | |
| Runtime/version | | | | |
| Module/classloader mode | | | | |
| Server/worker model | | | | |
| Allocator/build flags | | | | |
| Process identity/privilege | | | | |
| Feature/default config | | | | |
| Sandbox/mitigations | | | | |

Downgrade broad claims when the primitive is runtime-specific.

### Phase 7 — Safe proof ladder

- **C0:** pattern resemblance only.
- **C1:** realistic attacker control reaches the shipped entrypoint.
- **C2:** validation/representation invariant is demonstrably broken.
- **C3:** intermediate primitive is safely proven.
- **C4:** benign controlled execution or equivalent control primitive is proven.
- **C5:** victim/privileged/sandbox boundary is proven with negative control.
- **C6:** exact stable/default path, concrete impact, prior-art check, cleanup, and reproducibility are complete.

Do not call a candidate RCE below C4. Normally require C5-C6 for **STRONG**.

Allowed proof methods include harmless marker files in researcher-owned temporary directories, deterministic test callbacks, loopback listeners, mock gateways, test-only accounts/objects, debugger/sanitizer evidence, and isolated VMs. Never use persistence, credential access, public malicious packages, third-party data, or destructive effects.

### Phase 8 — Variant and duplicate analysis

For public fixes, search:

- sibling endpoints, alternate API versions, batch vs single routes;
- duplicate serializers/parsers in another language/service;
- compatibility/fallback/error paths;
- platform-specific implementations;
- stored-definition path vs caller-supplied override;
- other destinations consumed by the same privileged loader;
- partial patches that reject one token but not the semantic class;
- configuration keys that are read under the wrong name or scope;
- newer releases that reintroduced equivalent behavior.

A public PoC on the same root cause is **KILL** for novelty unless a distinct current path, patch bypass, sibling implementation, or separate boundary is proven.

Keep WordPress XSS2Shell (`CVE-2026-64638`) separate from WP2Shell
(`CVE-2026-63030` plus `CVE-2026-60137`). Different entry primitives, fixed
releases, and backport ranges must not be merged into one lineage.

## Code-search heuristics

Use runtime-aware searches as hypothesis generators, then read callers and callees.

### Structured metadata and parser mismatch

Search for:

- manual `join`/`split` on `;`, `,`, `:` or newline for internal records;
- duplicate keys assigned into maps without rejection;
- unknown fields preserved across trust boundaries;
- `first`, `last`, overwrite, merge, append, or case-normalized key behavior;
- user input copied into `X-*` headers, RPC metadata, environment blocks, hook options, or worker messages.

### Alignment and batching

Search for:

- multiple arrays/lists indexed by the same integer;
- `continue`, `filter`, exception handling, or early return in only one list-building path;
- `zip`, `enumerate`, positional joins, route/result arrays, and separate validation/execution loops;
- placeholder insertion on success but not failure;
- cached match/permission result reused after request mutation.

### Trusted definition override and evaluators

Search for public/shared endpoints with parameters named like:

- `data`, `graph`, `flow`, `definition`, `component`, `template`, `script`, `code`, `expression`, `module`, `class`, `export`, `plugin`, `handler`;
- stored object ID plus optional caller-supplied replacement;
- dynamic `exec`/`eval`/compile/import/require/reflection/template callbacks;
- build/preview/validate endpoints sharing execution helpers.

### State and object poisoning

Search for:

- raw query fragments and scalar/list coercion;
- ORM/domain object construction from query rows;
- object cache, session, identity map, memoization, or distributed cache writes;
- lazy loaders, save hooks, writeback, post-load callbacks, and role/user hydration;
- authorization based on cached mutable objects.

### Arbitrary write and consumers

Search for:

- remote fetch/import followed by filename construction;
- archive/CSV/manifest fields used in paths;
- suffix/prefix constraints that still land in config include or web roots;
- wildcard include directories, hook/plugin loaders, scheduled jobs, log rotation, startup/repair/update logic;
- privileged processes reading low-privileged writable directories.

### Filesystem and desktop execution

Search for:

- custom path validators that ignore platform semantics;
- backslash/colon/short-name/reserved-name handling;
- `ShellExecute`, `Process.Start`, URL openers, custom protocols, deep links, file associations;
- rendering of backend error text or auth challenges into HTML;
- local storage of privileged tokens accessible to rendered content.

### Native lifecycle

Search for:

- the same object appended to cleanup/free queues from multiple callbacks;
- reset/abort/error paths sharing ownership;
- refcount decrement in both caller and callback;
- callback/function pointer storage in pool-managed objects;
- feature/version-specific ownership changes visible in patch diffs.

## Immediate invalidation rules

Mark **KILL** when any of these applies:

- only a keyword/sink resemblance exists;
- attacker already has equal or higher code execution;
- privileged user explicitly and knowingly installs arbitrary code by design;
- file write has no automatic trusted consumer;
- XSS cannot reach a privileged same-origin/native capability and the program excludes it;
- dynamic resolution is restricted to an immutable generated registry;
- dynamic API objects are recursively flattened before protocol use, framing
  length and bytes share one immutable buffer, strict import-field allowlists
  close delayed consumers, or optional interpreters are absent/explicitly
  disabled and fail-closed on every relevant release path;
- the runtime/configuration needed is absent from stable deployments;
- the “different object” is actually revalidated after normalization;
- memory issue is only a crash with no controlled primitive;
- the same root cause and path are already public/fixed/known/duplicate;
- impact depends on another unproven vulnerability or invented gadget.

## Required output

Start with a candidate board:

| Candidate | Pattern family | Verdict | Release reachability | Attacker capability | Broken invariant | Primitive | Boundary | Evidence C0-C6 | Duplicate risk |
|---|---|---|---|---|---|---|---|---|---|

For each candidate provide:

- Verdict: STRONG / MEDIUM / WEAK / KILL
- Pattern family and public prior-art family:
- Scope and exact release proof:
- Attacker capability and required victim action:
- Component interpretation map:
- Forward and backward trace:
- Validated representation versus used representation:
- Missing invariant:
- Intermediate primitive:
- Confirmed gadget/consumer:
- Execution context and privilege:
- Concrete security impact:
- Runtime/mitigation matrix:
- Safe proof, baseline, and negative control:
- Evidence present and missing:
- Prior-art/duplicate result:
- Invalidation factors:
- Minimal fix direction and regression tests:
- Candidate status: VALID / INVALID / BLOCKED

If nothing survives, output exactly: **NO VALID FINDING**.

## Evidence-only boundary

Stop at technical candidate validation. Do not produce exploit release, reverse shell, persistence mechanism, stealth technique, or destructive payload.


<!-- MODEL_AGNOSTIC_RUNTIME:v1 -->
## Model-agnostic runtime

This skill binds to the local pack, not to Codex, OpenAI, Claude, Grok,
Gemini, or any other vendor. The current session's model is the operator.
Do not skip, defer, or weaken this skill because the product is Cursor,
Claude Code, Gemini, Codex CLI, or another runtime.
`agents/openai.yaml` is optional Codex UI metadata only.
<!-- END_MODEL_AGNOSTIC_RUNTIME -->

<!-- AUTHORIZED_OFFENSIVE_POSTURE:v1 -->
## Authorized offensive-first posture

For every explicitly authorized security task, prioritize adversary emulation:
`attacker objective -> reachable entrypoint -> exploit chain -> privilege or authority transition -> protected sink -> concrete impact`. Search for attack paths, bypasses, escalation, code execution, cross-tenant access, credential or data exposure, signing or supply-chain compromise, and fund or integrity impact supported by the target. Use defensive controls, detection, remediation, and hardening primarily as falsifiers or post-proof guidance unless the user explicitly requests blue-team work. Do not force a vulnerability class unsupported by target evidence. This posture never expands authorization: preserve exact scope, safe harbor, harmless proof, rate limits, stop conditions, cleanup, and prohibitions on destructive, stealthy, credential-stealing, persistence, evasion, or third-party activity.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->

## File or DOM primitive to terminal execution

Load `references/PATH_CLI_GADGET_CHAIN_METHOD.md` when an RCE hypothesis begins
with path escape, file read/write/truncation, child option grammar, or a shipped
DOM gadget. Prove the primitive first, then independently prove secret or
capability acquisition, signing/authentication acceptance, serializer or
gadget activation, process authority, environment compatibility, and the final
canary. Without every edge, retain the narrower primitive and mark the RCE
claim `NEEDS_PATH_CLI_GADGET_PROOF`. Never reuse historical cookie,
deserialization, SSH, internal-API, XSS, or command payloads.

<!-- PATH_CLI_GADGET_CHAIN:v1 -->
## Mandatory automatic routing

This skill never operates as a silent standalone module. For every security-focused invocation:

1. ensure `mandatory-auto-router` is active;
2. evaluate all installed skills and supporting artifacts through `config/AUTO_ROUTING_MAP.json`;
3. apply this skill only when marked **ACTIVE**, while recording **DEFERRED** and **NOT_APPLICABLE** routes;
4. load this skill's mapped companion prompts, references, worksheets, and safety protocols;
5. rerun routing after material discoveries that change language, runtime, platform, trust boundary, sink, release reachability, or prior art;
6. never auto-execute operational automation without explicit authorization and safety controls.

If the router is already active, acknowledge the existing routing session and do not recursively bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
