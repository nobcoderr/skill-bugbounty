# Fresh Evidence Verifier Node

Use a fresh context containing only the claim, exact scope/revision, raw
evidence, baseline, negative control, and frozen acceptance oracle. Withhold
discovery narrative, agent votes, intended conclusion, and proposed severity.

Return:

```text
CLAIM_REPRODUCED=<YES|NO|BLOCKED>
EVIDENCE_IDENTITY=<PASS|FAIL>
BASELINE=<PASS|FAIL|BLOCKED>
NEGATIVE_CONTROL=<PASS|FAIL|BLOCKED>
CAPABILITY_DELTA=<...>
COUNTEREVIDENCE=<...>
VERDICT=<PASS|FAIL|BLOCKED>
```

Model agreement is not evidence. Only executed tests, immutable operation
records, exact source traces, and authoritative state read-back can pass.
