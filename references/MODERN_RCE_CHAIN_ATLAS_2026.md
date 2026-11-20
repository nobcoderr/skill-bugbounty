# Modern Multi-Stage RCE Pattern Atlas — 2026

## Purpose

This reference distills public RCE research into reusable **authorized offensive
attack-path invariants, code shapes, search questions, falsifiers, and safe
proof designs**. It must be used together with
`skill/modern-rce-chain-hunter/SKILL.md`.

Public security research is prior art. A similar pattern is not a new finding. Retain a candidate only when the target has a distinct, in-scope, current, release-reachable root cause or an unpatched sibling/variant path with concrete security impact.

Do not copy public exploit payloads. Search for the broken invariant, then validate the target with harmless researcher-owned evidence.

## Universal extraction schema

For every historical case, capture:

`attacker capability -> controllable representation -> component disagreement or missing invariant -> intermediate primitive -> trusted consumer/gadget -> execution context -> impact`

Then ask:

1. What exact representation was authorized, signed, validated, or cached?
2. Was that exact representation later executed or consumed?
3. Which component silently changed identity, indexing, path semantics, trust, or execution context?
4. What runtime/deployment conditions were essential?
5. Which fix restored the invariant?
6. Which sibling paths may still omit the fix?

---

## Pattern 01 — Cross-service metadata injection into privileged execution options

**Historical family:** GitHub internal Git push/RPC RCE, reported as CVE-2026-3854 in the supplied research sources.

### Abstract chain

`user-controlled repository/protocol option -> delimiter-based internal serialization -> receiving parser accepts synthetic/duplicate privileged keys -> hook/path/environment option override -> trusted hook execution`

### Violated invariant

User-controlled fields must remain typed data and must never be reinterpreted as control-plane metadata. Producer and consumer must agree on escaping, field boundaries, duplicate handling, allowed keys, and value types.

### Search signatures

- internal headers or RPC metadata assembled with string concatenation;
- `join`/`split` using semicolon, comma, colon, newline, or NUL;
- maps where duplicate keys overwrite earlier trusted values;
- “last value wins” or merge behavior;
- user push options, labels, branch names, repository properties, or job inputs copied into internal control records;
- hook directories, environment names, executable paths, or feature flags carried beside user data.

### Questions

- Can a user value create an additional logical field after parsing?
- Are unknown keys accepted and forwarded?
- Does one service validate the original field while another acts on the parsed map?
- Are trusted defaults assigned before untrusted fields and then overwritten?

### Safe verification

Use a harmless synthetic metadata key and prove the receiver changes a non-executing test option or logs a distinct parsed field. Do not execute a hook until scope permits and a benign isolated canary is necessary.

### KILL conditions

- typed schema with length-prefixing and strict unknown-field rejection;
- duplicate privileged keys rejected before use;
- attacker cannot influence any field crossing the service boundary;
- path is internal-only and unreachable from an eligible attacker role.

### Fix pattern

Use typed serialization; separate untrusted data from privileged metadata; reject unknown/duplicate control keys; canonicalize once; authorize after parsing the final representation.

---

## Pattern 02 — Parallel-list or batch-route desynchronization

**Historical family:** WordPress WP2Shell chain, CVE-2026-63030 combined with CVE-2026-60137.

### Abstract chain

`malformed earlier batch element -> one derived list drops an entry -> indexes drift -> request B validated using route/policy A -> unsafe parameter reaches different handler -> SQL/control primitive`

### Violated invariant

The request, matched route, permission result, parsed parameters, and execution handler must remain one immutable tuple. Error handling must not alter positional correspondence.

### Search signatures

- arrays named like `requests`, `matches`, `routes`, `permissions`, `responses`;
- separate loops for matching, validation, and execution;
- `continue` or exception handling in only one array-building loop;
- placeholder appended only on success;
- positional indexing instead of object identity;
- batch and single-request implementations with different validation order.

### Primitive augmentation from the historical case

The initial routing mismatch enabled an unsafe scalar to reach SQL. Query results could then become trusted application objects, enter cache/state, and participate in lifecycle/writeback gadgets. The lesson is to trace beyond SQLi into **object identity and trusted state transitions**.

### Safe verification

Prove that two benign routes become mispaired using unique markers and no state-changing operation. Then separately demonstrate the downstream parameter validation failure in a local test fixture.

### KILL conditions

