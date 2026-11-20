---
name: expert-ai-model-bug-bounty-auditor
description: "Expert workflow for authorized bug bounty auditing of AI model products, inference APIs, agents, RAG, tools, connectors, memory, multimodal pipelines, model hosting, and model supply chains. Retains only reproducible, in-scope security-boundary failures with concrete impact; excludes standalone jailbreaks and quality issues unless explicitly eligible. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Expert AI Model Bug Bounty Auditor

Audit AI-model systems as complete security architectures, not as isolated chatbots. Trace untrusted instructions and model outputs through retrieval, memory, tools, identities, sandboxes, policy layers, backend services, and deployment pipelines. Retain only evidence-backed, bounty-grade security failures.

## Expert operating contract

Every surviving candidate must pass all gates below:

1. **Authorization and scope:** confirm that the exact AI product, model endpoint, feature, account type, tool, connector, model behavior class, automation method, and environment are permitted.
2. **Product reality:** identify the exact model/version/router, system configuration, tool set, retrieval source, tenant, feature flag, deployment, client, API version, and release path tested.
3. **Security boundary:** prove a break in identity, tenant isolation, authorization, confidentiality, integrity, sandboxing, tool policy, protected-network access, billing/resource ownership, model artifact trust, or release trust.
4. **End-to-end causality:** trace attacker-controlled input through prompt construction, tokenization/template, retrieval/memory, model inference, policy checks, tool selection, argument construction, authorization, execution, state change, and observable impact.
5. **Controlled reproducibility:** use researcher-owned tenants, files, connectors, endpoints, resources, and harmless canaries. Preserve baseline, negative controls, counterfactuals, timestamps, model/version metadata, traces, and cleanup.
6. **Stochastic rigor:** do not rely on one lucky completion. Repeat controlled trials, record success/failure rates, and distinguish deterministic product flaws from model variance.
7. **Prior art and exclusions:** check program rules, known limitations, model cards, safety documentation, advisories, changelogs, release notes, public research, issues, and duplicate families.
8. **Aggressive falsification:** search for user confirmation gates, least-privilege tool tokens, output filtering, sandbox boundaries, connector authorization, retrieval ACLs, provenance labels, and intended trust assumptions.
9. **No hallucination:** never invent prompts, hidden instructions, tool calls, model versions, logs, endpoint behavior, tenant data, code paths, or impact.
10. **Evidence-only boundary:** stop at validated technical evidence and remediation ideas.

## Scope gate: model behavior is not automatically a security bug

Before testing, classify the program's AI scope:

- model/provider API;
- consumer chat or enterprise workspace;
- assistants, threads, runs, files, vector stores, fine-tuning, batch, realtime, image/audio/video, or embeddings;
- agent, browser, computer-use, code interpreter, MCP/plugin, function calling, connector, webhook, or external action;
- RAG/indexing/search/memory/personalization;
- model hosting, inference gateway, router, safety classifier, tokenizer, prompt template, adapter, weights, artifact store, deployment, or update pipeline.

Explicitly record whether the program accepts:

- prompt injection or indirect prompt injection;
- jailbreak/safety-policy bypass;
- system-prompt disclosure;
- hallucination, bias, harmful content, or model-quality issues;
- model extraction, inversion, membership inference, or training-data leakage;
- denial of service, quota, metering, or cost amplification;
- third-party connector, plugin, or model-provider issues.

If the class is excluded, or impact remains purely content-policy or quality related, **KILL** it.

## AI system trust-boundary map

Map the full path:

`attacker-controlled content -> ingestion/parser -> metadata/ACL -> chunking/embedding/index -> retrieval/reranking -> prompt assembly/template -> model/router -> safety/policy layer -> tool planner -> argument validation -> authorization principal -> tool/backend/sandbox -> state/side effect -> response/log/memory/cache`

Also map:

- tenant, workspace, project, assistant, thread, run, file, vector-store, fine-tune, API-key, service-account, and connector ownership;
- user/developer/system/tool instruction precedence and provenance;
- model-selected versus server-enforced authorization decisions;
- tool credentials, scopes, audience, tenant binding, and revocation;
- shared caches, semantic caches, conversation memory, retrieval indexes, telemetry, eval stores, and training feedback paths;
- local/remote sandboxes, network egress, filesystem mounts, secrets, metadata endpoints, and privileged helper services;
- model artifacts, adapters, tokenizers, templates, deserialization formats, registries, signatures, provenance, and rollout channels.

## High-value bounty lanes

### 1. Agent and tool authorization failures

Hunt for cases where untrusted prompts, documents, webpages, emails, images, audio, or tool output cause the system to:

- invoke a tool the attacker is not authorized to use;
- act as the victim, workspace, service account, or privileged backend;
- bypass server-side confirmation, policy, role, tenant, object, or capability checks;
- substitute attacker-controlled tool arguments after user approval;
- perform unauthorized send, delete, purchase, publish, transfer, invite, configuration, secret, or data-access actions;
- reuse stale/revoked credentials or cross-account tool state.

A model deciding to call a tool is not itself proof. Show the server accepted the call under the wrong principal or without the required policy.

### 2. Indirect prompt injection crossing a protected boundary

Retain indirect prompt injection only when attacker-controlled external content causes a concrete protected-boundary impact, such as:

- exfiltration of researcher-owned secret canaries from private context to an attacker-controlled endpoint;
- unauthorized access to private files, emails, calendars, repositories, tickets, cloud resources, or internal services;
- unauthorized side effects through tools or connectors;
- persistent poisoning of shared memory, agent policy, retrieval data, or downstream automation;
- bypass of a meaningful human-confirmation or policy boundary.

Mere instruction following, prompt disclosure, or attacker-controlled text echoed to the user is normally **KILL**.

### 2A. Tokenizer and prompt-representation boundary

When repeated tokens/characters, control sequences, Unicode normalization,
tokenizer round trips, instruction blackout, or model divergence are evidenced,
load `llm-tokenization-boundary-hunter` and its repeated-token method. Capture
raw bytes, decoded text, tokenizer/version, token IDs, prompt roles/order,
router/filter behavior, matched token-budget controls, and repeated-trial data.

Treat the model effect as a primitive only. Retain it only when the same current
path reaches an unauthorized tool/API action, cross-tenant RAG or memory read,
protected disclosure, or explicitly eligible privacy boundary. Historical
Dropbox/OpenAI repeated-token behavior is prior art, not current target proof.

### 3. Tenant, object, and context isolation

Test ownership and authorization across:

- assistants/agents, threads/conversations, runs/jobs, messages, files/uploads, vector stores/indexes, fine-tunes, datasets, evals, batches, webhooks, API keys, service accounts, connectors, memories, and generated artifacts;
- IDs in URL paths, JSON bodies, tool arguments, pagination tokens, signed URLs, websocket channels, event streams, cache keys, and export/import objects;
- cross-region, cross-model, cross-version, and asynchronous worker boundaries.

Use A/B/C researcher-owned tenants and synthetic canaries. A cross-object response is not valid until ownership, unauthorized access, and data origin are proven.

### 3A. AI/NL-to-SQL data authority and export fan-out

When an AI analytics endpoint accepts dataset/space selectors, generates SQL,
executes a database tool, retrieves similar questions, or emits signed exports,
load `references/CROSS_BOUNDARY_COMPOSITION_METHOD.md` Lane F and route to the
auth, API/business-logic, and SQL/database specialists. Do not label intended
model-generated SQL as SQL injection unless attacker text crosses a distinct
SQL grammar boundary outside the product's intended query capability.

Require authorization at the final query consumer, not merely an accessible-
datasets endpoint or UI. Bind subject, canonical dataset/space, tenant, row
policy, database principal, memory namespace, streamed response, and export
object. Treat schema/system-prompt disclosure, cross-user memory, unauthorized
query results, and signed full-result URLs as separate effects with separate
proof and remediation. Use only owned synthetic canaries; abort immediately on
unexpected third-party PII or business data.

