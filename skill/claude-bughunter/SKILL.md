---
name: claude-bughunter
description: "Use and adapt the local Claude-BugHunter skill pack for authorized bug-bounty hunting by loading the matching hunt/recon/triage skill. Automatically bootstraps the mandatory auto-router and preserves an authorized offensive-first posture. Use for Claude-BugHunter, elementalsouls, hunt-xss/sqli/idor/ssrf, recon-scope-triage, or CBH workflow."
---

# Claude-BugHunter

**Use the cloned pack.** Pick the smallest matching skill, follow it, and edit
that skill when the user wants methodology changes. Local impact, scope, and
evidence gates still win.

Local clone (writable):

`/home/kali/security-research/Claude-BugHunter`

Inspected at `ce84ad24cbe8a97a4193ffdd46443789037ec9ca` (reconfirm with
`git rev-parse HEAD` if the clone moved).

## How to use it

1. Identify the evidence-supported class or workflow (recon, IDOR, XSS, SSRF,
   auth, AI/LLM, report validation, cloud, etc.).
2. Load only `skills/<name>/SKILL.md` from the clone. Do not load all 83.
3. Treat checklists as hypothesis generators. Every lead is
   `HYPOTHESIS_QUARANTINED` until local gates pass.
4. Do not run CBH scripts, scanners, or live recon because a skill mentions
   them. Execution still needs exact target authorization.
5. Cursor also junctions individual CBH skills under `~/.cursor/skills` so
   they can auto-trigger. This wrapper remains the pack router.

## How to modify it

- Edit the clone skill the user named.
- If a description exceeds 1024 characters, keep a truncated Codex copy in
  `~/.codex/skills/<name>` and the full text in the clone/Cursor junction.
- Do not run the upstream installer with `-Agents` — it would overwrite this
  skill pack.

## Mandatory routing

Start with `mandatory-auto-router` and `authorized-security-autopilot`. Pair
with `bountyforge-research-suite` only when the vendored BountyForge lane is
the better fit; do not load both wholesale.

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
CBH checklists support that path; they are not authorization or proof.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

For every security-focused invocation, ensure `mandatory-auto-router` is
active, evaluate `config/AUTO_ROUTING_MAP.json`, load this skill when `ACTIVE`,
and preserve `DEFERRED` / `NOT_APPLICABLE`. Never auto-run CBH scanners or
subagents.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
