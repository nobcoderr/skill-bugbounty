---
name: autonomous-research-cascade-engine
description: "Run authorized, target-native security research cascades from a concrete objective through bounded micro-inspiration, falsifiable hypotheses, clean probes, generic anomaly evaluation, harness falsification, shared-semantic reuse, second-order discovery, deterministic verdict gates, and human review. Use for NOVEL_DISCOVERY_MODE source audits or owned-fixture research where unknown behavior must be detected without known attack names, payload replay, or pre-proof vulnerability prior art. Automatically bootstrap the mandatory auto-router and authorized security autopilot. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Autonomous Research Cascade Engine

Build a bounded research loop that can discover unexpected target behavior
without importing the expected vulnerability answer. Treat every generated idea
as a hypothesis and every anomaly as evidence requiring falsification.

Always activate `mandatory-auto-router`, `authorized-security-autopilot`, and
`novel-vulnerability-hypothesis-engine`. Keep the work single-agent unless the
user explicitly requests delegation.

## Load the cascade methods

Read these package references before running their stage:

- `references/MICRO_INSPIRATION_RESEARCH_METHOD.md` for objective compilation,
  fragment provenance, hypothesis generation, and anchoring controls;
- `references/GENERIC_ANOMALY_EVALUATION_METHOD.md` for invariant-centered
  baselines, authoritative observables, and anomaly ledgers;
- `references/CLEAN_PROBE_REASONING_METHOD.md` for semantic cleanliness,
  permutation constraints, and research-priority rules;
- `references/SHARED_SEMANTIC_REUSE_METHOD.md` for shared-component domain
  asymmetries;
- `references/HARNESS_FALSIFICATION_METHOD.md` for independent runners,
  anomaly-origin attribution, evaluator anti-gaming, and deterministic gates;
- `references/DISCOVERY_CASCADE_METHOD.md` for genealogy, second-order
  questions, conceptual jumps, bounded depth, and `CASCADE_LEAD` handling.

Validate ledgers with
`automation/validate-autonomous-research-cascade.py`. Its companion regression
is a rule test only and never proves blind discovery.

## Enforce the absolute scope boundary

Before ideation, record the official program or owned environment, exact asset,
authorized testing mode, allowlist, rate and concurrency ceiling, abort
conditions, impact ceiling, cleanup plan, and current release.

Enforce these constants:

- `TARGET_SWITCHING=FORBIDDEN`
- `SCOPE_MUST_BE_EXPLICIT=true`
- `SAFETY_SIGNAL_MASKING=FORBIDDEN`
- `AGENT_REALITY_DECEPTION=FORBIDDEN`
- `CREDENTIAL_COLLECTION=FORBIDDEN`
- `DESTRUCTIVE_PROOF=FORBIDDEN`
- `HIGH_VOLUME_DOS=FORBIDDEN`
- `EARLY_EXIT_ON_MINIMUM_PROOF=true`

Never relabel a live target as a simulator or hide an authorization-relevant
signal. Do not run scanners, fuzzers, exploit harnesses, or state-changing
tests without task-specific authorization and limits.

## Execute the modules in order

1. **OBJECTIVE_COMPILER** — express one protected property or unexplored
   behavior as a concrete, falsifiable research question. Do not ask for a
   vulnerability class.
2. **MICRO_INSPIRATION_ENGINE** — select one small target-native or
   non-vulnerability semantic fragment. Record its ID and scope; withhold known
   attack terms and ground truth.
3. **HYPOTHESIS_FACTORY** — derive one to five testable hypotheses. Each must
   name the expected invariant, attacker-controlled variable, authoritative
   observable, and falsifier.
4. **CLEAN_PROBE_CLASSIFIER** — classify each proposed probe as `CLEAN`,
   `DIRTY`, or `UNKNOWN` before execution and record the governing grammar.
5. **PERMUTATION_SYNTHESIZER** — create bounded, one-variable transformations
   from the target grammar or semantics. Never replay a historical payload
   list.
6. **GENERIC_EVALUATOR** — compare a stable baseline with the probe using a
   deterministic invariant predicate. Detect any relevant violation without
   requiring a known output fingerprint.
