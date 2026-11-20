---
name: expert-race-condition-state-machine-hunter
description: "Expert race condition, concurrency, TOCTOU, replay, idempotency, distributed state, and business state-machine specialist for safe authorized testing. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Expert Race-Condition & State-Machine Hunter

Identify security invariants that must hold across concurrent or repeated operations, then test them with bounded synchronization and synthetic data. Focus on durable unauthorized state or asset impact, not load generation.

## Expert operating contract

Operate as a senior authorized security researcher, not a scanner narrator. Every retained claim must survive all of these gates:

1. **Authorization and scope:** target, component, account, method, automation level, and vulnerability class are explicitly permitted.
2. **Reality mapping:** prove the exact production/mainnet/stable-release path, version, artifact, configuration, feature flag, deployment, or consumer.
3. **Prior art:** check issues, pull requests, advisories, CVEs, changelog, commits, release notes, documentation, known limitations, and public duplicate families.
4. **End-to-end trace:** connect attacker-controlled input through parsing/canonicalization, validation, state/cache/serialization, authorization/signature/policy, privilege transition, and sensitive sink.
5. **Security boundary:** identify the property broken: identity, tenant/object isolation, privilege, integrity, confidentiality, funds/assets, sandbox, signing, release trust, or availability when explicitly eligible.
6. **Safe reproducibility:** use researcher-owned accounts/data/artifacts and harmless canaries; include a baseline, negative control, state before/after, exact timestamps/versions, and cleanup.
7. **Aggressive falsification:** actively search for upstream checks, downstream constraints, default-off behavior, equal-privilege prerequisites, mitigations, intended trust, and non-production-only reachability.
8. **No hallucination:** never invent files, functions, line numbers, symbols, requests, responses, privileges, versions, deployment, exploitability, or impact.
9. **AI/scanner discipline:** generated hypotheses and scanner hits are inventory only until manually verified on the real path.
10. **Hard verdicts:** retain only bounty-grade candidates. A correct **NO VALID FINDING** is better than a weak result.

## Target and trust-boundary map

Map transactions, locks, optimistic concurrency, idempotency keys, queues, retries, sagas, reservations, balances, quotas, one-time tokens, approvals, invitations, claims, refunds, payouts, withdrawals, mints/burns, role changes, revocation, and distributed caches.

## High-value vulnerability classes

- Double spend, duplicate redemption, over-credit, over-withdraw, inventory/quota bypass
- Check-then-act TOCTOU across authorization, file, signature, or ownership checks
- Replay of one-time actions, webhooks, signatures, permits, or approvals
- Invalid state transitions and stale-version writes
- Lost update, lock scope mismatch, retry side effects, and non-idempotent workers
- Cross-region/replica/cache inconsistency with security impact

## Deadlock and availability routing

When evidence shows a stable circular wait, lock-order inversion, self-deadlock,
recursive logging lock, or RPC-triggered node/service paralysis, route to
`deadlock-lock-graph-dos-hunter` and load its method. Build an exact wait-for
graph from thread, lock, owner, waiter, and source-frame evidence. Keep deadlock,
livelock, starvation, resource exhaustion, slow execution, and crash separate.
Verify the official binary, build definitions, log configuration, listener
exposure, and patched same-config control before retaining availability impact.

## Expert workflow

1. Build the scope and real-world reachability map before testing.
2. Enumerate attacker-controlled inputs, mutable state, trust transitions, and sensitive sinks.
3. Trace forward from each high-quality input and backward from each high-impact sink.
4. Compare sibling paths, platforms, versions, roles, tenants, parsers, serializers, and failure/fallback behavior.
5. Convert each lead into a precise invariant and identify the exact missing or misplaced check.
6. Design a minimal safe proof with baseline, negative control, evidence capture, and cleanup.
7. Attempt to falsify the candidate through upstream/downstream checks, realistic prerequisites, mitigations, and prior art.
8. Apply **STRONG / MEDIUM / WEAK / KILL** and preserve only technically defensible candidates.

## Expert heuristics

- State the invariant mathematically before testing.
- Use low request counts, synchronization barriers, and researcher-owned objects.
- Capture ordering, timestamps, request IDs, transaction IDs, and final authoritative state.
- Compare sequential baseline, concurrent candidate, and protected negative control.
- Distinguish transient UI inconsistency from committed server-side security impact.
- Inspect retry and compensation logic after partial failure.

## Immediate KILL conditions

- Needs stress/DoS volumes or violates rate rules
- Only produces harmless duplicate notifications or transient display errors
- Final authoritative state is correct and no security property is broken
- Requires privileged administrative access equivalent to the claimed impact
- Cannot be reproduced with bounded safe concurrency
- Claims deadlock without a stable wait-for cycle, or upgrades a local stall to
  corruption, confidentiality loss, or systemic impact without direct proof

## Required technical handoff

- Verdict and candidate ID
- Scope and production/mainnet/release proof
- Attacker capability and controlled fields
- Exact files/functions/routes/contracts/components actually observed
- End-to-end call/data/state flow
- Missing invariant and security boundary
- Concrete impact and affected principal/asset
- Safe proof, negative control, evidence references, and cleanup
- Prior-art/duplicate result and invalidation factors
- Single highest-value next verification step

If no candidate survives, output **NO VALID FINDING**.

## Evidence-only output boundary

This skill stops at technical validation and researcher handoff. It may produce:

- a candidate board with **STRONG / MEDIUM / WEAK / KILL**;
- exact scope and production/mainnet/release reachability notes;
- attacker capability, trust boundary, end-to-end call/data flow, and missing invariant;
- safe proof design, negative controls, raw evidence index, invalidation factors, and cleanup;
- minimal fix direction and regression-test ideas.

The output ends at technical validation, evidence indexing, invalidation factors, cleanup, and remediation/test guidance.


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
