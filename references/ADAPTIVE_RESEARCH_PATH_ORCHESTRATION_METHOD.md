# Adaptive Research-Path Orchestration Method

## Purpose

This method controls an explicitly authorized multi-agent security audit after
scope, target reality, and the expected security model are known. It prevents
repeated work, redirects capacity away from converged hypotheses, launches
specialists only for material coverage gaps, and stops when further rounds
would only repeat exhausted paths.

When the parent orchestrator is active for bug bounty, VRP, or an authorized
vulnerability hunt, this method governs automatic specialist waves. It still
does not authorize recon, scanners, installers, or live PoCs by itself.

## 1. Research-path registry

Maintain one registry entry for every material attack surface or hypothesis
family investigated. Each entry has exactly one status:

- `ACTIVE`: currently assigned and producing evidence.
- `PROMISING`: survives initial falsification and has a defined next proof.
- `BLOCKED`: cannot progress without named evidence, runtime, authorization, or
  environment access.
- `EXHAUSTED`: the defined hypothesis family and reasonable target-native
  variants were investigated without a surviving candidate.
- `KILLED`: contradicted, unreachable, by design, duplicate, fixed, out of
  scope, or lacks a security boundary.
- `VALIDATED`: the path produced a candidate that passed its applicable proof
  gates; this does not bypass manual reproduction or final evidence judgment.

Record:

- path ID, attack surface, and hypothesis family;
- scope/release component and trust boundary;
- evidence inspected and exact last result;
- reason for `BLOCKED`, `EXHAUSTED`, or `KILLED`;
- the specific evidence that would unblock or legitimately reopen it;
- assigned role, wave, and root-cause family;
- status history and materially new evidence.

Do not assign discovery capacity to `EXHAUSTED` or `KILLED` paths. Reopen one
only when materially new evidence changes its trust boundary, consumer,
release reachability, dependency behavior, state transition, or downstream
impact path. A new agent opinion, paraphrased hypothesis, or repeated source
read is not new evidence.

Use `config/CODEX_CLI_RESEARCH_PATH_REGISTRY_SCHEMA.json` for the registry and
`automation/validate-adaptive-research-orchestration.py` for deterministic
checks.

## 2. First-wave discovery

After the architecture and invariant maps are complete, run three independent
core scouts when parallel work was explicitly authorized:

1. `AUTHORITY_CAPABILITY`: principals, permissions, tenant/object scope,
   capability lifecycle, confused deputies, and privilege transitions.
2. `REPRESENTATION_CONSUMER`: parse/canonicalization/serialization drift,
   checked-versus-consumed identity, protocol grammar, and shared consumers.
3. `STATE_COMPOSITION`: state machines, queue/retry/cache behavior, races,
   lifecycle changes, and composition of individually weak primitives.

These are reasoning lanes, not predetermined vulnerability classes. Each scout
must register the surfaces it actually covered and return hypotheses or hard
negative evidence. Agreement does not change proof quality.

## 3. Convergence check

After the first wave, group candidates by root cause, not title, endpoint, or
CWE. If several scouts converge on the same root-cause family:

- preserve one best-evidenced candidate for falsification and verification;
- do not count agreement as evidence;
- stop assigning discovery work to that family;
- redirect remaining capacity toward materially neglected surfaces;
- do not launch another discovery round merely to reconfirm a candidate already
  owned by verification.

The convergence record must identify the retained candidate, redirected roles,
and the uncovered surfaces they will investigate.

## 4. Adaptive second wave

Perform coverage-gap analysis after the convergence check. Launch zero to three
specialists only when at least one material condition exists:

- an uncovered attack surface or trust boundary;
- a newly discovered implementation or consumer;
- exact dependency/runtime behavior that was not inspected;
- a surviving primitive with an untested downstream transition.

Choose specialists from target evidence, for example cryptography/protocol,
parser/serialization, concurrency/lifecycle, filesystem/configuration,
execution consumer, or platform/runtime. Do not launch a fixed roster merely
because those labels exist.

Every adaptive scout needs:

- a named coverage gap;
- a bounded question and falsifier;
- evidence it receives and evidence it must produce;
- a unique path assignment not already `EXHAUSTED`, `KILLED`, or owned by
  verification;
- a stop condition.

### Execution-plane proof

An adaptive assignment is a plan, not an executed specialist. The root must
invoke the collaboration spawn primitive directly. It must not simulate a
specialist as another internal reasoning pass or call collaboration through a
shell/exec wrapper.

For every planned specialist:

1. call spawn_agent with a unique task name, a bounded input, and a fresh
   context;
