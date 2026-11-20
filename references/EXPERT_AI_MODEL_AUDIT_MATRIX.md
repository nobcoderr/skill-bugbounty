# Expert AI Model Audit Matrix

Use this worksheet only for authorized, in-scope AI-model bug bounty research. Replace every placeholder with observed evidence. Do not use real third-party data.

## 1. Target identity

| Field | Value |
|---|---|
| Program / owner | |
| In-scope product / feature | |
| API / client / region | |
| Account / project / tenant | |
| Model name / snapshot / router | |
| Tokenizer / version / normalization | |
| Tools / connectors / retrieval | |
| Date and exact build/version | |
| Eligible AI vulnerability classes | |
| Exclusions | |

## 2. Security invariant

| Field | Value |
|---|---|
| Protected principal / tenant / asset | |
| Expected invariant | |
| Attacker capability | |
| Attacker-controlled input channel | |
| Privileged context or victim state | |
| Sensitive sink / side effect | |

## 3. End-to-end trace

```text
input -> ingestion/parser -> ACL/provenance -> retrieval/memory/cache ->
prompt/template -> model/router -> policy -> tool selection -> argument validation ->
authorization principal -> backend/sandbox -> state/side effect -> observable impact
```

| Stage | Observed evidence | Missing proof |
|---|---|---|
| Input and ingestion | | |
| Raw bytes / normalization / token IDs | | |
| ACL / provenance | | |
| Retrieval / memory / cache | | |
| Prompt / model / router | | |
| Policy / confirmation | | |
| Tool and arguments | | |
| Acting identity / token scope | | |
| Backend / sandbox | | |
| State before / after | | |
| Impact | | |

## 4. Controlled trials

| Trial | Condition | Model/version | Expected | Observed | Tool/backend action | Pass/fail |
|---|---|---|---|---|---|---|
| B1 | Baseline | | | | | |
| C1 | Candidate | | | | | |
| N1 | Negative control | | | | | |
| F1 | Tool/credential removed | | | | | |
| F2 | Access revoked / tenant changed | | | | | |
| R1..Rn | Repeated candidate trials | | | | | |

Success rate: `___ / ___`

Model or router drift observed: `yes / no / unknown`

## 5. AI-specific hard gates

- [ ] Exact model/version/router and product path recorded.
- [ ] Vulnerability class explicitly eligible.
- [ ] Protected boundary is not merely content policy or output quality.
- [ ] Server/tool/backend accepted an unauthorized operation or disclosed protected data.
- [ ] A/B/C researcher-owned isolation controls used where relevant.
- [ ] Synthetic canaries used; no real third-party data collected.
- [ ] Repeated trials distinguish flaw from stochastic variance.
- [ ] Repetition/tokenization candidates use equal-token-budget and
      non-repeated controls and record prompt roles/position.
- [ ] Baseline, negative control, and counterfactual captured.
- [ ] Tool arguments, acting identity, policy decision, and state diff preserved.
- [ ] Production/release reachability proven.
- [ ] Prior art, documentation, known limitations, and duplicate families checked.
- [ ] Cleanup complete.

## 6. Immediate KILL checks

- [ ] Standalone jailbreak/harmful output/hallucination/bias only.
- [ ] System prompt disclosure without secret or concrete impact.
- [ ] Prompt injection changes text only.
- [ ] Self-injection or attacker-owned context only.
- [ ] Same user explicitly authorized the action; no privilege change.
- [ ] Data was public, user-provided, or legitimately accessible.
- [ ] Single lucky completion; no repeatable controls.
- [ ] Repeated-token blackout/divergence only; no protected-boundary bridge.
- [ ] Local/demo/test-only; no deployed path.
- [ ] Crash/cost/latency/quota only and not explicitly eligible.
- [ ] Known, public, fixed, documented, excluded, or duplicate.

## 7. Verdict

| Field | Value |
|---|---|
| Verdict: STRONG / MEDIUM / WEAK / KILL | |
| Scope confidence | |
| Production/release confidence | |
| Boundary crossed | |
| Concrete impact | |
| Evidence present | |
| Evidence missing | |
| Invalidation factors | |
| Prior-art / duplicate status | |
| Next safe verification step | |
| Minimal fix / regression eval | |
| Candidate validity: VALID / INVALID / BLOCKED | |

If no candidate survives: **NO VALID FINDING**.
