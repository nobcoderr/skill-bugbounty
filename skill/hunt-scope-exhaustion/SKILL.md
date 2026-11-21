---
name: hunt-scope-exhaustion
description: "Finish every feature and every reachable vulnerability class on the current in-scope asset before rotating. If a program has 5 scopes, do not stop on the first empty host. Use automatically during bug bounty. Ordinary coding does not enter this skill."
---

# Hunt scope exhaustion

Authorized offensive-first. A program with several in-scope assets is
not done after one host. Empty findings on scope 1 are a rotate signal
only after that asset was fully audited.

Rule: when hunting, if the target has 5 scopes, do not focus on 1
scope then stop. If the first scope has no finding, continue to the
next scope, but only after the first scope was fully audited: every
feature and every reachable vulnerability class was tried.

## Order

1. Read the official in-scope list. Each listed URL, wildcard, API,
   app, or source tree is one asset. Out-of-scope stays out.
2. `hunt-director` ranks assets (critical impact first). Test **one
   asset at a time**.
3. `target-system-model` maps **every feature** on that asset: pages,
   APIs, roles, objects, workflows, uploads, webhooks, admin, shares.
4. Fill the coverage matrix in
   `references/scope-coverage-matrix.md`. Every reachable `hunt-*`
   class must run against every feature that can feed it.
5. Inside the current asset, spawn class, logic, reentrancy, writeup,
   and validator lanes in parallel. Do not skip a class because IDOR
   missed.
6. Mark the asset `EXHAUSTED` only when every matrix cell is
   `VALIDATED`, `KILLED`, `BLOCKED`, or `UNREACHABLE` with evidence.
7. Then rotate to the next asset. Repeat until every in-scope asset
   has a terminal state.

A validated hit on asset 1 does **not** stop the hunt. Hand it to
`hunt-severity-climb` and keep filling the rest of that asset, then
rotate.

## Stop is forbidden

Do not stop because:

- the first host returned 401/404 on one IDOR guess;
- one class is empty;
- signup on asset 1 failed (test unauth classes, then `BLOCKED` only
  the classes that need that account);
- a Low/Medium/High already exists (climb it, keep covering).

Rotate early only when the whole asset is unreachable (dead DNS,
program-excluded, or a documented paid-wall with no free test path).
Record `BLOCKED` with the exact reason and move to the next asset.

## Agents

Spawn `agents/scope-rotator.md` as the parent coverage owner for the
current asset. It does not submit. `hunt-orchestrator` fires the
class lanes. The parent hunt still owns `REPORT_READY`. Empty cells
are not `NO VALID FINDING`. `hunt-terminal-verdict` speaks only after
every asset is terminal.

```text
PROGRAM=
ASSET_INDEX=
ASSET_TOTAL=
CURRENT_ASSET=
FEATURES=
CLASSES_REACHABLE=
CLASSES_DONE=
COVERAGE_STATE=
NEXT_ASSET=
```
