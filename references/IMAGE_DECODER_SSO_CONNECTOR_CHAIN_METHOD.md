# Image Decoder to SSO and Connected-Integration Chain Method

<!-- IMAGE_DECODER_SSO_CONNECTOR_CHAIN:v1 -->

Use this method only for explicitly authorized research where target evidence
shows an untrusted image or media upload reaching a native decoder and a
plausible identity or connected-integration boundary. It is a chain-research
method, not a payload library and not authorization to reproduce a public
incident.

## Research invariant

Keep these boundaries separate:

`untrusted media -> format dispatch -> native decoder -> process authority -> application authority -> SSO/session authority -> connected integration -> protected action`

Each arrow is an independent claim. A decoder crash does not prove code
execution. Code execution in an image worker does not prove application or SSO
authority. A compromised relying party does not prove an identity-provider
session. Account access does not prove a connector can reach a protected
resource. Severity may inherit only edges demonstrated on one continuous,
authorized path.

## Activation evidence

Activate this method when at least two of the following are established:

- HEIC, HEIF, AVIF, or another attacker-controlled media format is accepted;
- application dispatch invokes ImageMagick, libheif, libde265, or another
  native parser/decoder;
- the exact container, package, SBOM, or binary revision can be identified;
- the processing service has a meaningful sandbox, filesystem, network, secret,
  session, or application trust boundary;
- the application participates in SSO, identity federation, account linking,
  or session brokering;
- the resulting account has an explicitly scoped connector or integration.

A public article title, vendor name, or generic `image upload` keyword alone is
insufficient.

## Required ledgers

### 1. Artifact and patch ledger

Record:

- application and image-processing release;
- container image digest and base distribution;
- package name, version, build identifier, architecture, allocator, and hardening;
- upstream commit ancestry and downstream backports;
- the exact vulnerable function, faulting operation, and primitive;
- patched, closest-safe, and malformed-but-non-triggering controls.

Version strings alone are not proof. A distribution may backport a fix without
changing the upstream version, or carry the same visible version with a
different patch set. Prefer binary/package provenance, source package revision,
symbols, reproducer behavior, and vendor advisory evidence.

### 2. Representation ledger

Trace exact bytes and object identity through:

`upload validation -> MIME/extension detection -> format-specific dispatch -> conversion wrapper -> decoder entrypoint -> decoded object -> application consumer`

Record which component checks the object and which component consumes it.
Prove whether HEIF-family input bypasses an ordinary image checker and reaches a
different native path. Do not infer reachability from installed dependencies.

### 3. Primitive ledger

Classify only observed behavior:

- deterministic rejection;
- crash or availability effect;
- sanitizer-confirmed out-of-bounds read/write;
- information disclosure;
- controlled memory primitive;
- controlled in-process execution;
- process-level code execution.

For native memory research, prefer a local exact-revision build, sanitizers,
debugger instrumentation, synthetic images, and a harmless in-process canary.
Do not deploy a shell, persistence, credential collector, or stealth mechanism.

### 4. Process-authority ledger

After a primitive is validated, enumerate what the decoder process can actually
reach:

- UID/GID, namespaces, seccomp/AppArmor/SELinux profile, chroot/container;
- mounted paths and writable directories;
- environment variables and injected secrets;
- loopback/private network and service identities;
- application queues, databases, session stores, and control sockets;
- token/cookie signing or encryption material;
- sandbox lifetime, isolation, and cleanup.

`RCE in worker` is a post-state, not automatically server compromise. If the
sandbox prevents a new protected capability, retain the process primitive at
its observed impact and stop the higher chain.

### 5. Identity and SSO ledger

Model the application/relying party and identity provider independently:

- issuer, audience, client, redirect URI, subject, tenant, nonce, state, PKCE;
- login initiation, callback, account-linking, session minting, and logout;
- cookies/tokens available to the compromised application;
- whether relying-party compromise can mint, substitute, replay, or port a
  session into a different first-party service;
- whether employee status or group membership is server-derived and rechecked;
- session revocation and credential lineage.

Use researcher-owned A/B identities and synthetic tenants only. Application
administration, database access, or cookie-signing material is not an SSO
takeover until a controlled account transition proves the exact identity
boundary.

### 6. Connected-integration ledger

For each connector, record:

- whether it is present for the controlled account;
- issuing principal, OAuth client, scopes, installation, organization, and
  resource allowlist;
- user confirmation or server-side authorization gates;
- token storage and whether account/session authority can invoke it;
- the least harmful protected action and authoritative read-back;
- revocation, cleanup, and residual artifacts.

Prove the connector boundary with a researcher-owned sandbox resource and a
reversible canary. Never access a third party's repository, messages, files, or
credentials. A connected GitHub, Slack, email, or code-agent UI does not imply
the integration can reach internal resources.

## Attacker-state transitions

Maintain explicit states:

