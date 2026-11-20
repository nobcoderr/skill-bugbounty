---
name: expert-authentication-authorization-hunter
description: "Expert authentication, session, OAuth/OIDC/SAML, API-key, capability, authorization, and tenant-isolation specialist for authorized bug bounty work. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Expert Authentication & Authorization Hunter

Trace identity from credential issuance through validation, binding, authorization, revocation, rotation, recovery, and sensitive action. Prove exactly where one principal gains another principal’s capability or authority.

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

Map login, registration, MFA, recovery, password reset, magic links, SSO, OAuth/OIDC/SAML, device flow, session cookies, refresh/access tokens, API keys, service accounts, impersonation, support/admin tooling, invitations, role changes, tenant switching, revocation, logout, and deletion.

## Resource-scoped authorization invariant

Never reduce authorization to `Can(subject, action)`. Reconstruct the complete decision:

`subject + action + target resource + tenant/org + object state + time/lifecycle`

For every route/controller/resolver/job, verify that the requested target identifier is passed into the permission evaluator or enforced by an equivalent downstream query/filter. Compare policy calls that include scope with sibling calls that omit it. A permission granted on Resource A must not authorize Resource B merely because both use the same action string.

Use a fresh Codex CLI security-model mapper and semi-triage pass to distinguish a true cross-resource capability gain from global/admin authority, intended inheritance, same-tenant collaboration, or downstream filtering. Explicitly record attacker condition, server condition, and security impact.

For AI/NL-to-SQL and analytics tools, a dataset-listing or entitlement endpoint
is not proof that execution is authorized. Trace every dataset/space alias to a
canonical resource and require the authenticated subject plus tenant and row
policy at the database-tool, memory, and export consumers. Load
`references/CROSS_BOUNDARY_COMPOSITION_METHOD.md` Lane F when these components
fan out from the same request. Use researcher-owned synthetic data only and
stop on unexpected third-party data.

## Missing-control and fail-open invariant

For every protected operation, identify the component responsible for
authentication/authorization and trace what happens when that component is
configured, absent, nil, empty, explicitly no-op, implicitly defaulted,
successful, unknown, or failing. Distinguish an explicit caller choice to make
an operation public from framework code that silently converts an omitted
control into success.

A protected operation must not become accessible merely because an
authentication callback, provider, policy, middleware, or dependency is
absent. Likewise, the resource consumed by the final query/mutation must be the
same resource that was resolved and authorized. Inventory route, query, body,
context, loaded-object, and worker identifiers separately.

Before KILLing any auth candidate, apply
`references/AUTHORIZATION_INVARIANT_KILL_CHALLENGE.md`. State the invariant,
prove the enforcing component, exercise absence/failure states, trace the
protected operation and consumed resource end to end, and prove both preserved
invariant and no attacker-controlled authority transition. `Looks intentional`
or a named no-op helper is not sufficient. If this evidence is incomplete,
keep `HYPOTHESIS / NEEDS_INVARIANT_PROOF`; do not promote it and do not KILL it.

<!-- AUTHORIZATION_KILL_CHALLENGE:v1 -->

## High-value vulnerability classes

- Authentication bypass, account takeover, session fixation/confusion, token substitution
- Missing issuer/audience/nonce/state/PKCE/signature validation
- Cross-tenant/object/role authorization bypass and confused deputy
- AI query confused deputy or dataset-entitlement bypass where the final
  database, memory, or export consumer omits canonical resource authorization
- Revocation, rotation, logout, recovery, and stale-session failures with persistent impact
- API key scope/restriction bypass and capability leakage
- Exposed or hard-coded credentials whose current validity, principal,
  environment, and effective permissions can be established safely; load
  `credential-exposure-capability-hunter` and never treat possession as
  authorization to replay the credential
- Leaked OAuth/bearer administrative tokens where a successful endpoint must be
  bound to its exact read/write scope, role permission, instance, environment,
  and data class; one admin read route never proves every documented write route
- Impersonation/delegation/support-tool boundary failures
- Canonical identity mismatch across email, username, subject, tenant, domain, or Unicode forms
- Browser-assisted issuance of Application Passwords, API keys, OAuth grants,
  or other durable capabilities where a same-origin primitive may invoke an
  approval flow. Separate victim authentication, explicit interaction,
  authorization state, credential delivery, principal, effective API
  permissions, last use, primary-password/MFA/session lifecycle, and explicit
  revocation. Issuance is not automatically full account takeover.
- Dynamic-object or protocol-injection chains that write authentication/session
  state. Load `references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md` and prove
  the exact protected session consumer separately; an intermediate cache or
  key/value write is not authentication bypass or code execution by itself.

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

- Build a credential lifecycle and principal-binding table.
- For exposed credentials, separate artifact visibility, authenticity, current
  validity, declared roles/scopes, effective permissions, protected capability,
  revocation, and residual copies. Prefer vendor-side confirmation when live
  credential use is not explicitly authorized.
- For staging admin APIs, distinguish production from staging while checking
  whether staging contains real identities/PII or production trust. Stop on
  third-party data, preserve only sanitized structural evidence, and never
  paginate accounts to inflate impact.
- Build a token × instance × endpoint × HTTP action × OAuth scope × role
  permission matrix. A successful `GET` proves that read action only; product
  documentation for create/update/delete is not evidence that the token has the
  corresponding write scope or effective permission.
- For SaaS team/site credentials, record the assigned `role`, role-option
  metadata such as `roles_allowed`, and resource restriction such as
  all-versus-selected sites as separate fields. A Developer on one selected
  site is not an Owner, Billing Admin, or team-wide identity, and a function
  metadata listing does not prove deployment or invocation authority.
- Build a route × subject × action × target resource × tenant × state × policy-argument matrix.
- Trace target IDs/UIDs/slugs/org IDs/project IDs from the request to authorization and the final data mutation/query.
- Test token type, issuer, audience, client, tenant, subject, scope, device, and session binding independently.
- Compare enforcement before and after password reset, role removal, tenant removal, key rotation, and account deletion.
- Inspect caches and introspection behavior against the program’s explicit validity contract.
- Distinguish expected grace periods from authority that persists beyond the credential’s permitted lifetime.
- For WordPress Application Passwords, verify HTTPS/local availability,
  global/per-user filters, plugin policy, intended API-only use, one-time
  display, exact REST principal, and individual revocation. Do not assume a
  primary-password change or MFA action revokes this separate credential; do
  not claim persistence until that lifecycle is verified. Load the
  XSS2Shell seven-boundary reference when the credential is reached through
  `CVE-2026-64638`-shaped JSONP/SOME approval.

## Immediate KILL conditions

- Merely long token lifetime or current-session-only logout when documented/by design
- Requires possession of the victim’s secret without a separate exposure path
- Only reveals account existence or non-sensitive metadata
- No cross-principal/cross-resource/cross-tenant capability, protected action, or persistent authority gain
- Action permission exists but no missing target scope or unauthorized effect is proven
- Identity provider behavior is third-party and out of scope

These conditions do not bypass the mandatory authorization KILL challenge when
the candidate involves an absent/default/error control or competing resource
identities.

They also do not permit KILL when attacker-controlled structured data can alter
protocol framing, persisted import state, or optional-interpreter activation
before an authentication/session consumer. In that case complete the execution-
consumer challenge and retain `NEEDS_INVARIANT_PROOF` until the terminal edge is
either proven or falsified.

## Required technical handoff

- Verdict and candidate ID
- Scope and production/mainnet/release proof
- Attacker condition, server condition, and security impact
- Authorization subject/action/resource/tenant/state propagation
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
