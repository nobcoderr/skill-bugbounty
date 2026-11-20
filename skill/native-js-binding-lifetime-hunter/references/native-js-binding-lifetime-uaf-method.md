# Native JavaScript Binding Lifetime and UAF Method

## Purpose

Use this method for authorized review of V8/Gin, Blink, Electron, Node/N-API,
WebView, extension, renderer, or other JavaScript-to-native bindings. The
reusable failure is an ownership disagreement:

`JavaScript-reachable callable -> raw or externally owned native receiver -> receiver destruction -> later callback -> use-after-free`

The test is not whether a suspicious pointer exists. The test is whether a
realistic JavaScript object graph can keep the callable alive after the native
receiver dies on a current shipped path.

## Authoritative platform model

- V8 local handles live within a handle scope. Once that scope is gone, an
  object may be reclaimed if JavaScript and other handles no longer reach it.
  Persistent/weak handles exist for lifetimes that cross calls.
- Chromium Gin describes `gin::Wrappable` as a native object owned through its
  corresponding V8 wrapper; the wrapper's weak callback is the deletion signal.
- Chromium callback guidance permits `base::Unretained` only when an external
  guarantee proves the receiver outlives every callback. `WeakPtr` provides
  cancel-on-destroy behavior when that guarantee is absent.
- Chromium's dangling-pointer guidance treats an invoked dangling
  `base::Unretained` callback as a UAF/crash even where mitigations reduce
  exploitation. Do not use mitigations to deny the lifetime bug or use the UAF
  alone to claim code execution.
- AddressSanitizer is the preferred local evidence for allocation, free, and use
  stacks. A symbolized report must be tied back to the same source and release.

Primary references:

- V8 embedding and handle lifetime: https://v8.dev/docs/embed
- Chromium Gin overview: https://chromium.googlesource.com/chromium/src/+/HEAD/gin/
- Chromium callback guidance: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/callback.md
- Chromium dangling `Unretained` guidance: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/unretained_dangling_ptr_guide.md
- Chromium ASan guide: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/asan.md

## Target and scope evidence card

| Field | Required evidence |
|---|---|
| Authorization | Program/internal authorization and permitted local/runtime testing |
| Exact asset | Repository, component, package, signed binary, or release archive |
| Version identity | Tag/commit, artifact hash, channel, platform, architecture |
| Binding framework | V8/Gin, Blink, Electron, Node/N-API, WebView, or custom bridge |
| Attacker position | Web content, extension, renderer script, local file, plugin, or trusted UI |
| Feature mode | Provider choice, flag, policy, default, fallback, or extension state |
| JS graph | Parent, proxy target/handler, child, function, closure, realm/context |
| Native graph | Wrapper, receiver, owner, raw/weak/strong edge, remote/observer |
| Teardown | GC, delete/overwrite, navigation, frame/context destruction, disconnect, unload |
| Process boundary | Renderer, utility, browser, service, helper, sandbox, privilege |
| Restrictions | Live target, real wallet/data, exploit development, DoS, automation |

Missing fields are `DEFERRED`; they are never permission to assume reachability.

## Dual object and ownership graph

Build both graphs and align their edges.

### JavaScript graph

`global/property -> proxy -> target/handler -> parent wrapper -> child object -> function/closure -> native trampoline`

For every node record:

- owning realm/context/frame;
- strong references held by attacker JavaScript;
- `configurable`, `writable`, getter/setter, proxy traps, and overwrite behavior;
- whether deletion actually succeeds;
- whether navigation or context loss invalidates it;
- whether a child/function can be retained independently of the parent.

### Native graph

`V8 wrapper -> gin/native receiver -> parent/service/frame/remote -> callback state`

Classify every edge:

| Edge | Meaning | Required proof |
|---|---|---|
| Strong/ref-counted | Receiver cannot die while edge exists | exact owner and release behavior |
| GC-owned wrapper | Native deletion follows wrapper weak callback | wrapper identity and child relationship |
| `WeakPtr` | Callback is cancelled after destruction | factory order and invalidation path |
| Raw/`Unretained` | No ownership added | complete external lifetime proof |
| Owned remote/receiver | Pending work may cancel on disconnect | documented disconnect and callback behavior |
| Observer/context hook | Explicit teardown invalidation | registration, ordering, and all exit paths |

The essential differential is:

`JS node still reachable` **while** `native receiver already freed`.

## Discovery signatures

