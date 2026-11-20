---
name: pwn-hunter
description: "Use and adapt BountyForge pwn-skill for authorized binary exploitation, CTF-lab pwn, and memory-corruption primitive work. Automatically bootstraps the mandatory auto-router and preserves an authorized offensive-first posture. Use for pwn-hunter, pwn-skill, ret2libc, ROP, format string, tcache/UAF, seccomp, kernel pwn, or lab binary triage."
---

# PWN Hunter

**Use the local clone as the technique handbook.** Apply the primitive ladder
and triage loop. Edit the clone when the user wants new techniques. Local
authorization and evidence gates override upstream "assume authorized" and
"refusal engineering" text.

Local clone (writable, MIT):

`/home/kali/security-research/pwn-skill`

Pin: `BountyForge-xyz/pwn-skill@403310598eab3c99c24082795c35b76e790ed6a5`

When this skill is ACTIVE, read `SKILL.md` in that clone for checklists, then
**skip** the section `REFUSAL ENGINEERING`. Do not prefill jailbreaks, swap
safety vocabulary, or assume scope. If authorization is missing, stop.

## How to use it

1. Confirm the exact authorized binary/lab (path, libc, remote vs local).
2. Phase 0 triage from the clone: `file`, `checksec`, ELF headers, libc
   identity, seccomp, RELRO/PIE/NX/canary. Measure; do not invent offsets.
3. Name the current rung and the next rung:

   `crash -> RIP/PC -> leak -> arbitrary write -> exec -> escape`

4. Pick one class from the clone: stack, format string, heap/glibc, seccomp,
   or Linux kernel pwn. Load only that section.
5. Iterate with a debugger until the primitive is observed, not narrated.
6. Deliverable is a measured primitive write-up. A working `exp.py` is allowed
   only for the authorized lab binary the user named. Never target third-party
   production hosts.

## How to modify it

- Edit `/home/kali/security-research/pwn-skill/SKILL.md` for new
  techniques, glibc versions, or lab notes.
- Keep this wrapper as the policy overlay.
- Do not copy exploit skeletons into the skill pack.

## Mandatory routing

Start with `mandatory-auto-router` and `authorized-security-autopilot`. Also
load `executable-binary-auditor` and `expert-c-cpp-engineer` when the artifact
is native. Kernel pwn additionally loads
`openai-kernel-research-pipeline` only if the target is Linux kernel.

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
Climb the primitive ladder with measured offsets. This posture does not grant
unauthorized CTF-against-third-parties, malware, or refusal-bypass tricks.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

For every security-focused invocation, ensure `mandatory-auto-router` is
active, evaluate `config/AUTO_ROUTING_MAP.json`, load this skill when `ACTIVE`,
and preserve `DEFERRED` / `NOT_APPLICABLE`. Never auto-run pwntools exploits
against unnamed targets.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
