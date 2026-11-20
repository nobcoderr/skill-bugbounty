---
name: credential-exposure-capability-hunter
description: "Expert authorized workflow for exposed, leaked, or hard-coded credentials in source code, Git history, public or private CI logs, Docker/OCI images and layers, build artifacts, documentation, tickets, Slack/Teams/chat files, support bundles, notebooks, packages, or screenshots. Use for AWS access-key pairs, database credentials, Jira or Mastodon admin bearer tokens, Netlify personal access tokens, staging credentials, API-token disclosure, service-account credentials, PII-safe evidence handling, CI-log provenance, credential validity, principal identity, resource-scoped effective-permission proof, revocation, artifact cleanup, and residual-copy review. Automatically bootstraps the mandatory auto-router and never treats artifact access, credential replay, account enumeration, cloud enumeration, deployment, or database access as implicitly authorized. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Credential Exposure Capability Hunter

Assess whether an exposed secret is a current, in-scope security boundary break. Prove only the minimum chain needed to establish identity and effective capability, then stop and prioritize containment.

## Mandatory bootstrap

1. Activate `mandatory-auto-router` and `authorized-security-autopilot`.
2. Build the target/scope evidence card before inspecting a collaboration system, artifact, repository, or credential.
3. Load `references/credential-exposure-capability-method.md` for the evidence ladder, safe-validation decision tree, and Mozilla Jira, Mastodon staging, Common Voice container-image, plus public-CI-log-to-Netlify prior-art lessons.
4. Route API-key identity, scope, lifecycle, and revocation to `expert-authentication-authorization-hunter`.
5. Route source, CI, artifact, package, cloud, or service-account exposure to `expert-cloud-ci-cd-supply-chain-hunter` and the relevant source/runtime specialist.
6. Route a credential that bridges into another protected service to `compositional-exploit-chain-hunter`.
7. When the credential is embedded in client-readable signed state or may be
   reused as that state's integrity key, load
   `evidence-to-terminal-oracle-bug-bounty` and
   `references/EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY_METHOD.md`. Prove the
   relationship offline with exact framework derivation; do not replay the
   credential or forged state without separate written authorization.
8. For GitHub Actions fork or pull-request workflows, load
   `github-actions-fork-trust-hunter` and inventory explicit step `env`/action
   inputs, `github.token`, checkout-persisted Git configuration or helpers,
   CLI/cloud login files, OIDC request capability, artifacts/caches, and runner
   residue as separate channels.

Keep all stages in the current agent unless the user explicitly requests subagents.

## Non-negotiable boundary

- Confirm written authorization for the exact artifact source, registry/repository, tag or immutable digest, platform manifest, collaboration workspace/channel, account, API, database, and validation method.
- Treat pulling an image, retrieving historical manifests/layers, inspecting a registry mirror, authenticating to AWS, or connecting to a database as separate actions that require explicit authorization. Public visibility is not authorization for every follow-on action.
- Treat internal access, NDA status, or channel membership as an attacker precondition, not permission to search unrelated content.
- Treat an out-of-scope report that received a discretionary bounty as a scope exception, never as future authorization or precedent.
- Never store the raw credential in a prompt, skill, report draft, terminal history, screenshot, log, fixture, or evidence bundle.
- Do not authenticate with a disclosed credential unless the current written policy or vendor explicitly authorizes that exact validation.
- Do not enumerate users, groups, projects, tickets, repositories, registry objects, buckets, IAM resources, databases, tables, secrets, or data merely to demonstrate blast radius.
- Stop on third-party data, unexpected privilege, scope drift, uncertainty about ownership, or evidence that the credential has already been revoked.
- If an administrative response exposes email addresses, IP addresses, or other third-party personal data, set `PII_EXPOSED_STOP`, stop pagination and further calls, retain only sanitized structural metadata, and request secure vendor-side handling/redaction.

## Evidence chain

Build and falsify this chain:

`authorized artifact access -> immutable artifact identity -> secret-bearing layer/path -> credential-like value -> issuer/type and pair binding -> current validity -> principal -> effective permissions -> protected control plane/resource -> minimum safe impact -> credential rotation plus artifact purge -> residual-copy handling`

Do not collapse distinct claims:

