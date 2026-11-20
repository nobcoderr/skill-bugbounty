# Credential Exposure to Effective Capability Method

## Contents

1. Public prior-art lessons
2. Security model and lifecycle
3. Scope and safety decision tree
4. Evidence collection without propagation
5. Validity, identity, and effective-permission proof
6. Proof levels and severity
7. Prior-art and KILL rules
8. Containment and regression tests

## Public prior-art lessons

### Mozilla Slack to Jira administrative credential

The historical public case [HackerOne #2467999, “Jira Credential Disclosure within Mozilla Slack”](https://hackerone.com/reports/2467999) provides a useful evidence pattern:

`authorized NDA contributor -> internal Slack channel -> shared script -> hard-coded Jira API credential -> principal/group evidence -> Jira administrative capability -> report -> credential revocation and artifact deletion`

Use only the generalized pattern. Never retain or reproduce the disclosed credential.

The report's disposition is a critical scope lesson: Mozilla moved the report to no structured scope and described it as out of scope, then paid a discretionary bounty because of the impact. That is a **scope exception**. A payout is not scope precedent, does not authorize future Slack searches, and does not authorize credential use against Jira or another SaaS control plane.

The historical report supports these distinctions:

- an authorized internal audience can still expose a high-value secret to more principals than intended;
- a hard-coded credential in a shared script can bridge collaboration access into an unrelated administrative control plane;
- role/group evidence can establish material privilege without reading sensitive project content;
- rapid revocation is more important than maximizing exploit depth;
- deleting the shared artifact reduces exposure but does not prove residual copies are gone.

Treat the exact report as public prior art and a duplicate. Search only for distinct current exposures on explicitly authorized surfaces.

### Mozilla Slack to Mastodon staging administrative token

The historical public case [HackerOne #2137154, “Mozilla Mastodon Staging
Instance Admin API Key Disclosure Through Slack”](https://hackerone.com/reports/2137154)
adds an environment-, endpoint-, and privacy-sensitive pattern:

`authorized NDA/staff Slack access -> trust-and-safety channel -> exposed bearer token -> Mozilla Mastodon staging instance -> GET /api/v1/admin/accounts -> administrative account data including email/IP fields -> report -> rotation -> old token rejected -> resolved`

According to the public transcript supplied by the user, Mozilla triaged the
report, moved the scope to none, rotated the token, resolved the report, and
rated it High because the affected instance was staging. Mozilla paid a bounty
and bonus while stating that Mastodon was out of scope and might be included in
the program later. “Will be included” is not current authorization, and a bonus
for an exception is not scope precedent.

The current Mastodon documentation provides the crucial falsifier. Listing
administrative accounts requires a user token with `admin:read:accounts` and
the `Manage Users` permission. Mutating or deleting accounts uses separate
write scopes such as `admin:write:accounts` and may require a different role
permission. Therefore:

- the historical successful list call established a real confidentiality boundary for that staging instance and that endpoint;
- the response schema can contain email and IP data, so continued pagination or copying the response creates unnecessary privacy harm;
- one successful read endpoint does not prove account creation, password changes, deletion, or every other documented administrator action;
- documentation establishes possible operations and required scopes, not that the leaked token possessed every scope or effective permission;
- staging is not production and should reduce claims accordingly, but staging is not automatically harmless if it contains real user identities, personal data, trusted integrations, or a production bridge;
- a post-rotation authentication failure is useful revocation evidence only when the retest itself is explicitly authorized; prefer vendor confirmation and audit logs;
- token rotation does not remove the Slack message, attachments, exports, bot previews, local downloads, logs, screenshots, or reports that may contain the token or returned personal data.

The historical report also demonstrates an evidence-handling failure mode: the
API response containing email addresses and IP addresses required later
redaction. For new work, use `PII_EXPOSED_STOP` immediately when third-party
personal data appears. Do not paste the response into the report body. Preserve
only endpoint, timestamp, record count range if safe, field names, response
fingerprint, and vendor confirmation through the program's approved secure
channel.

Treat #2137154, its Slack artifact, token lineage, staging endpoint, and rotation
as resolved public prior art and a duplicate. A new candidate requires a
distinct currently authorized artifact, credential, instance, and protected
capability.

### Mozilla Common Voice container image to AWS and database credentials

The user-supplied public HackerOne transcript for the historical report titled
“two aws access key and secret key and database username and password exposed”
provides another container-specific pattern. Its exact HackerOne report ID was not independently
identified, so do not invent one or present the transcript as a current scope
statement:

`public Docker Hub image -> mutable latest tag -> immutable image/layer -> /code/scripts/test/config.json -> two AWS access-key pairs plus database credentials -> vendor confirms AWS authentication -> image deletion plus credential rotation and AWS user removal`

The report says Mozilla validated that the AWS keys authenticated, removed the
affected Common Voice images, rotated the credentials, and removed the unused
AWS users. It also says Common Voice was out of scope and the bounty was a
critical-impact exception. Treat the exact image, file path, credential lineage,
and root cause as resolved public prior art. Do not pull an old image, search
mirrors, recover deleted layers, or replay any credential to reproduce it.

This historical case adds several durable distinctions:

- a public image can distribute a secret far beyond the source repository or intended build audience;
- `latest` is a mutable discovery pointer, not evidence identity; preserve the repository, platform, manifest/image digest, layer digest/index, and in-layer path available at the time of authorized observation;
- two AWS access-key IDs and two secret access keys must be tracked as two correctly bound pairs; never mix components, retain raw values, or infer validity from an ID alone;
- temporary AWS credentials additionally require the matching session token;
- database username and password exposure is separate from AWS impact and still requires evidence for endpoint, environment, network reachability, database identity, and effective role;
- “the AWS users were not used” means no observed use in the vendor's evidence window, not that the credentials lacked capability or that the exposure was harmless;
- image deletion, tag deletion, registry-blob cleanup, credential rotation, AWS user removal, and database-password rotation are different containment actions;
- deleting a file in a later filesystem layer may leave its bytes recoverable from an earlier layer, so a clean rebuild and retained-layer review matter.

For current work, search for a distinct authorized digest and a distinct live
credential lineage. A stale tag, a removed historical image, a revoked key, or
the same configuration path without new effective capability is `KILL`.

### Mozilla public CI log to a selected-site Netlify token

The user-supplied public transcript titled “Netlify Authentication Token
Exposed in Public Mozilla CI Logs” describes a resolved 2024-2025 lineage. A
public index corroborates the title, reporter, resolved status, disclosure date,
and critical label, but no stable HackerOne report ID was independently
identified; do not invent one. Use the title and dates for duplicate screening:

`public Taskcluster live.log -> Netlify authentication token echoed by an application task -> accepted bearer credential -> Developer principal -> selected crash-pings site -> possible site deploy/configuration authority -> token revocation and CI-log remediation`

Mozilla's official crash-ping lifecycle documentation independently confirms
the operational bridge: crash-ping ingestion is scheduled with Taskcluster,
Netlify CLI authentication is used in the workflow, and the crash-pings website
is hosted at `https://crash-pings.mozilla.org`. This supports the architecture;
it does not reveal a credential or prove that a historical token remains valid.

Preserve these evidence corrections from the public transcript:

| Historical evidence | What it supports | What it does not support |
|---|---|---|
| token text appeared in a public `live.log` | public artifact exposure if the exact task/run/log identity and anonymous access were observed | a Taskcluster platform vulnerability by itself |
| accepted `GET /api/v1/accounts` response | validity at observation time and access to returned account metadata | every account, every team action, or current validity after revocation |
| response field `role: Developer` | the principal's assigned role in that response | Owner, Billing Admin, Publisher, Reviewer, or Content Editor authority |
| `site_access: selected` plus one `selected_access_site_ids` entry | resource-scoped access to the selected site | team-wide access or control of every Mozilla/Netlify site |
| `roles_allowed` lists several role names | roles the account/product can make available in that context | roles assigned to the leaked-token principal |
| successful function-list request | read access to existing function/deploy metadata for the selected site | function upload, deploy creation, production publication, invocation, environment-variable access, or deletion |
| Netlify API/CLI documentation permits deploys and functions | the product has those operations and documents their protocol | that this token passed each write authorization check |
| vendor analysis that malicious replacement deployment may be possible | a credible selected-site integrity impact pending exact capability confirmation | a completed site takeover or full Netlify-team compromise |

Current Netlify documentation says Developers can manage site deploys and site
configuration, while Owners can restrict Developers to specific sites. That is
strong product-model context for the historical `Developer` plus `selected`
fields, but runtime token evidence or vendor confirmation is still required for
the exact write capability. `roles_allowed` must never be rewritten as “the
token had all these roles.”

Keep the execution boundary exact. If an explicitly authorized and controlled
proof establishes that this principal can deploy a serverless function, the
code runs in a Netlify-managed function runtime for the selected site. Call it
provider-hosted function deployment or code execution. Do not call it RCE on
Mozilla's Taskcluster service, Mozilla application servers, or the CI runner
without a separate path and proof. Function access to site environment values,
connected data, internal networks, or other secrets also requires separate
evidence; documentation or the existence of an old function is insufficient.
In short, provider-hosted execution is not automatically RCE on the CI service.

Mozilla's public response provides the scope/root-cause lesson: Taskcluster was
the log carrier and build/test ecosystem, while the vulnerable behavior was the
application task configuration or command invocation that echoed the Netlify
token. The affected authority was the selected `crash-pings.mozilla.org`
Netlify site. Do not assign a leak to the log-hosting platform merely because it
served the bytes.

The strongest safe current proof plan is:

1. identify one explicitly authorized CI task/run/job/step and its raw plus rendered log without downloading unrelated logs;
2. prove the log's audience using an anonymous negative-control session, then retain only metadata and a one-way token fingerprint;
3. request vendor-side confirmation of current validity, assigned role, team/site binding, `site_access`, and selected-resource list;
4. separate read evidence (`accounts`, site, deploy, or function metadata) from write evidence (create deploy, publish, upload function, edit configuration, or delete);
5. if write proof is required, use only a vendor-operated or explicitly authorized disposable site/canary, capture the provider audit event and authoritative read-back, and clean it up;
6. never deploy to `crash-pings.mozilla.org`, upload a function, read environment values, alter billing, delete a site, or enumerate the account merely to maximize impact.

The following historical impact upgrades are unsupported and must be killed
unless separately proven: all-role/full-account access from `roles_allowed`,
Owner or Billing Admin authority, payout diversion, all-site deletion,
irreversible loss of the Netlify team, environment-secret access, RCE on
Taskcluster or Mozilla servers, and compromise of assets outside the selected
site. Selected-site content/configuration integrity is the material boundary;
provider-hosted function execution is a distinct downstream capability.

Containment must keep these actions separate:

- revoke the exposed token and invalidate derived authorization where applicable;
- audit Netlify account, site, deploy, function, configuration, and token events for the exposure window;
- remove or redact the secret from raw/rendered logs, downloadable artifacts, mirrors, caches, previews, indexes, and retained support copies;
- fix the exact task command/configuration so authentication values cannot be echoed through normal, verbose, debug, error, or retry output;
- reduce the principal to the smallest site and action set, and prefer short-lived workload identity when the provider supports it;
- add a synthetic-canary CI regression proving that raw logs, rendered logs, downloadable artifacts, and failure paths redact the canary without printing it in alerts.

Treat this exact Mozilla/Taskcluster/Netlify/crash-pings token lineage as
`PUBLIC / FIXED / DUPLICATE`. A new finding requires a distinct current log,
credential, resource binding, effective capability, allowed validation path,
and root cause. The historical out-of-scope payment and bonus are exceptions,
not future scope or testing authorization.

## Security model and lifecycle

Model the complete lifecycle:

`issue -> store/inject -> build or task command -> stdout/stderr/artifact/image layer -> redact/publish/tag -> mirror/cache/index/pull -> discover -> validate -> use -> rotate/revoke -> redact/delete/garbage-collect/rebuild -> residual copies`

At each stage record:

| Stage | Required question |
|---|---|
| Issue | Which issuer created the credential, for which principal and environment? |
| Store | Was it meant for a secret manager, environment injection, user vault, or service configuration? |
| Embed | Which script, source file, notebook, screenshot, log, document, package, image config, or filesystem layer contains it? |
| CI publish | Which provider, task/run/job/step, raw or rendered stream, artifact, redactor, public audience, retention policy, mirror, cache, or index exposed it? |
| Share | Which exact audience can access the artifact, and is that audience authorized? |
| Identify | What immutable digest, platform manifest, layer index/digest, and in-layer path identify the bytes rather than only a mutable tag? |
| Discover | Was discovery passive and within written scope? |
| Validate | Is any use of the secret explicitly allowed, or must the vendor validate it? |
| Capability | What identity, tenant, environment, exact endpoint/action, scope, role, policy condition, and protected action are actually effective? |
| Privacy | Can a response contain third-party email, IP, message, account, or other personal data, and what immediate stop/redaction rule applies? |
| Revoke | Was the original value invalidated, not merely removed from one artifact? |
| Residual | Do history, exports, caches, forks, logs, packages, backups, and local copies remain? |

Common exposure sources include repositories and Git history, public/private CI raw and rendered logs, job summaries, downloadable CI artifacts, build outputs, environment dumps, package registries, Docker/OCI image configs and layers, exported image archives, registry caches and mirrors, documentation, notebooks, gists, issue trackers, support bundles, screenshots, paste systems, Slack/Teams/chat files, and bot-generated previews.

### Container-image identity and lower-layer model

For an authorized Docker/OCI artifact, record:

1. registry and repository;
2. tag as observed, while treating it as mutable;
3. media type and multi-platform index/manifest-list digest when present;
4. selected operating-system/architecture platform manifest digest;
5. image config digest;
6. ordered layer digests and the exact layer containing the path;
7. in-layer path, file metadata, and a fingerprint of the redacted secret-bearing content;
8. acquisition time and the explicit authority that permitted the pull or inspection.

Container filesystems are unions of ordered layers. A later whiteout or file
replacement affects the assembled view but does not retroactively erase bytes
from an earlier blob. Therefore, “the file is absent from the running image” is
not a sufficient negative control. Inspect only the authorized immutable
artifact and its retained layers; do not enumerate a registry or recover
historical/deleted blobs without explicit permission.

## Scope and safety decision tree

Before inspecting content:

1. Is the repository, channel, workspace, ticket system, artifact store, registry/repository, exact image, or package explicitly in scope?
2. Does the researcher have authorized access to this exact location?
3. Does the policy allow searching files/messages or only testing named products?
4. Does the policy permit validating leaked credentials, or require immediate reporting without use?
5. Is the downstream provider first-party and in scope, or a third-party SaaS boundary?
6. What rate, privacy, data-access, and stop rules apply?
7. Does authorization cover pulling the image, resolving a tag to a digest, reading layers, checking mirrors/caches, authenticating to AWS, or connecting to a database? Treat these as separate permissions.

Decision:

- **Artifact access unauthorized:** `KILL / BLOCKED`; do not inspect or search.
- **Artifact access authorized, credential use not authorized:** fingerprint, report, and request vendor-side validation/revocation.
- **Credential validation explicitly authorized:** use the least-invasive allowed method and stop at sufficient proof.
- **Unexpected data or privilege appears:** stop, preserve minimal metadata, notify the program, and do not continue.
- **Third-party personal data appears:** set `PII_EXPOSED_STOP`, stop pagination and follow-on calls, do not paste the response into ordinary evidence, and request vendor-side secure handling/redaction.
- **Credential already revoked:** record containment; do not seek another copy or adjacent live token.
- **Historical image removed:** do not search mirrors, caches, third-party archives, or pulled clients for a replacement copy unless the program explicitly authorizes that exact residual-exposure audit.

Internal membership, NDA status, employee/contributor status, or accidental access does not broaden the program's written scope. Historical bounty decisions do not change this rule.

## Evidence collection without propagation

Never store the raw credential.

Preserve only:

- artifact identifier and authorized location, including immutable digest and platform when applicable;
- CI provider plus exact task/run/job/step, raw/rendered log form, access-control observation, publication time, and retention/cache metadata when applicable;
- container manifest/config/layer metadata and secret-bearing path, without raw secret bytes;
- message/file/commit/package metadata;
- discovery timestamp and timezone;
- audience classification and access precondition;
- credential family and issuer confidence;
- a one-way cryptographic fingerprint generated in a local controlled context;
- a heavily redacted prefix/suffix only if the vendor needs it to locate the secret;
- vendor confirmation, audit-event identifier, or sanitized capability metadata;
- privacy status (`NO_PII_SEEN`, `PII_EXPOSED_STOP`, or `VENDOR_REDACTED`) and sanitized field-level description rather than response contents;
- revocation timestamp and confirmation;
- residual-copy inventory.

Do not place a live credential in shell history, command-line arguments, process listings, Docker build arguments, image environment metadata, layer history, exported archives, screenshots, copied chat messages, AI prompts, test fixtures, issue titles, URLs, or ordinary ticket comments. Use the program's approved secure disclosure channel for any unavoidable transfer.

Evidence labels:

- `NOT_RETAINED` — the value was not copied out of the original authorized view;
- `FINGERPRINT_ONLY` — only a one-way fingerprint remains;
- `REDACTED` — limited identifying characters remain with written justification;
- `RAW_PRESENT` — unsafe evidence state; stop distribution and coordinate secure removal.

## Validity, identity, and effective-permission proof

### Distinct proof questions

Answer each independently:

1. **Authenticity:** Is the value structurally consistent with the claimed issuer and context?
2. **Current validity:** Does the issuer currently accept it? Only test when explicitly authorized.
3. **Principal:** Which user, app, service account, bot, or integration owns it?
4. **Environment:** Production, staging, sandbox, test, or an unrelated tenant?
5. **Declared scope:** Which scopes, roles, groups, grants, or policy documents describe authority?
6. **Effective permissions:** Which protected operation is actually authorized after tenant, object, conditional, and downstream policy checks?
7. **Impact:** What confidentiality, integrity, identity, control-plane, release, or operational boundary exceeds the researcher's starting authority?

Do not infer effective permissions from token format, account name, role label, group name, documentation, or UI alone. A group such as “administrators” is strong context, but scope conditions and downstream policy may still reduce authority.

### OAuth/bearer admin API endpoint and environment proof

Build a per-endpoint permission matrix rather than treating “admin token” as a
single unlimited capability:

| Evidence | Establishes | Does not establish |
|---|---|---|
| token format or `Bearer` header | likely credential family | validity, principal, instance, scopes, or permissions |
| declared OAuth scope | authority requested or granted in metadata | that every role/policy condition permits the action |
| successful authorized `GET` | effective read capability for that endpoint and response | write/delete authority or unrelated admin routes |
| API documentation for a write route | required scope and product capability | possession of that scope or successful authorization by the leaked token |
| vendor-confirmed rotation | old credential was invalidated at the checked boundary | residual copies, derived sessions, or unrelated tokens are gone |

For a SaaS team/account response, record assigned role and resource restriction
as independent fields. A list such as `roles_allowed` describes role options or
assignment policy, not the current subject's effective roles. Likewise,
`site_access: selected` and `selected_access_site_ids` constrain the resource
set even when the assigned role can normally manage deployments. Build a token
x team x selected site x endpoint x action matrix before naming impact.

For deployment providers, distinguish four boundaries:

1. metadata read from the control-plane API;
2. selected-site content or configuration mutation;
3. code execution in the provider-managed build/function runtime;
4. code execution in the source CI service or customer's own server.

Proof of an earlier boundary never automatically proves a later one.

For staging, record whether accounts and data are synthetic, copied from
production, generated by employees/testers, or unknown. Also record network and
identity trust into production, shared OAuth clients/secrets, shared storage,
and operational integrations. Use `STAGING_REAL_DATA`, `STAGING_SYNTHETIC`, or
`UNKNOWN`; do not silently relabel staging as production or dismiss real PII as
test data.

### AWS and database credential binding

Treat each credential family as a separate evidence object:

| Family | Components | What presence proves | What remains unproven |
|---|---|---|---|
| AWS long-term access key | one access-key ID plus its matching secret access key | a structurally complete pair | current validity, AWS account/principal, policy conditions, and effective actions |
| AWS temporary credential | access-key ID, secret access key, and session token | a structurally complete session credential | expiry, session principal, boundary policy, and effective actions |
| Database credential | username plus password, normally with endpoint/database/TLS context | a potential authentication pair | live endpoint, network reachability, environment, database identity, role, and accessible objects |

Do not cross-pair multiple key components. Store pair labels and separate
fingerprints, never the values. AWS documents that an IAM access key has an
access-key ID and secret access key that are used together. An identity-only
AWS result, when vendor-performed or explicitly authorized, establishes account
and ARN but not effective service permissions. Database connectivity or query
execution is not an implicit proof step; request vendor-side validation unless
the exact database and minimum method are explicitly authorized.

### Least-invasive validation hierarchy

Use the first sufficient and authorized option:

1. vendor/triage confirmation of validity, principal, and privilege;
2. vendor audit logs or incident-response evidence;
3. offline signed metadata or configuration binding that exposes no protected data;
4. issuer self/introspection response limited to the credential's own identity and scope;
5. one harmless read-only check against a researcher-owned or vendor-provided canary;
6. a reversible owned-object action only if the policy explicitly requires and permits it.

Do not authenticate with a disclosed credential merely because an API endpoint is read-only. Authentication itself can be unauthorized access and can create audit, legal, and privacy impact.

For AWS, do not interpret an identity-only response as permission enumeration.
For databases, do not list schemas, tables, rows, users, extensions, or grants.
Prefer the vendor's IAM policy simulator, access analysis, CloudTrail evidence,
database audit logs, or a sanitized administrator statement over researcher
replay. The historical Common Voice report's vendor confirmation is evidence
for that incident only, not authorization to repeat its validation method.

### Minimum sufficient proof

For an administrative credential, material impact can often be established with:

- current validity or vendor confirmation;
- principal and environment binding;
- scope/role/group or policy evidence;
- one protected capability or vendor statement confirming administrative authority;
- the contrast between the researcher's starting access and the credential's authority.

Do not enumerate projects, users, accounts, issues, groups, secrets, integrations, or configuration after sufficient privilege is established. Do not paginate an administrative list or preserve email/IP payloads. “Maximum PoC” means maximum certainty with minimum operational and privacy impact, not maximum access.

## Proof levels and severity

| Level | Evidence | Maximum verdict |
|---|---|---|
| E0 | Secret pattern or scanner hit only | WEAK |
| E1 | Exact authorized artifact and audience exposure proven; for containers, immutable digest/platform/layer/path recorded | WEAK |
| E2 | Issuer/type/environment and multi-part credential binding supported by context | MEDIUM |
| E3 | Current validity proven by an explicitly authorized method or vendor | MEDIUM |
| E4 | Principal plus declared scopes/roles/groups proven | MEDIUM |
| E5 | Effective protected capability and authority gain proven safely | STRONG candidate |
| E6 | Scope, current path, prior-art clearance, controls, manual confirmation, containment, and residual-copy status complete | STRONG + MANUALLY_CONFIRMED |

Score impact from the combination of:

`audience breadth x immutable artifact reach/distribution x current validity x principal privilege x effective permission x environment x protected resource sensitivity x exposure duration x revocation/residual risk`

Do not set severity from a token prefix, `AWS`, `database`, “admin” label, `roles_allowed`, or theoretical maximum. Distinguish internal-channel exposure from a public CI log or public image, a single observed pull from broad distribution, identity proof from effective service permissions, database credential completeness from reachable production access, one successful read endpoint from unproven write/delete/deploy operations, selected-site Developer access from Owner/team-wide access, provider-hosted function execution from CI/application-server RCE, staging with real PII from production and synthetic test data, one project from site administration, and test from production.

Recommended controls:

- baseline: same protected resource without the credential or with an owned low-privilege credential;
- negative control: random/expired/revoked token or a forbidden owned object, only when such testing is permitted;
- positive proof: one minimum authorized capability result;
- authoritative read-back: vendor log, policy result, or owned-object state;
- abort: third-party data (`PII_EXPOSED_STOP`), unexpected privilege, mutation, pagination, instability, scope drift, or rate-limit behavior;
- cleanup: revoke/rotate, delete owned canary changes, remove local secret material, and document residual copies.

Container-specific negative controls include a rebuilt synthetic image whose
assembled filesystem and every retained layer omit a canary secret, and a
registry response that resolves the remediated tag to a new digest. Never use a
live secret as a canary. A missing file in the final root filesystem alone is
not a sufficient control.

## Prior-art and KILL rules

Search before deep validation:

- exact artifact path, filename, message title, registry/repository, tag, immutable digest, layer digest/index, integration name, principal, and sanitized fingerprint;
- open/closed issues and PRs, merged fixes, security advisories, CVEs, commits, blame, secret-removal history, changelog, releases, docs, known issues, incident notes, and maintainer comments;
- public reports for the same leak, same principal, same token family, same artifact, and same missing secret-management invariant.

KILL when:

- the surface, access path, search method, or token validation is unauthorized;
- the credential is fake, placeholder, example, expired, revoked, public-by-design, or has no sensitive capability;
- only a scanner match, format match, source line, HTTP status, group label, or screenshot exists;
- the candidate requires reading third-party data or performing mutations to prove impact;
- the exact exposure or root cause is known, fixed, duplicate, or the token was already rotated;
- the candidate is HackerOne #2137154 or the same resolved Mastodon staging token, Slack artifact, endpoint, or credential lineage;
- the candidate is the resolved “Netlify Authentication Token Exposed in Public Mozilla CI Logs” lineage or merely replays its Taskcluster `live.log`, selected crash-pings site, token, or command-echo root cause;
- only the historical Common Voice image/configuration lineage remains, or the candidate depends on recovering a deleted public image from an unauthorized mirror/cache;
- scope relies on a historical exception, discretionary payment, NDA, or implied trust;
- effective authority does not exceed the researcher's starting privilege.

## Containment and regression tests

Prioritize response in this order:

1. revoke or rotate the credential;
2. invalidate derived sessions, refresh tokens, application passwords, or cached grants;
3. review issuer, SaaS, Netlify account/site/deploy/function, CI task, cloud control-plane, CloudTrail, database, identity-provider, Mastodon, and downstream audit logs for use; treat **No observed use** as a monitoring result, not proof that the exposed capability was harmless;
4. remove the artifact from the primary location and accessible history;
5. for containers, delete affected tags/manifests according to registry semantics, expire retained blobs, purge authorized caches/mirrors, and rebuild from a clean context; verify lower layer and multi-platform variants independently;
6. locate Slack/chat history, attachments, exports, bot previews, local downloads, screenshots, report copies, caches, forks, packages, build logs, container layers, image archives, registry mirrors, pulled copies, backups, and local copies; securely redact or delete unnecessary PII-bearing evidence;
7. reduce the principal to least privilege and replace long-lived secrets with short-lived workload identity where possible;
8. move secret injection to an approved secret manager or ephemeral build secret mount; never use Dockerfile `ARG` or `ENV` for secrets because those values can persist in the final image or metadata;
9. add pre-commit, CI raw/rendered-log, failure-path, downloadable-artifact, container-layer, registry, and collaboration-upload secret detection with a verified incident-response path;
10. test CI log redaction with a synthetic canary across normal, verbose, error, and retry output; confirm public/download/cache copies do not contain it;
11. test credential rotation, AWS user removal where appropriate, database credential rotation, revocation propagation, image deletion, garbage collection, clean rebuild, and historical-artifact cleanup as distinct controls.

Regression tests should use synthetic canary secrets, never production values. Verify that commits, build contexts, image configs, every layer in every supported platform manifest, build artifacts, logs, package contents, chat uploads, bot previews, exports, and support bundles reject or quarantine the canary without exposing it in alert text. Verify both the assembled filesystem and lower layers, then confirm the published tag resolves to the expected clean immutable digest.

Remediation completeness matrix:

| Control | Proves | Does not prove |
|---|---|---|
| AWS key disabled/rotated | that credential no longer authenticates | image bytes are gone or another key is absent |
| AWS user removal | that principal was removed | no assumed roles, sessions, or related credentials remain |
| Database password rotated | old database pair is invalidated | cloud keys or image copies are removed |
| Tag/image deletion | normal discovery path is removed | lower blobs, mirrors, caches, pulled copies, or credentials are invalid |
| Blob garbage collection | registry-retained blob removal | third-party or client copies are gone |
| Clean rebuild with secret mounts | current build avoids secret persistence | every historical artifact was purged |
