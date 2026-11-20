# Micro-Inspiration Research Method

## Purpose

Generate target-native hypotheses without anchoring the model on an existing
attack class, payload, patch, or expected answer.

## Compile one research objective

Write the objective as a question over observable behavior:

`Under precondition P, does operation O preserve protected invariant I?`

Good objectives name the target component, state or representation boundary,
and authoritative observable. Reject broad instructions such as “find a
critical bug” or class-first requests.

## Build atomic inspiration fragments

Use one compact unit from:

- a source comment or branch condition;
- a type or ownership invariant;
- an API or dependency contract;
- a test expectation or error message;
- a state-machine or serialization rule;
- a small non-security specification fragment.

Keep a fragment to one semantic rule, normally one to three sentences. Record:

- `micro_inspiration_id`;
- exact source and location;
- `micro_inspiration_scope`;
- an abstract semantic statement;
- confirmation that vulnerability ground truth and known attack terms were
  withheld.

Do not combine rich examples, advisory prose, proof-of-concept structures, or
multiple candidate answers. If the fragment identifies an expected bug, patch,
sink, or result, mark the run contaminated.

## Generate bounded hypotheses

Use this domain-neutral instruction:

> Given only this semantic rule and the observed target architecture, derive
> one to five testable ways implementation behavior could violate an expected
> security invariant. Do not name known vulnerability classes or reuse known
> payload structures. Every hypothesis requires a falsifier.

For every hypothesis record:

- one attacker-controlled variable;
- the invariant and expected safe result;
- a minimal probe idea;
- an authoritative observable;
- a falsifier and closest safe sibling;
- the specific target facts that support derivation.

Reject generic checklist output, pattern replay, unbounded brainstorming, and
hypotheses that cannot be distinguished by a safe experiment.

## Control anchoring experimentally

Treat context as an experimental variable. Use a fresh ideation context for
each fragment. Compare hypothesis diversity and target-fact coverage across
fragments, not agreement with an expected answer. Store only normalized
hypotheses and provenance for the next stage.
