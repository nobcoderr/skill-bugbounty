# Methodology Novelty Critic

The critic rejects false novelty before execution. It evaluates procedure
graphs, reasoning signatures, evidence types, oracles, falsifiers, input
availability, existing methods, and existing research paths—not persuasive
prose.

## Hard KILL conditions

- canonical procedure graph equals an existing method;
- name, synonym, ordering, example, or prompt changed but semantics did not;
- definition is a vulnerability checklist or target-specific bug guess;
- it reopens an exhausted exact root without a new factual relation;
- it is already represented by a V12 method or research path;
- evidence inputs are unavailable or out of scope;
- procedure is excessively broad or lacks deterministic termination;
- oracle/falsifier is model judgment or candidate count; or
- likely output is speculative inference rather than new factual evidence.

## Novelty evaluation

The deterministic helper compares canonical procedure operators and dependency
edges, reasoning-signature fields, input/evidence types, oracle class,
falsifier, and termination class. Lexical difference cannot override semantic
overlap.

PASS requires either:

- at least two material reasoning-signature fields change; or
- one architecture-level traversal changes together with a new oracle or
  falsifier;

and the method addresses a factual gap not covered by an existing path.

Coverage delta is derived from new uncovered dimensions, new graph relation
types, new oracle classes, and new locally available input types:

- `NONE = 0`
- `LOW = 1..2`
- `MEDIUM = 3..5`
- `HIGH >= 6`

## Output contract

```text
NOVELTY=<PASS|FAIL>
EXECUTABLE=<PASS|FAIL>
EXPECTED_COVERAGE_DELTA=<HIGH|MEDIUM|LOW|NONE>
FALSE_POSITIVE_RISK=<HIGH|MEDIUM|LOW>
DECISION=<EXECUTE|KILL>
RATIONALE=
```

Only `NOVELTY=PASS`, `EXECUTABLE=PASS`, and at least MEDIUM coverage delta may
execute. The deterministic validator is authoritative over a self-declared
critic PASS.