- route, authorization, parameters, and handler are stored in one object;
- every failure path inserts a placeholder or aborts the batch;
- execution re-resolves and reauthorizes each request independently;
- no unsafe downstream primitive exists.

### Fix pattern

Eliminate parallel arrays; bind route match and authorization to the immutable request object; abort on parse mismatch; add malformed-first-element regression tests.

---

## Pattern 03 — Primitive-to-object/cache poisoning and privileged writeback

**Historical family:** the second half of WP2Shell.

### Abstract chain

`query/deserialization primitive -> attacker-shaped row/object -> trusted domain hydration -> object cache/session/identity map -> authorization or writeback gadget -> privileged state/code execution`

### Violated invariant

Objects loaded from storage must satisfy schema, identity, ownership, type, and lifecycle invariants before becoming trusted cached objects or authorization principals.

### Search signatures

- constructors such as `from_row`, hydration, model factories, or magic property access;
- caches keyed only by attacker-influenced IDs;
- object writeback in destructors, save hooks, oEmbed, customizer, sync, or nested update flows;
- user/role objects reconstructed from partial rows;
- authorization checks consuming mutable cached objects.

### Safe verification

Use a local database fixture to create a malformed row that cannot pass normal creation, then prove whether the object layer/cache accepts it. Stop before creating a real administrator or deploying code.

### KILL conditions

- strict schema/type/ownership validation during hydration;
- cache entries are signed/versioned or reconstructed from authoritative storage;
- writeback reauthorizes and validates the object;
- primitive cannot influence identity or privileged fields.

### Fix pattern

Parameterized queries; typed inputs; validate hydrated objects; isolate cache namespaces; reauthorize writeback; reject impossible object states.

---

## Pattern 04 — Attacker-selected backend content rendered in a trusted administrative origin

**Historical family:** Windows Admin Center one-click chain, CVE-2026-32196.

### Abstract chain

`attacker-controlled gateway/base URL -> trusted TLS connection to attacker server -> malicious error/auth response -> HTML rendering in privileged origin -> same-origin token/API/native capability -> RCE or credential boundary break`

### Violated invariant

Selecting a backend must not grant that backend authority to inject active content into the client’s trusted origin. Error and authentication responses are untrusted data.

### Search signatures

- gateway/base URL accepted from query string, deep link, config, or project file;
- TLS validation used as the only trust decision;
- server error text or `WWW-Authenticate` content inserted through HTML sinks;
- privileged tokens in `localStorage`/DOM-accessible storage;
- PowerShell, terminal, process, file, extension, or server-management APIs callable from the rendered origin.

### Safe verification

Use a researcher-owned mock gateway and render a harmless inert marker. Prove script execution only in an isolated test account/VM and use a non-sensitive API action if explicitly allowed.

### KILL conditions

- backend host is immutable or cryptographically bound to a trusted tenant;
- all remote text is rendered as text, not HTML;
- CSP/sandbox and bridge authorization prevent privileged calls;
- no token or privileged same-origin capability is available.

### Fix pattern

Strict backend allowlist/binding; structured error rendering; no raw HTML; isolate untrusted content in a sandboxed origin; keep privileged tokens outside script-accessible storage; authorize every native/API operation.

---

## Pattern 05 — Unsafe deserialization and dynamic module/class/export resolution

**Historical families:** PTC Windchill advisory GHSA-F345-WXWR-FXFH; Qwik server-function RCE research.

### Abstract chain

`attacker-controlled serialized descriptor -> type/QRL/class/module/export resolver -> dynamic import/require/reflection -> callable gadget or initializer -> execution`

### Violated invariant

Deserialized data may select only capabilities from an immutable server-generated allowlist. Integrity hashes over attacker-created descriptors do not establish authorization.

### Search signatures

- serialized objects carrying `type`, `class`, `module`, `path`, `export`, `method`, `handler`, `qrl`, or plugin identifiers;
- dynamic `require`, import, `Class.forName`, reflection, method handles, `ObjectInputStream`, XStream-like frameworks, or custom gadget deserializers;
- fallback resolver when generated registry lookup fails;
- local dependency exports callable with attacker arguments;
- constructors/static initializers with side effects.

### Runtime matrix requirement

Verify CommonJS/ESM/Bun/Node behavior, global `require`, bundler output, classloader, dependency versions, path suffixing, and package resolution. A gadget that works in one runtime is not universal.

### Safe verification

Resolve only a benign test export or constructor that writes a temporary marker in an isolated fixture. Prefer proving attacker-selected symbol resolution before code execution.

