# GitHub Actions Fork, Credential, and Supply-Chain Trust Method

## Purpose

Use this method for authorized audits where attacker-controlled pull-request
code or data may cross from an untrusted GitHub Actions run into credentials,
writable repositories, internal runners, artifacts, releases, registries,
signing, deployment, CDN publication, or downstream product updates.

The reusable root cause is not simply `pull_request_target`. It is:

`untrusted fork input -> executable/interpreted consumer -> credential channel -> effective protected capability`

## Authoritative platform model

- GitHub documents `pull_request` fork runs as untrusted: normally read-only
  `GITHUB_TOKEN`, no other repository/organization secrets, and fork approval
  protections.
- `pull_request_target` uses the base repository's trusted workflow context and
  may receive a read/write base-repository token and secrets. It is safe only
  while fork code and untrusted artifacts remain data and are not executed.
- Repository/organization secrets must be explicitly referenced by a workflow to
  become available to an action or step. Treat them as step-scoped/action-scoped
  channels, not all ambient environment
  variables. `GITHUB_TOKEN` is special: it is created per job and actions can
  access `github.token` even when the workflow does not explicitly pass it.
- Historical `actions/checkout` v4/v5 behavior persisted the authentication token
  in local Git configuration by default and removed it only during post-job
  cleanup. Code executed before cleanup could read/use that credential. Checkout
  v6 moved persisted credentials to a separate file under `$RUNNER_TEMP`; v7
  added safer fork-PR handling. Always analyze the pinned action version.
- npm runs lifecycle scripts by default during `npm ci` unless script execution
  is disabled or constrained. A fork-controlled `package.json`, dependency,
  local action, test, or build configuration can therefore be an execution sink.
- Steps in one job share the runner workspace. GitHub documents that an action
  can modify `GITHUB_WORKSPACE` content which subsequent actions can access.
  Therefore step-scoped secrets are insufficient isolation if a later
  secret-bearing step executes a file or dependency an earlier untrusted step
  could replace.

Primary references:

- GitHub `pull_request_target` security:
  https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
- GitHub secrets model:
  https://docs.github.com/en/actions/concepts/security/secrets
- GitHub `GITHUB_TOKEN` model:
  https://docs.github.com/en/actions/concepts/security/github_token
- GitHub Actions checkout:
  https://github.com/actions/checkout
- GitHub-hosted runner filesystem and shared workspace:
  https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- GitHub Security Lab pwn requests:
  https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/
- GitHub Security Lab untrusted input and credential residue:
  https://securitylab.github.com/resources/github-actions-untrusted-input/
- npm `ci` and lifecycle-script controls:
  https://docs.npmjs.com/cli/commands/npm-ci/

## Target and scope evidence card

| Field | Required evidence |
|---|---|
| Authorization | Named program/internal authorization and permitted test method |
| Repository | Owner/name, visibility, fork network, exact workflow path |
| Snapshot | Workflow commit, default branch, action SHAs/tags, date/time |
| Event | `pull_request`, `pull_request_target`, `workflow_run`, comment/review, reusable call |
| Actor | External fork, first-time contributor, collaborator fork, same-repo branch, Dependabot |
| Approval | Required/received/reused approval and rerun actor semantics |
| Workflow provenance | Base/default branch, PR merge commit, PR head, reusable workflow ref |
| Untrusted input | Code/ref/SHA, lifecycle script, local action, artifact, cache, event field, config |
| Runner | GitHub-hosted/self-hosted, ephemeral/reused, network and filesystem authority |
| Credentials | Explicit secrets, `GITHUB_TOKEN`, Git helpers/config, OIDC, CLI/cloud files |
| Effective permissions | Runtime token principal, repo scope, actions/contents/statuses/id-token permissions |
| Consumer | Branch push, PR review/comment, artifact/release, CDN, deploy, signer, updater |
| Restrictions | Live PRs, secret access, mutation, external callbacks, release/deploy prohibitions |

Missing fields are `DEFERRED`, not permission to assume them.

## Four-provenance model

Record these independently:

1. **Workflow definition provenance** — which trusted/untrusted branch supplies
   the YAML and reusable workflow.
2. **Code/data provenance** — which repository and exact SHA supplies files,
   artifacts, cache entries, action code, or event data.
3. **Execution provenance** — which step/action/interpreter turns that input into
   behavior.
4. **Authority provenance** — which job/token/environment/runner supplies the
   protected capability.

Use this table:

