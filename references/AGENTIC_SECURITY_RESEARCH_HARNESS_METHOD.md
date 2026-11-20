# Agentic Security Research Harness Method

<!-- AGENTIC_SECURITY_RESEARCH_HARNESS:v1 -->

## Purpose

This method turns useful patterns from public AI-security harnesses into a
local, evidence-gated research workflow. It intentionally does not adopt their
commands, payloads, service accounts, cloud dependencies, agent-spawning rules,
or claims of effectiveness.

## 1. Provenance and claim classes

Every external statement is one of:

| Class | Meaning | Allowed use |
|---|---|---|
| `UPSTREAM_CLAIM` | Author/vendor/project says it happened | Context and hypothesis only |
| `INSPECTED_IMPLEMENTATION_FACT` | Exact pinned file shows the property | Architecture and risk modeling |
| `REASONED_INFERENCE` | Conclusion derived from facts | Must retain assumptions/falsifier |
| `LOCALLY_VALIDATED_BEHAVIOR` | Reproduced in an authorized isolated fixture | Narrow factual claim only |

Do not collapse a bounty narrative, CVE attribution, benchmark result, tool
count, success rate, or ROI figure into an implementation fact.

## 2. Control-plane architecture

```text
operator authorization + target/scope card
                  |
                  v
        controller / campaign state
                  |
                  v
       stage-specific orchestrator
                  |
                  v
      typed deny-by-default broker
                  |
                  v
        isolated bounded worker
                  |
                  v
        append-only evidence store
                  |
          +-------+-------+
          |               |
          v               v
 provenance-bound     independent
 memory / RAG         verifier + human gate
```

The knowledge plane proposes. The broker authorizes. The worker executes only
an already-authorized typed action. The evidence plane records. The verifier
and human decide promotion. No article, prompt, skill, RAG hit, or tool output
may bypass the broker or self-promote.

## 3. Campaign state

Create one campaign record with:

- authorization and official scope snapshot;
- exact target, release, artifact hashes, topology, and platform;
- attacker starting role and protected property;
- stage budgets, worker limits, credentials, egress policy, and stop conditions;
- hypothesis, finding, demotion, attempt, evidence, cleanup, and prior-art
  ledgers;
- terminal status and unresolved blockers.

All state transitions are append-only events. A current view is derived from
events; do not overwrite failed hypotheses or contradictory evidence.

## 4. Hallucination quarantine and promotion

Every lead begins in `HYPOTHESIS_QUARANTINED`, including a lead from a human,
model, scanner, fuzzer, decompiler, RAG query, patch diff, or article.

Promotion ladder:

| State | Minimum proof |
|---|---|
| `CODE_DERIVED_HYPOTHESIS` | Exact target-native facts and source-to-sink theory |
| `BUILD_OR_STATIC_REPRODUCED` | Pinned artifact/build or exact static fact independently re-read |
| `CLEAN_SNAPSHOT_REPRODUCED` | Positive case repeats in a clean environment with baseline and negative control |
| `PRIMITIVE_VALIDATED` | Concrete read/write/execute/auth/state/fund primitive, not label or crash alone |
| `LOW_PRIV_REACHABLE` | Trigger works from the claimed lowest attacker authority |
| `IMPACT_GATE_PASS` | Nonzero capability delta to an unauthorized protected action/recipient |
| `MANUALLY_CONFIRMED` | A human independently reproduces the minimum harmless proof |
| `REPORT_READY` | `STRONG` plus manual confirmation plus `TRIAGER_PROOF=PASS` |

`DEMOTED` is a normal state. Record the contradiction, invalidated edge, former
state, new state, evidence, and whether retesting is justified. Use `KILL` for a
terminal reason such as no reachability, no primitive, no capability delta,
duplicate, ineligible scope, or environment mismatch.

Compiling a PoC is never terminal proof. A clean crash is not exploitability.
Exploitability is not low-privilege reachability. Low-privilege reachability is
not program impact. Valid impact is not report readiness.

## 5. Staged workflow

Use:

`scope/reality -> recon -> hunt -> adversarial validate -> trace -> impact -> manual confirmation -> report-readiness`

- **Scope/reality** freezes authorization, target, release, and program rules.
- **Recon** maps entrypoints, trust boundaries, high-authority consumers, and
  testable invariants.
- **Hunt** explores bounded target-native hypotheses. Its output cannot be
  `STRONG`.
- **Validate** is instructed to falsify and independently re-read evidence.
- **Trace** proves attacker-controlled data and state reach the exact sensitive
  consumer on the same current path.
- **Impact** applies the program capability-delta gate and severity ceiling.
- **Manual confirmation** reproduces the minimum harmless proof and cleanup.
- **Report-readiness** answers triager objections and indexes redacted evidence.

Use separate prompts and schemas per stage. Handoffs contain facts, artifact
references, unresolved assumptions, falsifiers, and budgets—not persuasive
narrative. Multi-agent parallelism is optional and explicit-only; the same
logical stages work in one agent.

## 6. Independent verification

The verifier receives:

