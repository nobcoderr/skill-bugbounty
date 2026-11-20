---
name: zephrfish-harness-kit
description: "Use, customize, and run Andy Gill / ZephrFish Harness Kit staging (recon, hunt, validate, trace, report) plus harnessing-harnesses context budgets. Automatically bootstraps the mandatory auto-router and preserves an authorized offensive-first posture. Use for harness-kit, climbing the LLM hills, Jenny MCP pipeline, hallucination bin, or staged LLM vulnerability research."
---

# ZephrFish Harness Kit

The kit is a **template you operate and edit**, not a finished product. Apply
the stage machine in this agent. Customize the clone's `CUSTOMISE` blocks for
the current target. Do not copy Andy Gill article bodies.

Local clone (writable, no license file):

`/home/kali/security-research/harness-kit`

Pin: `ZephrFish/harness-kit@db3a53411fe3eff966d0f9061540bd4ee4342887`

Companion article patterns (facts only): harness owns tools/prompts/state/gates;
stage-specific prompts; structured handoffs; adversarial validate before trace;
context budgets; RAG memory with provenance. MCP tools are not the harness.

## How to use it

Work one stage at a time in the current agent. Default: **no subagents**.

1. Read and fill `skills/01-recon/SKILL.md` + `prompts/01-recon.md`.
   Output a structured briefing: subsystems, entry points, trust boundaries,
   git security history, `hunt_tasks`.
2. For each hunt task, read `skills/02-hunt/SKILL.md`. One hypothesis, one
   evidence record or an explicit null result. Findings start quarantined.
3. Adversarial validate with `skills/03-validate/SKILL.md`. Default verdict
   `UNCERTAIN`. Only `TRUE_POSITIVE` continues.
4. Trace with `skills/04-trace/SKILL.md` until attacker-controlled input
   reaches the sink with code citations, or mark `TRACE_BLOCKED`.
5. Report only `TRACE_CONFIRMED` items via `skills/05-report/SKILL.md`.

Apply `config/context-budgets.yaml` (recon ~32k, hunt ~8k, validate ~16k,
trace ~24k, report ~32k). Summarise tool output; do not dump raw logs.
Cheap models may classify; keep validate/trace on the stronger model.

Also apply Andy Gill campaign gates when hunting with tools: PoC exists,
clean-snapshot reproduce, exploitable not null-deref, standard-user reachable,
first-class demotion.

## How to modify it

When the user asks to change the harness:

- Edit the clone: stage `SKILL.md`, `prompts/*.md`,
  `config/model-routing.yaml`, `config/context-budgets.yaml`, and
  `skills/_templates/`.
- Keep this wrapper as the pack contract and evidence gates.
- New stages belong in the clone, then get a sentence here.

## Mandatory routing

Start with `mandatory-auto-router`, `authorized-security-autopilot`,
`agentic-security-research-harness`, and
`external-ai-security-tool-governor`. Do not start RAPTOR, Baby Naptime,
Audit, VVAH, or MCP servers because this kit mentions them.

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

For explicitly authorized security work, prioritize:
`attacker objective -> reachable entrypoint -> exploit chain -> privilege or authority transition -> protected sink -> concrete impact`.
The harness exists to prove or falsify that path with staged evidence, not to
maximize scanner volume. This posture grants no MCP, fuzzer, or scanner
execution by itself.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

For every security-focused invocation, ensure `mandatory-auto-router` is
active, evaluate `config/AUTO_ROUTING_MAP.json`, load this skill when `ACTIVE`,
and preserve `DEFERRED` / `NOT_APPLICABLE`. Never auto-run RAPTOR, MCPs, or
subagents.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
