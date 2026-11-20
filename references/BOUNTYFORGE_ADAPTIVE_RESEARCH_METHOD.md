# BountyForge Adaptive Research Method

This method integrates the useful parts of the BountyForge corpus without
preloading its large checklists or inheriting its operational assumptions.

## 1. Evidence-first lane selection

Build a scope card before opening an upstream source:

```text
ASSET=
VERSION_OR_COMMIT=
PROGRAM_OR_OWNER=
ALLOWED_MODE=
EXCLUSIONS=
ATTACKER_POSITION=
OBSERVED_RUNTIME=
ENTRYPOINT=
BOUNDARY=
SINK=
```

Select a lane only when at least two independent signals support it, such as a
Solidity manifest plus contract sources, an OpenAPI document plus an HTTP API,
or an explicit HackenProof triage request plus a report artifact.

## 2. Progressive source loading

Use the source catalog to locate one relevant vendored `SKILL.md`. Extract only:

- a non-obvious invariant or attack relation;
- the minimum target-specific checks needed to falsify it;
- any verifier or output format that materially improves evidence quality.

Do not load broad payload corpora merely because the task is security-related.
Do not replay examples against their original public targets.

## 3. Translate pattern to target-native hypothesis

Every imported idea becomes:

```text
FACT_ANCHOR=
INVARIANT=
ATTACKER_CONTROL=
PRODUCER_GUARANTEE=
CONSUMER_REQUIREMENT=
ONE_VARIABLE_MUTATION=
EXPECTED_ORACLE=
FALSIFIER=
```

A named vulnerability class without those fields is routing context, not a
candidate.

## 4. Verification and capability accounting

Hold attacker authority constant. Compare baseline and probe on the same
release/runtime. Record source trace or immutable operation evidence, state
before and after, authoritative protected-effect read-back, and a safe sibling
or patched control. Compute the exact new read, write, execution, identity,
tenant, financial, or availability capability. If no new capability exists,
terminate that lane.

## 5. Composition

Preserve a primitive only when its resulting capability satisfies a concrete
prerequisite of a newly reachable surface. Chain edges require identity,
environment, privilege, and state continuity. Similar bug classes or adjacent
files do not form an edge.

## 6. Execution boundary

Vendored commands are inert examples by default. Live or state-changing work
requires explicit authorization for the exact target and operation, including
rate/concurrency limits, harmless canaries, abort conditions, and cleanup.
External MCPs, paid services, scanners, fuzzers, and toolchain installers need
separate user authorization.

## 7. Judgment

Apply current-release reachability, duplicate/prior-art screening, and the
program impact boundary gate. Classify unsupported patterns as `HYPOTHESIS`,
zero-delta behavior as `KILL_NO_CAPABILITY_DELTA`, and exhausted lanes as
`NO VALID FINDING`. Only evidence that is both `STRONG` and
`MANUALLY_CONFIRMED` is report-ready.
