---
name: oss-scanner
description: "Offensive source audit of an authorized GitHub or open-source repo using the Anthropic OSS Scanner method. Trace untrusted input to a privileged sink and land a working reproducer. Use automatically on OSS/GitHub hunts."
---

# OSS Scanner

Authorized offensive-first. The hosted Anthropic service is opt-in. For
a bounty or source hunt, steal its method: map what the repo claims to
protect, then break it from untrusted input to a privileged sink with a
working reproducer.

Local clone: `/home/kali/security-research/oss-scanner` (`a7e4e11`)
Upstream: `https://github.com/anthropics/oss-scanner`

## Attack loop

1. Inventory entrypoints, parsers, auth, serialization, workers, and
   helpers. Use `.oss-scanner/` or clone `templates/` as the claimed
   security boundary.
2. Trace attacker-controlled data to identity, tenant, RCE, secret, or
   integrity impact on the current in-scope commit.
3. Land a harmless reproducer. Hand hits to `finding-validator` then
   `hunt-severity-climb`.
4. Also fire `corpus-writeup-transfer` and `expert-source-code-bug-hunter`.

Spawn `agents/oss-source-auditor.md` for one repo.

If this authorized repo has a Dockerfile, a local no-network shell after
build is useful. `tools/validate.py` and `tools/check` in the clone are
enrollment helpers, not a generic scanner CLI. Use them only on a
maintainer-owned enrollment the user asked for.

## Limits

Stay on the named repository. Do not open an enrollment PR on
`anthropics/oss-scanner` for a bounty target or third-party project.
Do not claim Anthropic scanned the target unless a real service report
is in hand. Scanner prose is a lead until the reproducer hits.
