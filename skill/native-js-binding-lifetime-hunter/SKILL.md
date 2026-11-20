---
name: native-js-binding-lifetime-hunter
description: "Expert authorized workflow for finding and validating use-after-free and lifetime mismatches across JavaScript-to-native bindings such as V8/Gin, Blink, Electron, Node/N-API, WebView bridges, and renderer APIs. Use when JavaScript objects, proxies, child objects, functions, callbacks, GC, context teardown, base::Unretained, WeakPtr, or native wrappers may disagree about ownership. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Native JavaScript Binding Lifetime Hunter

Audit the ownership boundary where JavaScript reachability controls, or fails to
control, the lifetime of a native receiver. The core invariant is:

> Every JavaScript-reachable callable must have a native receiver that is still
> alive, safely cancelled, or independently owned for the entire callable
> lifetime.

Read `references/native-js-binding-lifetime-uaf-method.md` whenever this skill is
active. Treat the historical Brave `JSEthereumProvider` case as fixed public
prior art, not as a payload recipe or a current finding.

## Evidence-driven routing

Start with `mandatory-auto-router` and `authorized-security-autopilot`. Activate
this skill only when target evidence shows both:

1. JavaScript can retain or invoke a native-backed object, function, proxy,
   child object, or callback; and
2. a distinct GC, context/frame teardown, owner destruction, disconnect,
   navigation, or configuration path may end the native receiver first.

Route alongside:

- `expert-c-cpp-engineer` for ownership, raw pointers, callbacks, sanitizers,
  allocator behavior, and ABI/build configuration;
- `expert-javascript-typescript-engineer` for object graphs, proxies, property
  descriptors, retained closures/functions, realms, navigation, and GC;
- `expert-source-code-bug-hunter` and `secure-code-reviewer` for exact
  source-to-use/free/allocation traces;
- `executable-binary-auditor` and `expert-reverse-engineer` for shipped desktop
  artifacts, crash stacks, symbols, renderer processes, and patch/binary diff;
- `patch-diff-root-cause-analyzer` for prior art, fixed invariants, affected
  releases, uplift branches, and sibling-path review;
- `executable-rce-hunter` only when evidence progresses beyond a crash into a
  controlled corruption primitive or an unrestricted native capability.

Unsupported routes remain `DEFERRED` or `NOT_APPLICABLE`. A lone
`base::Unretained`, raw pointer, `gin::Wrappable`, crash, or GC call is only a
hypothesis.

## Required chain

Build and prove this ledger:

`attacker JavaScript -> binding installation/configuration -> JS object graph -> retained callable/child -> native ownership edge -> owner loss or teardown -> allocation free -> post-free callback -> sanitizer evidence -> process/sandbox boundary -> concrete impact`

Forward tracing from attacker-controlled JavaScript and backward tracing from
the native call must meet on the same shipped configuration. Record exact
source/tag/artifact, platform, feature/provider mode, property descriptor,
object identities, allocation/free/use stacks, baseline, negative control,
patched control, cleanup, and prior art.

## Mandatory distinctions

- JavaScript reachability is not automatically C++ object lifetime.
- A parent wrapper, child object, proxy target, bound function, or closure can
  each have a different lifetime. Retaining one does not prove the others live.
- `delete` must be checked by its return value and the actual property
  descriptor. A non-configurable property invalidates that trigger path.
- V8 GC timing is implementation-dependent. Allocation pressure and a crash ID
  do not prove which allocation was freed or reused.
- `base::Unretained` is not automatically vulnerable. It is acceptable only
  when a documented, enforceable external lifetime or cancellation guarantee
  survives every callback path.
- A renderer crash is not renderer code execution. A renderer compromise is not
  a browser-process compromise or sandbox escape.
- An ASan/HWASan UAF proves memory unsafety at the observed use, but not
  attacker-controlled corruption, exploit reliability, or an RCE boundary.
- Property non-configurability can block one trigger but is not a complete
  ownership fix when another reference, realm, navigation, or configuration can
  retain the callable.

## Workflow

1. **Scope and release:** verify program permission, exact component, current
   release, platform, feature/default setting, allowed local testing, and prior
   art before runtime work.
2. **Binding inventory:** enumerate objects, proxies, accessors, functions,
   native receivers, wrapper types, callback binds, weak pointers, remotes, and
   context/frame observers.
