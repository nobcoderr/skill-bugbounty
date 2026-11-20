---
name: codex-cli-multi-agent-audit-orchestrator
description: "Use proactively for bug bounty, VRP, HackerOne, Bugcrowd, Intigriti, YesWeHack, and authorized vulnerability hunts. Automatically turn on subagents, delegasi, parallel agents, and multi-agent review without the user naming this skill. Spawn role-separated specialists with Cursor Task, Codex spawn_agent, Claude Code Agent, or sequential fresh-context roles. Skip ordinary product implementation, UI/CSS, and non-security coding. The folder name is a routing id, not a Codex-only limit. Model-agnostic. Bootstraps the mandatory auto-router and separates discovery, falsification, security-model verification, reachability/prior-art verification, final evidence judgment, and mandatory manual reproduction. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

## Mandatory package-wide auto-routing

Before any target analysis, activate `mandatory-auto-router`, read `config/AUTO_ROUTING_MAP.json`, evaluate all installed skills and supporting artifacts, load every relevant specialist and companion, and re-route after material discoveries. The routing ledger is mandatory; silent omission is invalid.

# Multi-Agent Security Audit Orchestrator

The folder name `codex-cli-multi-agent-audit-orchestrator` is a stable routing
id. This skill is **not Codex-CLI-only**. Use the current runtime's isolated
subagent tool: Cursor `Task`, Codex `spawn_agent`, Claude Code `Agent`, or
sequential fresh-context roles when no spawn tool exists.

Multi-agent here means independent, role-isolated audit passes: separate
sessions, subagents where supported, or sequential fresh-context runs. It does
not require multiple model vendors. When one model is used for every stage,
independence is preserved by fresh contexts, constrained evidence bundles,
separate output files, and blind re-evaluation.

Activate this skill automatically for bug bounty, VRP, platform hunts, and
authorized vulnerability research. That includes subagents, delegasi, parallel
agents, and multi-agent review. Do not wait for the user to name it. Skip
ordinary product implementation, UI/CSS, and non-security coding. If the task
or scope prohibits subagents, stay in the current agent. Recon, live scanners,
installers, and red-team planning remain separate explicit-intent routes.

When active, also read
`references/ADAPTIVE_RESEARCH_PATH_ORCHESTRATION_METHOD.md` and maintain the
registry defined by
`config/CODEX_CLI_RESEARCH_PATH_REGISTRY_SCHEMA.json`.
Also load `references/OFFENSIVE_RESEARCH_GRAPH_ENGINEERING_METHOD.md` and
`references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md` when compiling the graph or
when a validated candidate has not yet exhausted higher-impact paths.

## Non-negotiable operating contract