| State | Required proof | Newly available capability |
|---|---|---|
| `S0_UPLOAD` | accepted owned media input | reach upload pipeline |
| `S1_NATIVE_REACH` | exact decoder call path | reach native parser |
| `S2_MEMORY_PRIMITIVE` | local runtime evidence | scoped memory effect |
| `S3_PROCESS_EXECUTION` | harmless in-process control-flow canary | execute in decoder process |
| `S4_APPLICATION_AUTHORITY` | protected application action/read-back | application-level authority |
| `S5_IDENTITY_AUTHORITY` | owned A/B session transition | SSO/account authority |
| `S6_CONNECTOR_AUTHORITY` | owned connector canary | scoped integration authority |
| `S7_TERMINAL_IMPACT` | reversible protected action | maximum demonstrated impact |

If a stage creates no measurable capability delta, return
`KILL_NO_CAPABILITY_DELTA`. Search the next stage only among surfaces whose
prerequisites are satisfied by the demonstrated post-state.

## Exact-root and attribution discipline

Keep separate attribution records for:

1. upstream native library root cause;
2. distribution or backport status;
3. container/artifact packaging;
4. application's format dispatch and sandbox;
5. SSO or identity configuration;
6. connected-integration authorization.

The public Hacktron account states that an upstream change was not documented
as a security fix or CVE at discovery time. The Discourse advisory associates
its image-upload RCE lineage with CVE-2026-32882. Do not declare those labels
identical unless the fixing commit, vulnerable function, crashing input class,
and primitive match. Record `EXACT_ROOT_IDENTITY=PROVEN|UNRESOLVED|DIFFERENT`.

Public roots are prior art and duplicate-burn entries. A current candidate must
show a distinct unpatched artifact, incomplete backport, variant operation
domain, different protected consumer, or incomplete downstream fix.

## Safe validation ladder

1. Map official scope, exact asset, allowed upload/testing mode, limits, and
   stop conditions.
2. Resolve exact artifact provenance using SBOM, package metadata, image digest,
   and source/binary correspondence.
3. Reproduce only in a local exact-revision harness with sanitizers and a
   non-sensitive synthetic image.
4. Establish the minimum memory primitive and a harmless in-process canary;
   do not create a remote shell.
5. Enumerate sandbox/process authority read-only and compare with a patched
   control.
6. Validate application and SSO edges with researcher-owned A/B accounts and
   reversible state.
7. Validate any connector only against an owned sandbox repository or resource,
   using the minimum reversible action.
8. Stop immediately when impact is sufficient, unexpected real data appears,
   a vendor requests cessation, or any edge leaves scope.

Never disguise a live target as a CTF, conceal target identity from an agent,
mask safety signals, or use a proxy to induce a model to perform work it would
otherwise refuse. Authorization must be represented truthfully to every human,
agent, harness, and adapter involved.

## Required controls

For every edge, require:

- baseline with a well-formed safe image or ordinary login/action;
- one-variable positive case;
- malformed/non-triggering sibling;
- patched or backported artifact control where available;
- authoritative before/after read-back;
- repeated trials for nondeterministic allocator or deployment behavior;
- cleanup and evidence identity.

## Falsifiers and KILL codes

- `KILL_FORMAT_NOT_REACHABLE`: target does not accept or decode the format.
- `KILL_PATCH_PRESENT`: exact artifact contains the relevant fix/backport.
- `KILL_NO_RELEASE_REACHABILITY`: only a lab/source build is affected.
- `KILL_CRASH_ONLY`: no capability beyond a bounded local crash is proven.
- `KILL_SANDBOX_CONTAINS_CAPABILITY`: process compromise creates no protected
  post-state needed by the next edge.
- `KILL_SSO_BINDING_CORRECT`: issuer/audience/client/session/subject binding
  prevents the claimed transition.
- `KILL_CONNECTOR_ABSENT_OR_SCOPED`: no integration exists or scopes block the
  protected action.
- `KILL_CONTINUITY_BROKEN`: identity, environment, privilege, or state changes
  without a proven bridge.
- `KILL_KNOWN_OR_DUPLICATE`: exact public/fixed root or chain is reused.
- `KILL_SCOPE_BRIDGE`: the next service, account, or connector is outside the
  authorized program.

## Severity and report gate

Keep every Low, Medium, or High label provisional while a proven capability
unlocks an in-scope higher boundary. Raise severity only after the higher edge
and its protected effect are observed. Lock severity at the maximum demonstrated
impact after all realistic, capability-continuous expansions are proven,
falsified, or blocked by scope/safety/environment.

`STRONG + MANUALLY_CONFIRMED` establishes vulnerability validity. Set
`REPORT_READY=YES` only after `TRIAGER_PROOF=PASS`, including exact artifact and
patch provenance, edge-by-edge controls, owned-account proof, current-release
reachability, root-cause attribution, prior-art result, cleanup, reproducibility,
and an objection matrix.

## Public methodology seeds

- Hacktron, *Hacking OpenAI*: https://www.hacktron.ai/blog/hacking-openai
- Discourse advisory GHSA-vhm9-85gw-x335:
  https://github.com/discourse/discourse/security/advisories/GHSA-vhm9-85gw-x335
- Debian DSA-6417-1: https://security-tracker.debian.org/tracker/DSA-6417-1
- libheif releases: https://github.com/strukturag/libheif/releases
- libheif security policy: https://github.com/strukturag/libheif/security

These sources supply prior art, patch lineage, and evidence-shape lessons only.
They do not authorize testing OpenAI, Discourse, Debian, libheif deployments, or
any third-party service.
