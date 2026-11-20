---
name: github-actions-fork-trust-hunter
description: "Expert authorized workflow for finding and validating GitHub Actions trust-boundary failures involving fork pull requests, pull_request, pull_request_target, workflow_run, issue_comment, reusable workflows, untrusted artifacts, actions/checkout credential persistence, npm lifecycle scripts, GITHUB_TOKEN permissions, step-scoped secrets, runner files, and downstream release or supply-chain consumers. Use when untrusted PR code or data may execute in a credentialed job. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# GitHub Actions Fork Trust Hunter

Audit whether untrusted fork-controlled code or data crosses into a runner
authority that it should not receive. The core invariant is:

> Untrusted PR code and artifacts execute only in an unprivileged compartment;
> privileged workflows consume only validated data and never expose usable
> credentials, writable repositories, release channels, or protected services.

Read `references/github-actions-fork-trust-method.md` whenever this skill is
active. Treat the historical DuckDuckGo privacy-configuration and
content-scope-scripts reports as nuanced prior art: checkout-persisted job
credentials and same-job workspace tampering are distinct channels, while a
later-step secret is never assumed ambient to an earlier install step.

## Evidence-driven routing

Start with `mandatory-auto-router` and `authorized-security-autopilot`. Activate
this skill only when evidence shows both:

1. a fork author controls code, lifecycle scripts, an action, artifact, cache,
   event field, ref, path, or configuration processed by a workflow; and
2. that input reaches an execution or interpretation point in a job with a
   credential, writable token, protected runner, release consumer, or trusted
   downstream workflow.

Route alongside:

- `expert-cloud-ci-cd-supply-chain-hunter` for workflow, runner, OIDC, release,
  signing, artifact, package, and deployment authority;
- `credential-exposure-capability-hunter` only after identifying an actual
  credential channel, then prove current validity and effective permissions;
- `expert-javascript-typescript-engineer` for npm lifecycle scripts, JavaScript
  actions, local actions, expression handling, and package execution;
- `expert-source-code-bug-hunter` and `secure-code-reviewer` for exact event-to-
  runner-to-consumer traces;
- `patch-diff-root-cause-analyzer` for workflow/action-version changes,
  backports, hardening versus root-cause fixes, and duplicate screening;
- `compositional-exploit-chain-hunter` when a runner credential bridges into a
  second repository, release workflow, CDN, registry, signing service, cloud
  role, or client update channel.

A lone `pull_request_target`, `permissions: write`, secret reference,
`actions/checkout`, `npm ci`, fork guard, or hardening PR is a hypothesis only.

## Required chain

Build this ledger:

`fork actor -> event and workflow provenance -> untrusted ref/artifact -> checkout/download -> execution consumer -> credential channel -> effective token authority -> protected mutation/read -> downstream consumer -> concrete impact`

For every edge record the repository, workflow commit, event/action, fork state,
approval state, workflow-definition provenance, checked-out SHA/repository,
action version, step order, job permissions requested and effective, credential
location, token principal/scope/expiry, runner type, branch/environment gates,
baseline, negative control, cleanup, and prior art.

## Mandatory distinctions

- `pull_request` and `pull_request_target` have different workflow provenance,
  token, and secret models. Do not transfer conclusions between them.
- Runner code execution is not secret theft. Secret theft is not repository
  write. Repository write is not release or downstream client compromise.
- Repository and organization secrets are not process-wide ambient variables.
  A secret referenced in a later trusted step is not automatically available to
  an earlier `npm ci` process.
- Step-scoped secrets do not make the job safe when earlier untrusted code can
  modify a script, dependency, executable, command file, path, or workspace
  object that the later secret-bearing step executes or interprets. A trusted
  base checkout loses its integrity if fork code can rewrite it before use.
- A job-scoped `GITHUB_TOKEN` is special. It may be reachable through an action
  context or checkout-persisted Git credentials even when not visible in the
  current shell environment.
- `actions/checkout` credential behavior is version-specific. For v4/v5 the
  token was persisted in local Git configuration by default; later versions
  changed storage and fork protections. Pin the version and commit.
- Requested YAML permissions are not proof of effective fork-run permissions.
  Capture the actual event/repository visibility/settings and runtime permission
  result.
- A trusted base-branch action receiving secrets is not exploitable merely
  because a fork can trigger it. Prove attacker-controlled code, executable
  input, action substitution, injection, or credential residue reaches it.
- A PR that adds a fork check may be defense in depth. It is not by itself proof
  that the reported exploit worked.
- Redacted `***` in a log proves masking, not that attacker code received the
  secret or that its value was exfiltrated.

## Workflow

1. **Scope and snapshot:** verify official authorization, exact repositories,
   workflow commit, action versions, event settings, runner type, and allowed
   testing before execution.
2. **Provenance map:** identify which branch supplies the workflow definition,
   which repository/SHA is checked out, and which artifacts/actions/config files
   are attacker-controlled.
