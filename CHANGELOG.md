# Changelog

## 2026.11.14 — Control bypass variation engine

- Added conditional `control-bypass-variation-engine`: from one blocked
  in-scope request, forge ranked control-vs-sink variation cards across CSRF,
  CORS, auth, 403/WAF, CSP, redirect, IDOR, SSRF, cache, and rate-limit
  families. CORS is one family, not the default.
- Canonical family is representation mismatch (example: CSRF POST 403 vs GET
  query that still executes the sink). Cards stay `HYPOTHESIS_QUARANTINED`;
  encoding-only churn is `MUTATION_ONLY`.
- Added the families worksheet, Codex `agents/openai.yaml`, and a Cursor user
  subagent. Live probes still require the current campaign's exact
  authorization.
- Bumped the live package to `2026.11.14-control-bypass-variation-engine-v1`
  (84 skills).

## 2026.11.13 — Modern Web Guidance + AI Web3 Security Hub

- Added conditional `modern-web-guidance` over the pinned
  `GoogleChrome/modern-web-guidance-src` clone (`326dd826`). Reference-only;
  do not run its pnpm/eval toolchain from a mention.
- Added conditional `ai-web3-security-hub` over the pinned
  `pashov/ai-web3-security` catalog (`988f6f4b`). Listed tools stay
  `REFERENCE_ONLY`; prefer already-installed local web3 skills.
- Bumped the live package to `2026.11.13-guidance-web3-hub-v1` (83 skills).

## 2026.11.13 — Authorized offensive tool-loop skill + install hygiene

- Added conditional `authorized-offensive-tool-loop`: analyze the target
  environment, select and run in-scope tools, install only with exact
  authorization, evaluate command results, and adjust the next attack step.
- Added the operator-loop method worksheet, Codex `agents/openai.yaml`, and a
  Cursor user subagent. Install still delegates to
  `security-automation-tool-installer`; RAPTOR/Strix/ARTEX/HexStrike remain
  `REFERENCE_ONLY`.
- Replaced Codex duplicate `REALDIR` skill copies with junctions to the pack or
  Claude-BugHunter clone, keeping truncated Codex copies only for
  `bb-local-toolkit`, `bug-bounty`, and `osint-methodology` (1024-char
  description cap). Distinct Cursor agent bodies replace the identical stubs.
- Previously bumped through `2026.11.13-multi-agent-any-runtime-v1`.
- Declared `MODEL_AGNOSTIC_RUNTIME:v1` on every top-level skill. Skills and
  Cursor agents follow the current session's model (Cursor Grok/GPT/Claude/
  Gemini, Codex CLI, Claude Code, or other). `agents/openai.yaml` remains
  Codex UI metadata only. Autopilot no longer triggers only when the user
  "asks Codex".
- Unbound `codex-cli-multi-agent-audit-orchestrator` from Codex CLI. The
  folder name stays for routing; Cursor `Task`, Codex `spawn_agent`, and
  Claude Code `Agent` are equivalent spawn tools.
- Auto-activate that orchestrator for bug bounty, VRP, and authorized
  hunts. It no longer waits for an explicit subagent request. Ordinary
  product/UI work stays single-agent. Recon, scanners, and installers
  remain explicit-intent.
- Bumped the live package to `2026.11.13-multi-agent-bounty-auto-v1`.

## 2026.10.12 — Agentic security research harness v1

- Added the conditional `agentic-security-research-harness` skill, Codex master
  prompt, passive Hermes evidence prompt, logical harness evidence analyst,
  methodology reference, pinned source catalog, and network-free validator.
- Derived an evidence-state machine in which every human/model/scanner/fuzzer/
  RAG/RE lead begins `HYPOTHESIS_QUARANTINED` and advances only through static
  or build reproduction, clean snapshot, concrete primitive, claimed
  low-privilege reachability, program capability delta, manual confirmation,
  and `TRIAGER_PROOF=PASS`. Demotion and KILL remain append-only first-class
  events.
- Added provenance/expiry-bound research memory, narrowly scoped negative
  results, persistent-session authorization and revocation, stage-specific
  context budgets, independent evidence-only verification, and ROI ordering
  only after scope and eligibility.
- Pinned Harness Kit `db3a53411fe3eff966d0f9061540bd4ee4342887`,
  RAPTOR `17e4227b7797dbcd734b56706e5783e58a4ba62f`, Defending Code
  `d3bea6b5793b5f3d59a75ebe69a58efa88383145`, Baby Naptime
  `f54648d903c167660a18e15cde0523fd54cc425c`, evilsocket Audit
  `d6ee73035f47d9b6ff3353e6fe030395d85e6e08`, Visa VVAH
  `4128e870377850db16cb082115105cc8ee6f1a72`, Anthropic OSS Scanner
  `16e4101f1ca8678ae2122b9f11d8ec02f384c021`, Sequester
  bug-bounty-triage `9684e1bfc876e841f9c789f0b258902b43d461e4`, and REA
  `428eee00fdd0406cdf2b734c9ea14a2bb02da279`.
- Recorded that the user-supplied `carlini/oss-scanner` URL returned HTTP 404
  and used the current canonical `anthropics/oss-scanner` source. Recorded that
  Harness Kit has no license file at the pinned revision and explicitly calls
  itself a non-functional architecture template.
- Treated the Andy Gill success stories, CVEs, bounty outcomes, tool counts,
  performance, and ROI figures as attributed but independently unverified
  upstream claims. No article body, command, payload, or PoC was copied.
- Integrated the harness with the mandatory router, authorized autopilot,
  system overlay, external-tool governor, bug-bounty triage, orchestrator,
  AGENTS, autoload, docs, validation, and routing regression. No repository was
  cloned, installed, registered, started, or executed.
- Bumped the live package to
  `2026.10.12-agentic-security-research-harness-v1-reference-only` while
  preserving frozen V9-V15, V12/V13, XCHAIN, and unrelated target trees.

## 2026.10.12 — WebHackList 2026 AI corpus v1

- Added the conditional `webhacklist-2026-research-corpus` skill, Codex master
  prompt, passive Hermes prompt, logical corpus analyst, corpus-derived method,
  pinned record catalog, and network-free validator.
- Pinned the official WebHackList repository at
  `2f17d6249c178f9b895d2c00536a3009df117afa`, official collection SHA-256
  `3003a015550d9fca47c8843eb6a7f9ec9d2ac3321c59d9873080a5a82ce84dc9`,
  and sources SHA-256
  `3f0db6d47e830ef79c6da8d7b794e9d51bbc19ba95bb21a9cda31c8f6cfe3018`.
- Covered all 299 collection records. Read all 298 archived Markdown sources
  byte-for-byte (12,121,660 bytes; derived archive-root SHA-256
  `4f24ca8755c30916491b579d300915e058c975bb8cc318ce354098e26e2a9476`)
  and reviewed the one unarchived primary URL through an indexed render after
  direct retrieval returned HTTP 403. That final record is explicitly not a
  byte-exact capture.
- Preserved the source collection's preliminary, unranked, AI-collected,
  incomplete, not-community-vetted status. Derived method families are search
  hints, not novelty judgments, duplicate proof, findings, or validation of
  source claims.
- Added corpus-derived representation, authority, protocol/parser, browser,
  agent/tool, execution-consumer, file/renderer, supply-chain, lifecycle,
  arithmetic-invariant, evidence-oracle, and prior-art/impact review lenses.
- Vendored no article body or executable PoC. Repository tooling is MIT while
  preserved research retains original terms; archived commands grant no
  execution or target authority.
- Integrated router, autopilot, system overlay, AGENTS, bug-bounty orchestrator,
  docs, validation, and routing regression while preserving frozen V9-V15,
  V12/V13, XCHAIN, and unrelated target trees.
- Bumped the live package to
  `2026.10.12-webhacklist-2026-ai-corpus-v1-preliminary-prior-art`.

## 2026.10.12 — External AI security tool governance v1

- Added the conditional `external-ai-security-tool-governor` for HackerAI,
  HexStrike AI, AI pentesting platforms, security MCP servers, third-party
  agent skill packs, and autonomous scanner orchestrators.
- Added a Codex master prompt, passive-only Hermes evidence prompt, logical
  external-tool policy analyst, integration methodology, and pinned source
  catalog.
- Pinned HackerAI `main` at
  `44228036160fad2998a09af26049d07b2874ecd8`, its vendored Strix skills at
  `62b496430da5df5e9e79a190e7af6f92529883a3`, and HexStrike AI `master` at
  `d689933ff579d839c676c82b231f8e98326c5f04` for provenance. No repository was
  cloned or executed by this integration.
- Adopted only inert architecture patterns: knowledge does not grant tools,
  parent/child authorization is rechecked, execution is brokered and isolated,
  evidence is append-only, and scanner/model outputs remain hypotheses.
- Recorded HackerAI's additional license-use conditions and HexStrike's broad
  shell/Python/package/file/process/scanner execution surfaces as blockers for
  automatic installation or operation.
- Added router, autopilot, system overlay, AGENTS, orchestrator, documentation,
  validator, and routing-regression integration. The default state is
  `REFERENCE_ONLY`; installation and execution require a separate exact
  authorization.
- Bumped the live package to
  `2026.10.12-external-ai-security-tool-governance-v1-reference-only` while
  preserving frozen V9-V15, V12/V13, and XCHAIN evaluation artifacts.

## 2026.10.12 — Consensus accounting invariant-chain method

- Added `references/CONSENSUS_ACCOUNTING_INVARIANT_CHAIN_METHOD.md` for Web3,
  ledger, node, payment, bridge, and protocol paths where a bounded economic
  transition composes with a bounded safety invariant.
- Added independent arbitrary-precision conservation oracles, arithmetic-domain
  and value-flow ledgers, same-residue composition gates, native release-build
  semantics, constraint solving, rollback, commit/finality/spendability, and
  feature/amendment/validator deployment matrices.
- Extended the evidence-to-terminal-oracle skill, its evidence-chain agent,
  Hermes passive prompt, master prompt, Web3 auditor, compositional-chain
  hunter, router, autopilot, system overlay, global agent instructions, and
  package documentation.
