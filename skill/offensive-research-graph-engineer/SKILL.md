---
name: offensive-research-graph-engineer
description: "Design and, only when explicitly requested, execute dependency-aware multi-agent graphs for authorized red-team, offensive-security, and bug-hunting research. Bootstraps the mandatory auto-router, uses an offensive-first posture, isolates workers and verifier context, anchors decisions to executed evidence, and keeps severity provisional until bounded escalation is proven or exhausted."
---

# Offensive Research Graph Engineer

Use this skill when the user explicitly requests an agent graph, parallel
security agents, a multi-agent offensive audit, or graph-engineering for an
authorized bug-hunting campaign. It supplements rather than replaces
`codex-cli-multi-agent-audit-orchestrator` and
`exploit-chain-research-orchestrator`.

The source article is a user-supplied methodology seed. Its product limits,
costs, and scale claims are not treated as verified platform guarantees. The
portable insight is dependency-aware scheduling with independent verification.

## Activation boundary

- Planning the graph is read-only.
- Spawning workers requires an explicit request for subagents, delegation,
  parallel agents, or multi-agent execution.
- Live recon, fuzzing, PoCs, and state-changing tests still require exact
  target authorization, rate/concurrency limits, abort conditions, and cleanup.
- Never infer permission from the requested graph width. A configured queue can
  be larger than runtime concurrency, but both remain bounded by user, product,
  cost, and safety limits.

Read [the graph method](../../references/OFFENSIVE_RESEARCH_GRAPH_ENGINEERING_METHOD.md)
when decomposing work. When a candidate exists, also read
[the severity method](../../references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md).
Use [the root prompt](../../prompts/MASTER_PROMPT_OFFENSIVE_RESEARCH_GRAPH_ENGINEERING.md)
and the two schemas in `../../config/` as handoff contracts.

## Security graph contract

1. Define one node as one bounded job with immutable inputs, allowed tools,
   workspace, expected output schema, evidence anchors, and stop conditions.
2. Add an edge only when the downstream node actually consumes a named output
   from the upstream node. The phrase “and then” is not an edge.
3. Schedule only dependency-ready nodes in parallel. Keep genuinely sequential
   exploit-chain transitions sequential.
4. Prefer independent attack-surface slices or trust boundaries over blind
   one-file-per-agent fan-out when cross-file state matters.
5. Give every writing worker an isolated worktree or workspace. Read-only
   workers may share source only when their outputs are separate and immutable.
6. Deduplicate candidates by root cause before verification. Agent agreement is
   neither coverage nor proof.
7. A fresh verifier receives raw evidence, the exact claim, and the frozen
   acceptance oracle—never the discovery narrative or proposed severity.
8. The root alone merges results, updates attacker state, and decides which
   graph nodes become ready.

Use [the worker contract](agents/graph-worker-node.md),
[the verifier contract](agents/fresh-evidence-verifier-node.md), and
[the escalation contract](agents/severity-escalation-node.md) as logical roles.
They do not authorize child-agent creation.

## Severity escalation rule

Every technically validated Low, Medium, or High assessment is provisional.
Do not stop at the first impact. Recompute attacker state, enumerate newly
reachable protected surfaces, and test only evidence-supported escalation edges
toward the next severity tier. A severity is locked only after higher impact is
proved, every realistic capability-expanding edge is falsified, or scope,
safety, environment, or the program ceiling prevents further proof.

Never inflate severity. The final value is the maximum demonstrated impact,
not the most severe hypothetical chain. Preserve direct primitive severity,
chain severity, CVSS, and program-specific severity as separate fields.

## Evidence anchors

Freeze before execution:

- exact scope, revision/deployment, attacker and victim principals;
- DAG, node budgets, maximum concurrency, cost/time caps, and abort rules;
- baseline, negative controls, deterministic acceptance oracle, and artifact
  hashes or immutable operation IDs;
- workspace ownership, merge authority, conflict policy, and cleanup;
- zero-new-evidence and runaway termination rules.

Return `GRAPH_VALIDATED`, `GRAPH_PARTIAL`, `GRAPH_NOT_NEEDED`, or
`GRAPH_ABORTED`. `STRONG + MANUALLY_CONFIRMED` with `SEVERITY_LOCKED=YES`
establishes vulnerability validity; report readiness additionally requires an
independent `TRIAGER_PROOF=PASS`.

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

For authorized work, follow `attacker objective -> reachable entrypoint -> exploit chain -> privilege or authority transition -> protected sink -> concrete impact`. Defensive guidance follows proof or falsification unless explicitly requested first. This ordering never broadens authorization.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

Activate this skill only after the mandatory auto-router marks it `ACTIVE` from
explicit multi-agent intent and compatible target/scope evidence. Load mapped
companions, reroute on material discoveries, and never auto-execute subagents or
operational testing. Reuse an existing router session rather than recursing.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
