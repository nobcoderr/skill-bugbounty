# Discovery Cascade Method

## Purpose

Turn a proven observation into bounded second-order research without replaying
the original input or allowing evidence inheritance.

## Ask the two cascade questions

For every target-confirmed observation ask:

1. How can equivalent behavior be detected in another implementation,
   component, or semantically equivalent path?
2. Does the mechanism that produced this behavior enable a different protected
   security effect?

Derive a general property from the observation, not a reusable payload.

## Preserve genealogy

Each node records:

- `candidate_id` and `cascade_parent`;
- observation and invariant ancestry;
- `micro_inspiration_id`;
- `cascade_depth`;
- the conceptual change from parent to child;
- two second-order questions;
- the child's independent evaluation plan.

The child cannot inherit source, runtime, reachability, impact, or negative-
control proof. A missing genealogy edge contaminates the cascade claim.

## Use CASCADE_LEAD deliberately

Assign `CASCADE_LEAD` when an observation is independently reproducible and
conceptually useful but has no proven protected impact. Preserve it with an
explicit budget, next discriminator, and expiry condition. Do not report it and
do not KILL it solely because it is not currently exploitable.

## Bound autonomous expansion

Search siblings and pairs before triples. Limit children per node, maximum
depth, compute, and live requests. A child that changes scope, target, or
testing mode requires a new authorization gate; it must never switch targets
autonomously.

## Measure conceptual jumps

Record whether the child changes implementation, semantic domain, consumer,
state, or protected effect. Simple mutation of parent syntax is not a
conceptual jump. Retain anomaly fingerprints as data, but keep hidden target
answers and post-proof prior art out of future ideation contexts.