Search for combinations, never lone keywords:

- JavaScript-exposed child or function bound to a parent through
  `base::Unretained(parent)`;
- a plain `v8::Object`, proxy, accessor, or closure retaining a method after a
  Gin/native parent wrapper can be collected;
- wrapper children stored only as raw native pointers or created outside the
  parent's managed wrapper graph;
- callbacks posted across sequences, Mojo/IPC, promises, timers, tasks, or
  navigation without weak/cancel-on-destroy semantics;
- context/frame observers that invalidate some but not all callbacks;
- property configuration or provider mode that changes whether a global can be
  overwritten or deleted;
- extensions or fallback providers that replace the same global object;
- a patch that changes a child from plain V8 object to `gin::Wrappable`, raw
  bind to weak bind, or adds teardown invalidation;
- crash stacks near native trampolines after GC/navigation/disconnect.

A `base::Unretained` match alone is `L0 / HYPOTHESIS`. Prove the lifecycle.

## Configuration and lifetime matrix

| Build/version | Platform/arch | Feature/provider mode | Property descriptor | Attacker retains | Owner-loss event | GC/context behavior | Result/trials |
|---|---|---|---|---|---|---|---|
| Baseline | | | | | | | |
| Candidate | | | | | | | |
| Negative | | | | | | | |
| Patched | | | | | | | |

Also record allocator/mitigations such as ASan, PartitionAlloc, BackupRefPtr,
MiraclePtr/raw_ptr, sandbox level, and whether the build materially differs from
the released artifact.

## Safe validation protocol

Use a local, isolated, researcher-owned profile with no wallet seed, funds,
credentials, personal browsing data, extensions unrelated to the test, or
third-party origin. Do not deploy the trigger publicly.

1. Confirm the exact property descriptor and provider/feature setting.
2. Establish a baseline where parent and child remain reachable.
3. Retain only the candidate child/function and exercise the owner-loss event.
4. Verify the owner is destroyed through instrumented logs/debugger or sanitizer
   lifetime evidence; do not infer it from allocation pressure.
5. Invoke the retained callable and capture the symbolized ASan/HWASan report.
6. Repeat enough trials to distinguish probabilistic GC from unrelated crashes.
7. Run negative controls: deletion/overwrite fails, parent remains retained,
   callback is invalidated, wrong feature mode, or no owner loss.
8. Run the fixed build/tag and require the UAF to disappear for the intended
   invariant, without accepting a silent functional regression as the fix.
9. Clean the test profile, temporary files, crash dumps containing sensitive
   data, and feature configuration.

Use debug `--expose-gc` or a testing GC hook only to isolate the lifetime model;
also verify a release-equivalent trigger because a debug-only GC primitive is
not a shipped attacker capability. Never progress into heap grooming,
arbitrary-read/write, code execution, or sandbox escape.

## Impact ladder

| Level | What is proven | Maximum honest claim |
|---|---|---|
| I0 | Suspicious raw callback only | Hypothesis |
| I1 | Controlled renderer/process crash | Crash/availability, if eligible |
| I2 | ASan/HWASan allocation-free-use trace | Use-after-free/memory safety |
| I3 | Controlled non-executable corruption in lab | Corruption primitive |
| I4 | Harmless controlled instruction/control-flow effect | Code execution in that process |
| I5 | Proven cross-sandbox/privileged effect | Sandbox escape or privilege boundary |

Never borrow impact from the vulnerability class. I2 is not I4; I4 in a
renderer is not I5.

## Prior art: Brave JSEthereumProvider `_metamask` UAF

The user supplied a public HackerOne transcript titled **“UAF on
JSEthereumProvider”**, submitted to Brave on May 8, 2023. No stable HackerOne
report ID was provided, so this method does not invent one. Official Brave
source and patch history independently support the root-cause lineage:

- historical source commit:
  `45c6649a124dd8d0ffb19ca6f7047bebb6e6da2c`;
- component:
  `components/brave_wallet/renderer/js_ethereum_provider.cc`;
- the parent `JSEthereumProvider` was a Gin-wrapped object exposed through
  `window.ethereum`/a proxy;
- a plain JavaScript `_metamask` child exposed `isUnlocked`, whose callback was
  bound to `base::Unretained(provider.get())`;
- retaining the child while the parent became collectible could leave the
  callable pointing at a freed native provider;
