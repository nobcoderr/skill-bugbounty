---
name: chromium-v8-variant-hunter
description: "Patch-led, evidence-first variant analysis for explicitly authorized Chromium and V8 security research. Use when a public fixed Chrome/V8 issue, CVE, CL, regression test, or compiler invariant can seed a bounded search for current release-reachable siblings, especially JIT metadata, equality/hash/cache-key completeness, deoptimization, representation, state, or lifecycle bugs. Automatically bootstraps the mandatory auto-router. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof. Do not use for random whole-tree ideation or to treat historical PoCs as new findings."
---

# Chromium V8 Variant Hunter

Use public, fixed bugs as semantic seeds. The objective is a new current root
cause with a deterministic Chrome-relevant oracle, not a renamed historical
bug or more raw candidates.

## Required context

Start through `mandatory-auto-router`, `authorized-security-autopilot`, and
`program-impact-boundary-gate`. Read:

- `references/DERIVED_METADATA_EQUIVALENCE_VARIANT_METHOD.md` for the core
  equality/hash/cache methodology.
- `references/CHROME_PUBLIC_REPORT_ROUTING.md` for source priority, eligibility,
  and the study ladder.
- `../../prompts/CHROMIUM_V8_VARIANT_HUNTER.md` for the execution
  and output contract.

Before source review, freeze a target/scope card containing the current Chrome
VRP rules, exact repository and revision, release channel, platform, component,
attacker-controlled input, trusted consumer, expected invariant, allowed flags,
and safe test boundary. If authorization, scope, or release reachability is
unclear, stop at `DEFERRED_SCOPE`.

## Operating sequence

1. **Choose one public root.** Start at Chrome Releases, then the public
   Chromium issue, landed CL, commit, and regression test. Record the vulnerable
   and fixed revisions and the exact semantic invariant restored by the patch.
2. **Freeze the root card.** Separate the compared identity, omitted fact,
   equivalence mechanism, optimizing consumer, invalidation/deopt event, and
   observable consequence. Historical code and PoCs are prior art only.
3. **Build the completeness matrix.** For the relevant type hierarchy, enumerate
   base and derived fields and every equality, hash, cache key, interning key,
   clone/copy, serializer, and invalidation path. A hash collision is harmless
   if a complete equality check follows it.
4. **Trace the consumer.** Prove that an incomplete identity reaches CSE/GVN,
   memoization, type feedback, deoptimization, code generation, parser reuse,
   or another protected consumer. Field omission without a divergent consumer
   is not a finding.
5. **Generate bounded siblings.** Prefer same abstraction and nearby call sites,
   then analogous compiler tiers. Hold all base fields constant and vary one
   security-relevant derived fact. Reject payload, identifier, and encoding
   churn as `MUTATION_ONLY`.
6. **Falsify before exploitation.** Check type discriminators, pointer identity,
   later recomputation, invalidation, build flags, feature state, and current
   source. First prove a harmless wrong-value, wrong-type, stale-state, or
   incorrect-merge oracle.
7. **Validate in an owned lab.** Use byte-identical source revisions and paired
   vulnerable/patched controls. Prefer an upstream regression shape, d8, ASAN,
   traces, and a minimized local HTML/JS reproducer. Do not modify the target to
   manufacture the bug.
8. **Recheck Chrome reachability.** A retained candidate must reproduce on a
   currently eligible Stable, Beta, or Dev build under accepted configuration,
   or remain `STRONG_SOURCE_HOLD`. Test-only intrinsics may explain a root but
   do not establish a flag-free Chrome path.
9. **Screen prior art again.** Search public issues, CLs, commits, regressions,
   CVEs, release notes, and researcher write-ups by exact root cause and fix
   requirement. Same-root public/fixed work is `KILL_KNOWN_OR_DUPLICATE`.
10. **Apply the impact gate.** Require a nonzero capability delta and concrete
    renderer, sandbox, memory-safety, confidentiality, integrity, or authority
    consequence recognized by the current program.

## Runtime chain research loop

When a validated primitive changes attacker capability, activate
`exploit-chain-research-orchestrator` and continue with this exact loop:

```text
source audit -> build exact revision -> debug instrumentation -> benign PoC
-> crash/wrong-value triage -> primitive classification -> attacker post-state
-> newly reachable surfaces -> next primitive search -> proven chain edge
```

