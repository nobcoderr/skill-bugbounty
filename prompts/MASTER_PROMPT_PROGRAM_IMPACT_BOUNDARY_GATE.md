# Master Prompt — Program Impact Boundary Gate

Apply this gate to every authorized bug-bounty candidate before expensive proof
work and again before report-ready classification.

Technical behavior is not enough. Determine whether exploitation grants a
concrete capability the attacker did not already possess across a boundary the
current program recognizes and rewards.

For each candidate, produce a target-specific impact card:

- current official program scope, exclusions, severity floor, and desired
  security effects;
- asset maturity and program impact ceiling: production product versus demo,
  sample, quickstart, local-development server, self-hosted component, or
  development preview;
- exact current production/release deployment evidence, especially for archived,
  old, or unmaintained source components;
- attacker starting role, privileges, ownership, resource access, and trusted or
  consented domains;
- defended threat model, including whether the same local user/operator controls
  the downstream resolver, workdir, UID/PID namespace, or unrestricted process;
- exact victim action, default/opt-in server conditions, and feature state;
- intended security promise supported by documentation, architecture, policy,
  UI trust language, or enforced controls;
- exact promised security property: confidentiality, integrity, authenticity,
  authorization, isolation, revocation, availability, or non-security
  presentation/reconstruction behavior; do not infer confidentiality from a
  signature or integrity check;
- when permissions are involved, whether they govern the control plane,
  discovery/connectivity plane, or final data plane, and which protected action
  is actually denied;
- whether the observed mitigation is a security guarantee or only documented
  behavior, convenience redaction, or defense-in-depth hygiene;
- exact protected asset/action and unauthorized recipient/principal;
- equivalent supported paths already available to the attacker;
- exploit transition and resulting capability;
- concrete capability delta;
- credential validity, lifetime, principal, effective permissions, target
  audience, exchange path, and protected action when credentials are involved;
- authorization issuance time, whether later policy is retroactive, and whether
  in-flight or pre-issued authority is intentionally grandfathered;
- parent and derived credential lineage: whether secondary authority was already
  obtainable during the parent's valid lifetime and which event revokes each;
- approval granularity and authorization-server binding: whether a user trusted
  only one immutable credential recipient or reapproved a workspace-controlled
  configuration domain that already has equivalent execution and forwarding
  capabilities;
- dependency authority at the affected build stage: whether the influencing
  package is metadata-only or already executes build scripts with equivalent
  access to build inputs, outputs, credentials, and network policy;
- temporal trust equivalence across snapshots, heads, logs, and state versions;
- primitive-to-protected-consumer bridge for headers, local file effects,
  uninitialized values, routing changes, and generated code;
- authoritative read-back, negative controls, and missing proof;
- adjudication basis: merits, environmental mismatch, procedural inactivity,
  explicit exclusion, intended behavior, or prior knowledge;
- submission-time reachability and later patch timing;
- production stack equivalence across middleware, cache/CDN, proxy, file
  serving, browser permission, and consensus layers;
- canonical consensus, inclusion, and finality rather than one local node view;
- the exact closest comparison path, including same-URL top-level navigation;
- report readiness: length limits, requested video/E2E proof, Needs More Info
  questions, and response deadlines.
- for races and environment-dependent chains: attacker-controlled trigger,
  timing window, measured reliability, topology, common/default prerequisites,
  and absence of lab-only synchronization;
- for filename/state collisions: attacker knowledge, entropy or predictability,
  state lifetime, victim-event prevalence, attempt budget, and measured success
  rate;
- counterfactual mitigation under the same attacker authority: whether the
  proposed control removes the attacker's capability or merely makes the same
  trusted source/channel take another step;
- exact lifecycle contract: which role change, password change, logout, client
  deletion, credential revocation, or synchronization event invalidates which
  session, credential, cache entry, authorization, or persistent object;
- known/public/fixed/duplicate/remediation status as an independent eligibility
  gate, separate from technical validity.

Positive-control promotion test:

- begin with the actor's exact limited role and owned-resource authority;
- prove that attacker-controlled stored data reaches a separate privileged
  consumer;
- enumerate all downstream consumers when one representation fans out;
- distinguish separate findings by terminal sink, protected effect, and fix;
- require shipped reachability, authoritative read-back, adjacent-role and
  cross-owner controls, and a safe minimum proof;
- preserve conventional post-exploitation as impact context rather than
  claiming steps that were not executed; and
- burn the exact public/fixed root for novelty unless a current-release bypass
  or distinct consumer is proven.

Use this equation as a decision aid:

`security impact = proven post-exploit capability - intended starting capability`

The result must be nonzero and cross a program-recognized boundary. A more
surprising route to an already permitted action is not automatically a security
impact.

