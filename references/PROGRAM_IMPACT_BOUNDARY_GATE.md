# Program Impact Boundary Gate

## Purpose

This method converts the user's supplied HackerOne adjudications into two
corpora: Informative, Not Applicable, and Duplicate negative controls; and
Resolved plus rewarded positive controls. Negative controls stop spending
research and reporting effort on technically accurate behavior without
program-recognized impact. Positive controls identify the evidence shape that
should survive hard triage.

These adjudications are evidence about the named program decisions at the time
they were made. They are not universal law. A future candidate that resembles
one of them must be evaluated against its own current program policy, documented
trust model, attacker role, deployment, consumer, and impact. Similarity creates
a falsification obligation, not an automatic KILL.

## Core invariant

A bounty-grade candidate needs all of the following:

1. an attacker-controlled transition on a current eligible asset;
2. an intended security boundary supported by program policy, documentation,
   architecture, UI trust language, or enforced controls;
3. a protected asset/action/identity unavailable under the attacker's starting
   authority;
4. a nonzero capability delta caused by the vulnerability;
5. a concrete security effect observable through authoritative read-back;
6. a severity/class that meets the current program's written eligibility bar.

Use:

`starting capability -> exploit transition -> resulting capability`

If the resulting capability is equivalent to an intended capability already
held by the same principal or trust domain, the security delta is zero even if
the route is surprising or the implementation is inconsistent.

## Mandatory program-impact card

Record before expensive proof work:

| Field | Required evidence |
|---|---|
| Program fit | current official scope, exclusions, severity floor, eligible impacts |
| Asset maturity | production product versus demo, sample, quickstart, local-development server, self-hosted component, or development preview; current program impact ceiling |
| Production reachability | current eligible deployment or shipped consumer, not only an archived/unmaintained repository, local harness, or source tree |
| Adjudication basis | security/impact rejection, environmental mismatch, procedural inactivity, explicit excluded class, intended behavior, or prior knowledge; do not treat the status label alone as technical evidence |
| Submission-time state | dated evidence that the behavior was reachable when submitted, later patch timing, and whether current-only replay uses a deliberately old revision |
| Production stack equivalence | every material middleware, cache/CDN, proxy, file-serving, browser-permission, consensus, and deployment layer represented by the proof |
| Canonical consensus | for distributed ledgers, unmodified multi-node admission, canonical inclusion, finality, and acceptance by independently validating nodes rather than one local view |
| Exact comparison control | the closest ordinary supported primitive under the same URL, redirect, browser settings, actor, and state, including top-level navigation when relevant |
| Report readiness | program format/word limits, requested realistic PoC/video, Needs More Info deadline, and complete evidence package before submission or response |
| Starting authority | exact role, tenant/org/project, owned resources, existing supported actions |
| Consent/trust | directory/repository/provider/config/organization trust decision and warning/UI |
| Defended threat model | actors and local/operator/process/workdir powers the feature actually promises to resist |
| Intended promise | what control is supposed to prevent, with source or documentation |
| Guarantee type | security boundary versus documented behavior, convenience redaction, or defense-in-depth hygiene |
| Property purpose | confidentiality, integrity, authenticity, authorization, isolation, revocation, availability, or non-security presentation/reconstruction behavior |
| Protected target | exact secret, data, action, identity, artifact, recipient, or system |
| Equivalent path | whether the actor can already reach the same result by a supported route |
| Conditions | default versus DEBUG/operator opt-in/nonstandard configuration |
| Exploit realism | attacker-controlled timing/topology, default/common prerequisites, measured reliability, and absence of lab-only synchronization |
| Collision feasibility | attacker knowledge, entropy, state lifetime, victim-event prevalence, attempts, and measured success rate |
| Counterfactual defense | whether the proposed fix removes authority from the same attacker or merely adds a step through another attacker-controlled trust channel |
| Authorization time | when authority was validly issued, whether later policy changes are retroactive, and whether in-flight work is intentionally grandfathered |
| Derived credential lineage | whether a secondary token is newly created by the flaw, was already obtainable during valid authority, and which event revokes it |
| Temporal trust equivalence | whether old and new snapshots, heads, logs, or states are controlled by the same principal and trust class |
| Operation-specific signed scope | exact fields and outcomes authorized by each distinct signed operation; do not infer cross-operation symmetry |
| Effect-to-impact bridge | whether a wrong header, file effect, uninitialized value, routing change, or generated-code difference reaches a protected real consumer |
| Exploit transition | source-to-consumer/state flow causing the claimed delta |
| Resulting authority | exact new read/write/execute/auth/sign/exchange capability |
| Capability delta | what is newly available and why it matters |
| Evidence | baseline, negative control, current release, authoritative read-back, cleanup |
| Prior art | public, previously reported, known, fixed, duplicate, or already under remediation |
| Missing proof | the single fact that would change the verdict |

Treat every revocation claim as a **lifecycle contract**: identify the exact
event, authoritative state, invalidated object, propagation timing, and
documented guarantee. Never assume that a role change, password change,
logout-all action, OAuth-client deletion, cache invalidation, and deletion of a
user-owned persistent object are interchangeable.

## Cross-report rejection patterns

### 1. Operator-enabled diagnostics are not automatically cross-privilege

Report `#3975775` demonstrated an OIDC value in runtime logs when DEBUG was
enabled. The supplied adjudication rejected the impact because the separation
between a Runtime Logs viewer and project identity was not established, the
credential was short-lived, and acceptance by a protected external service was
not proven.

Gate lesson:

- distinguish default production behavior from explicit diagnostic opt-in;
- prove the logs role cannot obtain equivalent identity elsewhere;
- prove current token audience, lifetime, effective permissions, and a concrete
  protected action;
- do not promote hypothetical cloud exchange or external trust policies.

### 2. Already-consented provider content needs an independent trust victim

Report `#3973303` showed a Marketplace skill path changing install scope to
global and installing more content from the same provider. The adjudication
treated that as broader reach for provider-controlled content the user had
already chosen to install. The overwritten skill in the PoC was also created by
the PoC, not an independently trusted official skill.

Gate lesson:

- prove the overwritten target belongs to a distinct trusted principal;
- prove automatic consumption creates a new protected effect;
- widening persistence or visibility is not enough when the same provider was
  already authorized to supply agent instructions.

### 3. Repository-local executable resolution can stay inside repo trust

Report `#3973467` showed a repository-local Windows command shim receiving a
fresh project token. The adjudication found that running authenticated tooling
inside an attacker-controlled repository already granted repository code the
developer's authority, and the short-lived token did not add capability.

Gate lesson:

- compare against all intended repository execution paths, not only the exact
  command path;
- prove a pre-trust, sandbox, privilege, or credential boundary not already
  lost to the repository;
- a new route to the same developer authority is zero delta.

### 4. Correct cryptographic mismatch can still miss the program severity bar