1. **Discovery and verification are separate.** Discovery agents generate hypotheses only. They cannot certify a finding, assign STRONG, or write a submission.
2. **Fresh-context falsification is mandatory.** Every retained candidate must be reviewed by at least one independent triage pass that is instructed to KILL it.
3. **Three explicit conditions are mandatory:** attacker condition, server condition, and concrete security impact. A candidate missing any one is incomplete.
4. **Security-model verification is mandatory.** Check official policy, permissions model, intended trust, default configuration, and program scope before calling source-level behavior a vulnerability.
5. **Action permission is not resource authorization.** For authorization paths, trace `subject + action + resource scope + tenant/org + object state` and verify the target identifier reaches the policy engine.
6. **Evidence outranks consensus.** Multiple sessions or models agreeing is not proof. Source/runtime evidence, a real release path, safe reproduction, and negative control are proof.
7. **Manual reproduction remains the final gate.** No candidate is report-ready until the researcher manually reproduces the protected-boundary impact on an allowed target or equivalent official/local environment.
8. **No correlated narrative inheritance.** Final triage receives the candidate dossier and raw evidence, not the discovery agent's persuasive prose or severity claim.
9. **Read-only by default.** Do not modify target code, run network requests, scanners, fuzzers, installers, or PoCs unless the user explicitly authorizes that action and safety controls are defined.
10. **No hallucination or silent execution.** Never claim a file, line, command result, deployment, test, or reproduction that is not present in the evidence index.
11. **Research paths are stateful.** Register every material surface as `ACTIVE`, `PROMISING`, `BLOCKED`, `EXHAUSTED`, `KILLED`, or `VALIDATED`; never silently recycle an exhausted lane.
12. **Agreement is not coverage.** When agents converge on one root cause, preserve one candidate for verification and redirect remaining discovery capacity to neglected surfaces.
13. **Second waves are adaptive.** Launch zero to three additional specialists only for a recorded coverage gap, new trust boundary or implementation evidence, or an untested downstream transition.
14. **Primitives require impact chains.** A parser discrepancy, SSRF, path primitive, race, or authorization primitive is not bounty-grade until it directly crosses a protected boundary or follows evidence-backed transitions to concrete impact.
15. **Version-match implementations.** If correctness depends on runtime, parser, framework, database, crypto, serializer, package, dependency, or protocol semantics, inspect the exact shipped/version-matched source when available.
16. **Stop on evidence exhaustion.** Another wave requires materially new work; stop when all material paths are covered or terminal, when only repetition remains, or when unavailable runtime/authorization evidence is required.
17. **A specialist is an execution fact, not prose.** Count an adaptive
    specialist only after a direct successful spawn via the runtime tool
    (Cursor `Task`, Codex `spawn_agent`, Claude Code `Agent`, or equivalent)
    returns a unique child ID, the child produces separate output, and the
    root consumes it. Failed or absent spawn events count as zero. Sequential
    same-context reasoning is not a spawn.
18. **Provenance is mandatory.** Derive spawn attempts, successes, failures,
    child IDs, input/output hashes, and root consumption from the JSONL
    transcript with automation/validate-adaptive-execution-provenance.py.
    Root narration cannot override the deterministic result.
19. **Edges are real data dependencies.** Add an edge only when the downstream
    node consumes a named upstream output. Fan out only dependency-ready nodes;
    keep shared attacker/runtime state and exploit prerequisites ordered.
20. **Workspace isolation is mandatory for writers.** Each mutable node owns an
    isolated worktree or disposable workspace. The root alone merges results
    and resolves conflicts.
21. **Verification context is clean.** Independent verifiers receive the claim,
    immutable evidence, baseline, negative control, and frozen oracle without
    discovery prose, votes, or proposed severity.
22. **Severity is provisional.** Low, Medium, and High remain unlocked until
    capability-continuous higher-impact edges are proven, falsified, or stopped
    by an explicit program, scope, safety, or environment ceiling.
23. **Report readiness is triager-proof.** `STRONG + MANUALLY_CONFIRMED`
    establishes vulnerability validity only. A separate evidence judge must
    pass scope, release, prerequisites, reproduction, controls, protected
    read-back, cleanup, root cause/fix locus, prior art, severity rationale,
    reproducibility, evidence integrity, and triager-objection coverage before
    setting `REPORT_READY=YES`.

## Role-separated pipeline

### Role 0 — Scope and authorization mapper

Produce:

- program and exact in-scope asset/repository/component;
- eligible vulnerability classes and exclusions;
- allowed automation/testing methods;
- production/mainnet/stable-release mapping requirements;
- researcher-owned accounts/data/environment plan;
- explicit stop conditions.

If scope or authorization cannot be established, stop with **KILL** or **BLOCKED**.

### Role 1 — Target reality and architecture mapper

Independently map:

- repository structure, packages, build targets, deployment/release consumers;
- entrypoints, routes, RPCs, jobs, parsers, importers, hooks, plugins, IPC, CI/release workflows;
- trust boundaries, principals, tenants, roles, objects, states, caches, queues, serializers, policy engines, and sensitive sinks;
- exact version/tag/commit/artifact/config/feature flags relevant to production or stable release.

This role maps facts. It does not generate vulnerability verdicts.

### Role 2 — Security-model mapper

Extract the expected invariants from:

- official security documentation and program policy;
- route and API contracts;
- permission/action/resource-scope definitions;
- tests, comments, schemas, threat model, default configuration, and intended role hierarchy;
- deployment/release assumptions.

For authorization, build a matrix:

| Principal | Action | Target resource | Tenant/org | Object state | Required scope parameters | Actual parameters passed |
|---|---|---|---|---|---|---|

Flag missing target scope only as a hypothesis until a real unauthorized effect is proven.

### Role 3 — First-wave discovery swarm

When the user explicitly authorized parallel agents, start with three
independent target-native lanes:

- **A — Authority/capability:** principals, permission scope, tenant/object
  identity, confused deputy, and capability lifecycle;
- **B — Representation/consumer:** checked-versus-consumed identity, parser,
  canonicalization, serialization, protocol grammar, and shared consumers;
- **C — State/composition:** transitions, queues, retries, caches, races,
  lifecycle changes, and cross-feature composition.

Within those lanes, investigate evidence-supported surfaces such as:

- authorization/tenant/object scope;
- authentication/session/capability lifecycle;
- parser/canonicalization/serialization/cache differentials;
- race/replay/TOCTOU/state-machine invariants;
- command/file/plugin/deserialization/sandbox sinks;
- cloud/CI/CD/release/signing/supply-chain paths;
- Web3 signature/accounting/bridge/governance invariants;
- mobile/desktop/native boundaries.

Each discovery pass must output only structured candidates with direct source
references. It starts them at `CODE_DERIVED_HYPOTHESIS`, never VALID or STRONG.

The root orchestrator—not individual scouts—updates the research-path registry.

### Role 3A — Convergence and coverage-gap control

After the first wave:

1. group candidates by root-cause family;
2. retain one best-evidenced representative of every converged family for
   verification;
3. treat duplicate agent agreement as zero additional proof;
4. redirect remaining capacity to uncovered surfaces;
5. launch zero to three adaptive specialists only when the registry records a
   material gap, new trust boundary/implementation evidence, or an untested
   downstream transition.

For every launched specialist, the root must call the runtime spawn tool
directly (Cursor `Task` with a unique agent id, Codex `spawn_agent`, Claude
Code `Agent`, or equivalent) with a fresh context and bounded task. Record the
returned child ID before waiting. The child must end its separate result with
a fresh SPECIALIST_RESULT_TOKEN=<token> not present in its input. After
receiving and using that result, the root emits
CONSUMED_SPECIALIST_RESULT_TOKEN=<same-token>. Do not wait on an empty or
invented ID.

If spawn fails, record the failure and continue with
ADAPTIVE_EXECUTION_PROVEN=NO; do not perform a local pass and label it an
adaptive specialist. ADAPTIVE_SPECIALIST_COUNT is the count of completed child
contexts with verified root receipts, not planned assignments.

Do not assign a specialist to an `EXHAUSTED` or `KILLED` path unless materially
new evidence is recorded. Do not use discovery capacity to reconfirm a
candidate already assigned to verification.

### Role 3B — Dependency scheduler and workspace controller

Compile nodes and edges before spawning. Every node records immutable inputs,
named required outputs, allowed actions, workspace ownership, output schema,
evidence anchors, acceptance oracle, time/cost budget, and stop conditions.
Schedule only the ready set whose dependencies have passed. Queue excess work
in bounded waves using actual runtime capacity; never assume a published
thousand-node or concurrency ceiling applies locally.

Read-only agents may inspect the same immutable source tree while writing
results to separate locations. Any code-writing, harness-writing, or generated
artifact node uses its own worktree or disposable workspace. No worker may run
shared reset, checkout, clean, force-push, or broad deletion commands. The root
owns merge order, conflict decisions, candidate deduplication, and graph state.

Terminate a lane after two zero-new-evidence waves, repeated failure without a
new technical hypothesis, cost/time breach, workspace collision, scope drift,
or a safety abort.

### Role 4 — Semi-triage killer

Review one candidate at a time in a fresh context. Explicitly answer:

