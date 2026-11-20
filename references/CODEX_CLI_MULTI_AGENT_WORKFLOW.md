# Multi-Agent Vulnerability Research Workflow

## Design provenance

This workflow incorporates the discovery-versus-false-positive-verification architecture described by Hyunseo Shin in *How I Found Open-Source 0-days with an LLM Multi-Agent Workflow* (February 23, 2026). It adapts the underlying separation-of-duties principles for any agent runtime (Cursor, Codex CLI, Claude Code, Gemini, or other); it does not copy the article's vendor/model stack or treat model output as proof.

## Purpose

This workflow adapts role-separated vulnerability discovery and false-positive verification to a researcher who uses **any local agent runtime**. It is designed for one model running multiple independent sessions or subagents. The security benefit comes from separation of duties and evidence handoffs—not from model branding or agent count. File names such as `CODEX_CLI_*` are stable schema ids, not a Codex-only requirement.

## Core principle

Use broad, inexpensive context during discovery and progressively deeper context during verification:

`scope/reality map -> security model -> independent discovery -> semi-triage KILL pass -> specialist verification -> blind final judge -> human reproduction`

Discovery optimizes recall. Verification optimizes precision. Human reproduction remains the source of truth.

The discovery control plane is adaptive rather than open-ended:

`three core scouts -> convergence check -> coverage-gap analysis -> zero to three adaptive specialists -> termination`

Read `ADAPTIVE_RESEARCH_PATH_ORCHESTRATION_METHOD.md` for the normative path
statuses, wave launch gates, primitive chaining, exact implementation
escalation, and stop conditions.

## Workspace and provenance

Recommended local state:

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
  evidence/
    INDEX.md
  commands/
    README.md
  final/
