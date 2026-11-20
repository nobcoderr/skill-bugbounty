---
name: program-impact-boundary-gate
description: "Always-active program-impact and capability-delta gate for authorized bug-bounty work. Starts through the mandatory auto-router; rejects by-design, equal-authority, consented-trust, environmental-mismatch, non-production, excluded, duplicate, severity-ineligible, or impact-unproven candidates before reporting while preserving unresolved and procedurally closed cases as BLOCKED. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Program Impact Boundary Gate

Use this skill for every authorized bug-bounty candidate. Technical correctness
is necessary but not sufficient: the candidate must create a concrete capability
the attacker did not already possess across a boundary the current program
recognizes and rewards.

Load:

- `references/PROGRAM_IMPACT_BOUNDARY_GATE.md`
- `prompts/MASTER_PROMPT_PROGRAM_IMPACT_BOUNDARY_GATE.md`
- `config/PROGRAM_IMPACT_NEGATIVE_CONTROL_CASES.json`
- `config/PROGRAM_IMPACT_POSITIVE_CONTROL_CASES.json`

The user-supplied Informative and Not Applicable decisions in the reference are negative controls,
not universal vendor policy and not a reason to suppress novel research. Use
them to form falsifiers. Kill a new candidate only after target-specific evidence
proves the same trust, authority, ownership, equivalence, configuration, or
program-severity condition.

The 2026-09 additions require separate checks for: technically valid duplicates;
program-excluded execution inside an untrusted-code updater sandbox; SDK
identities explicitly marked unverified; plaintext proxy threat models;
application-controlled library or descriptor lifecycles; and niche build
configurations without a shipped consumer. These are independent gates. Do not
use any one of them as a generic excuse to suppress a target-specific exploit
that proves a different protected boundary.

Also separate field-level configuration changes from the authority of the
approved domain. Renewed approval of an MCP or project configuration does not
create authorization-server binding when the trusted workspace already has
equivalent hooks, settings, or execution authority, unless the product promises
that narrower isolation. For build-system candidates, compare metadata influence
with the package's complete authority at that stage. A crate already executing a
build script has no new capability merely because transitive metadata can replace
direct-dependency metadata; require a lower-trust metadata-only source or an
effect unavailable to existing build-time code execution.

The positive-control corpus shows what should survive the gate: limited
starting authority, attacker-controlled data crossing into a real higher-
authority consumer, an in-scope protected effect, shipped reachability,
authoritative read-back, and controls proving the result is unavailable through
ordinary permissions. Trace one admitted representation to every downstream
consumer; a single unsafe metadata write can support distinct valid findings
when it reaches independent sinks with materially different effects and fixes.
Exact public/fixed roots remain `KILL_KNOWN_OR_DUPLICATE` for new submissions.

## Provisional severity and bounded escalation

The first supported Low, Medium, or High impact is a provisional floor. Load
`references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md`, recompute attacker state,
and inspect only protected consumers newly reachable through the demonstrated
capability delta. A higher label requires a proven edge, continuity, current
release reachability, authoritative protected-effect read-back, and a new pass
through this impact gate.

Lock only the maximum demonstrated program severity after terminal impact is
proven, every realistic expansion edge is falsified, or an explicit program,
scope, safety, or environment ceiling prevents further proof. A blocked edge
may explain remaining uncertainty but cannot raise severity.

## Mandatory two-pass gate

Run the gate twice:

1. **Early impact preflight** — before expensive PoC work, establish the current
   program severity floor, production-versus-demo asset status, starting
   authority, trusted/consented domain, defended threat model, protected asset,
   intended security promise, current production reachability, prior-art status,
   realistic exploit conditions, plausible capability delta, adjudication basis,
   report readiness, submission-time reachability, production stack equivalence,
   exact ordinary comparison path, and canonical consensus requirements.
2. **Pre-report impact adjudication** — after technical reproduction, prove the
   real unauthorized recipient/action, actual post-condition, authoritative
   read-back, current scope/severity eligibility, and absence of an equivalent
   intended path.

## Required capability-delta model

Record:

`starting capability -> exploit transition -> resulting capability`

Then answer:

- What exact action, data, identity, secret, resource, or trust decision was
  unavailable before exploitation?
- Which documented or architecture-supported boundary forbids it?
- What exact property is promised: confidentiality, integrity, authenticity,
  authorization, availability, revocation, isolation, or only reconstruction,
  routing, presentation, and compatibility?
- Does the attacker, repository, provider, organization role, project member,
  model, or OAuth principal already have an equivalent supported path?
- Did the user explicitly trust the repository/provider/workspace/configuration
  domain that supplies the input?
