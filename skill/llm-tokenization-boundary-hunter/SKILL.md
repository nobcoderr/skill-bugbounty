---
name: llm-tokenization-boundary-hunter
description: "Expert authorized AI/LLM bug-bounty workflow for repeated-token and repeated-character attacks, tokenizer/prompt representation gaps, instruction blackout, model divergence, memorization claims, and filter bypasses. Use when evaluating whether tokenization-level adversarial input crosses a real RAG, tenant, tool, API, authorization, confidentiality, or agent-action boundary. Treats Dropbox llm-security and related research as prior art, not as a production target or automatic scanner. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# LLM Tokenization Boundary Hunter

Audit tokenization-level model behavior as one stage of a complete product-security chain. A repeated-token effect is a primitive or research signal, not automatically a bounty finding.

Read `references/repeated-token-llm-security-method.md` whenever this skill is active.

## Routing contract

Start with `mandatory-auto-router` and `authorized-security-autopilot`. Activate this skill only when target evidence shows an AI/LLM surface plus repeated tokens/characters, tokenizer behavior, instruction blackout, divergence, memorization, or a repetition-filter gap.

Route alongside:

- `expert-ai-model-bug-bounty-auditor` for the complete AI product and evidence gates;
- `compositional-exploit-chain-hunter` when model behavior bridges into tools, RAG, memory, identity, or side effects;
- `expert-cache-proxy-parser-differential-hunter` when raw bytes, Unicode, JSON, normalization, chunking, tokenization, or model input disagree;
- `expert-authentication-authorization-hunter` only when a real principal, tenant, object, or capability boundary is evidenced;
- `api-security-reviewer` for inference, agent, retrieval, and tool APIs;
- `authorized-universal-jailbreak-evaluator` only after an explicit request for an official authorized jailbreak program.

Keep source-code and model-supply-chain routes `DEFERRED` unless actual target artifacts support them. Do not activate this skill from the word `token` alone.

## Core chain

Trace:

`attacker-controlled bytes/content -> decoding and normalization -> tokenizer and token IDs -> prompt roles/template/order -> model/router/filter -> output or plan -> deterministic policy and authorization -> tool/RAG/API/action -> protected boundary -> impact`

Every retained candidate must prove the same current deployed path in both directions: forward from the input and backward from the protected effect.

## Mandatory distinctions

- Character repetition and token repetition are different representations; record both.
- A template written inside one `user` message is not evidence of bypassing a real `system` role.
- Instruction betrayal, blackout, divergence, hallucination, or unrelated text alone is usually `KILL`.
- System-prompt text is not automatically a secret or security boundary.
- Suspected memorization is not proven training-data extraction; public-source overlap and model completion must be ruled out statistically.
- A model choosing a tool is not authorization. Prove the backend accepted an unauthorized action under the wrong principal or scope.
- RAG output is not cross-user access until the source document, ACL, unauthorized principal, and retrieval path are proven.
- Long output, latency, token burn, and resource exhaustion are normally `KILL` when DoS or cost issues are excluded.
- Provider filtering of one literal or single-token pattern does not prove the semantic class is fixed; conversely, historical filter gaps do not prove a current model is vulnerable.

## Workflow

1. **Scope:** verify the exact AI product, model/build, eligible class, testing channel, automation/rate/cost limits, and prohibited impacts.
2. **Prior art:** search the Dropbox repository/blogs, academic lineage, program known issues, model cards, release notes, and current vendor statements before testing.
3. **Representation map:** capture raw bytes, decoded text, Unicode normalization, tokenizer/version, token IDs, prompt roles, placement, chunking, and final request.
4. **Matched controls:** compare ordinary input, equal-length/token-budget controls, repeated versus non-repeated structures, and tool/credential/ACL counterfactuals.
5. **Reproducibility:** pin model/router/configuration, use multiple trials, report successes and failures, and separate filter rejection from model behavior.
6. **Boundary bridge:** prove a protected disclosure, cross-tenant retrieval, unauthorized tool/API operation, persistent privileged state change, or explicitly eligible privacy failure.
7. **Backend proof:** capture tool arguments, acting identity, policy decision, authoritative read-back, state before/after, and cleanup.
8. **Falsification:** test public-data contamination, intended access, user consent, server-side checks, model drift, fallback, stochastic variance, and duplicate lineage.
9. **Verdict:** only a current, novel, in-scope chain with controls and manual confirmation can be `STRONG`.

## Safe proof ladder

- **T0 — Historical signature:** repeated-token research resembles the target; hypothesis only.
- **T1 — Current representation:** exact current input becomes the observed tokens and prompt roles.
- **T2 — Model effect:** repeatable behavior differs from token-budget-matched controls.
- **T3 — Bridge:** the effect reaches a real tool, retrieval, policy, memory, or API decision.
- **T4 — Boundary:** researcher-owned A/B resources prove unauthorized disclosure or mutation.
- **T5 — Backend:** identity, authorization decision, state diff, negative control, and cleanup are authoritative.
- **T6 — Reality and novelty:** current deployment, scope, prior art, repeated trials, and manual reproduction all pass.

Only T6 can be `STRONG / MANUALLY_CONFIRMED`.

## Safe testing boundary

Do not run the Dropbox scripts or any live token-search/fuzzing automatically. Live model experimentation requires explicit authorization, model allowlist, maximum requests/tokens/cost, concurrency, abort conditions, evidence handling, and cleanup. Never seek real third-party training data, PII, credentials, or secrets. Use synthetic canaries or an owned local/fine-tuned fixture.

Do not copy known effective token sequences into target tests by default. Start from a minimal, deterministic representation check and a harmless product-boundary canary.

## Remediation lens

- Never use model adherence as an authorization mechanism.
- Enforce tool, object, tenant, and argument authorization outside the model.
- Preserve instruction/content provenance through ingestion, RAG, memory, and tool output.
- Add token-aware repetition and anomaly controls across normalized and tokenized forms; avoid one-literal blacklists.
- Bound input/output tokens, execution time, retries, tool calls, and cost.
- Keep retrieval ACLs independent of model reasoning and recheck them at read/use time.
- Use deterministic validators and confirmation gates for sensitive actions.
- Regression-test current tokenizer/model combinations with matched controls and protected-boundary assertions.

## Hard KILL rules

KILL standalone jailbreaks, hallucinations, prompt-template deviations, harmless system-prompt disclosure, one-off divergence, public/common text, unverified memorization, token burn/DoS outside scope, self-injection, same-privilege actions, historical model behavior, public/fixed/duplicate findings, and any path lacking a real tool/RAG/auth/confidentiality boundary.

The exact historical Dropbox/OpenAI repeated-token findings are public prior art. The repository itself is experimental research code, not evidence of a Dropbox production-backend vulnerability.

## Required output

| Candidate | Verdict | Model/build | Tokenizer | Representation | Model effect | Bridge | Boundary | Impact | Prior art | Manual status |
|---|---|---|---|---|---|---|---|---|---|---|

For each survivor include the target/scope card, exact prompt-role and token map, trial matrix, matched controls, tool/RAG/backend trace, acting principal, state diff, cleanup, duplicate analysis, missing proof, and remediation. If nothing survives, return **NO VALID FINDING**.


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
