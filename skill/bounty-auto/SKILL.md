---
name: bounty-auto
description: "Authorized offensive-first bug-bounty chain. Map the in-scope surface, fire the highest-impact class, land matching public writeups as PoCs, then chain toward Critical. Use automatically on an official program. Ordinary coding does not enter this skill."
---

# Automatic bug bounty

Authorized offensive-first. As soon as the task is a named official
program or an in-scope hunt, attack: map the surface, pick the highest
impact reachable class, steal matching public writeups, land a PoC, then
chain toward Critical. Do not wait for a skill or class to be named.
Ordinary coding, product, UI, or writing does not enter this skill.

## Offensive-first execution

Run every lane as adversary emulation:

`attacker state -> reachable entry -> bypass or primitive -> capability delta -> protected sink -> concrete impact`

Prioritize target-native exploitability, alternate control paths, chainable
primitives, authorization transitions, cross-tenant effects, code execution,
credential or sensitive-data access, signing or supply-chain compromise, and
fund or integrity impact when the real surface supports them. Do not replace
this work with generic headers, configuration advice, detection ideas,
compliance, or remediation. Use defensive controls to design negative tests
and attempt bounded bypasses; write remediation only after the candidate is
proven or killed, unless the user explicitly requested blue-team output.

Offensive-first does not mean speculative or destructive. Preserve exact
scope, program rules, rate limits, owned test data, harmless proof, cleanup,
and the evidence gates below. The maximum reportable impact is the maximum
actually demonstrated capability.

## Open without being asked

Read these before testing:

1. `valid-bug-hunt`
2. `target-system-model`
3. `vuln-variant-coverage`
4. `hackerone-reports`
5. `corpus-writeup-transfer`
6. `nobcoder-writeup-transfer`
7. `hunt-scope-exhaustion`
8. `hunt-director`
9. `hunt-orchestrator`
10. `adaptive-plan-check-loop`
11. `hunt-terminal-verdict`
12. `payload-forge`
13. `payloadsallthethings`
14. `oss-scanner` when the target is a GitHub or open-source repository

Then follow them. Program policy still wins over this skill.

## Specialists

When the system model shows a class can be reached, read that `hunt-*`
skill, including its `Corpus shapes` section, and fire one attack
hypothesis. Cover every reachable class, not only IDOR. Load a class
only after its surface exists.

A technology skill such as `hunt-nodejs` or `hunt-laravel` only routes
the title to the class skill. It does not replace that class skill.

For each reachable class, automatically query the two pinned HackerOne corpora
with `hackerone-reports/scripts/query-corpus-cards.py --skill HUNT_SKILL
--program-b PROGRAM_B`, and query `github.com/nobcoderr/writeup` with
`nobcoder-writeup-transfer/scripts/query-writeup-cards.py --skill HUNT_SKILL
--program-b PROGRAM_B`. Run the passive corpus-card router, exclude N/A,
informative, by-design, duplicate-only, spam, and impact-free cards, then give
one surviving program-A shape at a time to the variant tester for program B.
Do not wait for the user to name the corpus or the class. Follow
`hunt-scope-exhaustion` so an empty first scope does not end the hunt.
For injection and filter classes, query PayloadsAllTheThings with
`payloadsallthethings/scripts/query-patt.py --skill HUNT_SKILL` and
forge B-specific payloads with `payload-forge`.

## Agents and tools

Spawn these without being asked, one question each:

- `hunt-director` to assign lanes
- `hunt-orchestrator` to run those lanes and evaluate results
- `explore` using `target-system-model/agents/system-model-explorer.md` to map
  one in-scope system or asset
- `generalPurpose` using `hunt-reentrancy/agents/reentrancy-hunter.md` when
  contracts or callbacks exist
- `generalPurpose` using `hunt-logic-vulnerability/agents/logic-hunter.md`
  when workflows, money, or entitlement exist
- `generalPurpose` using
  `vuln-variant-coverage/agents/variant-hypothesis-tester.md` for a single
  falsifiable hypothesis
- `generalPurpose` using `finding-validator/agents/finding-validator.md` on
  every survivor
- `adaptive-plan-check-loop` after a failed step, including a new technique
  wave
- `capability-gap-skill-builder` when a needed skill or agent is missing
- a passive corpus-shape analyst when local disclosed reports are relevant
- `generalPurpose` using `corpus-writeup-transfer/agents/writeup-poc-tester.md`
  for one disclosed writeup at a time
- `generalPurpose` using
  `nobcoder-writeup-transfer/agents/writeup-shape-tester.md` for one local
  writeup from `github.com/nobcoderr/writeup` at a time
- `generalPurpose` using `hunt-scope-exhaustion/agents/scope-rotator.md` to
  finish the current asset before rotating to the next official scope
- `generalPurpose` using `oss-scanner/agents/oss-source-auditor.md` when the
  in-scope asset is a GitHub or open-source repository
- `hunt-severity-climb` as soon as a candidate is technically valid
- `generalPurpose` using `hunt-terminal-verdict/agents/verdict-lock.md`
  before any user-facing audit conclusion
- `generalPurpose` using `payload-forge/agents/payload-mutator.md` when a
  probe is blocked or a class needs a forged payload
- `generalPurpose` using `payloadsallthethings/agents/patt-method-tester.md`
  for the matching swisskyrepo chapter on this host
- `security-review` only after `SEVERITY_LOCKED=YES`

There is no cap on how many independent questions run together. The
parent owns scope, severity lock, and `REPORT_READY`.

Use `burp-suite` when HTTP traffic needs a proxy or history. Use
`bug-bounty-browser` when a page, login, signup, or browser challenge
must run in the user's browser. Spawn `generalPurpose` with
`bug-bounty-browser/agents/browser-operator.md` for that one page.
Use `gtm-recon` when a page loads Tag Manager. Use `bug-bounty-account`
when a researcher account or email code is required. Use `nobcoder`
to query the local harness. Use `bug-bounty-tool-bootstrap` when a
local tool is missing. If that install asks for sudo, follow
`local-sudo-install` without asking. Do not ask first. Stop and tell
the user when a paid account or a balance top-up is required.

## Severity escalation before submission

When any candidate becomes technically valid, do not stop at its first Low,
Medium, or High label and do not mark it `REPORT_READY` yet. Automatically load
`hunt-severity-climb`, `exploit-chain-research-orchestrator`,
`../../../skill/references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md`, and
`exploit-chain-research-orchestrator/agents/severity-escalation-agent.md`.

Freeze the direct proof, compute the exact post-exploit capability, enumerate
only surfaces newly reachable from that state, and search for a continuous
target-native edge toward higher impact. Use `adaptive-plan-check-loop` for
bounded retries with materially different techniques. Re-run impact, current
release, prior-art, duplicate, controls, and cleanup gates after every proven
edge.

Critical is a search direction, not a required outcome. Never raise severity
from hypothetical, blocked, unrelated, or unsafe edges. After the terminal
impact is proven, all realistic expanding edges are falsified, or scope,
program, safety, or environment supplies a documented stop, set
`SEVERITY_LOCKED=YES` and retain the maximum actually proven tier. Only then may
the ordinary independent `security-review` decide `REPORT_READY`.
