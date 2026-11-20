---
name: vuln-variant-coverage
description: "After the target system model exists, take disclosed reports from program A and test the same bug shape on authorized program B, one hypothesis at a time. Cover OWASP Top 10 and variants of SQL injection, XSS, CSRF, IDOR, file inclusion, RCE, SSRF, upload, and the other listed classes. A report from A is a pattern, not a payload and not a finding on B."
---

# Vulnerability variant coverage

Run this only after `target-system-model` has a current attack surface.
Test one falsifiable hypothesis at a time on one in-scope entry point.
Finish or kill that hypothesis before starting the next. Follow
`valid-bug-hunt` for severity order, proof, and the duplicate gate.

## Coverage

Cover every vulnerability class the attack surface can reach, including
the OWASP Top 10 and every `hunt-*` skill that has a `Corpus shapes`
section. Read that section, then the files it names, and turn each
remaining title into one card. SQL injection, XSS, CSRF, IDOR, file
inclusion, RCE, SSRF, and file upload are lanes, not the whole list.
The same rule applies to XXE, request smuggling, open redirect, race,
OAuth, OpenID, SAML, SSTI, cache, GraphQL, business logic, authentication
and authorization, account takeover, MFA, clickjacking, subdomain
takeover, information disclosure, session, JWT, CORS, host header, HTML
injection, deserialization, NoSQL, password reset, WebSocket, LDAP, API
and cloud misconfiguration, and the stack skill for the technology
program B actually runs.

`TOPMOBILE.md` is an asset list, not a class. Route each mobile title to
the class skill that matches its effect.

Skip a class the system model cannot reach. Do not force a class onto
an architecture that has no consumer for it.

Read `references/variant-coverage-matrix.md` only after the model identifies
the reachable surfaces. Select the narrowest matching `hunt-*` skill. Use
`agents/corpus-shape-analyst.md` to convert public reports into target-neutral
cards and `agents/variant-hypothesis-tester.md` to test exactly one surviving
card. Do not load or test the next card until the current card is `VALIDATED`,
`KILLED`, `BLOCKED`, or `EXHAUSTED`.

## Drop N/A and informative

Do not make a card from a report whose disclosed outcome is N/A,
informative, duplicate-only, spam, or by design. The JSON field
`severity` value `none` is not that label. Read the title.

Drop a title when the whole finding is any of these:

- a missing header, version banner, directory listing, or stack trace
- a rate-limit gap, email bomb, or missing captcha that never reaches an account or a payment
- self-XSS, a logout CSRF, or a framed page with no protected action
- a bare open redirect that carries no token and no account
- a best-practice TLS, cipher, or expired-certificate warning
- a crash, null dereference, or resource-exhaustion claim whose only effect is availability
- a public file or bucket that contains no sensitive data
- a design-principle label with no change to someone else's data, account, or authorization

Keep a report when it changes confidentiality, integrity, or another
person's account, including when the bounty is zero. A zero bounty is
not N/A.

## Program A to program B

Program B is the authorized program under test. Program A is a different
program in the local corpora. Read A's disclosed titles, then test whether
B has the same bug shape. Do not send traffic to A's hosts, and do not copy
A's request, host, token, or payload onto B.

Read local files only. Do not run the corpus fetchers.

- `/home/kali/security-research/hackerone-reports` at `4c279ab`
  (`docs/tops_by_program/TOP*.md`, `docs/tops_by_bug_type/`, `data.csv`)
- `/home/kali/security-research/hackerone-bug-bounty-reports` at `cb5d63c`
  (`results/based_on_program/*.md`, `results/based_on_vulnerability_type/`)

After selecting the reachable specialist skill, query the merged offline index
automatically. For example:

```bash
python3 /home/kali/.codex/skills/hackerone-reports/scripts/query-corpus-cards.py \
  --skill hunt-idor --program-b "PROGRAM B" --format jsonl
```

Use the actual selected `hunt-*` name. `--limit 0` is the default and returns
every matching card; process them one by one rather than loading them all into
one agent context. The router has no target capability and its output remains
quarantined until `agents/corpus-shape-analyst.md` passes the complete
N/A/informative and target-shape review.

Before using A, read B's own file in both corpora. A report that already
names B is prior art for the duplicate gate, not a new test.

Choose A because its product shape matches B's system model: commerce,
identity, chat, CI, storage, mobile, GraphQL admin, OAuth, or file upload.
When no program matches, use the bug-type files for the lane under test and
keep only titles whose feature exists on B.

For each selected report that survives the N/A and informative exclusion, write one card:

- source program and report id
- bug class
- who could supply the input on A
- what A trusted
- which protected effect changed
- the entry point on B that has the same shape
- the observation that kills the hypothesis

If B has no matching feature, kill the card. Then test the surviving card
on B with the specialist skill for that class and
`corpus-writeup-transfer` for the public writeup or PoC method. One card
at a time. A hit
on B is a lead until `valid-bug-hunt` has an end-to-end proof and the
duplicate gate shows it is not the same resolved issue.

## One-by-one test

Each lane states the entry, the expected protected effect, and the
observation that kills it. Active testing uses the program's allowed
methods, a researcher-owned account, and the smallest harmless proof. A
lane ends as validated, killed, blocked, or exhausted. Then move to the
next uncovered class on the same program, across every in-scope asset, not
only the first host.

Maintain a per-asset queue with `CARD_ID`, class, variant, entry condition,
protected effect, specialist skill, current release, negative control,
falsifier, and terminal state. A scanner signature or corpus resemblance may
create a card but cannot validate it.