- Preserved the supplied XRPL/rippled narrative and PoC only as unverified
  user-supplied prior art. The live pack does not copy exploit parameters,
  execute Docker or node software, install packages, contact a network, or
  authorize value creation or consensus-risk testing.
- Bumped the live package to
  `2026.10.12-consensus-accounting-invariant-chain-v1-live-audit-only` while
  preserving frozen V9-V15, V12/V13, and XCHAIN evaluation artifacts.

## 2026.10.12 — Evidence-to-terminal-oracle bug-bounty method

- Added the conditional `evidence-to-terminal-oracle-bug-bounty` skill for
  signed client state, cross-purpose secret reuse, unsafe deserialization,
  passive captured-evidence review, long-horizon systems state machines, and
  protected terminal-oracle proof.
- Added a contract-driven master prompt, a passive-only Hermes prompt, and a
  logical evidence-chain analyst role. Passive analysis may produce and rank
  hypotheses, but cannot touch a live target or promote a lead without separate
  deterministic or manual proof.
- Added representation, authority, state-transition, attempt/reliability, and
  terminal-oracle ledgers with one-variable controls, topology/version gates,
  current-release reachability, prior-art screening, and capability-delta
  enforcement.
- Integrated the method into the mandatory router, authorized-security
  autopilot, AI bug-bounty orchestrator, compositional-chain and credential
  specialists, system overlay, autoload entry point, routing map, and routing
  regression tests.
- Preserved the supplied Google DevSite, Gemini CLI, and kvmCTF narratives only
  as user-supplied methodology provenance. Vendor, reward, date, flag, CVE,
  attribution, and “first” claims remain unverified until checked against
  authoritative sources.
- Preserved frozen V9-V15, V12/V13 archives, XCHAIN baselines, and the unrelated
  Hermes target repository. Bumped only the live skill package to
  `2026.10.12-evidence-terminal-oracle-bug-bounty-v1-live-audit-only`.

## 2026.09.21 — Native media decoder → SSO → connector chain method

- Added `references/IMAGE_DECODER_SSO_CONNECTOR_CHAIN_METHOD.md`, derived as a
  safe evidence methodology from the public Hacktron OpenAI/Discourse/libheif
  case and official patch/advisory sources.
- Added exact artifact/backport, format-dispatch, native-primitive,
  process-sandbox, application-authority, SSO/session-binding, connector-scope,
  and terminal-action ledgers with independent chain-edge and KILL gates.
- Added an explicit prohibition on target-reality deception, including
  presenting live services as CTFs or hiding safety signals from agents.
- Added conditional routing, agent/prompt/system integration, a deterministic
  route regression case, validator coverage, and five APEX capability families
  (180 total typed capability/lens workers).
- Preserved frozen V9-V15, V12/V13 archives, and XCHAIN baselines. Bumped only
  the live package to
  `2026.09.21-native-media-sso-connector-chain-v1-live-audit-only`.

## 2026.09.16 — APEX BLACK v0.1 implicit routing

- Added the independent `/home/nobcoder/APEX-BLACK` authorization-first graph
  runtime with 160 typed capability/lens workers, exact-scope adapters,
  attacker-state chaining, clean replay, severity locking, redacted hash-chain
  evidence, kill switches, and offline vulnerable/patched/clean fixtures.
- Added conditional implicit `apex-black` routing for authorized application
  audits, so users need not name the skill. Live interaction still requires a
  signed, unexpired target manifest and a target-specific reviewed probe plan.
- Separated `VULNERABILITY_VALID` from `REPORT_READY`; the latter now requires
  `TRIAGER_PROOF=PASS` in addition to production reachability, prior-art,
  controls, indexed evidence, and human reproduction.
- Replaced the malformed vendored `godmod/SKILL.md` shell heredoc with valid,
  quarantined metadata that grants no operational capability.
- Preserved frozen V9-V15 and XCHAIN baselines. Bumped the live version to
  `2026.09.16-apex-black-v0.1-implicit-routing-live-audit-only`.

## 2026.09.14 — Offensive Research Graph Engineering v1.1

- Route explicit severity-escalation and maximum-proven-severity requests to
  `exploit-chain-research-orchestrator` without activating graph or multi-agent
  execution.
- Add an English regression profile for severity-only escalation and retain
  Indonesian trigger equivalents for `eskalasi severity`, `severity maksimum`,
  and `kunci severity`.

## 2026.09.14 — Offensive Research Graph Engineering v1

- Added the conditional `offensive-research-graph-engineer` for explicitly
  requested red-team, offensive-security, and bug-hunting agent graphs.
- Added dependency-ready DAG scheduling, named producer-to-consumer edges,
  isolated writable workspaces, root-only merge authority, fresh-context
  evidence verifiers, frozen acceptance oracles, bounded queue/concurrency,
  Goodhart-resistant metrics, and zero-new-evidence termination.
- Added logical worker, verifier, and severity-escalation agent contracts plus a
  master prompt, graph methodology, two JSON schemas, routing, autoload, system
  overlay, autopilot, XCHAIN, and impact-gate integration.
- Made Low, Medium, and High severity provisional. Severity is now locked only
  at the maximum demonstrated program impact after a higher edge is proven,
  all realistic capability-expanding edges are falsified, or an explicit
  program, scope, safety, or environment ceiling is recorded.
- Preserved the single-agent default: no child agent, live recon, fuzzer, PoC,
  or state-changing test is started merely because a graph was planned or an
  article described a large fleet.
- Preserved frozen V9/V12/V13/XCHAIN artifacts and changed only the live pack.
  Bumped the version to
  `2026.09.14-offensive-research-graph-v1-live-audit-only`.

## 2026.09.14 — BountyForge Research Suite v1

- Added the conditional `bountyforge-research-suite` adapter and pinned the
  requested `Gabson0x/bountyforge` `skills/` corpus to commit
  `75f5280260ad16c957f36518d5a1384fc943da1a`.
- Vendored 27 unique source directories representing all 32 upstream
  `SKILL.md` paths. Identical Pashov/Fizz copies are deduplicated through the
  source catalog instead of being activated twice.
- Quarantined the malformed `godmod/SKILL.md`, which is a shell heredoc rather
  than valid skill metadata. It is preserved for provenance but is neither
  loaded nor executed.
- Added a focused local skill, agent metadata and logical evidence role,
  adaptive methodology, master prompt, provenance catalog, router mapping,
  autoload/system/autopilot integration, and a positive routing regression.
- Kept upstream commands, scanners, fuzzers, MCP installers, payloads, and
  subagent directions inert behind local authorization and execution gates. No
  upstream operational script was executed during installation.
- Preserved the frozen V9/V12/V13/XCHAIN baselines and changed only the live
  package. Bumped the version to
  `2026.09.14-bountyforge-research-suite-v1-live-audit-only`.

## 2026.09.04 — XCHAIN-LAB-v1 Stateful Exploit-Chain Engine

- Added the independent conditional `exploit-chain-research-orchestrator`
  without modifying or renaming any V9–V15 frozen lineage and without creating
  V16.
- Added persistent attacker-state, primitive, chain-graph, failed-assumption,
  and exploit-attempt contracts; empty state transitions now terminate as
  `KILL_NO_CAPABILITY_DELTA`.
- Added primitive hunter, capability expander, chain linker, gated exploit
  engineer, chain falsifier, chain-value scoring, eight failure classes, and
  one-dimension evidence-driven retry rules.
- Added a standard-library, network-free evidence engine with append-only
  hash-chained registries, incremental record ingestion, sealed campaign
  snapshots, graph integrity checks, exact capability-to-prerequisite edge
  validation, and eight regression tests.
- Added `XCHAIN-LAB-v1`, whose owned synthetic two-stage benchmark passes three
  attacker states, two primitives, one valid edge, one classified failed
  assumption, and two exploit attempts. This is engineering readiness, not an
  XBOW-parity, generalization, zero-day, or production-exploitability claim.
- Extended Chromium/V8 research with type, representation, JIT-assumption,
  GC/lifetime, sandbox-boundary, exploitability, and Chrome chain-linker logical
  roles plus the exact-revision runtime loop.
- Integrated stateful chain routing into the mandatory router, system overlay,
  global autopilot, compositional chain skill, routing map, and validators.
  Added two routing profiles, bringing the deterministic suite to 83.
- Bumped the live package version to
  `2026.09.04-xchain-lab-v1-live-audit-only`.

## 2026.09.03 — AI Data-Authority Composition Lane v1

- Added Lane F, `AI-to-data authorization and result fan-out`, to
  `references/CROSS_BOUNDARY_COMPOSITION_METHOD.md` for natural-language query
  endpoints that select datasets/spaces, generate SQL, execute database tools,
  retrieve shared memories, stream tool/schema material, or emit signed full-
  result exports.
- Classified the root as dataset/object authorization, tenant isolation, or a
  confused deputy rather than SQL injection when SQL generation is intended.
  The entitlement list, query executor, database/RLS principal, memory store,
  event stream, and export object are now modeled as separate enforcement and
  evidence points.
- Added canonical-selector and result-fan-out ledgers, A/B/C owned-tenant
  canaries, `S/C/P` controls, invalid-selector and alias controls, data-origin
  read-back, separate read/write judgments, SAS bearer-capability analysis, and
  an immediate abort/minimization rule for unexpected third-party data.
- Marked the supplied “SQLi Without SQLi” article as an unverified methodology
  seed because no source URL or target identity was supplied. OpenAPI/docs,
  public configuration, AI output, prompt/schema disclosure, and signed URLs
  remain enablers or separate candidates—not proof of unauthorized data access.
- Integrated the lane into the AI-model, authentication/authorization,
  SQL/database, API/business-logic, and compositional skills; the compositional
  agent metadata; AI/compositional/mandatory prompts; system overlay; global
  autopilot; AUTOLOAD; README; pattern atlas; routing map; and validator.