**Attacker condition**

- network position;
- starting privilege/account/role/tenant;
- attacker-controlled input/object/state;
- required victim interaction;
- whether prior equal or higher compromise is required.

**Server condition**

- exact version/tag/commit/build;
- production/stable-release/deployment reachability;
- default or realistic configuration;
- required plugin/feature flag/platform/OS;
- upstream/downstream checks and actual consumers.

**Security impact**

- concrete primitive: unauthorized read/write/action/execute/sign/state/fund capability;
- affected principal, tenant, object, secret, asset, release, or privilege context;
- CIA/security property broken;
- durable consequence and boundary crossed.

KILL obvious false positives, unreachable paths, by-design behavior, equal-privilege cases, and source-only suspicions without a sensitive effect.

### Role 5 — Independent specialist verifiers

Only semi-triage survivors enter these independent checks:

1. **Reachability verifier:** prove source-to-build/package/artifact/deployment/stable-release path.
2. **Security-model verifier:** prove the behavior violates the project's documented or code-enforced security model rather than intended design.
3. **Prior-art verifier:** inspect issues, PRs, advisories, CVEs, changelog, commits, tests, release notes, and duplicate families.
4. **End-to-end trace verifier:** reconstruct attacker input through validation/state/auth/policy to sensitive sink, plus the backward trace.
5. **Test-design verifier:** define baseline, positive case, negative control, evidence capture, abort condition, and cleanup.
6. **Implementation verifier:** when semantics depend on a dependency/runtime,
   bind the conclusion to its exact shipped version and implementation source;
   documentation-only reasoning returns `BLOCKED`.

A verifier must return `PASS`, `FAIL`, or `BLOCKED` with evidence. It must not fill missing facts by inference.

### Role 6 — Final evidence judge

Use a fresh isolated context (new subagent or new session). Provide only:

- scope/reality record;
- security-model record;
- structured candidate dossier;
- raw source/runtime evidence index;
- independent verifier outputs;
- prior-art results;
- test results if already authorized and performed.

Apply **STRONG / MEDIUM / WEAK / KILL**. Agreement among prior agents cannot upgrade the verdict. Missing manual reproduction prevents `MANUALLY_CONFIRMED` status.

Before final severity, run the severity-escalation node. Starting from the
validated post-state, enumerate only protected surfaces newly reachable through
the primitive, test capability-to-prerequisite matches, and preserve identity,
environment, privilege, and state continuity. Lock the maximum demonstrated
program severity only after terminal impact, complete falsification of
realistic expansion edges, or an explicit program/scope/safety/environment
ceiling. Hypothetical impact remains blocked and cannot upgrade the result.

### Role 7 — Human reproduction gate

The researcher manually validates survivors using only permitted, safe methods. Record:

- exact environment/version/hash/config;
- baseline and expected behavior;
- harmless positive reproduction;
- negative control changing one variable;
- authoritative state before/after;
- raw logs/requests/tests;
- reproduction count and nondeterminism;
- cleanup.

Only after this gate may the candidate be marked `MANUALLY_CONFIRMED`. It still
requires `TRIAGER_PROOF=PASS` before `REPORT_READY=YES`. The package stops at
technical evidence handoff and does not submit reports.

## Context-isolation rules (any runtime)

- Start each role in a fresh session or isolated subagent context.
- Give discovery agents only the target map, security model, and relevant code—not previous candidate conclusions.
- Give triage agents a single candidate plus evidence, not a batch of persuasive summaries.
- Remove severity labels from blind final review where practical.
- Store outputs in separate immutable files and preserve hashes when evidence matters.
- Record every command actually executed; do not infer command output.
- Use the smallest relevant code slice first, then expand only when call-path evidence demands it.
- Re-route package skills whenever a new language, runtime, trust boundary, sink, release path, or prior-art family appears.

## Recommended workspace

Use the optional local scaffold from `automation/init-codex-cli-audit-workspace.py` only after explicit user approval. The scaffold creates no network traffic and does not invoke any model. The `.codex-security/` directory name is legacy; it is just an evidence folder.

