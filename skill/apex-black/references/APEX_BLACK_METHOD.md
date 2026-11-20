# APEX BLACK method

1. Validate authorization, official scope, target identity, owned accounts,
   limits, abort conditions, and cleanup.
2. Map application surfaces and choose only target-supported capability lenses.
3. Schedule independent probes as a bounded graph; preserve strict scope at
   every interaction.
4. Convert anomalies into candidates only when attacker control, boundary,
   sink, and a measurable post-state are evidenced.
5. Replay candidates in a fresh verifier context with baseline and negative
   control.
6. Update the attacker-state registry and enumerate only surfaces newly
   reachable from the proven capability delta.
7. Link primitives only through exact capability/prerequisite equality and
   continuity across actor, environment, privilege, and state.
8. Attempt severity escalation one technical hypothesis at a time. Record why
   each higher-impact edge failed, then lock the maximum observed severity.
9. Deduplicate by root cause and prior art.
10. Produce a hash-linked, redacted evidence index and a triager objection
    matrix. `STRONG + MANUALLY_CONFIRMED` establishes vulnerability validity;
    `TRIAGER_PROOF=PASS` is separately required for `REPORT_READY`.

For an evidence-supported native media-decoder chain, use
`/home/nobcoder/skill/references/IMAGE_DECODER_SSO_CONNECTOR_CHAIN_METHOD.md`.
Add graph nodes for exact artifact/backport identity, format dispatch, native
primitive, process authority, application authority, SSO/session binding,
connector authority, and terminal action. No downstream node may inherit proof
from an upstream crash or RCE label.

Stop on scope drift, kill switch, budget exhaustion, unexpected real data,
destructive effect, non-owned accounts, or missing authorization. Minimize
real-world impact and never persist, evade, steal credentials, phish, or run
high-volume denial-of-service activity. Never misrepresent a live target as a
CTF or conceal target identity or safety signals from any agent or harness.