- Added a network-free routing regression that activates the AI, auth, SQL,
  API, web/business-logic, and composition routes while keeping recon, mobile,
  Windows, Web3, and multi-agent routes inactive, bringing the suite to 81
  target/scope profiles.
- Preserved all V9/V12 comparator and V10-V15 frozen lineage artifacts without
  modification. Bumped the live package version to
  `2026.09.03-ai-data-authority-composition-v1-live-audit-only`.

## 2026.09.03 — Cross-Boundary Composition Method v1

- Added `references/CROSS_BOUNDARY_COMPOSITION_METHOD.md`, distilling five
  user-supplied research families into conditional audit lanes: workflow
  shared-context identity collision, Jint/CLR serializer coercion, JWT
  legacy-verifier drift, Active Directory ACL chains, and layered mobile
  request-signing reconstruction.
- Added representation/authority ledgers, actual runtime member and overload
  enumeration, resolver-fallback analysis, directory-edge ledgers, verifier
  matrices, mobile security-property classification, and one-variable `S/C/P`
  controls with authoritative read-back.
- Recorded HackerOne `#3858504`, `#3861550`, and `#3800870` as exact public
  prior-art roots. Kept the supplied fictionalized AD chain and unsourced mobile
  write-up as methodology seeds pending target-specific verification.
- Integrated the method into the compositional skill, its agent metadata,
  compositional and mandatory master prompts, the authorized-offensive system
  overlay, global autopilot, AUTOLOAD, README, routing map, and deterministic
  validator.
- Added five network-free routing regressions covering all five lanes, bringing
  the target/scope routing suite to 80 profiles. No operational payloads,
  credentials, live recon, target interaction, or subagent execution were
  added.
- Preserved all V9/V12 comparator and V10-V15 frozen lineage artifacts without
  modification. Bumped the live package version to
  `2026.09.03-cross-boundary-composition-method-v1-live-audit-only`.

## 2026.09.03 — Chromium/V8 Patch-Led Variant Hunter v1

- Added `chromium-v8-variant-hunter`, a conditional specialist for bounded
  variant analysis anchored to public fixed Chromium/V8 issues, CLs, commits,
  regressions, and release notes rather than random whole-tree ideation.
- Added the derived-metadata equivalence method for auditing base/derived
  equality, hash, cache-key, copy/clone, invalidation, parser-state, and
  deoptimization consumers with one-variable differential pairs.
- Added official-source routing from Chrome Releases to the public issue, fix,
  regression, current source, current-release reproduction, prior-art gate, and
  capability-delta gate. CVE-2026-6307, CVE-2026-0899, and CVE-2021-30632 are
  explicitly historical learning roots, not new candidates.
- Added a current Chrome VRP eligibility boundary: no static-only promotion,
  experimental/unsafe configuration, custom harness, auto-run public exploit,
  or historical vulnerable-build result may become report-ready evidence.
- Integrated the skill, prompt, references, agent metadata, AUTOLOAD route, and
  deterministic routing map. Bumped the live package version to
  `2026.09.03-chromium-v8-variant-hunter-v1-live-audit-only`.

## 2026.09.02 — Counterfactual Methodology Synthesis v9

- Added `counterfactual-methodology-synthesizer`, a conditional post-
  `NO VALID FINDING` module that produces target-native what-if methodologies
  without replaying exhausted payload or vulnerability families.
- Added material-independence checks across actor, ownership, representation,
  order, lifetime, topology, cardinality, consumer, failure, and composition
  axes; cosmetic changes are classified `MUTATION_ONLY`.
- Added a hard two-cycle, three-method-card budget plus required fact anchors,
  deterministic oracle, baseline, safe sibling, negative control, falsifier,
  release and impact plans, harmless proof, cleanup, and stop conditions.
- Added 14 network-free decision regressions and a read-only ledger validator.
  A method only produces a valid finding when the resulting candidate reaches
  the unchanged `STRONG + MANUALLY_CONFIRMED` gate.
- Integrated the conditional transition into the local system prompt, router,
  autopilot, novelty and cascade engines, agent metadata, README, and routing
  protocol. Bumped the live package version to
  `2026.09.02-counterfactual-methodology-synthesis-v9-live-audit-only`.

## 2026.09.02 — Program Impact Boundary Gate v8 Positive Controls

- Added WordPress reports `#3931777` and `#3931771` as a separate structured
  Resolved/rewarded positive-control corpus.
- Added promotion rules for low-privilege owned input crossing into arbitrary
  filesystem deletion or higher-privilege browser execution, with shipped
  reachability, authoritative read-back, and adjacent-role/cross-owner controls.
- Added multi-consumer tracing: one stored representation must be followed into
  every later authority-bearing sink, while report separation requires a
  materially distinct terminal effect and consumer fix.
- Marked the exact disclosed and fixed WordPress roots as novelty burn entries;
  future work requires a current-release bypass or distinct consumer.
- Extended system, master, skill, agent, routing, and regression layers and
  bumped the live package version to
  `2026.09.02-program-impact-boundary-gate-v8-positive-controls-live-audit-only`.

## 2026.09.02 — Program Impact Boundary Gate v7 and System Overlay

- Added seven unique user-supplied adjudications to the structured negative-
  control corpus, bringing it to 70 cases. Reused the existing Discourse
  `#3739926` case instead of duplicating it.
- Added explicit falsifiers for known/duplicate roots, program-excluded updater
  sandbox execution, synthetic consumers that ignore unverified identity
  status, caller-manufactured library lifecycles, unsecured transport threat
  models, unusual local launch prerequisites, and niche builds without a
  current shipped consumer.
- Added an always-active authorized offensive impact system-prompt overlay and
  linked it through global AGENTS instructions, mandatory routing, autopilot,
  skill prompts, and agent metadata.
- Extended deterministic regression tests and routing validation for all new
  cases and the mandatory system-prompt route.
- Bumped the live package version to
  `2026.09.02-program-impact-boundary-gate-v7-system-overlay-live-audit-only`.

## 2026.08.29 — Authorized Offensive Red-Team-First v1

- Made authorized offensive red-team analysis the model-neutral default across
  all 64 live skills while preserving exact authorization and harmless-proof
  requirements.
- Updated all 23 master prompts and all 13 existing agent metadata prompts to
  prioritize attacker objectives, reachable entrypoints, exploit chains,
  privilege transitions, protected sinks, and concrete program impact.
- Retained legacy `*-defensive-researcher` route names for compatibility while
  changing their operating posture to authorized offensive exploitability and
  privilege-boundary research.
- Kept defensive controls, detection, remediation, and hardening as hypothesis
  falsifiers or post-proof guidance unless blue-team work is explicitly asked.
- Applied the posture to GPT-5.6 Sol, GPT-Daybreak Blue, GPT-5.5, Terra, Luna,
  and other models through shared local instruction surfaces; no model-specific
  internal weights or hosted system prompts are modified.
- Added regression validation for the policy, skill, prompt, and agent layers.
  Frozen V12 and B8 remain untouched.
- Bumped the live package version to
  `2026.08.29-authorized-offensive-red-team-first-v1-live-audit-only`.

## 2026.08.28 — Program Impact Boundary Gate v6

- Added 9 user-supplied Not Applicable adjudications, bringing the structured
  negative-control corpus to 63 cases.
- Separated adjudication status from closure basis so procedural inactivity is
  never treated as a merits-based security rejection.
- Added `KILL_ENVIRONMENT_MISMATCH`, production stack equivalence, canonical
  consensus/finality, exact browser top-level-navigation controls, and dated
  submission-time reachability checks.
- Added exact privacy-promise scope, verifier trust-anchor analysis, explicit
  excluded-impact handling, and report-readiness/deadline gates.
- Added 12 deterministic adversarial decision scenarios plus a valid positive
  control, preventing both promotion of known N/A/Informative patterns and a
  trivial reject-everything implementation.
- Updated the live skill, prompts, router, triage, autopilot, AGENTS surfaces,
  validators, and manifest. Frozen V12 and B8 remain untouched.
- Bumped the live package version to
  `2026.08.28-program-impact-boundary-gate-v6-live-audit-only`.

## 2026.08.28 — Program Impact Boundary Gate v5

- Added 10 user-supplied Informative adjudications, bringing the structured
  negative-control corpus to 54 cases.
- Added authorization-issuance-time analysis for forward-looking denylists,
  pre-issued attestations, and explicitly retroactive policy changes.
- Added parent/derived credential lineage and independent revocation analysis,
  including whether secondary authority was already obtainable while the parent
  credential remained valid.
- Added operation-specific signed-scope and temporal snapshot trust-equivalence
  checks; different operations or heads do not imply a boundary when authority
  and content principal remain unchanged.
- Added a primitive-to-protected-consumer gate for wrong-origin authentication
  material, local file effects, uninitialized values, callback routing, and
  generated example code.
- Updated the live skill, prompts, router, triage, autopilot, AGENTS surfaces,
  validators, and manifest. Frozen V12 and B8 remain untouched.
- Bumped the live package version to
  `2026.08.28-program-impact-boundary-gate-v5-live-audit-only`.

## 2026.08.28 — Program Impact Boundary Gate v4

- Added 9 user-supplied Informative adjudications, bringing the structured
  negative-control corpus to 44 cases.
- Added an explicit promised-property check so integrity/authenticity controls
  such as signatures are not misreported as confidentiality guarantees.
- Added control-plane versus data-plane permission scoping and comparison of
  malformed parser inputs with well-formed equivalent requests.
- Added collision-feasibility evidence for attacker knowledge, entropy,
  persistence, event prevalence, attempt budget, and measured success rate.
- Added counterfactual-defense analysis that holds attacker authority constant;
  mitigations that merely add a step through the same attacker-controlled trust
  source or channel do not prove a capability delta.
- Updated the live skill, prompts, router, triage, autopilot, AGENTS surfaces,
  validators, and manifest. Frozen V12 and B8 remain untouched.
- Bumped the live package version to
  `2026.08.28-program-impact-boundary-gate-v4-live-audit-only`.

## 2026.08.28 — Program Impact Boundary Gate v3