7. **ANOMALY_LEDGER** — freeze inputs, outputs, measurements, state, scope,
   cleanliness, and evaluator version. An anomaly is not yet a finding.
8. **HARNESS_SELF_AUDITOR** — reproduce with an independent runner or
   implementation and classify origin as `TARGET_CONFIRMED`,
   `HARNESS_CONFIRMED`, `MIXED`, or `UNKNOWN`.
9. **EXPLANATION_ENGINE** — produce multiple plausible root-cause hypotheses
   from frozen evidence; include a discriminator and falsifier for each.
10. **SHARED_SEMANTIC_REUSE** — find components used across domains and ask
    whether a rule valid in one domain is invalid in another.
11. **DISCOVERY_CASCADE** — derive second-order detection and security-effect
    questions while preserving complete parent/child genealogy.
12. **DETERMINISTIC_VERDICT_GATE** — let versioned code decide whether the
    primitive proof passed. Model prose cannot assign success.
13. **HUMAN_AMPLIFIER_GATE** — reserve human review for scope, conceptual
    leaps, high-value anomalies, novelty, and final judgment.

## Advance state monotonically

Use this research state machine:

`MICRO_INSPIRATION -> CODE_DERIVED_HYPOTHESIS -> TESTABILITY_GATE -> SAFE_PROBE -> GENERIC_EVALUATION -> ANOMALY -> HARNESS_FALSIFICATION -> ROOT_CAUSE_HYPOTHESES -> INVARIANT_PROOF -> NEEDS_CONSUMER_PROOF -> NEEDS_STATE_PROOF -> DISCOVERY_CASCADE -> AUTHORITATIVE_READBACK -> NEEDS_PRIOR_ART_CHECK -> STRONG_CANDIDATE`

`CASCADE_LEAD`, `KILLED`, and `BLOCKED` are also allowed. Use `CASCADE_LEAD`
for an independently reproducible, conceptually useful observation that has no
proven protected impact yet. Do not KILL it solely for being non-exploitable;
bound its follow-up budget and keep it below finding status.

## Keep novelty and proof separate

When `NOVEL_DISCOVERY_MODE=true`, preserve the existing prior-art embargo until
the independently derived source-to-sink, harmless runtime effect, and negative
control gates pass. Keep `novelty_status=UNVERIFIED` until post-proof scope,
release, duplicate, and prior-art checks finish.

Reject `PATTERN_REPLAY`, known payload structures, hidden target answers,
model-selected success criteria, or a child that inherits its parent's runtime
or impact proof. A candidate becomes report-ready only at
`STRONG + MANUALLY_CONFIRMED` under the package-wide evidence gate.

For large source trees, keep each cascade child inside one threat-model slice.
Route to `expert-source-code-bug-hunter` and its thin-slice context method when
the stable scaffold begins to compete with target evidence. Evaluate the full
skill pack for routing, but load detailed conditional bodies just in time. A
slice handoff carries verified facts and evidence pointers rather than the full
conversation or persuasive candidate narrative.

If the complete cascade terminates in `NO VALID FINDING`, emit its exhausted
paths, KILL reasons, fact anchors, and falsifiers as a
`prior_method_exclusion_digest`. When scope and budget still permit,
`counterfactual-methodology-synthesizer` may use that digest to construct a
materially different, bounded what-if methodology. Do not relabel an existing
cascade child as a new method, and never inherit proof from the exhausted run.

## Preserve benchmark integrity

Keep V9-A through V9-E seeds, expected classes, affected files, patches,
target counts, and historical ground truth outside the auditor package. Exclude
all development lineages from v1-v9, including the complete technical lineage
of any source used to design this method. Rule regressions do not demonstrate
generalization.


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

1. Ensure the existing router and security-autopilot session is active.
2. Evaluate all installed skills through `config/AUTO_ROUTING_MAP.json`.
3. Load this skill and its companions only for authorized research-cascade
   work or when the novelty engine requires the cascade layer.
4. Reroute after a new runtime, boundary, consumer, anomaly, or cascade edge.
5. Never auto-execute operational automation.

If the router is already active, reuse it and do not bootstrap recursively.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
