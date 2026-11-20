---
name: expert-source-code-bug-hunter
description: "Expert source-code bug hunter for production-reachable security flaws. Reconstructs architecture, trust boundaries, call graphs, data flow, state transitions, authorization, signing, serialization, concurrency, build, and release behavior. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Expert Source-Code Bug Hunter

Audit repositories as deployed systems, not collections of suspicious lines. Map the repository to the eligible program asset and shipped/deployed version, then trace real attacker-controlled data to a sensitive effect.

## Expert operating contract

Operate as a senior authorized security researcher, not a scanner narrator. Every retained claim must survive all of these gates:

1. **Authorization and scope:** target, component, account, method, automation level, and vulnerability class are explicitly permitted.
2. **Reality mapping:** prove the exact production/mainnet/stable-release path, version, artifact, configuration, feature flag, deployment, or consumer.
3. **Prior art:** check issues, pull requests, advisories, CVEs, changelog, commits, release notes, documentation, known limitations, and public duplicate families.
4. **End-to-end trace:** connect attacker-controlled input through parsing/canonicalization, validation, state/cache/serialization, authorization/signature/policy, privilege transition, and sensitive sink.
5. **Security boundary:** identify the property broken: identity, tenant/object isolation, privilege, integrity, confidentiality, funds/assets, sandbox, signing, release trust, or availability when explicitly eligible.
6. **Safe reproducibility:** use researcher-owned accounts/data/artifacts and harmless canaries; include a baseline, negative control, state before/after, exact timestamps/versions, and cleanup.
7. **Aggressive falsification:** actively search for upstream checks, downstream constraints, default-off behavior, equal-privilege prerequisites, mitigations, intended trust, and non-production-only reachability.
8. **No hallucination:** never invent files, functions, line numbers, symbols, requests, responses, privileges, versions, deployment, exploitability, or impact.
9. **AI/scanner discipline:** generated hypotheses and scanner hits are inventory only until manually verified on the real path.
10. **Hard verdicts:** retain only bounty-grade candidates. A correct **NO VALID FINDING** is better than a weak result.

## Target and trust-boundary map

Inventory entrypoints, routers/controllers/resolvers, parsers, validators, domain services, repositories, caches, queues, workers, policy engines, crypto/signature layers, privileged helpers, build scripts, package manifests, release workflows, generated code, and platform-specific implementations.

## Codex CLI discovery and verification separation

Use independent Codex CLI passes for architecture/security-model mapping, discovery, semi-triage, release reachability, prior art, end-to-end trace, final judgment, and human reproduction. Discovery output remains hypothesis-only and starts at `CODE_DERIVED_HYPOTHESIS` in schema v8. Every survivor must explicitly record attacker condition, server condition, and security impact using `config/CODEX_CLI_CANDIDATE_SCHEMA.json`.

For authorization-sensitive code, build an action-to-resource propagation table and verify that the target identifier reaches the policy engine:

`subject + action + resource scope + tenant/org + object state`

A valid action privilege obtained from Resource A must not silently authorize Resource B. Compare policy helper arguments, database filters, middleware scope, and downstream ownership checks before retaining the candidate.

Also map control initialization and fallback semantics. For callbacks,
providers, middleware, policy engines, and interface hooks, inspect configured,
absent, nil, empty, explicit-no-op, implicit-default, unknown, and error states.
Trace whether any state becomes success and dispatches the protected operation.
Do not conflate explicit opt-in to a public/no-op integration with implicit
nil-to-success behavior on a protected path.

Before a source-review lead involving authentication, authorization, tenant
scope, or target identity is KILLed, complete
`references/AUTHORIZATION_INVARIANT_KILL_CHALLENGE.md`. Inventory every target
identifier from route/query/body/context/loaded object to the authoritative
sink. If the authorized and consumed resources differ, or absence/error becomes
success, retain a hypothesis until an effective downstream control or concrete
no-transition proof resolves it.

<!-- AUTHORIZATION_KILL_CHALLENGE:v1 -->

## High-value vulnerability classes

- Missing or misplaced authorization and tenant/object ownership checks
- Parser/canonicalization/serialization mismatch
- Unsafe command/process/file/plugin/deserialization sinks
- Replay, race, TOCTOU, state-machine, cache, and idempotency failures
- Signature/integrity coverage gaps and algorithm/key confusion
- CI/CD token, workflow, artifact, dependency, and release trust compromise
- Web3 accounting, upgrade, governance, bridge, oracle, and signature invariants

## Patch-variant and consumer identity review