| Stage | Repository/ref/SHA | Controlled by | Representation | Executed or data-only? | Authority present | Evidence |
|---|---|---|---|---|---|---|
| Event | | | | | | |
| Workflow | | | | | | |
| Checkout/download | | | | | | |
| Install/build/test/action | | | | | | |
| Credential channel | | | | | | |
| Protected effect | | | | | | |
| Downstream consumer | | | | | | |

## Event and gate matrix

Do not reason from the trigger name alone.

| Event/actor | Workflow source | Default code source | Default secret model | Token expectation | Required runtime verification |
|---|---|---|---|---|---|
| `pull_request`, external public fork | PR merge/base workflow behavior | merge commit unless overridden | non-`GITHUB_TOKEN` secrets withheld | read-only maximum normally | actual permissions in run, approvals, repo settings |
| `pull_request`, same repo | PR-controlled workflow/code | PR branch/merge | secrets may be available | requested permissions may apply | actor already has repo write and exact privilege delta |
| `pull_request_target` | base default branch | base branch unless overridden | secrets available if referenced | base-repo token | whether fork code/artifact is fetched and executed |
| `workflow_run` privileged follow-up | base default branch | base unless downloaded | secrets/token available | privileged | provenance and validation of downloaded artifacts |
| issue/review/comment dispatch | base workflow | base unless fetched | depends on event | often privileged | untrusted expressions/ref selection and authorization gate |

For each gate record its position and failure behavior:

- collaborator/permission/association check;
- `head.repo.fork`, repository equality, actor allowlist, environment approval;
- whether failure stops the job or later steps use `if: always()`,
  `continue-on-error`, separate jobs, or independent triggers;
- whether reruns use the original actor, triggering actor, or changed code;
- whether approval covers only one commit or future pushes.

## Execution-consumer inventory

Require one real consumer:

- `npm ci/install`, `pip install`, `bundle install`, Maven/Gradle plugins,
  Cargo build scripts, Go generators, package prepare hooks;
- local action `uses: ./...`, composite action, Docker action, Makefile, test,
  linter, formatter, generator, or build configuration from the PR;
- inline shell expression using attacker-controlled event fields;
- downloaded artifact extracted, sourced, imported, executed, or interpreted;
- cache content loaded as executable package/tool/configuration;
- branch/ref/repository selection that lets the attacker substitute an action or
  base checkout;
- self-hosted runner persistence or internal-network access.

Static checkout without an execution/interpreter edge is not runner RCE.

## Credential-channel inventory

Inspect channels separately; never use `env | grep secret` as the proof model.

| Channel | Example | Reachability question | Common false claim |
|---|---|---|---|
| Explicit step `env` | `${{ secrets.X }}` | Is attacker code in the same step/process tree? | Later-step secret assumed ambient earlier |
| Action `with` input | token/password input | Is the action trusted and can attacker control its code or interpreted input? | Triggerability confused with action compromise |
| `github.token` context | JS action context | Does attacker control the action/local action? | Arbitrary shell assumed to get context automatically |
| Git credential persistence | checkout extraheader/helper/config | Which checkout version/path, and is it readable before cleanup? | Only checking process environment |
| Same-job workspace integrity | earlier code rewrites later script/tool/dependency | Does a secret-bearing step execute or interpret the modified object? | Step-scoped secret mistaken for process isolation |
| CLI/cloud login files | `.npmrc`, Docker, AWS, Azure, gcloud | Did a prior trusted step create residue in the same job? | Different job/runner residue assumed shared |
| OIDC request capability | request URL/token env plus `id-token: write` | Can attacker request a token and does trust policy accept its subject? | OIDC permission equated with cloud role |
| Command files | `$GITHUB_ENV`, output/state files | Can attacker write data consumed by a privileged later step? | Step isolation assumed complete |
| Artifact/cache | output from untrusted job | Is it validated as data before privileged use? | Artifact provenance equated with integrity |
| Self-hosted runner state | workspace, processes, credentials | Is the runner reused and what network/host authority exists? | GitHub-hosted behavior assumed identical |

Post-job deletion is not protection when attacker code runs before cleanup.
Log masking is not access control, and `***` does not prove what value entered the
attacker process.

## Token capability matrix

For every token record:

| Field | Evidence |
|---|---|
| Token kind | `GITHUB_TOKEN`, PAT, App installation token, OIDC-derived token |
| Principal | GitHub App installation/user/service identity |
| Issuing job/event | exact run/job and actor |
| Repository/org scope | exact accessible repositories/resources |
| Requested permissions | workflow/job YAML |
| Effective permissions | runtime header/API/vendor-side confirmation |
| Expiry/revocation | timestamps and invalidation event |
| Branch/ruleset limits | push, force-push, review, status, bypass behavior |
| Workflow-trigger semantics | whether token-generated push triggers deploy/publish |
| Protected capability | minimum read/mutation proven in owned fixture |