3. **Gate ordering:** trace permission/association/fork/approval checks and
   failure behavior before every checkout, download, install, build, or action.
4. **Execution proof:** identify a real consumer such as lifecycle script, local
   action, build/test hook, shell expression, container entrypoint, or artifact
   parser. Validate only in disposable researcher-owned repositories.
5. **Credential inventory:** inspect explicit `env`/`with`, `github.token`, Git
   credential config/helpers, CLI config files, cloud login files, OIDC request
   capability, caches, artifacts, and cross-step residue separately.
6. **Cross-step integrity:** before every secret-bearing or privileged step,
   identify all executable files, dependencies, tools, command files, PATH
   entries, and inputs that earlier untrusted code could modify. Treat a shared
   workspace or runner as a capability bridge, not a clean boundary.
7. **Capability proof:** fingerprint synthetic credentials and use the smallest
   owned canary action to prove the token's actual principal and permissions.
   Never print or replay a vendor credential.
8. **Chain proof:** if supply-chain impact is claimed, prove branch protections,
   merge/push authority, workflow triggering semantics, environment approvals,
   artifact publication, and real consumer reachability one edge at a time.
9. **Controls:** compare external fork, same-repository PR, trusted branch,
   `persist-credentials: false`, scripts disabled, patched action/workflow, and a
   metadata-only trusted action.
10. **Prior art and verdict:** screen issues, PRs, commits, action advisories,
   docs, workflow history, release notes, and vendor comments. Retain only the
   exact current non-duplicate boundary that was manually demonstrated.

## Safe proof ladder

- **G0 — Static signature:** suspicious event, checkout, execution, or credential
  reference exists.
- **G1 — Untrusted execution:** a deterministic synthetic marker proves fork code
  executed in the expected job; no credential claim yet.
- **G2 — Credential channel:** a redacted/fingerprinted owned fixture proves the
  execution context can reach the exact credential location or helper.
- **G3 — Effective authority:** the credential authenticates as the expected
  principal with exact runtime permissions; requested YAML permissions alone do
  not qualify.
- **G4 — Protected capability:** a harmless controlled read or mutation affects
  a researcher-owned protected resource and survives authoritative read-back.
- **G5 — Downstream chain:** the controlled mutation reaches an owned release,
  registry, CDN, deploy, signer, or update consumer with every gate proven.
- **G6 — Reality:** current scope, repository/workflow/action version, novelty,
  repeated manual proof, controls, cleanup, and production/release mapping pass.

Only G6 can be `STRONG / MANUALLY_CONFIRMED`. Severity is capped at the highest
proven boundary; do not borrow supply-chain impact from architecture diagrams.

## Remediation invariant

- Use `pull_request` for untrusted code with least-privilege read-only tokens and
  no secrets.
- Split privileged follow-up into a base-branch workflow that consumes a strict,
  validated data artifact rather than executable PR content.
- Never place untrusted execution and a later secret-bearing execution consumer
  in the same job or reusable runner workspace. Use separate ephemeral jobs and
  transfer only schema-validated, non-executable data.
- Set explicit least-privilege `permissions`, `persist-credentials: false`, and
  disable install scripts unless they are required and reviewed.
- Pin actions by immutable commit and keep privileged actions/configuration under
  trusted base-repository control.
- Never check out fork code in a privileged event and then install, build, test,
  source, import, evaluate, or run a local action from it.
- Use environments, approvals, branch protections, short-lived scoped tokens,
  OIDC subject conditions, ephemeral isolated runners, and post-job cleanup as
  independent defense layers.

## Hard KILL rules

KILL when the workflow never runs for external forks, a pre-execution gate fails
closed, only trusted base code executes, artifacts are data-only and validated,
the claimed secret is not in the step/action/file/memory channel, the effective
token is read-only and adds no protected capability, postinstall is disabled,
the path is fixed/duplicate, or downstream write/deploy/consumer edges are only
assumed.

The user-supplied 2026 DuckDuckGo privacy-configuration report and HackerOne
#3619287 for content-scope-scripts are public prior art. Do not duplicate their
fork-to-runner credential/workspace classes or preserve disproven ambient-secret
and unproven all-browser supply-chain claims as methodology conclusions.

Never auto-run live fork PRs, OAST callbacks, secret enumeration, token
extraction, credential replay, repository mutation, release publication, cache
poisoning, or deployment against a vendor. Use disposable owned repositories,
synthetic canaries, rate limits, abort conditions, and cleanup.

## Required output

| Candidate | Verdict | Event/workflow provenance | Fork-controlled input | Execution consumer | Credential channel | Effective authority | Protected effect | Downstream reach | Prior art | Manual status |
|---|---|---|---|---|---|---|---|---|---|---|

If no candidate reaches a protected boundary with current manual evidence,
return **NO VALID FINDING**.


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