Report `#3971480` demonstrated that artifact-signature verification used one
certificate while code-signing EKU validation used another. The technical
boundary mismatch was real, but the supplied Coinbase decision classified the
supported result below its then-current High/Critical/Extreme program floor.

Gate lesson:

- bind the mismatch to an actual protected artifact consumer and unauthorized
  release/signing decision;
- prove the maximum concrete downstream effect, not a hypothetical workflow;
- check the current program severity floor before deepening a Low/Medium lane.

### 5. Untrusted deployment configuration plus shared project access can be zero delta

Report `#3972786` showed a repository-controlled deployment root collecting a
file outside the clone. The adjudication emphasized that the victim chose to
run an authenticated deploy against attacker-supplied configuration and that
the demonstrated recipient already had access to the destination project.

Gate lesson:

- prove a documented tracked-source or repository-root isolation guarantee;
- prove the recipient could not otherwise read the destination or influence the
  deployment;
- do not equate out-of-tree collection with cross-privilege disclosure when the
  demonstrated recipient is already an authorized project reader.

### 6. Programmatic configuration execution may be the feature's purpose

Report `#3972687` showed `vercel link` evaluating repository-controlled
programmatic configuration. The adjudication treated evaluation as documented
behavior within a trusted repository, with no promise that linking was inert.

Gate lesson:

- establish an explicit non-execution promise for the command or pre-trust
  phase;
- do not infer a boundary from a command name;
- if trusted project configuration is intentionally executable, file access
  under that authority is not a new capability.

### 7. Routing inconsistency is not authorization when an equivalent path exists

Report `#3968095` demonstrated direct execution of a callee omitted from the
model-facing tool set. The adjudication confirmed the inconsistency but found
the callee already reachable through the documented caller with the same
application authority; approval controls still applied, and the PoC's custom
caller policy was outside the documented authorization interface.

Gate lesson:

- compare direct and documented indirect paths, arguments, approvals, and
  authority;
- prove the bypass skips a supported security control, not a routing convention;
- hiding a capability from one representation is not access control when the
  actor can invoke it through an equivalent intended interface.

### 8. Integrity primitives are not automatically authorization boundaries

Report `#3624130` demonstrated cross-group replay of signed flag precompute
codes. The adjudication treated the signing mechanism as an integrity/performance
building block, not an SDK authorization boundary; security impact required an
application to use rollout flags as its sole authorization control.

Gate lesson:

- prove the primitive's documented security purpose;
- trace replay to a program-owned protected action or data disclosure;
- application misuse or an anti-pattern cannot be assumed to convert an SDK
  correctness issue into bounty impact.

### 9. Shared organization WRITE authority can include shared resource mutation

Report `#3926585` demonstrated an organization WRITE member replacing a
scheduled job artifact that later ran with another member's supplied secret.
The supplied Hugging Face adjudication treated organization jobs as shared org
resources modifiable by org writers.

Gate lesson:

- map ownership at the resource level, not the creator-name level;
- prove the platform promises per-member isolation for the artifact or secret;
- member-private data alone does not establish isolation if the execution
  resource is intentionally shared and mutable by that member role.

### 10. Revoking one credential need not revoke user-owned persistent objects

Report `#3955537` showed a read-scoped OAuth client creating a scheduled export
that survived client deletion. The adjudication found that the read role could
already view the same data, scheduled reports belonged to the Matomo login, and
client revocation was not defined to remove the user's scheduled reports.

Gate lesson:

- separate OAuth-client lineage from user/resource ownership;
- prove the external recipient receives data beyond the principal's read scope;
- prove a documented revocation cascade before claiming persistence bypass.

### 11. Symlink/archive mechanics need a recognized source-isolation promise

Report `#3923008` showed deployment archiving dereferencing a tracked symlink
into an ignored local file. The supplied Notion response requested concrete
platform exploitability beyond the mechanism.

Gate lesson:

- prove the deployment tool promises tracked bytes or repository-root isolation;
- prove a realistic attacker can plant the link and receive the protected bytes
  without already controlling an equivalent execution or destination path;
- a synthetic canary and hosted read-back prove transport, but not necessarily
  the missing program-recognized trust boundary.

### 12. Workspace trust can authorize project-selected endpoints and configuration

Report `#3950679` showed a trusted project setting redirecting a client
connection carrying an OAuth access token. The Anthropic adjudication treated
the directory trust dialog as the control point: after trust, hooks, MCP servers,
environment variables, permissions, and project configuration operate in the
user's trust domain.

Gate lesson:

- distinguish pre-trust and post-trust behavior;
- prove a trust-dialog bypass, misleading scope promise, or forbidden credential
  forwarding after a narrower consent;
- post-trust configuration effects are not a new boundary merely because they
  reach a sensitive client subsystem.

### 13. A complete development-preview exploit can still miss the impact ceiling

Report `#3857254` demonstrated cross-site discovery of a loopback development
WebSocket, unauthenticated state mutation, attacker-controlled extension code
execution, and authenticated read capability inside a Shopify development
preview. The supplied adjudication nevertheless required impact outside that
limited preview, such as protected production merchant data, authenticated
actions on a non-development shop, credential replay, or persistence.

Gate lesson:

- score the strongest protected effect in the asset category actually reached;
- do not promote development-preview authority to production impact by analogy;
- check the program's explicit impact ceiling for development tooling before
  building an elaborate browser-to-loopback chain.

### 14. Documented local demos are not production authentication boundaries

Report `#3948952` showed permissive CORS exposing synthetic mailbox contents
from a local Email Agent demo. The supplied adjudication treated the repository
as an explicitly local, single-user demonstration with a security warning, no
authentication, and no production-security promise; the same root cause also
had prior program treatment.

Gate lesson:

- classify production product versus demo before vulnerability ideation;
- a browser can reach localhost does not make a documented sample a production
  service;
- require an eligible production or cross-user asset and screen duplicate roots.

### 15. A local user's deliberate self-bypass may be outside the policy threat model

Report `#3948366` showed Git `url.insteadOf` rewriting an allowlisted marketplace
URL after validation. The supplied adjudication found that the same local user
could modify their own Git configuration and that the managed setting did not
promise resistance to deliberate changes in the user's resolver environment.

Gate lesson:

- identify whether the protected actor and attacker are actually distinct;
- prove the enterprise control remains authoritative over the downstream
  resolver configuration;
- local-user self-bypass is not an administrative policy bypass when that user
  owns the enforcement environment and no tamper-resistance promise exists.

### 16. Self-hosted workdir content plus unrestricted execution can erase the delta

Report `#3948342` showed automatic skill setup following a pre-existing workdir
symlink and replacing an outside directory. The adjudication treated the
self-hosted workdir as operator-trusted input and noted that unrestricted shell
execution was already an intended capability, so the precondition already
provided the meaningful host authority.

Gate lesson:

- compare the primitive with all existing capabilities of the accepted workdir;
- distinguish a narrower filesystem route from new host authority;
- require a lower-privilege writer or a promised containment boundary before
  treating path escape as a security delta.

