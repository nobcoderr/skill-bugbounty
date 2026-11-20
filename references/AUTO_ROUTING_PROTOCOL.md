# Mandatory Automatic Routing Protocol

## Objective

For explicitly authorized security work, routing is offensive red-team first:
prioritize attacker objectives, reachable entrypoints, exploit chains,
privilege or authority transitions, protected sinks, and concrete impact.
Defensive controls are used mainly to falsify hypotheses or as post-proof
guidance unless the user explicitly requests blue-team work. This priority is
model-neutral and never expands authorization or weakens safety constraints.

Guarantee complete package coverage without loading irrelevant material into the active context. Every security task must evaluate every installed skill and supporting artifact, activate all relevant modules, and record why the remainder are not applicable.

## Required states

Each skill receives exactly one current state:

- **ACTIVE** — evidence or task structure makes the skill materially relevant; its instructions must influence the analysis.
- **DEFERRED** — relevance depends on a specific unresolved fact; state the activation condition.
- **NOT_APPLICABLE** — evaluated and rejected with a concrete reason.

No unclassified skill is permitted.

## Core activation sequence

1. `prompts/SYSTEM_PROMPT_AUTHORIZED_OFFENSIVE_IMPACT_GATE.md`
2. `mandatory-auto-router`
3. `authorized-security-autopilot`
4. `expert-bug-hunter`
5. `ai-assisted-bug-bounty-orchestrator`
6. `expert-authorized-hacker`
7. `bug-bounty-auditor`
8. `bug-bounty-triage`
9. `novel-vulnerability-hypothesis-engine`
10. `autonomous-research-cascade-engine`
11. `program-impact-boundary-gate`
12. Novel invariant frontier, state-machine, metamorphic differential, resource
   amplification, cross-feature composition, and evaluation-first research
   cascade methods; micro-inspiration, generic anomaly evaluation, clean-probe,
   discovery-cascade, shared-semantic-reuse, and harness-falsification methods;
   plus candidate schema, scope/reachability checklist, core protocol,
   candidate ledger, safe-test matrix, and authorization invariant KILL
   challenge; program-impact prompt, method, Informative negative controls, and
   Resolved/rewarded positive controls

The system-prompt overlay is mandatory across model variants. It does not turn
historical adjudications into automatic suppressions: each candidate still
requires target-specific equivalence and current policy verification.

`counterfactual-methodology-synthesizer` is not always active. Route to it only
after the current bounded campaign records `NO VALID FINDING`, or when the user
explicitly requests counterfactual methodology synthesis for such a completed
campaign. The target must remain authorized, current, eligible, and materially
unexplored. Its two-cycle, three-card limit and mutation-only rejection are
mandatory; it never lowers the `STRONG + MANUALLY_CONFIRMED` gate.

Specialists activate after this sequence and can activate additional specialists when evidence changes. Any consuming runtime (Cursor, Codex CLI, Claude Code, Gemini, or other) keeps discovery, semi-triage, specialist verification, final judgment, and human reproduction as distinct stages. For bug bounty, VRP, and authorized vulnerability hunts, automatically activate the multi-agent orchestrator and spawn specialists through the current runtime tool without waiting to be named. Skip ordinary product/UI work.

## Evidence-driven selectors

Build a target/scope evidence card before specialist activation:

- program and exact asset;
- positive in-scope surfaces and explicit exclusions;
- permitted testing mode, rate limits, and automation rules;
- repository/artifact/endpoint/contract/deployment;
- language/runtime/build evidence;
- platform, entrypoint, attacker position, trust boundary, primitive, and sink.

Apply exclusion precedence first. An out-of-scope mobile app, live domain,
third-party service, archived repository, vulnerability class, or testing mode
cannot be reactivated by a matching keyword or file.

Select modules from actual evidence, including:

- repository file extensions, manifests, dependencies, build files, and runtime imports;
- endpoint/protocol/transport types;
- platform APIs, operating-system semantics, privilege boundaries, and release artifacts;
- dangerous sinks and their callers;
- state/cache/serialization/parser transformations;
- checked-versus-consumed object/value identity, arithmetic/library error
  domains, downstream protocol capability, and critical lifecycle error
  propagation;
- dynamic runtime method/attribute surfaces, protocol length/data identity,
  remote import attribute provenance, persisted/queued execution state,
  process argv/data separation, and optional-interpreter activation;