### KILL conditions

- immutable generated registry with opaque IDs;
- path and symbol are server-generated and signed;
- deserializer produces data-only types;
- runtime lacks the required resolver/gadget;
- advisory does not identify a reachable current target path.

### Fix pattern

Remove dynamic fallback; use capability IDs mapped to immutable functions; strict type allowlist; data-only serialization; update runtime/dependency; regression-test arbitrary module/class/export rejection.

---

## Pattern 06 — Sandbox escape through cross-context evaluation and global clobbering

**Historical family:** ServiceNow CVE-2026-6875 exploitation analysis.

### Abstract chain

`pre-auth/low-priv expression evaluation -> nominal sandbox -> include/helper evaluated in different context -> mutable global/prototype/function clobbering -> constructor or callback created outside sandbox -> privileged execution`

### Violated invariant

All code reachable from an untrusted expression must remain in the same restricted security domain, with immutable host intrinsics and no path to unsandboxed function construction.

### Search signatures

- `include`, script include, plugin load, template import, macro expansion, or callback registration from inside a sandbox;
- shared mutable globals or prototypes across sandbox and host;
- ability to replace clone/extend/helper functions;
- access to constructors through class factories or reflection;
- host callbacks created in one realm and invoked in another;
- “guarded script” checks applied only at the first entrypoint.

### Safe verification

Use a harmless boolean or marker callback to prove realm/context escape. Do not access tables, create accounts, execute OS commands, or pivot to connected agents.

### KILL conditions

- separate process/VM with capability-secure IPC;
- frozen intrinsics/globals and no host object mutation;
- every include/helper is parsed by the same restricted evaluator;
- untrusted code cannot select or redefine callbacks.

### Fix pattern

Capability-based sandbox; immutable intrinsics; no shared globals; guarded grammar for all nested evaluations; remove general-purpose include/constructor access; authorize host operations independently.

---

## Pattern 07 — Cross-platform repository/archive path semantics to protected-directory execution

**Historical family:** Dulwich/Git Windows RCE, CVE-2026-42305.

### Abstract chain

`repository tree entry valid as one name on producer OS -> victim filesystem interprets separator/ADS/short alias/device name -> write under protected metadata directory or outside worktree -> Git hook/loader later executes`

### Violated invariant

Path validation must model the destination filesystem before materialization, including aliases and reserved semantics. Protection configuration must be read under the documented key and default safely.

### Search signatures

- validation on POSIX before checkout/extraction on Windows;
- backslash accepted as a filename byte;
- colon/alternate data stream not rejected;
- only one literal short-name alias checked;
- reserved device names not normalized;
- trailing dots/spaces and case folding ignored;
- config lookup like duplicated namespace/key causing protection to remain disabled;
- protected metadata directories such as `.git`, hooks, plugin metadata, or package control files.

### Safe verification

Construct a local repository/archive with benign entries and verify path decomposition in an isolated Windows VM. Use a harmless hook marker only after confirming scope and automatic execution.

### KILL conditions

- destination-platform validator runs immediately before write;
- protected directory identity is checked after filesystem canonicalization;
- archive/repo entries cannot contain hostile names;
- hook execution is disabled or requires an unrelated trusted action outside the threat model.

### Fix pattern

Platform-aware validation; reject separators/ADS/aliases/reserved names; canonicalize after extraction target resolution; protect metadata dirs; correct config keys; default protection on; add cross-platform regression corpus.

---

## Pattern 08 — Resource lookup side effect before deserialization/type rejection

**Historical family:** Fastjson 1.2.83 research summarized in the supplied FearsOff article.

### Abstract chain

`attacker-controlled type/resource string -> DNS/URL/JAR/classpath lookup occurs before policy rejection -> fetched/cached/open artifact survives -> second-stage path or descriptor references it -> class/module load -> initializer execution`

### Violated invariant

Validation must be side-effect free. No external resolution, DNS, download, class loading, or cache mutation may occur before the type/resource is authorized.

### Search signatures

- type checks calling resource lookup or classloader APIs;
- URL/JAR/schema/plugin resolution during validation;
- caches populated before allowlist decision;
- temporary files deleted by name but kept open by a descriptor;
- `/proc/self/fd`, file handles, or loader URLs accepted as classpath entries;
- multi-request exploit state.

### Runtime matrix requirement

