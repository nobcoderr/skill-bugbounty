---
name: valid-bug-hunt
description: "Run an authorized bug bounty hunt across every in-scope asset. Prioritize critical, then high, medium, and low. Require an end-to-end PoC and STRONG triager-proof evidence, check the official program docs, and reject duplicates, theoretical, N/A, informative, and by-design leads. Use parallel falsifiable agents, Hermes review, Burp, and local tools without asking for another confirmation."
---

# Valid bug hunt

`bounty-auto` enters this skill on its own. Do not wait for the user to
name it.

Use this for every authorized HackerOne, Intigriti, or other official bug
bounty program. The researcher identities are:

- HackerOne: `argareksapatii` / `argareksapatii@wearehackerone.com`
- Intigriti: `nobcoderr`

Read the current official program page before testing and again before
`REPORT_READY`. Scope, exclusions, safe harbor, severity table, and
prohibited methods override this skill.

Start with `target-system-model`. After that surface exists, use
`vuln-variant-coverage` to test one vulnerability hypothesis at a time.

## Authorization already given

The user has given standing permission to hunt valid vulnerabilities on a
program they name, to install local tools, and to use Burp and the other
local tools below without asking again. That permission does not add assets,
remove exclusions, or allow destructive proof, credential theft, or a third
party. If a paid account, API credit, or wallet top-up is required, stop and
tell the user. Do not spend money.

## Severity order

Search every in-scope asset, not one scope. Schedule critical first across
the whole program: remote code execution and other program-critical impact.
When the critical lanes for the current pass are killed, blocked, or
exhausted, move to high, then medium, then low. A failed hypothesis rotates
to another falsifiable lane inside the same program. It is not a reason to
leave the program or to stay on a single host.

Maintain this portfolio for every official in-scope asset:

| Asset | Scope status | Current release | Critical | High | Medium | Low | Prior art | Coverage state | Next falsifiable question |
|---|---|---|---|---|---|---|---|---|---|

Use `UNMAPPED`, `ACTIVE`, `PROMISING`, `BLOCKED`, `EXHAUSTED`, `KILLED`, or
`VALIDATED` for coverage state. A severity tier advances only after every
asset's evidence-supported lanes in the higher tier have a recorded terminal
state. Critical-first is scheduling priority, not permission to force an RCE
hypothesis unsupported by the architecture.

## Evidence bar

Keep a lead at `HYPOTHESIS_QUARANTINED` until an end-to-end proof exists.
Theoretical reasoning, a strong argument, `N/A`, informative behavior, and
by-design behavior are not findings. The proof must show the real protected
effect on the current release. Maximize evidentiary completeness and the
capability-continuous chain to the highest eligible impact, but stop at the
minimum harmless action using owned accounts, canaries, local fixtures, and
authoritative read-back. Never require destructive RCE, credential theft,
third-party data access, persistence, mainnet fund movement, or denial of
service merely to raise severity. Prefer a realistic reproducible path over a
lab-only path, and record prerequisites, user interaction, reproduction count,
observed reliability, cleanup, and the exact terminal capability.

`STRONG` requires a reproducible PoC, a negative control, the exact request
or commit, and the program impact. `REPORT_READY` additionally requires the
triager-proof gate below. Do not submit before both gates pass. A valid Low,
Medium, or High is not finished: follow `hunt-severity-climb` until
`SEVERITY_LOCKED=YES`.

## Triager-proof gate

Before calling a candidate valid or submittable, prove the same root cause
or bug class is not already known. Check, for the current product and
release:

- GitHub open issues, closed issues, pull requests, merged PRs, discussions, and advisories
- commit history, changelog, release notes, and known issues
- official documentation and maintainer comments
- the program's public hacktivity, disclosed reports, and CVEs
- whether a reported fix actually holds on the current release