Aggressively test these falsifiers:

1. The repository/provider/workspace/organization role was explicitly trusted
   to supply the same class of executable content, configuration, or resource.
2. The attacker already has an equivalent documented path to the same action,
   callee, data, project, or resource.
3. The effect requires DEBUG, operator opt-in, a nondefault policy, a victim
   anti-pattern, or an unproven external consumer.
4. The credential is short-lived, project-scoped, otherwise obtainable by the
   same role, or never shown to perform an otherwise forbidden action.
5. The persistent object belongs to the same user/role and revocation was never
   documented to revoke that separately owned object.
6. The technical mismatch reaches no production/release consumer whose trust
   decision protects a concrete asset.
7. The maximum supported severity is below the current program floor.
8. The PoC demonstrates only localhost mechanics, synthetic canary movement, a
   PoC-created overwrite target, or a patched difference without a real
   cross-privilege effect.
9. The strongest effect ends inside a documented demo, sample, quickstart,
   local-development server, or development preview and the current program
   requires production impact.
10. The alleged attacker is the same local user/operator who deliberately owns
    or changes the resolver, workdir, self-hosted deployment, or unrestricted
    same-UID execution environment the feature does not promise to resist.
11. A redaction, environment filter, path check, or other defense-in-depth
    hygiene is being mistaken for a process, host, credential, or authorization
    guarantee.
12. The parser/resolver differential performs an operation already available
    through an equivalent valid declaration, or remains within the configured
    and lockfile-pinned trust set.
13. The root cause was already public, reported, known, fixed, or under
    remediation before submission even though the technical impact is valid.
14. The source is archived or unmaintained and no current eligible production
    deployment or shipped consumer is proven.
15. The PoC forces a race with a database/table lock, debugger pause, or exact
    curator-controlled ordering but does not show an attacker-controlled window,
    success rate, or realistic production trigger.
16. Exploitation requires explicit selection of an active-content/unsafe viewer
    or disabling a relevant warning/control, and no stronger isolation promise
    is documented.
17. Forwarding-header identity depends on an operator-selected proxy topology,
    but the edge overwrite and trusted-proxy contract are not established.
18. A build contributor controls schemas/descriptors plus an equivalent
    executable manifest, build script, or generated-code input.
19. A role change, password change, logout-all, OAuth-client deletion, and
    credential revocation are being conflated despite distinct documented
    lifecycle semantics.
20. A high-level validation result intentionally summarizes one layer while the
    nested failure remains available, and no default protected consumer or
    aggregation guarantee is violated.
21. A signed or authenticated carrier is treated as confidential even though
    its documented property is only integrity and its readable/replayable state
    is the feature's intended function.
22. A malformed parser input reaches a state the same caller can already submit
    using a well-formed request, so the parser differential creates no new
    capability.
23. A configured package source, registry, mirror, schema, or build input is a
    trust anchor with an equivalent supported path to the same fetch, write, or
    execution effect.
24. A collision requires an exact filename, extension, rare victim event, or
    unmeasured guessing window whose practical success is not demonstrated.
25. A control-plane connectivity check is called a bypass of a data-plane deny,
    but the denied data operation remains blocked and the permission was not
    promised to suppress discovery or traversal traffic.
26. The proposed fix does not reduce the stated attacker's authority. For
    example, an attacker controlling the same trust-bootstrap channel can also
    replace a signing key and sign substituted content.
27. A denylist or revocation is assumed to invalidate pre-issued signed or
    attested authority even though the design is forward-looking and must
    preserve in-flight settlement.
28. A secondary token is called a post-revocation privilege gain although the
    same bearer could obtain it during its original valid lifetime and no
    cross-token revocation lineage is promised.
29. Signature fields from one operation are assumed to be mandatory for another
    despite internally consistent typehash, witness, documentation, and bounded
    signer-approved outcome.
30. A local profile editor is treated as a remote attacker despite already
    owning the adjacent token cache and the reused token's identity domain.
31. Snapshot or live-head drift changes only the version of untrusted input
    controlled by the same principal under the same repository-wide authority.
32. Authentication-derived bytes reach the wrong peer, but no compatible replay,
    oracle, or accepted protected action is demonstrated.
33. A remote value triggers a local file effect only because the user explicitly
    selected the stream and target, with no security-critical consumer proven.
34. A memory checker reports an uninitialized value, but protected memory bytes
    are not shown in an attacker-observable output and no shipped caller exists.
35. A specialized callback contract is violated without a production application
    that relies on it as an enforced routing or egress boundary.
36. Security-sensitive state drifts only in generated example code that the
    developer must review, while the actual product runtime remains safe and no
    deployed consumer is demonstrated.
