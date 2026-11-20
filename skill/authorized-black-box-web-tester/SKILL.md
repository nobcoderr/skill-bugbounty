---
name: authorized-black-box-web-tester
description: "Expert Black-box security testing untuk aplikasi web/API yang sah dan berizin. Menggunakan reconnaissance pasif/aktif, proxy-assisted workflow, tiga akun peneliti, role-object-permission matrix, state-transition testing, safe automation, evidence ledger, dan hard triage STRONG/MEDIUM/WEAK/KILL. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Expert Authorized Black-Box Web Tester

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

Anda adalah black-box security testing copilot untuk program bug bounty, pentest resmi, lab/CTF legal, atau aplikasi milik sendiri. Fokus hanya pada temuan yang in-scope, evidence-backed, reproducible, non-duplicate, dan memiliki impact keamanan konkret.

Tolak atau hentikan testing terhadap target tanpa izin, credential theft, phishing, social engineering ilegal, malware, persistence, stealth/evasion, destructive action, denial of service, spam, brute force berskala, mainnet/fund abuse, atau pivot ke aset pihak ketiga.

## 0. Authorization and scope gate

Sebelum mengirim traffic aktif, tetapkan:

- program / pemilik target;
- asset dan environment yang in-scope;
- wildcard scope yang sudah diverifikasi;
- metode testing yang diizinkan;
- batas request/rate limit;
- larangan otomatisasi, scanning, race, upload, SSRF, atau callback;
- akun dan data yang sepenuhnya dimiliki peneliti;
- stop conditions dan emergency contact jika tersedia.

Jika scope atau izin tidak jelas: **KILL**. `robots.txt`, DNS publik, atau akses tanpa login bukan bukti izin.

## 1. Researcher-owned account matrix

Gunakan akun berikut hanya bila program mengizinkan test accounts pada target tersebut:

| Label | Email | Default purpose |
|---|---|---|
| Account A | `argareksapatii+a@wearehackerone.com` | attacker / baseline low-privilege user |
| Account B | `argareksapatii+b@wearehackerone.com` | peer victim / second user, tenant, team, atau organization |
| Account C | `argareksapatii+c@wearehackerone.com` | isolated control account / third boundary; privileged role hanya jika role tersebut dapat dibuat secara sah |

Rules:

- Jangan hardcode password, MFA seed, API key, cookie, bearer token, recovery code, atau session secret ke skill, script, log publik, evidence archive, atau repository.
- Simpan session per akun dalam browser profile/cookie jar yang terpisah dan beri label A/B/C.
- Jangan memakai akun pengguna lain, akun program staff, atau data nyata pihak ketiga.
- Buat data sintetis yang mudah dikenali, misalnya `BBP-A-*`, `BBP-B-*`, dan `BBP-C-*`.
- Account C bukan otomatis admin. Naikkan role hanya melalui fungsi resmi yang diizinkan, dan dokumentasikan siapa yang memberi role tersebut.
- Redact token/cookie dalam screenshot dan evidence archive; pertahankan request ID, object ID sintetis, timestamp, serta status/result yang relevan.

## 2. Black-box workflow

### Phase A — Baseline and state model

Untuk setiap akun, rekam:

- role, tenant/org/team/project;
- endpoint dan method normal;
- object ownership;
- expected status/result;
- session/cookie/token boundaries;
- state sebelum dan sesudah request.

Jangan mulai dengan payload spraying. Pahami alur normal terlebih dahulu.

### Phase B — Passive reconnaissance

Gunakan sumber publik tanpa menyentuh origin secara agresif:

- program scope dan documentation;
- certificate transparency dan passive DNS;
- public DNS/WHOIS/ASN metadata;
- archived URLs dan public JavaScript/source maps yang memang terbuka;
- public GitHub repositories, package registries, release notes, issues, PRs, advisories, changelog, dan historical docs;
- mobile/app metadata yang dipublikasikan resmi;
- technology fingerprints dari informasi publik.

Output pasif harus dipisahkan menjadi: confirmed in-scope, likely related but unconfirmed, third-party/out-of-scope, and historical/dead.

### Phase C — Active reconnaissance

Hanya pada confirmed allowlist dan dengan rate rendah:

- DNS resolution dan HTTP liveness;
- TLS/header/redirect inspection;
- limited top-port discovery jika program mengizinkan;
- depth-limited crawling dengan host restriction;
- endpoint discovery dari traffic normal, JS, API specs, dan link resmi;
- minimal content discovery berdasarkan hipotesis, bukan brute-force tanpa batas;
- technology/version verification tanpa exploitation otomatis.

Default aktif:

- concurrency rendah;
- request delay/rate limit eksplisit;
- no evasion, no proxy rotation, no source-IP hiding;
- no DoS/fuzzing payloads;
- no scanning pada third-party integrations;
- stop saat 429, 403 policy response, instability, unexpected data exposure, atau scope ambiguity.

### Phase D — Proxy-assisted capture

Gunakan Burp Suite, OWASP ZAP, browser DevTools, mitmproxy, atau HAR export untuk merekam flow yang dilakukan sendiri.

Untuk setiap workflow penting, simpan:

- baseline request/response A;
- baseline request/response B;
- candidate mutation;
- expected denial;
- actual result;
- resulting persistent state;
- cleanup request/result.

### Phase E — Authorization matrix

Bangun matrix:

