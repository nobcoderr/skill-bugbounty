# OPERATOR_LOOP_METHOD:v1

Worksheet for `authorized-offensive-tool-loop`. Fill one cycle at a time.
Do not treat this file as authorization to install or scan.

## Cycle header

- Cycle ID:
- Program / asset:
- Attacker starting privilege:
- Exact question this cycle must falsify:
- Allowed actions this cycle:
- Abort / cleanup:

## Step 1 — Environment

- Runtime / version / WAF / auth class:
- In-scope observations:
- Excluded / off-host hops (do not follow):
- Unknowns that block probing:

## Step 2 — Tool selection

- Candidate tools (max three):
- Chosen tool and binary path:
- Why this is the least-harm probe:
- Tools rejected and why:

## Step 3 — Install

- Missing binary: yes/no
- Exact install authorized: yes/no (quote the user sentence)
- Installer used / skipped:
- Post-install `command -v` / version:

If install was not authorized, skip to analysis-only and mark `BLOCKED`.

## Step 4 — Evaluate

- Argv:
- Expected observable:
- Observed status / body class:
- Capability delta vs previous cycle: none / unknown / named
- Extra-user data seen: no / STOP+PURGE

Step verdict: `CONFIRMED` | `NEGATIVE` | `INCONCLUSIVE` | `OUT_OF_SCOPE` | `ABORT`

## Step 5 — Adjust

- Material relation changed (one only):
- Mutation-only? yes → reject
- Next cycle question **or** stop (`KILL` / `BLOCKED` / `NO VALID FINDING`)

Two consecutive zero-new-evidence cycles on the same question exhaust that
lane. Do not switch targets to avoid `NO VALID FINDING`.