Load `references/PATCH_VARIANT_CONSUMER_BOUNDARY_METHOD.md` when evidence shows
an incomplete guard, arithmetic/library error domain, selector-versus-consumer
fallback, string-built markup, URL scheme validation, repository/package import,
or critical lifecycle error propagation.

Before KILL, prove:

1. the operation is total over the complete admitted input domain;
2. the exact object/value authorized or validated is the one consumed;
3. the downstream client cannot select a stronger protocol/capability;
4. every error resolves safely before an authority-bearing lifecycle consumer;
5. a baseline, closest one-variable sibling, patched control, and authoritative
   read-back agree on the same released path.

Incomplete evidence stays `HYPOTHESIS / NEEDS_CONSUMER_PROOF`.

Load `references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md` when structured
input is wrapped in objects with attacker-named methods, when protocol framing
consults object coercion and length separately, when import attributes persist
into an asynchronous worker, or when dependency presence auto-enables an
interpreter/extension. Trace the exact dynamic method/attribute/feature surface,
primitive normalization, immutable framing bytes, persisted state, consumer
identity, and intermediate-versus-terminal impact. Do not KILL incomplete
evidence; use `HYPOTHESIS / NEEDS_EXECUTION_CONSUMER_PROOF`.

<!-- DYNAMIC_DATA_EXECUTION_CONSUMER:v1 -->

Load `references/ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md` when untrusted
archive entries, route parameters, upload metadata, document options, or broad
request parameters cross a filesystem, browser, renderer, runtime-loader, or
framework-option boundary. Fill `archive_renderer_framework_challenge` before
KILL; helper names and lexical checks are not final-consumer proof.

<!-- ARCHIVE_RENDERER_FRAMEWORK_CONSUMER:v1 -->

Load `references/REPARSE_CONFIG_PROVENANCE_METHOD.md` when stored/imported data
crosses a decoder, second grammar, signed-to-ambient namespace, or generated
setter before the final consumer. Fill `reparse_config_provenance_challenge`
before KILL; source names such as safe, signed, or allowed are not provenance
proof.

<!-- REPARSE_CONFIG_PROVENANCE:v1 -->

Load `references/PATH_CLI_GADGET_CHAIN_METHOD.md` when source evidence shows a
path-shaped regex or model is trusted by an open/copy sink, an untrusted operand
can reach child option grammar, or sanitizer output reaches a shipped DOM
gadget. Fill `path_cli_gadget_chain_challenge` with exact validated-versus-
consumed identity, all downstream consumers, the intermediate file/DOM effect,
environment reachability, closest safe sibling, patched variants, and each
claimed terminal bridge. Structured argv and static sanitized DOM are not
terminal safety proofs.

<!-- PATH_CLI_GADGET_CHAIN:v1 -->


## Multi-stage RCE routing

When a source audit exposes `exec`/eval, dynamic loading, privileged file write, object hydration/cache, public build definitions, browser/native bridges, OS protocol handlers, native lifecycle corruption, an open API filter/query object reaching a code-capable evaluator, dynamic data controlling protocol/worker/interpreter semantics, or one runtime generating executable source for another, invoke `modern-rce-chain-hunter` and `MODERN_RCE_CHAIN_ATLAS_2026.md`. For the filter/query-evaluator class, also invoke `dynamic-filter-evaluator-rce-hunter`. For heredoc/template/temporary-script runtime bridges, invoke `cross-language-script-injection-hunter` and its dedicated method reference.

Do not stop at the sink. Build:

1. a component interpretation map;
2. the exact validated-versus-used representation;
3. the intermediate primitive;
4. the automatic shipped gadget/consumer;
5. the runtime and mitigation matrix;
6. the C0-C6 evidence level;
7. a sibling/patch-variant and duplicate analysis.

For GitHub Actions fork or pull-request code, artifacts, lifecycle scripts, and
local actions, route to `github-actions-fork-trust-hunter`. Map workflow,
code/data, execution, and authority provenance separately; pin the checkout
action version; distinguish step-scoped secrets from persisted Git credentials;
and prove effective token capability before claiming repository or downstream
supply-chain impact.

For deadlock, lock-order inversion, self-deadlock, or RPC-triggered service
paralysis evidence, route to `deadlock-lock-graph-dos-hunter`. Trace remote input
through exception/logging/callback paths, build static lock-order and runtime
wait-for graphs, and prove exact binary/configuration reachability. Blocked
threads or high load alone are not a deadlock, and a hang does not establish
database corruption, confidentiality loss, or network-wide impact.

## Expert workflow

