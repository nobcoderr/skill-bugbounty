# Authorized Black-Box Evidence Worksheet

## Engagement

- Program/owner:
- Program URL/policy snapshot date:
- In-scope asset:
- Environment:
- Allowed methods:
- Rate/concurrency limits:
- Explicit exclusions:
- Research timestamp/timezone:

## Accounts and synthetic data

- Account A role/tenant:
- Account B role/tenant:
- Account C role/tenant:
- Synthetic object IDs/names:
- How roles were legitimately assigned:

## Baseline

- Normal UI workflow:
- Baseline request A:
- Baseline response/state A:
- Baseline request B:
- Baseline response/state B:
- Expected authorization rule:

## Candidate

- Candidate title:
- Entry point:
- Exact mutation/substitution:
- Candidate request:
- Candidate response:
- Persistent state after request:
- Independent control request:
- Control result:
- Cleanup performed:

## End-to-end trace

`input -> parsing/canonicalization -> routing -> validation -> authentication/session -> tenant/object authorization -> state/cache/job -> sensitive sink -> impact`

- Input:
- Parser/canonicalization:
- Routing:
- Validation:
- Authentication/session:
- Tenant/object authorization:
- State/cache/job boundary:
- Sensitive sink:
- Concrete impact:

## Evidence inventory

- HAR/Burp project:
- Raw requests/responses:
- Screenshots/video:
- Server-visible identifiers/timestamps:
- Tool commands and versions:
- Workspace path:
- Redactions applied:

## Triage

- Verdict: STRONG / MEDIUM / WEAK / KILL
- Scope fit:
- Reproducibility:
- Victim/trust boundary:
- Production reachability:
- Security impact:
- Duplicate/prior-art search:
- Public/known status:
- Invalidation factors:
- Missing proof:
- Safe next action:
- Candidate validity: VALID / INVALID / BLOCKED
