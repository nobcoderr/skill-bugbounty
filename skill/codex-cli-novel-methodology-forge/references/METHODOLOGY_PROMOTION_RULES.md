# Methodology Promotion Rules

Method definitions are immutable after execution begins. Execution records and
promotion decisions are append-only. Statistics are derived from events; an
executor cannot update counters or status.

## States

`EXPERIMENTAL -> SOURCE_USEFUL -> REPRODUCIBLE -> BLIND_VALIDATED -> PROMOTED`

- `EXPERIMENTAL`: frozen definition; no accepted material evidence yet.
- `SOURCE_USEFUL`: at least one deduplicated, source-backed new factual atom.
- `REPRODUCIBLE`: the same property is reproduced by an independent executor
  and isolated capsule.
- `BLIND_VALIDATED`: a frozen method passes independently curated sealed blind
  trials with no answer leakage.
- `PROMOTED`: paired V12/V13 evidence satisfies all metrics and a human records
  a signed/hashed promotion decision.

## Minimum promotion evidence

- at least three independent `method x target snapshot x blind seed` executions;
- new-material-evidence execution rate at least 50 percent in DISCOVERY/BLIND
  runs, deduplicated by semantic evidence identity;
- at least one non-duplicate valid finding that passed the normal full pipeline;
- report-ready false-positive rate no greater than the frozen V12 baseline;
- `BLIND_GENERALIZATION=PASS` across more than one target family;
- `EXACT_ROOT_REGRESSION=0` in paired equal-budget V12 controls;
- `PATCHED_CONTROL_FALSE_POSITIVE=0`;
- `GROUND_TRUTH_LEAKAGE=0`;
- `RUNAWAY=0`; and
- explicit independent human approval.

Three runs on one target, one duplicate/public finding, fragmented evidence,
unsealed B11/B12/B13 fixtures, or a self-declared PASS cannot satisfy promotion.
B11, B12, and B13 are readiness placeholders until independently curated and
executed; their initial status must remain `NOT_RUN`.

The scoring helper reports a recommended state and promotion eligibility. It
never writes the registry, promotes a method, or changes the default stack.