37. A Not Applicable status came from procedural inactivity, so it supplies no
    merits-based falsifier until the missing report-readiness evidence is added.
38. A local harness skips a production middleware, file-serving, hosting,
    browser, or consensus layer that can change the authorization result.
39. One node accepts a state transition, but independently validating nodes do
    not reach canonical consensus or finality.
40. A browser privilege comparison tests fetch or subresources but omits the
    exact same-URL top-level navigation and redirect control.
41. A later local pre-fix replay is substituted for dated submission-time live
    reachability after the target was patched.
42. The claimed privacy promise covers document bytes but is expanded without
    evidence to intentionally public metadata, filenames, or pages.
43. The strongest terminal effect is a vulnerability class the current program
    explicitly excludes, even though the underlying mechanism is real.
44. Arbitrary code execution occurs only inside an updater sandbox expressly
    designed for untrusted dependency code, and no sandbox escape, unauthorized
    private-network reach, secret extraction, or cross-tenant access is proven.
45. An SDK creates an identity object but labels it unverified/local, while only
    a synthetic consumer ignores that status and authorizes on non-null output.
46. A library bug requires the application itself to construct an unusual
    handle, pool, share-detach, raw-I/O, descriptor, or command-line lifecycle
    that a remote attacker cannot trigger.
47. A transport-routing claim assumes confidentiality on plaintext or otherwise
    explicitly unsecured proxy traffic without an enforced route-isolation
    promise.
48. A compiler/backend combination builds in CI but no current production or
    shipped consumer is identified using the exact affected configuration.
49. A technically valid root cause was already reported or tracked; technical
    validity remains, but new-submission eligibility is
    `KILL_KNOWN_OR_DUPLICATE` unless the candidate crosses a distinct boundary.
50. A private duplicate is treated as something the researcher should have
    predicted. Only available prior art can be screened before submission.
51. A user renews approval for changed MCP or project configuration inside an
    already trusted workspace, and that workspace can reach the same credential
    or protected effect through equivalent hooks, settings, or execution paths;
    no narrower authorization-server binding promise is proven.
52. A transitive or direct dependency changes metadata precedence, but the same
    attacker-controlled package is already in the resolved graph with build-time
    code execution capable of producing the same output or access.

Positive controls `#3931777` and `#3931771` demonstrate gate-passing structure:
an Author controls only an owned attachment, untrusted media metadata reaches
real filesystem-deletion or Administrator-browser consumers, direct effects
are manually observed, lower-role and cross-owner controls fail, and the
capability delta crosses a recognized privilege boundary. Their exact
WordPress roots are now public and fixed, so reuse is
`KILL_KNOWN_OR_DUPLICATE`; retain the generalized multi-consumer audit method.

Verdicts:

- `IMPACT_GATE_PASS`
- `IMPACT_GATE_BLOCKED`
- `INFORMATIVE_LIKELY`
- `KILL_NO_CAPABILITY_DELTA`
- `KILL_TRUSTED_DOMAIN`
- `KILL_BY_DESIGN`
- `KILL_NON_PRODUCTION_TARGET`
- `KILL_THREAT_MODEL`
- `KILL_KNOWN_OR_DUPLICATE`
- `KILL_NO_PRODUCTION_REACHABILITY`
- `KILL_PROGRAM_SEVERITY`
- `KILL_ENVIRONMENT_MISMATCH`

Do not kill by pattern resemblance alone. The Informative corpus is a set of
negative controls. Prove that the same target-specific trust or capability
condition applies. If decisive evidence is unavailable, use
`IMPACT_GATE_BLOCKED` and name the exact unblocking evidence.

Only `IMPACT_GATE_PASS` may advance toward `STRONG`. `STRONG` plus
`MANUALLY_CONFIRMED` establishes vulnerability validity; report readiness also
requires `TRIAGER_PROOF=PASS`. Otherwise return
`NO VALID FINDING`.


<!-- AUTHORIZED_OFFENSIVE_PROMPT:v1 -->
## Authorized offensive-first default

For every explicitly authorized security task, begin with attacker objectives, reachable entrypoints, exploit-chain composition, privilege or authority transitions, protected sinks, and concrete program-recognized impact. Prioritize proving or falsifying exploitability over generic hardening, detection, compliance, remediation, or blue-team telemetry; produce those defensive outputs after offensive proof unless the user explicitly requests them first. Preserve exact scope, safe harbor, researcher-owned data, harmless proof, rate limits, abort conditions, cleanup, and all prohibitions on destructive, stealthy, credential-stealing, persistence, evasion, or third-party activity. This model-agnostic posture applies to every model that consumes this prompt.
<!-- END_AUTHORIZED_OFFENSIVE_PROMPT -->
