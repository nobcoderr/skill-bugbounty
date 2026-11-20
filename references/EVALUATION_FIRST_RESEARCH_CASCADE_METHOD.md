# Evaluation-First Research Cascade Method

## Purpose and source boundary

Turn target-native observations into a repeatable research loop whose creative
steps can explore broadly while deterministic gates keep the evidence precise.
This method distills general research-system lessons from James Kettle's 2026
PortSwigger paper, [Can AI do novel security research? Meet the HTTP
Terminator](https://portswigger.net/research/can-ai-do-novel-security-research).

Use the source as methodology prior art only. Do not copy its HTTP payloads,
named technical discoveries, target set, or exploitation workflow into live
candidate generation. Treat the paper's complete technical lineage as
ineligible for held-out evaluation of any package trained with this method.

## 1. Design evaluation before ideation

Create a four-part blueprint:

1. **Objective:** the protected property or unexplored system behavior.
2. **Evaluation strategy:** the smallest safe experiment that can distinguish a
   real effect from ordinary variation.
3. **Inspiration sources:** small target-native or non-vulnerability fragments
   that vary the search space without revealing an expected answer.
4. **Cascade routes:** ways a proven observation can generate adjacent,
   independently testable questions.

Do not start high-volume ideation until the evaluation oracle, false-positive
controls, abort conditions, and cleanup are defined. A weak oracle turns scale
into noise.

## 2. Use bounded micro-inspiration

Feed ideation one compact fragment at a time. Prefer:

- target code, tests, types, comments, and architecture contracts;
- protocol or file-format requirements that do not describe vulnerabilities;
- runtime anomalies already observed in an owned fixture;
- a previously proven discovery represented only by its abstract invariant.

For every fragment record a stable source identifier, provenance kind, concise
abstraction, and whether vulnerability ground truth is present. In novelty mode
the last value must be false. Do not mix multiple rich examples into one prompt;
extra context can anchor the model on known techniques instead of the underlying
principle.

Review early output and encode rejection rules for recurring low-value answers.
Reject pattern replay, familiar payload templates, untestable speculation, and
ideas that do not bind to target facts. Do not encode the hidden target answer
as a rejection rule.

## 3. Separate creative search from acceptance

Use AI for hypothesis diversity, code for reproducible orchestration and
acceptance checks, and a human for safety, scope, novelty, and final judgment.
Model agreement is never the oracle.

The deterministic evaluator must record:

- the security property under test;
- a stable baseline and one-variable perturbation;
- an authoritative observable independent of the model's prose;
- explicit acceptance and rejection predicates;
- negative and false-positive controls;
- anomaly channels capable of retaining unexpected effects.

Design the oracle around an invariant violation, not the exact response or bug
class expected by the researcher. Preserve raw evidence for evaluator review.

## 4. Defend the evaluator from gaming

Assume the hypothesis generator may accidentally satisfy a weak validator
without proving the intended property. Require deterministic checks that bind
the baseline, perturbation, affected principal or resource, and authoritative
effect to distinct evidence values.

Reject:

- status codes, log text, crashes, or response length alone;
- fingerprints that can match the stimulus or baseline itself;
- client-side reuse or local state mistaken for server-side contamination;
- non-deterministic success criteria selected after seeing the result;
- a model-generated assertion without machine-readable evidence.

Version evaluation rules as data where practical. Keep anomaly channels
extensible so a new observation can be retained without weakening the primary
oracle.

## 5. Isolate research stages

Run ideation, evaluation, impact proof, cascade generation, and final judgment
with fresh or evidence-only context. Handoff only source slices, normalized
inputs, deterministic scripts, measurements, and prior-stage verdicts required
by the next stage. Do not pass suspected fixes, hidden ground truth, expected
bug class, or persuasive narrative.

Record `target_answer_leakage=false`. If a stage receives hidden target facts,
mark the run contaminated and exclude it from blind-generalization claims.

## 6. Convert leads into safe impact proof

An anomalous effect is a research lead. Promote it only after the source path,
consumer, state, protected boundary, baseline, negative control, and realistic
release composition are proven.

Use local fixtures, researcher-owned environments, or an explicitly authorized
allowlist with conservative rate and concurrency limits. Never disguise a real
target as a simulator, let an agent switch targets, automate victim-data access,
or use harmful volume to make a proof succeed. Stop at the minimum harmless
evidence required by the program.

## 7. Build a provenance-preserving cascade

For every proven observation ask two abstract questions:

1. How could equivalent behavior be detected in another implementation or
   path?
2. Does the mechanism that produced the behavior expose a different protected
   effect?

Create child hypotheses with a parent identifier, discovery-chain evidence,
new invariant, and independent evaluation plan. A child cannot inherit the
parent's runtime or impact proof. Feed only the abstract mechanism into the next
ideation context; do not replay the parent payload.

Search pairs before bounded triples. Preserve unexpected anomalies even when
they fall outside the original research class, but require a new scope and
safety gate before testing them.

## 8. Distinguish research value from one-off defects

Classify observations as:

- `ONE_OFF_LEAD`: reproducible on one fixture but no transfer evidence;
- `TRANSFER_SUPPORTED`: the invariant applies to independent implementations
  or semantically equivalent paths;
- `REALISTIC_COMPOSITION_PROVEN`: the effect survives a real deployment or
  release composition;
- `PROTECTED_IMPACT_PROVEN`: a safe end-to-end security boundary is crossed.

Do not call a technique broadly novel from one unusual implementation. Do not
discard a one-off lead if it can seed a new cascade, but keep it below finding
status until the ordinary evidence gates pass.

## 9. Preserve benchmark integrity

Keep evaluator seeds, expected findings, patches, and target counts outside the
auditor package. A curator must reject any held-out family derived from this
paper or its technical descendants. Rule regressions may test the loop's
contracts, but they do not demonstrate novel discovery.

Measure at least false-positive bounty grade, hard failure, prior-art leakage,
context contamination, evaluator gaming, code-derived hypotheses, and exact
held-out discovery. Never inherit results across package hashes.
