---
name: apple-macos-research
description: "Use and adapt the pinned dawgyg/AppleResearch dump plus agent_guidance for authorized macOS/Apple vulnerability research. Automatically bootstraps the mandatory auto-router and preserves an authorized offensive-first posture. Use for AppleResearch, XNU, IOKit, XPC helpers, SIP/TCC, smbd/nfs, UDF/exFAT, installd, remoted, WebGPU on Apple, or macOS LPE."
---

# Apple macOS Research

**Use this corpus as a living lab notebook.** Read the guidance, map surfaces,
adapt checks to the *current* authorized macOS build, and edit the local clone
when the user asks. Do not replay zipped submission packages against a host.

Local clone (writable):

`/home/kali/security-research/AppleResearch`

Pin: `dawgyg/AppleResearch@110b51dee16b75001888012230e23b0a11b514d0` (no
license file → do not republish the dump; personal research use only).

## How to use it

1. Read `agent_guidance/AGENTS.md` first (verify both sides of every memory
   sink; physical-host hard lock).
2. Load the matching guidance file for the surface:
   `CODEX_DEEP_RE_RULES.md`, `broker_kernel_uc_candidates.md`,
   `clocksyncd_effect.md`, `webgpu_audit.md`, `helper_sweep_results.md`,
   `escalation_results_template.md`, `gemini.md`.
3. Treat `fuzzers/` and `submission_packages/` as **evidence indexes**, not
   runnable kits. Names hint surfaces (smbd, nfs rpcsecgss, UDF/exFAT/cd9660,
   softraid, installd, syspolicyd, screensharingd, remoted, opendirectoryd,
   storagekitd, WebGPU/USD). Re-derive the bug on the authorized current
   build; do not assume a 2026 zip still hits.
4. Default dynamic work to an identified VM. The physical Mac is read-only
   static analysis until the user gives a literal `go` for that exact command.
5. Before any VM trigger, verify hostname, `sw_vers -buildVersion`, `id -u`,
   and virtualization identity in the same session.
6. Findings start in quarantine. Promote only after clean-snapshot
   reproduction as the claimed low-privilege user.

## How to modify it

- Edit files under the clone `agent_guidance/` when the user wants new rules,
  templates, or surface notes.
- Add new guidance files rather than bloating this wrapper.
- Keep `PINNED.json` updated if the clone moves.
- Never copy PoC binaries or exploit zips into the skill pack.

## Mandatory routing

Start with `mandatory-auto-router` and `authorized-security-autopilot`. Also
load `executable-binary-auditor` / `expert-c-cpp-engineer` when the artifact
is native, and `expert-mobile-client-hunter` only for iOS/ipa evidence.

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
Prefer unprivileged local entry (XPC, filesystems, network services, helpers)
over already-root contexts. This posture does not authorize host panics,
kernel extension loads, or replay of third-party submission packages.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

For every security-focused invocation, ensure `mandatory-auto-router` is
active, evaluate `config/AUTO_ROUTING_MAP.json`, load this skill when `ACTIVE`,
and preserve `DEFERRED` / `NOT_APPLICABLE`. Never auto-run AppleResearch
fuzzers, zips, or host PoCs.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
