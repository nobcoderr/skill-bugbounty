---
name: evidence-linked-api-research-orchestrator
description: "Schema-driven, evidence-linked orchestration for explicitly authorized API security research. Compiles Discovery, OpenAPI, protobuf, and GraphQL surfaces into bounded groups; ties every candidate to replayable operation evidence, calibrated controls, and concrete protected impact. Automatically bootstraps the mandatory auto-router and defaults to an authorized offensive-first posture within exact scope, rate, account, and cleanup limits."
---

# Evidence-Linked API Research Orchestrator

Use machine-readable API descriptions to obtain systematic coverage without
letting model output become evidence. The core unit is a replayable operation
record, not a narrative claim.

## Mandatory boundaries

1. Start through `mandatory-auto-router`, `authorized-security-autopilot`,
   `api-security-reviewer`, and `program-impact-boundary-gate`.
2. Activate only for an explicitly authorized API, owned lab, internal test, or
   in-scope program. Record exact hosts, methods, accounts, rate/concurrency,
   exclusions, abort conditions, and cleanup before active requests.
3. Never collect, recover, enumerate, or replay third-party credentials, API
   keys, cookies, session material, or private resources. Use only
   researcher-owned or program-issued test identities.
4. A public schema, introspection response, undocumented method, API key,
   verbose error, status 200, or identifier oracle is not itself a finding.
5. Never auto-run mass scanning, credential harvesting, broad enumeration,
   state-changing probes, or subagents. Active work requires a sealed allowlist
   and the minimum harmless proof.
6. Preserve V9-V15 and the frozen XCHAIN-v1 archive. This skill is a separate
   live methodology module and does not promote XCHAIN or claim blind-chain
   performance.

The offensive sequence remains:

`attacker objective -> reachable entrypoint -> exploit chain -> authority transition -> protected sink -> concrete impact`

Defensive advice follows proof or falsification unless the user asks for it
first. Offensive-first never expands authorization.

## Activate when

Use this skill when target evidence includes one or more of:

- Google-style Discovery documents;
- OpenAPI or Swagger descriptions;
- protobuf/gRPC service descriptors;
- GraphQL SDL or introspection results;
- a large, standardized API surface where coverage and replayability matter;
- model-assisted authorization testing whose claims need operation-linked
  evidence.

Do not activate from the word `API` alone. A schema artifact, coverage need,
operation-evidence requirement, or equivalent target-native signal is required.

## Campaign card

Before probing, record:

```text
AUTHORIZED_TARGETS=
ALLOWED_METHODS=
EXCLUDED_METHODS=
TEST_IDENTITIES=
OWNED_RESOURCE_IDS=
PERMITTED_AUTH_MODES=
RATE_LIMIT=
CONCURRENCY_LIMIT=
MUTATION_POLICY=
ABORT_CONDITIONS=
CLEANUP_PLAN=
SCHEMA_SNAPSHOT_DIGEST=
```

If these are incomplete, compile the surface and test plan only. Do not send
requests.

## Persistent records

Maintain:

- `METHOD_REGISTRY`: immutable normalized methods and schema hashes;
- `ENDPOINT_GROUP_REGISTRY`: bounded semantic groups and coverage state;
- `OPERATION_EVIDENCE_REGISTRY`: exact request/response/control records;
- `CAMPAIGN_FACT_REGISTRY`: verified IDs, relationships, and target-specific
  protocol facts safe to reuse across groups;
- `REPRESENTATION_LEDGER`: raw/JSON/binary/encoded forms, exact schema, and the
  consumer that decodes each form;
- `BACKEND_EQUIVALENCE_LEDGER`: endpoint aliases, service counterparts,
  deployment cohorts, and evidence that they do or do not share an enforcing
  backend;
- `FAILED_ASSUMPTION_REGISTRY`: rejected interpretations and their falsifiers.

Use `config/OPERATION_EVIDENCE_SCHEMA.json` for operation records. Never store
live secrets in these registries; store redacted references or secret-manager
handles when a permitted harness needs credentials.

## Research workflow

1. **Surface compiler** — load
   [SURFACE_COMPILER_PROMPT.md](prompts/SURFACE_COMPILER_PROMPT.md) and
   [SCHEMA_DRIVEN_CAMPAIGN_METHOD.md](references/SCHEMA_DRIVEN_CAMPAIGN_METHOD.md).
   Normalize exact methods from the supplied schema snapshot, hash definitions,
   and group them by resource and trust boundary.
2. **Probe planner** — load
   [PROBE_PLANNER_PROMPT.md](prompts/PROBE_PLANNER_PROMPT.md). Build the smallest
   role-object-action/control matrix that covers each in-scope method.
3. **Error normalizer** — load
   [ERROR_NORMALIZER_PROMPT.md](prompts/ERROR_NORMALIZER_PROMPT.md) and
   [REJECTION_STAGE_NORMALIZATION_METHOD.md](references/REJECTION_STAGE_NORMALIZATION_METHOD.md).
   Infer rejection stages only from target-native baselines; never transplant
   another provider's error semantics.
4. **Bounded execution** — use a harness that accepts stable method ID, typed
   parameters, owned identity selector, and harmless probe intent. The harness,
   not the model, resolves host, version, verb, and credential material from the
   sealed registry.
5. **Evidence linking** — assign an immutable `operation_id` to every request,
   response, timing observation, and state read-back. Deduplicate identical
   bodies by hash while preserving every auth/config variant.