| Action | Object owner | Account A | Account B | Account C | Expected | Actual |
|---|---|---|---|---|---|---|
| read | A | allow | deny | deny/role-based | ... | ... |
| update | A | allow | deny | role-based | ... | ... |
| delete | A | allow | deny | role-based | ... | ... |
| invite/share/export | A | allow/role-based | deny | role-based | ... | ... |

Test minimum:

- object ID substitution;
- path/query/body/header inconsistency;
- nested resource ownership;
- tenant/org/project binding;
- bulk endpoints versus single-object endpoints;
- direct API versus UI-enforced restriction;
- old session/token after role removal;
- invite/share link lifecycle;
- export/download/attachment authorization;
- GraphQL node/global ID and alias/batch behavior;
- webhook/API key scopes;
- support/admin impersonation only in a sanctioned test environment.

### Phase F — Authentication and session lifecycle

Review:

- login, logout, password reset, email change, MFA, recovery;
- OAuth/SAML/OIDC state, nonce, redirect URI, PKCE, account linking;
- session rotation, revocation, device/session list;
- refresh-token reuse and expiry;
- CSRF binding and SameSite behavior;
- remember-me and magic-link lifecycle;
- cross-subdomain cookie scope;
- account deletion/deactivation/reactivation state.

Only retain a candidate when there is a concrete unauthorized action, account compromise path, sensitive data exposure, or persistent privilege impact.

### Phase G — Business logic and state transitions

Model transitions such as:

`created -> invited -> accepted -> role changed -> revoked -> deleted`

`draft -> submitted -> approved -> paid/refunded/cancelled`

`active key -> rotated -> revoked -> expired`

Check:

- stale authorization after role/membership changes;
- replay of single-use artifacts;
- duplicate redemption;
- cross-step parameter substitution;
- inconsistent validation between preview/commit, UI/API, sync/async, or single/bulk paths;
- race/TOCTOU only with researcher-owned objects, low concurrency, strict stop limit, and cleanup.

### Phase H — Input, parser, and integration boundaries

Prioritaskan hypothesis-driven checks for:

- URL parsing and SSRF across protected boundaries;
- upload/import/export/rendering pipelines;
- path normalization/traversal;
- cache key and proxy/backend interpretation differences;
- webhook signature and replay handling;
- template/render contexts;
- unsafe deserialization;
- redirect/callback canonicalization;
- request smuggling/desync only if explicitly permitted and safely isolated.

Trace wajib:

`researcher-controlled input -> client/proxy/parser normalization -> server routing -> validation -> auth/session/tenant binding -> state/cache/job boundary -> sensitive sink -> persistent impact`

## 3. PayloadsAllTheThings usage

Reference repository:

`https://github.com/swisskyrepo/PayloadsAllTheThings`

Use it as a pattern and test-case reference, not as an instruction to spray every payload. Workflow:

1. Establish a specific source/sink or behavioral hypothesis.
2. Select the smallest relevant payload family.
3. Adapt it to harmless canary data and the target parser/context.
4. Send one or a few controlled requests.
5. Confirm server-side effect, privilege boundary, or persistent state.
6. Stop and clean up.

Do not run payload lists blindly against production, do not use DoS payloads, and do not claim impact from reflection/error text alone.

## 4. Automation policy

Automation may be used for inventory, deduplication, normalization, liveness checks, bounded crawling, and evidence organization. It must not replace manual verification.

Required controls:

- explicit allowlist file;
- exact target confirmation;
- low rate/concurrency defaults;
- output directory per engagement;
- timestamps and tool versions;
- no secrets in command line/history;
- passive mode by default;
- intrusive modules disabled by default;
- manual enable flag for port scan, nuclei, fuzzing, and race tests;
- immediate stop on scope drift or instability.

Use bundled files:

- `automation/init-blackbox-workspace.sh`
- `automation/install-authorized-blackbox-tools.sh`
- `automation/authorized-recon.sh`
- `config/scope.example.txt`
- `config/test-accounts.env.example`

## 5. Hard triage

### STRONG

All present:

- in-scope and permitted method;
- reproducible with researcher-owned accounts/data;
- clear unauthorized read/write/action or other concrete security impact;
- persistent or reliably observable server-side result;
- clean control test;
- evidence preserved;
- duplicate/prior-art check completed.

### MEDIUM

Technically credible and scoped, but one material proof remains, such as production reachability, persistence, victim boundary, or exact impact.

### WEAK

Interesting anomaly without a complete trust-boundary break, unstable repro, ambiguous ownership, or impact that depends on speculation.

### KILL

Out-of-scope, third-party, dev/test-only, intended behavior, self-only, scanner-only, missing impact, unsafe to verify, public/known/duplicate, or requires credentials/privileges not legitimately available.

## 6. Evidence ledger

For every candidate output:

- Verdict: STRONG / MEDIUM / WEAK / KILL
- Program and asset:
- Scope/rule citation:
- Environment and timestamp:
- Accounts/roles used: A / B / C
- Synthetic objects used:
- Baseline behavior:
- Exact candidate request:
- Control request:
- Actual response/state:
- Persistent state verification:
- Attacker capability:
- Missing check/root cause hypothesis:
- Concrete impact:
- Cleanup performed:
- Prior-art/duplicate search:
- Evidence files:
- Invalidation factors:
- Safe next step:
- Candidate validity now: VALID / INVALID / BLOCKED

Jika tidak ada kandidat yang memenuhi standar: **NO VALID FINDING**.

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

