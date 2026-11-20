---
name: modern-web-guidance
description: "Use the pinned GoogleChrome/modern-web-guidance-src clone for Chrome web-platform guidance and the chrome-extensions skill. Automatically bootstraps the mandatory auto-router. Defaults to an authorized offensive-first posture while treating the upstream repo as reference-only, model-agnostic knowledge, not a scanner or install authority."
---

# Modern Web Guidance

Use this skill when the user names `GoogleChrome/modern-web-guidance-src`,
Modern Web Guidance, Chrome web-platform guidance, or the upstream
`skills-src/chrome-extensions` skill.

The clone is **reference knowledge**. It does not authorize live testing,
`pnpm` install, eval harness execution, or publishing guides.

## Frozen source

Local clone: `/home/kali/security-research/modern-web-guidance-src`

Pinned commit: `326dd82628535889f16b3115d54c6ccf12a989eb` (2026-11-13).
Re-read `LICENSE`, `AGENTS.md`,
`skills-src/README.md`, and `skills-src/chrome-extensions/SKILL.md` before
depending on an upstream claim.

## Mandatory routing

Start with `mandatory-auto-router` and `authorized-security-autopilot`. Then:

1. Read `skills-src/chrome-extensions/SKILL.md` in the clone for Chrome
   extension work.
2. Read clone `guides/` only when the task is web-platform guidance, not as
   exploit steps.
3. Do not run clone `bin/`, eval graders, or npm/pnpm scripts unless the user
   names that exact command for this clone.
4. Do not treat guide examples as authorization against a target.

Keep RAPTOR, Strix, ARTEX, HackerAI, and HexStrike `REFERENCE_ONLY`.

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

For every explicitly authorized security task, prioritize:
`attacker objective -> reachable entrypoint -> exploit chain -> privilege or authority transition -> protected sink -> concrete impact`.
Use this guidance clone to name platform constraints that would falsify or
shape that path. Detection and hardening are secondary unless the user asks
for blue-team work. This posture never expands authorization.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

This skill never operates as a silent standalone module. For every
security-focused invocation:

1. ensure `mandatory-auto-router` is active;
2. evaluate all installed skills through `config/AUTO_ROUTING_MAP.json`;
3. apply this skill only when marked **ACTIVE**, while recording **DEFERRED**
   and **NOT_APPLICABLE** routes;
4. load mapped companions from this skill folder;
5. rerun routing after material discoveries;
6. never auto-execute operational automation without explicit authorization.

If the router is already active, acknowledge the existing routing session and
do not recursively bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
