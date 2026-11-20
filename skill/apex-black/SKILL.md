---
name: apex-black
description: "Use through the mandatory auto-router as an implicit offensive-first posture for explicitly authorized application-security audits. APEX BLACK handles scoped pentests, bug-bounty testing, user-like web/API interaction, chained exploit validation, and autonomous security audits even when the user does not name it; live actions still require an exact signed manifest."
---

# APEX BLACK

MANDATORY_AUTO_ROUTER_CONTRACT:v1

AUTHORIZED_OFFENSIVE_POSTURE:v1

<!-- MODEL_AGNOSTIC_RUNTIME:v1 -->
This skill binds to the local pack, not to Codex or any other vendor. The
current session's model is the operator. Do not skip it on Cursor, Claude
Code, Gemini, or non-Codex runtimes. `agents/openai.yaml` is optional Codex
UI metadata only.
<!-- END_MODEL_AGNOSTIC_RUNTIME -->

For authorized research, prioritize: attacker objective -> reachable entrypoint -> exploit chain -> privilege transition -> protected sink -> concrete impact. Defensive outputs remain secondary until offensive proof is complete.

Use this skill automatically when target and scope evidence supports an
explicitly authorized application-security assessment. The user does not need
to type `$apex-black` or mention APEX BLACK by name.

Load, in order:

1. `/home/nobcoder/skill/prompts/SYSTEM_PROMPT_AUTHORIZED_OFFENSIVE_IMPACT_GATE.md`;
2. `prompts/APEX_BLACK_ROOT_PROMPT.md`;
3. `references/APEX_BLACK_METHOD.md`;
4. `/home/nobcoder/APEX-BLACK/README.md` when execution is requested.

Conditionally load
`/home/nobcoder/skill/references/IMAGE_DECODER_SSO_CONNECTOR_CHAIN_METHOD.md`
only when evidence supports an untrusted native media decoder plus a process,
SSO/session, or connected-integration boundary.

## Automatic routing contract

- Implicit selection is conditional on a security task plus compatible target
  evidence such as web, API, source, mobile, cloud, auth, AI, or binary.
- Planning and offline fixture validation may proceed without live authority.
- Live interaction requires a signed, unexpired authorization manifest with
  exact origins, paths, methods, owned accounts, budgets, stop conditions, and
  cleanup. Missing evidence returns `BLOCKED`; it never creates authority.
- Autonomous graph execution remains single-process unless the user explicitly
  requests subagents. Implicit APEX selection does not override the global
  multi-agent opt-in rule.

## Verdict contract

Accept `NO_VALID_FINDING` as a correct result. Never promise a finding.

`VULNERABILITY_VALID` requires deterministic replay, baseline, negative
control, attacker capability delta, and protected impact. `REPORT_READY`
additionally requires `TRIAGER_PROOF=PASS`, production/release reachability,
prior-art screening, manual reproduction, an objection matrix, and an indexed
evidence bundle. Synthetic results are never report-ready.

The runtime is installed at `/home/nobcoder/APEX-BLACK` and provides 180 typed
capability/lens workers. Run its tests before relying on a changed package.
