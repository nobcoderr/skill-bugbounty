# Reparse, Configuration Grammar, and Provenance Method

`REPARSE_CONFIG_PROVENANCE:v1`

## Purpose and status

Use this method when untrusted stored content, package metadata, URLs, multipart
fields, or import attributes cross a decoder, a second parser, a configuration
grammar, a signed-to-ambient namespace boundary, or a generated model setter
before reaching an authority-bearing consumer.

The lineages below are **PUBLIC / FIXED / PRIOR ART**. They are regression
seeds, not findings, payload libraries, or authority to exercise a live target.

| Historical lineage | Reusable boundary | Public record |
|---|---|---|
| GitLab ReferenceRedactor | encoded recovery text -> attribute decode -> markup reparse | GitLab issue `#213273`; fixed in GitLab 13.1.2 |
| GitLab PyPI simple index | stored package metadata -> string-built HTML attribute -> browser document | GitLab issue `#215640`; fixed in GitLab 13.1.2 |
| Gitaly repository import | URL data -> Git configuration-key grammar -> Git/curl network behavior | GitLab issue `#215212`; fixed in GitLab 13.2.3 |
| GitLab Workhorse multipart middleware | signed rewritten field -> nested parser identity -> ambient path override -> file open | GitLab issue `#214636`; fixed historical release |
| GitLab project import and CarrierWave | imported attribute -> generated virtual setter -> network side effect | GitLab issue `#212089`; `CVE-2020-10956`; fixed in GitLab 12.9.1 |

Do not perform a real file read, special-namespace enumeration, live SSRF,
metadata-service access, public callback, credential access, destructive
request, command execution, or public-service reproduction. Use inert parser
fixtures, synthetic records, fake model setters, loopback-only stubs, and
disposable files owned by the test.

## Unified theorem and invariant

```text
untrusted stored/import/request representation
  -> decode, parser, namespace, or provenance drift
  -> downstream grammar or authority consumer
  -> protected effect
  -> independently proven terminal impact
```

> An untrusted carrier must not gain syntax, configuration authority,
> filesystem identity, or network authority merely because it is decoded or
> reparsed, reserialized, projected through another parser, or assigned to a
> virtual setter.

Structured process arguments alone do not prove safety when one argument is
itself interpreted as an HTML fragment, configuration key, URL subsection,
multipart namespace, or model-assignment instruction.

## Required representation and provenance ledger

Record each stage independently:

1. untrusted carrier and raw representation;
2. every parse, entity decode, percent decode, normalization, and serialization;
3. representation validated and representation actually consumed;
4. output or configuration grammar at the final consumer;
5. trusted provenance source and all ambient override surfaces;
6. generated or virtual setters and their assignment order;
7. downstream authority consumer;
8. intermediate protected effect;
9. terminal impact edge;
10. closest one-variable safe sibling and patched control.

If decode count, parser order, field identity, setter order, release
reachability, or the terminal edge is inferred rather than observed, retain
`NEEDS_REPARSE_PROVENANCE_PROOF`.

## Family A: trusted recovery text is decoded and reparsed as markup

Trace the exact sequence:

```text
source text -> initial HTML parse -> attribute storage -> attribute decode
  -> redaction/recovery -> string serialization -> second HTML parse -> DOM
```

Maintain a decode-depth ledger for every entity and encoding layer. Recovery
content that is semantically text must be inserted with a text-node API or
escaped for the new output context. A value safely encoded for an attribute is
not automatically safe when later used as element content or parsed as an HTML
fragment.

Before KILL, prove that the recovery path never reparses attacker-controlled
text as markup, including unauthorized/redacted views and notification or
cached-rendering variants. CSP is a mitigation at the script-execution edge;
it is not proof that markup generation is safe.

## Family B: stored metadata becomes a generated HTML document

Inventory every stored field used by the document generator, not only visible
text. Record whether each field enters text, quoted attribute, URL, CSS, script,
or raw-fragment context and require context-appropriate encoding or a typed
builder.

Also test document composition across records and ordering. Two individually
inert record fragments may become active when concatenated by a presenter,
template, cache, or pagination layer. An API route that returns HTML is a web
rendering sink even if it is named a package or machine-client endpoint.

Separate these claims:

- malformed or injected markup;
- browser parsing into active DOM;
- script execution under the actual content type and CSP;
- victim reachability and terminal account or data impact.

