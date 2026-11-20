# Archive, Renderer, and Framework Consumer Boundary Method

`ARCHIVE_RENDERER_FRAMEWORK_CONSUMER:v1`

## Purpose and status

Use this method when untrusted archive entries, upload metadata, document
options, route parameters, or broad request parameters are checked in one
representation and later consumed by a filesystem, browser, renderer, URL
builder, loader, or interpreter with greater authority.

The historical examples below are **PUBLIC / FIXED / PRIOR ART**. They are
regression lineages, not findings, signatures, payload libraries, or authority
to test a live service.

| Historical lineage | Reusable boundary | Public record |
|---|---|---|
| GitLab BulkImports UploadsPipeline | archive entry -> extracted object -> later file open | GitLab issue `#349524`; fixed in GitLab 14.6.2 |
| GDK letter_opener_web | cross-origin browser request -> decoded route id -> recursive delete | GDK issue `#1314`; development-only lineage |
| GitLab DesignReferenceFilter | upload filename grammar -> string-built markup -> DOM/redactor -> secondary renderer | GitLab issue `#332420`; `CVE-2021-22238`; fixed historical releases |
| GitLab Kramdown wiki renderer | inline option -> dynamic class -> constructor options -> nested loader/gadget | GitLab issue `#324452`; upstream kramdown PR `#708`; fixed in GitLab 13.9.4 |
| GitLab SafeParamsHelper | request parameter -> framework-reserved URL option -> redirect/async HTML consumer | GitLab issue `#232829`; fixed in GitLab 13.4.2 |

Do not reproduce destructive requests, real file reads, live SSRF, credential
access, metadata-service access, command execution, reverse shells, or public
service behavior. Safe local fixtures must use synthetic paths, inert objects,
loopback-only stubs, and reversible state.

## Unified security theorem

The common chain is:

```text
untrusted packaged/request/document input
  -> parser, extraction, decoding, projection, or helper namespace
  -> representation or object-identity change
  -> authority-bearing filesystem/browser/framework/renderer/loader consumer
  -> protected effect
  -> separately proven terminal impact
```

The protected invariant is:

> An untrusted carrier MUST NOT change filesystem object identity, canonical
> root, URL-helper option namespace, markup grammar, runtime class/loader
> capability, origin, or authority between validation and use.

Names such as `safe_params`, `sanitize`, `untar`, `valid format`, `renderer`, or
`development only` are not proof that the invariant is preserved.

## Evidence model

For every candidate, record these representations independently:

1. raw bytes, archive header, upload metadata, URL, or document text;
2. parser-decoded entry/parameter and its type;
3. value or object actually validated;
4. value or object persisted, queued, rendered, opened, deleted, or loaded;
5. canonical root/origin/namespace at the final consumer;
6. feature, environment, browser, dependency, and release reachability;
7. intermediate effect;
8. separately demonstrated terminal security impact.

If any edge is inferred only from a helper name or a source sink, retain
`HYPOTHESIS / NEEDS_ARCHIVE_RENDERER_PROOF`.

## Family A: archive entry becomes a different filesystem object

### Mandatory archive-entry inventory

Do not review only member names. Enumerate every admitted entry type and the
consumer behavior for each:

| Entry/object type | Questions |
|---|---|
| regular file | Is the final open bound to the extracted inode and root? |
| directory | Can later traversal cross a replaced directory? |
| symbolic link | Is it rejected before extraction and before use? |
| hard link | Can it alias a file outside the intended object set? |
| FIFO/socket/device | Can later open block or access a special object? |
| sparse/extended metadata | Can size, path, owner, or link semantics change? |

Trace:

```text
archive header
  -> extractor policy
  -> extracted object type
  -> post-extract walk/glob
  -> lstat/canonical-root check
  -> open/delete/upload
  -> fstat/read-back of the opened object
```

A lexical `../` check does not prove safety. A post-extract list of paths is
also insufficient when the eventual `open` follows links. Prefer extraction
that rejects links and special entries, a private root, directory-descriptor
relative operations, no-follow semantics, and an open-time identity check.

### Archive KILL rule

Before KILL, prove all of:

- unsupported entry types are rejected;
- the extracted object cannot escape the private root through links or parent
  replacement;
- the object validated is the object opened;
- the final open uses no-follow/root-bound semantics where available;
- a closest sibling link fixture remains blocked;
- no TOCTOU window changes object identity between check and use.

## Family B: browser request reaches a destructive filesystem sink

Map the entire browser-to-sink path:

```text
attacker origin
  -> browser URL normalization
  -> simple-request / preflight decision
  -> method override
  -> router decoding
  -> authentication and CSRF
  -> path join/canonicalization
  -> delete primitive
```

Mandatory checks:

- development, test, production, and packaged-artifact route presence;
- binding interface and realistic developer-machine reachability;
- authentication, same-site cookies, CSRF verification, Origin/Referer checks,
  and method-override behavior;
- encoded dot, separator, and mixed-normalization behavior in each supported
  browser, proxy, router, and framework;
- whether recursive deletion receives an attacker-controlled path component;
- whether the canonical target remains inside an owned private fixture.

`mode: no-cors` does not make a request harmless; it limits response access.
Likewise, CORS is not a CSRF defense for a simple state-changing request.

Never test a real delete path. A safe proof stops at a mocked delete receiver or
an empty disposable directory created solely for the test.

## Family C: upload metadata becomes markup and a secondary resource load

Separate the chain into edges:

```text
multipart/upload metadata grammar
  -> persisted filename or model field
  -> reference selector/regex and decode
  -> URL/attribute construction
  -> HTML parser or DOM builder
  -> redactor/rewrite stage
  -> stored rendering context
  -> notification/email renderer
  -> CSS/resource loader
  -> local/network read
  -> observable output
```

For each edge, record the exact representation and escaping context. Validation
of the child node does not authorize consuming a parent attribute. A valid
selector match does not prove that the value later interpolated into markup was
validated. HTML string interpolation is not equivalent to a typed DOM builder.

Treat these as distinct claims:

- stored markup injection;
- script execution under the actual CSP and interaction model;
- notification generation;
- secondary local/network resource loading;
- response or rendered-output exfiltration.

Do not inflate the first proven edge into the last. If the terminal output edge
is missing, use `NEEDS_ARCHIVE_RENDERER_PROOF`.

## Family D: inline document options select runtime capability

Build an option-to-capability table before KILL:

| Stage | Evidence required |
|---|---|
| inline option parser | exact permitted keys, nesting, aliases, and types |
| class/constant resolution | namespace, inheritance search, allowlist, fallback |
| constructor | exact attacker-controlled options and side effects |
| nested resolver/loader | `require`, import, driver, plugin, template, formatter |
| loaded-class universe | classes and dependencies present in shipped runtime |
| terminal consumer | file, network, process, deserializer, or privileged renderer |

Dynamic constant lookup must be scoped to an explicit namespace and positive
allowlist; inheritance/ancestor lookup must be disabled where the language API
supports it. Security-sensitive inline options should be forbidden before they
reach the renderer. A class name regex is not a capability allowlist.

Do not begin with command strings or a reverse shell. Use inert constructor
spies and fake loaders to prove whether attacker-controlled options reach a
runtime capability.

## Family E: request parameters enter a framework-reserved option namespace

Trace:

```text
request parameters
  -> permit/except/safe helper
  -> business parameters mixed with framework options
  -> URL/redirect/async-viewer builder
  -> generated origin/scheme/path
  -> browser/fetch/HTML consumer
```

Maintain a framework-version-specific inventory of reserved URL/helper options.
An incomplete denylist is fragile because the framework owns more keys than
`host`, `port`, and `protocol`, and the list may change between versions.

Preferred invariant:

- positively allow only business parameters;
- supply routing options from trusted constants;
- require relative or same-origin generated URLs when that is the contract;
- parse and validate the final generated URL, not just individual input fields;
- bind the claim to the consumer: redirect, clickable link, async fetch, script
  URL, or HTML insertion have different impacts and controls.

## Cross-family consumer-boundary KILL challenge

Before KILLing a candidate, answer all of these with evidence:

1. What untrusted carrier enters the system?
2. What exact representation and object are validated?
3. What exact representation and object are consumed?
4. Can link resolution, decoding, browser/framework normalization, fallback,
   inheritance, or secondary rendering change identity or authority?
5. Which feature/environment/dependency/browser state makes the path reachable?
6. What component enforces the canonical root, origin, namespace, or capability
   boundary at the final consumer?
7. Does that control remain effective for absent, default, error, link, alias,
   encoded, and secondary-consumer states?
8. What closest one-variable sibling is safe?
9. What patched control closes the root cause?
10. Is the terminal impact edge independently proven?

Verdict logic:

- `DO_NOT_KILL`: an untrusted value reaches an authority-bearing consumer, the
  invariant is not preserved, and a protected effect is observed.
- `NEEDS_ARCHIVE_RENDERER_PROOF`: evidence, release reachability, browser or
  dependency state, object identity, or terminal impact is incomplete.
- `KILL_ALLOWED`: the final consumer is unreachable or every relevant
  representation is constrained by a positive allowlist/root/origin/capability
  boundary and the protected effect is absent.

`Looks intentional`, `development only`, `the selector matched`, `the path was
sanitized`, or `the helper is named safe` is never sufficient for KILL.

## Safe proof ladder

Use the minimum harmless step needed:

- **E0** — source and release trace only;
- **E1** — parser/option/route unit fixture;
- **E2** — synthetic archive or URL object-type fixture;
- **E3** — mocked final consumer records the exact value/object;
- **E4** — isolated private-root or loopback-only renderer fixture with canary;
- **E5** — closest one-variable safe sibling;
- **E6** — patched control;
- **E7** — authoritative read-back, cleanup, and source-integrity verification.

Stop immediately on third-party data, unexpected secrets, external callbacks,
service instability, destructive scope, or a path outside the disposable test
root.

## Remediation patterns

- Reject archive links and special entries; use private roots and no-follow,
  descriptor-relative final opens.
- Authenticate state-changing routes, enforce CSRF/Origin controls, restrict
  method override, and canonicalize before a non-recursive owned-root delete.
- Normalize upload metadata once, persist a safe identifier, and construct
  markup with typed DOM/content APIs.
- Disable secondary network/filesystem loaders by default and allowlist schemes,
  roots, and hosts only when explicitly required.
- Forbid security-sensitive inline document options and use a closed mapping
  from symbolic names to known-safe classes.
- Replace framework-option denylists with positive business-parameter
  allowlists and validate the final generated URL.
- Add regression tests for the closest unsafe and closest safe sibling at the
  final consumer, not only at the first parser.

Only `STRONG + MANUALLY_CONFIRMED` is report-ready. These historical lineages
remain fixed prior art and must not be presented as newly discovered findings.