- archive member/object type, canonical-root and open-time identity, browser
  and framework normalization, upload-to-secondary-renderer/resource-loader
  transitions, inline option-to-class/loader capability, and framework-reserved
  option namespaces;
- identity, role, tenant, signature, replay, and capability checks;
- auth-control initialization/default/failure semantics and authorized-versus-consumed resource identity;
- source-to-production or source-to-release mapping;
- CVE, advisory, patch, changelog, issue, PR, and duplicate lineage in normal
  mode, or only after the novelty embargo proof gate in novel mode;
- test evidence needed to validate or falsify the candidate;
- current review stage, required verification pass, and manual-reproduction status.
- current program severity floor, intended trust/consent domain, starting and
  resulting capability, equivalent supported paths, unauthorized recipient or
  action, promised security property and control/data-plane scope, collision
  feasibility, counterfactual residual authority, authorization issuance time,
  derived credential lineage, temporal trust equivalence, protected-consumer
  bridge, and capability delta;
- adjudication basis, submission-time reachability, production stack
  equivalence, canonical consensus/finality, exact ordinary-path and top-level
  navigation controls, privacy-promise scope, and report readiness;
- code-native fact anchors, invariant and assumption derivation, equivalent
  paths, state sequence, representation changes, resource cost, composition
  edges, counterfactuals, negative controls, embargo status, and historical-
  seed independence.
- objective and oracle design, inspiration provenance, deterministic acceptance,
  false-positive controls, anomaly channels, stage-context isolation,
  responsibility partition, and cascade provenance.
- probe cleanliness and semantic proof, baseline/anomaly fingerprints, anomaly
  origin, independent runners, shared semantic domains, cascade genealogy,
  authoritative read-back, and deterministic validator identity.

Keyword matching is only a bootstrap hint. It cannot replace architecture and call-path evidence.

### Activation threshold

Activate a conditional skill only when at least one of these is true:

1. official target/scope evidence directly identifies its primary surface;
2. an observed file, manifest, dependency, build artifact, runtime import, API,
   platform primitive, trust boundary, or sink directly supports it;
3. a specific high-confidence phrase identifies its domain and is compatible
   with scope;
4. two independent ambiguous signals corroborate each other; or
5. the route is intent-only and the user explicitly requested it.

A single ambiguous word such as `agent`, `token`, `service`, `browser`,
`package`, `oracle`, `node`, `role`, or `workflow` stays `DEFERRED` unless a
compatible target surface corroborates it. Irrelevant or scope-contradicted
routes are `NOT_APPLICABLE` and their full bodies are not loaded.

Use the deterministic selector with separate evidence channels when useful:

```bash
python3 automation/route-security-task.py \
  --task "authorized audit request" \
  --target "exact product, repository, artifact, or endpoint" \
  --scope "official in-scope and out-of-scope text" \
  --observed path/to/observed/artifact
```

Use `--scope-file` for a local official policy snapshot and `--json` for the
complete `ACTIVE / DEFERRED / NOT_APPLICABLE` ledger. The helper is read-only
and network-free; it never authorizes active testing.

## Companion loading

When a skill becomes ACTIVE, load every existing path in its `companions` list in `config/AUTO_ROUTING_MAP.json`. Missing companions are package-integrity failures and must be reported.

## Continuous rerouting

Rerun the selector after each material discovery. Typical examples:

- a Python API invokes a native C extension;
- a web XSS reaches a desktop/native bridge;
- an arbitrary file write reaches a privileged scheduled consumer;
- an API authorization lead becomes a race/state-machine issue;
- an optional/nil auth callback or competing route/body target reveals a fail-open or resource-identity invariant;
- a parser bug crosses cache, proxy, filesystem, or cross-service boundaries;
- a selector validates one node/value while a fallback consumer uses another;
- a URL validator hands a broader scheme/redirect domain to Git, HTTP, package,
  archive, or another authority-bearing client;
- a narrow arithmetic guard leaves another admitted error that reaches a
  consensus/job lifecycle consumer;
- remote data becomes methods used by a wire encoder, survives as importer
  state into a worker, or changes parser behavior because an optional
  interpreter dependency is present;
