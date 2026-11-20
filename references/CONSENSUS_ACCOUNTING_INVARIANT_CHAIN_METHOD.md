# Consensus Accounting and Invariant-Chain Bug-Bounty Method

<!-- CONSENSUS_ACCOUNTING_INVARIANT_CHAIN:v1 -->

## Provenance and claim status

This method distills a user-supplied 11–12 October 2026 corpus describing an
XRPL/rippled offer-aggregation overflow composed with an anti-inflation
invariant overflow. Vendor, market-cap, bounty, timeline, validator-upgrade,
release, affected-value, exploitation, attribution, and “largest” claims are
**user-supplied prior art** until independently verified against authoritative
sources. The supplied Docker replay, ledger snapshot, transaction constants,
account material, and code are not copied into this method and are not
authorization to execute a historical exploit.

The reusable lesson is narrower and more valuable: a safety invariant can fail
in the same arithmetic domain as the state transition it is meant to police.
Two individually limited defects may align under the same modulus so that the
producer creates an invalid economic state while the checker observes an
apparently valid residue.

## Contents

1. Protected economic property
2. Arithmetic and value-flow inventory
3. Same-domain composition search
4. Constraint solving without exploit transplantation
5. Runtime and build semantics
6. Consensus, release, and deployment reachability
7. Safe proof ladder and terminal oracle
8. Patch-completeness review
9. AI-agent and passive-review discipline
10. Required evidence and verdicts

## 1. Protected economic property

Write the protocol property as unbounded mathematics before reading machine
types. Examples include:

- native supply cannot increase except through an explicitly authorized mint;
- the sum of debits, credits, fees, burns, and reserves must conserve value;
- an individual balance and the global supply must each stay within their own
  independent bounds;
- rejected or failed transitions must not commit partial economic effects;
- every validating implementation must reach the same deterministic result.

Represent a generic conservation rule as:

`sum(after) - sum(before) = authorized_mint - authorized_burn - fees`

The oracle uses arbitrary-precision integers or another mathematically exact
representation. It must not reuse the implementation type, helper, fold,
serialization, or assertion under review.

Record separately:

| Layer | Question |
|---|---|
| Item | Is each debit/credit individually legal? |
| Aggregate | Is the total computed without truncation or wrap? |
| Account | Does each account remain within its bound? |
| Global | Does total supply satisfy conservation? |
| Commit | Was the invalid transition actually persisted? |
| Finality | Would canonical consensus retain the state? |
| Spendability | Can the resulting balance reach an ordinary protected consumer? |

A per-account cap does not prove global conservation. A successful submit or
preflight result does not prove commit, finality, or spendability.

## 2. Arithmetic and value-flow inventory

Trace the complete transaction path and annotate every numeric domain:

`attacker-controlled transaction -> per-item validation -> aggregation -> debit -> per-item credits -> invariant accumulation -> commit -> finality -> downstream spend`

For each arithmetic site record:

| Field | Evidence |
|---|---|
| Semantic value | Amount, fee, reserve, supply delta, quality, share, or count |
| Source type | Signed/unsigned width, fixed point, multiprecision, wrapper type |
| Operation | Add, subtract, multiply, convert, negate, accumulate, round |
| Range proof | Explicit bound and why it holds on every reachable path |
| Failure behavior | Checked error, exception, saturation, wrap, trap, UB |
| Consumer | Debit, credit, invariant, serialization, consensus, UI, or API |
| Identity | Whether the checked value is the exact value later consumed |
| Build evidence | Compiler, flags, optimization, sanitizer/trap behavior |

Search all sibling aggregation sites, not only the function named in a public
case. Generic reducers, `operator+=`, implicit conversions, negation of minimum
values, mixed signedness, and intermediate-width promotion frequently create a
wider error domain than one patched call site.

## 3. Same-domain composition search

For every producer defect, inspect every checker that is supposed to contain
its effect. Build an arithmetic-domain graph:

`producer exact value -> producer machine residue -> committed item effects -> checker exact delta -> checker machine residue -> predicate`

