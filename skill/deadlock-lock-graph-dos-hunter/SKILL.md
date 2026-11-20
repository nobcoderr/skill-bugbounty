---
name: deadlock-lock-graph-dos-hunter
description: "Expert authorized workflow for finding and validating deadlocks, lock-order inversions, recursive logging locks, livelocks, and remotely reachable availability failures in source code, RPC services, nodes, daemons, and shipped binaries. Use when thread dumps, mutex ownership, logging or exception paths, build flags, or patch diffs indicate circular wait. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Deadlock and Lock-Graph DoS Hunter

Audit whether attacker-controlled work can place a current, in-scope service in
a genuine circular wait or equivalent unrecoverable availability state. The
core invariant is:

> Untrusted requests cannot force service threads to acquire shared resources
> in an inconsistent or re-entrant order that prevents bounded progress.

Read `references/deadlock-lock-graph-dos-method.md` whenever this skill is
active. Treat Monero HackerOne #3307874 as public, fixed prior art whose useful
lesson is lock-graph and build/configuration validation—not its overstated
headline, CVSS, or unsupported integrity and confidentiality claims.

## Scope and safety gate

- Confirm that availability testing is explicitly eligible. Generic source-code
  scope does not authorize load testing or denial of service.
- Prefer static analysis, patch diffing, model checking, unit tests, and an
  isolated local fixture. Never target public nodes or third-party services.
- Before any runtime test, define exact binary/hash, build flags, configuration,
  bind address, test data, request ceiling, concurrency ceiling, timeout,
  watchdog, resource limits, abort conditions, recovery, and cleanup.
- Do not automate floods, oversized batches, compression amplification,
  randomized `User-Agent` or `X-Forwarded-For`, rate-limit evasion, or adaptive
  bypass logic.
- Snapshot disposable state and prove recovery. A process requiring `SIGKILL`
  is evidence of a stalled process, not proof of permanent state damage.

## Mandatory distinction: deadlock is not generic slowness

Classify the observed failure before assigning a verdict:

| Class | Required evidence |
|---|---|
| Deadlock | Stable wait-for cycle with each thread waiting on a resource held by another participant |
| Self-deadlock | A thread re-acquires a non-recursive lock it already owns |
| Livelock | Threads continue executing but the protected operation makes no progress |
| Starvation | A runnable participant is indefinitely denied a resource without a circular wait |
| Resource exhaustion | Memory, descriptors, queue slots, workers, CPU, or disk are saturated |
| Slow path | Work eventually completes within a justified operational bound |
| Crash | Process terminates; no lock-cycle claim without independent evidence |

High thread counts, blocked requests, missing logs, or an unresponsive signal
handler do not by themselves prove a deadlock.

## Evidence workflow

### 1. Build the target evidence card

Record program, exact asset, release/tag/commit, binary hash, official versus
self-built artifact, compiler/build type, compile definitions, dependency
versions, OS/architecture, runtime flags, log level/categories, RPC exposure,
authentication/restriction mode, and prohibited test methods.

### 2. Screen prior art first

Search open and closed issues, PRs, merged fixes, discussions, advisories, CVEs,
commit history, changelog, release notes, docs, known issues, and maintainer
comments. Search by lock names, stack frames, logging/exception paths, symptom,
configuration, and fix shape—not only the report title.

### 3. Trace the full progress path

Map:

`remote/local input -> RPC/parser/batch dispatcher -> handler -> shared state -> exception/stack trace/log writer -> lock acquisition/re-entry -> blocked service surfaces`

Identify every lock, owner, waiter, acquisition site, release site, scope, rank,
recursive/non-recursive property, condition variable, callback, destructor,
exception edge, and logging call made while another lock is held.

### 4. Reconstruct a real wait-for graph

For each frozen snapshot, build both graphs:

- lock-order graph: `Lock A -> Lock B` means code may acquire B while holding A;
- runtime wait-for graph: `Thread -> Lock -> Owner thread` from debugger or
  instrumented evidence.

A retained deadlock needs a stable cycle, exact source frames, and consistent
lock identities. Repeatedly capture all-thread stacks so a transient wait is not
mistaken for a cycle.

### 5. Prove release and configuration reachability

Compare official release artifacts with debug/custom builds. Verify compile-time
definitions such as `STACK_TRACE`, logging configuration, and optional
dependencies from the actual binary—not assumptions from source. Test default,
candidate, and disabled-path controls such as lower log level when safe.

### 6. Use bounded controls

Minimum matrix:

- idle and ordinary-request baseline;
- same workload with the suspected logging/exception path disabled;
- sequential versus the smallest bounded concurrent trigger;
- vulnerable versus patched build from the same toolchain/configuration;
- official release versus custom/debug build when reachability differs;
- restart/recovery and state-integrity comparison using disposable data.

Do not increase traffic merely because the first run did not reproduce. A path
that requires unsafe stress is `KILL` for testing unless the written rules
expressly permit an isolated load test.

### 7. Bound impact precisely

Prove each impact independently:

- RPC unavailability;
- P2P or background-worker unavailability;
- local administrative-command failure;
- process signal/recovery behavior;
- restart success and downtime;
- persistent state corruption using authoritative checks;
- network-wide or multi-node impact.

Availability loss does not imply confidentiality loss, integrity loss,
database corruption, fund loss, or network-wide catastrophe.

## Evidence ladder

- **D0:** suspicious nested locks, logging under lock, or source/patch signature;
- **D1:** exact endpoint, call path, build, and configuration are reachable;
- **D2:** bounded isolated reproduction shows a persistent progress failure;
- **D3:** repeated thread dumps establish the concrete wait-for cycle;
- **D4:** the minimum attacker-controlled trigger and affected service surfaces
  are reproduced with baseline and negative control;
- **D5:** the invariant-restoring patch breaks the cycle while preserving normal
  behavior;
- **D6:** exact shipped/deployed exposure, recovery cost, and availability impact
  are proven without inflating integrity/confidentiality claims;
- **D7:** scope, current-release reachability, novelty, prior-art clearance,
  repeated manual confirmation, cleanup, and evidence preservation pass.

Only D7 is **STRONG / MANUALLY_CONFIRMED** and report-ready.

## Hard KILL rules

KILL when the path is public/fixed/duplicate, absent from official releases,
requires a non-default custom build excluded by policy, is unreachable without
an explicitly enabled public listener, reproduces only through prohibited load,
lacks a stable wait-for cycle, is merely slow/resource-exhausted, recovers
normally within the service contract, or claims corruption/confidentiality/
network impact without direct evidence.

Monero HackerOne #3307874, PRs #10065/#10066, commits `179c924`/`36b12ed`, and
release v0.18.4.3 are an existing duplicate family. Reproducing that lineage is
not a new finding; retain only a distinct current root cause, incomplete fix,
sibling path, or release-reachable regression with its own proof.

## Required output

| Candidate | Verdict | Endpoint/input | Exact artifact/build | Configuration | Lock cycle | Minimum bounded trigger | Affected surfaces | Recovery/state result | Patched control | Prior art | Manual status |
|---|---|---|---|---|---|---|---|---|---|---|---|

If no candidate reaches D7, return **NO VALID FINDING**.


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