- Added 13 user-supplied Informative adjudications, bringing the structured
  negative-control corpus to 35 cases.
- Added `KILL_NO_PRODUCTION_REACHABILITY` for technically valid source behavior
  on archived, unmaintained, or source-only components when the program requires
  a current live production consumer.
- Added exploit-realism gates for host/network prerequisites and races:
  attacker-controlled trigger, default/common topology, measured timing window
  and success rate, and rejection of lab-only locks or forced ordering as proof
  of production exploitability.
- Added explicit lifecycle-contract analysis separating role change, password
  change, logout, credential/client deletion, synchronization, cache invalidation,
  and persistent-object ownership.
- Added negative controls for active-content viewer consent, forwarding-header
  topology, layered validation summaries, trusted schema/codegen inputs,
  defense-in-depth reauthentication, and valid authorization bugs below a
  program's impact floor.
- Updated the live skill, master prompts, router, triage, autopilot, AGENTS
  surfaces, validators, and manifest. Frozen V12 and B8 remain untouched.
- Bumped the live package version to
  `2026.08.28-program-impact-boundary-gate-v3-live-audit-only`.

## 2026.08.28 — Program Impact Boundary Gate v2

- Added 10 user-supplied Informative adjudications to the negative-control
  corpus, bringing it to 22 cases without turning historical patterns into a
  blacklist.
- Added explicit production-product versus demo/sample/quickstart/local-
  development/development-preview classification and a program impact-ceiling
  check. A complete technical chain is not promoted when its strongest effect
  remains inside a non-production context the current program does not reward.
- Added defended-threat-model and guarantee-versus-defense-in-depth checks for
  same-local-user configuration, self-hosted workdirs, unrestricted same-UID
  execution, documented DEBUG body logging, and equivalent supported resolver
  or dependency paths.
- Added `KILL_NON_PRODUCTION_TARGET`, `KILL_THREAT_MODEL`, and
  `KILL_KNOWN_OR_DUPLICATE`. Known/duplicate status remains independent of
  technical validity.
- Updated the always-active skill, prompts, routing instructions, global AGENTS
  surfaces, deterministic corpus regression, and routing validator. The frozen
  V12 package and B8 auditor snapshots remain outside this live-pack update.
- Bumped the live package version to
  `2026.08.28-program-impact-boundary-gate-v2-live-audit-only`.

## 2026.08.28 — Program Impact Boundary Gate

- Added the always-active `program-impact-boundary-gate` to reject technically
  real but by-design, equal-authority, consented-trust, severity-ineligible, or
  impact-unproven candidates before expensive PoC work and reporting.
- Added a two-pass impact contract based on
  `starting capability -> exploit transition -> resulting capability`, requiring
  a nonzero capability delta across a boundary recognized by the current
  program, an unauthorized protected recipient/action, realistic conditions,
  authoritative read-back, and the current written severity floor.
- Distilled 12 user-supplied HackerOne Informative adjudications into a
  target-agnostic negative-control corpus covering DEBUG-only credential logs,
  consented provider/repository/workspace content, equivalent caller paths,
  shared org/project authority, revocation ownership, integrity primitives,
  cryptographic mismatch without eligible downstream impact, and synthetic-only
  proof. Similarity is a falsifier, never an automatic KILL.
- Added a dedicated master prompt, detailed reference, structured negative-
  control cases, and a deterministic 12/12 regression test.
- Integrated the gate into the mandatory router, global security autopilot,
  bug-bounty triage, main audit prompt, AUTOLOAD, routing protocol, and both
  workspace/global AGENTS instruction surfaces.
- Expanded the live routed pack from 63 to 64 skills and from 22 to 23 master
  prompts. The frozen V12 validation package and B8 snapshots were not modified.
- Bumped the live package version to
  `2026.08.28-program-impact-boundary-gate-live-audit-only`.

## 2026.08.26 — Adaptive Execution Provenance v11

- Forked the frozen V10 experimental baseline without changing its B2/B3/B4
  artifacts or claiming blind-generalization improvement.
- Added a fail-closed execution-plane contract: adaptive assignments count only
  after a real collaboration spawn returns a unique child ID, separate child
  output is observed, and the root records a matching post-output receipt.
- Added a transcript-derived provenance schema and validator for persisted
  Codex sessions and codex exec JSON streams, including spawn attempts,
  successes, failures, waits, unique child IDs, input/output hashes, and root
  consumption. Persisted rollouts are authoritative because current
  `codex exec --json` streams can omit successful spawn and child-message
  events.
- Added ten network-free execution-provenance regressions that reject
  narrative-only specialists, empty waits, failed spawns, missing output,
  missing root receipts, pre-seeded result tokens, and duplicate child IDs.
- Added a real synthetic runner that binds the `codex exec` root thread ID to
  its persisted root/child rollouts, hashes the evidence, and fails closed when
  that binding or any execution-provenance gate is absent.
- Passed the real synthetic execution gate with one spawn attempt, one
  successful unique child, zero spawn failures, separate child output, and a
  matching root-consumption receipt. This is an engineering result only; V11
  blind recall and generalization remain untested.
- Preserved the V10 discovery methodology and candidate schema. V11 changes
  execution reliability and auditability only; it does not inherit a blind
  superiority or generalization verdict.
- Bumped the active package version to
  `2026.08.26-adaptive-execution-provenance-v11-audit-only`.

## 2026.08.25 — Adaptive Research-Path Orchestration v10

- Preserved the frozen V8 and V9 archives and their prior identities unchanged;
  V10 inherits no blind-generalization or autonomous-hunter capability result.
- Extended the explicit-only `codex-cli-multi-agent-audit-orchestrator`; the
  package still defaults to a single agent and never spawns subagents without
  an explicit user request.
- Added `RESEARCH_PATH_REGISTRY` with `ACTIVE`, `PROMISING`, `BLOCKED`,
  `EXHAUSTED`, `KILLED`, and `VALIDATED` states, evidence/unblock history, and
  a hard ban on recycling terminal discovery paths without materially new
  implementation or boundary evidence.
- Added a first wave of authority/capability, representation/consumer, and
  state/composition scouts followed by convergence analysis and zero to three
  adaptive specialists selected only from recorded coverage gaps.
- Added an anti-convergence gate: multiple agent opinions never count as
  evidence; one candidate moves to verification while remaining discovery
  capacity is redirected to neglected surfaces.
- Added primitive-to-impact chaining with evidence per transition, exact
  dependency/runtime source inspection bound to the target version, and
  evidence-based termination when remaining paths are blocked, exhausted,
  killed, repetitive, or require unavailable runtime/authorization evidence.
- Added the V10 candidate fields, a dedicated research-path registry schema,
  workspace scaffold support, a network-free validator, and 15 regressions for
  exhausted-path reuse, wave launch/cap, convergence, material reopening,
  primitive chaining, implementation binding, and termination.
- Kept 63 routed top-level skills and 22 master prompts. Bumped the active
  package version to
  `2026.08.25-adaptive-research-orchestration-v10-audit-only`.

## 2026.08.17 — Autonomous Research Cascade v9

- Preserved the frozen v8 archive and SHA-256 unchanged; v9 inherits no v8
  behavioral, blind-generalization, or held-out capability result.
- Added the separate always-active `autonomous-research-cascade-engine`, taking
  the routed package from 62 to 63 top-level skills without mutating v8.
- Distilled only domain-neutral research-system lessons from James Kettle's
  PortSwigger paper, `Can AI do novel security research? Meet the HTTP
  Terminator`: evaluation-first design, bounded micro-inspiration,
  deterministic oracles, fresh-context stage isolation, AI/code/human
  responsibility partitioning, anomaly retention, and provenance-preserving
  discovery cascades.
- Excluded the paper's HTTP payloads, named technical discoveries, target set,
  and exploitation workflow from the methodology. Its full technical lineage
  is curator-marked ineligible for v9 held-out benchmarks.
- Added six focused methods for micro-inspiration, generic anomaly evaluation,
  clean-probe reasoning, shared semantic reuse, harness falsification, and
  provenance-preserving discovery cascades.
- Extended candidate schema v9 with mandatory target-native objective,
  hypothesis/falsifier, cleanliness, fingerprints, harness origin and
  independent reproduction, cascade genealogy, deterministic validator,
  authoritative read-back, scope, impact ceiling, and cleanup fields. Added
  `CASCADE_LEAD` without allowing it to self-certify as a finding.
- Added 12 deterministic cascade regressions covering anchoring, pattern replay,
  unknown anomalies, clean-versus-dirty semantics, shared reuse, second-order
  and cross-feature jumps, harness-created and harness-suppressed anomalies,
  validator bypass, context contamination, and a safe repository.
- Added hard safety constraints against target switching, safety-signal
  masking, agent-reality deception, credential collection, destructive proof,
  and high-volume DoS, with explicit scope and minimum-harmless-proof exit.
- Bumped the active package version to
  `2026.08.17-autonomous-research-cascade-v9-audit-only`; blind generalization
  remains `NOT_PROVEN` pending external V9-A–E and independent held-out
  evaluation.

## 2026.08.17 — Novel Invariant Frontier v8

- Replaced the temporary novelty overlay with the always-active
  `novel-vulnerability-hypothesis-engine` while keeping the package total at 62
  routed skills.
- Added code-native invariant and assumption mining, differential-equivalence,
  state-machine, metamorphic, resource-amplification, counterfactual, and
  cross-feature composition workflows without embedding historical target
  ground truth.
- Added `NOVEL_DISCOVERY_MODE=true` embargo enforcement: vulnerability prior
  art stays blocked until hypothesis, source-to-sink, harmless runtime effect,
  and negative-control proof exist. Scope and current-release mapping remain
  mandatory before discovery.
- Added monotonic frontier states from `CODE_DERIVED_HYPOTHESIS` through
  `STRONG_CANDIDATE`, mandatory code anchors and proof gates, post-proof prior-
  art tracking, `novelty_status=UNVERIFIED`, and a hard ban on zero-day certainty
  fields or states.
