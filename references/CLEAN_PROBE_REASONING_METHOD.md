# Clean Probe Reasoning Method

## Purpose

Separate high-value semantic anomalies from behavior that may simply follow
from malformed, ambiguous, or undefined input.

## Classify before execution

Use exactly one class:

- `CLEAN`: valid under the governing grammar, semantically unambiguous, and
  expected to have one interpretation;
- `DIRTY`: deliberately malformed, undefined, or plausibly interpreted in more
  than one way;
- `UNKNOWN`: cleanliness cannot yet be established from authoritative rules.

Record the grammar/version, parsed structure, expected interpretation, and the
source of that expectation. Classification performed after seeing the result is
invalid.

## Prioritize correctly

- `CLEAN + unexpected protected effect` receives high research priority.
- `DIRTY + unexpected behavior` remains `NEEDS_SEMANTIC_PROOF` and cannot be
  promoted solely from weird output.
- `UNKNOWN` is treated like `DIRTY` until resolved.

Cleanliness raises research value; it does not prove security impact.

## Synthesize target-derived permutations

Generate transformations from the target grammar, types, state transitions,
equivalence relations, or documented semantics. Change one dimension at a
time. Examples include equivalent encodings, order-preserving operations,
single versus batch, synchronous versus delayed consumption, and boundary
values derived from target limits.

Do not load historical payload dictionaries or known exploit templates. Every
permutation must name the semantic property it preserves or intentionally
changes, its budget, and its inverse or closest safe control.

## Require semantic proof

Before a non-clean probe advances past anomaly triage, establish which parser
or consumer interpretation occurred and why that interpretation remains
security-relevant in a realistic current release composition.
