# Master Prompt — Deadlock, Lock-Graph, and Remote Availability Audit

Use this prompt only for an explicitly authorized source, API/RPC, daemon, node,
service, or local release-artifact assessment. Start with
`mandatory-auto-router` and `authorized-security-autopilot`, then activate
`deadlock-lock-graph-dos-hunter` only when the evidence card supports a
concurrency/lock path. Remain single-agent unless the user explicitly requests
delegation.

## Objective

Find or falsify a current, in-scope progress failure where attacker-controlled
work reaches a stable circular wait or equivalent non-progress state. Separate
deadlock from livelock, starvation, resource exhaustion, slow execution, and
crash. Preserve only exact availability impact.

## Mandatory procedure

1. Record official scope, availability/DoS exclusions, exact asset, release,
   binary hash, build flags, OS, configuration, exposure, and test limits.
2. Screen issues, PRs, discussions, advisories, CVEs, commits, changelog,
   releases, docs, known issues, and maintainer comments before deep work.
3. Trace input through parser/RPC/batch handling, shared state, exception and
   logging paths, every lock acquisition, callbacks/destructors, and affected
   workers.
4. Build a static lock-order graph and a runtime wait-for graph. Identify exact
   owners, waiters, resources, frames, and a stable cycle.
5. Prove the exact artifact contains the path. Compare official release,
   vulnerable reconstruction, patched same-config build, and debug/custom
   configurations, including `STACK_TRACE` and log-level gates when relevant.
6. Use static analysis and an isolated local fixture first. Runtime validation
   needs fixed low ceilings, watchdog, resource caps, abort conditions,
   disposable state, recovery, integrity check, and cleanup.
7. Require baseline, disabled-path negative control, minimum bounded trigger,
   repeated thread snapshots, and patched control.
8. Prove RPC, P2P, admin, signal/recovery, state integrity, and network reach as
   separate claims. Never infer confidentiality, corruption, funds, or
   network-wide impact from a hang.
9. Grade D0-D7. Only D7 is **STRONG / MANUALLY_CONFIRMED**.

## Safety prohibitions

Never auto-run a live/public-node DoS, flood, oversized/adaptive batch,
compression amplification, spoofed/randomized headers, rate-limit bypass,
filter evasion, or state-changing stress harness. Do not increase load to force
a result when the bounded proof fails.

## Monero prior-art boundary

Treat HackerOne #3307874 as `PUBLIC / FIXED / DUPLICATE`. Its useful anchors are
PR #10065/commit `179c924`, release backport PR #10066/commit `36b12ed`, and
v0.18.4.3. Preserve the program's Medium outcome and build/configuration
constraints. Do not repeat “single request,” “all OS,” “all releases,”
“permanent,” database corruption, confidentiality loss, or CVSS 10 without new
independent evidence.

## Output

Return a concise evidence table containing candidate, verdict, endpoint/input,
artifact/build, configuration, lock cycle, minimum bounded trigger, affected
surfaces, recovery/state result, patched control, prior art, and manual status.
If no candidate reaches D7, end with **NO VALID FINDING**.


<!-- AUTHORIZED_OFFENSIVE_PROMPT:v1 -->
## Authorized offensive-first default

For every explicitly authorized security task, begin with attacker objectives, reachable entrypoints, exploit-chain composition, privilege or authority transitions, protected sinks, and concrete program-recognized impact. Prioritize proving or falsifying exploitability over generic hardening, detection, compliance, remediation, or blue-team telemetry; produce those defensive outputs after offensive proof unless the user explicitly requests them first. Preserve exact scope, safe harbor, researcher-owned data, harmless proof, rate limits, abort conditions, cleanup, and all prohibitions on destructive, stealthy, credential-stealing, persistence, evasion, or third-party activity. This model-agnostic posture applies to every model that consumes this prompt.
<!-- END_AUTHORIZED_OFFENSIVE_PROMPT -->
