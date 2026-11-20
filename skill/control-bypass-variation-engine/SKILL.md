---
name: control-bypass-variation-engine
description: "Forge ranked web/API control-bypass variation cards across CSRF, CORS, auth, 403/WAF, CSP, redirect, IDOR, SSRF, cache, and rate-limit families, not CORS-only. Automatically bootstraps the mandatory auto-router. Defaults to an authorized offensive-first posture while remaining model-agnostic. Use when the user asks for variasi bypass, POST-to-GET, body-to-query, method override, or other bypass variations besides CORS."
---

# Control Bypass Variation Engine

Turn one **blocked** in-scope request into a ranked set of **representation-mismatch** variation cards. CORS is one family, not the whole engine.

The engine asks: which request dimensions does the **control** key on, and which dimensions does the **sink** still honor? A bypass exists only when those sets differ and the sink still executes the protected action.

Load `references/VARIATION_FAMILIES.md` after the control snapshot. Do not emit a live request unless the current campaign already authorized that exact asset and class.

## When to use

- User asks for `variasi bypass`, bypass besides CORS, POST→GET, body→query, method override, 403/WAF/CSRF/auth bypass ideas.
- A named in-scope request returned 401/403/CORS fail/CSRF fail/WAF/CSP block, and a same-session sibling still proves the sink exists.
- After a CORS-only pass that found nothing, rotate to other control families on the same asset.

Do **not** use this as a generic payload fuzzer, a WAF-spam list, or a substitute for `hunt-cors` / `hunt-csrf` deep dives.

## Hard gates

1. Scope card exists (program, asset, exclusions, testing mode). Missing card → cards only, no live probe.
2. Name the **control** (what rejected) and the **sink** (what would change protected state).
3. Cap **12** cards per blocked request. One material axis per card.
4. Reject `MUTATION_ONLY`: encoding/case/alias churn that does not change which component keys the control.
5. Findings start `HYPOTHESIS_QUARANTINED`. A card is not a finding.
6. Harmless researcher-owned accounts and canaries only. Stop at the first protected effect.

## Engine procedure

### 1. Freeze the blocked request

Record method, path, content-type, parameter locations (query/body/header/cookie/path), auth material **names** only, and the exact reject oracle (`403 CSRF validation failed`, `CORS error`, WAF HTML, `401`, etc.).

### 2. Prove the sink independently

Find a same-session, in-scope sibling that **does** execute the action (normal UI POST, documented API, or already-captured 200). If no sink proof exists, stop: there is nothing to bypass.

### 3. Split control-key vs sink-key

| Dimension | Control likely keys on | Sink often still reads |
| --- | --- | --- |
| HTTP method | POST/PUT only | GET/HEAD/PATCH/DELETE or `_method` |
| Parameter location | JSON/form body | query, path, multipart, header |
| Content-Type | `application/json` | `x-www-form-urlencoded`, `text/plain`, multipart |
| Origin/Referer | exact origin | missing, `null`, trusted substring |
| Token/header | CSRF header or body field | omitted, empty, cookie-only |
| Path prefix | `/api` middleware | `/`, `/internal`, `/graphql`, `/v1` vs `/v2` |
| Authn vs authz | 401 gate | object-level check on another verb |

The Instagram-class CSRF pattern is Family A in the families file: POST without token → 403; GET same route with body fields in the query → action runs.

### 4. Emit ranked cards

Prefer (highest first):

1. Verb + location swap that a **browser** can still send (form GET, simple-content-type POST).
2. Control on middleware, sink on a second parser (GraphQL GET, method override, alternate path).
3. CORS/origin family **after** CSRF/auth/verb families when the goal is a state change, not a cross-origin read.
4. 403/WAF path or header families only when the oracle is the edge, not the app CSRF parser.
5. Encoding-only cards last, and only if they change which parser sees the field.

### 5. Route the surviving family

Load the matching specialist; do not duplicate its full methodology here:

| Family | Load |
| --- | --- |
| CSRF / SameSite / JSON-as-form | Claude-BugHunter `hunt-csrf` |
| CORS / postMessage / null origin | `hunt-cors` |
| Authn/authz / session | `expert-authentication-authorization-hunter` |
| IDOR | `hunt-idor` |
| SSRF | `hunt-ssrf` |
| CSP / XSS sink | `hunt-xss` |
| Open redirect | `hunt-open-redirect` |
| Clickjacking | `hunt-clickjacking` |
| Cache | `hunt-cache-poison` |
| Host / forwarding | `hunt-host-header` |
| HTTP request splitting | `hunt-http-smuggling` |
| Race | `expert-race-condition-state-machine-hunter` |

### 6. One-variable test or stop

If live testing is authorized: change **one** axis, keep the sink fields, compare to the blocked baseline and to an intentional negative control (wrong id, missing cookie, safe sibling). Otherwise return the cards and wait.

## Output

```text
CONTROL_SNAPSHOT
- request: method path content-type
- reject_oracle:
- sink_proof:
- control_key_guess:
- sink_key_guess:

VARIATION_CARD
- id: V1
- family: csrf-verb-location | cors | auth | waf-403 | csp | redirect | idor | ssrf | cache | ratelimit | other
- axis: method | location | content-type | origin | token | path | header | parser
- hypothesis: control keys on A; sink still honors B
- browser_reachable: yes/no (form/img/fetch simple request)
- expected_observable:
- negative_control:
- hunt_skill:
- status: HYPOTHESIS_QUARANTINED
```

Do not dump a 50-payload cheat sheet. Rank, cap, and name the invariant.

## Stop

- 12 cards or two zero-new-evidence waves.
- Control and sink share the same key on every remaining axis.
- `program-impact-boundary-gate` would call the effect equivalent-path or by-design.

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
Use variation cards to find a reachable entrypoint around a named control.
Detection and hardening are secondary unless the user asks for blue-team work.
This posture never expands authorization.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

This skill never operates as a silent standalone module. For every
security-focused invocation:

1. ensure `mandatory auto-router` is active;
2. evaluate all installed skills through `config/AUTO_ROUTING_MAP.json`;
3. apply this skill only when marked **ACTIVE**, while recording **DEFERRED**
   and **NOT_APPLICABLE** routes;
4. load mapped companions, including `references/VARIATION_FAMILIES.md`;
5. rerun routing after material discoveries;
6. never auto-execute operational automation without explicit authorization.

If the router is already active, acknowledge the existing routing session and
do not recursively bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