- a secret-looking string is not a valid credential;
- a valid credential is not necessarily privileged;
- one successful administrative endpoint proves that endpoint and its effective read/write scope, not every capability advertised elsewhere in the API documentation;
- staging is not production, but staging is not automatically harmless when it contains real identities, personal data, trusted integrations, or a path into production;
- a role or group label is not proof of every possible action;
- a response field such as `roles_allowed` is not the principal's assigned role; bind authority to the effective `role`, resource-access fields, and an authorized action result;
- a Netlify `Developer` restricted to selected sites is not an Owner, Billing Admin, or team-wide principal;
- listing an existing function or deploy proves read access to its metadata, not create, upload, publish, execute, environment-read, delete, or rollback authority;
- documented serverless-function deployment is not proof that the exposed token can deploy; if it can, execution occurs in the provider-managed function runtime and is not automatically RCE on the CI service, source organization, or application server;
- visibility to an internal channel is not anonymous public exposure;
- source presence is not current production validity;
- a repository or organization secret referenced by a later workflow step is
  not automatically ambient to an earlier fork-controlled install/build step;
- nevertheless, the later secret may become reachable when that step executes a
  script, dependency, executable, command file, or workspace object that the
  earlier untrusted step could rewrite. Prove that write-then-execute edge rather
  than claiming environment inheritance;
- a job `GITHUB_TOKEN` may still be reachable through an action context or
  checkout-persisted Git credentials even when absent from shell environment
  output; pin the action version and prove the exact channel without retaining
  the raw token;
- a mutable tag such as `latest` is not an immutable artifact identity;
- deleting a file in a later image layer is not proof that its bytes are absent from a lower layer;
- deleting a tag or image is not credential revocation, and credential rotation is not artifact deletion;
- two AWS access-key IDs and two secret access keys are not evidence until each correct pair is bound without exposing the values;
- database credentials do not prove database reachability, environment, role, or data access;
- a payout is not proof that a surface remains in scope;
- deletion of one message is not proof that history, exports, caches, forks, or local copies are gone.

## Workflow

### 0. Scope and prior art

Capture the exact asset, artifact location, registry/repository, tag, platform, manifest and image digest, layer/path, CI provider, task/run/job/step, log URL or artifact ID, publication timestamp, authorized audience, retention/cache/mirror behavior, discovery method, secret-validation rules, privacy limits, and stop conditions. Search exact fingerprints only in authorized local material; search public history by root cause and artifact path without publishing the secret. Never mass-pull registries, mirrors, CI logs, historical tags, or deleted objects.

Check issues, PRs, advisories, commits, secret-removal history, changelog, incident notes, official docs, program known issues, and maintainer statements. A public, fixed, revoked, duplicate, fake/example, or out-of-scope lineage is `KILL` unless a distinct current exposure and boundary are proven.

### 1. Preserve without propagating

Record artifact identity, location, timestamp, audience, file/message metadata, and a one-way fingerprint. For CI logs, bind the observation to the exact provider, task/run/job/step, raw versus rendered log form, public-access control, publication time, and cache/download artifact. For containers, prefer the immutable manifest/image digest, platform, layer index/digest, and in-layer path over a mutable tag. Redact all but the minimum prefix/suffix required by the vendor. Do not copy the complete value into new systems, image history, exported archives, or build logs.

### 2. Classify the credential

Identify the likely issuer, token family, environment, principal class, expiry model, revocation mechanism, and expected scope from surrounding evidence. Bind every multi-part credential correctly: AWS long-term keys require the matching access-key ID and secret access key, temporary AWS credentials additionally require the session token, and database credentials require their own username/password pair plus separately proven endpoint, environment, and role. For OAuth/bearer admin APIs, bind the token to the exact instance, principal, declared scopes, role permission, and endpoint action. Distinguish production credentials from staging, examples, test fixtures, placeholders, expired values, public client identifiers, and non-secret metadata without treating `staging` as a sufficient KILL by itself.

### 3. Select the least-invasive validity proof

Prefer, in order:

1. vendor confirmation or an authorized incident-response check;
2. offline metadata, signature, format, or deployment evidence that does not use the secret;
3. an issuer-provided self/introspection endpoint that returns only the credential's own identity and scopes, but only when explicitly authorized;
4. one read-only, non-enumerating capability check against a researcher-owned or vendor-provided canary, but only when explicitly authorized.

If no validation method is authorized, report the exposure with fingerprinted evidence and request revocation/verification. Never improvise a replay path.

### 4. Prove effective capability, not imagined impact

