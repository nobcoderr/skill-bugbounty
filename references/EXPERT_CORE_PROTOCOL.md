# Expert Bug Bounty Core Protocol

This protocol is mandatory across the pack.

## 0. Codex CLI role separation

When auditing in any agent runtime (Cursor, Codex CLI, Claude Code, Gemini, or other), use independent fresh-context roles for scope/reality mapping, security-model mapping, discovery, one-candidate semi-triage, reachability/prior-art/end-to-end verification, blind final judgment, and human reproduction. Discovery output is hypothesis-only and starts at `CODE_DERIVED_HYPOTHESIS` in schema v8. Multiple agreeing sessions are not evidence. Every candidate must explicitly state attacker condition, server condition, and security impact.

## 1. Authorization gate

Record the program, exact asset/component, eligible vulnerability classes, exclusions, automation and rate rules, safe harbor, account restrictions, privacy constraints, and stop conditions. Unknown scope is not permission.

## 2. Reality map

Prove the real target path:

`repository/tag/commit -> build/package/artifact -> configuration/feature flag -> deployment or stable release -> user workflow -> privileged or sensitive sink`

For Web3, replace deployment with chain, address, proxy/implementation, initialization state, roles, balances, integrations, and current code hash. For SaaS, map tenant, role, region, API version, feature rollout, and backend ownership.

## 3. Prior-art map

Search issues, PRs, security advisories, CVEs, changelog, commits, release notes, documentation, tests, known limitations, public security research, dependency advisories, and sibling products. Record exact overlap and why a candidate is or is not duplicate.

## 4. End-to-end security trace

Use both directions:

`attacker input -> parser/decoder -> canonicalization -> validation -> state/cache/serialization -> auth/signature/policy -> privilege transition -> sink -> impact`

`sensitive sink <- helper/wrapper <- caller <- state/policy assumptions <- attacker-controlled source`

The paths must meet on one production/mainnet/release-reachable flow. For authorization, additionally trace `subject + action + target resource + tenant/org + object state` and verify the target scope reaches the policy engine or an equivalent downstream filter.

## 5. Expert hypothesis ranking

Rank each lead by:

`scope fit × real reachability × attacker control × missing check certainty × boundary crossed × impact × reproducibility × novelty`

Scanner severity is not part of the score.

## 6. Safe proof design

Use researcher-owned accounts, synthetic objects, local/disposable environments, loopback listeners, harmless marker files, mock services, controlled contracts, and non-destructive canaries. Include baseline, positive case, negative control, exact state before/after, timestamps, versions/hashes, and cleanup.

## 7. Falsification

Try to KILL every lead:

- upstream or downstream check exists;
- equal/higher privilege is already required;
- component is dev/test/nightly/local-only or disabled by default;
- attacker cannot realistically control the input;
- action is intended within the same trust boundary;
- signature/hash/authorization covers the real object at the right time;
- impact is only cosmetic, self-XSS, scanner noise, crash-only, or theoretical;
- behavior is known, public, fixed, duplicate, excluded, or requires prohibited testing.

### Authorization KILL challenge

Before KILLing authentication, authorization, tenant/object-scope, optional
middleware, or policy-provider behavior, load
`AUTHORIZATION_INVARIANT_KILL_CHALLENGE.md` and prove:

- the protected-operation invariant and enforcing component;
- configured plus absent/nil/empty/no-op/default/unknown/error behavior;
- the resource authorized is the resource consumed by the sink;
- the protected handler/query/mutation result end to end;
- documented/architectural intent, invariant preservation, and no
  attacker-controlled authority transition.

Missing proof means `HYPOTHESIS / NEEDS_INVARIANT_PROOF`, not KILL and not a
finding.

## 8. Manual reproduction status

Track the technical verdict separately from manual status: `NOT_TESTED`, `BLOCKED`, or `MANUALLY_CONFIRMED`. A source-level STRONG candidate is not report-ready until the researcher manually reproduces the protected-boundary impact with baseline, negative control, raw evidence, and cleanup.

## 9. Verdicts

- **STRONG:** scope, real reachability, root cause, primitive, boundary, impact, safe reproduction, controls, and prior-art status are substantially proven.
- **MEDIUM:** credible and reachable, but one major primitive/boundary/impact proof remains.
- **WEAK:** suspicious signal with material assumptions or incomplete reachability.
- **KILL:** invalid, out of scope, unreachable, by design, duplicate/known, unsafe to test, or lacks concrete impact.

If nothing survives: **NO VALID FINDING**.

## 10. Output boundary

Produce technical candidate validation and evidence handoff only.
