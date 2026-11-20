# Resource Amplification Method

## Model cost

For every attacker-controlled count, depth, offset, index, size, expansion
ratio, fan-out, retry count, parser nesting, or work factor, identify the final
consumer and estimate:

`amplification = victim_cost / attacker_cost`

Track separate dimensions for CPU, resident memory, virtual memory, disk,
database rows, queue jobs, recursion/stack, decompressed bytes, network fan-out,
and cryptographic operations.

## Trace the bound

Map:

`attacker representation -> numeric conversion -> arithmetic -> allocation or loop -> lifetime -> release/backpressure`

Check overflow, underflow, truncation, signedness, sparse versus committed
allocation, lazy versus eager work, amortization, deduplication, quotas,
cancellation, and global/per-principal accounting.

An input-size limit is not sufficient when an attacker-controlled numeric value
selects a much larger victim resource independently of input bytes.

## Prioritize disproportion

Retain hypotheses where a small authorized request can cause a substantially
larger protected resource effect under realistic concurrency and defaults.
Measure attacker bytes/requests and victim cost using an isolated local fixture
or harmless owned environment.

Do not perform availability-impacting tests against live services. Use bounded
canaries, allocator/accounting hooks, fake queues, temporary stores, and abort
thresholds.

## Proof requirements

Record:

- attacker cost units and measurement;
- victim cost units and measurement;
- ratio or asymptotic bound;
- attacker-controlled numeric axis;
- missing cap or accounting invariant;
- lifetime, cleanup, and recovery;
- baseline and one-variable negative control;
- current-release/default reachability;
- concrete availability or quota-boundary impact.

KILL ordinary linear work, documented/intentional limits, default-off paths,
effective quotas, negligible ratios, non-committed resource observations, or
effects requiring prior privileged control.