Record JDK/runtime, classloader, fat-JAR launcher, Linux `/proc`, URL/JAR caching, temporary-file behavior, file-descriptor predictability, and security manager/container restrictions.

### Safe verification

Use loopback DNS/HTTP and a benign non-executable resource to prove pre-rejection lookup and persistence. Test class resolution only with a local inert class in an isolated harness.

### KILL conditions

- authorization occurs before any lookup;
- resolver is network-disabled and side-effect free;
- fetched artifact cannot become loader-visible;
- required classloader/filesystem behavior is absent from shipped deployment.

### Fix pattern

Pure validation first; strict type allowlist; disable network/resource resolution; close and unlink artifacts safely; do not accept arbitrary loader URLs or file-descriptor paths.

---

## Pattern 09 — Configuration or import primitive to arbitrary write and privileged consumer

**Historical families:** Redis deployment-to-RCE techniques; OPNsense CVE-2026-57155.

### Abstract chain

`low-privileged config or exposed service command -> attacker-selected source/path/content -> file write with partial filename constraints -> privileged scheduler/parser/loader consumes destination -> execution`

### Violated invariant

A low-privileged configuration capability must not become arbitrary content placement in a directory interpreted by a more privileged automatic consumer.

### Search signatures

- URL/import source configurable by non-root users;
- remote CSV/JSON/archive fields used as filenames;
- directory and filename configured separately;
- fixed suffix still compatible with a config include glob or web root;
- root cron, log rotation, service loader, package/plugin discovery, shell profile, or startup task consuming the target;
- database snapshot/module configuration writable over the network.

### Redis-specific falsification

Differentiate a product vulnerability from an intentionally exposed administrative Redis interface. If the attacker already has unrestricted Redis administration and the program treats that as deployment misconfiguration, KILL unless a separate product boundary is crossed.

### Safe verification

Write a benign marker/config comment into a researcher-owned test destination and prove the privileged consumer parses it without executing commands. Use a disposable appliance/VM for scheduler behavior.

### KILL conditions

- attacker already has equivalent root/admin capability by design;
- destination has no automatic executable consumer;
- path is constrained to a non-interpreted data directory;
- privileged consumer validates ownership, mode, path, and grammar.

### Fix pattern

Restrict configuration roles; fixed trusted source; sanitize path components; atomic safe directory writes; no wildcard includes from writable locations; strict config grammar; drop privileges before fetch/parse.

---

## Pattern 10 — Stored XSS to privileged same-origin API and web-root/plugin execution

**Historical families:** DotNetNuke stored SVG XSS to RCE; WordPress
XSS2Shell `CVE-2026-64638` / `GHSA-52p2-r8wf-jcrf` as a longer pre-auth parser,
DOM, JSONP/SOME, Application Password, REST, and plugin-upload chain.

### Abstract chain

`low-privileged stored active content -> administrator views/clicks -> script runs in privileged origin -> obtains CSRF/session capability -> calls privileged config/file/plugin API -> writes executable server content -> RCE`

### Violated invariant

Untrusted stored content must not execute in an administrative origin, and privileged APIs must not rely solely on same-origin script possession or ambient administrator session.

### Search signatures

- SVG/HTML/Markdown uploads rendered inline;
- messaging/notification features delivering user content to administrators;
- anti-CSRF token readable by script;
- config file, template, skin, plugin, extension, package, or web-root write APIs;
- API authorization based only on admin session without reauthentication or object constraints.

### Safe verification

Demonstrate harmless DOM execution and a non-destructive privileged API read or temporary researcher-owned config marker. Do not deploy a webshell.

For XSS2Shell-shaped paths, load
`skill/compositional-exploit-chain-hunter/references/wordpress-xss2shell-seven-boundary-method.md`.
The pre-auth entry does not remove the logged-in administrator's active
interaction or configuration prerequisites. Prove reflection-to-DOM,
automatic gadget, script response, SOME invocation, credential issuance and
receipt, exact REST authority, stored script, upload/extraction, and direct PHP
execution independently. The exact WordPress chain is public fixed prior art,
not a new finding.

### KILL conditions

- content is served as attachment or isolated origin;
- robust SVG sanitization and CSP prevent script;
- privileged write API requires reauthentication or immutable allowlisted paths/content;
- victim interaction is outside program rules.

### Fix pattern

Sanitize/disable active content; isolate uploads; strong CSP; reauthorize sensitive API actions; prohibit arbitrary server-side file writes; use signed packages and immutable templates.