3. **Ownership graph:** model strong, weak, raw, GC-owned, ref-counted, and
   externally guaranteed edges separately.
4. **Destruction matrix:** enumerate GC, explicit delete/overwrite, navigation,
   frame/context loss, disconnect, extension unload, process shutdown, and
   feature-mode transitions.
5. **Reachability proof:** show the attacker can retain and invoke the exact
   child/function after the candidate owner-loss path in a shipped mode.
6. **Safe confirmation:** use an isolated owned profile and instrumented build;
   capture a sanitizer report with allocation, free, and use stacks. Do not
   build heap grooming or code-execution primitives.
7. **Controls:** run normal retained-parent, non-configurable/blocked trigger,
   candidate configuration, and patched-release controls across repeated trials.
8. **Impact:** report only the proven process and security boundary. Keep crash,
   UAF, controlled corruption, renderer execution, and sandbox escape separate.
9. **Sibling and patch review:** test the restored ownership invariant and search
   for distinct callbacks/children/teardown paths without relabeling the public
   root cause as new.
10. **Verdict:** only a current, in-scope, non-duplicate release path with manual
    evidence can survive.

## Safe proof ladder

- **L0 — Signature:** raw callback or mismatched wrapper/child ownership exists.
- **L1 — Lifetime path:** retained JavaScript callable and native owner-loss path
  meet on the same source/release configuration.
- **L2 — Release crash:** the exact shipped artifact crashes repeatably with
  baseline, negative control, property/configuration evidence, and crash stack.
- **L3 — Sanitizer UAF:** ASan/HWASan reports the post-free access with allocation,
  free, and use stacks at the expected binding callback.
- **L4 — Determinism:** repeated candidate trials and a patched control isolate
  the lifetime invariant; stale state and unrelated crashes are excluded.
- **L5 — Corruption primitive:** only if explicitly authorized, a harmless lab
  proof establishes controlled memory corruption beyond the crash.
- **L6 — Boundary impact:** code execution, sandbox escape, or privileged effect
  is claimed only when that exact boundary has a safe controlled proof.

L3-L4 can support a strong UAF finding when release reachability, scope, novelty,
and attacker conditions are proven. They do not upgrade impact to RCE. Only L6
can support the corresponding execution or sandbox claim. Report readiness also
requires `MANUALLY_CONFIRMED`.

## Remediation invariant

Prefer one of these ownership-restoring designs:

- expose every independently retainable JavaScript child as its own managed
  native wrapper whose lifetime follows its JavaScript wrapper;
- make the callable strongly own the receiver when that ownership is intended;
- bind through `WeakPtr` or cancellation when invocation after destruction must
  become a no-op;
- invalidate callbacks during context/frame/navigation/disconnect teardown;
- use an owned remote/receiver only when disconnect semantics demonstrably
  cancel every pending callback before owner destruction.

Regression tests must cover retaining a child/function while losing the parent,
property-descriptor variants, all provider/feature modes, forced GC in an
instrumented test, natural GC in a release-equivalent build, navigation/context
teardown, disconnect/pending callback behavior, and a patched negative control.

## Hard KILL rules

KILL when the exact lineage is public/fixed/duplicate, the release does not ship
the binding, the attacker cannot retain/invoke the callable, the property cannot
be removed or replaced in the claimed mode, native lifetime is enforceably
longer, callbacks are synchronously invalidated, the sanitizer stack does not
match, or only an unrelated crash remains.

The May 2023 Brave `JSEthereumProvider` `_metamask` / `isUnlocked` lineage fixed
by brave-core PR #18411 and commit `a8e497b` is prior art. New work must show a
distinct owner edge, callback, teardown path, configuration, or incomplete fix
on a current in-scope release.

Never turn this skill into exploit development. Do not produce heap grooming,
arbitrary read/write, shellcode, sandbox-escape chains, wallet-key access,
credential theft, persistence, destructive actions, or third-party targeting.

## Required output

| Candidate | Verdict | Release/config | JS retained object | Native receiver | Destruction path | Use/free evidence | Proven impact | Prior art | Manual status |
|---|---|---|---|---|---|---|---|---|---|

For each survivor include the ownership graph, property/configuration matrix,
allocation/free/use stacks, reproduction rate, baseline, negative and patched
controls, exact process boundary, cleanup, missing proof, and hard impact label.
If none survives, return **NO VALID FINDING**.


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
