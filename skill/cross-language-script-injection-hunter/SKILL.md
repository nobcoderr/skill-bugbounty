---
name: cross-language-script-injection-hunter
description: "Expert authorized source and API workflow for finding and validating injection where one runtime interpolates attacker-controlled values into generated JavaScript, shell, Python, PowerShell, or other source text that is then executed by another interpreter. Use for Ruby heredocs, string templates, temporary scripts, Open3/subprocess wrappers, Playwright automation, hand-written quote escaping, and data-to-code boundary failures. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Cross-Language Script Injection Hunter

Audit the boundary where one language generates source code for another runtime. The core invariant is:

> Untrusted values must cross runtime boundaries as typed data, never as interpolated source text.

Read `references/cross-language-script-injection-rce-method.md` whenever this skill is active. Treat the public `0din-ai/ai-scanner` advisory as prior art, not as a payload library or a new target.

## Evidence-driven routing

Start with `mandatory-auto-router` and `authorized-security-autopilot`. Activate this skill only when evidence shows both:

1. attacker-influenced data reaches a source generator, heredoc, template, string builder, or code emitter; and
2. the generated text reaches an interpreter, runtime, browser-automation worker, temporary script, `eval`, `-e`, stdin, or equivalent execution consumer.

Route alongside:

- `expert-php-ruby-engineer` for Ruby heredocs, `Open3`, `Tempfile`, Rails controllers, and Pundit policies;
- `expert-javascript-typescript-engineer` when JavaScript or Node.js is the generated language or execution runtime;
- the matching source-language and target-language specialists for other runtime pairs;
- `expert-cache-proxy-parser-differential-hunter` for validation grammar versus target-language literal grammar;
- `expert-authentication-authorization-hunter` when route names, namespace, policy calls, tenant membership, or roles affect reachability;
- `expert-source-code-bug-hunter`, `secure-code-reviewer`, `modern-rce-chain-hunter`, and `patch-diff-root-cause-analyzer` for source-to-sink, execution, release, and duplicate proof;
- `compositional-exploit-chain-hunter` when the path crosses controller, policy, service, generated artifact, child runtime, and authority boundaries.

Mark unsupported routes `DEFERRED` or `NOT_APPLICABLE`. Do not infer a language or live surface from a generic keyword.

When the generated target language is a shell command string built around a
remote path/import attribute, also load
`references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md`. Trace the remote
attribute through model persistence and asynchronous worker state before the
shell boundary. A fixed executable plus argv/stdin is the closest safe sibling;
an API wrapper name does not prove that a shell parser is absent.

<!-- DYNAMIC_DATA_EXECUTION_CONSUMER:v1 -->

## Required chain

Build this exact ledger:

`request/config field -> principal and authorization -> source-language validation -> generator context -> emitted source bytes -> script transport -> interpreter invocation -> child-runtime authority -> protected impact`

For each edge, record the exact file/function, stable release, controlled bytes, transformation, consumer, principal, baseline, negative control, and invalidation condition. Forward tracing from input and backward tracing from the interpreter must meet on the same shipped path.

## Mandatory distinctions

- URL, selector, path, or identifier validation is not target-language string encoding.
- A route or module named `admin` is not an authorization check. `verify_authorized` proves that a policy ran, not that it required an administrator.
- Escaping only quotes is unsafe when backslashes are not encoded first; manual escaping remains context-fragile even when order is corrected.
- A generated program must parse completely before the injected statement can execute; a suspicious substring is not a primitive.
- An HTTP success or generic error neither proves nor disproves child-runtime execution. Use an authoritative local marker and control.
- Default seed credentials, broad container permissions, inherited secrets, and network reach amplify impact but are not the interpolation root cause.
- A persisted import path in a string-form process call is a cross-runtime data
  boundary even when no temporary script is written. Prove whether the runtime
  invokes a shell and whether attacker text remains one argv/data value.
- Child-process execution is not required for the root primitive: arbitrary Node/Python/PowerShell statements already cross the code-execution boundary.

## Workflow

