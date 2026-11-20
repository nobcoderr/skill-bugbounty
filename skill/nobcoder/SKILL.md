---
name: nobcoder
description: "Use the pinned nobcoderr/nobcoder harness when the user names nobcoder, bbp-harness, or an autonomous authorized audit. Read the local clone and its control plane. The repository itself does not authorize a live target."
---

# nobcoder

Local clone: `/home/kali/security-research/nobcoder`
Pinned commit: `1775d26` (2026-11-11).
Control command: `bbp-harness` (`/home/kali/.local/bin/bbp-harness`).
State: `/home/kali/.bbp-ai`.

The installed `codex-security-harness` skill remains the pack copy. This skill
points at the cloned source. Do not replace either one unless the user asks
for an update.

## Use

Read the clone `README.md` and `skill/codex-security-harness/SKILL.md` before
operating the harness. Knowledge search:

```bash
bbp-harness query '<target-native terms>'
```

Index only local files. The configured roots include this clone,
`/home/kali/security-research/hackerone-reports`, and
`/home/kali/security-research/ai-web3-security`.

## Authorization

Adding this repository does not start a campaign and does not authorize a
target. Run `bbp-harness audit` only after the user has named an official
in-scope program, repository, or asset. Keep network and state-changing
actions inside that scope. Treat worker output as a hypothesis.
