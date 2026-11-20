# Methodology Forge Method

The Forge converts a factual material coverage gap into a repeatable reasoning
procedure. It does not propose a vulnerability.

## Canonical procedure graph

Every methodology must define:

`input facts -> reasoning operators -> evidence queries -> oracle -> falsifier -> termination`

The graph is canonicalized independently of name, prose wording, example,
step-label, and topological ordering of independent nodes. A methodology is new
only when an inference/evidence-generating relation changes materially.

## Forge procedure

1. Select exactly one material `GAP_ID`.
2. Freeze its factual anchors and existing-coverage references.
3. State a security-reasoning principle and one core question without naming a
   vulnerability, affected file, function, payload, or desired outcome.
4. Define typed procedure steps with operator, consumed fact types, produced
   evidence types, and dependencies.
5. Define the required inputs and prove they are locally available.
6. Define a deterministic expected signal, negative signal, oracle,
   falsification strategy, and termination condition.
7. Compare the procedure graph and reasoning signature with the complete V12
   methodology registry and current research paths.
8. Enumerate false-positive modes and the cheapest control for each.
9. Freeze the definition before critic review.

## Required methodology fields

```text
METHODOLOGY_ID
NAME
TARGET_GAP_IDS
SECURITY_REASONING_PRINCIPLE
CORE_QUESTION
PROCEDURE_GRAPH
REASONING_SIGNATURE
REQUIRED_INPUTS
EXPECTED_SIGNAL
NEGATIVE_SIGNAL
ORACLE
FALSIFICATION_STRATEGY
TERMINATION_CONDITION
OVERLAP_WITH_EXISTING_METHODS
WHY_THIS_IS_MATERIALLY_DISTINCT
POTENTIAL_FALSE_POSITIVE_MODES
DEFINITION_DIGEST
```

Do not generate more than four definitions per wave. Prefer architecture-
derived methods over generic vulnerability taxonomies.

## Useful procedure families

These are operators, not automatically new methodologies:

- invariant inversion;
- consumer-first backward authority tracing;
- authority lifetime analysis;
- partial-failure/retry/rollback state analysis;
- composition assumption comparison;
- identity projection analysis;
- security-decision cache-key fact analysis;
- partial-order concurrency modeling; and
- negative-space sibling-path analysis.

If the same procedure already exists in V12 or the registry, it is overlap even
when the target, name, example, or wording differs.