6. **Privileged-consumer chain analysis** — when a descriptor, queue record,
   workflow feature, hidden task type, identifier oracle, or alternate execution
   path creates a new capability, load
   [PRIVILEGED_CONSUMER_CHAIN_ANALYZER_PROMPT.md](prompts/PRIVILEGED_CONSUMER_CHAIN_ANALYZER_PROMPT.md)
   and [PRIVILEGED_CONSUMER_CHAIN_METHOD.md](references/PRIVILEGED_CONSUMER_CHAIN_METHOD.md).
   Prove each state transition and the actual downstream authority; an error,
   stack trace, accepted configuration, or arbitrary-RPC shape is not terminal
   code execution.
7. **Evidence judge** — load
   [EVIDENCE_JUDGE_PROMPT.md](prompts/EVIDENCE_JUDGE_PROMPT.md) and
   [OPERATION_EVIDENCE_REPLAY_METHOD.md](references/OPERATION_EVIDENCE_REPLAY_METHOD.md).
   Require replay, one-variable negative control, protected recipient/action,
   nonzero capability delta, and cleanup before retention.
8. **Coverage gate** — finish only when every in-scope method is `TESTED`,
   `BLOCKED_WITH_REASON`, or `NOT_APPLICABLE_WITH_SCOPE_EVIDENCE`. Coverage is a
   completeness property, never a finding-quality property.

Use [API_RESEARCH_ROOT_PROMPT.md](prompts/API_RESEARCH_ROOT_PROMPT.md) as the
campaign overlay. Logical roles run sequentially in the current agent; separate
agents require explicit user instruction.

## Evidence contract

A retained candidate must cite immutable operation IDs for:

- authorized baseline;
- unauthorized or cross-boundary attempt;
- malformed/nonexistent-object control where useful;
- authoritative state or protected-data read-back;
- replay result;
- cleanup result for mutations.

The candidate must prove the same resource/action, same environment, and only
the intended authority or ownership variable changed. A report that cannot be
reconstructed from its operation records is `KILL_UNREPLAYABLE_CLAIM`.

## Strict KILL states

- `KILL_SCHEMA_DISCLOSURE_ONLY`
- `KILL_INTROSPECTION_ONLY`
- `KILL_IDENTIFIER_ENUMERATION_ONLY`
- `KILL_ERROR_ONLY`
- `KILL_STATUS_WITHOUT_PROTECTED_EFFECT`
- `KILL_NO_CAPABILITY_DELTA`
- `KILL_NO_UNAUTHORIZED_RECIPIENT_OR_ACTION`
- `KILL_HIGH_ENTROPY_IDENTIFIER_NOT_RECOVERABLE`
- `KILL_PRIVILEGED_CONSUMER_NOT_PROVEN`
- `KILL_SERVICE_IDENTITY_AUTHORITY_INFERRED`
- `KILL_NON_PRODUCTION_TARGET` unless the program explicitly accepts it and the
  exact accepted impact is proved
- `KILL_UNREPLAYABLE_CLAIM`
- `KILL_OUT_OF_SCOPE_OR_UNSAFE_PROOF`
- `KILL_KNOWN_OR_DUPLICATE`

Do not treat staging/sandbox naming as proof of non-production data, and do not
treat production-looking data as proof either. Establish backend/data-plane
equivalence through permitted, researcher-owned markers and official evidence.

## Chaining handoff

If a validated API primitive creates a new capability that exposes a previously
unreachable surface, route it to `exploit-chain-research-orchestrator`. The handoff
must include the operation IDs, entry and post-state, capability delta, identity,
environment, privilege, and state continuity. Do not link findings by thematic
similarity. A chain using two researcher-owned principals must model the
attacker as an explicitly authorized principal set and prove every ACL/approval
transition; it must not silently claim single-identity continuity.

## Source provenance

The article-derived lessons are sanitized in
[BRUTECAT_AI_GOOGLE_RESEARCH_LESSONS.md](references/BRUTECAT_AI_GOOGLE_RESEARCH_LESSONS.md).
The descriptor-to-privileged-consumer lessons from the StubZero case are in
[STUBZERO_CLOUD_RPC_CHAIN_LESSONS.md](references/STUBZERO_CLOUD_RPC_CHAIN_LESSONS.md).
Both are methodology seeds and public prior art, not authorization to reproduce
historical Google requests, use exposed keys, or test any live service.

## Required output

```text
CAMPAIGN_SCOPE=
SCHEMA_SNAPSHOT=
METHOD_COVERAGE=
OPERATION_IDS=
BASELINE=
NEGATIVE_CONTROL=
PROTECTED_EFFECT=
CAPABILITY_DELTA=
REPLAY_RESULT=
CLEANUP_RESULT=
PRIOR_ART_RESULT=
VERDICT=<VALID|BLOCKED|KILL|NO_VALID_FINDING>
```

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
Use defensive controls and hardening mainly as falsifiers or post-proof guidance
unless the user requests them first. This posture never broadens authorization:
preserve scope, safe harbor, harmless proof, rate limits, stop conditions,
cleanup, and prohibitions on destructive, stealthy, credential-stealing,
persistence, evasion, or third-party activity.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

For every security-focused invocation, ensure `mandatory-auto-router` is active,
evaluate the full installed pack through `config/AUTO_ROUTING_MAP.json`, load
this skill only when marked `ACTIVE`, preserve `DEFERRED` and
`NOT_APPLICABLE` routes, and reroute when evidence reveals a new API grammar,
authority boundary, consumer, or capability. Never auto-run operational
automation, public exploits, or subagents. If the router is already active,
reuse that session and do not recursively bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
