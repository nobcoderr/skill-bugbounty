# Deadlock, Lock-Graph, and Remote Availability Method

## Purpose

Use this reference for authorized source and local-artifact audits where a
request, message, batch, exception, stack trace, logger, callback, or shutdown
path may create circular wait or another non-progress state. The reusable chain
is:

`attacker-controlled work -> concurrency/interleaving -> nested or re-entrant lock acquisition -> wait-for cycle -> bounded service availability loss`

Do not reduce the bug class to “many threads make the service hang.” That
description also fits queue saturation, resource exhaustion, pathological
complexity, disk stalls, and ordinary overload.

## Target and scope evidence card

| Field | Required evidence |
|---|---|
| Authorization | Named program/owner and explicit permission for source review and any availability testing |
| Asset | Repository/component plus exact RPC/service/binary in scope |
| Snapshot | Commit/tag/release, dependency revisions, binary hash, observation time |
| Build | Official or self-built, compiler, build type, compile definitions, optional libraries |
| Platform | OS, architecture, container/service manager, signal and thread model |
| Exposure | Bind address, external-bind confirmation, proxy, authentication, restricted mode |
| Configuration | Log level/categories, worker/thread count, batch/body limits, timeouts |
| Trigger | Exact controlled fields, request count, concurrency, batch size, payload bytes |
| Guardrails | Local-only allowlist, resource cap, watchdog, abort, snapshot, recovery, cleanup |
| Prior art | Issues, PRs, advisories, commits, releases, docs, maintainer comments |

An unresolved card is `DEFERRED`; it never authorizes a live test.

## Progress and lock model

For each candidate, write the progress invariant first:

> Every accepted operation either completes, fails, or is cancelled within a
> justified bound, and no thread waits forever for a resource whose release
> depends on that same wait chain.

Inventory:

- mutexes, recursive mutexes, read/write locks, spinlocks, semaphores, condition
  variables, futures/promises, event loops, thread pools, queues, database
  transactions, file locks, and process-global logger locks;
- constructors/destructors and RAII lifetime, especially when a temporary
  logger/writer owns synchronization state;
- exception and stack-unwinding paths, signal handlers, cleanup callbacks,
  shutdown joins, and log/error formatting;
- calls made under lock into extensible or blocking code: logging, formatting,
  allocation, filesystem, network, database, RPC, virtual dispatch, callbacks,
  plugins, and user-defined destructors.

Use an acquisition table:

| Thread/role | Held resource | Requested resource | Acquire frame | Owner/release frame | Recursive? | Blocking operation under lock | Evidence |
|---|---|---|---|---|---|---|---|

Then construct:

1. a static lock-order graph from all feasible paths;
2. a runtime wait-for graph from a frozen process;
3. an exception/logging graph showing callbacks and re-entry;
4. a progress graph showing which RPC, P2P, admin, and shutdown workers depend
   on the blocked participants.

## Proving a wait-for cycle

A candidate is not a confirmed deadlock until the evidence establishes:

1. at least one thread is blocked acquiring a known resource;
2. the resource owner is identified, not merely guessed from a symbol name;
3. the owner is blocked on another resource or event;
4. following ownership/wait edges returns to an earlier participant, or a
   non-recursive self-acquisition is shown;
5. repeated all-thread snapshots show the cycle is stable rather than transient;
6. the relevant stack frames map to the exact audited source and build.

Useful evidence can include debugger all-thread backtraces, mutex owner IDs,
thread-sanitizer/lock-order diagnostics, instrumented lock events, scheduler
traces, and deterministic tests. A process-level CPU graph or “29 threads
blocked” count is supporting context, not the graph itself.

## Build and release reachability

Build flags can remove the vulnerable path. Verify them from build metadata,
symbol/string inspection, disassembly, or a controlled runtime marker in the
exact artifact. Do not infer them from source defaults alone.

Matrix:

| Artifact | Build type | Relevant definition/feature | Logging path | Trigger reaches it? | Result |
|---|---|---|---|---|---|
| Official current release | | | | | |
| Official prior release | | | | | |
| Reconstructed vulnerable build | | | | | |
| Patched same-config build | | | | | |
| Debug/custom build | | | | | |

If only a self-built artifact with a non-default definition is affected, say so.
Do not label the corresponding official release vulnerable without independent
proof.

## Safe validation design

Availability testing is unusually easy to overstep. The default workflow is
static and local:

1. reproduce the build in a disposable isolated environment with no external
   listener;
2. use synthetic/minimal state and snapshot it before testing;
3. establish idle and ordinary-request baselines;
4. exercise the suspected path sequentially before any bounded concurrency;
5. use the smallest fixed request/concurrency/batch budget justified by the
   source trace;
6. capture thread state via a watchdog before the process is terminated;
7. compare the candidate path with a disabled-path negative control and a
   patched same-config build;
8. restart, run authoritative state-integrity checks, and clean up.

Stop on unexpected CPU, memory, disk, queue, network, or state growth. Do not
add gzip amplification, large bodies, randomized headers, address spoofing,
adaptive retries, filtering bypass, or public endpoints. If safe bounded proof
cannot distinguish the class, retain it as `WEAK` or `KILL`.

## Impact separation

