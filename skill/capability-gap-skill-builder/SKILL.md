---
name: capability-gap-skill-builder
description: "When a needed skill or agent is missing, create the smallest local skill and optional agent, then resume the original task. Use automatically during bug bounty or other multi-step work if no installed skill fits. Do not wait to be named. Do not use for one-off questions, missing binaries, accounts, or authorization."
---

# Capability Gap Skill Builder

Create local capabilities only when doing so improves the current task and
future similar tasks. Absence of a skill name is not a capability gap.

This skill may create or update files under `/home/kali/.codex/skills` because
the user explicitly requested automatic local skill generation. It does not
authorize package installs, repository clones, plugins, MCP registration,
accounts, network traffic, target testing, or any other external action.

## Non-recursion rule

Do not invoke this skill to create another meta-skill builder, router, or copy of
itself. Never recursively create a skill because the newly generated skill lacks
another optional capability. Return to the original task after one gap decision.

## 1. Prove the gap

Write a short gap card:

- original user outcome;
- decision or workflow Codex cannot reliably perform with current guidance;
- evidence that the gap is affecting the task now;
- at least one likely future reuse case;
- observable behavior the new capability must improve;
- why general reasoning or a one-time plan is insufficient.

If the gap is merely a missing binary, dependency, plugin, MCP server, account,
credential, permission, exact target scope, or user choice, do not create a
skill. Route or report that dependency instead.

## 2. Inventory before creating

Search every available skill root and the current task's `AGENTS.md` before
designing anything. Start with names and frontmatter descriptions, then read the
full `SKILL.md` of plausible matches. Check supporting references and agents only
for the candidates that remain relevant.

Prefer these outcomes in order:

1. `REUSE`: an installed skill already covers the behavior;
2. `EXTEND`: one existing skill owns the workflow and needs a narrow addition;
3. `CREATE`: a distinct reusable workflow is genuinely missing;
4. `NO_SKILL`: ordinary reasoning or a one-time solution is sufficient;
5. `NEEDS_AUTH`: the missing capability is actually permission, scope, an
   account, external installation, or another authority boundary.

Do not create aliases, bug-class duplicates, target-specific payload skills, or
skills whose only purpose is to restate global instructions.

## 3. Design the smallest capability

For `CREATE`, define:

- a discriminating lowercase hyphenated name under 64 characters;
- a concise description that says when it applies and when it does not;
- the exact outcome, non-obvious decisions, and safety boundaries;
- only the scripts, references, or assets with a concrete reusable benefit;
- an agent role only when delegation has a distinct input, output, and verdict.

For `EXTEND`, inspect callers and preserve unrelated instructions, metadata,
policy, and resources. Prefer a narrow patch over accumulating universal rules.

Never put passwords, tokens, cookies, OTPs, private keys, mailbox contents,
target secrets, or live credentials into a skill. User preferences may be
encoded only when they are non-secret and genuinely reusable.

## 4. Build through skill-creator

Read and follow `skill-creator` completely. Use its initializer for a new skill
and `apply_patch` for intentional edits. Read the `openai.yaml` reference before
changing UI metadata or invocation policy.

Because this user requested automatic availability, set
`policy.allow_implicit_invocation: true` unless they explicitly request an
explicit-only skill. Automatic discovery does not mean automatic permission for
the actions performed by that skill.

Maximum: create one new skill for one concrete gap in a turn. If several gaps
appear, rank them and handle the one blocking the original outcome; record the
rest as candidates rather than generating a skill tree.

## 5. Validate behavior, not just files

At minimum:

1. run `quick_validate.py` on the completed directory;
2. confirm there are no TODOs, broken relative references, empty resources, or
   duplicate names;
3. test one safe representative request or reason through an observable
   behavioral invariant;
4. verify the description does not attract unrelated tasks;
5. verify authorization and external-state boundaries remain explicit.

Use [`agents/capability-gap-evaluator.md`](agents/capability-gap-evaluator.md)
for an independent gap verdict before `CREATE`. Do not wait for the user to
request that agent. A generated agent is evaluation support, not evidence that
a gap exists.

On this machine write the skill under `/home/kali/.codex/skills/<name>/`,
symlink it from `/home/kali/skill/skill/<name>`, omit
`disable-model-invocation`, set `allow_implicit_invocation: true`, and add a
`skill_routes` entry so it can run without being named. Follow Cursor
`create-skill` for `SKILL.md` shape. Do not put secrets in the skill.

If validation fails, use `adaptive-plan-check-loop`: diagnose, patch once, and
rerun validation. Do not install or publish a broken skill.

## 6. Resume the original task

After a valid `CREATE` or `EXTEND`, read the resulting skill directly and apply
it to the original request in the same turn when possible. Do not stop merely to
announce installation. If the runtime only refreshes discovery on the next
turn, state that limitation without claiming the skill already ran.

## Gap ledger

Report:

- gap card;
- candidate skills checked;
- verdict: `REUSE` / `EXTEND` / `CREATE` / `NO_SKILL` / `NEEDS_AUTH`;
- files created or changed;
- validation and behavioral check;
- how the original task resumed;
- deferred gaps, if any.
