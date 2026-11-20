---
name: security-review
description: "Independently judge a frozen bug-bounty candidate for scope, current-release reachability, exploit-chain continuity, concrete impact, duplicate risk, severity, and triager-proof report readiness. Use after discovery and manual reproduction; do not use it to generate findings or self-certify the discovering agent."
---

# Security review

Use this as the clean skeptical pass for `valid-bug-hunt`. Activate
`mandatory-auto-router` and `bug-bounty-auditor`, then review frozen raw
evidence without the scout's persuasive narrative or requested severity.

## Inputs

Require the official program policy and scope snapshot, current release or
deployment identity, attacker/server conditions, raw request-response or local
test evidence, chain-edge ledger, baseline, one-variable negative control,
before/after authoritative state, reproduction count, cleanup, and prior-art
ledger. Missing evidence stays missing; never fill it with model agreement.

## Review questions

Return `PASS`, `FAIL`, or `BLOCKED` for each:

1. Is the exact asset and testing method currently in scope?
2. Is the observed component/version/configuration reachable on the current
   production, mainnet, or stable-release path?
3. Does each chain output capability exactly satisfy the next edge's
   prerequisites with continuous identity, privilege, state, and environment?
4. Does the negative control distinguish the claimed root cause from expected
   behavior, harness error, or an equivalent authorized path?
5. Is there an unauthorized protected effect with authoritative read-back and
   a nonzero attacker capability delta?
6. Was the result independently and manually reproduced using owned accounts,
   data, fixtures, or harmless canaries, followed by cleanup?
7. Did the prior-art pass cover semantic root cause and fix lineage across
   open/closed issues, open/closed/merged PRs, discussions, advisories/CVEs,
   commits, changelog, releases, official docs, maintainer comments, known
   issues, and public program reports?
8. Is the severity the maximum demonstrated impact rather than the maximum
   narrated impact, with every realistic escalation edge proven, falsified, or
   explicitly blocked?
9. Can a triager reproduce the same terminal effect from the evidence alone?

## Verdict

Only return `REPORT_READY=YES` when all of these are present:

- `STRONG=YES`
- `MANUALLY_CONFIRMED=YES`
- `SEVERITY_LOCKED=YES`
- `TRIAGER_PROOF=PASS`
- `PRIOR_ART_COMPLETE=YES`
- `DUPLICATE_RISK=LOW|MEDIUM`
- `ALL_ESSENTIAL_CHAIN_EDGES_PROVEN=YES`

Otherwise return `REPORT_READY=NO`, the exact blockers, the minimum next
falsifiable question, and any `KILL` reason. A scanner hit, source-only
argument, CVE/banner match, theoretical bridge, missing release identity,
missing control, or missing protected read-back cannot pass.

Hermes may be used only as a passive secondary evidence analyst through
`/home/kali/skill/prompts/HERMES_PASSIVE_EVIDENCE_ANALYST.md`. Hermes cannot
access a target, proxy, credentials, execute candidates, assign `STRONG`, or
override this verdict.

Do not send traffic, install tools, mutate external state, or submit reports
from this skill. If new target evidence is necessary, return `BLOCKED` and a
single exact verifier question to the parent campaign.