### 17. Quickstart APIs can be explicitly outside the product security boundary

Report `#3934602` demonstrated DNS rebinding against an unauthenticated local
assistant quickstart, including transcript reads and approval of a pending tool.
The supplied adjudication treated it as a single-developer sample whose docs
required real authentication and per-user scoping before broader use, with
effects confined to its own hosted sandbox sessions.

Gate lesson:

- do not report missing production hardening in code explicitly labeled a
  quickstart or sample;
- require credential disclosure, cross-user access, or an effect beyond the
  sample-created session on an eligible asset;
- generic local-development-server exposure is not automatically product impact.

### 18. Documented DEBUG body logging is not a redaction guarantee

Report `#3934184` showed a request-body authorization token appearing only at
an explicitly enabled DEBUG level. The supplied adjudication cited documentation
that full HTTP requests and responses, including sensitive bodies, may be logged;
header redaction was a convenience rather than a guarantee that logs were safe
to share.

Gate lesson:

- read the logging contract before treating partial redaction as a boundary;
- distinguish default exposure from operator-enabled diagnostic disclosure;
- schema-aware body redaction can be worthwhile hardening without constituting
  a security fix.

### 19. A valid vulnerability can still be known or duplicate

Report `#3910136` proved that a deleted API key remained authorized through a
stale positive cache and performed a protected payment, but the program stated
it already knew the vulnerability and had remediation in progress before the
submission. Its Informative classification did not negate the technical proof.

Gate lesson:

- keep technical validity separate from bounty novelty and eligibility;
- prior-art screening is an independent hard gate even after end-to-end impact;
- use `KILL_KNOWN_OR_DUPLICATE`, not a no-impact verdict, when the root cause was
  already known or under remediation.

### 20. Best-effort credential hygiene is not process isolation

Report `#3933799` showed an unrestricted Bash tool reading credentials from its
same-UID parent process despite child-environment scrubbing. The supplied
adjudication treated shell environment filtering as best-effort hygiene, not a
promise to isolate an unrestricted process from same-user operating-system
state; operators were instructed to provide their own container boundary.

Gate lesson:

- identify whether a defense is a security guarantee or defense-in-depth hygiene;
- an unrestricted same-UID shell already possesses broad parent-process read
  capability under the stated execution model;
- require an explicit isolation promise or a genuinely constrained attacker.

### 21. Parser drift has no security delta when a supported input grants the same fetch

Report `#3930172` showed a raw lockfile match causing a private Git fetch that
Cargo itself ignored. The supplied adjudication noted that the same workspace
author could declare the repository as an ordinary Git dependency, producing
the same fetch, while subsequent shared-store readability belonged to the Nix
deployment model.

Gate lesson:

- compare malformed or parser-differential inputs with equivalent valid inputs;
- if the actor can trigger the identical protected operation through a supported
  declaration, the differential is robustness rather than capability gain;
- separate component behavior from ambient shared-store policy.

### 22. Resolver differences remain correctness issues inside the configured trust set

Report `#3929882` showed Cargo and a Nix plugin resolving registry metadata
differently under split configuration. The supplied adjudication emphasized
that the workspace already selected the lower-trust replacement registry and
that every resulting artifact remained pinned by the lockfile.

Gate lesson:

- prove the differential introduces bytes, identity, or authority outside the
  configured registry and locked artifact set;
- metadata influence from an explicitly selected registry is not itself a new
  trust boundary;
- require a protected consumer effect, not merely behavioral divergence.

### 23. Disputed host prerequisites keep a strong primitive BLOCKED

Report `#3924650` demonstrated a disabled PKCS#11 rule loading an attacker DLL
from a UNC path while Burp project trust was disabled. PortSwigger's supplied
decision treated exploitation as impractical under its default Windows model
because it believed additional firewall and share prerequisites were required;
the reporter later supplied contrary two-VM evidence, but the status remained
Informative in the material provided.

Gate lesson:

- freeze the exact stock host edition, policy, firewall, SMB authentication, and
  mapping state before calling remote library loading realistic;
- preserve contradictory evidence as `IMPACT_GATE_BLOCKED`, not an automatic KILL;
- prove both common reachability and the security promise of untrusted-project mode.

### 24. Current production reachability is independent of source validity

Report `#3925580` proved a cross-subtree page takeover in an old CMS repository.
The supplied adjudication required a live production system because the source
had not been maintained for roughly twelve years.

Gate lesson:

- do not infer deployment from an in-scope-looking repository or local E2E;
- record the exact current production consumer before deep exploit work;
- use `KILL_NO_PRODUCTION_REACHABILITY` when the program requires live evidence
  and only archived or unmaintained source is available.

### 25. Active rendering can be an explicit trust decision

Report `#3919124` showed rendered attacker HTML reading an authenticated response
reused from Burp's Site map. The supplied decision treated the effect as a
consequence of intentionally enabling active rendering of attacker content;
the reporter's sticky-view appeal attempted to narrow that consent but did not
change the recorded status.

Gate lesson:

- distinguish safe/default viewers from explicitly active content modes;
- prove automatic execution without the relevant consent or a documented
  credential-context isolation promise;
- do not treat every dangerous consequence inside an unsafe viewer as a bypass.

### 26. Forwarding-header identity belongs to the deployed proxy topology

Report `#3885945` showed direct clients spoofing forwarding headers that
tracker-proxy converted into authenticated visitor IPs. Matomo treated header
trust as an operator/front-end deployment decision, including for its documented
direct installation, and considered analytics pollution below the security bar.

Gate lesson:

- map the actual edge, `REMOTE_ADDR`, header overwrite, and trusted-proxy model;
- prove a product-owned invariant rather than assuming all forwarding headers
  must be authenticated by the application;
- establish a protected effect beyond the operator-selected visitor-IP model.

### 27. Layered validation summaries require a documented aggregation invariant

Report `#3646244` showed a top-level C2PA validation state remaining valid while
an embedded ingredient retained a nested invalid result. The supplied decision
treated this as layered validation: the primary manifest summary and ingredient
details were separate surfaces, and applications requiring strict chain checks
could inspect the nested result.

Gate lesson:

- prove what the high-level status contract actually summarizes;
- do not assume every nested failure must poison every aggregate status;
- trace the mismatch into a default protected consumer that accepts an artifact
  contrary to a documented policy.

### 28. Trusted schema inputs can be equivalent to executable build inputs

Report `#3905967` demonstrated Rust injection through a newline in a protobuf
source path. Anthropic treated schemas and descriptor metadata supplied to code
generation as trusted build artifacts in the same class as manifests and build
scripts, giving their controller equivalent build-input authority.

Gate lesson:

- classify the contributor's complete build-input authority, not only file type;
- prove an explicit non-executable or lower-trust schema contribution boundary;
- generated-code execution is zero delta if the actor already controls an
  equivalent executable build input.

