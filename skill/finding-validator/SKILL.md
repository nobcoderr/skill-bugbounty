---
name: finding-validator
description: "Independent re-exploit of a candidate. Replay the primitive on frozen evidence, confirm the protected effect, then pass it to severity climb. Use automatically after PROMISING or PRIMITIVE_VALID."
---

# Finding validator

Authorized offensive-first. Re-run the attack from a fresh context.
If the protected effect still happens, it is `PRIMITIVE_VALID` and
goes straight to `hunt-severity-climb`. If it does not, `KILLED`.

Confirm:

- in-scope host or artifact on the current release
- attacker condition, server condition, protected effect
- baseline, one-variable control, authoritative read-back

Do not invent a new class here. Chain impact in `hunt-severity-climb`.