- initial reproduction failed in the **Brave Wallet** provider mode because the
  global property was non-configurable; the vendor reproduced in **Extensions
  (wallet fallback)** where overwrite/delete behavior differed;
- reporter and vendor reproduced a renderer crash on a released 1.51 build, but
  the transcript did not demonstrate renderer code execution;
- brave-core PR #18411, merged May 9, 2023, changed `_metamask` into its own
  `gin::Wrappable` with a lifetime equivalent to its JavaScript wrapper;
- fix commit: `a8e497b`; uplift PRs #18418 and #18419 covered the 1.52.x and
  1.51.x release branches.

Official prior-art links:

- historical source: https://github.com/brave/brave-core/blob/45c6649a124dd8d0ffb19ca6f7047bebb6e6da2c/components/brave_wallet/renderer/js_ethereum_provider.cc
- fix PR: https://github.com/brave/brave-core/pull/18411
- fix commit: https://github.com/brave/brave-core/commit/a8e497b
- 1.52.x uplift: https://github.com/brave/brave-core/pull/18418
- 1.51.x uplift: https://github.com/brave/brave-core/pull/18419

Important falsifiers and lessons:

1. A PoC premise can be configuration-specific. Always verify property
   descriptors and deletion results instead of assuming a global is removable.
2. GC and allocator state make crash location and timing probabilistic. Require
   sanitizer or debugger lifetime evidence rather than many unrelated dumps.
3. The invariant-restoring patch is lifetime equivalence, not merely making the
   global non-configurable.
4. The fixed code can still contain an intentional `base::Unretained(this)` in a
   different async callback when an owned Mojo remote's disconnect semantics
   cancel pending work. Review the guarantee; do not ban the token.
5. This exact root cause and affected lineage are `KILL / DUPLICATE / FIXED`.
   A new candidate needs a distinct owner edge, callback, teardown event,
   configuration, or incomplete patch on a current release.

## Patch and sibling analysis

From the patch, enumerate the fixed invariant rather than copying changed lines:

- Is every independently retainable child a managed wrapper or strong owner?
- Can a bound function escape the wrapper that owns its receiver?
- Are weak callbacks invalidated before native destruction on every sequence?
- Does disconnect actually cancel queued and in-flight callbacks?
- Do navigation, frame deletion, extension unload, and process shutdown share
  the same teardown contract?
- Do alternate provider/feature modes create a different descriptor or object
  graph?
- Do sibling wallet/provider APIs repeat the plain-child/raw-parent pattern?

Matching the old class name or `Unretained` token is not novelty. A surviving
sibling must have its own current release, attacker path, lifetime proof,
sanitizer trace, boundary, and prior-art result.

## Remediation and regression tests

Preferred order:

1. Align native object lifetime with the independently reachable JavaScript
   wrapper using the framework's managed wrapper/ownership mechanism.
2. Use `WeakPtr` or explicit cancellation when the callback must not keep the
   receiver alive.
3. Where strong ownership is intended, make it explicit and cycle-safe.
4. Invalidate all callbacks before context/frame/remote/owner destruction.
5. Add debug assertions and lifetime annotations, but do not treat them as the
   ownership fix.
6. Keep renderer/native interfaces least-privileged so any future memory bug has
   a smaller authority boundary.

Regression coverage must include both historical provider modes, retained child
without parent, retained bound function alone, deletion success/failure, forced
GC in test, natural GC in release-equivalent build, navigation/context teardown,
pending IPC callback teardown, ASan, repeated trials, and the patched negative
control.

## KILL rules

KILL when:

- the asset/class/release is out of scope, archived, test-only, or unshipped;
- the exact root cause is the fixed Brave PR #18411 lineage;
- the property cannot be removed/replaced in the claimed configuration and no
  other owner-loss path exists;
- JavaScript cannot retain the child/function independently;
- the native receiver is strongly owned for the entire callback lifetime;
- `WeakPtr`, context teardown, or remote disconnect reliably cancels invocation;
- the crash lacks a matching free/use stack or disappears under instrumentation
  because it was unrelated;
- the result is only source suspicion, a release crash without root-cause
  evidence, or a sanitizer finding without shipped attacker reachability;
- impact is upgraded from UAF/crash to RCE without a controlled proof.

Only a current, in-scope, non-duplicate, manually reproduced chain may reach
`STRONG`. Otherwise return `MEDIUM`, `WEAK`, `KILL`, or **NO VALID FINDING**.