- frozen target/release identity;
- exact claim and claimed attacker/server conditions;
- raw evidence references and hashes;
- baseline, one-variable negative control, oracle, and cleanup expectations;
- no scout confidence, severity, hidden answer, or expected output.

Require fresh environment state for environment-sensitive claims. For crashes,
separate reproducibility, attacker control, memory primitive, and final impact.
For source findings, re-read the cited code and verify the real caller,
configuration, release path, and sink. For binary findings, bind static and
runtime evidence to the exact shipped artifact.

## 7. Low-privilege and authority checks

Freeze the claimed starting authority before validation. Test from that role,
not from administrator, SYSTEM, root, maintainer, validator, or operator context
unless that is the actual attacker model. Record access-control failures before
the vulnerable code as evidence against reachability.

Hold authority constant in controls. A path that works only because the test
runner has a stronger account, filesystem ownership, debugger privilege,
network placement, or trusted signing key is not the claimed primitive.

## 8. Memory and knowledge loop

Store each memory atom with:

- source and immutable digest;
- target/product, component, release, configuration, topology, and platform;
- method, evidence state, result, falsifier, reviewer, and timestamp;
- validity horizon or expiry trigger;
- sensitivity and permitted retrieval audience.

Before a campaign, retrieve bounded relevant atoms. After a campaign, record
validated findings, killed hypotheses, failed techniques, defenses, coverage
plateaus, and cleanup outcomes. A RAG similarity match is a lead. It never
imports truth, authorization, target identity, severity, or a KILL decision.

Guard against memory poisoning: separate source text from local conclusions,
retain contradiction links, require hashes, score freshness, and prevent a
single model from writing and later self-validating the same conclusion.

## 9. Sessions and tool capabilities

Persistent sessions are capabilities. They reduce setup cost while retaining
authority across time, so lifecycle controls are part of the security model.

Persistent SSH, WinRM, debugger, browser, MCP, RE, and worker sessions reduce
setup cost but increase authority. Bind each to:

- campaign, target allowlist, user/role, transport, credential source, and
  working directory;
- permitted tools/actions and structured parameters;
- creation, last-use, expiry, cancellation, and revocation events;
- network/filesystem/process/resource limits;
- append-only command/result evidence and process-tree cleanup.

Recheck parent and child authorization before every tool call. Do not let a
stale session survive target, scope, role, or credential changes.

## 10. Context, model, and cost budgets

Treat context as a stage budget:

- retrieve the smallest relevant code/evidence slice;
- reduce scanner/fuzzer logs into indexed facts while preserving raw evidence;
- keep a rolling state summary, not full conversation replay;
- route cheap models to classification/summarization only when their output is
  independently checked;
- reserve stronger reasoning for trace, falsification, and synthesis;
- stop on duplicate evidence, exhausted hypotheses, budget ceiling, or a
  terminal KILL.

Expected reward or ROI may rank authorized candidates after scope and
eligibility checks. It cannot justify testing a forbidden target, ignoring a
severity floor, skipping low-privilege or impact proof, or inflating a finding.
Record zero-result campaigns honestly.

## 11. Reference-specific boundaries

- **Andy Gill articles / Harness Kit:** adopt quarantine, staged prompts,
  structured artifacts, context budgets, negative-result memory, and human
  judgment. The kit explicitly says it is not a functioning harness; no
  execution claim follows.
- **RAPTOR, Defending Code, Baby Naptime, Audit, VVAH:** adopt only abstract
  pipeline, fresh-verifier, runtime-feedback, adversarial-validation, typed
  report, and threat-model patterns. Their repositories remain external and
  reference-only. Source/tool execution needs separate authorization.
- **Anthropic OSS Scanner:** its online build and offline scan are different
  trust phases. A submitted Dockerfile is executable supply-chain input; local
  `tools/check` may reach the host/local network. Model-generated reports are
  unreviewed hypotheses. Enrollment, email disclosure, Docker/QEMU execution,
  and service terms remain outside this method.
- **Sequester bug-bounty-triage:** adopt observed-vs-inferred separation,
  independent validation, impact escalation, and concise evidence. Do not
  import its browser/email installation or live-validation authority.
- **REA:** adopt artifact routing, evidence envelopes, provenance, explicit
  limitations, and static-vs-runtime separation. Do not install npm packages,
  register MCP, run a target, or invoke Hopper/Ghidra/IDA/JEB/Frida/browser/
  device tooling from reference inclusion.

## 12. Minimum schema

```yaml
candidate_id: immutable
state: HYPOTHESIS_QUARANTINED
target_release: exact
attacker_starting_authority: exact
protected_property: exact
entrypoint: evidence_ref
trace: []
primitive: null
capability_delta: null
baseline: null
negative_control: null
oracle: null
clean_snapshot: NOT_RUN
low_privilege: NOT_RUN
independent_verifier: NOT_RUN
manual_status: NOT_TESTED
prior_art: NOT_RUN
cleanup: NOT_RUN
demotion_history: []
report_ready: false
```

Unknown is not PASS. Missing evidence is preserved as a blocker.