### 29. Cross-system role synchronization is not automatically revocation

Report `#3887461` showed a WordPress role downgrade leaving previously
synchronized Matomo superuser authority usable with a still-valid Application
Password until synchronization. Matomo treated this as delayed consistency;
revoking the credential or account was the supported immediate access-control
action, while role mutation alone did not promise credential invalidation.

Gate lesson:

- separate authentication credential validity from authorization synchronization;
- identify the documented revocation event and propagation guarantee;
- do not infer immediate cross-system invalidation from a role change alone.

### 30. Reauthentication prompts may be defense in depth for a full session

Report `#3894878` showed a fully authenticated Matomo session using a login-only
2FA setup path to view recovery codes and replace the authenticator without the
password confirmation used by sibling routes. Matomo stated that the confirmation
was defense in depth, not a security boundary it rewarded against an actor with
full session control.

Gate lesson:

- establish whether session hijack resistance is an explicit protected invariant;
- compare resulting durable authority with everything the starting session can
  already do;
- a sibling step-up check does not alone prove a program-recognized boundary.

### 31. A laboratory race needs an attacker-controlled production window

Report `#3896366` accurately showed an in-flight request restoring a session row
after logout-all. The PoC forced overlap with a database table lock; Matomo found
no realistic attacker-controlled timing window and noted that password change
still invalidated the restored session.

Gate lesson:

- prove the attacker can create and hold the overlap using ordinary privileges;
- measure the window, reliability, attempts, and victim action under production-
  realistic timing;
- test every supported revocation action rather than generalizing from one API.

### 32. Read authority can include creating user-owned delivery resources

Report `#3895960` is the same scheduled-export family represented elsewhere in
this corpus: a read-scoped client created a user-owned report that survived
client deletion. The supplied decision found no data beyond existing view
authority and no lifecycle promise binding user reports to the OAuth client.

Gate lesson:

- treat recipient delivery as an authority question, not automatically a write;
- model user-owned objects separately from delegated-client credentials;
- require cross-principal data or an explicit revocation-lineage guarantee.

### 33. Sub-second revocation races can fall below the marginal-impact bar

Report `#3895989` showed a session started with the old password surviving when
session creation and password modification shared one-second timestamp precision.
Matomo considered the added impact minimal because the attacker already knew the
valid password, had full account access, and additionally had to win a
sub-second race.

Gate lesson:

- calculate marginal post-race authority relative to the attacker's starting state;
- quantify timing reliability and session lifetime;
- check program guidance and severity before investing in credential-revocation
  races with prior full-account compromise.

### 34. Workdir confinement can collapse into existing worker authority

Report `#3885565` showed a repository-controlled `skills` symlink redirecting
Managed Agents setup outside the workdir. Anthropic treated the self-hosted
workdir as operator-trusted and the unrestricted worker shell as equivalent host
authority; later reports of the same family received the same treatment.

Gate lesson:

- compare path escape with every capability already granted to workdir content;
- require a distinct lower-trust writer or promised containment boundary;
- screen same-root prior reports before repeating a technically correct PoC.

### 35. Valid authorization bypasses can still miss the program impact floor

Report `#3820783` was validated as a legacy endpoint bypass of `release:delete`,
but Mozilla ultimately assessed deletion of a scheduled release insert as
minimal impact and closed it Informative after a Medium severity discussion.

Gate lesson:

- technical validation and authorization noncompliance do not determine payout;
- prove the concrete production release, availability, or integrity consequence;
- apply the current program severity floor before deepening a low-impact legacy
  administrative action.

### 36. Signed and replayable state is not necessarily confidential state

Report `#3849097` showed raw unlisted flag values in a signed-but-readable URL
and server-side reconstruction without the original request. Vercel treated
signature as an integrity mechanism and reconstruction from the code as the
purpose of precompute; flags and shareable URLs were not confidentiality
boundaries despite documentation using the word "encrypt."

Gate lesson:

- name the promised property before testing the primitive;
- JWS/signing does not imply encryption or secrecy;
- require a normative confidentiality guarantee and a protected first-party
  value, not developer misuse that places secrets in a shareable URL.

### 37. A credential-shaped configuration key needs supported-config proof

Report `#3867328` showed URI userinfo in a Bundler mirror key reaching unrelated
origins through the User-Agent and authorizing a private registry on replay.
The maintainer accepted the mechanism but disputed that real credentials belong
in setting names or authenticated mirror-source keys; the reporter supplied a
technical clarification, but no changed adjudication appears in the material.

Gate lesson:

- separate parser acceptance from documented and realistically used configuration;
- verify official docs, native tests, and current behavior for the exact
  credential-bearing key position;
- keep a real cross-origin secret flow `IMPACT_GATE_BLOCKED` when the decisive
  supported-configuration premise remains disputed.

### 38. A configured package source may be the trust anchor

Report `#3849853` demonstrated a gem source causing constrained out-of-cache
`.gemspec` writes before safe deserialization. Ruby treated a selected source or
mirror as a trust anchor that can influence the client more directly through
ordinary package delivery.

Gate lesson:

- enumerate all ordinary capabilities of the configured source;
- prove a lower-trust metadata channel or a protected path unavailable through
  package contents and install behavior;
- path traversal alone does not establish capability delta against a hostile
  source already authorized to supply packages.

### 39. Revoked UI state can still be a low-impact product bug

Report `#3857175` showed disabled or trashed MailPoet forms continuing to create
subscriber/list state and welcome-email tasks. Automattic treated the effect as
a general bug or best-practice issue; the report itself claimed only low
subscriber/list integrity impact and no confidentiality or availability effect.

Gate lesson:

- quantify the protected asset and maximum program-recognized consequence;
- lifecycle inconsistency is not sufficient when the resulting write is low
  value, self-selected, or ordinary spam/list pollution;
- apply the severity floor before building a long E2E around minor integrity.

### 40. Shared temporary-state collisions need practical key discovery

Report `#3847712` showed one phpBB uploader finalizing another user's partial
upload when filename, extension, and temporary state collided. phpBB acknowledged
missing ownership binding but found exploitation impractical because incomplete
uploads were rare and the attacker needed the exact name and extension, even
with a possible 24-hour cleanup window.

Gate lesson:

- record collision key entropy and every attacker knowledge requirement;
- measure incomplete-state prevalence, persistence, attempts, and success rate;
- a deterministic chosen-name PoC proves the primitive, not victim-key discovery.

### 41. Parser differentials are zero delta when valid input reaches the same state

Report `#3830857` demonstrated lenient `google.protobuf.Any` JSON parsing that
canonicalized malformed input into empty/default messages. Anthropic confirmed
the divergence but found that clients could send well-formed empty/default Any
messages producing the same handler-visible states, while the security effects
came from synthetic application logic and no production service was affected.

Gate lesson:

- compare malformed input with every semantically equivalent well-formed input;
- require a security check that rejects all valid equivalents but is bypassed by
  the differential;