- Added five frontier methods, candidate schema v8, a network-free validator,
  and 15 rule regressions covering V8-A through V8-E rule shapes, embargo
  leakage, composition KILL safety, cost ratios, source derivation, and safe-
  repository false positives.
- Specified evaluator-only V8-A through V8-E blind tracks and a 3-5-family
  historical held-out protocol. Ground truth remains outside the package and
  held-out capability remains `NOT_PROVEN` until a separate blind run passes.
- Preserved the frozen v7 and temporary overlay archives unchanged. Bumped the
  active package version to
  `2026.08.17-novel-invariant-frontier-v8-audit-only`.

## 2026.08.17 — Target-Native Novel Discovery Overlay v1

- Added always-active `novel-vulnerability-discovery-hunter`, which derives
  hypotheses from the current target's authority, representation, state,
  consumer, release, and producer/consumer assumption graphs rather than
  replaying historical exploit recipes.
- Added contract, identity, representation, authority, lifecycle,
  failure/default, multiplicity, topology, metamorphic-equivalence, capability-
  delta, and target-defined synthesized reasoning operators. Operators are
  questions over target facts, not vulnerability signatures or payload lists.
- Added hard anti-overfitting gates: at least two independent target facts,
  derivation provenance, a falsifiable invariant, bounded counterfactual,
  authoritative observable, two falsifiers, closest safe mimic, and historical-
  seed dependency `NONE` for every live hypothesis.
- Added a network-free campaign validator and nine deterministic regression
  cases covering valid target-native derivation, synthesized operators,
  pattern-replay rejection, independent-source requirements, safe-mimic KILL,
  false-positive budget, and STRONG/manual evidence gating.
- Kept the frozen v7 archive and its SHA-256 immutable. This overlay has a new
  package identity and inherits no v7 behavioral or blind-generalization
  capability claim until separately evaluated.
- Bumped the active package version to
  `2026.08.17-novel-discovery-overlay-v1-audit-only`.

## 2026.08.17 — Path, CLI Grammar, and Gadget-Chain Method v7

- Added `references/PATH_CLI_GADGET_CHAIN_METHOD.md`, unifying five
  public/fixed GitLab/Gitaly lineages around path capture versus canonical
  object authorization, argv operands entering child option grammar,
  per-subcommand and working-directory semantics, sanitizer output reaching a
  shipped JavaScript gadget, and separately proven capability/RCE bridges.
- Recorded GitLab issue `#212175`, Gitaly issues `#1801`, historical `#1799`,
  historical GitLab FOSS issue `#65335`, and Gitaly issue `#1892` as prior-art
  regression seeds only. One fixed endpoint/scope/subcommand is not accepted as
  proof that a sibling consumer preserves the invariant.
- Extended candidate schema v7 with `path_cli_gadget_chain_challenge`, added 17
  deterministic network-free KILL regressions, and added five positive plus
  five closest-safe routing profiles across API, compositional, parser, Go,
  JavaScript, Ruby, source, web/business, modern-RCE, patch-diff, and secure
  review routes.
- Added exact canonical object/token/DOM identity, option-terminator and
  per-subcommand checks, working-directory/mode review, static-DOM versus
  runtime-gadget tracing, and strict primitive-versus-terminal impact gates.
- Prohibited operational traversal, protected-file access, Git flag payloads,
  secret/key acquisition, signed-cookie construction, unsafe deserialization,
  SSH/internal-API use, live XSS, destructive/race/flood/DoS testing, and
  public-target reproduction.
- Bumped the package version to
  `2026.08.17-path-cli-gadget-chain-v7-audit-only`; frozen v6 remains immutable
  for provenance and regression comparison.

## 2026.08.17 — Reparse, Configuration Grammar, and Provenance Method v6

- Added `references/REPARSE_CONFIG_PROVENANCE_METHOD.md`, unifying five
  public/fixed GitLab lineages around decode/reparse drift, stored metadata to
  generated HTML, data entering a secondary configuration grammar, signed
  multipart provenance loss, and import-time virtual setter side effects.
- Added decode-depth and representation ledgers, multi-record composition,
  config-key/data separation, exact signed-carrier identity, ambient namespace
  collision review, open-time object identity, generated-setter inventories,
  scalar-versus-nested assignment order, and intermediate-versus-terminal
  impact separation.
- Recorded GitLab issues `#213273`, `#215640`, `#215212`, `#214636`, and
  `#212089` / `CVE-2020-10956` as public/fixed prior art only. The historical
  custom-header extension on the CarrierWave import path is retained as a
  negative control because assignment order prevented it from affecting the
  first request.
- Extended candidate schema v6 with `reparse_config_provenance_challenge`,
  added 18 deterministic network-free KILL regressions, and wired selective
  API, compositional, parser, Ruby/Rails, Go, source, web/business, patch-diff,
  and secure-review routing.
- Prohibited live XSS/SSRF, real file reads, special-namespace enumeration,
  metadata/credential access, destructive requests, command execution, and
  public-target reproduction.
- Bumped the package version to
  `2026.08.17-reparse-config-provenance-v6-audit-only`; frozen v5 remains
  immutable for provenance and regression comparison.

## 2026.08.17 — Archive, Renderer, and Framework Consumer Method v5

- Added `references/ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md`, unifying
  five public/fixed GitLab lineages into reusable filesystem, browser,
  renderer, runtime-loader, and framework-option invariants.
- Added archive entry-type and open-time object-identity review; browser URL
  normalization, CSRF/method-override and destructive-sink tracing; upload
  metadata through string-built markup and secondary notification/resource
  loaders; inline document options through dynamic class/loader capabilities;
  and request parameters entering framework-reserved URL option namespaces.
- Recorded GitLab issues `#349524`, `#332420`, `#324452`, `#232829`, GDK issue
  `#1314`, `CVE-2021-22238`, and upstream kramdown PR `#708` as public/fixed
  prior art only. Destructive requests, real file reads, live SSRF, secrets,
  metadata access, command payloads, and reverse shells are excluded.
- Extended candidate schema v5 with `archive_renderer_framework_challenge`,
  added 16 deterministic network-free KILL regressions, and wired selective
  source, parser, Ruby/Rails, web/API, compositional, patch-diff, secure-review,
  and modern-RCE routing.
- Bumped the package version to
  `2026.08.17-archive-renderer-framework-consumer-v5-audit-only`; frozen v4
  remains immutable for provenance and regression comparison.

## 2026.08.17 — Dynamic Data to Execution Consumer Method v4

- Added `references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md`, generalizing
  three public GitLab lineages into reusable invariants: attacker-named dynamic
  methods crossing a protocol encoder, remote import metadata surviving into a
  delayed execution consumer, and optional dependency presence silently
  enabling an interpreter for untrusted content.
- Added same-immutable-buffer framing, method-surface inventory, import
  attribute provenance, persistence/queue tracing, fixed argv/data separation,
  dependency activation matrices, sandbox completeness, terminal-impact edge
  separation, closest-sibling controls, and a mandatory KILL challenge.
- Recorded HackerOne #1679624 / GitLab issue #371884, HackerOne #1609965 /
  GitLab issue #366088 / CVE-2022-2185, and HackerOne #1401444 / GitLab issue
  #345892 / MR !76174 as public/fixed prior art only. Operational Redis/session
  payloads, deserialization gadgets, shell commands, reverse shells, and live
  dependency installation are explicitly excluded.
- Extended the candidate schema with `execution_consumer_challenge`, added 11
  deterministic network-free regression cases, and wired the method through
  selective parser, source, Web/API, Ruby, auth/session, compositional,
  patch-diff, and modern-RCE routing.
- Bumped the package version to
  `2026.08.17-dynamic-data-execution-consumer-v4-audit-only`; frozen v3 remains
  unchanged for provenance and regression comparison.

## 2026.08.17 — Patch-Variant and Consumer-Boundary Method v3

- Added a generalized method for incomplete security guards, full numeric/
  library error-domain analysis, selector-versus-consumer identity, string-built
  markup, URL-validator-versus-downstream-protocol capability, asynchronous
  import consumers, and critical lifecycle error propagation.
- Recorded HackerOne #3018307 and Cosmos SDK `GHSA-x5vx-95h7-rv4p` and
  `GHSA-47ww-ff84-4jrg` as fixed prior art for literal-guard versus complete
  operation-domain review. Added strict separation between transaction error,
  lifecycle failure, deterministic validator failure, and proven chain halt;
  public-node/mainnet availability testing remains prohibited.
- Recorded HackerOne #1731349 / GitLab Kroki `CVE-2023-0050` as fixed prior art for
  eligible-node-versus-consumed-node mismatch, unsafe string-built DOM, and
  evidence-gated CSP/data-attribute gadget composition.
- Recorded GitLab issue #372165 / HackerOne #1685822 as fixed prior art for URL
  validation without an explicit scheme boundary before a Git transport
  consumer, including service-account filesystem authority and cross-tenant
  repository disclosure.
- Wired the method into patch-diff, wallet/node, parser-differential,
  compositional, API, web/business-logic, source, and secure-review routes,
  alongside evidence-driven Go, Ruby, and JavaScript routing, without adding a
  new always-active specialist.
- Added three positive and three closest-safe routing profiles, seven abstract
  KILL-decision regressions, and structural contract checks. No live XSS, production path enumeration,
  third-party repository import, or chain/public-node halt testing is automated.
- Bumped package version to
  `2026.08.17-patch-variant-consumer-boundary-v3-audit-only`. Historical v1/v2
  benchmark results remain bound to their original package hashes.

## 2026.08.14 — Authorization Invariant and KILL Challenge v2

- Added a mandatory authorization invariant method that distinguishes explicit
  no-op opt-in from implicit nil/absent/error-to-success fallback on protected
  operations.
- Added resource-identity provenance across route, query, body, context, loaded
  object, queue payload, policy decision, and authoritative sink so authorization
  on Resource A cannot silently justify mutation/read of Resource B.
- Added a hard KILL precondition: protected invariant, enforcing component,
  absence/failure-state matrix, end-to-end sink result, documented intent,
  invariant preservation, and no attacker-controlled authority transition.