---

## Pattern 11 — Remote protocol lifecycle bug to double free and allocator-dependent control

**Historical family:** Apache HTTP Server HTTP/2 CVE-2026-23918.

### Abstract chain

`remote reset/abort timing -> same stream/object enters multiple cleanup paths -> duplicate queue/cleanup registration -> double free -> allocator-specific reuse/callback corruption -> possible execution`

### Violated invariant

Every protocol object has one explicit owner and one terminal transition. Cleanup must be idempotent, and callbacks must not queue the same object twice.

### Search signatures

- stream/request reset before full initialization;
- cleanup from both protocol callback and worker/error path;
- arrays/queues of objects pending destruction without membership guard;
- refcount or state flag changed after queueing;
- one-version regression in ownership logic;
- multi-threaded model differences;
- pool allocators storing cleanup callbacks near reusable objects.

### Safe verification

First prove deterministic double cleanup with ASAN/debug allocator in the exact affected version/configuration. Only evaluate control primitives in an isolated lab; do not target public servers or perform availability testing outside explicit permission.

### KILL conditions

- only unaffected versions/configurations are deployed;
- object cleanup is idempotent or membership-guarded;
- prefork/single-thread model excludes the path;
- only non-deterministic crash is shown and availability is excluded;
- no credible control primitive for an RCE claim.

### Fix pattern

Single owner/state machine; idempotent cleanup; remove duplicate registration; assertions and regression tests for early reset/abort; harden allocator/callback storage.

---

## Pattern 12 — Document or Markdown link to OS protocol-handler execution

**Historical family:** Windows Notepad CVE-2026-20841.

### Abstract chain

`attacker-supplied document -> rendered clickable link -> insufficient scheme policy -> ShellExecute/registered protocol handler -> installer/script/application action`

### Violated invariant

A document renderer must allow only explicitly safe resource schemes and must not delegate arbitrary protocol semantics to the operating system.

### Search signatures

- Markdown/HTML links passed to `ShellExecute`, URL openers, `Process.Start`, or platform launch services;
- allowlist based on substring/prefix without URL canonicalization;
- custom protocols, app installers, file URLs, UNC paths, and file associations;
- warning/confirmation applied after handler resolution or absent for “trusted” schemes.

### Safe verification

Register or use a benign researcher-owned protocol handler that writes a temporary marker in a VM. Require the exact documented victim interaction; do not disguise the file or induce third-party clicks.

### KILL conditions

- only HTTP(S) and safe local resources survive canonicalized allowlist;
- explicit user confirmation clearly identifies the executable action and program treats it as by design;
- protocol handler cannot execute or install content;
- target component/version is not shipped.

### Fix pattern

Canonical scheme allowlist; block executable/custom handlers; display destination; isolate renderer; avoid generic OS launch APIs for untrusted content.

---

## Pattern 13 — Public build/preview endpoint accepts attacker replacement definition

**Historical family:** Langflow CVE-2026-33017.

### Abstract chain

`public/shared flow ID -> optional attacker-supplied graph/data definition -> build helper prefers caller data over stored trusted definition -> custom component code reaches exec during validation/build -> unauthenticated RCE`

### Violated invariant

A public execution endpoint may accept **inputs to** a trusted server-owned workflow, but must not accept a replacement workflow definition or executable component graph.

### Search signatures

- public/shared/template endpoints with both object ID and optional `data`/`graph`/`flow`/`definition`;
- helper functions where `data != None` bypasses database loading;
- custom component validation that compiles or executes code;
- preview/build/validate endpoints reusing authenticated execution helpers;
- old CVE fix adding auth to one direct `exec` endpoint while sibling callers remain public.

### Safe verification

Create a researcher-owned public flow with a benign stored definition, submit a replacement definition that only changes a harmless constant, and prove which definition is built. In a local isolated instance, use a temporary marker only if needed to confirm execution.

### KILL conditions

- public endpoint ignores/rejects caller definitions and loads only authoritative storage;
- custom code is disabled for public flows;
- build runs in a real sandbox with no protected boundary;
- endpoint is not reachable unauthenticated in released configuration.

### Fix pattern

Remove the replacement parameter; force stored definition; separate runtime inputs from executable graph; authenticate code-authoring endpoints; sandbox custom components; regression-test extra field rejection/ignore behavior end-to-end.

---

## Pattern 14 — Configuration/control data crosses into code without a clear privilege boundary