Bind the credential to its principal, tenant/site, environment, scopes, groups/roles, resource-access restrictions, policy conditions, exact endpoint/action, and one concrete protected capability. Prefer authorization metadata, audit logs, vendor confirmation, or a harmless owned-object check. A successful read endpoint does not prove write/delete/password-reset/deploy authority unless the same token's write scope and effective role permission are independently established. For SaaS deploy platforms, record site/team binding and execution locus separately: site-content integrity, provider-hosted function execution, CI-service compromise, and source-organization server compromise are four different claims. Stop once material privilege is established, and stop immediately on third-party PII.

### 5. Containment and residual exposure

Recommend immediate revocation or rotation, invalidation of derived sessions/tokens, cloud and database audit-log review, removal from the original artifact, and review of message history, exports, caches, commit history, forks, build logs, packages, support bundles, registries, manifests, tags, lower layers, mirrors, build caches, pulled copies, and backups. Track cloud-key rotation, database-password rotation, IAM-principal removal, tag/image deletion, blob garbage collection, and clean rebuild as separate controls. Do not claim remediation complete from message or image deletion alone.

### 6. Final judgment

Use the reference's E0-E6 proof ladder. Only E6 with scope fit, current validity or vendor confirmation, principal/effective-permission evidence, concrete boundary, prior-art clearance, containment status, and manual confirmation can be `STRONG + MANUALLY_CONFIRMED`.

## KILL rules

KILL when any applies:

- artifact access or credential validation is not explicitly authorized;
- the value is fake, placeholder, public-by-design, expired, revoked, or otherwise unusable;
- only format/pattern matching or scanner output exists;
- only a mutable image tag, access-key ID, username, or secret-looking layer string exists;
- privilege is inferred only from naming, a UI label, or documentation;
- the starting user already has equal or higher authority;
- impact requires data enumeration, mutation, persistence, third-party access, or an unsafe live replay;
- the exact leak or root-cause family is public, fixed, known, or duplicate, including the resolved public Mozilla CI-log-to-Netlify lineage without a distinct current log, token, selected resource, and root cause;
- the program excludes the surface or method and no written exception exists;
- no protected resource or control-plane capability is proven;
- the historical image/tag is deleted and its credentials are revoked, with no distinct current digest, credential, or residual exposure in scope;
- the candidate is HackerOne #2137154 or the same Mozilla Mastodon staging token/artifact lineage, already rotated and resolved, with no distinct current credential or boundary;

## Required output

- Verdict: STRONG / MEDIUM / WEAK / KILL
- Manual status: NOT_TESTED / BLOCKED / MANUALLY_CONFIRMED
- Scope and validation authority:
- Artifact source and authorized audience:
- CI-log identity when applicable: provider, task/run/job/step, raw/rendered form, public-access proof, timestamp, retention/cache/mirror:
- Container identity when applicable: registry/repository, platform, tag-at-observation, manifest/image digest, layer digest/index, and path:
- Credential type and issuer confidence:
- Credential components and pair binding: COMPLETE / INCOMPLETE / TEMPORARY_SESSION_TOKEN_REQUIRED:
- Raw-secret handling: NOT_RETAINED / REDACTED / FINGERPRINT_ONLY
- Current validity evidence:
- Principal, tenant, environment, and effective permissions:
- Resource-access restriction and effective role: ALL / SELECTED / UNKNOWN:
- Endpoint/action evidence and declared-versus-effective scope:
- Execution locus when applicable: CI_RUNNER / APPLICATION_SERVER / PROVIDER_MANAGED_RUNTIME / UNKNOWN:
- Environment and data classification: PRODUCTION / STAGING_REAL_DATA / STAGING_SYNTHETIC / TEST / UNKNOWN:
- Privacy status: NO_PII_SEEN / PII_EXPOSED_STOP / VENDOR_REDACTED:
- Protected boundary and minimum demonstrated impact:
- Evidence level: E0-E6
- Baseline and negative control:
- Prior-art and duplicate result:
- Revocation/rotation status:
- Artifact-removal status: TAG / MANIFEST / BLOB / CACHE / MIRROR / REBUILD:
- Residual-copy review:
- Evidence missing and single safest next step:
- Invalidation factors:

If no candidate survives, output **NO VALID FINDING**.

## Evidence-only output boundary

Stop at technical validation, containment guidance, and evidence handoff. Do not output raw credentials, live replay commands, resource-enumeration procedures, secret harvesting, persistence, destructive actions, or unauthorized access guidance.


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