- Added required `authorization_kill_challenge` fields to candidate schema v2,
  expanded the evidence ledger and safe-test matrix, and synchronized auth,
  source, web/business-logic, secure-review, triage, router, autopilot, and master
  prompts.
- Added six deterministic development regressions covering route/body resource
  mismatch, implicit missing-provider success, explicit public no-op, fail-closed
  absence, error-to-success, and correctly denied same-resource behavior.
- Preserved historical benchmark failures as regression inputs rather than
  reclassifying or rerunning them as blind evidence.
- Bumped package version to
  `2026.08.14-auth-invariant-kill-challenge-v2-audit-only`.

## 2026.08.12 — Self-Contained 61/61 Router Coverage

- Added the top-level `authorized-security-autopilot` wrapper to the routing map
  as an always-active core skill instead of relying on external instructions.
- Expanded source inventory validation across both `skill/*/SKILL.md` and
  top-level `*/SKILL.md` layouts, with explicit `TOP_LEVEL_SKILLS`,
  `ROUTED_SKILLS`, `UNMAPPED_SKILLS`, and `MANUAL_ACTIVATION_REQUIRED` metrics.
- Added regression assertions that both `mandatory-auto-router` and
  `authorized-security-autopilot` are active for every target/scope profile.
- Synchronized bootstrap docs and bumped package version to
  `2026.08.12-self-contained-router-61-v1-audit-only`.

## 2026.08.12 — WordPress XSS2Shell Seven-Boundary Method

- Expanded `compositional-exploit-chain-hunter` with a dedicated defensive
  method for WordPress `CVE-2026-64638` / `GHSA-52p2-r8wf-jcrf`: login parser
  differential, DOM clobbering, automatic core gadget, REST JSONP/SOME,
  Application Password approval, REST content authority, upload/extraction,
  and direct PHP execution are now seven separately falsifiable edges.
- Preserved the official `High 8.9`, high-complexity, active-user-interaction
  boundary. The entry is pre-auth XSS; the terminal chain is not labeled
  zero-click or purely unauthenticated RCE.
- Added the exact advisory branch matrix from WordPress 7.0.3/6.9.6 through
  4.7.34, deployment/configuration falsifiers, isolated proof ladder W0-W7,
  detection-confidence correlation, incident response, and deployment-specific
  hardening. Kept XSS2Shell separate from WP2Shell.
- Routed the pattern through parser, auth, REST/API, web/business-logic, PHP,
  JavaScript, source, modern-RCE, and patch-diff specialists only when target and
  scope evidence support them. Added positive and narrow patched-regression
  profiles; no live scan, real admin interaction, credential collection, shell,
  or persistence was performed or automated.
- Bumped package version to
  `2026.08.12-wordpress-xss2shell-seven-boundary-v2-audit-only`.

## 2026.08.12 — Public CI Log to Resource-Scoped Netlify Capability Method

- Extended `credential-exposure-capability-hunter` for public/private CI raw and rendered logs, exact provider/task/run/job/step identity, publication audience, retention/cache/mirror state, and the application task command or configuration that emitted a credential.
- Recorded the user-supplied resolved report “Netlify Authentication Token Exposed in Public Mozilla CI Logs” as public/fixed prior art without inventing a HackerOne report ID. Official Firefox documentation supports the Taskcluster ingestion, Netlify CLI, and `crash-pings.mozilla.org` architecture.
- Preserved the effective authorization boundary: the historical response showed `role: Developer`, `site_access: selected`, and one selected site. `roles_allowed` is role-option metadata, not proof that the principal was Owner, Billing Admin, Publisher, Reviewer, or Content Editor.
- Separated account/function metadata reads, selected-site deployment/configuration authority, provider-hosted function execution, and RCE on the CI/application server. Product documentation or a function listing does not prove write/deploy/execute/environment access.
- Rejected unsupported impact inflation including team-wide/full-account control, billing/payout diversion, all-site deletion, environment-secret access, and Taskcluster/Mozilla-server RCE without separate proof.
- Added containment and synthetic-canary regression coverage for raw/rendered logs, verbose/error/retry output, downloadable artifacts, indexes, caches, mirrors, token revocation, provider audit logs, and least-privilege resource scoping.
- Added positive and negative routing profiles for a public CI log to Netlify selected-site control-plane bridge and for ordinary synthetic log-redaction review without an exposed credential.
- Bumped package version to `2026.08.12-public-ci-netlify-token-v1-audit-only`.

## 2026.08.12 — Deadlock, Lock-Graph, and Remote Availability Method

- Added `deadlock-lock-graph-dos-hunter` plus a dedicated master prompt and methodology for remote RPC/service deadlocks, lock-order inversion, self-deadlock, recursive logging locks, livelock, starvation, resource exhaustion, and bounded availability impact.
- Added a static lock-order graph, runtime wait-for graph, thread/lock ownership table, build/configuration matrix, D0-D7 evidence ladder, and patched same-configuration controls. A hang, blocked-thread count, high load, or unresponsive signal handler no longer substitutes for a stable circular wait.
- Recorded Monero HackerOne #3307874 as public/fixed prior art anchored to source fixes `179c924`/`36b12ed`, merge commits `b591866`/`2d19722`, PR #10065/#10066, and v0.18.4.3.
- Preserved the evidence corrections: the supplied PoC description used 50 threads and batch size 500 rather than proving a single request; only Linux was reproduced at the stated point; maintainers said release binaries were not affected because `STACK_TRACE` was disabled; the program assessed Medium and paid 5 XMR.
- Rejected unsupported upgrades from a local node deadlock to database corruption, confidentiality/integrity loss, irreversible state, network-wide catastrophe, or CVSS 10. Official release, custom/debug build, log level, public RPC exposure, recovery, and state integrity must be proven independently.
- Added strict safety controls prohibiting automatic public-node DoS, floods, oversized/adaptive batches, compression amplification, spoofed headers, filtering/rate-limit bypass, and load escalation. Validation defaults to static analysis and bounded isolated local fixtures.
- Added positive and negative routing profiles and wired the new specialist into C/C++, race/state-machine, source-code, patch-diff, API, binary, scope, and test-design surfaces.
- Bumped package version to `2026.08.12-deadlock-lock-graph-dos-v1-audit-only`.

## 2026.08.12 — GitHub Actions Same-Job Workspace-to-Secret Method

- Extended `github-actions-fork-trust-hunter` for cross-step write-then-execute: untrusted fork code can modify a trusted-path script, dependency, executable, PATH entry, command file, or workspace object that a later step executes with a step-scoped secret.
- Added HackerOne #3619287, DuckDuckGo `content-scope-scripts/semver-label.yml`, as public/fixed prior art anchored to historical snapshot `b5066fbcf6` and mitigation commit `eb01151209` / PR #2659.
- Preserved the exact evidence boundary: the attached uniquely tagged callback supports fork-runner code execution; it did not contain a secret and does not independently prove `ANTHROPIC_API_KEY` theft, effective job-token permissions, label mutation, release poisoning, or downstream browser consumption.
- Corrected the ambient-secret model: the key was scoped to the later semver-analysis step, while the source-reachable credential hypothesis is earlier fork code rewriting `base/.github/scripts/semver-analysis.mjs` in the shared job workspace before that later step executes it.
- Separated `pull-requests: write` label authority from merge, main-branch write, release dispatch, poisoned artifacts, and per-platform client consumption. The historical release trigger required `merged == true` plus a semver label.
- Recorded that patch `eb01151209` touched four privileged PR workflows and that its displayed parent is `11e2a57`; `b5066fbcf6` is not labeled the last pre-fix commit without an ancestry proof.
- Added a dedicated positive regression profile for fork execution, shared-workspace tampering, later secret-bearing trusted-script execution, patch analysis, and falsified supply-chain inflation.
- Bumped the package version to `2026.08.12-github-actions-cross-step-trust-v2-audit-only`.

## 2026.08.12 — GitHub Actions Fork Trust and Persisted-Credential Method

- Added `github-actions-fork-trust-hunter` plus a dedicated master prompt and methodology for `pull_request`, `pull_request_target`, `workflow_run`, untrusted artifacts/caches, local actions, install/build hooks, runner credentials, and downstream release consumers.
- Added a four-provenance model for workflow definition, code/data, execution, and authority, plus G0-G6 evidence levels that keep runner execution, credential reach, effective token authority, protected mutation, and supply-chain impact separate.
- Recorded the user-supplied DuckDuckGo privacy-configuration 2026 report as public/fixed prior art without inventing a HackerOne ID. Preserved the vendor-confirmed root cause: fork-controlled npm `postinstall` could reach the job `GITHUB_TOKEN` persisted by `actions/checkout@v5`.
- Preserved the crucial falsifiers: repository/organization secrets were not ambient to the `npm ci` step, external forks were excluded from later `PRIVACY_CONFIG_PAT` steps, the Asana job used trusted base code, and PR #5002 was defense-in-depth hardening rather than proof of the originally claimed exfiltration.
- Added exact channel analysis for explicit step/action secrets, `github.token`, Git configuration/helpers, CLI/cloud files, OIDC, command files, artifacts/caches, and runner residue; requested YAML permissions never substitute for runtime effective permissions.
- Added positive and negative routing profiles so fork execution plus persisted credentials activates CI/CD, credential, JavaScript, source, patch-diff, and compositional specialists, while a metadata-only trusted-base action does not activate the new skill.
- Prohibited automatic vendor fork PRs, OAST callbacks, raw-token capture, credential replay, vendor mutation, releases, or deployments; safe proof uses disposable owned repositories and synthetic canaries.
- Bumped the package version to `2026.08.12-github-actions-fork-trust-v1-audit-only`.

## 2026.08.12 — Native JavaScript Binding Lifetime and UAF Method