- Is the asset a production product, or a documented demo, sample, quickstart,
  local-development server, self-hosted worker, or development preview with a
  lower program impact ceiling?
- Does the claimed protection belong to the feature's defended threat model, or
  is it only defense-in-depth hygiene beneath unrestricted same-UID/local-user
  authority?
- Was the historical status caused by a merits decision, environmental mismatch,
  explicit exclusion, intended behavior, prior knowledge, or procedural
  inactivity? A status label alone is not security evidence.
- Does the PoC include every production middleware, file-serving, cache, browser,
  proxy, and consensus layer that can alter the result?
- For a distributed system, is the effect canonically included and final on
  independently validating nodes, or only accepted by one local harness?
- Does the negative control use the exact closest supported path, including the
  same URL and top-level navigation for browser redirect claims?
- Is the behavior default/reachable, or dependent on DEBUG, operator opt-in,
  nonstandard trust policy, or an unproven downstream consumer?
- Is the exact component deployed on a current eligible production system, or
  only present in an archived/unmaintained repository or local harness?
- For a race or environment-dependent chain, can the attacker create the timing,
  topology, and prerequisite state reliably without curator-only locks, uncommon
  host policy, pre-added resources, or administrator setup?
- Does the user explicitly opt into an active-content, rendering, unsafe-project,
  or other mode whose documented purpose includes the disputed behavior?
- If exploitation depends on collision or guessing, what information must the
  attacker know, what is its entropy, how long does state persist, how frequent
  is the victim event, and what measured success rate is realistic?
- Does the proposed mitigation actually remove attacker capability under the
  same threat model, or can the attacker bypass the counterfactual by controlling
  the trust root, key, source, or equivalent input channel?
- Does a permission govern the control plane, data plane, or both? Is the
  claimed protected operation inside the documented scope of that permission?
- Does a credential proof establish current validity, lifetime, principal,
  effective permissions, protected recipient, and concrete protected action?
- When was the disputed authority issued? Does the later denylist, revocation,
  profile change, or snapshot change explicitly invalidate already-issued or
  in-flight authority?
- If a secondary credential is obtained, was it already available during the
  parent credential's valid lifetime, and what exact event revokes each token?
- Are the before and after snapshots controlled by different principals or
  merely different versions of input from the same trust class?
- Does the primitive reach a real protected consumer: successful authentication,
  security-critical file/state, observable protected memory, enforced routing
  policy, or deployed generated code?
- Is the demonstrated impact high enough for the program's current written
  eligibility threshold?

## Fail-closed verdicts

- `IMPACT_GATE_PASS` — nonzero capability delta across a recognized boundary is
  proven and the impact meets current program eligibility.
- `IMPACT_GATE_BLOCKED` — a potentially meaningful delta exists, but one or more
  decisive facts are unavailable. Do not submit or inflate.
- `INFORMATIVE_LIKELY` — the mechanism is real but current evidence shows no
  material program-recognized security impact.
- `KILL_NO_CAPABILITY_DELTA` — post-exploit authority is equivalent to the
  attacker's intended starting authority.
- `KILL_TRUSTED_DOMAIN` — the effect stays inside an explicitly trusted or
  consented repository/provider/workspace/organization boundary.
- `KILL_BY_DESIGN` — documented behavior and security model preserve the claimed
  boundary.
- `KILL_NON_PRODUCTION_TARGET` — the best proven effect is confined to a
  documented demo, sample, quickstart, local-development, or development-preview
  context the current program does not accept at the required impact level.
- `KILL_THREAT_MODEL` — exploitation relies on authority explicitly assigned to
  the same local user/operator, self-hosted environment, unrestricted process,
  or other actor the feature does not promise to resist.
- `KILL_KNOWN_OR_DUPLICATE` — the same root cause was public, previously known,
  already reported, or under remediation before submission. Preserve technical
  validity separately from bounty eligibility.
- `KILL_NO_PRODUCTION_REACHABILITY` — the source behavior is reproduced, but the
  exact component is archived, unmaintained, source-only, or not shown on a
  current eligible production system when the program requires live deployment.
- `KILL_PROGRAM_SEVERITY` — the best supported impact is below the current
  program severity floor or excluded class.
- `KILL_ENVIRONMENT_MISMATCH` — the proof omits a production layer or replaces
  consensus/deployment behavior such that the effect is not demonstrated on the
  real eligible environment.

Only `IMPACT_GATE_PASS` may proceed toward `STRONG`. It still requires all
normal scope, reachability, evidence, prior-art, safety, negative-control, and
manual-confirmation gates.

## Hard rules

- A localhost or synthetic-token PoC proves mechanism, not realistic privilege
  separation or platform impact.
