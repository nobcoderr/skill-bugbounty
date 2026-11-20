---
name: expert-web-api-business-logic-hunter
description: "Expert web, API, and business-logic bug hunter for REST, GraphQL, gRPC, webhooks, queues, async jobs, SaaS workflows, and multi-tenant products. Focuses on unauthorized actions and state transitions. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Expert Web/API & Business-Logic Hunter

Model the product as identities, objects, permissions, workflows, and side effects. Use researcher-owned A/B/C accounts and synthetic objects to test whether server-side authority and state remain correct across every transition.

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

Map web routes, API versions, GraphQL resolvers, gRPC services, webhooks, callbacks, background jobs, queues, admin/support tools, import/export, billing/order/refund flows, invitations, sharing, ownership transfer, deletion/recovery, OAuth/OIDC, and caches/proxies.

## Route-to-policy scope propagation

For every object-sensitive endpoint, map:

`route target ID -> object/tenant resolution -> authorization subject/action/resource scope/state -> authoritative query or mutation`

Compare whether the requested UID/ID/slug/project/org/tenant is passed to the policy engine. An action privilege derived from one object must not become a global capability. Check middleware, resolver context, database filters, background jobs, and asynchronous consumers before claiming a missing scope check.

Use Codex CLI role isolation: one pass maps the security model, independent discovery passes generate hypotheses, and a fresh semi-triage pass explicitly proves attacker condition, server condition, and security impact.

## Authorization default-state and KILL challenge

For protected routes, resolvers, jobs, and middleware, map who installs the auth
control and what happens when it is absent, nil, empty, explicitly no-op,
implicitly defaulted, successful, unknown, or failing. Confirm whether the
protected handler or authoritative side effect is dispatched in every state.

Collect all resource identities from route, query, body, session/context,
database object, and async payload. The identity used by policy must equal the
identity consumed by the read/write unless a proven downstream constraint binds
them.

Before KILL, complete
`references/AUTHORIZATION_INVARIANT_KILL_CHALLENGE.md`. `Optional`, `named
no-op`, or `looks intentional` is not a KILL reason without documented intent,
preserved invariant, end-to-end trace, and proof that no attacker-controlled
authority transition occurs. Incomplete evidence remains `HYPOTHESIS /
NEEDS_INVARIANT_PROOF`, not a finding.

<!-- AUTHORIZATION_KILL_CHALLENGE:v1 -->

## High-value vulnerability classes

- BOLA/IDOR, BFLA/BAC, tenant isolation, role and ownership bypass
- Invite/share/transfer/revoke/delete/recover state abuse
- Price, quantity, coupon, credit, refund, payout, inventory, or order manipulation
- Webhook signature/replay and async job authorization gaps
- OAuth/OIDC redirect, state, nonce, PKCE, token audience/scope, and session binding failures
- SSRF to protected services, unsafe upload/import/export, cache poisoning, request smuggling differentials
- Import/migration pipelines where a remote party supplies repository/package
  metadata and a downstream worker consumes a broader URL scheme, redirect, or
  local filesystem capability than the validator constrained. Load
  `references/PATCH_VARIANT_CONSUMER_BOUNDARY_METHOD.md`; trace request, queue,
  worker placement, storage authority, imported artifact, and cross-tenant
  read-back.
- Import/API pipelines where a remote response becomes a rich dynamic object,
  supplies broad model attributes, persists execution-adjacent state, or
  reaches a serializer/worker/interpreter. Load
  `references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md`; inventory dynamic
  method/coercion collisions, exact protocol framing bytes, attribute
  allowlists, alternate source-type/feature-gate paths, queued consumers, and
  terminal impact edges separately.
- GraphQL alias/batch/resolver authorization inconsistency
- Browser-to-API approval chains where untrusted page structure or script uses
  an authenticated user's ambient origin to mint an Application Password,
  OAuth grant, API key, or upload capability. Treat explicit user interaction,
  approval state, credential receipt, API permission, content mutation, and
  file/execution consumers as distinct state transitions.