- Added `native-js-binding-lifetime-hunter` for authorized V8/Gin, Blink, Electron, Node/N-API, WebView, renderer, and other JavaScript-to-native bindings where independently retained objects/functions may outlive native receivers.
- Added a dual JavaScript/native ownership graph, property-descriptor and provider-mode matrix, GC/context/navigation/disconnect teardown analysis, ASan/HWASan allocation-free-use evidence, repeated trials, and baseline/negative/patched controls.
- Recorded the user-supplied May 2023 Brave “UAF on JSEthereumProvider” transcript without inventing a HackerOne report ID, and anchored the lineage to official historical source, brave-core PR #18411, fix commit `a8e497b`, and the 1.51.x/1.52.x uplift PRs.
- Preserved the crucial falsifiers: deletion failed in the non-configurable Brave Wallet mode, reproduction depended on Extensions wallet fallback, GC/crash behavior was probabilistic, and the public proof established a renderer UAF/crash rather than renderer code execution.
- Added strict impact levels separating source suspicion, crash, sanitizer-confirmed UAF, controlled corruption, code execution in the affected process, and sandbox/privilege escape. A UAF class name or crash never upgrades itself to RCE.
- Added positive and negative routing profiles so V8/Gin lifetime evidence activates the specialist with C/C++, JavaScript, source, binary/reverse-engineering, and patch-diff support, while an ordinary JavaScript wrapper review does not.
- Bumped the package version to `2026.08.12-native-js-binding-lifetime-uaf-v1-audit-only`.

## 2026.08.12 — Mastodon Staging Admin Token and PII-Safe Evidence Method

- Added HackerOne #2137154, “Mozilla Mastodon Staging Instance Admin API Key Disclosure Through Slack,” as resolved public prior art for an authorized collaboration-artifact to staging administrative API boundary.
- Added a per-endpoint authorization matrix that separates token format, declared OAuth scope, effective role permission, successful read capability, and unproven write/delete operations. A successful `GET /api/v1/admin/accounts` is not treated as proof of every documented admin action.
- Added explicit environment labels for production, staging with real data, staging with synthetic data, test, and unknown. Staging lowers production claims but is not automatically harmless when it contains real identities, PII, trusted integrations, or a production bridge.
- Added `PII_EXPOSED_STOP`: stop pagination and follow-on calls when third-party email/IP/account data appears; retain sanitized field metadata and request vendor-side secure handling/redaction instead of copying the response.
- Recorded token rotation, old-token rejection, Slack/chat artifact cleanup, response redaction, derived-session review, and residual copies as separate containment claims.
- Preserved the scope lesson that Mozilla's out-of-scope bounty/bonus and statement that Mastodon might be included later were exceptions, not present or future testing authorization.
- Added a dedicated routing regression profile for Slack to Mastodon staging admin-token evidence and bumped the package version to `2026.08.12-mastodon-staging-admin-token-v1-audit-only`.

## 2026.08.12 — Container Image Credential Exposure Method

- Extended `credential-exposure-capability-hunter` and the cloud/supply-chain route for authorized Docker/OCI image, manifest, config, layer, registry cache/mirror, and exported-image credential exposure.
- Recorded the user-supplied historical Mozilla Common Voice Docker Hub case as resolved prior art: two AWS access-key pairs and database credentials were reportedly embedded in `/code/scripts/test/config.json`; Mozilla validated AWS authentication, removed affected images, rotated credentials, and removed the AWS users. No report ID or raw credential was stored or invented.
- Added immutable evidence identity across registry/repository, tag-at-observation, multi-platform index, platform manifest, image config, layer digest/index, and in-layer path. A mutable `latest` tag or final-rootfs absence is not accepted as artifact identity or lower-layer cleanup proof.
- Added separate AWS long-term versus temporary credential binding, database endpoint/environment/role gates, vendor-side capability proof, and hard no-replay/no-cloud-enumeration/no-database-access controls.
- Separated credential rotation, database-password rotation, IAM-principal removal, tag/manifest deletion, blob garbage collection, cache/mirror purge, pulled/exported-copy review, and clean rebuild into independently verified containment claims.
- Added positive and negative routing regression profiles for Docker Hub/OCI image credential exposure so credential, cloud/supply-chain, auth, and compositional specialists activate only when evidence supports them.
- Bumped package version to `2026.08.12-container-image-credential-exposure-v1-audit-only`.

## 2026.08.12 — Credential Exposure to Effective Capability Method

- Added `credential-exposure-capability-hunter` for authorized exposed or hard-coded credentials in source, Git history, CI logs, artifacts, documentation, tickets, Slack/Teams/chat files, notebooks, packages, screenshots, and support bundles.
- Added a dedicated methodology covering artifact audience, credential authenticity, current validity, principal/environment binding, declared scope versus effective permissions, minimum protected capability, E0-E6 evidence levels, revocation, and residual-copy review.
- Recorded HackerOne #2467999, “Jira Credential Disclosure within Mozilla Slack,” as resolved historical prior art and an explicit out-of-scope exception; its discretionary bounty is not treated as scope precedent.
- Prohibited raw-credential retention, implicit authentication/replay, user/project/data enumeration, and mutation. When validation is not explicitly authorized, the workflow requires fingerprinted evidence plus vendor-side validation and revocation.
- Wired the method into API, authentication/authorization, cloud/supply-chain, compositional-chain, scope/test, and automatic-routing surfaces without loading it for unrelated targets.
- Added positive and negative routing regression profiles for an authorized Slack artifact containing a Jira API credential and for an unrelated Slack integration with no credential exposure, preserving vendor-side capability confirmation and hard no-replay/no-enumeration controls.
- Bumped package version to `2026.08.12-credential-exposure-capability-v1-audit-only`.

## 2026.08.12 — LLM Tokenization and Repeated-Token Boundary Method

- Added `llm-tokenization-boundary-hunter` for authorized AI/LLM targets where repeated tokens/characters, tokenizer representations, instruction blackout, divergence, memorization, or repetition-filter gaps may bridge into a real product-security boundary.
- Added a dedicated methodology covering bytes/Unicode/token IDs, prompt roles/order, model/router/filter behavior, token-budget-matched controls, stochastic trials, tool/RAG/backend authority, privacy validation, safe proof levels, and hard KILL rules.
- Recorded `dropbox/llm-security`, Dropbox's 2023/2024 research, and arXiv:2311.17035 as public historical prior art. The repository is explicitly classified as experimental research code, not a production backend or automatic vulnerability scanner.
- Added important falsifiers: the historical Q&A harness uses a single user-role prompt rather than a true system-role boundary, and its model-based response judge is not independent evidence.
- Wired the method into AI-model, compositional-chain, tokenizer/parser, master-prompt, and audit-matrix routing while keeping universal-jailbreak evaluation explicit opt-in.
- Added an automatic-routing regression profile for repeated-token instruction blackout reaching an unauthorized agent tool action on researcher-owned resources, while preserving no-live-fuzzing, no-training-data-collection, and single-agent defaults.
- Bumped package version to `2026.08.12-llm-tokenization-boundary-v1-audit-only`.

## 2026.08.12 — Cross-Language Generated-Script Injection Method

- Added `cross-language-script-injection-hunter` for authorized paths where one runtime interpolates untrusted values into generated source that another runtime executes.
- Added a dedicated methodology covering principal/policy reachability, semantic-validator versus target-language grammar, emitted artifacts, full-program parsing, temporary-script transports, interpreter authority, safe proof controls, and typed-data remediation.
- Recorded `0din-ai/ai-scanner` `GHSA-r27j-xxgx-f5vr` / `CVE-2026-41512` as vendor-confirmed prior art affecting 1.0.0 through 1.4.0 and fixed in 1.4.1 by moving dynamic values into a JSON data channel.
- Wired the method into compositional, modern-RCE, parser-differential, API, Ruby, JavaScript/TypeScript, source-code, secure-review, and patch-diff routing without loading it for unrelated targets.
- Added an automatic-routing regression profile for Rails/Playwright Ruby-heredoc to generated-JavaScript execution while preserving single-agent, no-live-command, no-secret-harvesting defaults.
- Bumped package version to `2026.08.12-cross-language-script-injection-v1-audit-only`.

## 2026.08.12 — Dynamic Filter and Query-Evaluator RCE Method

- Added `dynamic-filter-evaluator-rce-hunter` for authorized GraphQL/REST open-filter and query-DSL paths that can select code-bearing operators or dynamic predicate compilers.
- Added a dedicated methodology covering schema openness, raw-object forwarding, dependency/operator semantics, runtime gates, anonymous/resolver authorization, deterministic non-empty invocation, output channels, process authority, safe proof controls, impact validation, and patch variants.
- Recorded Taskcluster `GHSA-ccv5-c45x-2q38` / `CVE-2026-11892` as vendor-confirmed prior art affecting versions before 100.3.0, with PR #8718's typed `searchTerm` replacement and `sift` removal as the invariant-restoring fix.
- Wired the method into compositional, modern-RCE, parser-differential, API, JavaScript/TypeScript, source-code, and secure-review routing without loading it for unrelated targets.
- Added an automatic-routing regression profile for Node.js GraphQL `filter: JSON` -> `sift` `$where` -> `new Function` evidence while preserving single-agent and no-live-exploit defaults.
- Bumped package version to `2026.08.12-dynamic-filter-evaluator-rce-v1-audit-only`.

## 2026.08.09 — Target- and Scope-Aware Relevant-Skill Router

- Replaced substring-only bootstrap selection with a target/scope evidence profile covering source, web, API, mobile, binary, Windows, cloud, CI/CD, supply chain, Web3, AI, authentication, and patch surfaces.
- Added separate `--target`, `--scope`, `--scope-file`, and `--observed` evidence channels to `route-security-task.py`.
- Added scope-exclusion precedence, language/runtime artifact detection, high-confidence versus ambiguous trigger handling, primary-surface activation, and distinct `ACTIVE / DEFERRED / NOT_APPLICABLE` ledgers.
- Made recon, black-box automation, tool installation, implementation, red-team, jailbreak evaluation, and multi-agent orchestration explicit-intent routes.
- Added regression coverage for .NET source/API/auth, Solidity/Web3 replay, Windows binary/token, AI browser chains, ambiguous generic terms, mobile scope exclusion, explicit multi-agent use, cloud metadata chains, WordPress parser-to-RCE, Node.js-versus-Web3 `node` disambiguation, negated recon requests, and Indonesian Go source/API routing.
- Updated mandatory-router, autopilot, master prompt, routing protocol, autoload, workspace instructions, and global instructions so Codex loads only evidence-supported specialist bodies.
- Preserved the mandatory core, continuous rerouting, single-agent default, no automatic operational tooling, and `STRONG + MANUALLY_CONFIRMED` evidence gate.
- Bumped package version to `2026.08.09-target-scope-router-v2-audit-only`.