```text
.codex-security/
  00-authorization-scope.md
  01-target-reality.md
  02-security-model.md
  03-routing-ledger.md
  04-research-path-registry.json
  candidate.schema.json
  research-path-registry.schema.json
  candidates/
  reviews/
  evidence/INDEX.md
  commands/README.md
  final/
```

## Structured candidate requirement

Every candidate must conform to `config/CODEX_CLI_CANDIDATE_SCHEMA.json` and include:

- candidate identity and current stage;
- research-path identity, discovery wave, and root-cause family;
- explicit attacker condition;
- explicit server condition;
- explicit security impact;
- exact source and release-reachability evidence;
- end-to-end trace and missing invariant;
- authorization scope propagation where applicable;
- patch-variant/consumer-boundary challenge where applicable, including checked
  versus consumed identity, operation error domain, downstream protocol
  capability, lifecycle propagation, closest sibling, and patched control;
- dynamic-data/execution-consumer challenge where applicable, including remote
  representation, synthesized method/attribute surface, protocol framing
  identity, persisted or queued state, feature/dependency activation,
  intermediate effect, terminal edge, closest sibling, and patched control;
- prior-art/duplicate status;
- primitive-to-impact chain with evidence for every transition and an explicit
  stop reason when a boundary cannot be crossed;
- exact dependency/runtime implementation binding where correctness materially
  depends on external semantics;
- baseline, positive proof, negative control, cleanup;
- invalidation factors and missing proof;
- verdict and manual-reproduction status.

## Cost and context control for a single model

Do not emulate model tiering by weakening verification. Save cost and context through routing:

- many shallow, independent discovery passes;
- immediate schema rejection for incomplete candidates;
- one-candidate-per-session semi-triage;
- deep call-graph and runtime work only for survivors;
- compact evidence dossiers instead of entire chat histories;
- hard candidate caps and explicit KILL reasons;
- no repeated re-analysis unless new evidence changes the model.
- no additional discovery wave without a material registry-backed launch
  condition;
- no reassignment of `EXHAUSTED` or `KILLED` paths without materially new
  evidence.

## Required technical handoff

- Pipeline stage and candidate ID
- Role outputs and their PASS/FAIL/BLOCKED results
- Scope and production/mainnet/stable-release proof
- Attacker condition
- Server condition
- Security impact
- Exact files/functions/lines actually observed
- End-to-end call/data/state flow
- Missing invariant and security boundary
- Authorization action/resource/tenant/state propagation where applicable
- Safe proof, baseline, negative control, evidence index, and cleanup
- Prior-art/duplicate result
- Invalidation factors and missing proof
- Final verdict: STRONG / MEDIUM / WEAK / KILL
- Manual status: NOT_TESTED / BLOCKED / MANUALLY_CONFIRMED
- Vulnerability validity: VALID / INVALID / BLOCKED
- Triager-proof gate: PASS / FAIL / BLOCKED
- Likely triager objections and evidence-backed answers
- Report ready: YES / NO, with exact blockers
- Research-path registry, convergence decision, adaptive-wave justification,
  adaptive-execution provenance, primitive-chain result, exact implementation
  binding, and termination reason

If no candidate survives: **NO VALID FINDING**.

## Evidence-only output boundary

This skill stops at technical validation and researcher handoff. It does not generate or submit vulnerability reports, execute live testing implicitly, or treat agent consensus as evidence.


<!-- MODEL_AGNOSTIC_RUNTIME:v1 -->
## Model-agnostic runtime

This skill binds to the local pack, not to Codex, OpenAI, Claude, Grok,
Gemini, or any other vendor. The current session's model is the operator.
Do not skip, defer, or weaken this skill because the product is Cursor,
Claude Code, Gemini, Codex CLI, or another runtime.
`agents/openai.yaml` is optional UI metadata only; this skill runs on Cursor, Codex CLI, Claude Code, Gemini, or any other consumer.
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
