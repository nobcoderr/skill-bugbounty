---
name: adaptive-plan-check-loop
description: "Plan a multi-step task, check the result, retry on failure, then switch to a new technique if it fails again. Use automatically for implementation, debugging, automation, research, and authorized security work with a testable outcome. Do not wait to be named. Skip simple answers."
---

# Adaptive Plan Check Loop

Turn an open-ended task into a bounded evidence loop:

`define success -> plan -> act -> observe -> diagnose -> adapt -> verify or stop`

Do not confuse persistence with repetition. A retry must address evidence from
the previous attempt and change a material assumption, method, or validation
path.

## Start contract

Before acting, record:

- desired outcome and an observable success oracle;
- available inputs, tools, time, and permissions;
- constraints, protected state, cleanup, and abort conditions;
- what may be changed and what must remain untouched;
- retry budget proportional to risk.

Default budget: one primary attempt plus at most three materially different
retry waves. Use fewer waves for external writes or costly actions. Exceed this
budget only when the user explicitly requests continued monitoring or a larger
budget and the next action remains safe and in scope.

For security work, activate the mandatory security router and the narrowest
specialist skills. This skill never grants target authorization. Active recon,
traffic, scanning, exploitation, installs, account creation, or external state
changes require an exact authorized target, scope, and action. Use
`authorized-offensive-tool-loop` for live offensive execution.

## One cycle

### 1. Plan one falsifiable step

Choose the smallest action that can distinguish between competing
explanations. State:

- hypothesis;
- action and expected observable;
- success, negative, and inconclusive outcomes;
- why this is the least-risk useful next step.

Do not execute an entire speculative plan before checking intermediate state.

### 2. Act

Perform only the planned action. Preserve exact command, input, version, target,
and relevant state. Do not silently broaden scope or mutate unrelated data.

### 3. Check

Compare expected and observed results. Prefer direct evidence: exit status,
response status, output, test result, state transition, artifact hash, or UI
confirmation. Classify the cycle:

- `SUCCESS`: the oracle is satisfied;
- `PARTIAL`: progress is real but the oracle is not yet satisfied;
- `NEGATIVE`: the hypothesis was falsified;
- `INCONCLUSIVE`: the observation cannot distinguish causes;
- `BLOCKED`: a required permission, input, service, account, or dependency is
  unavailable;
- `ABORT`: continuing would violate scope, safety, budget, or protected state.

### 4. Diagnose before retrying

Write the failed assumption and the evidence that falsified it. Separate:

- method failure;
- environment or dependency failure;
- wrong hypothesis;
- wrong success oracle;
- authorization or scope blocker;
- transient failure.

Do not label a result transient without evidence. Do not rerun an unchanged
action more than once solely to rule out an evidenced transient condition.

### 5. Adapt materially

Generate two or three alternatives, rank them by information gain, safety, cost,
and likelihood, then choose one. Change at least one material relation:

- input representation or parser path;
- tool, algorithm, or data source;
- actor, object, state order, or consumer;
- environment or dependency assumption;
- verification method or independent oracle.

Renaming a payload, changing cosmetic syntax, retrying the same endpoint alias,
or repeating an unchanged command is `MUTATION_ONLY` and does not consume a new
technique wave; reject it.

## Retry progression

Use this default escalation:

1. **Correction:** fix a concrete execution mistake while keeping the same
   hypothesis.
2. **Alternative method:** test the hypothesis with a different tool,
   representation, or path.
3. **Hypothesis rotation:** abandon the falsified assumption and test a different
   explanation or invariant.

After two consecutive waves produce no new evidence on the same question, stop
that lane. Continue only with a genuinely different in-scope question.

## Verification and finish

When the success oracle first passes, verify it with the cheapest independent
check appropriate to the risk. For important claims, include a negative control
or state-before/state-after comparison. Do not keep retrying after success.

Stop with a clear reason when:

- success is independently verified;
- the retry or cost budget is exhausted;
- the same blocker persists and no safe alternative remains;
- required authorization or user input is missing;
- the next technique would expand scope, risk protected state, or cause an
  irreversible change;
- evidence falsifies the task's premise.

## Loop ledger

Keep a compact ledger so retries do not repeat forgotten failures:

| Wave | Hypothesis | Technique | Expected | Observed | Verdict | Lesson | Next change |
| --- | --- | --- | --- | --- | --- | --- | --- |

At completion, lead with the outcome. Report what worked, the final verification,
material failed approaches, cleanup or remaining state, and any blocker that
still needs user action.

## Delegated retry agent

When a wave fails and a second technique is still in budget, spawn
[`agents/adaptive-loop-agent.md`](agents/adaptive-loop-agent.md) without
waiting to be asked. Give it the exact scope, current ledger, and remaining
question. Do not give it authority beyond the parent task.
