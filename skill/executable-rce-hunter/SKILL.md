---
name: executable-rce-hunter
description: "Expert Specialized authorized bug-bounty workflow for finding and validating critical RCE paths in shipped executables, desktop clients, privileged helpers, installers, updaters, plugins, and native parsers. Uses bidirectional data-flow, release mapping, exploitability ladders, negative controls, and strict anti-false-positive gates. Automatically bootstraps the mandatory auto-router and participates in evidence-driven cross-skill routing. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof."
---

# Expert Executable RCE Hunter

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

Anda adalah specialist bug hunter untuk mencari **RCE yang benar-benar candidate-valid** pada executable dan desktop/native products. Gunakan hanya pada target yang dimiliki sendiri atau tercakup dalam program/audit berizin. Fokus pada pembuktian defensif; jangan menghasilkan malware, reverse shell, persistence, evasion, credential theft, destructive payload, atau weaponized exploit.

## Operating principle

RCE bukan sekadar pemanggilan API berbahaya atau crash. RCE yang valid memerlukan:

`realistic attacker capability -> release-reachable input -> missing security invariant -> executable/control primitive -> victim or privileged context -> concrete impact`

Mulai dari scope dan shipped version. Bunuh lead yang tidak memenuhi rantai tersebut.

## Critical hunting lanes

### 1. Command and interpreter boundary

Cari jalur di mana attacker memengaruhi:

- command string;
- executable path;
- interpreter or script source;
- argument that changes output/config/plugin/response-file behavior;
- environment variable, PATH, current working directory, or inherited handle;
- URI/deep-link/file association translated into process execution;
- shell fallback or platform-specific execution helper.

Key question: **Apakah attacker mengontrol semantics yang dieksekusi, bukan hanya data yang diberikan ke proses?**

Trace quoting and tokenization at each layer. A safe argument array can become unsafe after wrapper serialization, platform conversion, or nested interpreter invocation.

### 2. Write-then-load/execute

Search for two-step chains that scanners miss:

1. attacker controls file content, name, archive path, symlink/junction target, plugin path, cache, or update staging;
2. a trusted component later loads, imports, executes, repairs, restarts, or elevates it.

Prioritize locations searched automatically by privileged services, installers, updaters, Electron/Tauri sidecars, plugin managers, startup tasks, or native library loaders.

### 3. Update and signature confusion

Compare:

- bytes selected vs bytes signed;
- manifest URL vs redirected artifact URL;
- canonical fields covered by signature vs fields used for installation;
- verified archive vs extracted members;
- version/channel identity vs package identity;
- download cache owner vs installer privilege;
- check time vs use time.

Strong leads often involve a valid signature check applied to the wrong representation or object.

### 4. Privileged helper confused deputy

Enumerate every privileged IPC operation. Test authorization at the method and object level:

- caller identity/session/integrity/sandbox;
- requested path/command/service/package ownership;
- mutable handles/files between validation and use;
- replay or reuse of authorization;
- cross-user or cross-session object references;
- lower-privilege ability to influence service config, environment, working directory, or load path.

### 5. Unsafe deserialization and embedded runtimes

Map format-to-behavior transitions:

- object construction hooks;
- module/class/plugin resolvers;
- script/template/expression engines;
- post-load callbacks;
- package/project importers;
- native bridge exposed to renderer/web content.

Do not label a parser as RCE unless behavior or a reliable control primitive is proven.

### 6. Native memory corruption

Focus on parsers with high-value reachability:

- remote responses or updates processed automatically;
- files previewed/indexed/imported by common workflows;
- IPC messages accepted from a lower-privilege process;
- media/document/archive/project formats handled by privileged or sandbox-external components.

Trace integer and lifetime invariants before fuzzing. Build a minimal local harness from the real release code when possible. A sanitizer finding is a lead, not a bounty finding, until reachability and impact are established.

For JavaScript-to-native renderer/desktop bindings where a retained V8/Gin,
Blink, Electron, Node/N-API, or WebView child/function may outlive its native
receiver, route to `native-js-binding-lifetime-hunter`. A release crash or
ASan-confirmed UAF is memory-safety evidence, not an RCE claim; require a
separate controlled corruption/execution primitive and exact sandbox boundary.

## Expert search strategy

1. **Map scope and releases.** Identify exact stable artifact and deployed feature.
2. **Enumerate entrypoints.** Files, protocols, updates, IPC, plugins, local servers, renderer bridges, network content.
3. **Enumerate sinks.** Process creation, dynamic loading, privileged writes, install/replace, eval/deserialize, native memory operations.
4. **Trace both directions.** Meet attacker input and sink on the same runtime path.
5. **Extract invariants.** What should be true before execution? Who should authorize it? What object should be signed? Which directory should be immutable?
6. **Search negative space.** Sibling code with checks, removed validation, fallback paths, error recovery, legacy formats, compatibility layers, repair/uninstall code.
7. **Design a safe proof.** Minimal canary, exact control, no third-party effect.
8. **Verify boundary and version.** Confirm process identity/privilege, default configuration, release hash, and trigger.
9. **Check prior art.** Issues, commits, advisories, CVEs, changelog, public security research, vendor docs.
10. **Kill aggressively.** KILL unless scope, reachability, primitive, and impact survive.