### 4. Retrieval, memory, and semantic-cache isolation

Look for:

- ACLs applied before indexing but not at retrieval, or vice versa;
- stale ACLs after share/revoke/delete/move operations;
- chunk, embedding, reranker, or semantic-cache keys missing tenant/user/model/policy dimensions;
- retrieval of deleted, revoked, private, or another tenant's content;
- persistent memory writable by untrusted content and later consumed in privileged contexts;
- provenance loss that changes instruction priority or authorization decisions;
- cross-session contamination caused by fallback, retry, batching, or cache reuse.

Prove the source document, ACL/state before and after, exact retrieval path, and unauthorized principal.

### 5. Model endpoint and control-plane authorization

Audit authentication and authorization for:

- model selection and restricted-model access;
- fine-tuning, deployment, endpoint creation, model sharing, adapters, datasets, evals, and checkpoints;
- batch/realtime jobs, logs, traces, usage, billing, quotas, and organization/project controls;
- signed download/upload URLs, webhook callbacks, event streams, and asynchronous result retrieval;
- admin/moderation/review consoles and internal control-plane APIs.

Prioritize cross-project/organization access, privileged mutations, secret disclosure, and ownership bypass. Rate-limit or quota bypass alone requires explicit eligibility and material impact.

### 6. Sandbox, interpreter, browser, and multimodal execution

Trace files, archives, notebooks, code, URLs, documents, images, audio, and model-generated commands into:

- code interpreters and notebook kernels;
- browser/computer-use agents;
- document converters, OCR, media parsers, and preview services;
- plugin/MCP servers and native helpers;
- container runtimes, filesystem mounts, environment variables, local sockets, internal DNS, cloud metadata, and egress controls.

Retain only when the chain proves protected file/network/secret access, sandbox escape, privileged execution, or cross-tenant impact. A crash or arbitrary code execution inside an intentionally disposable, isolated researcher-owned sandbox is not enough unless the program explicitly accepts it.

### 7. SSRF and protected-network access through AI features

Test URL fetchers, browsing, connectors, image/document retrieval, webhook verification, tool schemas, and model-generated requests for:

- localhost, link-local, cloud metadata, internal admin/control-plane, private DNS, redirect, DNS rebinding, alternate IP encoding, protocol smuggling, or parser differential;
- credential forwarding, signed headers, cookies, bearer tokens, or internal identity attached to attacker-selected destinations;
- differences between URL validation, browser fetch, backend fetch, preview, redirect handling, and final connection.

Use only researcher-controlled destinations and harmless canaries. Never probe third-party internal assets.

### 8. Model and inference supply chain

Audit:

- model/adapter/tokenizer/template/config loading;
- unsafe deserialization or executable model formats;
- registry ownership, dependency confusion, unpinned remote code, and mutable references;
- artifact signatures, hashes, provenance, promotion, rollback, cache, and mirror behavior;
- CI/CD for training, evaluation, packaging, deployment, and inference images;
- secrets and privileged runners exposed to untrusted models, datasets, notebooks, or pull requests;
- model router/fallback paths that silently select weaker policy, isolation, or authentication behavior.

Map the exact artifact to a shipped or deployed path. Local proof without a real consumer is **WEAK** or **KILL**.

### 9. Confidentiality and secret handling

Differentiate:

- public or user-supplied text;
- generic system instructions;
- proprietary prompt text without a security boundary;
- secrets, credentials, private tenant data, regulated data, unreleased model artifacts, or protected internal context.

System-prompt extraction alone is normally **KILL** unless explicitly eligible or it exposes actual secrets/security controls whose disclosure enables a concrete attack. Never collect real third-party data; use synthetic canaries.

### 10. Model extraction and privacy research

Only pursue model extraction, inversion, membership inference, memorization, or training-data leakage when explicitly in scope. Require:

- a clear protected asset and attacker model;
- evidence beyond public/common text or user-provided content;
- controls against search-engine/public-source contamination;
- repeated, statistically defensible results;
- minimization and immediate cessation if real personal or third-party data appears.

