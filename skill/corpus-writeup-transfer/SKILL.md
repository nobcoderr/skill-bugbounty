---
name: corpus-writeup-transfer
description: "Offensive transfer of disclosed HackerOne writeups onto the current in-scope bounty target. Search reddelexc, codebygk, and reddelexc.github.io for the same class, steal the attack method, and land a working PoC on program B. Use automatically during bug bounty."
---

# Corpus writeup transfer

Authorized offensive-first. Paid and high-ranked public writeups are
attack playbooks. Pull the same class from the local corpora, rebuild
the exploit against the current in-scope target, and prove a protected
effect.

Indexes:

- `/home/kali/security-research/hackerone-reports` at `4c279ab`
- `/home/kali/security-research/hackerone-bug-bounty-reports` at `cb5d63c`
- `https://reddelexc.github.io/hackerone-reports/`

```bash
python3 /home/kali/.codex/skills/hackerone-reports/scripts/query-corpus-cards.py \
  --skill HUNT_SKILL --program-b "PROGRAM B" --format markdown --limit 8
```

## Attack loop

1. Rank cards by bounty, then upvotes. Skip N/A, informative, by-design,
   duplicate-only, spam, and impact-free titles.
2. Open the public writeup `https://hackerone.com/reports/ID`.
3. Steal the invariant: attacker input, trusted mistake, sink, and the
   step that changes another account, secret, or authority.
4. Same program as B: retest on the current release. If it still hits,
   that is an incomplete fix. If it is dead, rotate to the next writeup.
5. Different program A: rebuild the attack on B's own hosts, params, and
   researcher accounts. Drive the same trust mistake until a protected
   effect appears, then chain with `hunt-severity-climb`.
6. One writeup at a time. Spawn `agents/writeup-poc-tester.md`.

## Limits

Stay on the named in-scope host. Rebuild the method for B; do not fire
A's URL, cookie, token, or payload bytes. Do not run corpus fetchers
unless the user asks to refresh. Private HackerOne bodies stay unread.
Harmless owned-account proof only.