- a custom consumer that misuses default values does not prove platform impact.

### 42. Intentional compatibility downgrade needs a current forbidden invariant

Report `#3799781` showed an SSL-incapable Revive runtime intentionally falling
back to HTTP update metadata that could produce administrator XSS. The maintainer
described the fallback as historical design and planned its removal as cleanup.

Gate lesson:

- distinguish a bad legacy design from violation of a current security promise;
- prove realistic prevalence on supported production runtimes and the program's
  expectation that transport must fail closed;
- do not infer bounty eligibility solely from a proposed hardening issue.

### 43. Permission labels can govern the data plane but not connectivity control

Report `#3808838` showed a remote-access-disabled Meshnet peer still exchanging
connectivity-check messages, endpoint candidates, and traversal probes. Nord
stated that connectivity checks run regardless of incoming permissions, while
the final incoming data plane remained blocked by firewall rules.

Gate lesson:

- map permission scope across control plane and data plane separately;
- endpoint discovery or probes are not a full access bypass without a denied
  final capability or explicit control-plane guarantee;
- do not inflate preconnection behavior into remote-access compromise.

### 44. A counterfactual control must reduce the same attacker's capability

Report `#3803376` showed Nord's RPM installer accepting an unsigned substituted
package under a TLS-interception model. Nord reasoned that an attacker controlling
the same path for package bytes and publisher key material could simply replace
the key and sign the package, so enforcing `gpgcheck` added a step but did not
remove capability under the stated attacker model.

Gate lesson:

- hold attacker authority constant in positive and counterfactual controls;
- prove a pinned trust root the package-body attacker cannot modify;
- a security check is not an effective boundary when every trust input it relies
  on is controlled by the same attacker.

### 45. Forward-looking policy need not revoke pre-issued authority

Report `#3803950` showed a transfer package issued before denylisting remaining
redeemable afterward. Circle confirmed the code path but treated attestations as
irrevocable in-flight settlement authority: new entry and issuance were blocked,
the recipient was already signed, and the same depositor retained an ordinary
withdrawal route.

Gate lesson:

- freeze authority at issuance time, not only at later redemption time;
- prove that the policy promises retroactive invalidation rather than
  forward-looking denial;
- require a distinct victim, post-policy issuance, or movement outside the
  original signed bounds before calling grandfathered settlement a bypass.

### 46. A derived token must add authority unavailable during the parent token's life

Report `#3792094` showed a revoked FxA bearer surviving a positive
introspection cache and retrieving a Relay-native token that outlived the FxA
bearer. The initial closure treated cache validity until expiry as an accepted
distributed-system tradeoff; the later derived-token evidence did not establish
a changed final adjudication or a documented cross-token revocation contract.

Gate lesson:

- map parent and derived credentials as separate lifecycle objects;
- ask whether the same actor could already mint or read the derived credential
  while the parent token was valid;
- keep the lane blocked until official lineage semantics and a genuinely new
  post-revocation capability are proven.

### 47. Different operations may intentionally sign different authorization scopes

Report `#3680070` showed `cancel()` omitting the attester identity that
`execute()` includes. Circle found the cancel typehash, witness string, hash
function, and documentation consistently attester-agnostic; the payer still
authorized nonce consumption and bounded fee routing, while the remaining harm
was one retryable nonce and required an unproven signature-sharing channel.

Gate lesson:

- derive authorization from the exact signed statement for each operation;
- do not assume two operations must share the same witness fields;
- require realistic authorization-material acquisition and impact outside the
  signer-approved outcome.

### 48. Wrong local profile selection can be correctness inside one user's trust domain

Report `#3797857` showed a saved OIDC profile reusing a fresh cached token after
the same local user changed its workspace or service-account target. Anthropic
treated the profile and adjacent credential cache as one trusted local domain;
the editor could already read and use the cached token and no new organization
or identity authority was obtained.

Gate lesson:

- distinguish wrong-principal execution from cross-principal access;
- map who can modify configuration and who can read the credential cache;
- require a lower-trust switch actor or inaccessible protected target before
  promoting local stale-scope behavior.

### 49. Snapshot drift is zero delta when both snapshots have the same content authority

Report `#3796714` showed a PR review created for head A reading later-head B CI
logs. Anthropic treated head selection as relevance filtering: the token's
`actions:read` authority was repository-wide and the same PR author controlled
untrusted log content at both heads.

Gate lesson:

- compare the author and trust class of both temporal states;
- a trigger-time snapshot is a security boundary only when it excludes content
  from a different or stronger authority;
- prove a protected action that later content can influence but equivalent
  original-head content cannot.

### 50. Authentication-derived material needs protected-peer acceptance proof

Report `#3968729` showed a stale Digest challenge causing libcurl to send an
authentication-derived response to another origin. Curl fixed the state-binding
bug but did not accept the security classification; the report did not complete
an accepted replay against the protected first peer or prove the proposed
signing-oracle chain on a real application.

Gate lesson:

- separate public challenge parameters from password-derived response material;
- prove nonce/method/URI-compatible acceptance by the protected peer;
- do not promote a wrong-origin header from mechanism to credential compromise
  without a realistic consumer and authoritative protected action.

### 51. A remote-triggered file effect can remain below the security-impact floor

Report `#3970639` showed `--etag-save -` truncating a file the user opened with
append redirection when a server returned an ETag. Curl reproduced and fixed the
bug but considered the immediately observable, explicit-output behavior a normal
bug without a protected consequence.

Gate lesson:

- distinguish filesystem effect from impact on a security-critical asset;
- account for the user's explicit stream and target selection;
- require a supported workflow and downstream protected decision, not a
  hypothetical important log file.

### 52. An uninitialized-value diagnostic is not automatically information disclosure

Report `#3972196` showed documented long-double formatting read as `double`,
producing garbage and Valgrind uninitialized-value findings. No in-tree use,
remote trigger, protected bytes in output, or production consumer was found.

Gate lesson:

- prove that protected memory bytes reach an attacker-observable sink;
- incorrect output or undefined control flow is not itself confidentiality loss;
- require an actual shipped caller before elevating a discouraged API mismatch.

### 53. A callback contract violation needs a real security-policy consumer

Report `#3971496` showed HTTP/3 reconnecting a UDP socket despite
`CURL_SOCKOPT_ALREADY_CONNECTED`. The callback arrangement was specialized and
no production application relying on it as an egress or relay boundary was
identified; curl documented the limitation rather than classifying a vulnerability.

Gate lesson:

- identify the shipped application that turns a callback contract into policy;
- prove unauthorized network reach or disclosure beyond a routing mismatch;
- a clean patched A/B for library semantics is not production security impact.

### 54. Generated example code is not automatically the product's runtime boundary

Report `#3972316` showed `--libcurl` example source carrying `--insecure` across
`--next` while the curl CLI remained safe. Curl treated generated source as an
incomplete example that developers must review, and no deployed consumer was
shown.