Use `hackerone-reports`, `bbp-harness query`, and `gh` when the source
repository is known. A public report is prior art. Retest it only to learn
whether the fix is incomplete. If the same path still works, keep it only
when the remaining behavior is distinct and proven. If duplicate risk stays
high, do not submit it.

Record `DUPLICATE_RISK=LOW|MEDIUM|HIGH`. `HIGH` blocks report readiness until
a distinct current root cause, version, consumer, or incomplete-fix path is
proven.

For source-code targets, the GitHub checks above are mandatory before any
validation deep-dive. For shipped JavaScript, read the current bundles,
source maps, endpoints, secrets, and DOM sinks, and follow `gtm-recon` when
the page loads Google Tag Manager. For a CVE, reproduce it on the current
in-scope build or drop it.

## Parallel work

Do not stay in one passive agent. Split by independent falsifiable questions,
not by "agent A reads file X". One question is one lane: the entry condition,
the protected effect, and the observation that would kill it. Use
`hunt-director` and `hunt-orchestrator` without being asked. Spawn
reentrancy, logic, class, and validator specialists in parallel. Use
`adaptive-plan-check-loop` on a failed lane. Use `security-review` for the
clean skeptical triager pass only after `SEVERITY_LOCKED=YES`. The parent
agent alone owns scope, severity lock, and `REPORT_READY`.

Load Hermes only as passive reviewers, from
`/home/kali/skill/prompts/HERMES_PASSIVE_EVIDENCE_ANALYST.md`,
`HERMES_WEBHACKLIST_PRIOR_ART_ANALYST.md`,
`HERMES_EXTERNAL_SECURITY_TOOL_EVIDENCE_ANALYST.md`, and
`HERMES_AGENTIC_HARNESS_EVIDENCE_ANALYST.md`. Their output stays a
hypothesis.

Treat a disclosed report from another program as program A and the current
authorized target as program B. Extract only the invariant bug shape from A,
then test a fresh B-specific hypothesis one at a time. Never replay A's
request, host, credentials, identifiers, or payload against B.

## Tools

Use Burp through the `burp` MCP server when HTTP history or Repeater is
needed. Also use the local tools already on `PATH`: `nuclei`,
`httpx-toolkit` (ProjectDiscovery HTTPX; `/usr/bin/httpx` is the Python client),
`ffuf`, `nmap`, `sqlmap`, `amass`, `subfinder`, `katana`, `dnsx`, `naabu`,
`jq`, `gitleaks`, and `gh` when that tool answers the current lane.

If a normal local tool is missing, install it into `~/.local/bin` or an
isolated environment through `bug-bounty-tool-bootstrap`, without asking again
once the named program, scope, and required analysis lane are known. Use its
fixed allowlist and record source, exact version, and checksum where available.
Installation never launches a scan. Do not install a paid product, spend
money, or install a tool that needs a balance without telling the user. Active
use of `sqlmap`, `nuclei`, `naabu`, `nmap`, fuzzers, or dynamic Web3/mobile/
cloud tooling stays inside the official scope, program rules, and rate limits.

## Candidate promotion

The only allowed progression is:

`HYPOTHESIS_QUARANTINED -> PRIMITIVE_VALID -> CHAIN_VALID -> STRONG + MANUALLY_CONFIRMED -> TRIAGER_PROOF=PASS -> REPORT_READY=YES`

No stage may self-certify the next. `REPORT_READY=YES` requires all of:

- `SEVERITY_LOCKED=YES` with the maximum demonstrated impact;
- `PRIOR_ART_COMPLETE=YES` and `DUPLICATE_RISK!=HIGH`;
- every essential chain edge proven on the same current release;
- baseline, one-variable negative control, before/after authoritative state,
  cleanup, raw evidence index, root cause, and fix locus;
- an independent `security-review` pass from frozen evidence.

Otherwise preserve `REPORT_READY=NO` with exact blockers. A scanner hit,
source-only argument, theoretical bridge, unknown release, missing negative
control, or missing protected read-back cannot be promoted.