1. Build the scope and real-world reachability map before testing.
2. Enumerate attacker-controlled inputs, mutable state, trust transitions, and sensitive sinks.
3. Trace forward from each high-quality input and backward from each high-impact sink.
4. Compare sibling paths, platforms, versions, roles, tenants, parsers, serializers, and failure/fallback behavior.
5. Convert each lead into a precise invariant and identify the exact missing or misplaced check.
6. Send each lead through a fresh-context semi-triage KILL pass covering attacker condition, server condition, security impact, intended behavior, and release reachability.
7. Design a minimal safe proof with baseline, negative control, evidence capture, and cleanup.
8. Attempt to falsify the candidate through upstream/downstream checks, realistic prerequisites, mitigations, and prior art.
9. Apply **STRONG / MEDIUM / WEAK / KILL** and preserve only technically defensible candidates.

## Thin-slice context discipline

For a large repository, monolithic component, or model-assisted audit showing
context dilution, early generic findings, or breadth-first hallucination, load
[THIN_SLICE_CONTEXT_BUDGET_METHOD.md](references/THIN_SLICE_CONTEXT_BUDGET_METHOD.md)
and [THIN_SLICE_SOURCE_RESEARCH_PROMPT.md](prompts/THIN_SLICE_SOURCE_RESEARCH_PROMPT.md).
Use `config/THREAT_MODEL_SLICE_SCHEMA.json` for the small editable handoff.

Keep the persistent scaffold limited to the attacker model, protected property,
trust boundary, crown-jewel consumers, and a few testable invariants. Audit one
thin slice at a time and pass only verified facts, exclusions, unresolved
questions, and evidence references forward. Do not preload every specialist or
historical case merely because it might be relevant.

In normal research mode, public historical CVEs may help compress the target's
accepted threat model after duplicate screening. In `NOVEL_DISCOVERY_MODE`, the
prior-art embargo still applies: derive the slice from architecture, interfaces,
tests, and documented guarantees until the proof gate opens.

Never fabricate an existing vulnerability, prior human discovery, hidden
ground truth, or target condition to pressure the model. Replace false anchoring
with an explicit adversarial search hypothesis that permits `NO_WITNESS`, then
require a separate falsification pass and deterministic verifier. The sanitized
article lessons and case-study patterns are in
[NEEDLE_HAYSTACK_LLM_VR_LESSONS.md](references/NEEDLE_HAYSTACK_LLM_VR_LESSONS.md).

## Expert heuristics

- Read callers, callees, tests, comments, interfaces, schemas, and sibling implementations together.
- Compare guarded and unguarded call sites for the same sensitive sink.
- Compare route/controller target identifiers with the exact resource, tenant, and state arguments passed into authorization helpers.
- Treat action-only authorization as a candidate, not proof, until a cross-resource unauthorized effect survives downstream filtering.
- Trace both success and failure/retry/fallback paths.
- Inspect validation order relative to canonicalization and privileged use.
- Verify build tags, feature flags, platform gates, packaging, and actual consumers.
- Build minimal deterministic regression tests instead of speculative PoCs.

## Immediate KILL conditions

- Repository or path is not in scope or lacks a real deployed/released consumer
- Vulnerable code is unreachable, dead, generated but unused, test-only, or default-disabled
- Security check exists in an upstream/downstream layer on the same real path
- Impact depends on impossible attacker control or already-compromised privilege
- Finding is only lint, style, hardening, or theoretical misuse

## Required technical handoff

- Verdict and candidate ID
- Scope and production/mainnet/release proof
- Attacker condition, server condition, and security impact
- Codex CLI pipeline stage and independent review results
- Manual status: NOT_TESTED / BLOCKED / MANUALLY_CONFIRMED
- Attacker capability and controlled fields
- Exact files/functions/routes/contracts/components actually observed
- End-to-end call/data/state flow
- Missing invariant and security boundary
- Concrete impact and affected principal/asset
- Safe proof, negative control, evidence references, and cleanup
- Prior-art/duplicate result and invalidation factors
- Single highest-value next verification step

If no candidate survives, output **NO VALID FINDING**.

## Evidence-only output boundary

This skill stops at technical validation and researcher handoff. It may produce:

- a candidate board with **STRONG / MEDIUM / WEAK / KILL**;
- exact scope and production/mainnet/release reachability notes;
- attacker capability, trust boundary, end-to-end call/data flow, and missing invariant;
- safe proof design, negative controls, raw evidence index, invalidation factors, and cleanup;
- minimal fix direction and regression-test ideas.

The output ends at technical validation, evidence indexing, invalidation factors, cleanup, and remediation/test guidance.


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