- A Not Applicable closure caused by procedural inactivity is not a technical
  rejection. Preserve it as `IMPACT_GATE_BLOCKED` and fix report readiness,
  reviewer format, requested evidence, and response deadlines.
- Production stack equivalence is mandatory when middleware, hosting, file
  delivery, browser permissions, redirects, or consensus can change the result.
- One node's `accepted=true`, especially with consensus stubs, is not canonical
  consensus, fund movement, or finality.
- For browser network-delta claims, test the exact same-URL top-level navigation
  and redirect path, not only fetch and subresource primitives.
- Preserve dated submission-time production evidence when a target is patched
  later; a later local pre-fix replay cannot replace that evidence.
- Apply a privacy promise only to the exact bytes, fields, metadata, filenames,
  or pages it covers.
- A complete exploit chain can still be non-eligible when its strongest effect
  ends inside a documented demo, quickstart, local-development server, or
  development-preview context and the program requires production impact.
- Distinguish a security guarantee from defense-in-depth hygiene. Environment
  scrubbing, header redaction, path convenience, or best-effort filtering does
  not create process, host, or credential isolation when unrestricted same-user
  execution is explicitly part of the model.
- A local user deliberately rewriting their own downstream resolver or a
  self-hosted operator supplying the workdir is not an attacker-victim split
  unless the product expressly defends that boundary.
- A patched control proves behavioral difference, not bounty eligibility.
- A local/unit/in-memory reproduction against an old repository does not prove
  a current eligible deployment. When the program requires a live production
  system, source validity alone is `KILL_NO_PRODUCTION_REACHABILITY`.
- A deterministic lab lock proves a race mechanism, not attacker-controlled
  exploitability. Require an unprivileged trigger, measured window and success
  rate, realistic concurrency, and the actual supported revocation operation.
- Explicit selection of an active renderer or disabling a warning/control can
  place attacker content inside a consented execution domain. Prove execution
  under the safe/default path or violation of a documented isolation promise.
- Forwarding-header trust belongs to the deployed proxy topology. Do not call a
  spoofable header a product bypass until the supported topology, trusted edge,
  overwrite behavior, and product-owned trust invariant are established.
- Token presence is not impact without effective authority and a protected
  action unavailable to the attacker before exploitation.
- Signing proves integrity/authenticity of a payload; it does not imply secrecy.
  Do not report readable or replayable signed state when reconstruction is the
  documented purpose and the primitive is not a confidentiality boundary.
- A documentation word such as "encrypt" can be inaccurate without making all
  encoded values secrets. Prove the normative API contract and a protected
  first-party value before promoting the mismatch.
- Persistence after credential revocation is not a boundary break when the
  persistent object belongs to the same authorized user and cleanup inheritance
  was never promised.
- Cryptographic, parser, routing, scope, or lifecycle inconsistencies remain
  correctness findings until a real protected consumer and concrete security
  effect are proven.
- A parser or resolver mismatch has zero security delta when an equivalent
  supported declaration grants the same fetch/selection capability, or when all
  resulting artifacts remain within the configured and locked trust set.
- Build-time schemas, descriptors, manifests, and generated-code inputs may be
  one trusted build-input class. A code-generation injection is zero delta when
  the same contributor already controls an equivalent executable build input,
  unless the product expressly promises a non-executable schema boundary.
- Authorization-server binding must be a defended product property, not inferred
  solely from the fact that a stored OAuth credential was originally issued by
  one server. When a user reapproves changed configuration in a trusted workspace,
  prove that the workspace lacks equivalent credential-forwarding or execution
  authority before retaining the recipient change.
- Dependency metadata authority must be compared with existing build-time code
  execution. If the same malicious package is already resolved and its build
  script runs, metadata overwrite or source injection is zero delta unless it
  reaches a separately protected consumer beyond that execution context.
- A configured package source, mirror, registry, or update service can be a
  trust anchor. Do not treat hostile responses as a boundary crossing until the
  actor gains a capability beyond ordinary trusted-source inputs.
- A mitigated counterfactual is evidence only if it removes authority from the
  same attacker. Signature enforcement is not protective when the stated
  attacker can replace both package bytes and the trusted signing key.
- Missing user/session binding in temporary state remains `IMPACT_GATE_BLOCKED`
  when exploitation requires a rare incomplete object plus exact unknown name,
  extension, identifier, and timing. Quantify predictability and prevalence.
- A parser differential is zero delta when the attacker can send a well-formed
  request that produces the same handler-visible state and protected effect.
- A permission enforced at the final data plane does not automatically prohibit
  connectivity, discovery, negotiation, health-check, or traversal control-plane
  traffic. Prove the permission's documented scope and a denied final capability.