**Historical family:** the Redis guide and multiple supplied research sources share this general lesson.

### Abstract chain

`apparently low-risk configuration field -> privileged worker fetches/parses/loads it -> field controls code-adjacent semantics -> automatic execution`

### Examples of code-adjacent semantics

- executable or hook search path;
- plugin/module/class/export identifier;
- web root, config include, log path, cron/task file;
- gateway/base URL whose responses are rendered as trusted HTML;
- repository tree paths materialized on another OS;
- workflow/flow definitions passed to an evaluator;
- cleanup callback or object ownership state.

### Audit rule

Treat configuration as untrusted code input whenever it selects **what**, **where**, **which interpreter/loader**, or **which privileged consumer** acts later.

---

## Pattern 15 — Open API filter/query object reaches an executable evaluator

**Historical family:** Taskcluster `GHSA-ccv5-c45x-2q38` /
`CVE-2026-11892`, fixed by Taskcluster PR #8718 in release 100.3.0.

### Abstract chain

`GraphQL/REST open filter object -> generic query/operator DSL -> code-bearing operator -> dynamic predicate compilation -> invocation over live data -> server process authority -> protected impact`

### Violated invariant

An API advertised as data-only filtering must expose only typed, server-owned,
data-only operators. Caller-controlled objects must not select the full control
language of a general evaluator.

### Required distinctions

Prove separately the open schema, raw-object forwarding, installed dependency
and operator set, runtime/configuration gate, caller principal, resolver/upstream
authorization, deterministic non-empty result, predicate invocation, output
channel, execution context, and protected impact. None of GraphQL, JSON,
`new Function`, anonymous middleware continuation, error reflection, or package
presence proves the complete chain alone.

### Method and safe verification

Load
`skill/dynamic-filter-evaluator-rce-hunter/references/dynamic-filter-evaluator-rce-method.md`.
Begin with an owned data element and harmless computed marker. Do not start with
shell execution, environment dumps, credential replay, persistence, or public
service exploitation.

### Fix pattern

Remove the generic evaluator; replace open JSON with typed fields implementing
only the required search semantics. If a DSL is unavoidable, recursively
allowlist data-only fields/operators and reject unknown executable semantics
before dependency code. Treat CSP/runtime flags as defense in depth.

### Novelty rule

The exact Taskcluster `sift`/`$where` path before 100.3.0 is public and fixed.
Retain only a distinct current endpoint, evaluator, sibling implementation,
incomplete patch, or regression with its own release and impact proof.

---

## Pattern 16 — One runtime interpolates data into another runtime's source

**Historical family:** `0din-ai/ai-scanner`
`GHSA-r27j-xxgx-f5vr` / `CVE-2026-41512`, affecting 1.0.0 through
1.4.0 and fixed in 1.4.1.

### Abstract chain

`authenticated or public field -> source-language semantic validation -> heredoc/template interpolation -> complete generated script -> temporary file/stdin/-e -> target interpreter -> application-process authority -> protected impact`

### Violated invariant

Dynamic values must cross runtime boundaries through a typed data channel.
Executable templates must remain static. Validating that a value is a URL,
selector, path, or identifier does not encode it for JavaScript, shell, Python,
PowerShell, SQL, or any other target grammar.

### Search signatures

- heredocs or multiline templates containing interpolation and executable code;
- `Tempfile`, `.js`/`.py`/`.sh`/`.ps1` writes followed by an interpreter;
- `Open3.capture3`, subprocess/spawn wrappers, interpreter `-e`, or stdin code;
- Playwright/Puppeteer helpers that generate scripts around URLs, selectors,
  user agents, messages, paths, callbacks, or options;
- quote-only `gsub`/`replace` escaping that does not correctly preserve
  backslashes, newlines, comments, template markers, or nested contexts;
- route/module names implying administration without an actual role predicate.

### Required distinctions

Prove separately the caller principal, policy predicate, source validator,
target lexical context, exact emitted bytes, parse-clean full artifact,
interpreter invocation, process authority, and protected effect. An `admin`
namespace, `verify_authorized`, URL parser, HTTP error, source snippet, or
presence of Node.js is not enough.

### Safe verification

Load
`skill/cross-language-script-injection-hunter/references/cross-language-script-injection-rce-method.md`.
Start by capturing and parsing the locally generated artifact. Use a benign,
dependency-free child-runtime canary in an isolated owned fixture, with a
baseline, negative control, authoritative read-back, and cleanup. Do not begin
with shell commands, environment dumps, credential replay, persistence, or a
public service.

