# Operation Evidence and Replay Method

## Evidence atom

Every executed probe produces an immutable operation record with:

- operation ID and campaign ID;
- method ID plus definition hash;
- authorized identity and owned-resource labels;
- redacted request target and typed parameters;
- request/response header and body digests;
- timestamp, status, latency, and normalized response class;
- authoritative post-state when applicable;
- references to baseline, negative control, replay, and cleanup operations.

Secrets and raw third-party data are never stored. Preserve only the minimum
redacted excerpt needed to show the protected field or state.

## Candidate linking

A candidate statement cites operation IDs inline. Review tooling must resolve an
ID to the exact immutable record and permit replay only under the same scope
card and owned identity/resource registry.

The model may summarize evidence; it may not manufacture an operation ID or
replace a missing record with a proposed request.

## Replay gate

Replay checks:

1. schema definition hash still matches;
2. target and scope card remain current;
3. same identity/resource labels resolve;
4. baseline still behaves as expected;
5. candidate operation produces the same security-relevant state;
6. independent read-back confirms any side effect;
7. cleanup restores the owned fixture.

Classify drift explicitly: schema drift, deployment drift, state drift, policy
drift, nondeterminism, or false original interpretation.

## Response deduplication

Hash-grouping identical bodies reduces review volume. The grouped view retains:

- all producing operation IDs;
- identity/auth/config variant for each;
- status and header differences;
- first and last observation time.

Never infer that variants are equivalent merely because bodies hash equally;
the authority context remains evidence.

## Manual reproduction

Before `STRONG + MANUALLY_CONFIRMED`, reproduce the minimum proof outside the
model-driven orchestration using the approved harness or a clear manual request.
Verify the operation IDs, one-variable control, protected effect, and cleanup.

## Failure states

- missing record: `KILL_UNREPLAYABLE_CLAIM`
- stale definition: `BLOCKED_SCHEMA_DRIFT`
- no protected effect: `KILL_NO_PROTECTED_EFFECT`
- no authority delta: `KILL_NO_CAPABILITY_DELTA`
- only error/status difference: `KILL_ERROR_ONLY`
- unsafe replay required: `BLOCKED_MINIMUM_SAFE_PROOF_REACHED`
