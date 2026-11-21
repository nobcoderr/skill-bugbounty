---
name: counterfactual-methodology-synthesizer
description: "Synthesize and evaluate genuinely new target-native security-audit methodologies after a bounded campaign ends in NO VALID FINDING, using counterfactual changes to actors, representations, state order, lifetimes, consumers, topology, cardinality, ownership, and failure semantics. Automatically bootstraps the mandatory auto-router and uses an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Counterfactual Methodology Synthesizer

Use this skill when an authorized, evidence-complete audit pass ends in
`NO VALID FINDING` but the current eligible target still has materially
unexplored architecture. Do not recycle dead candidates or merely rename a
payload. Generate a new way to interrogate the target, then test whether that
method can produce a real vulnerability candidate.

Always reuse the active `mandatory-auto-router`,
`authorized-security-autopilot`, `novel-vulnerability-hypothesis-engine`,
`autonomous-research-cascade-engine`, and `program-impact-boundary-gate`
session. Keep work single-agent unless the user explicitly requests delegation.

Load:

- `references/COUNTERFACTUAL_METHODOLOGY_SYNTHESIS_METHOD.md`;
- `prompts/MASTER_PROMPT_COUNTERFACTUAL_METHODOLOGY_SYNTHESIS.md`;
- `config/COUNTERFACTUAL_METHODOLOGY_REGRESSION_CASES.json`;
- `automation/validate-counterfactual-methodology.py`; and
- `automation/test-counterfactual-methodology.py`.

## Activation gate

Remain `DEFERRED` while the current methodology still has live candidates.
Activate only when:

1. the prior pass records `NO_VALID_FINDING` and `hunt-terminal-verdict`
   has `HUNT_CLOSED=YES` (todos and assets are actually finished, not a
   mid-Cursor premature summary);
2. its killed, blocked, and exhausted paths are frozen as an exclusion digest;
3. the target remains explicitly authorized, in scope, current, and eligible;
4. at least one architecture or semantics axis remains unexplored; and
5. another bounded cycle is permitted by the task's time and safety limits.

A target that is prohibited, archived without an eligible consumer, outside
scope, or blocked by missing authorization cannot be rescued by a new method.

## What-if synthesis loop

Ask target-specific counterfactuals:

`What if A becomes B while protected invariant P should remain true?`

Mutate one or two meaningful axes at a time:

- actor or authority;
- object ownership or alias identity;
- representation before and after normalization;
- operation order or state phase;
- lifetime, retry, revocation, or cache epoch;
- direct, queued, worker, proxy, or compatibility topology;
- single, batch, aggregate, or partial cardinality;
- primary versus delayed consumer;
- error, nil, default, rollback, or recovery semantics; or
- composition between independently reachable features.

Build every method from at least two current target-native fact anchors. Define
its invariant, authoritative oracle, stable baseline, closest safe sibling,
negative control, falsifier, release check, impact plan, safety boundary, and
stop condition before testing.

## Independence requirement

A method is `MUTATION_ONLY` unless it changes an architecture-level relation or
at least two material semantic axes and also introduces a new oracle, consumer,
or falsifier. Changing only payload spelling, filename, endpoint alias, numeric
constant, encoding decoration, or vulnerability label is not a new method.

Feed the previous campaign only as an exclusion digest. Do not use its expected
bug class, known payloads, or desired answer as inspiration.

## Bounded evaluation

Default limits:

- maximum two post-`NO VALID FINDING` cycles;
- maximum three method cards per cycle;
- maximum one primary invariant per method card; and
- immediate stop when scope, safety, or a decisive KILL condition appears.

Operational tests remain subject to the existing explicit authorization gate.
This skill may design safe tests automatically but never runs live recon,
scanners, fuzzers, exploit harnesses, state-changing requests, or destructive
proof merely because a new method was generated.

## Success semantics

A methodology is only shown to have produced a valid vulnerability when its
candidate independently proves:

- attacker control and complete source-to-sink flow;
- invariant violation and harmless runtime effect;
- baseline, closest safe sibling, and negative controls;
- harness-independent reproduction and authoritative read-back;
- current production or shipped-release reachability;
- nonzero program-recognized capability delta;
- post-proof prior-art and duplicate clearance; and
- `STRONG + MANUALLY_CONFIRMED` status.

Otherwise use one of:

- `METHOD_READY_FOR_SAFE_EVALUATION`;
- `METHOD_GENERATED_NO_VALID_FINDING`;
- `MUTATION_ONLY`;
- `NO_MATERIAL_NEW_METHODOLOGY`;
- `STOP_BUDGET_EXHAUSTED`; or
- `BLOCKED_BY_SCOPE`.

Never claim that a regression test proves general vulnerability-discovery
ability. It proves only that the synthesis rules reject obvious false novelty
and preserve valid evaluation requirements.

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

1. Reuse the existing `mandatory-auto-router` and security-autopilot session.
2. Activate this skill only after `NO VALID FINDING` or an explicit request for
   counterfactual methodology synthesis.
3. Load its mapped prompt, method, regression cases, and validators.
4. Reroute after each material new actor, representation, state, consumer,
   topology, reachability, or impact fact.
5. Never auto-execute operational automation.

If the router is already active, do not bootstrap it recursively.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