An out-of-bounds read/write, type confusion, stale object, or miscompile is not
the terminal conclusion. Record what object or representation is controlled,
which checks remain, what scoped capability follows, and what protected
consumer is newly reachable. A V8-sandbox arbitrary read/write does not imply
renderer or browser-process authority.

Use these logical roles in the current agent by default; subagents require an
explicit user request:

- `prompts/v8-type-reasoning-agent.md`
- `prompts/v8-representation-agent.md`
- `prompts/v8-jit-assumption-agent.md`
- `prompts/v8-gc-lifetime-agent.md`
- `prompts/v8-sandbox-boundary-agent.md`
- `prompts/v8-exploitability-agent.md`
- `prompts/chrome-chain-linker.md`

For failed runtime attempts, classify `FAIL_REACHABILITY`,
`FAIL_TYPE_CONSTRAINT`, `FAIL_SANDBOX`, `FAIL_LIFETIME`,
`FAIL_CANONICALIZATION`, `FAIL_PRIVILEGE`, `FAIL_REPRESENTATION`, or
`FAIL_NONDETERMINISM`. Change only the failed assumption and retry only when new
material evidence supports the mutation.

## Canonical seed invariant

For CVE-2026-6307, treat this as a historical pattern, not a candidate:

```text
derived type carries security-relevant metadata
        -> base equality/hash/cache identity omits it
        -> optimizer treats distinct recovery states as equivalent
        -> wrong metadata reaches deoptimization/materialization
        -> wrong representation or type
        -> memory-safety consequence
```

Search for variants only when the new site has a different unburned root,
current reachability, and its own proof. Also inspect object slicing and copying,
because a correct equality check does not repair metadata lost before comparison.

## Verdict contract

Use one of these exact outcomes:

- `STRONG + MANUALLY_CONFIRMED`: current eligible Chrome build, exact source
  trace, deterministic runtime proof, negative and patched controls, current
  prior-art screen, and program-recognized impact all pass.
- `STRONG_SOURCE_HOLD`: compelling source and local evidence, but Chrome release
  reachability, accepted configuration, reliability, or manual browser proof is
  incomplete.
- `HYPOTHESIS`: a concrete traceable invariant with a falsifier, but no runtime
  violation yet.
- `KILL_KNOWN_OR_DUPLICATE`, `KILL_NO_PRODUCTION_REACHABILITY`,
  `KILL_EXPERIMENTAL_OR_UNSAFE_CONFIG`, `KILL_ZERO_CAPABILITY_DELTA`, or
  `NO VALID FINDING`.

Candidate count and exploit sophistication never substitute for exact-root
proof. Preserve killed roots so later searches cannot rescue them by renaming.

## Safety boundary

Use researcher-owned local builds and benign oracles. Never target third-party
browsers or users. Do not auto-run public exploit repositories, shellcode,
sandbox escapes, heap grooming, arbitrary read/write, or code-execution payloads.
Escalate beyond a crash or wrong-value oracle only when explicitly authorized,
necessary for the program impact threshold, and bounded to the minimum harmless
proof with cleanup.

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
`attacker objective -> reachable entrypoint -> exploit chain -> privilege or authority transition -> protected sink -> concrete impact`.
Search for attack paths, representation failures, stale security metadata,
incorrect compiler reuse, memory corruption, renderer compromise, and sandbox
boundary transitions supported by target evidence. Use defensive controls,
detection, remediation, and hardening primarily as falsifiers or post-proof
guidance unless the user explicitly requests blue-team work. This posture never
expands authorization: preserve exact scope, safe harbor, harmless proof, rate
limits, stop conditions, cleanup, and prohibitions on destructive, stealthy,
credential-stealing, persistence, evasion, or third-party activity.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

This skill never operates as a silent standalone module. For every
security-focused invocation:

1. ensure `mandatory-auto-router` is active;
2. evaluate installed skills and supporting artifacts through
   `config/AUTO_ROUTING_MAP.json`;
3. apply this skill only when marked **ACTIVE**, while recording **DEFERRED** and
   **NOT_APPLICABLE** routes;
4. load the mapped prompt, references, checklists, and safety protocols;
5. rerun routing after discoveries that change runtime, compiler tier, platform,
   trust boundary, release reachability, or prior art;
6. never auto-execute operational automation or public exploits.

If the router is already active, acknowledge the existing routing session and
do not recursively bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
