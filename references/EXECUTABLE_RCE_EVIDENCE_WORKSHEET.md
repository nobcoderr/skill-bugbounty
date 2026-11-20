# Executable / RCE Evidence Worksheet

## Scope and artifact

- Program/owner:
- In-scope product/component/platform:
- Eligible vulnerability class:
- Restrictions:
- Stable/beta/nightly:
- Version/build/architecture:
- Artifact filename and SHA-256:
- Signing/notarization identity:
- Source tag/commit mapping:
- Default configuration/feature flag:

## Runtime boundary

- Process/service/helper:
- User/privilege/integrity/sandbox:
- Parent/child process tree:
- IPC/listener/plugin/update boundary:
- Victim interaction required:

## Candidate

- Title:
- RCE lane: command / write-load / updater / IPC / deserialize / memory / renderer bridge / parser-desync / state-poison / dynamic-resolver / sandbox-context / filesystem-semantic / protocol-handler / other
- Modern RCE pattern family / public prior-art family:
- Attacker capability:
- Attacker-controlled input/field:
- Container/encoding/transport:
- Component interpretation map:
- Representation validated:
- Representation ultimately used/executed/loaded/cached/written:
- Identity-changing transformations:
- Parser/canonicalization result:
- Validation/auth/signature/invariant:
- Missing check:
- Exact call/data-flow chain:
- Intermediate primitive:
- Confirmed automatic gadget/consumer:
- Sensitive sink:
- Execution/control primitive:
- Security boundary crossed:
- Concrete impact:

## Proof

- Evidence level R0-R5:
- Modern-chain evidence level C0-C6:
- Safe canary/control primitive:
- Negative control:
- Logs/debugger/sanitizer/IPC/filesystem/process evidence:
- Reproduction rate:
- Runtime/mitigation matrix (OS/filesystem/runtime/loader/module mode/allocator/worker model/privilege/feature flags):
- Mitigations/hardening observed:
- Cleanup performed:

## Triage

- Scope confidence:
- Release reachability confidence:
- Primitive confidence:
- Impact confidence:
- Public/known/fixed/duplicate search:
- Invalidation factors tested:
- Evidence still missing:
- Verdict: STRONG / MEDIUM / WEAK / KILL
- Candidate validity: VALID / INVALID / BLOCKED

## Fix

- Minimal invariant-restoring fix:
- Regression test:
- Sibling paths requiring review:
- Patch-variant matrix completed:
