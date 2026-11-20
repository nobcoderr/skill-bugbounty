# Meta GraphRAG Primitive-to-Cloud Chain Method

## Purpose and prior-art status

Use this method when a web or AI service exposes a client-side credential, a
file-ingestion surface, path-derived storage, Python loading/deserialization,
and a cloud workload identity. It distills the evidence shape from Zondou's
public May 2026 Meta GraphRAG report.

The reported Meta path is public prior art. Its hostname, key, endpoint names,
traversal layout, pickle consumer, and cloud escalation are not novel leads and
do not authorize testing Meta or any other deployment. Reconstruct every
candidate from the current target's own code and runtime evidence.

## Chain model

Maintain both an attacker-state ledger and a representation ledger:

```text
public client artifact
  -> credential accepted by API
  -> authenticated dataset/file capability
  -> path normalization escape
  -> controlled file at a security-relevant location
  -> shipped loader/deserializer consumes that exact file
  -> process execution
  -> workload identity reachable from that process
  -> program-authorized protected cloud action
```

No arrow is implied. Each edge needs its own baseline, positive case, negative
control, runtime continuity, and authoritative read-back.

## Procedure

### 1. Treat a leaked key as a capability, not a severity label

Record:

- where the value is shipped and who can obtain it;
- the principal/project/environment it represents;
- accepted endpoints, methods, and data classes;
- expiry, restrictions, and whether anonymous users gain anything new;
- the closest intended public or low-privilege path.

A public key with no additional authority is not a finding. A key that grants
read, write, delete, upload, or administrative actions creates a scoped
post-state that may unlock the next surface.

### 2. Build a post-auth capability matrix

Use researcher-owned records and harmless canaries only:

| Capability | Baseline without key | With key | Protected effect |
|---|---|---|---|
| enumerate | rejected/limited | observed | existence or metadata |
| read | rejected | canary read | confidentiality |
| create/update | rejected | canary mutation | integrity |
| delete | do not test unless expressly allowed | n/a | destructive; normally stop |
| upload | rejected | benign file accepted | bridge candidate |

Do not access victim datasets merely to prove that listing exists.

### 3. Prove path escape as a one-variable differential

For an upload path assembled from a project/dataset root plus a fixed
subdirectory and client filename, record all three representations:

```text
raw filename -> joined path -> canonical opened path
```

Use a disposable local harness or expressly authorized researcher-owned target.
Compare a safe sibling filename with one path-changing input. A response that
echoes `../` is not proof; verify the canonical destination using a harmless
marker read-back. Check filename and root/dataset selectors independently.

### 4. Do not equate arbitrary file write with RCE

Inventory shipped consumers of writable locations:

- import/module search paths;
- templates, plugins, startup files, jobs, and configuration;
- archive or model loaders;
- pickle, marshal, YAML object, or other executable deserializers;
- scheduled, restart, visualization, export, or conversion paths.

The bridge exists only when the real service loads the exact attacker-written
object under the same deployment identity and state. A writable source file
that nothing imports remains a file-write primitive.

### 5. Bind selector traversal to the unsafe consumer

When a dataset/project parameter chooses the directory later read by a loader,
trace:

```text
request selector
  -> normalization/allowlist
  -> resolved directory
  -> fixed loader filename
  -> parser/deserializer
  -> side effect
```

Test the safe dataset baseline, a nonexistent sibling, a traversal attempt, and
a patched canonical-root control. For Python, also account for import caching
when reproducing locally; stale module state must not masquerade as a second
successful run.

### 6. Prove blind execution without collecting secrets

An HTTP 500 after deserialization is not RCE evidence. Prefer, in order:

1. a local file canary readable through the researcher-owned harness;
2. a loopback callback controlled by the researcher;
3. a single scoped callback to researcher-owned infrastructure when the
   program expressly permits out-of-band proof.

Capture the exact trigger, process identity, timestamp, unique nonce, and
negative control. Do not enumerate environment variables, cloud credentials,
secret stores, customer data, or unrelated services as routine proof.

### 7. Escalate cloud authority with explicit permission gates

After process execution, identify potential authority surfaces from deployment
manifests and documentation before touching them:

```text
process identity -> workload identity -> policy -> protected cloud operation
```

Use provider identity inspection or a synthetic canary when allowed. Prove the
least harmful protected read/write that distinguishes the role from the
attacker's starting authority. Secret enumeration, credential replay, lateral
movement, and cross-cloud access require explicit program authorization; stop
and report when policy or the vendor asks testing to cease.

### 8. Apply environment and severity gates

Classify production, staging, development, demo, and event-only assets before
severity claims. Development root access does not automatically equal
production compromise. Severity is the maximum demonstrated, eligible impact
after capability continuity is proven, not the most sensitive hypothetical
secret that might exist.

## Evidence matrix

```text
CLIENT_CREDENTIAL_PUBLIC          = PASS / FAIL
ANONYMOUS_TO_API_AUTHORITY_DELTA  = PASS / FAIL
CANONICAL_FILE_ESCAPE             = PASS / FAIL
SHIPPED_EXECUTION_CONSUMER        = PASS / FAIL
BLIND_EXECUTION_ORACLE            = PASS / FAIL
SAME_RUNTIME_CONTINUITY           = PASS / FAIL
WORKLOAD_IDENTITY_REACHABLE       = PASS / BLOCKED / NOT_TESTED
PROTECTED_CLOUD_EFFECT            = PASS / BLOCKED / NOT_TESTED
CURRENT_SCOPE_AND_ENVIRONMENT     = PASS / FAIL
PUBLIC_EXACT_ROOT_PRIOR_ART       = FOUND / NOT_FOUND
IMPACT_GATE                       = PASS / BLOCKED / KILL
```

## Falsifiers and kill conditions

- The key grants no capability beyond the documented public client.
- The canonical path remains inside the intended upload root.
- The written file is never consumed by a shipped authority-bearing component.
- The loader uses a safe format or authenticates the object before loading.
- The trigger changes identity, host, container, or release without a proven
  bridge.
- Only a crash/500 occurs and no execution oracle exists.
- Cloud authority is inferred from environment names rather than an allowed
  protected action.
- The effect is confined to an ineligible development/demo environment.
- The exact root is public, fixed, known, or already under remediation.

## Source

- Zondou, "Root RCE and full cloud takeover on a Meta service," May 8, 2026:
  https://zonduu.me/posts/meta-graphrag-rce/

