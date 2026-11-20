---
name: openai-kernel-research-pipeline
description: "Apply and adapt OpenAI's autonomous Linux-kernel discovery, isolated validation, exploitability screening, and candidate-patch pipeline for authorized kernel research. Automatically bootstraps the mandatory auto-router and preserves an authorized offensive-first posture. Use for thousand fewer paths to root, OpenAI cyber model, 948 LPE, Patch the Planet, stock desktop kernel LPE, or kernel leak-vs-LPE funnels."
---

# OpenAI Kernel Research Pipeline

Load this skill whenever kernel vulnerability discovery, isolated reproduction,
LPE/leak screening, or AI-assisted kernel patching is in play. **Use the
pipeline. Adapt the stages to the authorized kernel. Do not treat OpenAI's
counts, dollars, or novelty claims as local facts.**

Pinned public claims (all `UPSTREAM_CLAIM` until independently reproduced):

- Source: OpenAI, 5 Nov 2026, "One thousand fewer paths to root"
- Stated funnel: 2308 candidates → 1724 validated → 291 working leak PoCs and
  948 working LPE exploits on a stock Linux desktop with standard protections
- Stated cost: about $1,213,430 API credits
- Stated novelty: at least 10 previously unseen Linux exploitation techniques
- Stated process: human researchers review before maintainer reports/patches

Those numbers are not findings in this workspace.

## How to use it

Run the stages in the current agent. Edit stage prompts, isolation notes, and
kernel version pins in this directory when the user asks to modify the
pipeline.

1. **Discovery** — map security-sensitive kernel code (syscalls, ioctls,
   filesystems, net, drivers, LSM hooks). Every hit starts as
   `HYPOTHESIS_QUARANTINED`.
2. **Dynamic validation** — only in an isolated, researcher-owned VM/snapshot.
   Confirm the issue is real, triggerable, and impactful. Fail closed on host
   kernel.
3. **Screening** — split leak candidates from LPE candidates. Do not promote a
   leak to LPE without a new primitive.
4. **Exploitability assessment** — prove the claimed attacker context on a
   stock config with standard protections (SMEP/SMAP/KPTI/KASLR/and current
   distro defaults). This is the low-privilege gate.
5. **Candidate patches** — generate a patch only after a validated primitive.
   Rebuild, re-run the triggering case, and record the negative control.
6. **Human review** — no maintainer report without `MANUALLY_CONFIRMED` plus
   `TRIAGER_PROOF=PASS`.

Keep leak PoCs and LPE proofs on separate ledgers. Volume is not severity.

## How to modify it

When the user wants this pipeline changed:

- Edit this `SKILL.md` and `PINNED.json` in place.
- Narrow Discovery to the exact subsystem/version in scope.
- Change isolation (QEMU, virtme, syzkaller, distro VM) only with explicit
  runtime authorization.
- Keep OpenAI's funnel as a **shape**, not a quota. Never optimize for
  matching 948.

## Mandatory routing

Start with `mandatory-auto-router` and `authorized-security-autopilot`. Also
load `agentic-security-research-harness` and
`external-ai-security-tool-governor`. Kernel C/C++ specialists load only when
the authorized tree is actually Linux/XNU kernel source or a live authorized
kernel lab.

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
Use isolated reproduction and stock-protection bypass as proof, then patch.
This posture grants no live testing of unscoped kernels, no exploit
publication, and no skipping human review.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

For every security-focused invocation, ensure `mandatory-auto-router` is
active, evaluate `config/AUTO_ROUTING_MAP.json`, load this skill when `ACTIVE`,
and preserve `DEFERRED` / `NOT_APPLICABLE`. Never auto-run kernel exploits,
fuzzers, or VMs.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