## 2026.08.08 — Compositional Exploit Chain Hunter

- Added `compositional-exploit-chain-hunter` for authorized multi-stage chains across AI/browser agents, parser differentials, authentication and recovery, SSRF/cloud metadata, workload identity, package trust, and web-to-RCE paths.
- Added an original pattern atlas distilled from the public Zenity browser-agent research, PwnAI XSS2Shell, HackerOne report 341876, and the Immunefi write-up index without copying operational payloads.
- Added `MASTER_PROMPT_COMPOSITIONAL_EXPLOIT_CHAIN_AUDIT.md` with same-agent scope, prior-art, representation, authority, chain, critic, proof-design, and evidence-judge stages.
- Added explicit soft-versus-hard control classification, inter-agent confused-deputy analysis, authority graphs, and edge-by-edge proof requirements.
- Preserved strict authorization, current-release reachability, root-cause prior-art screening, harmless evidence, `STRONG + MANUALLY_CONFIRMED`, and `NO VALID FINDING` gates.
- Preserved single-agent default behavior; the new stage roles do not spawn or delegate to subagents automatically.
- Bumped package version to `2026.08.08-compositional-exploit-chain-v1-audit-only`.

## 2026.08.06 — Attack Surface, Chain, and Tooling Method

- Added an original evidence-first operating reference derived from the public BugBounty.info Attack Surface, Chains, and Tooling taxonomy.
- Added mandatory target-surface classification and `attacker position -> primitive -> bridge -> protected boundary -> impact` tracing.
- Added full high-level coverage for web, API, mobile, cloud, CI/CD, AI/LLM/agent/MCP, and Web3 surfaces plus 19 chain families.
- Added bounded tool-selection rules for Burp, DevTools, Nuclei, ffuf, local automation, and AI-assisted review; selection never authorizes execution.
- Wired the reference into the mandatory router, global authorized-security autopilot, bootstrap prompt, autoload entrypoint, routing map, and package validator.
- Preserved staged single-agent review, explicit multi-agent opt-in, prior-art-first screening, hard KILL gates, and safe manual confirmation.
- Bumped package version to `2026.08.06-bugbounty-info-method-v1-audit-only`.

## 2026.07.30 — Explicit Multi-Agent Opt-In

- Changed the global security workflow to staged single-agent verification by default.
- Removed automatic subagent invocation from global instructions, autopilot, mandatory routing, core prompts, and core references.
- Changed `codex-cli-multi-agent-audit-orchestrator` and its companions from always-active to explicit opt-in.
- Preserved manual multi-agent capability only for direct user requests.

## 2026.07.29 — Codex CLI Role-Separated Multi-Agent Audit

- Added always-active `codex-cli-multi-agent-audit-orchestrator` for the user's Codex CLI workflow.
- Adapted the discovery-versus-false-positive-verification architecture from Hyunseo Shin’s February 23, 2026 article into fresh-context roles: scope/reality mapper, security-model mapper, independent discovery passes, semi-triage KILL pass, reachability/security-model/prior-art/trace/test-design verifiers, blind final judge, and human reproduction gate.
- Added mandatory explicit `attacker condition`, `server condition`, and `security impact` fields to stop vague model conclusions.
- Added authorization-scope tracing for `subject + action + target resource + tenant/org + object state`, including route-target propagation into policy helpers and downstream filters.
- Added `MASTER_PROMPT_CODEX_CLI_MULTI_AGENT_AUDIT.md`, `CODEX_CLI_MULTI_AGENT_WORKFLOW.md`, and `CODEX_CLI_CANDIDATE_SCHEMA.json`.
- Added `init-codex-cli-audit-workspace.py`, a local scaffold-only helper that does not invoke Codex, network access, scanners, fuzzers, or PoCs.
- Added correlated-error controls for single-model multi-agent use: fresh sessions, blind review, one-candidate dossiers, structured evidence, and agent-consensus rejection.
- Separated technical verdict from manual status (`NOT_TESTED`, `BLOCKED`, `MANUALLY_CONFIRMED`).
- Updated mandatory routing and package validation to cover 52 skills and all supporting artifacts.
- Bumped package version to `2026.07.29-codex-cli-multi-agent-v1-audit-only`.

## 2026.07.27 — Audit-only cleanup

- Removed the dedicated publication-oriented pattern-mining skill.
- Removed the publication-oriented Web3 historical-pattern worksheet and its routing references.
- Removed narrative-drafting language and routes; retained only technical audit, evidence, duplicate/root-cause checks, and remediation/test guidance.
- Updated mandatory routing from 52 to 51 skills and added validation that writing/report-specific skill or artifact names cannot return.
- Bumped package version to `2026.07.27-mandatory-auto-router-v2-audit-only`.

## 2026.07.27 — Mandatory Package-Wide Automatic Routing

- Added `mandatory-auto-router` as the compulsory first-entry skill for every authorized security task.
- Added a complete machine-readable `config/AUTO_ROUTING_MAP.json` covering all 52 skills and every prompt, reference, config template, and automation artifact.
- Added `AUTOLOAD.md`, `MASTER_PROMPT_MANDATORY_AUTO_ROUTER.md`, and `AUTO_ROUTING_PROTOCOL.md`.
- Added a mandatory bootstrap contract to every `SKILL.md`, so direct specialist invocation still activates global routing.
- Added continuous rerouting on new language/runtime, platform, entrypoint, trust-boundary, sink, release, and prior-art evidence.
- Added deterministic `route-security-task.py` and coverage/integrity validator `validate-auto-routing.py`.
- Operational scripts may be selected automatically as relevant resources but cannot execute automatically; explicit authorization and safety controls remain mandatory.
- Preserved hard scope/release/prior-art gates, safe evidence, negative controls, aggressive falsification, STRONG/MEDIUM/WEAK/KILL triage, and the audit-only output boundary.

## 2026.07.20 — Expert Programming, Reverse Engineering & Defensive Windows Research Expansion

- Added 10 language-specialist engineering skills for Python, JavaScript/TypeScript, Go, Rust, C/C++, Java/Kotlin, C#/.NET, PHP/Ruby, shell/PowerShell, and SQL/databases.
- Added `expert-reverse-engineer` for exact-artifact static/dynamic analysis, symbol provenance, ABI/calling convention reconstruction, patch diffing, and safe runtime confirmation.
- Added `expert-windows-internals-vulnerability-researcher` for token/impersonation, Object Manager, registry hives, NTFS links/reparse points/oplocks, minifilters, Defender, WinRE, BitLocker, and service/driver trust boundaries.
- Added nine repository-specific **defensive** skills for LegacyHive, GreatXML, RedSun, MiniPlasma, YellowKey, BlueHammer, UnDefend, GreenPlasma, and RoguePlanet.
- Added four master prompts and three references covering polyglot engineering, reverse engineering, Windows internals research, repository mapping, and isolated-lab safety.
- Public exploit repositories are explicitly treated as prior art. Reproduction alone is KILL for novelty; only a distinct current root cause, patch bypass, sibling path, or separate security boundary can survive.
- Prohibited operationalization: no exploit reliability improvements for deployment, persistence, stealth/evasion, credential access, third-party targeting, or modified public malware binaries.
- Preserved the audit-only output boundary.

## 2026.07.18 — Expert AI Model Bug Bounty Expansion

- Added `expert-ai-model-bug-bounty-auditor` for authorized auditing of AI model products, inference APIs, agents, RAG, tools/connectors, memory/cache, multimodal pipelines, sandboxes, control planes, and model supply chains.
- Added `MASTER_PROMPT_EXPERT_AI_MODEL_AUDIT.md` with strict product-security gates, stochastic reproduction requirements, A/B/C isolation controls, and end-to-end model-to-tool/backend tracing.
- Added `EXPERT_AI_MODEL_AUDIT_MATRIX.md` for model/version capture, trial matrices, protected-boundary proof, controls, and hard KILL checks.
- Explicitly rejects standalone jailbreaks, harmful outputs, hallucinations, bias, prompt leakage, and text-only prompt injection unless the program accepts the class and a concrete protected boundary is crossed.
- Preserved the audit-only output boundary: outputs stop at technical validation and evidence handoff.

## 2026.07.18 — Expert Bug Hunter / Evidence-only output

- Upgraded every retained skill with a mandatory expert operating contract, hard scope/reality/prior-art gates, end-to-end tracing, falsification, safe verification, and evidence-only output boundary.
- Removed the former narrative-generation module completely.
- Standardized all skills around technical validation, evidence handoff, falsification, cleanup, and remediation/test guidance.
- Added 10 expert bug-hunting skills:
  - expert-bug-hunter
  - expert-authorized-hacker
  - expert-source-code-bug-hunter
  - expert-web-api-business-logic-hunter
  - expert-authentication-authorization-hunter
  - expert-race-condition-state-machine-hunter
  - expert-cache-proxy-parser-differential-hunter
  - expert-cloud-ci-cd-supply-chain-hunter
  - expert-mobile-client-hunter
  - expert-crypto-signature-protocol-hunter
- Added 7 new expert master prompts for general bug hunting, authorized hacking, source audits, web/API business logic, auth/identity, cloud/supply chain, and state/race/cache/parser research.
- Added shared expert protocol, scope/reachability checklist, candidate ledger, and safe test-design matrix.
- Changed the black-box workspace `reports/` directory to `handoff/`.
- Preserved strict authorization, safe proof, rate-limit, non-destructive, and no-weaponization boundaries.
