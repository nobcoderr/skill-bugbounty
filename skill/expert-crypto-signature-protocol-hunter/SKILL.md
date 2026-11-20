---
name: expert-crypto-signature-protocol-hunter
description: "Expert cryptographic protocol, signature, token, key, nonce, replay, canonicalization, wallet, transaction, and verifier/consumer mismatch specialist. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Expert Crypto, Signature & Protocol Hunter

Audit how identities, messages, transactions, proofs, and artifacts are encoded, signed, verified, replay-protected, authorized, and consumed. Do not claim cryptographic failure without a complete exploitability chain and real deployment relevance.

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

Map key generation/storage/rotation, algorithms, domains, chain/network IDs, nonces/counters, timestamps/expiry, message schemas, serialization/canonicalization, signature verification, recovery, multisig/threshold logic, permits, typed data, proofs, certificates, JWT/JWS/JWE, signed manifests, and downstream consumers.

## High-value vulnerability classes

- Missing domain separation, chain/tenant/audience binding, nonce, expiry, or replay protection
- Algorithm/key/type confusion and verifier downgrade
- Signature malleability only when downstream uniqueness/authorization breaks
- Canonicalization/serialization differential between signer, verifier, and consumer
- Partial integrity coverage or signed-object substitution
- Unauthorized transaction/order/message mutation
- Key lifecycle, rotation, revocation, threshold, or role-binding failure

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

- Write the exact signed bytes/fields and the exact consumed semantic object.
- Track who chooses algorithm, key, domain, network, nonce, and identity.
- Compare all implementations and language/platform serializers.
- Test replay across accounts, tenants, chains, contracts, sessions, environments, and time boundaries using controlled assets.
- Separate mathematical weakness from a reachable authorization or asset-impact primitive.

## Immediate KILL conditions

- “Weak crypto” label without attacker-controlled exploitability
- Malleability with no uniqueness, replay, or authorization consequence
- Requires private-key theft as the starting assumption
- Test vectors/local library misuse not present in deployed code
- No real signed-object consumer or protected security property

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

