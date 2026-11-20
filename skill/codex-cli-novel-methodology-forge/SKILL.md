---
name: codex-cli-novel-methodology-forge
description: "Run the explicit V13-METHODOLOGY-LAB after a frozen V12-style authorized audit ends with no surviving candidate. Measures factual coverage gaps, forges materially distinct reasoning procedures, critics them, executes approved methods in isolated agents when delegation is authorized, and retains only new material evidence. Experimental only; never modifies or replaces frozen V12."
---

# Codex CLI Novel Methodology Forge

This is an experimental successor branch, not part of frozen V12 and not a
default audit stack. Use it only when the user explicitly enables
`V13-METHODOLOGY-LAB` for an authorized audit.

## Immutable baseline

Read `../../BASELINE_LOCK.json` and
`../../prompts/V13_ROOT_OVERLAY.md` first. Validate V12 hashes before and after
the lab run. Never write, link, chmod, or extract into the frozen baseline.

## Activation gate

Enter `NOVEL_METHODOLOGY_EXPANSION_MODE` only when all are true:

- the normal audit is schema-valid and frozen with an input digest;
- `SURVIVING_COUNT == 0` and `VALID_FINDING_COUNT == 0`;
- no candidate is awaiting verification;
- no research path is `ACTIVE`, `PROMISING`, or cheaply unblocked;
- the target remains current, explicitly authorized, and program-eligible;
- at least one factual, material, executable coverage gap remains; and
- the audit explicitly permits this experimental multi-agent lab.

An unavailable runtime, missing authorization, prohibited test, or absent
production consumer is a blocker—not a coverage gap the Forge may reinterpret.

## Stage routing

1. **Coverage Gap Analyzer** — read
   `references/COVERAGE_GAP_ANALYSIS.md` and use
   `agents/coverage-gap-analyzer.toml`. It identifies insufficiently investigated
   reasoning dimensions and never proposes a vulnerability.
2. **Methodology Forge** — read `references/METHODOLOGY_FORGE_METHOD.md` and use
   `agents/methodology-forge.toml`. It emits no more than four repeatable
   procedure graphs per wave.
3. **Novelty Critic** — read `references/METHODOLOGY_NOVELTY_CRITIC.md` and use
   `agents/methodology-critic.toml`. Only novelty/executability PASS with at
   least MEDIUM expected coverage delta may execute.
4. **Isolated Executor** — use `agents/methodology-executor.toml`. Spawn a fresh
   child for exactly one approved method only when delegation is explicitly
   authorized. Give it a content-addressed factual brief, architecture, source
   snapshot, and one procedure; withhold candidate conclusions, other generated
   methods, patches, ground truth, and sibling outputs.
5. **Evidence Pool + Aggressive Falsifier** — deduplicate evidence by semantic
   identity and artifact digest, then use `agents/methodology-falsifier.toml`.
   Only surviving new facts may open a research path or candidate.
6. **Promotion Gate** — read `references/METHODOLOGY_PROMOTION_RULES.md`.
   Promotion is a separate later decision and never occurs from one run.

## Methodology registry

Keep methodology state separate from the V12 research-path registry:

- `../../registry/v12-methodology-baseline.json` — hashed V12 definitions;
- `../../registry/generated-methodology-definitions.jsonl` — immutable generated definitions;
- `../../registry/methodology-executions.jsonl` — append-only run evidence;
- `../../registry/methodology-promotion-decisions.jsonl` — append-only human decisions; and
- derived statistics from `automation/score-methodology-value.py`.

An executor cannot write registry counters or promotion status. A methodology
is the canonical graph:

`input facts -> reasoning operators -> evidence queries -> oracle -> falsifier -> termination`

It is not a bug class, payload list, file/function accusation, or renamed
prompt. Use the three schemas in `config/` and validate every record.

## Evidence delta

`NEW MATERIAL EVIDENCE` must be factual, security-relevant, absent from frozen
V12 and earlier waves, and contain:

- evidence ID and semantic identity;
- exact artifact pointer and SHA-256;
- source-snapshot digest;
- factual claim and authoritative observation;
- comparison against existing evidence; and
- executor/input/output provenance.

Splitting one fact into several records does not increase marginal value.
Inference, hypothesis, duplicate conclusion, candidate count, and model
agreement are not new evidence.

## Limits and termination

- `MAX_FORGE_WAVES=2`
- `MAX_METHODS_PER_WAVE=4`
- `MAX_EXECUTED_METHODS_TOTAL=6`
- two consecutive zero-gain methods for one gap exhaust that gap
- a second wave requires a new factual gap discovered by wave one

If no material gap exists, stop. If all executions yield zero new facts, stop.
Do not generate another wave merely to avoid `NO VALID FINDING`.

## Candidate and promotion gates

Every issue remains `CODE_DERIVED_HYPOTHESIS` until it passes the normal V12
and program-impact pipeline. A methodology can advance through:

`EXPERIMENTAL -> SOURCE_USEFUL -> REPRODUCIBLE -> BLIND_VALIDATED -> PROMOTED`

`PROMOTED` additionally requires a frozen method definition, independent
multi-target blind trials, paired equal-budget V12 controls, no ground-truth
leakage, at least one non-duplicate valid finding, no exact-root regression, no
increase in report-ready false positives, no runaway, and recorded human
approval. The scoring tool reports eligibility but never mutates or promotes.

## Automation

The validators are network-free and do not execute target probes:

- `automation/validate-methodology-registry.py`
- `automation/validate-methodology-novelty.py`
- `automation/score-methodology-value.py`
- `automation/validate-forge-termination.py`
- `automation/test-v13-methodology-lab.py`

Operational source execution remains subject to exact target authorization,
safe-harbor rules, harmless proof, rate limits, abort conditions, cleanup, and
the parent audit's permissions.

<!-- AUTHORIZED_OFFENSIVE_POSTURE:v1 -->
## Authorized offensive-first posture

Prioritize attacker objectives, boundary crossings, authority changes,
protected consumers, and concrete program-recognized impact. Defensive guidance
is secondary until offensive proof or falsification is complete. This posture
never expands authorization or permits destructive, stealthy,
credential-stealing, persistence, evasion, or third-party activity.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory routing

Reuse `mandatory-auto-router`, `authorized-security-autopilot`, and
`program-impact-boundary-gate`. This experimental skill activates only for an
explicit V13 lab run after the normal workflow freezes at no finding. Do not
bootstrap recursively and do not auto-run operational automation.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