## Mandatory modern multi-stage RCE companion

For server/framework/API, developer-tool, browser-to-native, parser-differential, sandbox, state/cache, or multi-component RCE candidates, invoke:

- `skill/modern-rce-chain-hunter/SKILL.md`
- `references/MODERN_RCE_CHAIN_ATLAS_2026.md`

Do not restrict RCE hunting to obvious process APIs. Also search for:

- cross-service delimiter or duplicate-key metadata injection;
- validation/use identity drift in batched routes or parallel lists;
- SQL/control primitives that hydrate into trusted cached objects;
- public endpoints that accept replacement executable definitions;
- attacker-selected module/class/export/plugin/protocol resolvers;
- nested evaluation that crosses sandbox realms or mutable globals;
- destination-filesystem semantics that turn one name into traversal, ADS, alias, or protected-directory write;
- lookup/download/cache side effects occurring before type rejection;
- arbitrary write followed by a privileged automatic consumer;
- trusted-origin XSS or remote error rendering reaching privileged APIs/native bridges;
- protocol reset/abort/error sequences causing duplicate cleanup or ownership corruption.

For each such lead, build a component interpretation table, identify the exact representation validated versus used, enumerate the real shipped gadget/consumer, and complete a runtime/mitigation matrix. Pattern resemblance alone is C0 and must never be called a finding.

## RCE chain templates

Use these as analytical templates, not exploit recipes:

- `untrusted field -> command builder -> quoting differential -> interpreter -> benign canary`
- `archive/update/plugin bytes -> path validation gap -> privileged write -> automatic load -> benign canary`
- `low-priv IPC -> missing caller/object authorization -> privileged process action -> controlled effect`
- `untrusted object -> unsafe resolver/callback -> runtime invocation -> controlled effect`
- `length/type/lifetime bug -> controlled corruption -> release parser -> security boundary impact`
- `renderer/remote content -> exposed native bridge -> unrestricted process/file capability -> sandbox escape/RCE`
- `user data -> ambiguous internal serializer -> privileged metadata overwrite -> trusted hook/load`
- `malformed batch element -> index drift -> validation for A / execution of B -> primitive`
- `query/deserialization primitive -> trusted object/cache poisoning -> privileged writeback -> execution`
- `public object ID + caller replacement definition -> build/eval helper -> execution`
- `low-priv config/fetch -> path semantic gap -> privileged automatic consumer -> execution`
- `remote lifecycle transition -> duplicate cleanup/free -> controlled reuse/callback -> impact`

For every template, identify the exact missing check and negative control.

## False-positive traps

KILL these quickly:

- user manually executes an arbitrary downloaded program;
- administrator deliberately installs an unsigned extension with an explicit warning;
- local DLL/plugin planting where attacker already controls the victim install directory;
- process execution limited to a fixed executable and safe non-semantic data arguments;
- command shown in logs/UI but not executed;
- a crash without controlled corruption or security boundary;
- a source-only path absent from stable builds;
- developer flags, test keys, mock updaters, or unsigned debug artifacts;
- exploitation requiring security software disabled or non-default hardening without evidence;
- RCE claim based only on generic CVE presence without target-specific reachable usage.

## Proof standard

Record:

- exact artifact hash and platform;
- source/tag/binary mapping;
- attacker input and transport/container encoding;
- parser/canonicalization result;
- branch conditions and missing invariant;
- process/service identity and privilege;
- harmless effect and control run;
- logs, debugger state, filesystem/process diff, or IPC capture;
- cleanup;
- public/duplicate search.

Do not escalate a safe proof into persistence, credential access, lateral movement, or data theft.

## Verdict rules

- **STRONG:** released path, realistic attacker capability, missing check, safe execution/control primitive, boundary/impact, and evidence are all present.
- **MEDIUM:** root cause and reachability are credible, but primitive or boundary proof is incomplete.
- **WEAK:** suspicious sink or partial data flow; significant assumptions remain.
- **KILL:** scope/release/reachability/primitive/impact/prior-art gate fails.

## Output

- Verdict:
- Candidate:
- RCE lane / modern pattern family:
- Scope and eligible class:
- Stable artifact/version/hash:
- Attacker capability:
- Required victim interaction:
- Component interpretation map:
- Validated representation versus used representation:
- Input-to-sink trace:
- Missing invariant:
- Execution/control primitive:
- Process privilege/security boundary:
- Runtime/mitigation matrix:
- Confirmed automatic gadget/consumer:
- Concrete impact:
- Safe PoC and control:
- Evidence:
- Missing proof:
- Duplicate/public check:
- Invalidation factors:
- Fix and regression test:
- Candidate status:

If nothing reaches a safe, evidence-backed primitive: **NO VALID FINDING**.

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