Retain a composition hypothesis only when all of these are proven:

1. attacker-controlled values reach both arithmetic domains through one valid
   transaction or state transition;
2. the producer's wrapped/truncated value changes what the attacker pays,
   receives, or causes;
3. per-item side effects use a materially different representation from the
   aggregate result;
4. the checker independently accumulates the real side effects in a domain
   that can lose the same information;
5. the residues satisfy the checker while the exact mathematical state violates
   the protected property;
6. error handling does not abort, roll back, or canonicalize the transaction;
7. the same build and consensus path reaches commit.

Do not join two overflow-shaped functions merely because their widths match.
The same transaction values, sign convention, operation order, and state must
bridge them.

## 4. Constraint solving without exploit transplantation

Model cardinality, item bounds, transaction limits, account limits, fees,
rounding, and path selection symbolically. Useful questions include:

- Can a reachable number of individually valid items exceed the aggregate
  domain?
- Can the producer and invariant land on compatible residues under the same
  transaction constraints?
- Does a limit on offers/items/entries stop the exact mathematical threshold?
- Does distributing value across principals bypass an item-level or
  account-level cap while violating the global property?
- Does the fee or burn term change the required residue?
- Can the attacker fund and create the required state under ordinary protocol
  rules without privileged validator control?

Use a solver, arbitrary-precision script, or property test only against a local
model or authorized fixture. Derive parameters from the current target's own
types and bounds. Never transplant the public case's item count, amounts,
account set, ledger snapshot, transaction, or account material into another
target.

## 5. Runtime and build semantics

Source reasoning is insufficient when the language permits undefined,
implementation-defined, trapping, saturating, or optimized-away behavior.

For native code, bind every arithmetic claim to:

- exact source revision and dependency graph;
- official release artifact or reproducible build provenance;
- compiler family/version and optimization flags;
- overflow, sanitizer, and trap configuration;
- target architecture and integer ABI;
- observed release-binary behavior in an isolated authorized environment.

If a local debug build traps while the shipped release wraps, they are distinct
evidence states. If the language says the operation is undefined, do not call
wraparound a protocol property until the exact deployed artifact demonstrates
it. Conversely, a sanitizer crash does not prove the production artifact is
safe.

Consensus software adds another requirement: all supported validators must not
disagree about arithmetic or exception behavior. A candidate that only causes
heterogeneous-node divergence may be an availability or consensus-safety issue,
not the same economic-integrity finding.

## 6. Consensus, release, and deployment reachability

Maintain a deployment matrix:

| Dimension | Required state |
|---|---|
| Source | Exact commit/tag containing the path |
| Artifact | Official package/binary digest and build configuration |
| Protocol | Enabled amendment/feature/configuration |
| Topology | Standalone, local multi-node, test network, or production/mainnet |
| Validator cohort | Relevant implementation/version distribution |
| Activation | Voting, amendment, emergency release, or immediate behavior |
| Finality | Conditions under which the state becomes canonical |
| Patch rollout | Fixed versions and mixed-version behavior |

A standalone replay can prove deterministic transaction semantics for that
artifact. It cannot by itself prove current mainnet reachability, validator
agreement, finality, or present-day exposure. Require authoritative release and
deployment evidence, or retain `BLOCKED_PRODUCTION_REACHABILITY`.

Never submit a value-creating, consensus-splitting, fund-moving, or high-load
transaction to public networks. Use only an explicitly authorized local fork,
standalone node, private test network, or vendor-provided environment.

## 7. Safe proof ladder and terminal oracle

Advance only as far as authorization and the minimum sufficient proof require:

1. static type/range and value-flow proof;
2. independent arbitrary-precision model;
3. unit/property differential on synthetic values;
4. exact vulnerable-versus-fixed artifact differential;
5. isolated standalone ledger using researcher-owned state;
6. authorized private multi-node consensus replica, if required;
7. vendor-side confirmation of production/mainnet reachability.