### Fix pattern

Prefer direct library calls. Otherwise place dynamic values in strict-schema
JSON or structured IPC and let a static script read them as data. Use canonical
target-language serialization only when a literal is unavoidable, coerce
numeric/boolean options, minimize child authority, and regression-test semantic
value preservation for quotes, backslashes, newlines, delimiters, comments,
template markers, and Unicode separators.

### Novelty rule

The exact `ai-scanner` lineage through 1.4.0 is public and fixed. Retain only a
distinct current product or an independently reachable unfixed sibling or
regression with its own release, principal, source-to-interpreter proof, and
impact evidence.

---

## Pattern 17 — Dynamic structured data controls a protocol, worker, or interpreter

**Historical families:** GitLab HackerOne `#1679624` / issue `#371884`,
HackerOne `#1609965` / issue `#366088` / `CVE-2022-2185`, and HackerOne
`#1401444` / issue `#345892`.

### Abstract chains

`remote map -> recursive rich object -> attacker-selected runtime method -> protocol framing disagreement -> protected state -> separate state consumer -> terminal impact`

`remote import metadata -> broad attribute transformation -> persisted/queued execution-adjacent state -> string-form process consumer -> worker authority`

`untrusted renderer input -> optional dependency auto-registers interpreter extension -> incomplete sandbox -> host capability`

### Violated invariant

Untrusted structured data must remain typed, data-only primitives. It must not
select runtime methods, framing semantics, model attributes, feature
activation, interpreter availability, or executable grammar. Optional package
presence is not authorization, and an intermediate protocol/state primitive
does not prove terminal RCE.

### Mandatory method

Load `references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md`. Build the dynamic
method/attribute/feature surface, exact framing-bytes table, import-attribute
provenance, optional-dependency activation matrix, and intermediate-versus-
terminal evidence ladder.

### Safe verification

Prefer a mock serializer/socket capture, fake queue, strict temporary state, and
fixed inert marker in an isolated owned fixture. Do not place operational
protocol/session payloads, deserialization gadgets, shell commands, reverse
shells, or optional dependency installers into regression fixtures.

### KILL conditions

- remote values are recursively flattened to schema-validated primitives;
- one immutable byte buffer supplies both wire length and transmitted bytes;
- strict positive attribute allowlists and authoritative service checks prevent
  execution-adjacent state from persisting;
- process execution uses fixed executable and argv/stdin without a shell;
- optional interpreter functionality is absent from the release or explicitly
  enabled by trusted configuration and remains fail-closed;
- sandbox/host capabilities required by the chain are unavailable;
- only the public/fixed historical lineage exists;
- the claimed terminal consumer is unproven.

### Fix pattern

Flatten and validate data-only primitives; reserve runtime method names as
defense in depth; frame a single immutable byte buffer; use minimal import-field
allowlists; revalidate queued state; preserve argv/data separation; require
explicit interpreter activation; remove unsafe extensions or isolate them
behind capability-secure IPC; regression-test alternate routes, nested objects,
dependency states, and every terminal edge.

---

## Archive, renderer, and framework consumers

Use:

`untrusted archive/document/request metadata -> object or namespace drift -> authority-bearing open/delete/render/load consumer -> protected effect`

Load `references/ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md`. Inventory
archive entry and extracted-object types, final open-time identity, browser and
framework normalization, upload-to-secondary-renderer/resource-loader edges,
inline option-to-class/constructor/loader capability, and framework-reserved URL
options. Never inherit RCE from markup injection, a dynamic class selection, a
resource fetch, or file exposure: prove the terminal interpreter/process edge
independently with an inert local fixture.

KILL only when the final consumer is unreachable or a positive allowlist plus
canonical root/origin/namespace and object-identity control remains effective
for link, alias, encoded, default, fallback, and secondary-consumer states.

---

## Cross-case audit matrices

### A. Representation identity matrix

| Candidate | Representation validated | Representation used | Transformations between them | Can identity drift? | Evidence |
|---|---|---|---|---|---|
| | | | | | |

### B. Primitive-to-consumer matrix

