---
name: dynamic-filter-evaluator-rce-hunter
description: "Expert authorized source/API workflow for finding and validating control-data confusion where a free-form filter or query object reaches an executable evaluator. Use for GraphQL JSON scalars, REST filters, Mongo-like operators, sift or similar predicate libraries, $where/$function-style operators, new Function/eval/VM compilation, anonymous resolver reachability, error-channel proofs, and process-authority impact. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Dynamic Filter Evaluator RCE Hunter

Audit authorized API and source paths where a value presented as filtering or
search data can select executable query-language semantics inside a trusted
runtime. Treat the Taskcluster `sift` incident as public, fixed prior art and as
a reusable invariant—not as a payload template or a novel finding.

## Mandatory routing

1. Activate `mandatory-auto-router` and `authorized-security-autopilot`.
2. Load `references/dynamic-filter-evaluator-rce-method.md` completely.
3. Route GraphQL/API surfaces to `api-security-reviewer`.
4. Route parser/operator disagreement to
   `expert-cache-proxy-parser-differential-hunter`.
5. Route JavaScript/Node.js implementation to
   `expert-javascript-typescript-engineer` and
   `expert-source-code-bug-hunter`.
6. Route a proven dynamic-code sink to `modern-rce-chain-hunter`.
7. Route anonymous/role/scope questions to
   `expert-authentication-authorization-hunter` only when that boundary is
   evidenced.
8. Route secret, credential, IAM, or lateral-impact stages to
   `compositional-exploit-chain-hunter` only when a real capability bridge is
   evidenced.
9. Route an advisory, CVE, or public patch lineage to
   `patch-diff-root-cause-analyzer`.

Keep all stages in the current agent unless the user explicitly requests
subagents. Do not run live payloads, command execution, secret extraction, or
credential replay automatically.

## Core invariant

Enforce:

`untrusted filter data must remain data and may select only an explicit, typed, data-only operator set`

The candidate chain is:

`public/API input -> open filter representation -> query/operator interpreter -> code-bearing operator -> dynamic compilation/evaluation -> live data trigger -> process authority -> protected impact`

Do not collapse the chain into “GraphQL is vulnerable” or “a dependency uses
`new Function`.” Prove every edge on the same current release and deployment.

## Required analysis

Build these maps before assigning a verdict:

- **Schema map:** exact scalar/input type, nesting, arrays, aliases, defaults,
  coercion, and unknown-key behavior.
- **Call-path map:** resolver/controller -> loader/service -> filter wrapper ->
  dependency -> operator implementation -> callback invocation.
- **Operator map:** default and custom operations, recursively accepted keys,
  code-bearing operators, and runtime/configuration gates.
- **Principal map:** authentication middleware outcome, anonymous principal,
  resolver authorization, upstream service scope, and process identity.
- **Liveness map:** whether a deterministic non-empty owned result reaches the
  evaluator; empty arrays can hide a reachable sink.
- **Output map:** returned value, error formatter, logs, timing, callback, or
  harmless state marker used to distinguish evaluation from parsing.
- **Impact map:** process privilege, filesystem/network reach, deployment
  tokens, databases, queues, encryption keys, OAuth clients, and internal
  services—without collecting or replaying real secrets.

Trace both forward from the filter and backward from every dynamic-code sink.

## Evidence gate

Treat these as separate claims:

1. free-form input reaches the filter wrapper;
2. the installed dependency/version enables a code-bearing operator;
3. runtime configuration leaves that operator enabled;
4. an eligible caller reaches an affected resolver;
5. a deterministic non-empty data set invokes the predicate;
6. a harmless marker proves server-side evaluation;
7. the evaluation context crosses a protected boundary;
8. the root cause is current and not already public/fixed/duplicate.

A schema, package version, dangerous operator, anonymous middleware branch,
HTTP success, reflected error, or environment-variable name alone is not a
complete finding.

## Safe proof ladder

- **C0:** open scalar or generic filter resemblance only.
- **C1:** controlled input reaches the shipped wrapper.
- **C2:** exact installed evaluator exposes the code-bearing operator.
- **C3:** eligible caller plus deterministic owned data invokes the predicate.
- **C4:** a harmless computed canary proves execution in the server runtime.
- **C5:** process identity or another protected capability is proven using a
  non-sensitive, reversible test and negative control.
- **C6:** current release/deployment, concrete impact, prior art, cleanup, and
  manual reproduction are complete.

Do not call the candidate RCE below C4. Normally require C5-C6 and
`MANUALLY_CONFIRMED` for `STRONG`.

## Immediate KILL conditions

- The path is the same Taskcluster `sift`/`$where` root cause fixed in 100.3.0.
- The filter is converted to a typed, server-owned search operation before use.
- The operator set is an allowlist that cannot compile or invoke code.
- The dependency/runtime gate disables code-bearing operators on the deployed
  path and the application rejects them before evaluation.
- Authentication or authorization blocks the affected resolver for the stated
  attacker, or the upstream call cannot return a trigger element.
- The code is dead, test-only, archived, unshipped, or absent from the current
  package lock/release artifact.
- Only error reflection, malformed input, package presence, or a suspicious
  sink is proven.
- Impact requires secret theft, third-party pivoting, persistence, or unsafe
  production exploitation to demonstrate.

## Required output

Provide:

- verdict: `STRONG / MEDIUM / WEAK / KILL`;
- exact target, scope, version, package, and deployment evidence;
- attacker and server conditions;
- schema, call-path, operator, principal, liveness, and output maps;
- forward and backward traces;
- exact broken invariant and execution context;
- safe proof, baseline, negative controls, abort condition, and cleanup;
- prior-art/advisory/patch lineage and sibling-path review;
- minimal fix and regression tests;
- manual status: `NOT_TESTED / BLOCKED / MANUALLY_CONFIRMED`.

If no distinct current path survives, return **NO VALID FINDING**.


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
