---
name: redsun-defensive-researcher
description: "Authorized offensive security analysis skill for RedSun-style Microsoft Defender remediation and link-resolution privilege-boundary research. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# RedSun Authorized Offensive Researcher

Repository reference: `https://git.projectnightcrawler.dev/NightmareEclipse/RedSun`

This skill converts a public Windows exploit repository into an **authorized adversarial exploitability, privilege-transition, root-cause, and patch-bypass research workflow**. It must not be used to operationalize or deploy the exploit.

## Mandatory safety and validity gates

- Treat the public repository as **known prior art**. Reproducing it alone is not a new bounty finding.
- Work only in a disposable, isolated Windows lab on researcher-owned systems and data.
- Do not publish modified exploit binaries, increase reliability for operational use, add persistence/evasion, or run against third parties.
- Pin exact Windows build/KB and component versions; public status and patching can change rapidly.
- Use inert marker effects, debugger/ETW/Procmon evidence, snapshots, and cleanup.
- A retained candidate must identify a new root cause, incomplete patch, distinct bypass, broader current-release reachability, or a separate security boundary with concrete impact.
- Apply STRONG / MEDIUM / WEAK / KILL and stop at evidence handoff.

## Research focus

Microsoft Malware Protection Engine remediation, cloud-placeholder metadata, link/reparse resolution, privileged file restoration/writes, quarantine state, and patch verification.

## Claim discipline

Public advisories associate RedSun with improper link resolution before privileged file access. Verify the exact engine version and remediation path instead of assuming all Defender file operations are affected.

## Core investigation questions

- What object/path is validated before remediation and what object is opened for the privileged write?
- How do Cloud Files tags or placeholder state alter the normal quarantine/delete/restore path?
- Are links/reparse points resolved under caller or service context, and is the final handle revalidated?
- Does the current engine open by ID/handle or still re-resolve attacker-controlled names?
- Can the effect reach a protected file with an inert marker and no destructive overwrite?

## Static analysis checklist

- Inventory source files, embedded binaries/resources, build instructions, compiler assumptions, and missing/stripped pieces.
- Separate author claims from code-proven behavior and from independently observed runtime evidence.
- Identify attacker-controlled paths, object names, metadata, timing, accounts, files, partitions, or inputs.
- Trace Windows APIs to the service/driver/component that performs the privileged action.
- Record every security descriptor, token/impersonation change, handle, object namespace, path resolution, and state transition.
- Compare current source with vendor patch diffs, symbols, component binaries, and sibling code paths.

## Safe dynamic validation

- Snapshot an isolated VM and record OS/KB/component versions before testing.
- Replace command shells or destructive targets with an inert marker or debugger breakpoint where technically possible.
- Capture Procmon/ETW/debugger timelines, process tree, tokens, file/registry/object changes, and service health.
- Include a negative control that removes the suspected race/link/state condition.
- Revert the VM after each run; do not leave security controls disabled or sensitive data mounted.

## Candidate rules

**STRONG** only for a distinct, current, release-reachable security boundary with complete evidence and prior-art separation.  
**MEDIUM** when root cause and impact are credible but current patch/reachability or a key control is incomplete.  
**WEAK** for an interesting code path without a safe demonstrated boundary.  
**KILL** for simple reproduction, known CVE behavior, old patched builds, sample-detection bypass only, equal-privilege prerequisites, or unsupported impact.

## Required handoff

- Exact repository commit/source snapshot and hashes
- Exact Windows/component versions and configuration
- Author claim versus independently proven behavior
- Input -> check -> object substitution/state transition -> privileged use -> effect
- Token, object identity, path/hive/section/file IDs, and timing evidence
- Baseline, negative control, cleanup, and VM snapshot state
- Vendor advisory/CVE/patch and duplicate/prior-art result
- Newness statement: new root cause, patch bypass, sibling path, or none
- Verdict and highest-value next verification step


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

This skill never operates as a silent standalone module. For every security-focused invocation:

1. ensure `mandatory-auto-router` is active;
2. evaluate all installed skills and supporting artifacts through `config/AUTO_ROUTING_MAP.json`;
3. apply this skill only when marked **ACTIVE**, while recording **DEFERRED** and **NOT_APPLICABLE** routes;
4. load this skill's mapped companion prompts, references, worksheets, and safety protocols;
5. rerun routing after material discoveries that change language, runtime, platform, trust boundary, sink, release reachability, or prior art;
6. never auto-execute operational automation without explicit authorization and safety controls.

If the router is already active, acknowledge the existing routing session and do not recursively bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->