A stolen read-only token for a public repository may be a credential exposure but
may add no meaningful protected capability. A PAT reference later in the file is
not proof the PAT was present in the executing step.

## Safe owned-fixture proof

Never test a suspected vendor workflow by opening a malicious PR or sending its
credentials to OAST. Recreate the architecture using disposable repositories and
synthetic secrets.

1. Pin the candidate event, checkout/action version, permissions, and step order.
2. Use a researcher-owned base and fork plus a unique synthetic canary secret.
3. Prove execution with a deterministic marker that contains no credential.
4. Detect a credential channel without printing values; record only channel
   presence, origin path, and a one-way fingerprint of the synthetic fixture.
5. Prove exact token authority through a harmless owned canary action and
   authoritative read-back. Test write denial as well as success.
6. Run external-fork, same-repo, trusted-branch, and approval controls.
7. Run `persist-credentials: false`, scripts-disabled, pinned patched action, and
   data-only artifact controls.
8. If downstream impact is in scope, publish only to an owned dummy artifact/CDN
   path and prove the consumer read-back; never touch vendor releases.
9. Revoke synthetic tokens, delete branches/repos/artifacts, and document cleanup.

Do not store raw tokens, `.git/config` authorization values, runner diagnostic
archives, or OIDC tokens in evidence. Use sanitized structure, fingerprints, and
vendor-side validation for live findings.

## Evidence ladder and verdict

- **G0:** static event/checkout/permission/secret signature;
- **G1:** fork-controlled code executes in the expected job;
- **G2:** exact credential channel is reachable in an owned equivalent;
- **G3:** token principal and effective runtime permissions are proven;
- **G4:** a protected owned read/mutation succeeds with negative control;
- **G5:** a downstream owned release/deploy/consumer edge is proven;
- **G6:** current target scope, exact snapshot, novelty, repeated manual result,
  cleanup, and real production/release mapping pass.

Only G6 is `STRONG / MANUALLY_CONFIRMED`. G1 is runner RCE only. G2 is a
credential-access primitive. G3-G4 define actual security impact. G5 is required
before claiming a direct supply-chain compromise.

## Public prior art: DuckDuckGo privacy-configuration, 2026

The user supplied a public HackerOne transcript titled **“RCE + PAT Exfiltration
via pull_request_target in privacy-configuration/auto-respond-pr.yml — Direct
Supply Chain to All DDG Browsers”**, submitted March 21, 2026. No stable
HackerOne report ID was provided, so this method does not invent one.

### Historical source facts

At the report snapshot:

- `.github/workflows/tests.yml` used `pull_request`, explicitly checked out the
  fork repository/head in its lint job with `actions/checkout@v5`, then ran
  `npm ci`; a fork-controlled root `postinstall` could execute on the runner;
- the lint job requested `contents: write`, but requested permissions are not the
  same as effective external-fork permissions;
- `PRIVACY_CONFIG_PAT` appeared only in later commit/push and dispatch steps
  gated on `head.repo.full_name == github.repository`, excluding external forks;
- `.github/workflows/auto-respond-pr.yml` used `pull_request_target`, but its
  `auto_respond` job performed a collaborator permission check before checking
  out/running fork code; an external fork failed that gate under normal
  fail-closed step behavior;
- `sync_asana_on_close` passed `ASANA_ACCESS_TOKEN` and `GH_RO_PAT` to the trusted
  base-repository `duckduckgo/action-asana-sync@v11` action. It did not check out
  or execute fork code merely because the fork could trigger the event;
- PR #5002 added explicit `!head.repo.fork` conditions to the Asana and
  auto-response jobs. The diff is defense in depth and is not, alone, proof of
  the originally claimed exfiltration;
- the base-branch publication workflow built generated configuration and synced
  it to a tracker-blocking S3 path on pushes to main, but reaching that consumer
  still required proven write authority and workflow-trigger behavior.

### Vendor-confirmed primitive

Broad environment scraping was the wrong proof model. DuckDuckGo
clarified that repository/organization secrets were not present in the `npm ci`
step environment and the PAT-gated steps did not run for fork PRs. The vendor
nevertheless internally validated a different primitive close to the report:
`actions/checkout` had persisted the job's `GITHUB_TOKEN` in Git configuration,
so the malicious postinstall could access that specific token. DuckDuckGo later
treated the report as valuable/critical and rewarded it.

Methodology conclusions:

1. Preserve the validated root cause as:
   `fork PR -> checkout@v5 -> persisted Git credential -> npm postinstall -> job GITHUB_TOKEN exposure`.
2. Do not preserve `PRIVACY_CONFIG_PAT`, `ASANA_ACCESS_TOKEN`, or `GH_RO_PAT`
   exfiltration as confirmed facts.
3. Do not equate PR #5002 with exploitation evidence.
4. Do not infer write or all-browser supply-chain compromise without the actual
   fork-run token permissions, branch/ruleset behavior, push-trigger semantics,
   publication path, and consumer proof.
5. A later reward/severity decision does not eliminate the need to prove the
   exact boundary on a new target.
6. This exact DuckDuckGo lineage is `PUBLIC / FIXED / DUPLICATE`. New candidates
   require a distinct current repository/workflow/action version or incomplete
   fix with their own manual proof.

Official prior-art anchors:

- DuckDuckGo PR #5002:
  https://github.com/duckduckgo/privacy-configuration/pull/5002
- Historical repository:
  https://github.com/duckduckgo/privacy-configuration
- Checkout credential behavior:
  https://github.com/actions/checkout

## Public prior art: DuckDuckGo content-scope-scripts, HackerOne #3619287

The user supplied the public report **“RCE + Supply Chain Attack via
pull_request_target in content-scope-scripts/semver-label.yml — Affects All
DuckDuckGo Browsers”**, submitted March 21, 2026 and later triaged/resolved on
May 12, 2026. Keep the demonstrated execution primitive, possible credential
bridges, and claimed downstream impact as separate conclusions.

### Historical source and patch facts

At user-identified historical snapshot `b5066fbcf6`, the official workflow:

- used `pull_request_target` for opened, synchronized, and reopened PRs;
- requested `contents: read` and `pull-requests: write`;
- checked the trusted base SHA into `base/` and the PR merge ref into `pr/`;
- ran `npm install` and `npm run build` inside attacker-controlled `pr/`;
- declared `GITHUB_TOKEN` only in the later “Get PR source files” step;
- declared `ANTHROPIC_API_KEY` only in the later “Run semver analysis” step,
  which executed `node base/.github/scripts/semver-analysis.mjs`.

The immediate parent displayed for patch commit `eb01151209` is `11e2a57`, so
do not call `b5066fbcf6` the last pre-fix commit without an ancestry proof. The
patch added `!github.event.pull_request.head.repo.fork` to `semver-label.yml`
and three sibling privileged PR workflows. That diff establishes mitigation
scope, not by itself the exact secret reached or downstream capability.

Official anchors:

- Vulnerable snapshot:
  https://github.com/duckduckgo/content-scope-scripts/blob/b5066fbcf6/.github/workflows/semver-label.yml
- Mitigation commit `eb01151209` / PR #2659:
  https://github.com/duckduckgo/content-scope-scripts/commit/eb01151209
- Historical release trigger:
  https://github.com/duckduckgo/content-scope-scripts/blob/b5066fbcf6/.github/workflows/semver-release.yml
- Historical release workflow:
  https://github.com/duckduckgo/content-scope-scripts/blob/b5066fbcf6/.github/workflows/build.yml

### Evidence-accurate root-cause split

1. **Fork code execution — demonstrated/public prior art.** The source path is
   `fork PR -> pull_request_target -> PR merge checkout in pr/ -> npm lifecycle
   or build script`. The report later attached a uniquely tagged HTTP callback
   timestamped April 22 from an Azure address and linked it to test PR #2658.
   This is strong support for runner execution when correlated with the Actions
   run. IP ownership alone is not a substitute for a workflow run ID/log, and
   the callback contained no secret proof.
2. **Direct ambient Anthropic-key claim — incorrect model.** The build step did
   not receive `ANTHROPIC_API_KEY`; it was scoped to the later analysis step.
3. **Write-then-secreted-execute bridge — source-reachable candidate.** Earlier
   fork code ran on the same job filesystem and could in principle rewrite the
   sibling `base/.github/scripts/semver-analysis.mjs`; the later step executed
   that path with `ANTHROPIC_API_KEY`. This is the correct same-job workspace
   and cross-step workspace
   hypothesis. The supplied callback did not demonstrate a key value,
   fingerprint, or synthetic canary, so do not state key exfiltration as
   independently proven unless vendor-side evidence confirms that exact edge.
4. **Job-token channel — analyze independently.** Checkout v6 persisted Git
   authentication by default using version-specific storage, and the job asked
   for `pull-requests: write`. Prove whether fork code could use or recover that
   credential and its effective runtime permissions; do not infer raw
   `GITHUB_TOKEN` exposure merely from a later step's `env` declaration.
