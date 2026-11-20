# Severity climber

Take one `PRIMITIVE_VALID` candidate. Do not submit.

Climb from the frozen post-state toward Critical using only proven
target-native edges. Follow
`/home/kali/skill/references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md`.

Return `SEVERITY_LOCKED` with the reason and the maximum proven tier.
Failed edges that need a new method go through `adaptive-plan-check-loop`.
