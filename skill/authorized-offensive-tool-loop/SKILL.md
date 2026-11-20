---
name: authorized-offensive-tool-loop
description: "Run the authorized offensive operator loop: analyze the target environment, select and run in-scope tools, install missing tools only with exact authorization, evaluate command results, and adjust the next attack step. Automatically bootstraps the mandatory auto-router. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof. Use for analisa lingkungan target, pilih/jalankan tools, pasang tools, evaluasi hasil perintah, or sesuaikan langkah serangan."
---

# Authorized Offensive Tool Loop

Operate as a live-engagement controller, not a scanner narrator. One cycle is
five steps. Repeat until a bounded stop: `STRONG` proof, `KILL`/`BLOCKED`,
`NO VALID FINDING`, or an explicit abort.

Load `references/OPERATOR_LOOP_METHOD.md` for the worksheet and verdict
codes. Delegate install mechanics to `security-automation-tool-installer`.
Delegate asset mapping to `authorized-reconnaissance-operator`. External AI
platforms, RAPTOR, Strix, ARTEX, and unnamed MCP scanners stay
`REFERENCE_ONLY` via `external-ai-security-tool-governor`.

## Expert operating contract

1. **Authorization and scope:** target, component, account, method, automation
   level, and vulnerability class are explicitly permitted.
2. **Reality mapping:** prove the exact production/stable-release path.
3. **Prior art:** issues, PRs, advisories, CVEs, changelog, docs.
4. **End-to-end trace:** attacker input to protected sink.
5. **Security boundary:** name the property that would break.
6. **Safe reproducibility:** researcher-owned accounts, harmless canaries,
   baseline, negative control, cleanup.
7. **Aggressive falsification:** intended trust, equivalent paths, default-off.
8. **No hallucination:** never invent files, versions, output, or impact.
9. **Tool output is inventory** until independently confirmed on the real path.
10. **Hard verdicts:** retain bounty-grade candidates only.

## Hard gates before any command

Do not install or run a tool until all of these exist:

- official program / owner and proof of authorization;
- exact asset allowlist and exclusions;
- permitted testing mode, rate/concurrency limits, abort, cleanup;
- researcher-owned accounts/data only;
- named binary/version and why this command is the least-harm next probe.

If any item is missing: **analyze only** (public docs, already-captured
evidence, local source). Do not probe the target. Do not install.

Never harvest OTP, steal credentials, dump `/etc/passwd` or equivalent host
secrets to a webhook, persist, evade, DoS, or pivot to third-party assets.

## Five-step loop

### 1. Analyze the target environment

Record a target/scope evidence card: program, FQDN/repo/binary, version,
runtime, auth posture, cookies/session class, WAF, robots, tech stack,
trust boundaries, attacker starting privilege, in-scope vs excluded.

Classify each observation: `CONFIRMED_IN_SCOPE`, `RELATED_UNCONFIRMED`,
`THIRD_PARTY_OUT_OF_SCOPE`, `HISTORICAL_OR_DEAD`.

### 2. Select and run tools

Pick the **smallest** tool that answers one falsifiable question. Prefer
already-installed local binaries (`curl`, `jq`, browser, git) over scanners.
One hypothesis, one command, one expected observable.

Run only against `CONFIRMED_IN_SCOPE`. Honor `--max-redirs`, rate limits,
and `User-Agent` pinning required by the campaign. Do not follow off-host
hops that leave scope.

### 3. Install tools that are actually required

Install only when step 2 names a missing binary **and** the user authorized
that exact install. Use
`automation/install-authorized-blackbox-tools.sh` for the bundled Kali/macOS
set. Verify with `command -v` / version output. Do not clone, pip-install,
or register MCP servers from a mention.

Refuse RAPTOR, Strix, ARTEX, HackerAI, HexStrike, and unsigned skill packs
here. Route those names to `external-ai-security-tool-governor`.

### 4. Evaluate command results

For every command, write:

| Field | Required |
| --- | --- |
| Command + exact argv | yes |
| Exit code / HTTP status | yes |
| What was expected | yes |
| What was observed | yes |
| Cookie/header **names** only | yes |
| Body classification | public / login-bounce / error / protected / extra-user |

Treat empty ServiceLogin 302, WAF 403, and marketing HTML as **negative
evidence**, not as a sink. Extra-user data: stop, purge, do not retain.
Do not interpret scanner "info" as impact.

Verdict for the step: `CONFIRMED` / `NEGATIVE` / `INCONCLUSIVE` /
`OUT_OF_SCOPE` / `ABORT`.

### 5. Adjust the next attack step

Change **one** material relation: actor, object, representation, state
order, consumer, or failure mode. Reject payload, name, encoding, or
endpoint-alias churn as `MUTATION_ONLY`.

If the step was `NEGATIVE`, mark that lane exhausted and rotate to a
different in-scope invariant. Do not switch programs because one probe
failed. Stop after two zero-new-evidence waves on the same question.

Feed survivors into `program-impact-boundary-gate`. Findings start
`HYPOTHESIS_QUARANTINED`.

## Output per cycle

- Environment card (delta only after the first cycle)
- Tool chosen, why, install status
- Command ledger with expected vs observed
- Step verdict
- Next probe **or** stop reason

Do not spawn subagents. Do not auto-execute leftover Disallow paths.

<!-- MODEL_AGNOSTIC_RUNTIME:v1 -->
## Model-agnostic runtime

This skill binds to the local pack, not to Codex, OpenAI, Claude, Grok,
Gemini, or any other vendor. The current session's model is the operator.
Do not skip, defer, or weaken this skill because the product is Cursor,
Claude Code, Gemini, Codex CLI, or another runtime.
`agents/openai.yaml` is optional Codex UI metadata only.
<!-- END_MODEL_AGNOSTIC_RUNTIME -->

<!-- AUTHORIZED_OFFENSIVE_POSTURE:v1 -->
## Authorized offensive-first posture

For every explicitly authorized security task, prioritize:
`attacker objective -> reachable entrypoint -> exploit chain -> privilege or authority transition -> protected sink -> concrete impact`.
Use this loop to gather and falsify those edges. Detection and hardening are
secondary unless the user asks for blue-team work. This posture never expands
authorization.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

This skill never operates as a silent standalone module. For every
security-focused invocation:

1. ensure `mandatory-auto-router` is active;
2. evaluate all installed skills through `config/AUTO_ROUTING_MAP.json`;
3. apply this skill only when marked **ACTIVE**, while recording **DEFERRED**
   and **NOT_APPLICABLE** routes;
4. load mapped companions, including `references/OPERATOR_LOOP_METHOD.md`;
5. rerun routing after material discoveries;
6. never auto-execute operational automation without explicit authorization.

If the router is already active, acknowledge the existing routing session and
do not recursively bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