The terminal oracle for economic-integrity bugs should bind all applicable
facts:

- transaction result and ledger index;
- committed state hash or equivalent authoritative read-back;
- exact pre/post balances and global supply;
- exact fee/burn delta;
- invariant result;
- canonical/finality status;
- ordinary spendability through a bounded researcher-owned transfer when
  explicitly authorized;
- vulnerable and fixed controls.

Use negligible synthetic denominations and stop before material value creation.
If proving the full exact amount would create meaningful assets, exhaust
resources, or risk network stability, use a reduced local model plus vendor-side
confirmation. Large narrated notional value is not a substitute for a safe
terminal oracle.

## 8. Patch-completeness review

A robust fix usually needs independent controls at both the producer and the
safety invariant:

- checked arithmetic before an aggregate affects debit, credit, path quality,
  or settlement;
- a sufficiently wide or arbitrary-precision invariant accumulator;
- explicit error propagation that aborts and rolls back the whole transition;
- sibling aggregation sites covered across paths/strands/books/batches;
- boundary tests at min/max, one below, exact boundary, one above, and mixed
  sign/order;
- property tests against an independent mathematical oracle;
- vulnerable-versus-fixed artifact tests;
- deterministic behavior across supported builds and validator versions.

Do not accept “wider type” without a reachable-total bound. Do not accept
checked addition when a later conversion narrows the value. Do not accept a
producer-only fix when the invariant remains unable to detect a future sibling
mint path.

## 9. AI-agent and passive-review discipline

An AI-discovered arithmetic chain remains a hypothesis until independently
validated. Keep responsibilities separate:

- the discovery model proposes invariants, arithmetic sites, and composition
  edges;
- deterministic code computes exact mathematical values and compares machine
  results;
- a human or independent verifier re-reads the current call path and build;
- an isolated harness proves commit semantics without public-network effects;
- authoritative release/deployment evidence establishes reachability;
- the program/vendor establishes remediation and disclosure status.

For Hermes or another passive reviewer, provide frozen source slices, type
definitions, transaction traces, proof records, and diffs without the expected
answer. It may identify mismatched arithmetic domains and missing evidence. It
must not execute the replay, contact a node, claim mainnet impact, or promote a
finding.

## 10. Required evidence and verdicts

Return:

- exact protected supply/accounting/consensus property;
- transaction and state-transition graph;
- arithmetic-domain inventory;
- producer-versus-checker exact and machine-width equations;
- constraint and reachability proof;
- source, build, artifact, feature/amendment, and deployment identities;
- baseline, boundary, order-permutation, and fixed-version controls;
- commit, finality, and spendability status as separate fields;
- deterministic oracle identity and artifact hashes;
- prior-art/duplicate status;
- capability-delta and maximum safely demonstrated impact;
- remaining blockers and cleanup.

Use these fail-closed outcomes where applicable:

- `KILL_SINGLE_OVERFLOW_CONTAINED`: downstream invariant rejects and rolls back
  the state.
- `KILL_NO_SHARED_VALUE_FLOW`: arithmetic sites cannot receive one continuous
  attacker-controlled state transition.
- `KILL_BUILD_SEMANTICS_MISMATCH`: the claimed behavior is absent from the
  relevant release artifact.
- `KILL_KNOWN_OR_DUPLICATE`: the same public/fixed root is being replayed.
- `BLOCKED_PRODUCTION_REACHABILITY`: local behavior is proven but current
  deployment or mainnet reachability is not.
- `BLOCKED_COMMIT_OR_FINALITY`: an intermediate success exists without
  canonical state commitment.
- `BLOCKED_SPENDABILITY`: abnormal balance/state exists but the claimed asset
  capability is not safely or authoritatively proven.
- `BLOCKED_CONSENSUS_EQUIVALENCE`: the local topology does not establish the
  required multi-node behavior.

Public-case similarity is a prior-art and falsification aid. A new finding must
be derived from current target-native types, paths, constraints, artifacts, and
deployment evidence.