- an archive member becomes a link or special object later opened, a browser
  request reaches a destructive route, upload metadata becomes markup or a
  secondary resource load, an inline option selects a runtime class/loader, or
  request data enters a framework URL option namespace;
- a regex-captured upload path reaches open/copy, a ref/path operand reaches a
  child option grammar or changes its working-tree namespace, or static
  sanitizer output reaches a shipped JavaScript gadget;
- a source finding maps to a CI, updater, package, or release pipeline;
- a public CVE patch reveals an unfixed sibling path.
- a clean probe creates a new invariant violation, an anomaly survives an
  independent runner, or a shared component applies a domain-specific rule in
  a semantically different domain;
- an accepted anomaly yields a new detection strategy or security-effect theory
  that must be recorded as a child hypothesis or `CASCADE_LEAD`.

## Automation safety

Files in `automation/` may be automatically selected as relevant resources, but never automatically executed. Execution requires explicit authorization, an allowlist, task-specific necessity, rate/concurrency limits where applicable, abort conditions, and cleanup.

## Completion assertion

Before technical handoff, verify:

- skill route coverage is 100%;
- no active specialist was merely named without being applied;
- all relevant companions were loaded;
- every deferred module has an activation condition;
- every not-applicable module has a reason;
- routing was repeated after material discoveries;
- no operational script ran implicitly;
- no discovery pass self-certified a finding or bypassed falsification;
- no live hypothesis depends on historical exploit instructions or resemblance
  alone; every survivor is reconstructible from at least two independent target
  facts and passed a safe-mimic challenge;
- every survivor states attacker condition, server condition, and security impact;
- every auth-related KILL includes invariant, enforcing component, absence/failure-state behavior, resource identity, end-to-end sink result, and no-authority-transition proof;
- every consumer-boundary KILL proves the complete admitted operation domain,
  checked-versus-consumed identity, downstream protocol capability, and safe
  error propagation;
- every dynamic-data execution-consumer KILL proves primitive normalization,
  same-buffer protocol framing, strict pre-persistence attribute allowlisting,
  fixed argv/data separation, explicit fail-closed activation, and the exact
  intermediate-versus-terminal impact boundary;
- every archive/renderer/framework KILL proves final-consumer object identity,
  canonical root/origin/namespace, browser and framework normalization,
  feature/environment reachability, secondary consumers, a closest safe
  sibling, and the independently proven terminal-impact boundary;
- every reparse/configuration/provenance KILL proves decode and parser order,
  validated-versus-consumed representation, final output/config grammar,
  exact signed carrier identity, ambient collision behavior, generated-setter
  inventory and assignment order, a closest safe sibling, and the separately
  proven terminal-impact boundary;
- every path/CLI/gadget-chain KILL proves exact canonical object, argv token or
  final DOM identity; every downstream subcommand/renderer/gadget; root or
  option-terminator enforcement; environment/platform reachability; the base
  file/DOM effect; patched sibling controls; and each separately claimed
  secret, signing, serializer/gadget, or terminal-impact bridge;
- every retained anomaly has a cleanliness classification, generic evaluation
  primitive, frozen baseline/anomaly fingerprint, explicit origin attribution,
  and harness-independent reproduction before `STRONG`;
- every cascade child has parent, observation, invariant, inspiration, and depth
  provenance, its own falsifier and proof, and never inherits impact;
- target switching, safety-signal masking, agent-reality deception, credential
  collection, destructive proof, and high-volume DoS did not occur; scope was
  explicit and testing exited at the minimum harmless proof;
- all retained findings survived scope, release reachability, security-model review, prior art, safe verification, negative control, manual-status tracking, and hard triage.
- all retained findings passed the two-stage program-impact gate; no candidate
  was promoted from technical correctness, a local/synthetic PoC, or a patch
  alone; production versus demo/quickstart/development-preview status, impact
  ceiling, defended threat model, defense-in-depth versus security guarantee,
  equivalent supported paths, current production reachability, realistic
  attacker-controlled timing/topology, lifecycle revocation semantics, and
  precise property purpose, control-plane/data-plane scope, collision
  feasibility, well-formed equivalent inputs, counterfactual defense efficacy,
  authorization issuance time, derived-token lifecycle, temporal principal
  equivalence, operation-specific signed scope, protected-consumer reachability,
  known/duplicate status were resolved; and Informative similarity was never
  used as an automatic KILL.
