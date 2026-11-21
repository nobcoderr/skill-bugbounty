---
name: nobcoder-writeup-transfer
description: "Search disclosed writeups in the local clone of github.com/nobcoderr/writeup for the same bug class, steal the attack method, and land it on the current in-scope bounty target. Use automatically during bug bounty. Do not use for ordinary coding."
---

# nobcoderr writeup transfer

Authorized offensive-first. The local corpus at
`/home/kali/security-research/writeup` is program A. The authorized
target under test is program B. Find the same vulnerability shape in
those writeups and try that method on B.

Index: `https://github.com/nobcoderr/writeup` pinned in `PINNED.json`.
Read local files only. Do not run `hackerone-reports/refresh_all.py`
or `build_program_writeups.py` unless the user asks to refresh.

```bash
python3 /home/kali/.codex/skills/nobcoder-writeup-transfer/scripts/query-writeup-cards.py \
  --skill HUNT_SKILL --program-b "PROGRAM B" --format markdown --limit 8
```

## Attack loop

1. Query cards for the current reachable class on B. Rank by bounty,
   then upvotes. Drop N/A, informative, by-design, duplicate-only,
   spam, and impact-free titles.
2. B's own folder under `programs/` is prior art for the duplicate
   gate. Do not treat it as a new transfer card.
3. Open the local markdown. If the body is empty, open the public
   `https://hackerone.com/reports/ID` writeup.
4. Steal the invariant: attacker input, trusted mistake, sink, and
   the step that changes another account, secret, or authority.
5. Rebuild the attack on B's own hosts, params, and researcher
   accounts. Do not fire A's URL, cookie, token, or payload bytes.
6. One writeup at a time. Spawn `agents/writeup-shape-tester.md`.
7. Hit: `hunt-severity-climb`. Miss: next card, then next class on
   the same asset via `hunt-scope-exhaustion`.

This skill is the personal writeup lane. `corpus-writeup-transfer`
still covers reddelexc and codebygk. Run both.

## Limits

Stay on the named in-scope host. Harmless owned-account proof only.
Private HackerOne bodies stay unread. The clone does not authorize
a target.