| Claim | Minimum proof |
|---|---|
| RPC unavailable | Independent bounded health request times out/fails while baseline succeeds |
| P2P unavailable | Existing peer progress/handshake evidence stops for the same lock dependency |
| Admin unavailable | Local control path is blocked by the proven cycle |
| Requires force termination | Graceful signal observed and process remains in the same wait cycle |
| Persistent corruption | Post-restart authoritative integrity check shows a new reproducible defect caused by the trigger |
| Confidentiality loss | Concrete unauthorized data disclosure path, not unsafe-shutdown speculation |
| Network-wide impact | Multiple independently reachable nodes/default exposure and systemic effect are proven |

Never derive the last three rows from a local deadlock alone.

## Patch analysis

Classify the fix by invariant:

- establish one global lock order;
- acquire once at object construction and release through RAII;
- remove nested/re-entrant logging;
- move blocking/logging/callback work outside a critical section;
- narrow lock scope or split unrelated locks;
- replace shared mutable state with ownership/message passing;
- add cancellation/timeout only when it safely breaks the dependency;
- disable an optional path or compile feature (mitigation, not always root fix).

Verify parent, fix commit, merge commit, release-branch backport, tagged release,
and binary inclusion separately. A tiny patch can restore the invariant, but the
diff alone does not prove the entire original exploit narrative.

## Public prior art: Monero HackerOne #3307874

The user supplied the disclosed report **“Critical Deadlock Vulnerability in
Monero RPC Leading to Complete Node Paralysis”**, HackerOne #3307874, submitted
August 21, 2025. Preserve it as evidence-accurate prior art.

### What is supported

- Maintainers reproduced a logging-lock problem on Linux under relevant build
  and logging conditions and classified it under the program as **Medium** for
  an individual node with public RPC exposure and increased log level.
- The reporter confirmed that the proposed logging-lock fix stopped the
  reproduction.
- Monero PR #10065 merged the master fix on September 24, 2025. Source commit
  `179c924` changed `external/easylogging++/easylogging++.h` by adding
  `base::threading::ScopedLock m_sync` to `Writer` and initializing it with
  `ELPP->lock()` in both constructors. Merge commit: `b591866`.
- PR #10066 backported the same change to `release-v0.18`; source commit
  `36b12ed`, merge commit `2d19722`.
- The v0.18.4.3 release notes list “Fix logging deadlock (#10066).” The report
  was resolved against that release, and 5 XMR was paid under the program's
  Medium precedent.

These facts support an invariant-restoring serialization change over the
`Writer` lifetime. Without the report attachments or an independently captured
thread dump, they do not by themselves establish every edge in the original
wait-for graph.

Official anchors:

- HackerOne #3307874: https://hackerone.com/reports/3307874
- Fix commit: https://github.com/monero-project/monero/commit/179c924
- Master PR #10065: https://github.com/monero-project/monero/pull/10065
- Release PR #10066: https://github.com/monero-project/monero/pull/10066
- Release v0.18.4.3: https://github.com/monero-project/monero/releases/tag/v0.18.4.3
- Release task #10080: https://github.com/monero-project/monero/issues/10080
- VRP: https://github.com/monero-project/meta/blob/master/VULNERABILITY_RESPONSE_PROCESS.md

### Claims that must not be preserved as facts

- **“One request”** conflicts with the supplied PoC description: it invoked 50
  threads, batch size 500, resource-heavy/malformed mixtures, compression, and
  adaptive behavior. Preserve the exact minimum trigger as unproven.
- **“All operating systems”** was not demonstrated; the maintainer said only
  Linux had been reproduced at that stage.
- **“All release binaries”** was contradicted by the maintainer's later note
  that release binaries were not affected because `STACK_TRACE` was disabled.
  Audit official binaries and custom/debug builds separately.
- **“All run modes”** omits exposure prerequisites. Public RPC binding and the
  relevant logging/build path must be proven; `--restricted-rpc` limits methods
  but is not itself authentication.
- **“Permanent/irreversible”** is too broad. The process reportedly remained
  blocked until force termination; that does not prove irreversible state.
- **Database corruption, confidentiality loss, and integrity loss** were
  speculative. The maintainer explicitly distinguished the deadlock from DB
  corruption, and no disclosure path was shown.
- **CVSS 10/Critical** was reporter-defined. The program applied Medium based on
  individual-node scope, non-default conditions, and historical RPC-crash
  precedent.

### Reuse rule

This lineage is `PUBLIC / FIXED / DUPLICATE`. A new candidate survives only if
it proves a distinct current lock cycle, incomplete fix, sibling logging path,
or regression in an exact current artifact. Similar symptoms, reproducing the
old build, or citing the fix are insufficient.

## Evidence levels and KILL rules

- **D0-D2:** hypothesis to bounded stall;
- **D3:** concrete wait-for cycle;
- **D4:** minimum remote trigger and affected surfaces;
- **D5:** patched control;
- **D6:** shipped exposure and precisely bounded impact;
- **D7:** current scope, novelty, repeated manual proof, and cleanup.

Only D7 is report-ready. KILL public/fixed duplicates; paths absent from shipped
artifacts; non-default custom builds when excluded; tests requiring prohibited
stress; transient waits; resource exhaustion mislabeled as deadlock; and any
confidentiality, integrity, corruption, fund, or network claim without direct
evidence.
