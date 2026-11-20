# Cross-Language Script Injection to RCE Method

## Purpose

Use this method for authorized audits where one runtime emits source code for a second runtime and attacker-controlled values may become syntax rather than data. It generalizes across Ruby-to-JavaScript, Python-to-shell, Java-to-JavaScript, Go-to-PowerShell, CI templating, browser automation, generated SQL or scripts, and similar cross-language code generation.

The reusable root cause is **cross-language code generation with a data/code boundary failure**:

`untrusted value -> validation in source-language domain -> textual interpolation -> target-language lexer/parser -> interpreter execution`

The security invariant is: **dynamic values cross the boundary through a typed data channel; executable source remains static**.

## Public prior art and novelty boundary

GitHub advisory `GHSA-r27j-xxgx-f5vr` / `CVE-2026-41512` documents authenticated remote code execution in `0din-ai/ai-scanner`:

- affected package: `0din-ai/ai-scanner`;
- affected versions: `>= 1.0.0, <= 1.4.0`;
- patched version: `1.4.1`;
- historical vulnerable tag/commit: `v1.4.0` / `522eafd42c66065c48c2968e4204ae5dd2d8d2a2`;
- fixed tag/commit: `v1.4.1` / `6e86cca4164c570daf22faa7d9415695789c215e`;
- advisory severity: Critical, CVSS 3.1 score 9.9.

The historical path was:

`authenticated Rails endpoint -> URL and selector fields -> Ruby URI/policy checks -> heredoc interpolation -> temporary Node.js source -> Open3 interpreter invocation -> Rails-container authority`

The patch replaced dynamic source interpolation with a JSON data file selected through `PLAYWRIGHT_DATA_PATH`, while keeping JavaScript templates static and coercing numeric/boolean options. That is the preferred invariant-restoring pattern.

This exact product/root-cause/version lineage is public and fixed. It is `KILL / DUPLICATE` for novelty. Retain only a distinct current product or a demonstrably incomplete sibling/fix path with its own release, reachability, principal, and impact evidence.

## Target and scope evidence card

Before loading further specialists, record:

| Field | Required evidence |
|---|---|
| Authorization | Program/internal authorization and allowed test mode |
| Exact asset | Repository, service, package, endpoint, or release artifact |
| Release | Current tag/commit/package and proof it ships or deploys |
| Source runtime | Ruby, Python, Go, Java, shell, or other generator runtime |
| Target runtime | Node.js, browser JavaScript, shell, Python, PowerShell, or other interpreter |
| Entrypoint | Route, job, CLI, config, webhook, queue, or file source |
| Principal | Anonymous, authenticated member, tenant role, admin, service, or local user |
| Generator | Heredoc, template, concatenation, format string, emitter, or transpiler |
| Transport | Temporary file, stdin, `-e`, environment, IPC, or stored script |
| Consumer | Exact interpreter/process invocation and caller |
| Boundary | Tenant, identity, process, sandbox, filesystem, network, or privilege |
| Restrictions | Live targets, scanners, rate limits, secret access, destructive tests |

An absent evidence field is `DEFERRED`, not permission to assume it.

## Two-runtime representation map

Build both maps and make them meet.

### Forward map

`raw request/config -> decoding -> source-language object -> validation -> normalization -> interpolation/serialization -> emitted bytes -> transport -> target parser -> execution`

### Backward map

`protected effect <- child-runtime authority <- interpreter process <- script transport <- generated artifact <- generator call <- service/controller <- attacker field`

Use this table:

| Stage | Runtime/component | Representation | Grammar or type | Transformation | Trust assumption | Evidence |
|---|---|---|---|---|---|---|
| Input | | | | | | |
| Validation | | | | | | |
| Generator | | | | | | |
| Artifact | | | | | | |
| Interpreter | | | | | | |
| Effect | | | | | | |

## Discovery signatures

Search for combinations, not isolated keywords:

- heredocs or multiline templates containing dynamic interpolation and target-language code;
- `Tempfile`, temporary `.js`/`.py`/`.sh`/`.ps1` creation, or write-then-execute flows;
- `Open3.capture3`, `spawn`, `exec`, `system`, `subprocess`, `ProcessBuilder`, `child_process`, interpreter `-e`, or stdin execution;
- Playwright/Puppeteer/Selenium helpers that generate wrapper scripts;
- `page.goto`, `locator`, selectors, user agents, output paths, messages, callbacks, or options embedded in quotes;
- manual `gsub`, `replace`, addslashes, slash doubling, or quote-only escaping;
- a validator for URL/path/selector syntax followed by embedding into JavaScript, shell, SQL, regex, or template source;
- scripts built in one service and executed in another worker or container;
- generated error/reporting expressions that include attacker text;
- numeric or boolean options interpolated without strict coercion.

A heredoc, interpreter, or user field alone is only a hypothesis. Require the complete chain.

## Grammar and escaping analysis

For every interpolated field record:

| Field | Source validation | Target context | Delimiter | Escape routine | Backslash handling | Structural tokens | Safe serializer? |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Test local fixtures with representative tokens for the actual context:

- quote matching the surrounding literal;
- backslashes before quotes and closing delimiters;
- CR, LF, and multiline heredoc behavior;
- comment introducers and statement separators;
- template-expression markers such as `${...}` when applicable;
- Unicode line separators and normalization-sensitive characters;
- nested JSON, HTML, CSS, regex, URL, or shell contexts;
- numeric/boolean strings where the emitter expects syntax rather than data.

