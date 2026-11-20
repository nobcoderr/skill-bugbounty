# Attack-Surface-to-Chain Bug-Bounty Method

This reference turns the public BugBounty.info taxonomy into an original,
evidence-first operating method for this skill pack. It is a coverage and
reasoning aid, not a payload library, scanner authorization, or substitute for
the target program policy.

## Contents

1. Source and freshness
2. Non-negotiable gates
3. Attack-surface map
4. Primitive-to-chain method
5. Documented chain families
6. Tool selection discipline
7. Source-code adaptation
8. Candidate record
9. KILL rules
10. Safe proof boundary

## 1. Source and freshness

Primary public indexes reviewed on 2026-08-06:

- https://bugbounty.info/Attack-Surface/
- https://bugbounty.info/Chains/
- https://bugbounty.info/Tooling/

The coverage snapshot contained 91 Attack-Surface pages, 20 Chains pages
including the index, and 7 Tooling pages including the index. The site is a
living resource. Re-check its current indexes before relying on changing tool,
platform, or program-specific claims.

Do not copy the site's payloads or prose into reports or automation. Apply the
taxonomy as a set of questions, then independently prove the actual target's
behavior.

## 2. Non-negotiable gates

Before generating or testing a hypothesis:

1. Prove authorization, asset scope, allowed method, rate limit, exclusions,
   abort conditions, and cleanup expectations.
2. Prove target reality: current production, mainnet, stable release, shipped
   artifact, or a documented current consumer.
3. Perform prior-art screening by root cause and missing invariant across open
   and closed issues, open/closed/merged pull requests, discussions,
   advisories, CVEs, commits, changelog, release notes, official docs, known
   issues, and maintainer comments.
4. State the attacker's starting privilege, controlled input/state, network
   position, required victim action, and whether prior compromise is assumed.
5. State the server/version/configuration/feature conditions and the real
   consumer that makes the path reachable.
6. Name the protected boundary and concrete confidentiality, integrity,
   authorization, authentication, tenant, signing, release, or funds impact.
7. Design baseline, positive proof, negative control, state read-back, cleanup,
   and manual reproduction before active testing.

Every scanner, model, static query, grep result, or suspicious sink is only a
`HYPOTHESIS` until the gates above and the end-to-end path are proven.

## 3. Attack-surface map

Classify by the real component being attacked first. A bug class alone does not
determine reachability, proof design, or impact.

### Web applications

Map all applicable families:

- authentication: login, registration, recovery, MFA, session lifecycle,
  cookies/tokens, OAuth/OIDC/SAML, account linking, and device trust;
- authorization: object, property, function, role, tenant, organization,
  ownership, lifecycle state, mass assignment, and indirect object references;
- injection and parsing: SQL/NoSQL, command, template, XML/XXE,
  deserialization, expression, header, path, URL, and parser differentials;
- server-side request initiation: URL fetchers, previews, imports, redirects,
  DNS changes, internal services, cloud metadata, and egress restrictions;
- client-side trust: reflected/stored/DOM XSS, postMessage, DOM clobbering,
  prototype pollution plus a reachable gadget, CSP boundaries, clickjacking,
  redirect handling, storage, and service workers;
- file operations: upload, download, archive extraction, path traversal,
  content-type interpretation, generated files, and executable consumers;
- business/state logic: ordering, race, replay, idempotency, quotas, rewards,
  payments, approvals, invitations, multi-step workflows, and async jobs;
- infrastructure: proxy/cache/CDN behavior, host routing, request boundaries,
  CORS with readable sensitive data, subdomain ownership, DNS, exposed
  management surfaces, and environment separation.

### APIs

Treat REST, GraphQL, gRPC, WebSocket, webhook, and internal/mobile APIs as
distinct protocols and consumers. Map discovery/schema exposure, object and
field authorization, function-level authorization, batching/aliasing, method
and content-type differences, pagination/filtering, version drift, callback
authentication, tenant propagation, and server-side rate controls. API surface
enumeration is not impact by itself.

### Mobile applications

Map Android/iOS package identity, current release provenance, deep/universal
links, exported components, intents/URL schemes, WebViews and native bridges,
local storage/backups/logs/clipboard, IPC, update flow, and the mobile-to-backend
API trust boundary. Hardcoded public identifiers, absent pinning, or local-only
client manipulation are not retained without a protected backend or user-data
impact.

### Cloud infrastructure

Map AWS/Azure/GCP identity and resource boundaries, IAM delegation and
assumption, storage policies, metadata access, serverless events, secrets,
control-plane versus data-plane authorization, network egress, tenant scoping,
and audit trails. Never claim an SSRF-to-cloud escalation without proving the
reachable asset and effective permissions using a harmless, owned test path.