Gate lesson:

- classify generator output as example, supported artifact, or production code;
- verify an explicit security-equivalence guarantee rather than general wording;
- require a current deployed consumer and real attacker path before converting
  generated-code drift into TLS compromise.

### 55. Low-impact cache poisoning needs policy fit and reliable material harm

Report `#3739926` showed a missing Referer cache-key dimension that could prevent
an embedded iframe from resizing. The N/A decision emphasized the narrow cache
conditions and limited widget disruption, while the report asserted a dated
live-at-submission reproduction and an explicit program example for partial DoS
via cache poisoning.

Gate lesson:

- preserve submission-time live evidence even if the target is patched later;
- resolve conflicts with exact current program severity examples before KILL;
- quantify cache-store conditions, victim prevalence, persistence, and material
  availability impact rather than relying on a local pre-fix replay alone.

### 56. Procedural N/A is not a security adjudication

Report `#3800002` was closed N/A due to inactivity after a Needs More Info
request. The program did not issue a merits decision on the sandbox fail-open
claim.

Gate lesson:

- record procedural inactivity separately from technical rejection;
- make report readiness a gate: concise format, requested end-to-end proof or
  video, response deadline, and reviewer questions must be satisfied;
- never use an inactivity closure as evidence that a new technical lane has zero
  impact.

### 57. A partial local stack cannot establish production authorization behavior

Report `#3862436` imported a VIP ACL component into a local WordPress/Nginx lab
and showed derivative image paths failing open. Automattic rejected the proof
because it skipped part of the production VIP file-handling stack and therefore
did not reproduce on VIP infrastructure.

Gate lesson:

- require production stack equivalence for all routing, middleware, cache, ACL,
  and file-serving layers that can change the decision;
- a byte-identical source component does not prove the complete deployed path;
- use `KILL_ENVIRONMENT_MISMATCH` when the omitted production layer is decisive.

### 58. Approval of an attacker endpoint can include its redirect behavior

Report `#3863692` showed an approved custom Wallet RPC following a 307 to a
compatible loopback JSON-RPC service. Brave treated redirects as expected
endpoint behavior and the user-approved malicious RPC as the relevant trust
decision.

Gate lesson:

- determine whether approval delegates only one origin or the endpoint's normal
  redirect behavior;
- require an explicit per-hop destination promise before calling redirect
  following a boundary bypass;
- identify a realistic protected local consumer, not only a researcher-created
  compatible service.

### 59. Privileged browser fetch claims need the exact ordinary-navigation control

Report `#3863048` showed WDP issuing a blind loopback GET after a redirect while
several webpage subresource primitives were blocked. Brave responded that an
ordinary user visit could follow the same redirect; the proof did not isolate
the exact same-URL top-level navigation comparison.

Gate lesson:

- compare the privileged path with the closest ordinary primitive, including
  top-level navigation and the exact redirect response;
- keep the lane blocked when a claimed network capability delta is disputed by
  an untested equivalent path;
- still require a concrete protected local service and consequence.

### 60. One node's accepted state is not canonical consensus impact

Report `#3816519` showed a previously verified pending transaction accepted by
one local TRON test node after key revocation. Consensus checks were stubbed and
the program explained that independently validating nodes would reject the
later block, preventing stable network consensus.

Gate lesson:

- distinguish local object/store acceptance from canonical inclusion and
  finality;
- require a production-equivalent multi-node network without consensus stubs;
- account for authority validly exercised before revocation and prove realistic
  attacker control of propagation and block timing.

### 61. An excluded terminal impact remains excluded despite a real primitive

Report `#3810858` demonstrated that an unsigned HTTP status could reclassify a
signed response and trigger logout. Nord closed it because the resulting denial
of service was explicitly out of scope.

Gate lesson:

- apply the current excluded-impact list before investing in a deep mechanism;
- classify by the strongest proven terminal consequence, not the sophistication
  of the integrity gap;
- use `KILL_PROGRAM_SEVERITY` unless a distinct eligible security effect exists.

### 62. A reproducibility helper is not automatically an authenticity anchor

Report `#3802645` showed a curl release helper executing build inputs from the
tarball being checked and reporting self-reproducibility. Curl identified the
GPG signature as the authenticity anchor and did not promise the helper could
independently authenticate an untrusted tarball.

Gate lesson:

- identify the exact verifier security property and its trust anchor;
- distinguish provenance/authenticity verification from reproducibility or
  self-consistency;
- warnings against blind trust and authenticated build inputs can make execution
  intended rather than a pre-auth boundary break.

### 63. Apply the privacy promise only to the fields it actually covers

Report `#3728070` treated public invoice metadata and document filenames as
private because document downloads were private. Liberapay stated that invoice
pages are intentionally transparent and the program was paused except for
critical vulnerabilities.

Gate lesson:

- map the exact privacy promise to document bytes, metadata, filename, page, or
  workflow state instead of expanding it by association;
- verify whether anonymous page access is intentional product behavior;
- apply the active program severity floor before reporting lower-impact privacy
  expectations.

### 64. A valid root cause can still be bounty-killed as a duplicate

Report `#3983944` correctly demonstrated missing Cardano public-key-to-address
binding, but an earlier report already covered the same check and code path.

Gate lesson:

- preserve technical validity while independently killing submission novelty;
- screen public, known, and researcher-owned prior art before expensive proof;
- private duplicates are not predictable, so do not distort future technical
  triage merely because an unseen earlier submission existed.

### 65. Expected updater code execution needs impact outside its sandbox authority

Report `#3977820` showed a submodule gemspec executing inside Dependabot and
using its configured registry proxy. GitHub's policy explicitly excludes code
execution inside update jobs because they are designed for untrusted package
code.

Gate lesson:

- apply component-specific bounty exclusions before building an RCE PoC;
- distinguish intended dependency resolution from unauthorized secret access;
- require sandbox escape, cross-tenant access, unauthorized private-network
  reach, or another currently eligible boundary.

### 66. An explicitly unverified identity needs a real consumer that trusts it

Report `#3975896` produced an attacker-chosen Passport identity, but the SDK
marked it `verified: false` and `tokenSource: local`. The protected server was a
synthetic consumer written to ignore those fields.

Gate lesson:

- trace verification status through the actual authorization decision;
- do not equate object construction or a non-null identity with authentication;
- require a shipped deployed integration that remains vulnerable while using
  the documented input and verification contract.

### 67. Plaintext proxy routing needs a recognized confidentiality boundary

Report `#3973127` showed an IPv6 zone-selection bug that could route plaintext
proxy authentication to another link-local interface. Curl treated unsecured
proxy transport as outside its protected confidentiality model.

Gate lesson:

- name the transport property the product actually promises;
- prove a realistic attacker-controlled multi-interface topology;
- retain only if an authenticated or encrypted route boundary, or an explicit
  interface-isolation guarantee, is crossed in a current consumer.