Do not retain speculative memorization claims.

## Controlled test design

For each candidate, record:

- exact date/time, region, account/project/tenant, client/API, endpoint, model name/version/snapshot, router/fallback behavior, temperature/seed if available, tool set, system/developer configuration, retrieval corpus, and feature flags;
- raw input hash/bytes, decoding and Unicode normalization, tokenizer name/version,
  token IDs or their evidence hash, repeat structure/count, prompt role and
  position, truncation/chunking, and provider-filter outcome when relevant;
- attacker input and where it entered the system;
- victim/privileged context and the security property expected;
- baseline without malicious content;
- candidate test;
- negative control with the same semantics but no attack instruction;
- counterfactual with tool removed, ACL changed, confirmation required, or credential revoked;
- number of trials, success count, failure modes, and model variance;
- tool traces, arguments, authorization principal, policy decision, backend request/response, state before/after, and cleanup.

Prefer minimal canaries such as unique random strings, no-op calendar entries, empty test repositories, synthetic files, harmless HTTP callbacks, and reversible state changes.

## Hard kill filter

Immediately mark **KILL** when the candidate is:

- a standalone jailbreak, harmful-content generation, hallucination, bias, refusal inconsistency, or model-quality complaint not explicitly eligible;
- system-prompt disclosure without secrets or concrete security impact;
- prompt injection that only changes the model's response and does not cross a protected boundary;
- self-injection in the attacker's own conversation, file, tenant, agent, or tool context;
- expected execution of commands explicitly authorized by the same user with no privilege change;
- public information, user-provided content, or data legitimately accessible to the acting principal;
- dependent on compromised admin/root/provider credentials or an intentionally trusted malicious tool/plugin at equal privilege;
- one stochastic completion without repeated controls;
- scanner/model speculation without runtime evidence;
- local/demo/test-only behavior with no production/release mapping;
- a crash, token burn, latency increase, or quota issue without explicit eligibility and concrete impact;
- repeated-token instruction betrayal, blackout, divergence, or suspected
  memorization without a current protected-boundary bridge and matched controls;
- known, public, fixed, documented, excluded, or duplicate;
- dependent on collecting third-party data or unsafe real-world side effects.

## Verdict framework

- **STRONG:** exact in-scope deployed path; repeatable protected-boundary break; server/tool/backend evidence; concrete impact; controls pass; prior-art risk low.
- **MEDIUM:** root cause and security boundary are credible, but one essential proof remains, such as exact production mapping, stable reproduction, victim context, or impact completion.
- **WEAK:** interesting model behavior or architecture concern without sufficient authorization, reachability, causality, boundary, reproducibility, or impact.
- **KILL:** excluded, expected, non-security, unreproducible, unsafe to validate, public/known/duplicate, or disproven.

## Required output

Start with:

| Candidate | Verdict | AI surface | Scope | Model/version | Boundary crossed | Concrete impact | Reproduction | Missing proof |
|---|---|---|---|---|---|---|---|---|

For each candidate provide:

- Candidate and class:
- Verdict: STRONG / MEDIUM / WEAK / KILL
- Program scope fit and exclusions:
- Product/feature/API/client:
- Model/version/router/region/configuration:
- Attacker capability and controlled assets:
- Victim/privileged principal and expected invariant:
- Exact input-to-retrieval/model/tool/backend/state chain:
- Root cause / missing server-side check:
- Security boundary crossed:
- Concrete impact:
- Trial matrix and success rate:
- Baseline, negative control, and counterfactual:
- Tool/backend traces and state before/after:
- Evidence present:
- Evidence missing:
- Prior-art/duplicate checks:
- Invalidation factors:
- Safe cleanup:
- Minimal fix and regression/evaluation tests:
- Candidate validity: VALID / INVALID / BLOCKED

If no candidate survives, answer exactly: **NO VALID FINDING**.

## Evidence-only output boundary

Produce technical candidate validation, evidence indexing, falsification results, and remediation/test guidance.


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