The key lesson is: **URL validation is not JavaScript string encoding**. Likewise, CSS-selector validation is not JavaScript encoding, filesystem validation is not shell quoting, and source-language escaping is not automatically correct for the target parser.

Quote-only escaping fails because attacker-controlled backslashes before quotes can change whether the emitted quote is escaped. Do not repair this class with a growing manual blacklist. Use a target-language serializer or, preferably, remove dynamic values from source text entirely.

## Authorization and reachability

Trace actual predicates rather than names:

- authentication before-actions and skip conditions;
- CSRF/session requirements;
- policy method return values and inherited policy defaults;
- tenant scoping versus role authorization;
- whether `verify_authorized` checks privilege or only checks that a policy was invoked;
- controller/module/URL namespace versus an actual admin predicate;
- feature flags, background jobs, and default deployment settings;
- whether an attacker can create or mutate the object holding the interpolated field.

Default credentials can reduce the starting cost on unchanged deployments, but they are not required evidence for a route reachable by an ordinary invited user. Keep prerequisite weaknesses separate from the code-generation root cause.

## Safe proof ladder

Do not begin with shell commands.

1. **C0 signature:** identify the exact generator and interpreter consumer.
2. **C1 input control:** prove the current principal can supply the value on the real route.
3. **C2 emitted structure:** capture the generated artifact in a local test and compare a benign value with delimiter/backslash controls.
4. **C3 parse proof:** run only the target parser or syntax checker and show that the full artifact remains valid while the controlled value changes structure.
5. **C4 benign execution:** in an isolated owned fixture, create a dependency-free in-memory or temporary canary without invoking a shell, network, or credential APIs.
6. **C5 boundary:** prove process identity or protected application state using a minimal owned marker; do not dump the environment or read real secrets.
7. **C6 reality:** confirm stable release, default/relevant configuration, prior art, repeated manual result, baseline, negative control, cleanup, and allowed test mode.

Suggested controls:

- baseline with a normal value;
- same value transported through the fixed typed channel;
- invalid-route or unauthorized-principal control;
- generated-source diff showing only the intended data changes in the safe version;
- canary absent before, present only for the candidate, absent after cleanup;
- repeated trials to exclude stale temporary artifacts.

An HTTP 200, generic error, source sink, parse error, or generated snippet is not enough. C6 plus a protected effect is required for `STRONG / MANUALLY_CONFIRMED`.

## Authority and impact analysis

After execution is proven safely, map rather than harvest:

| Capability | Present? | Protected boundary | Minimal safe proof | Prohibited shortcut |
|---|---|---|---|---|
| Process execution | | | benign child-runtime canary | shell command |
| Environment inheritance | | | variable-name inventory or synthetic value | dumping secrets |
| Filesystem write | | | owned temporary file | persistence/backdoor |
| Internal network | | | architecture/config proof | lateral movement |
| Database credential | | | configured capability and owned fixture | production login/replay |
| Signing/encryption secret | | | code-level derivation plus synthetic fixture | token forgery against live users |

Claim only impact directly demonstrated within authorization. Possession or existence of a secret does not by itself prove its usable authority.

## Remediation hierarchy

1. **Remove source generation:** call Playwright or the target library from the application runtime, or expose a narrow worker API.
2. **Use a typed data channel:** strict-schema JSON, structured IPC, stdin, or a data file. The executable template must not vary with attacker values.
3. **Use canonical serializers:** if a literal is unavoidable, use the target language's serializer for the exact value and context. Never hand-roll quote/backslash escaping.
4. **Constrain types:** coerce numeric and boolean options before code generation; reject unknown fields and enums.
5. **Enforce real authorization:** express role and tenant requirements in policy predicates, not route names or comments.
6. **Harden execution:** minimize inherited environment, filesystem permissions, network access, module loading, child-process ability, and temporary-file lifetime.
7. **Test semantics:** assert that the child runtime receives the exact original value as data for adversarial character classes and nested contexts.

Setting a blacklist, blocking one quote, or rejecting one known payload is not a complete fix. URL safety and SSRF validation may be independently necessary, but they do not replace the data/code separation fix.

## Patch and sibling analysis

From the invariant-restoring diff, enumerate:

- all methods using the same generator helper;
- URL, output path, selector, user-agent, message, callback, header, and option fields;
- alternate script transports such as stdin, `-e`, queue payloads, or worker files;
- sibling browser engines and PDF/screenshot/validation flows;
- direct library paths that bypass the shared serializer;
- error/fallback/retry paths that regenerate source differently;
- backports, release branches, vendored copies, and package lag;
- whether the fix moved data out of code everywhere or only blocked one delimiter.

Do not submit the published path under a new method name. A sibling survives only if it is current, independently reachable, not covered by the advisory/fix, and crosses a distinct or still-unfixed boundary.

## KILL rules

KILL when:

- the exact `ai-scanner` <=1.4.0 lineage is being reproduced;
- the scoped/current version is 1.4.1 or later and all dynamic values cross through the typed JSON channel;
- attacker input never reaches emitted source bytes;
- the artifact is not executed in a shipped/default/relevant path;
- the input is already serialized by a correct target-language serializer;
- the caller already holds equal execution privilege;
- only a parse error, log injection, error text, or best-practice concern exists;
- the candidate is archived, test-only, fixed, known, duplicate, or out of scope;
- proof requires live commands, secrets, credential replay, third-party data, persistence, destruction, or unauthorized targeting.

If no candidate survives, return **NO VALID FINDING**.