| Primitive | Controlled property | Automatic trusted consumers | Required privilege transition | Real shipped gadget? | Falsifier |
|---|---|---|---|---|---|
| SQL/control query | | | | | |
| Object/cache poison | | | | | |
| XSS | | | | | |
| Arbitrary file write | | | | | |
| Dynamic resolver | | | | | |
| Resource fetch/SSRF | | | | | |
| Memory corruption | | | | | |
| Dynamic object/protocol framing | | | | | |
| Persisted import metadata | | | | | |
| Optional interpreter activation | | | | | |

### C. Runtime dependency matrix

| Requirement | Observed | Default in stable release | Chain fails without it? | Evidence |
|---|---|---|---|---|
| OS/filesystem semantics | | | | |
| Runtime/JDK/Node/PHP/.NET version | | | | |
| Module/classloader mode | | | | |
| Allocator/server worker model | | | | |
| Feature flag/configuration | | | | |
| Process privilege/sandbox | | | | |
| Dependency/gadget present | | | | |

### D. Patch-variant matrix

| Original fix invariant | Patched path | Sibling/alternate path | Same sink? | Same attacker capability? | Distinct root cause/boundary? | Verdict |
|---|---|---|---|---|---|---|
| | | | | | | |

---

## Source index supplied for this atlas

These sources are included only as prior-art references and should be rechecked when current accuracy matters:

- GitHub RCE deep dive: `https://dev.to/mohamed_aboelkheir/github-rce-cve-2026-3854-deep-dive-lessons-learned-5e3`
- GitHub RCE analysis: `https://www.wiz.io/blog/github-rce-vulnerability-cve-2026-3854`
- WP2Shell explanation: `https://www.picussecurity.com/resource/blog/cve-2026-63030-and-cve-2026-60137-wp2shell-wordpress-rce-explained`
- WP2Shell technical analysis: `https://www.rapid7.com/blog/post/etr-cve-2026-63030-wp2shell-a-critical-remote-code-execution-vulnerability-in-wordpress-core/`
- WP2Shell detection: `https://www.elastic.co/security-labs/wp2shell-wordpress-rce-detection-elastic-defend`
- Windows Admin Center: `https://cymulate.com/blog/cve-2026-32196-one-click-rce-windows-admin-center/`
- Windchill advisory: `https://github.com/advisories/GHSA-F345-WXWR-FXFH`
- Qwik RCE: `https://www.sebsrt.xyz/blog/a-qwik-rce/`
- ServiceNow: `https://www.helpnetsecurity.com/2026/07/20/servicenow-cve-2026-6875-exploited/`
- Dulwich/Git Windows path issue: `https://www.sentinelone.com/vulnerability-database/cve-2026-42305/`
- Fastjson: `https://fearsoff.org/research/fastjson-1-2-83-rce`
- Redis RCE guide: `https://www.penligent.ai/hackinglabs/redis-rce-exposed-the-2026-survival-guide-for-security-engineers/`
- DotNetNuke XSS-to-RCE: `https://pentest-tools.com/blog/dotnetnuke-xss-to-rce`
- OPNsense: `https://hackingcult.de/advisories/2026-07-01-cve-2026-57155/`
- Apache HTTP/2: `https://hadrian.io/blog/cve-2026-23918-apache-http-server-double-free-rce-in-http-2-implementation`
- Windows Notepad: `https://www.zerodayinitiative.com/blog/2026/2/19/cve-2026-20841-arbitrary-code-execution-in-the-windows-notepad`
- Langflow overview: `https://labs.cloudsecurityalliance.org/research/csa-research-note-langflow-cve-2026-33017-ai-platform-rce-20/`
- Langflow researcher article: `https://medium.com/@aviral23/cve-2026-33017-how-i-found-an-unauthenticated-rce-in-langflow-by-reading-the-code-they-already-dc96cdce5896`
- ai-scanner advisory: `https://github.com/0din-ai/ai-scanner/security/advisories/GHSA-r27j-xxgx-f5vr`
- ai-scanner invariant-restoring fix commit: `https://github.com/0din-ai/ai-scanner/commit/6e86cca4164c570daf22faa7d9415695789c215e`
- WordPress XSS2Shell advisory: `https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-52p2-r8wf-jcrf`
- WordPress XSS2Shell primary research: `https://pwn.ai/blog/xss2shell`
- WordPress 7.0.3 release: `https://wordpress.org/news/2026/08/wordpress-7-0-3-release/`

## Final discipline

The atlas is successful only when it helps find and then **falsify or validate a target-specific current path**. It must never be used to inflate a generic sink, copied CVE, deployment misconfiguration, or public exploit reproduction into a bounty claim.
