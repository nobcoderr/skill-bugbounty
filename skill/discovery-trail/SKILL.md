---
name: discovery-trail
description: "Tuliskan jalur lengkap setiap kali pekerjaan keamanan yang berizin menemukan bug, primitif, atau cara baru keluar dari jalan buntu. Catat rekognisi, domain, alat, yang dicek, yang disingkirkan, yang di-spawn, dan belokan yang tidak diminta. Use automatically after a finding, a killed lead with a creative branch, or a novel unblock. Use when the user says jejak penemuan, discovery trail, /discovery-trail, or how did you find it. Automatically bootstraps the mandatory auto-router. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof. Model-agnostic."
---

# Discovery trail

Setiap bug, primitif, atau macet yang terpecahkan menulis satu jejak sebelum
kesimpulan ditutup. Bentuk isinya ada di `references/trace-template.md`.
Lokasi dan aturan mengangkat trik ada di `agents/discovery-trail-scribe.md`.

Jejak menjawab: domain mana, alat mana, apa yang dicek, apa yang disingkirkan,
apa yang di-spawn, dan belokan mana yang tidak diperintahkan tetapi menemukan
hasil. Belokan dan trik baru lebih berharga daripada daftar tool yang sudah
rutin.

File jejak boleh menyebut target yang sedang dikerjakan. Catatan promote
tidak boleh. Jangan menulis token, cookie, sandi, atau body eksploit ke
dalam salah satu file.

Jawaban di chat tetap singkat. Sebut path file jejak dan kutip bagian
Belokan. Jangan menempel seluruh jalur ke chat.

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
