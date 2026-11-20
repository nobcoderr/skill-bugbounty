# Offensive Research Graph Engineering Method

This method adapts graph engineering to authorized red-team, offensive
security, and bug-hunting research. It treats graph width as a scheduling
property, not as evidence quality.

## 1. Decide whether a graph is warranted

List the proposed jobs and ask whether each downstream job consumes an upstream
output. Independent jobs may fan out. Jobs sharing attacker state, runtime
state, a mutable artifact, or an exploit prerequisite remain ordered.

Return `GRAPH_NOT_NEEDED` when the work is small, exploratory, requires tight
step-by-step steering, or forms a genuinely sequential chain.

## 2. Compile nodes and edges

Each node records:

```text
NODE_ID
ROLE
SCOPE_SLICE
IMMUTABLE_INPUTS
REQUIRED_UPSTREAM_OUTPUTS
ALLOWED_ACTIONS
WORKSPACE
OUTPUT_SCHEMA
EVIDENCE_ANCHORS
ACCEPTANCE_ORACLE
TIME_COST_BUDGET
STOP_CONDITIONS
```

An edge is valid only when a named producer output satisfies a named consumer
input. Narrative order, file adjacency, shared CWE labels, or agent agreement
do not create edges.

## 3. Offensive-security topology

Use this default shape only when the dependencies fit:

```text
scope + target reality + threat model
              |
              v
 independent surface scouts
  authority | representation | state | release
              |
              v
 root-cause deduplication and KILL triage
              |
              v
 primitive proof -> attacker-state recomputation
              |
              v
 severity expansion / newly reachable surfaces
              |
              v
 fresh-context evidence verifier
              |
              v
 final impact gate -> human reproduction
```

Cross-file, cross-service, or cross-stage paths belong in a shared chain node or
must be reassembled through proven capability edges. Do not fragment away the
very relationship being audited.

## 4. Safe fan-out

- Cap total nodes, concurrently running nodes, retries, time, and cost before
  execution. Runtime capacity is authoritative; a vendor's advertised ceiling
  is not.
- Queue excess ready nodes in bounded waves.
- Assign one owner per mutable workspace. Use isolated worktrees or disposable
  workspaces for writers; store results separately from target source.
- The root owns merges and conflict decisions. Workers never run shared reset,
  checkout, clean, force-push, or broad deletion commands.
- Stop a wave on scope drift, unexpected third-party data, destructive effect,
  cost breach, runaway retries, or safety-signal loss.

## 5. Prevent graph self-agreement

Discovery nodes emit hypotheses only. Deduplicate by exact root cause and
evidence identity. A verifier uses a fresh context and receives no discovery
rhetoric or severity. Freeze rules and acceptance tests before execution; no
research node may tune them after seeing results.

Treat those immutable rules and tests as the frozen acceptance oracle for the
entire graph.

Truth anchors include executed tests, sanitizer/crash output, immutable request
and response operation IDs, source hashes, exact call chains, authoritative
before/after state, patched controls, and researcher replay. Agent count,
consensus, and confidence are never anchors.

## 6. Failure and retry

Classify a failure before retrying: dependency, reachability, representation,
type, lifetime, privilege, environment, nondeterminism, verifier rejection,
workspace conflict, cost, or scope. Change only the failed dimension and retry
only when new material evidence exists. Two zero-evidence waves terminate the
same lane.

## 7. Measure the right things

Track unique evidence atoms, independently reproduced primitives, valid chain
edges, newly covered trust boundaries, false positives, cost, and elapsed time.
Do not optimize raw candidate count, agent count, passing verifier count, or
nominal severity; those are Goodhart-prone.

## 8. Completion

The graph completes when all nodes are terminal, no dependency-ready node can
add material evidence, a safe terminal impact is proven, or a mandatory scope,
safety, environment, cost, or user boundary stops work. Preserve incomplete
nodes as `BLOCKED`; do not narrate them into success.
