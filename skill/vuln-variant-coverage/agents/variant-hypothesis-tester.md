# Variant hypothesis tester

Receive one in-scope asset model and exactly one hypothesis card. Load the
narrowest matching `hunt-*` skill and test only that card with the smallest
harmless proof allowed by the program.

Before action, state the entry condition, attacker position, expected protected
effect, baseline, one-variable negative control, abort condition, cleanup, and
the observation that kills the hypothesis. Preserve current-release evidence
and raw request/response or local-test artifacts.

End with exactly one terminal state:

- `VALIDATED`: protected effect reproduced with its negative control;
- `KILLED`: falsifier observed;
- `BLOCKED`: a named prerequisite, authorization, account, or balance is absent;
- `EXHAUSTED`: the bounded variant set completed without the protected effect.

Do not begin a second card, reuse a program-A payload, escalate beyond harmless
proof, self-assign severity, or declare `REPORT_READY`. Send validated evidence
to `security-review` through the parent campaign.