### 68. Caller-constructed library lifecycle anomalies are not remote exploits

Report `#3971585` required an application to create unrelated connection pools,
use CONNECT_ONLY, detach a share, and then invoke raw I/O. No remote party could
force that sequence.

Gate lesson:

- separate library correctness from an attacker-reachable product state;
- require a shipped caller and attacker control over every decisive transition;
- kill application-controlled API misuse unless it causes a protected effect in
  a realistic consumer.

### 69. A local process-launch antipattern needs a remote trigger

Report `#3973158` required stdin and stderr to be closed together, verbose proxy
authentication, and an upload sourced from closed stdin. The remote origin
could not establish these prerequisites and pipe allocation was platform-sensitive.

Gate lesson:

- freeze who controls process launch, descriptors, and command-line options;
- require portable reliability and a current deployed wrapper;
- do not infer remote credential theft from a locally manufactured launch state.

### 70. Supported source configuration is not production reachability

Report `#3973093` found an OCSP validation gap in a GCC plus Apple SecTrust
configuration that curl exercised in CI, but no production application or
distributed binary using that niche build was identified.

Gate lesson:

- CI coverage proves build support, not affected users;
- require the exact compiler, TLS backend, platform, and shipped consumer;
- use `KILL_NO_PRODUCTION_REACHABILITY` until end-to-end deployment evidence
  exists.

### 71. Reapproval inside a trusted workspace does not imply field-level credential isolation

Report `#3948506` showed a stored MCP OAuth refresh token being sent to a newly
configured authorization server after the old project approval was cleared and
the changed server was explicitly approved. Anthropic treated project settings,
hooks, and MCP definitions in a trusted workspace as one authority domain with
equivalent ways to reach the user's execution context and credentials.

Gate lesson:

- model what the renewed approval delegates: one immutable URL or the changed
  workspace-controlled configuration and its normal execution behavior;
- require an explicit authorization-server binding or credential-recipient
  isolation promise before treating issuer mismatch as a defended boundary;
- retain only if disclosure happens before trust, without renewed approval, or
  produces authority unavailable through every equivalent trusted-workspace path.

### 72. Metadata precedence is zero delta when the same dependency already executes code

Report `#3928810` showed transitive Cargo `links` metadata overwriting a direct
dependency's normalized metadata and changing generated build output. Anthropic
found no added security capability because the attacker-controlled crate was
already in the locked dependency graph and could execute its own build script
during the same build.

Gate lesson:

- inventory the package's full authority at the exact build stage, not only the
  disputed metadata channel;
- compare the observed output, registry access, and source injection with what
  the already-running build script can do;
- retain only when a lower-trust metadata-only dependency cannot execute code,
  or when an explicit isolation promise protects a consumer beyond build-script
  authority.

## Validated positive-control patterns

### A. Low-privilege owned data can reach an arbitrary filesystem sink

WordPress report `#3931777` began with an Author who could upload and edit only
their own attachment. A media-finalization path stored attacker-controlled
filenames in attachment metadata. A later image-edit step copied the poisoned
entry into backup metadata, and attachment deletion derived both the deletion
target and its confinement directory from attacker-controlled state. A safe
lab canary proved deletion outside the intended uploads and document roots.

Why this passed:

- starting authority was narrow and did not include arbitrary filesystem
  deletion;
- ownership checks worked, but owned-object data crossed into a stronger
  filesystem consumer;
- the released Gutenberg path and an independent core path were reproduced;
- Contributor and cross-owner controls were denied;
- before/after filesystem evidence proved the direct capability; and
- the report separated demonstrated deletion from the unexecuted conventional
  site-takeover continuation.

Research lesson: never let a containment directory share attacker provenance
with the target it is supposed to constrain. When structured metadata reaches
cleanup or deletion, inventory every key copied through backup, edit, migration,
and lifecycle paths.

### B. The same stored representation can cross into a privileged renderer

WordPress report `#3931771` used the same low-privilege metadata write but a
different consumer. An attacker-controlled sub-size filename was concatenated
into an image URL and rendered without contextual escaping in authenticated
administration views. An inert browser canary executed in an Administrator
session even though the Author lacked script-posting authority.

Why this passed:

- the protected consumer was a real higher-privilege browser session;
- the result crossed Author-to-Administrator authority rather than remaining
  self-content;
- real browser execution on genuine administration URLs provided authoritative
  read-back;
- adjacent roles, cross-owner writes, clean attachments, and unaffected views
  supplied negative controls; and
- the renderer fix differed from the filesystem-deletion fix.

Research lesson: after finding an unsafe stored write, enumerate every later
consumer and rendering context. Different terminal sinks may justify separate
findings when the protected effect and required consumer fix materially differ.
Do not split cosmetic variants of the same sink.

### Positive-control constraints

These two reports are now public and fixed. Their exact WordPress
`finalize_item()` chains are novelty burn entries, not live templates. For a
future candidate:

- derive the hypothesis from current target code rather than replaying these
  paths;
- verify the exact current release and official fixes first;
- require a distinct bypass, representation, consumer, or security boundary;
- use only disposable file and DOM canaries; and
- stop after the minimum direct proof without real configuration deletion,
  account creation, plugin installation, credential access, or third-party
  impact.

## Reusable KILL matrix