## Family C: data enters a secondary configuration grammar

Trace:

```text
attacker URL/data -> application URL parser -> config-key/subsection builder
  -> Git/config parser -> selected config option -> network client behavior
```

Build an explicit table for fixed key name, subsection, value, separator,
quoting, normalization, and downstream option precedence. A safe argv boundary
does not prevent injection into the grammar of a single `-c` value. Treat URLs
as data values only; construct security-sensitive configuration keys from
trusted constants or use a dedicated credential channel.

Prove network reachability, redirect/proxy/DNS prerequisites, target asset, and
response channel separately. A changed configuration value is an intermediate
effect, not automatically a reportable SSRF or secret read.

## Family D: signed multipart provenance is lost across parser namespaces

Build a field-identity ledger:

| Stage | Evidence |
|---|---|
| signed carrier | exact field name, path/value, issuer, and integrity scope |
| first parser | raw key and rewritten-field mapping |
| nested parser | brackets, duplicates, arrays/hashes, nil/empty projection |
| merge | precedence between signed data and ambient query/form parameters |
| consumer | exact value and provenance actually opened or moved |

The consumer must use the exact signed value from a typed trusted carrier.
Reject duplicate or colliding ambient names. Do not reconstruct trust by
re-parsing a field name and then reading a same-named ambient parameter.

Lexical allowed-root checks are not enough. Prove final object identity at open
time, including link, descriptor, and special-namespace aliases, with no-follow
and root-bound semantics where available. Safe tests use a mocked opener and
synthetic aliases; never enumerate process identifiers or descriptors.

## Family E: import attributes invoke generated or virtual setters

Attribute inventories must include generated methods, aliases, nested writers,
upload-library remote setters, callbacks, and assignment-time side effects.
Apply a strict positive import allowlist before model construction or mass
assignment.

Record scalar, hash/nested, multiparameter, callback, validation, persistence,
and worker phases. Assignment order is security evidence: a header/config
setter assigned after a URL setter cannot affect a request already issued.
Preserve that negative result instead of inflating the base primitive.

Separate setter reachability, the first network request, redirect behavior,
headers, response persistence, user-visible output, and terminal impact. A
source-level virtual setter is not enough without the shipped import path and a
controlled consumer observation.

## Cross-family reparse and provenance KILL challenge

Use these statuses:

- `DO_NOT_KILL`: complete evidence shows an untrusted carrier reaches an
  authority consumer, provenance or representation invariants fail, and a
  protected effect is observed.
- `NEEDS_REPARSE_PROVENANCE_PROOF`: a parser/decode/assignment/terminal edge is
  missing, ambiguous, or only source-inferred.
- `KILL_ALLOWED`: complete evidence shows no authority reach, or the exact
  representation/provenance invariant holds and the claimed protected effect
  is absent. Kill only the disproven claim; a narrower surviving primitive must
  be judged independently.

Before KILL, answer all of:

1. Which representation was validated and which was consumed?
2. How many decodes/parses occur, in which contexts, and with which grammar?
3. Can multiple records or parameter namespaces compose or collide?
4. What exact provenance was signed, and did the consumer retain it?
5. Which virtual setters exist and in what assignment order?
6. What authority-bearing consumer ran?
7. Was the intermediate effect separated from terminal impact?
8. Did a closest safe sibling and patched control behave as expected?

## Safe proof ladder

1. source and patch trace;
2. parser/decode/assignment-order unit fixture;
3. typed fake consumer or mocked opener/network adapter;
4. baseline and closest one-variable negative control;
5. patched control;
6. isolated end-to-end fixture with synthetic data only;
7. manual confirmation only when explicitly authorized.

Only `STRONG + MANUALLY_CONFIRMED` with current scope, release reachability,
prior-art clearance, negative control, cleanup, and an independently proven
terminal edge is report-ready.

## Remediation patterns

- Keep text as text; escape at the final context or use typed DOM/template APIs.
- Encode every stored field for its actual output context and test multi-record
  composition.
- Keep user data out of configuration-key and option-name grammars.
- Carry signed values in typed objects and reject ambient namespace collisions.
- Bind filesystem authorization to the object opened, not a lexical path.
- Allowlist import attributes before assignment and exclude side-effect setters.
- Make assignment order explicit and test it.
- Add negative controls for decode depth, duplicate fields, aliases, safe
  protocols, safe setters, and patched behavior.