2. record the spawn call ID plus the returned child thread/session ID;
3. call wait_agent only for a known live child ID;
4. require a separate child output ending with a child-generated
   SPECIALIST_RESULT_TOKEN=<token> that was absent from the spawn input;
5. consume the output in the root context and emit
   CONSUMED_SPECIALIST_RESULT_TOKEN=<same-token> after the child result;
6. derive execution counts from the transcript with
   automation/validate-adaptive-execution-provenance.py.

The authoritative transcript is the persisted root rollout bound to the root
thread ID emitted by the runner. Preserve the `codex exec --json` stream as a
diagnostic artifact, but do not use it alone to disprove or prove a spawn when
the installed CLI omits multi-agent events from that stream. Also preserve the
matched child rollout and a hash manifest.

ADAPTIVE_SPECIALIST_COUNT means completed child contexts whose output the root
consumed. A planned assignment, local reasoning pass, wait with an empty
receiver, failed spawn, prose claim, or unconsumed child output counts as zero.
When spawning fails, preserve the failure evidence, set
ADAPTIVE_EXECUTION_PROVEN=NO, and continue only with work that remains valid
without that specialist. Never rewrite the event as a successful pass.

Before a V11 build may enter blind validation, a synthetic execution regression
must prove all of:

ADAPTIVE_TRIGGERED=YES -> SPAWN_ATTEMPTS>=1 -> SPAWN_SUCCESS>=1 -> SPAWN_FAILURE=0 -> UNIQUE_SPECIALIST_IDS>=1 -> separate input -> separate output -> root receipt -> ADAPTIVE_EXECUTION_PROVEN=YES

Use config/CODEX_CLI_ADAPTIVE_EXECUTION_PROVENANCE_SCHEMA.json for the derived
evidence artifact. Unit fixtures prove validator behavior; only a real Codex
spawn transcript satisfies the engineering acceptance gate.

## 5. Primitive-to-impact chaining

A primitive is not automatically bounty-grade. For every surviving primitive:

1. identify the next security boundary;
2. test whether the primitive can cross that boundary;
3. bind every transition to source, runtime, or authoritative state evidence;
4. stop immediately when a required transition is impossible;
5. never invent attacker capabilities, victim behavior, credentials, network
   reach, or deployment assumptions to complete a chain.

Prefer the proven sequence:

`attacker input -> primitive -> capability gain -> next protected boundary -> protected resource/action -> concrete impact`

If the primitive itself already crosses a protected boundary, record
`NOT_REQUIRED` for further chaining and prove that concrete impact directly.
Otherwise use `ACTIVE`, `BLOCKED`, `EXHAUSTED`, `KILLED`, or `VALIDATED` for the
chain. A weak primitive without a validated transition cannot become `STRONG`.

## 6. Exact implementation escalation

When candidate correctness materially depends on a runtime, parser, framework,
database, cryptographic library, serializer, package manager, dependency, or
protocol implementation, documentation alone is insufficient.

Inspect the exact shipped or version-matched implementation source when it is
available. Bind the conclusion to:

- dependency/component name and exact target version or immutable revision;
- how that version is selected in the target build/artifact;
- implementation source and exact symbols/branches inspected;
- configuration, feature, platform, and compile-time conditions;
- the behavior the implementation evidence proves and what remains unknown.

If exact implementation source is unavailable, mark the path `BLOCKED` or the
candidate as needing consumer/runtime proof. Do not substitute documentation,
latest-main behavior, or a different version.

## 7. Termination rule

Launch another discovery wave only when at least one material launch condition
from section 4 is recorded. Stop when any of these holds:

- all material surfaces have adequate coverage;
- remaining paths are `BLOCKED`, `EXHAUSTED`, or `KILLED`;
- further rounds only repeat existing root-cause families;
- progress requires unavailable runtime/environment evidence or new
  authorization;
- all surviving candidates have moved from discovery into verification.

`BLOCKED` is not permission to fabricate an environment or broaden scope.
Record the exact evidence that could permit a future continuation. A correct
terminal result may be `NO VALID FINDING`.

## 8. Required pipeline

```text
scope + target reality + security model
  -> first wave: authority | representation | state/composition
  -> root synthesis + research-path registry update
  -> convergence check
  -> coverage-gap analysis
  -> zero to three adaptive specialist assignments when justified
  -> real spawn + unique child ID + separate output + root receipt
  -> KILL-oriented independent falsification
  -> specialist verification
  -> primitive-to-impact chaining
  -> safe runtime/manual proof
  -> post-proof prior-art/duplicate review
  -> final evidence judgment
  -> termination record
```

The root orchestrator owns the registry, assignments, convergence decisions,
and termination. Discovery agents cannot edit their own terminal status to
avoid independent review.