- A denylist or revocation can be forward-looking. Authority validly signed or
  attested before the event remains by design unless retroactive invalidation is
  promised; evaluate settlement correctness and intended exit paths.
- A derived token is not automatically a new capability when the same actor
  could retrieve it while the parent token was valid. Prove credential lineage,
  independent lifetime, and the exact cross-token revocation contract.
- Do not require symmetric signature fields across distinct operations. Derive
  each authorization scope from its typehash, signed statement, documentation,
  and resulting value/state bounds.
- Temporal snapshot drift is zero delta when both states contain attacker input
  from the same principal and the consuming token already covers both. Require
  a changed trust class or unique protected sink.
- A password-derived header sent to the wrong peer is a security hypothesis,
  not proven credential compromise, until the protected peer accepts it or a
  real oracle/replay capability is demonstrated.
- A file truncation, uninitialized read, socket-routing mismatch, or generated
  example difference is only a primitive. Require a shipped protected consumer
  and concrete confidentiality, integrity, authorization, or availability effect.
- A role change, password change, client deletion, logout-all action, and
  credential revocation are distinct lifecycle events. Prove which event is
  documented to invalidate which credential, session, cached authorization, or
  user-owned persistent object before claiming revocation bypass.
- A sibling password-confirmation or second-factor prompt can be defense in
  depth rather than a separately rewarded boundary for a fully authenticated
  session. Require program or product evidence that session hijack resistance is
  a defended credential-management invariant.
- Layered validation APIs may intentionally keep nested failures separate from
  top-level summaries. Prove the summary contract and a protected default
  consumer that makes an unauthorized acceptance decision.
- Prior art is independent of technical impact: a valid vulnerability that was
  already known or under remediation is still `KILL_KNOWN_OR_DUPLICATE` for a
  new submission.
- Do not call a candidate false positive merely because it is non-target or
  runtime-blocked. Use `IMPACT_GATE_BLOCKED` with exact missing evidence.
- Do not rescue a failed impact gate by describing hypothetical cloud exchange,
  downstream trust, victim configuration, or sensitive data without evidence.
- Do not stop at the first consumer of attacker-controlled stored metadata.
  Inventory every later filesystem, renderer, URL, backup, export, deletion,
  and privileged-browser consumer, then prove each terminal effect separately.
- A low-privilege actor operating only on an owned object can still cross a
  security boundary when a later privileged consumer turns that object's data
  into arbitrary filesystem effects or higher-privilege script execution.
- Preserve direct proof separately from conventional post-exploitation. A safe
  arbitrary-file canary or inert privileged-browser DOM canary can establish a
  strong capability delta without deleting real configuration, creating users,
  installing code, or stealing credentials.

## Required output

- Program and current severity floor:
- Asset maturity and program impact ceiling:
- Candidate:
- Starting authority:
- Trusted/consented domain:
- Defended threat model:
- Protected asset/action:
- Intended security promise:
- Promised security property and control-plane/data-plane scope:
- Security guarantee or defense-in-depth hygiene:
- Equivalent intended path:
- Counterfactual mitigation and residual attacker capability:
- Default/opt-in conditions:
- Resulting authority:
- Capability delta:
- Unauthorized recipient or principal:
- Concrete protected effect:
- Credential authority/lifetime, if applicable:
- Authorization issuance time and retroactive-policy contract:
- Parent/derived credential lineage and independent revocation:
- Temporal snapshot principals and trust equivalence:
- Primitive-to-protected-consumer bridge:
- Evidence and authoritative read-back:
- Production/release deployment evidence:
- Attacker-controlled timing/topology and measured reliability:
- Collision knowledge, entropy, persistence, prevalence, and success rate:
- Missing proof:
- Adjudication status and closure basis:
- Submission-time reachability and later patch timing:
- Production stack equivalence:
- Canonical consensus/finality, if applicable:
- Exact equivalent-path/top-level-navigation control:
- Report readiness and response deadline:
- Prior-art/known/duplicate status:
- Informative negative-control match:
- Gate verdict:
- Single highest-value unblocking test:
- Severity status: PROVISIONAL / ESCALATION_ACTIVE / LOCKED
- Escalation edges proven, falsified, and blocked:
- Maximum proven severity and lock reason:
- Vulnerability validity: VALID / INVALID / BLOCKED
- Triager-proof gate: PASS / FAIL / BLOCKED
- Report ready: YES / NO, with exact blockers

If no candidate passes, return `NO VALID FINDING`.


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

This skill is always active for security-focused work. It uses the current
`mandatory-auto-router` session, loads its mapped companions, reruns after a
material program-policy or trust-boundary change, and never authorizes live or
state-changing testing. If the router is already active, do not recursively
bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
