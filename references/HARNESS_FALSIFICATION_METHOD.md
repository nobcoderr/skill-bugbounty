# Harness Falsification Method

## Purpose

Prove that an anomaly belongs to the target rather than the test harness,
client, fixture, instrumentation, scheduler, cache, or evaluator.

## Classify anomaly origin

Use one state:

- `TARGET_CONFIRMED`: independent evidence attributes the property to the
  target;
- `HARNESS_CONFIRMED`: the harness creates the observation;
- `MIXED`: target and harness both contribute;
- `UNKNOWN`: attribution remains unresolved.

Only `TARGET_CONFIRMED` can advance toward a strong candidate.

## Audit the harness

Freeze and inspect:

- serialization and normalization before transmission;
- connection, process, cache, and fixture reuse;
- ordering, timing, retries, buffering, and truncation;
- instrumentation side effects and state leakage;
- comparison and fingerprint code;
- environmental differences between baseline and probe;
- evaluator configuration and version.

Run the baseline and negative controls through the identical pipeline. Confirm
that the harness neither invents the anomaly nor suppresses the expected
observable.

## Require independent reproduction

When feasible, reproduce the same property with two independently implemented
runners or one runner plus authoritative target-side read-back. Independence
requires separate parsing, sending, measurement, or state-observation code—not
two invocations of the same helper.

Record runner identifiers, versions, evidence digests, and whether both prove
the same invariant violation. If reproduction fails, retain `UNKNOWN` or mark
`HARNESS_CONFIRMED`; do not reinterpret noise as target behavior.

## Use deterministic verdict gates

The model may generate hypotheses, explain evidence, and propose a harmless
proof. Versioned deterministic code must enforce budgets, execute only an
authorized safe plan, compare the frozen baseline, validate read-back and
negative controls, confirm cleanup, and decide primitive success.

Reject model-only decisions, validators written after seeing the result,
mutable acceptance predicates, stimulus-matching fingerprints, and missing
validator digests. A fresh AI may interpret frozen evidence after the code gate;
human review owns scope, conceptual leaps, novelty, and final judgment.

## Safety boundary

Never mask safety signals, deceive the agent about target identity, switch
targets, collect credentials, perform destructive proof, or raise volume to
force a result. Exit after the minimum harmless proof.
