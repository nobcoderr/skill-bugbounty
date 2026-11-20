# Path, CLI Grammar, and Gadget-Chain Method

`PATH_CLI_GADGET_CHAIN:v1`

## Purpose and status

Use this method when untrusted path-like text, a repository ref, rendered
markup, or another apparently ordinary value is later consumed as a filesystem
object, command-line option, working-tree selector, DOM fragment, or input to a
shipped JavaScript gadget. It is designed to prevent three recurring mistakes:

1. treating a regex or route match as filesystem authorization;
2. treating argv construction as safe even though one argv token still enters
   the option grammar of the child program; and
3. treating sanitizer output as terminal even though shipped JavaScript later
   reparses an allowed attribute or subtree.

The lineages below are **PUBLIC / FIXED / PRIOR ART**. They are regression
seeds, not current findings, payload libraries, or permission to exercise a
live service.

| Historical lineage | Reusable boundary | Public record |
|---|---|---|
| GitLab UploadsRewriter issue move | markdown path capture -> uploader lookup -> cross-project copy -> arbitrary file read | [GitLab issue #212175](https://gitlab.com/gitlab-org/gitlab/-/issues/212175); fixed in GitLab 12.9.1 |
| Gitaly Search API `wiki_blobs` | request ref -> Git `log` option grammar -> controlled local file effect -> capability bridge | [Gitaly issue #1801](https://gitlab.com/gitlab-org/gitaly/-/issues/1801); fixed in GitLab 12.1.6 |
| Gitaly Commits API | request ref -> multiple Git subcommands -> overwrite or truncation with ordering/platform constraints | historical Gitaly issue `#1799`; fixed in GitLab 12.1.6 according to the disclosed report |
| GitLab RDoc wiki rendering | admitted structural markup -> shipped JavaScript gadget -> active DOM/script edge | historical GitLab FOSS issue `#65335`; fixed in GitLab 12.4.1 according to the disclosed report |
| Gitaly Search API `blobs` patch variant | sibling scope -> Git `grep` option grammar -> working-directory read channel | [Gitaly issue #1892](https://gitlab.com/gitlab-org/gitaly/-/issues/1892); fixed in GitLab 12.3.2 |

Do not reproduce these historical payloads. Never test real traversal, file
read/write, protected configuration, command flags against public services,
credential or key acquisition, cookie signing, unsafe deserialization, SSH,
internal APIs, live XSS, destructive effects, races, flooding, or denial of
service. Use synthetic roots, fake argv consumers, inert DOM fixtures, test
keys, and isolated canary consumers owned by the researcher.

## Unified theorem and invariant

```text
untrusted reference, ref, or markup
  -> admission parser, regex, or model
  -> path, CLI, or DOM secondary grammar
  -> authority-bearing consumer
  -> file or DOM effect
  -> separately proven capability bridge and terminal impact
```

> Validation must bind the exact canonical object and grammar token or
> capability that the consumer uses. An intermediate representation that is
> safe in isolation must remain safe through every downstream consumer.

This implies two independent proof obligations:

- **primitive proof:** the exact path, argv token, or DOM value reaches the
  consumer and produces the claimed file/DOM effect; and
- **impact proof:** every bridge from that effect to secret acquisition,
  signing authority, authentication, deserialization, code execution, account
  action, or another terminal consequence is reachable and observed under the
  same shipped environment.

Never upgrade a file read, file overwrite, truncation, malformed DOM, or stored
markup primitive to RCE merely because a historical product once had a
compatible bridge.

## Required path, grammar, and gadget ledger

Record each stage independently:

1. untrusted carrier and attacker authority;
2. admission parser, regex, route, model, and capture groups;
3. all decode, normalization, canonicalization, and serialization stages;
4. value validated and exact value consumed;
5. path root, descriptor/object identity, or argv grammar boundary;
6. every downstream subcommand, renderer, cache, worker, and browser consumer;
7. working directory, environment, release, feature, browser, and platform;
8. observed file or DOM effect;
9. secret or capability bridge, if claimed;
10. serializer or gadget activation, if claimed;
11. terminal impact edge;
12. closest one-variable safe sibling;
13. patched control and sibling/variant controls;
14. cleanup and authoritative read-back.

If the exact consumed object/token, command mode, downstream gadget, platform,
or terminal bridge is inferred rather than observed, retain
`NEEDS_PATH_CLI_GADGET_PROOF`.

## Family A: path capture is not path authorization

A path-shaped regex proves only that text has a shape. It does not prove that
the resulting object is beneath an authorized root, belongs to the expected
tenant/project, remains the same object between validation and use, or is a
regular file.

Trace the complete path:

```text
stored reference -> capture/decode -> uploader or path builder
  -> normalize/canonicalize -> existence check -> open/copy/move
  -> newly reachable object
```

Before KILL, prove all of the following:

- the accepted relative-name grammar excludes absolute, parent, separator,
  alternate-separator, device, stream, and encoded traversal semantics;
- the final canonical object is contained beneath the expected root;
- link, mount, descriptor, and special-namespace aliases cannot change the
  identity at open/copy time;
- the authorization decision applies to the same source object and destination
  object actually consumed;
- the file type and ownership/tenant relationship are expected; and
- every copy/move/rewrite path uses the same invariant.

Prefer root-bound descriptor APIs, no-follow semantics, regular-file checks,
and an allowlisted relative-name grammar. A lexical prefix, `exists?` check, or
uploader object alone is not sufficient evidence.

### Path impact separation

Keep these edges distinct:

```text
path escape -> synthetic file read/copy
  -> protected secret or signing material
  -> usable signing/authentication capability
  -> compatible serializer or privileged consumer
  -> isolated canary effect
```

A proven file primitive survives as its own candidate even when the later RCE
claim is unproven. The RCE claim remains non-reportable until every bridge is
demonstrated with synthetic material in an isolated test environment.

## Family B: argv data can become downstream option grammar

Avoid the false rule “no shell means no injection.” A process can receive a
perfectly structured argv array and still interpret an attacker-controlled
token as an option, revision expression, pathspec, configuration directive, or
mode selector.

Build a per-consumer table:

| Consumer | Token position | Grammar expected | Option termination | Ref/path validation | Working directory | Observable effect |
|---|---|---|---|---|---|---|
| subcommand A | exact index | ref, path, or expression | exact placement | exact validator | explicit | fixture only |
| subcommand B | exact index | ref, path, or expression | exact placement | exact validator | explicit | fixture only |

For every subcommand, prove:

- the token cannot be interpreted as an option in that exact position;
- trusted flags are constants and option/value pairs cannot be split or
  reinterpreted;
- option termination is supported and placed before all untrusted operands;
- strict typed validation matches the intended ref/path grammar;
- mode-changing flags cannot make the working directory, untracked files, or a
  different object namespace visible;
- output destination and output bytes are separately constrained; and
- error, caching, retry, and multi-command order cannot turn a transient effect
  into a stable protected-file effect.

Do not generalize safety from one Git subcommand, one search scope, or one
patched call site. Git subcommands have different grammars and effects. Sweep
all sibling endpoints and wrappers that pass the same semantic `ref`, revision,
path, or search selector.

### CLI impact separation

Classify evidence in this order:

1. attacker-controlled token reaches child argv;
2. child parses it as a different grammar class;
3. a synthetic read/write/truncate/mode effect is observed;
4. destination or returned data crosses a protected boundary;
5. content is sufficiently controlled and stable;
6. deployment/platform/retry/order prerequisites hold;
7. a protected capability actually accepts the resulting state; and
8. terminal privilege or execution is independently proven.

An observed argv token, a child error, or a zero-length fixture is not by
itself RCE. Preserve platform and reliability limits rather than borrowing the
best historical outcome.

## Family C: sanitizer output can activate through a shipped gadget

The security boundary is the final DOM and all code that consumes it, not only
the sanitizer's static output. An allowlisted element, class, `title`, `data-*`,
or other inert-looking attribute can become active when application JavaScript
reads it and inserts it through an HTML parsing API.

Trace both graphs:

```text
markup source -> renderer -> sanitizer -> static DOM
static DOM -> shipped listener/widget -> attribute read -> string composition
  -> HTML/URL/script sink -> activated DOM -> terminal action
```

Before KILL, prove:

- the exact renderer and sanitizer configuration used by the shipped page;
- final structural DOM, including parser repair and element nesting;
- the selector and lifecycle conditions that activate the shipped gadget;
- whether the gadget treats attacker content as text, typed data, URL, or HTML;
- event/user-interaction requirements;
- CSP, Trusted Types, content type, origin, and nonce behavior at the actual
  execution edge; and
- the terminal account/data action separately from script execution.

CSP is defense in depth, not proof that sanitizer output is safe. Conversely,
static DOM injection is not script execution until the actual gadget and policy
conditions are observed. Prefer text-node APIs, typed attributes, strict URL
builders, and removal of dynamic HTML construction.

## Patch-variant and sibling sweep

For a fix, reconstruct the missing invariant rather than matching the old
literal. Sweep:

- all path rewriters, upload movers, copy helpers, and storage backends;
- all API/UI endpoints carrying the same ref/revision/path semantic;
- every Git or other child-process subcommand and argument position;
- working-tree/no-index/config/output modes and wrapper-level defaults;
- all supported wiki/markup formats, sanitizers, and client-side gadgets;
- cached, notification, background-worker, and delayed render variants; and
- every release/backport branch claimed to be fixed.

A patch for one scope or subcommand is only a local fix until centralized
validation and sibling negative controls prove the invariant everywhere.

## Safe proof ladder

Use only researcher-owned local fixtures:

- **P0:** source trace and exact consumer inventory;
- **P1:** parser/canonicalizer or argv-construction unit test;
- **P2:** fake filesystem/command/DOM consumer records the exact value;
- **P3:** disposable synthetic root or inert browser fixture shows the base
  file/DOM effect;
- **P4:** closest safe sibling and patched control remain unaffected;
- **P5:** a synthetic capability bridge uses test-only material;
- **P6:** an isolated canary proves the terminal edge without shell, external
  network, real credentials, persistence, or destructive action.

Stop at the lowest level that answers the evidence question. P0-P4 can retain
a base primitive; P5-P6 are required only for a higher-impact chain claim.

## Cross-family KILL challenge

Use these statuses:

- `DO_NOT_KILL`: complete evidence shows untrusted data reaches a secondary
  path/CLI/DOM grammar, the exact-consumer invariant fails, and the claimed
  protected effect is observed. Every terminal claim included in the candidate
  must also be proven.
- `NEEDS_PATH_CLI_GADGET_PROOF`: object/token identity, subcommand behavior,
  gadget activation, environment, reliability, or a claimed terminal bridge is
  incomplete or source-inferred.
- `KILL_ALLOWED`: complete evidence shows the untrusted value cannot reach the
  authority consumer, or canonical/grammar identity is preserved and the
  claimed protected effect is absent. Kill only the disproven claim.

Before KILL, answer all of:

1. What exact value was admitted, validated, and consumed?
2. Is the consumer interpreting it as a path, operand, option, expression,
   markup, URL, text, or another grammar?
3. What final object/token/DOM identity was observed?
4. Which subcommands, workers, renderers, browsers, and platforms were tested?
5. What protected file or DOM effect was observed?
6. Which capability and serializer/gadget bridges are claimed, and which were
   independently proven?
7. Does a one-variable safe sibling remain safe?
8. Does the patched control reject the root cause across sibling consumers?
9. Are current release reachability, prior art, cleanup, and manual status
   complete?

Only a current, in-scope, non-duplicate candidate with complete source/runtime
evidence, baseline, negative and patched controls, cleanup, and
`STRONG + MANUALLY_CONFIRMED` is report-ready.

## Remediation and regression guidance

- Parse path references into typed identifiers, then resolve them through a
  root-bound storage API that checks final object identity at use time.
- Use trusted constant flags, explicit option termination, strict typed ref or
  path validation, and tests for every child subcommand.
- Set an explicit safe working directory and prevent mode changes that broaden
  the child process's object namespace.
- Preserve sanitizer guarantees through client code: use text insertion and
  typed builders, and audit every dynamic HTML gadget.
- Centralize the invariant so API/UI/search/import/move variants cannot drift.
- Assert the intermediate primitive and each terminal bridge separately in
  regression tests.

The package's deterministic fixtures are in
`config/PATH_CLI_GADGET_CHAIN_REGRESSION_CASES.json` and are evaluated by
`automation/test-path-cli-gadget-chain.py`. They are network-free and contain
no operational payloads.
