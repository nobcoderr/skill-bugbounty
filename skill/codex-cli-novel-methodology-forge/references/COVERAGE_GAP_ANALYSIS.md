# Coverage Gap Analysis

The Coverage Gap Analyzer measures which material security-reasoning dimensions
were not actually investigated. It does not find or propose vulnerabilities.

## Inputs

- frozen factual target brief and architecture map;
- V12 research-path and candidate registries;
- killed, blocked, exhausted, active, and pending-verification states;
- frozen methodology-definition and execution registries; and
- local source/dependency availability and current scope card.

## Material gap test

A gap is material only when it has at least two content-addressed factual
anchors, an `UNSEEN` or `PARTIAL` reasoning dimension, a program-relevant
security property, locally available evidence needed to investigate it, and no
semantic equivalence to an exhausted exact root or existing method.

Missing authorization, unavailable runtime, forbidden testing, absent current
consumer, or non-production-only reachability is `BLOCKED`, not material.
“Folder not read”, “try more payloads”, and a suspected bug are not gaps.

Candidate dimensions include an unfollowed trust boundary, decision/use
lifetime, representation projection, authority/ownership change, partial
failure or rollback, safe-component composition, retry/reconnect state,
security-decision cache identity, producer/consumer semantics, creation/use
privilege asymmetry, and locally vendored dependency semantics.

## Output contract

Output no prose outside:

```text
COVERAGE_GAP_COUNT=<derived integer>

GAP_ID=
FACTUAL_BASIS=
WHY_MATERIAL=
WHAT_EXISTING_METHODS_ALREADY_COVER=
WHAT_REMAINS_UNCOVERED=
REQUIRED_NEW_REASONING_PROPERTY=
EVIDENCE_AVAILABILITY=<LOCAL|BLOCKED>
STATUS=<MATERIAL|BLOCKED|REJECTED>
```

Never claim a vulnerability, exploit, bypass, impact, or affected function.
The claimed count must equal the number of `MATERIAL` records.