### CI/CD and software supply chain

Map event/trust semantics, pull-request and fork boundaries, workflow tokens,
permissions, secrets, third-party actions, self-hosted runners, checkout order,
untrusted build inputs, caches, artifacts, signing, provenance, registries,
package publication, installers, updaters, and release consumers. A workflow
snippet is insufficient without proving the real trigger identity and shipped
artifact path.

### AI, LLM, agents, RAG, and MCP

Map system/user/retrieved-content trust, direct and indirect prompt inputs,
tool and connector permissions, approval boundaries, RAG provenance, memory and
cache isolation, tenant context, generated code execution, sandbox boundaries,
MCP servers/clients, and model supply chain. Prompt injection, jailbreak, or
undesired text alone is `KILL` unless it crosses a protected product boundary
and produces a program-eligible security impact.

### Web3 and smart contracts

Map deployed contract and chain, upgrade/proxy state, access control,
accounting, reentrancy, callbacks, oracle freshness/manipulation, signature and
nonce/replay rules, rounding, liquidation, governance, bridge consensus,
relayer/signer/node boundaries, and off-chain consumers. Local simulations are
test design evidence; current deployment reachability and owned-funds proof are
still required. Never test destructively on public/mainnet assets.

## 4. Primitive-to-chain method

For every retained primitive, write:

`attacker position -> primitive -> bridge/enabler -> protected boundary -> impact`

Then apply these rules:

1. Describe the new attacker capability obtained from the primitive, not just
   the vulnerability label.
2. Enumerate only components reachable from that new position in the same real
   deployment and victim flow.
3. Identify the exact missing bridge needed for escalation.
4. Trace forward from attacker input and backward from the final sensitive
   sink; both traces must meet on the same runtime/release path.
5. Prove each edge separately with a baseline and negative control before
   claiming the whole chain.
6. Do not combine unrelated theoretical findings to inflate severity.
7. Preserve the weakest prerequisite in the final attacker model. An unlikely,
   prohibited, or already-compromised prerequisite can KILL the chain.
8. Rate only the demonstrated final impact, not the most severe impact the bug
   class is sometimes capable of producing.

## 5. Documented chain families

Use these families as coverage prompts, never as assumed findings:

- CSRF -> account takeover;
- file upload -> executable consumer -> code execution;
- GraphQL function-level authorization failure -> mass data extraction;
- object authorization failure + mass assignment -> privilege escalation;
- object authorization failure -> sensitive identity data -> account takeover;
- information disclosure -> a separately proven exploit path;
- OAuth/OIDC state or redirect validation failure -> account takeover;
- open redirect -> accepted OAuth redirect path -> account takeover;
- indirect prompt injection -> authorized tool action -> protected data exit;
- prototype pollution -> concrete browser or server gadget -> XSS/code execution;
- race condition -> broken financial/state invariant -> measurable loss;
- SSRF -> reachable cloud identity endpoint -> effective privileged action;
- server-side template injection -> harmless code-execution proof;
- self-XSS -> separately proven session-placement/clickjacking bridge -> victim impact;
- subdomain takeover -> accepted OAuth redirect path -> account takeover;
- subdomain takeover -> parent-domain credential/session exposure;
- XSS -> authenticated victim capability -> account takeover;
- stored XSS -> privileged renderer -> unauthorized admin action;
- XXE -> server-side request primitive -> reachable cloud privilege path.

Reject a family when any required edge is unavailable, prohibited, already
public/fixed, third-party-only, or reachable only in an obsolete configuration.

## 6. Tool selection discipline

Select the smallest tool that can answer the current evidence question:

- Burp Suite or an equivalent proxy: capture and manually compare owned
  requests, sessions, object identities, callbacks, and negative controls.
- Browser DevTools: inspect actual DOM/network/storage/message behavior and
  distinguish client assumptions from server enforcement.
- Nuclei: encode a narrowly scoped, non-destructive regression/discovery check
  only after target policy, template behavior, and rate limits are understood.
- ffuf or equivalent content discovery: use only with an explicit allowlist,
  bounded wordlist, rate/concurrency cap, stable baseline filtering, and abort
  condition.
- Local scripts/automation: make deterministic, bounded, logged, resumable, and
  cleanup-aware; avoid secrets and disable unsafe install hooks.
- AI-assisted review: use for architecture mapping, source tracing, test design,
  and falsification. Treat all outputs as hypotheses and manually verify them.