1. **Scope and lineage:** verify the exact repository, release, feature, account role, allowed testing mode, and prior art before deep work.
2. **Entrypoint and policy:** trace authentication, CSRF/session requirements, policy predicates, tenant scope, and downstream ownership checks.
3. **Source inventory:** search generated scripts, heredocs, templates, temporary files, interpreter wrappers, and interpolated values.
4. **Grammar comparison:** compare the validation grammar with the actual target-language lexical context, including delimiters, backslashes, newlines, comments, template expressions, and Unicode separators.
5. **Artifact reconstruction:** capture the exact emitted source locally and prove whether controlled data remains data or changes program structure.
6. **Execution proof:** in an isolated owned fixture, use a deterministic harmless marker with a baseline and negative control. Do not begin with shell commands.
7. **Authority and impact:** identify inherited environment, filesystem, network, credentials, and process identity, but prove only the minimum protected boundary needed.
8. **Patch and sibling sweep:** verify the fixed invariant, then inspect every sibling generator and alternate input without relabeling the published root cause as new.
9. **Verdict:** retain only a current, in-scope, non-duplicate path with `STRONG` and `MANUALLY_CONFIRMED` evidence.

## Safe proof ladder

- **C0 — Signature:** source generator and interpreter sink exist.
- **C1 — Control:** current attacker input reaches the generator under a proven principal.
- **C2 — Structure:** local emitted-source inspection shows a grammar breakout or proves safe data preservation.
- **C3 — Parse:** the complete generated artifact parses and a negative control remains inert.
- **C4 — Execute:** an isolated fixture produces a benign, dependency-free local canary in the child runtime.
- **C5 — Boundary:** the canary demonstrates the actual process/tenant/privilege boundary without reading secrets or invoking a shell.
- **C6 — Reality:** stable release, allowed deployment, novelty, cleanup, repeated manual confirmation, and prior-art gates all pass.

Only C6 can be `STRONG / MANUALLY_CONFIRMED`.

## Remediation invariant

Prefer eliminating generated source. Call libraries directly or pass values through a typed data channel such as strict-schema JSON, structured IPC, stdin, or a dedicated data file. If code generation is unavoidable, use the target language's serializer for data literals, keep executable templates static, coerce numeric/boolean options before generation, minimize the child's environment and network authority, and secure temporary artifacts.

Regression tests must cover quote, backslash-before-quote, CR/LF, closing delimiter, comment syntax, template interpolation markers, Unicode line separators, and nested contexts. Assert semantic equality after the child runtime reads the data; do not merely assert that one known payload string is blocked.

## Hard KILL rules

KILL when the path is public/fixed/duplicate, test-only, unreachable, archived, non-shipping, authorized only to equal privilege, safely serialized before execution, or lacks a protected effect. The exact `GHSA-r27j-xxgx-f5vr` / `CVE-2026-41512` `ai-scanner` lineage through version 1.4.0 is public and fixed in 1.4.1.

Never turn this skill into operational exploitation. Do not automate live command execution, environment or credential dumps, secret replay, lateral movement, persistence, reverse shells, destructive actions, or third-party targeting.

## Required output

| Candidate | Verdict | Runtime bridge | Principal | Input | Generated context | Interpreter | Boundary | Prior art | Manual status |
|---|---|---|---|---|---|---|---|---|---|

For each survivor include the release path, authorization trace, exact generated-source evidence, grammar matrix, safe canary, baseline, negative control, cleanup, authority map, patch/sibling analysis, and missing proof. If none survives, return **NO VALID FINDING**.


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

For every explicitly authorized security task, prioritize adversary emulation:
`attacker objective -> reachable entrypoint -> exploit chain -> privilege or authority transition -> protected sink -> concrete impact`. Search for attack paths, bypasses, escalation, code execution, cross-tenant access, credential or data exposure, signing or supply-chain compromise, and fund or integrity impact supported by the target. Use defensive controls, detection, remediation, and hardening primarily as falsifiers or post-proof guidance unless the user explicitly requests blue-team work. Do not force a vulnerability class unsupported by target evidence. This posture never expands authorization: preserve exact scope, safe harbor, harmless proof, rate limits, stop conditions, cleanup, and prohibitions on destructive, stealthy, credential-stealing, persistence, evasion, or third-party activity.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

This skill never operates as a silent standalone module. For every security-focused invocation:

1. ensure `mandatory-auto-router` is active;
2. evaluate all installed skills and supporting artifacts through `config/AUTO_ROUTING_MAP.json`;
3. apply this skill only when marked **ACTIVE**, while recording **DEFERRED** and **NOT_APPLICABLE** routes;
4. load this skill's mapped companion prompts, references, worksheets, and safety protocols;
5. rerun routing after material discoveries that change language, runtime, platform, trust boundary, sink, release reachability, or prior art;
6. never auto-execute operational automation without explicit authorization and safety controls.

If the router is already active, acknowledge the existing routing session and do not recursively bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
