# Generic Anomaly Evaluation Method

## Purpose

Detect violations of a target-defined invariant without requiring the
evaluator to know the vulnerability class or exact anomalous output in advance.

## Define the primitive before probing

Record:

1. the stable baseline input and state;
2. the expected security invariant `I`;
3. one controlled probe or transformation;
4. the authoritative observable `O`;
5. deterministic acceptance and rejection predicates;
6. negative and false-positive controls;
7. abort and cleanup conditions.

The core decision is:

`baseline satisfies I + probe produces O + O violates I -> ANOMALY`

It is never:

`output resembles a known issue -> vulnerability`.

## Use broad observations and narrow decisions

Capture status, state transitions, identity, authorization result, allocation,
latency distribution, storage changes, queue effects, and consumer read-back
when relevant. The acceptance predicate must bind the changed property to the
probe while anomaly channels may retain other unexpected behavior for later
review.

Examples of valid target-native differentials include:

- two equivalent consumers make different authorization decisions;
- a small attacker-controlled value produces disproportionate measured cost;
- a state transition violates an explicit lifecycle postcondition;
- a representation-preserving transformation changes protected behavior.

## Maintain an anomaly ledger

Freeze for every observation:

- baseline and anomaly fingerprints;
- exact input and one-variable difference;
- invariant, observable, runner, and evaluator version;
- probe cleanliness and semantic proof;
- repeated measurements and negative controls;
- scope, abort, cleanup, and runtime identity;
- anomaly origin and independent-reproduction status.

An anomaly remains a lead until harness falsification, source/root-cause proof,
consumer/state proof, authoritative read-back, reachability, and impact gates
pass.

## Prevent evaluator gaming

Reject model prose, a status code, crash, response length, self-selected
fingerprint, or stimulus echo as sole proof. Freeze predicates before execution
and bind stimulus, baseline, affected principal/resource, and effect to distinct
evidence fields. Version the validator and store its digest.