```

Rules:

- Do not overwrite prior evidence silently.
- Record repository commit, tag, branch, dirty state, build/artifact version, platform, and time zone.
- Record every command actually executed and its exit status.
- Do not claim line numbers until the exact file revision was read.
- Do not use chat consensus as evidence.
- Keep the target repository read-only unless the user explicitly asks for a regression test or fix.

The optional `automation/init-codex-cli-audit-workspace.py` creates this scaffold only. It does not invoke Codex, access the network, or run testing.

## Research-path registry

The root orchestrator maintains one entry per material attack surface and
hypothesis family. Use:

- `ACTIVE` while assigned;
- `PROMISING` when a falsifiable next proof exists;
- `BLOCKED` when named external/runtime/authorization evidence is missing;
- `EXHAUSTED` after reasonable target-native variants are covered without a
  survivor;
- `KILLED` when contradicted, unreachable, by design, duplicate/fixed, out of
  scope, or non-impactful;
- `VALIDATED` only after applicable proof gates pass.

For `BLOCKED`, `EXHAUSTED`, and `KILLED`, record why and what materially new
evidence could change the result. Do not repeatedly assign agents to terminal
paths. Another model opinion or repeated reading is not new evidence.

## Role handoffs

### Handoff A — Scope and reality

Required fields:

- program and rules source;
- in-scope asset/repository/component;
- exclusions and eligible classes;
- allowed testing/automation;
- exact release/deployment mapping hypothesis;
- attacker model;
- stop conditions;
- unresolved scope facts.

A missing essential fact results in `BLOCKED`, not optimistic inference.

### Handoff B — Security model

Extract:

- principals, roles, tenants/orgs, objects, ownership, and states;
- permission actions and resource scopes;
- credential/session/capability lifecycle;
- expected state transitions and invariants;
- default configuration and feature flags;
- trusted roles and by-design authority;
- sensitive sinks and protected assets.

For every authorization-sensitive route, use:

| Route/call | Subject | Action | Target identifier | Tenant/org | State | Policy helper | Parameters passed | Downstream filter |
|---|---|---|---|---|---|---|---|---|

A common high-value inconsistency is an action check that omits the target resource scope. The finding survives only when the missing parameter permits a concrete unauthorized operation against another resource, tenant, or principal.

### Handoff C — Discovery candidate

A discovery candidate must include direct evidence and start at
`CODE_DERIVED_HYPOTHESIS`. It cannot use persuasive severity language. Required
minimum:

- candidate ID and class;
- observed entrypoint and controlled field;
- observed policy/validation/sink path;
- suspected missing invariant;
- exact files/functions/lines actually read;
- candidate-specific falsification questions;
- no impact claim beyond what evidence currently supports.

### Handoff C1 — First wave and convergence

When multi-agent work is explicitly authorized, the first wave uses three
independent lenses:

| Lane | Primary question |
|---|---|
| Authority/capability | Can a lower-authority principal acquire or exercise authority outside its intended scope or lifecycle? |
| Representation/consumer | Does the checked representation or identity differ from what a downstream consumer interprets or uses? |
| State/composition | Can an invalid state, timing window, retry/cache behavior, or composition of weak primitives cross a boundary? |

After their handoff, group candidates by root cause. Retain one best-evidenced
candidate per converged family for verification. Redirect duplicate capacity
to uncovered surfaces; agreement itself contributes no evidence.

### Handoff C2 — Adaptive second wave

Coverage analysis may launch zero to three target-selected specialists. Each
launch requires a named uncovered surface/new trust boundary, new exact
implementation evidence, or an untested downstream transition. Record the
specialist, bounded question, path ID, falsifier, expected evidence, and stop
condition. Do not use an adaptive wave to reconfirm a candidate already in
verification.

### Handoff D — Semi-triage dossier

Explicitly answer all three sections.

#### Attacker condition

- external/internal/local/network position;
- unauthenticated/user/member/admin/local-low-privilege starting point;
- account, tenant, object, and role prerequisites;
- attacker-controlled representation/state;
- victim interaction;
- prior compromise assumptions.

#### Server condition

- vulnerable version/tag/commit/build/artifact;
- production/mainnet/stable-release path;
- default or realistic configuration;
- plugin, feature flag, platform, OS, and deployment prerequisites;
- real caller/consumer;
- upstream/downstream controls;
- reproducibility environment.

#### Security impact

- exact primitive obtained;
- affected principal/tenant/object/secret/asset/release/privilege;
- confidentiality, integrity, availability, authorization, signing, or trust property broken;
- durable consequence;
- boundary crossed;
- why the result exceeds the attacker's starting authority.

If any section is unsupported, downgrade or KILL.

## Independent verification passes

### Reachability verifier

Prove:

`repo path -> build/package -> shipped artifact/deployed service -> default/realistic configuration -> user workflow -> vulnerable entrypoint`

Reject test-only, dead, sample, default-off, unconsumed, or unsupported paths.

### Security-model verifier

Check official docs/policies, roles, tests, comments, schemas, and intended threat model. Distinguish:

- bug versus vulnerability;
- role authority versus cross-boundary authority;
- expected collaboration versus tenant/object isolation break;
- grace period versus credential authority beyond the contract;
- local/plugin trust decision versus silent privileged execution.

### End-to-end trace verifier

Require both directions to meet:

`attacker input -> decode/parse -> canonicalize -> validate -> state/cache/serialize -> auth/signature/policy -> trust transition -> sink -> impact`

`sink <- helper <- caller <- policy/state assumption <- attacker-controlled source`

Record every unsupported edge as missing proof.

### Primitive-to-impact verifier

Treat the initial primitive separately from bounty impact. Require:

`attacker input -> primitive -> capability gain -> next protected boundary -> protected resource/action -> concrete consequence`

Each transition is `PROVEN`, `FAILED`, or `UNTESTED` with evidence. Stop the
chain when a required transition fails. If the primitive directly crosses the
protected boundary, record that no further bridge is required and prove the
impact directly. Never assume credentials, connectivity, victim behavior, or
deployment features to complete a chain.

### Exact implementation verifier

When correctness depends on runtime, parser, framework, database, cryptographic
library, serializer, package manager, dependency, or protocol behavior, inspect
the exact shipped/version-matched implementation source when available. Bind
the conclusion to component name, immutable version/revision, target build
selection, source symbols/branches, and platform/configuration conditions.
Documentation-only or different-version reasoning remains `BLOCKED`.

### Prior-art verifier

Search and record issues, PRs, advisories, CVEs, changelog, commits, release notes, tests, docs, known limitations, public research, sibling products, and duplicate root-cause families. Do not equate a different endpoint title with a different root cause.

### Test-design verifier

Specify:

- baseline expected success/failure;
- candidate case changing one variable;
- negative control;
- harmless canary;
- evidence to capture;
- abort conditions;
- cleanup;
- nondeterminism/repetition requirements.

Do not run the test without explicit authorization.

## Final judge protocol

The final judge receives only structured evidence. It should not receive discovery excitement, bounty estimates, or unverified severity. It applies:

- **STRONG:** scope, release reachability, attacker control, missing check, protected boundary, concrete impact, reproduction/controls, and prior-art status are substantially proven.
- **MEDIUM:** credible candidate with one material proof gap.
- **WEAK:** major assumptions remain.
- **KILL:** invalid, unreachable, by design, equal privilege, duplicate/known/fixed, prohibited to test, or no concrete impact.

The final judge records `manual_status` separately:

- `NOT_TESTED`
- `BLOCKED`
- `MANUALLY_CONFIRMED`

A STRONG source candidate may still be `NOT_TESTED`; it is not report-ready until manual confirmation.

## Correlated-error controls

Using the same model repeatedly can amplify the same mistake. Reduce this risk by:

1. fresh sessions for discovery, triage, reachability, prior art, and final judgment;
2. blind review without discovery severity labels;
3. single-candidate dossiers rather than large candidate batches;
4. explicit instructions to disprove the candidate;
5. independent source re-reading rather than trusting quoted snippets;
6. machine-readable required fields;
7. raw command/source/runtime evidence indexes;
8. human reproduction and negative control.

## Cost and context routing

When all roles use the same model on any runtime:

- parallelize only independent read-only discovery when allowed by the local environment;
- keep discovery context narrow and role-specific;
- reject schema-incomplete candidates before deep review;
- reserve full repository/call-graph analysis for survivors;
- cap candidates per lane;
- re-open a killed candidate only when new evidence changes a hard gate;
- never trade away final verification depth for more hypotheses.
- do not assign `EXHAUSTED` or `KILLED` paths without materially new evidence;
- do not launch more than three adaptive specialists in one coverage wave;
- do not launch another wave without a registry-backed material condition.

## Termination

Continue discovery only while a material surface remains uncovered, a new
trust boundary or exact implementation behavior appears, or a surviving
primitive has an untested downstream transition. Stop when all material
surfaces have coverage, remaining paths are terminal, further rounds repeat
existing root causes, progress needs unavailable runtime/environment evidence,
or all survivors moved to verification. Preserve the unblock evidence so a
future audit can resume without repeating exhausted work.

## Candidate state machine

```text
CODE_DERIVED_HYPOTHESIS
  -> NEEDS_INVARIANT_PROOF
  -> NEEDS_CONSUMER_PROOF
  -> NEEDS_STATE_PROOF
  -> NEEDS_RUNTIME_PROOF
  -> NEEDS_REACHABILITY_PROOF
  -> NEEDS_PRIOR_ART_CHECK
  -> STRONG_CANDIDATE | KILLED | BLOCKED
```

No stage may be skipped. Discovery cannot jump directly to `STRONG_CANDIDATE`
or `MANUALLY_CONFIRMED`.

## Required conclusion

If no candidate survives all gates, return **NO VALID FINDING**. This is a correct and successful audit result.