Tool selection is automatic as planning context only. Tool execution is never
automatic. Live recon, scanners, fuzzers, installers, hooks, exploit harnesses,
or state-changing PoCs require explicit task authorization and safety controls.

## 7. Source-code adaptation

For a local repository:

1. Pin commit/tag/artifact and identify the current shipped consumer.
2. Map entrypoints and privileged consumers into the attack-surface taxonomy.
3. Trace attacker-controlled representations through parsing, normalization,
   validation, state/cache/serialization, policy/signature checks, trust
   transitions, and the sensitive sink.
4. Examine cross-layer mismatches: client/server, proxy/app, API/worker,
   workflow/runner, contract/relayer, model/tool, source/package/release.
5. Search prior art by invariant, sink, helper, patch family, and sibling path.
6. Build the smallest harmless proof that differentiates vulnerable and safe
   behavior, then add negative controls and authoritative state read-back.
7. Escalate into a chain only when every edge is proven on the same current
   release path.

For archives, uploads, route parameters, document options, and URL helpers,
also trace the final filesystem object, browser-normalized request, renderer or
secondary loader, runtime class/constructor, and framework-reserved option
namespace. Load `references/ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md` when
these representations cross an authority boundary; a parser-level check alone
does not justify KILL.

For stored recovery content, generated HTML endpoints, URL-derived
configuration keys, signed multipart fields, and imported model attributes,
also trace decode depth, parser order, final output/config grammar, exact
trusted provenance, ambient namespace collisions, generated/virtual setters,
and assignment order. Load `references/REPARSE_CONFIG_PROVENANCE_METHOD.md`;
safe argv, a signature, an allowed-root string, or a sanitized first parse does
not justify KILL when a later grammar or consumer sees a different value.

For upload/reference paths, repository refs or path operands, and sanitized
markup later consumed by application JavaScript, trace the final canonical
filesystem object, the child program's exact option/operand grammar and working
directory, or the runtime DOM/gadget graph. Load
`references/PATH_CLI_GADGET_CHAIN_METHOD.md`. A regex match, argv array, or safe
static DOM is only an intermediate representation. Prove the file/DOM primitive
and every later secret, signing/authentication, serializer/gadget, or terminal
impact edge independently.

## 8. Candidate record

Every candidate ledger entry must include:

- exact attack surface, component, protocol, version, and release consumer;
- vulnerability class and missing invariant;
- attacker position and controlled input/state;
- server/configuration/feature prerequisites;
- primitive obtained;
- bridge/enabler, or `NONE_PROVEN`;
- protected boundary and concrete final impact;
- forward and backward source/runtime traces;
- scope and prior-art evidence with URLs/IDs/commits checked;
- baseline, positive result, negative control, state read-back, cleanup;
- invalidation factors and missing proof;
- verdict: `STRONG`, `MEDIUM`, `WEAK`, or `KILL`;
- manual status: `NOT_TESTED`, `BLOCKED`, or `MANUALLY_CONFIRMED`.

Only `STRONG` plus `MANUALLY_CONFIRMED`, with no unresolved scope,
reachability, duplicate, or chain-edge gap, is report-ready.

## 9. KILL rules

KILL early when the candidate is:

- theoretical, best-practice-only, by design, informative, local-only,
  dev/test-only, outdated, archived, third-party-only, public, fixed, known, or
  duplicate by root cause;
- an exposed identifier, route, schema, version, or source sink without a
  protected-boundary consequence;
- CORS without a cross-origin readable sensitive response;
- open redirect without a separately proven trusted bridge;
- information disclosure without usable secret/capability or proven next edge;
- prototype pollution without a reachable security-relevant gadget;
- SSRF without a reachable sensitive service/asset and effective action;
- cache/proxy behavior without a victim path, stable baseline, and isolation
  controls;
- rate-limit or availability behavior excluded by program policy, or any path
  requiring prohibited DoS/brute force;
- prompt injection/jailbreak without a concrete protected-boundary impact;
- dependent on physical access, prior equivalent compromise, equal privilege,
  implausible victim behavior, or unowned third-party interaction;
- unable to survive authoritative read-back and a negative control.

Do not rescue a burned root cause by renaming or splitting it. End the lane with
`NO VALID FINDING` when nothing survives.

## 10. Safe proof boundary

Prefer harmless canaries, owned accounts/tenants/resources, local test harnesses,
read-only observation, minimal state changes, and immediate cleanup. Do not use
webshells, reverse shells, credential stuffing, phishing, persistence, evasion,
secrets exfiltration, destructive payloads, service disruption, third-party
pivoting, or public/mainnet exploitation. Stop once the minimum safe evidence
needed to prove the protected-boundary impact has been collected.