5. **Vendor disposition — useful, not proof inflation.** DuckDuckGo reopened,
   triaged, and resolved #3619287, stating that information from both related
   reports was valuable and mitigations were applied together. Preserve this as
   vendor-confirmed remediation/prior art, while keeping the exact demonstrated
   boundary at the evidence level actually shown.

### Supply-chain impact boundary

At the historical snapshot, `semver-release.yml` required the PR to be
`merged == true` and carry `semver-major` or `semver-minor` before dispatching
`build.yml` on `main`. A `pull-requests: write` token could affect labels, but
label authority alone did not merge attacker code, write `main`, bypass branch
protection, or poison release bytes. It could at most influence release timing
or version selection after an authorized merge unless another privilege was
proven.

Likewise, the repository description that code is shared across DuckDuckGo
browsers is not proof that every platform automatically consumes an attacker-
controlled release. A direct all-browser supply-chain claim requires exact
package/release branch, version resolution or pinning, build incorporation,
signature/integrity enforcement, update cadence, and downstream consumer
read-back for each platform.

Methodology conclusions:

1. Trace secret scope and workspace integrity together; neither alone is the
   full security model.
2. Treat any earlier untrusted step as able to modify same-job files, tools,
   dependencies, command files, and background processes until isolation is
   proven.
3. A uniquely tagged callback proves only the execution and attribution edges
   it actually records; it does not prove secret value, token permission, or
   downstream mutation.
4. Label manipulation, release dispatch, release-byte poisoning, and client
   consumption are four different boundaries.
5. Bundle neither sibling workflows nor additional PATs into one finding without
   an exact per-workflow source-to-consumer trace.
6. This exact #3619287 lineage is `PUBLIC / FIXED / DUPLICATE`; a new report
   requires a distinct current workflow/action version, incomplete fix, or new
   authority bridge with its own G0-G6 proof.

## Fix hierarchy

1. Keep untrusted PR execution on `pull_request` with explicit read-only
   permissions, no secrets, and GitHub-hosted ephemeral runners.
2. Set `persist-credentials: false` whenever subsequent code is not fully
   trusted; do not rely on post-job cleanup.
3. Disable lifecycle scripts (`npm ci --ignore-scripts`) when unnecessary, or
   use a reviewed allowlist and keep package metadata under trusted control.
4. Never combine privileged events with explicit fork checkout and execution.
5. Never execute a trusted-path script with secrets after untrusted code ran in
   the same job/workspace. Move it to a fresh ephemeral job and immutable trusted
   action; transfer only narrow validated data.
6. Split build and privilege: untrusted job emits a narrow artifact; privileged
   job pins the source run/SHA and validates schema, paths, size, count, hashes,
   signatures, and non-executability before use.
7. Pin third-party actions by full commit SHA and review whether their inputs can
   become code, paths, templates, commands, or credential files.
8. Use minimum `permissions`, protected environments, short-lived credentials,
   branch/rulesets, required reviews, and deployment approvals.
9. For OIDC, restrict issuer, audience, repository, ref/environment, workflow
   identity, and reusable-workflow claims at the cloud trust policy.
10. Isolate self-hosted runners from secrets/internal networks and never reuse a
   compromised workspace without reimaging.
11. Regression-test both allowed same-repo flows and denied external-fork flows,
    plus credential-file absence before any untrusted consumer.

## KILL rules

KILL when:

- an external fork cannot trigger the workflow/run without trusted approval;
- the workflow definition and all executed actions/code come from the trusted
  base commit and untrusted fields remain non-executable data;
- a permission check fails before checkout/execution and no independent job or
  `always()` continuation bypasses it;
- repository/organization secrets are not referenced in the attacker-controlled
  step/action, no later secret-bearing step executes attacker-modifiable state,
  and no credential residue/helper channel exists;
- the only token is effectively read-only and exposes no protected resource or
  meaningful capability beyond public access;
- `persist-credentials: false`, checkout/action protection, or isolated jobs
  remove the credential channel;
- install/build scripts are disabled or the attacker cannot change any executed
  code/configuration;
- the claim depends only on `***` masking, a static payload in a fork, a PR fix,
  a vendor response, or architecture diagrams;
- branch protection, token-trigger suppression, environment approval, signing,
  or consumer pinning breaks the downstream chain;
- the exact root cause is public, fixed, duplicate, stale, or out of scope.

If no candidate survives G6, return **NO VALID FINDING**.