| Condition proven for the current target | Default disposition |
|---|---|
| Same principal can already perform the same protected action | `KILL_NO_CAPABILITY_DELTA` |
| Attacker controls content inside an explicitly trusted repo/provider/workspace domain | `KILL_TRUSTED_DOMAIN` |
| Role intentionally owns or may mutate the same org/project resource | `KILL_NO_CAPABILITY_DELTA` |
| Behavior is the documented purpose of the feature/configuration | `KILL_BY_DESIGN` |
| Strongest effect is confined to a documented demo, sample, quickstart, local-development server, or development preview below the program impact ceiling | `KILL_NON_PRODUCTION_TARGET` |
| Exact component is archived, unmaintained, source-only, or lacks the live deployment proof required by the program | `KILL_NO_PRODUCTION_REACHABILITY` |
| Same local user/operator controls the resolver, workdir, unrestricted process, or self-hosted boundary the feature does not promise to resist | `KILL_THREAT_MODEL` |
| Same root cause was public, previously reported, known, fixed, or already under remediation | `KILL_KNOWN_OR_DUPLICATE` |
| Only DEBUG/operator opt-in exposes the value and role separation is unproven | `INFORMATIVE_LIKELY` |
| Credential value shown but effective protected action is unproven | `IMPACT_GATE_BLOCKED` |
| External consumer/trust policy is hypothetical | `IMPACT_GATE_BLOCKED` |
| Correctness mismatch has no protected downstream consumer | `INFORMATIVE_LIKELY` |
| Parser/resolver mismatch reaches only an equivalent supported operation or configured locked trust set | `KILL_NO_CAPABILITY_DELTA` |
| Signed/shareable state is readable or replayable but only integrity/reconstruction is promised | `KILL_BY_DESIGN` |
| Credential-bearing configuration position is accepted but official support and realistic use remain disputed | `IMPACT_GATE_BLOCKED` |
| Hostile configured source can already supply equivalent package/build inputs | `KILL_TRUSTED_DOMAIN` or `KILL_NO_CAPABILITY_DELTA` |
| Temporary-state collision requires unknown exact keys and rare victim state with no discovery channel | `IMPACT_GATE_BLOCKED` |
| Malformed input reaches the same state as a permitted well-formed input | `KILL_NO_CAPABILITY_DELTA` |
| Permission blocks final data traffic but explicitly permits control-plane connectivity checks | `KILL_BY_DESIGN` |
| Proposed mitigation leaves the same attacker able to replace the trust root or use an equivalent channel | `KILL_NO_CAPABILITY_DELTA` |
| Best concrete severity is below current written program floor | `KILL_PROGRAM_SEVERITY` |
| Only localhost/synthetic mechanism and patched difference are proven | `IMPACT_GATE_BLOCKED` |
| Race requires a curator-only lock or unmeasured exact overlap | `IMPACT_GATE_BLOCKED` |
| Remote/native loading depends on disputed uncommon host prerequisites | `IMPACT_GATE_BLOCKED` |
| User explicitly enables the active-content/unsafe mode and no isolation promise is shown | `KILL_BY_DESIGN` |
| Contributor controls an equivalent executable build input | `KILL_NO_CAPABILITY_DELTA` |
| Claimed revocation event does not promise invalidation of the surviving credential/object | `KILL_BY_DESIGN` |
| Later policy is forward-looking and the actor exercises authority validly issued beforehand within its signed bounds | `KILL_BY_DESIGN` |
| Derived credential was already obtainable during valid parent authority and no lineage revocation promise is proven | `IMPACT_GATE_BLOCKED` or `KILL_NO_CAPABILITY_DELTA` |
| Two operation signatures intentionally authorize different field scopes | `KILL_BY_DESIGN` |
| Local profile editor can already read and use the adjacent cached credential | `KILL_THREAT_MODEL` |
| Old and new snapshots contain untrusted input from the same principal under the same token authority | `KILL_NO_CAPABILITY_DELTA` |
| Authentication-derived header reaches a wrong peer but protected-peer acceptance is unproven | `IMPACT_GATE_BLOCKED` |
| Remote-controlled output causes only an explicit local file effect with no protected consumer | `INFORMATIVE_LIKELY` |
| Uninitialized value is detected but no protected bytes reach an attacker-observable sink | `IMPACT_GATE_BLOCKED` |
| Specialized library callback mismatch has no shipped security-policy consumer | `IMPACT_GATE_BLOCKED` |
| Security-sensitive drift exists only in incomplete generated example code with no deployed consumer | `IMPACT_GATE_BLOCKED` |
| Local proof omits a production middleware, hosting, browser, or consensus layer that can change the result | `KILL_ENVIRONMENT_MISMATCH` |
| N/A was caused only by procedural inactivity or an unanswered Needs More Info request | `IMPACT_GATE_BLOCKED`; not technical negative evidence |
| A target was vulnerable at submission time but patched before later reproduction | preserve dated submission-time evidence; reassess prior knowledge and policy |
| Single-node acceptance cannot become canonical or final under independent validation | `KILL_ENVIRONMENT_MISMATCH` |
| Browser capability delta omits the exact same-URL top-level navigation or redirect control | `IMPACT_GATE_BLOCKED` |
| User approved an attacker endpoint and no per-hop redirect isolation promise exists | `KILL_TRUSTED_DOMAIN` or `KILL_BY_DESIGN` |
| Terminal consequence is an impact class explicitly excluded by the program | `KILL_PROGRAM_SEVERITY` |
| Claimed privacy expands beyond the exact fields covered by the product promise | `KILL_BY_DESIGN` |
| Same technically valid root cause was already submitted or tracked | `KILL_KNOWN_OR_DUPLICATE` for bounty eligibility; preserve technical validity |
| Untrusted code executes only inside a program-excluded updater sandbox and uses intended dependency resolution | `KILL_PROGRAM_SEVERITY` unless an eligible outer boundary is crossed |
| SDK returns an explicitly unverified identity and only a synthetic consumer treats it as authenticated | `IMPACT_GATE_BLOCKED` |
| Plaintext proxy routing differs but no protected transport or interface-isolation promise exists | `KILL_THREAT_MODEL` |
| Caller constructs an unusual library lifecycle or process descriptor state that a remote actor cannot trigger | `KILL_THREAT_MODEL` |
| A niche CI build configuration has no current shipped or production consumer | `KILL_NO_PRODUCTION_REACHABILITY` |
| Changed project or MCP configuration is explicitly reapproved inside a trusted workspace and no finer authorization-server binding is promised | `KILL_TRUSTED_DOMAIN` |
| An attacker-controlled resolved dependency already has build-time code execution equivalent to the metadata effect | `KILL_NO_CAPABILITY_DELTA` |

## What can overturn an Informative-likely result

Retain a lane only when new evidence establishes at least one real boundary not
present in the negative control, such as:

- a lower-privilege principal cannot obtain the identity/secret/action through
  any intended route, but the exploit grants it;
- execution or credential forwarding happens before trust or outside the scope
  of the user's consent;
- a distinct official/trusted artifact is overwritten and automatically
  consumed under higher authority;
- a program-controlled production consumer makes an unauthorized signing,
  release, authentication, authorization, or secret-access decision;
- a shared-role action crosses into a resource or secret the role is explicitly
  denied from modifying or using;
- an actual protected recipient accepts a credential and returns data or performs
  an action unavailable to the attacker beforehand;
- the concrete supported impact meets the current program severity threshold.

## Final decision sequence

1. Verify current scope, severity floor, excluded impacts, and report-readiness requirements.
2. Freeze starting authority and trust/consent facts.
3. Name the protected asset/action, promised security property, and control- or
   data-plane scope.
4. Enumerate equivalent intended paths and well-formed equivalent inputs.
5. Prove default or realistic server conditions and collision feasibility.
6. Test the proposed defense counterfactually under the same attacker authority.
7. Freeze authorization issuance time, derived-credential lineage, and temporal
   trust equivalence.
8. Verify production stack equivalence and, for distributed systems, canonical consensus.
9. Run the exact equivalent-path control, including top-level navigation when relevant.
10. Prove the effect reaches a real protected consumer.
11. Reproduce the technical transition safely.
12. Prove the resulting authority with authoritative read-back.
13. Calculate the capability delta.
14. Compare against the negative-control corpus and classify its adjudication basis.
15. Assign a fail-closed gate verdict.

Never report because a mechanism is clever, a patch exists, or a local PoC says
`PASS`. Report only when the program-recognized security impact also passes.