## Expert workflow

1. Build the scope and real-world reachability map before testing.
2. Enumerate attacker-controlled inputs, mutable state, trust transitions, and sensitive sinks.
3. Trace forward from each high-quality input and backward from each high-impact sink.
4. Compare sibling paths, platforms, versions, roles, tenants, parsers, serializers, and failure/fallback behavior.
5. Convert each lead into a precise invariant and identify the exact missing or misplaced check.
6. Design a minimal safe proof with baseline, negative control, evidence capture, and cleanup.
7. Attempt to falsify the candidate through upstream/downstream checks, realistic prerequisites, mitigations, and prior art.
8. Apply **STRONG / MEDIUM / WEAK / KILL** and preserve only technically defensible candidates.

## Expert heuristics

- Build role × tenant × object-owner × state × endpoint × action/resource-scope matrices.
- Trace target IDs from route parameters through policy helper arguments to the final authoritative read/write.
- Replay captured requests while changing exactly one identity/object/state variable.
- Test authorization at action time, not only UI visibility or object lookup.
- Examine stale links, revoked tokens, deleted users, transferred objects, retries, and duplicate callbacks.
- Compare REST/GraphQL/mobile/internal variants and synchronous/asynchronous implementations.
- For import/export, compare the validator's protocol allowlist with the exact
  downstream client and record whether credentials are inserted before or after
  validation.
- For remote import metadata, compare the entire remote object schema with the
  exact model/service fields, persisted state, queue payload, retry/fallback,
  and process API. A UI feature flag or denylist is not proof that alternate
  API/source-type paths are closed.
- Require a concrete unauthorized read/write/action or persistent privilege/financial effect.

## Immediate KILL conditions

- UI-only restriction with correct server-side enforcement
- Self-impact, intended collaboration, public data, or same-tenant action allowed by design
- Rate-limit/CORS/header/version disclosure without impact
- Requires other users’ data or prohibited account interaction
- No reproducible unauthorized state or security-sensitive side effect
- Action-only permission suspicion without proven target-resource/tenant scope omission and cross-object impact
- Dynamic object/import/optional-interpreter suspicion whose primitive
  normalization, real consumer, and protected effect are unproven; keep it as
  `NEEDS_EXECUTION_CONSUMER_PROOF`, not a premature KILL, until the method's
  challenge is complete

<!-- DYNAMIC_DATA_EXECUTION_CONSUMER:v1 -->

For bulk uploads/imports, cross-origin method override, notification rendering,
async viewer URLs, or framework helper options, load
`references/ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md`. Bind business
workflow reachability to the exact entry/object/value consumed, browser and
framework normalization, secondary consumers, and authoritative end effect.

<!-- ARCHIVE_RENDERER_FRAMEWORK_CONSUMER:v1 -->

For generated HTML endpoints, signed upload handoffs, repository/import URL
configuration, or mass-assignment into side-effectful virtual setters, load
`references/REPARSE_CONFIG_PROVENANCE_METHOD.md`. Bind workflow reachability to
the exact parsed value, provenance source, assignment phase, authority
consumer, and authoritative effect.

<!-- REPARSE_CONFIG_PROVENANCE:v1 -->

## Workflow path, CLI, and client-gadget boundaries

Load `references/PATH_CLI_GADGET_CHAIN_METHOD.md` when a move/import/search/wiki
workflow carries a path, ref, or markup value into a later file, process, or
DOM consumer. Bind workflow authorization to the same canonical source and
destination objects, test every asynchronous/sibling scope and subcommand, and
record browser/gadget activation. Treat file read/write/truncation, DOM
activation, protected capability acquisition, and terminal impact as distinct
claims. Fill `path_cli_gadget_chain_challenge` before KILL.

<!-- PATH_CLI_GADGET_CHAIN:v1 -->

## Required technical handoff

- Verdict and candidate ID
- Scope and production/mainnet/release proof
- Attacker condition, server condition, and security impact
- Route-to-policy target-resource/tenant/state propagation
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
