# Repeated-Token LLM Security Method

## Contents

1. Purpose and prior-art boundary
2. What the Dropbox repository actually demonstrates
3. Bug-bounty threat model
4. Representation and authority maps
5. Candidate classes and hard verdicts
6. Controlled experiment design
7. Evidence and proof levels
8. Prior-art and novelty workflow
9. Remediation and regression strategy
10. KILL rules

## 1. Purpose and prior-art boundary

Use this reference for authorized AI/LLM product audits where repeated tokens,
repeated characters, tokenizer behavior, or prompt representation may weaken
instruction adherence. Convert the model behavior into a bounty candidate only
when it crosses a real protected boundary.

The public sources are:

- Dropbox `llm-security`, main commit
  `d5cd5615de671f2461ce542669aec0e9a881b00a`;
- Dropbox's July 2023 control-character prompt-injection research;
- Dropbox's March 2024 repeated-token/divergence follow-up;
- Nasr, Carlini, et al., *Scalable Extraction of Training Data from
  (Production) Language Models*, arXiv:2311.17035.

Treat these sources as historical prior art and methodological inspiration.
Do not treat their old model names, thresholds, token IDs, outcomes, or filters
as current facts. Do not replay their effective sequences against a live model
without explicit written authorization and strict test limits.

## 2. What the Dropbox repository actually demonstrates

The repository is Apache-2.0 experimental research code and stored results. It
is not a Dropbox production backend, product source tree, or vulnerability
scanner. At the verified main commit it has no releases, tags, or repository
security advisories and contains three primary harnesses:

| Harness | Historical method | Evidence produced | Important limitation |
|---|---|---|---|
| `repeated-tokens.py` | Sample token strings or repeat selected token sequences against old Chat Completions models | Prompt/output, token usage, timing, finish reason, token IDs | Old model allowlist and provider behavior; can incur cost and generate unsafe unexpected text |
| `repeated-sequences.py` | Search repeated byte/character sequences and binary-search a blackout threshold between two questions | Repeat threshold, prompt-token count, response, model-based answer judgment | Uses another LLM as judge; judgment is not independent and can be stochastic or injection-sensitive |
| `question-with-context.py` | Place repeated sequences before questions inside a content-constrained Q&A template | Instruction betrayal, context loss, hallucination, or apparent prompt leakage | The template is sent as one `user` message; it does not by itself prove bypass of a true system-role boundary |

`common/strings.py` constructs UTF-8 strings covering almost all of the
historical `cl100k_base` token alphabet and checks token encode/decode
round-trips. `common/openai.py` calls the historical Chat Completions endpoint
with fixed old model names and simple retries. The stored output files are
historical experiment artifacts, not current reproduction evidence.

The research distinguishes two related effects:

1. **instruction blackout/betrayal:** repeated representation causes earlier
   constraints or context to be ignored;
2. **model divergence:** repetition shifts an aligned conversational model
   toward a lower-level language-modeling mode, sometimes producing apparent
   memorized text.

Dropbox reported multi-token extraction findings to OpenAI in January 2024.
The vendor confirmed the training-data extraction issue and expanded filtering;
server-side timeouts were also added. The exact historical lineage is public
and is not a new bug-bounty finding.

## 3. Bug-bounty threat model

Use this complete product chain:

```text
attacker-controlled bytes or content
  -> transport decoding and Unicode normalization
  -> tokenizer and token IDs
  -> chunking, truncation, and prompt construction
  -> system/developer/user/tool roles and provenance
  -> provider filter, model router, fallback, and model
  -> textual output, structured plan, or tool arguments
  -> deterministic policy, authorization, and confirmation
  -> retrieval, memory, tool, API, or agent action
  -> protected boundary
  -> concrete impact
```

Model the attacker position:

- direct user input;
- indirect content in a webpage, document, email, image/OCR result, or issue;
- content indexed into RAG or persistent memory;
- tool/API output later reinserted into a prompt;
- cross-user or shared-workspace content;
- attacker-controlled metadata, filenames, titles, alt text, or hidden fields.

Model the protected boundary separately:

- tool or API authorization;
- tenant, project, conversation, file, or vector-store isolation;
- RAG document ACLs and deletion/revocation state;
- confidentiality of synthetic secrets or private context;
- integrity of persistent memory or privileged configuration;
- agent confirmation, transaction, or action policy;
- explicitly eligible model privacy or training-data boundary.

## 4. Representation and authority maps

### Representation map

| Stage | Required observation |
|---|---|
| Raw input | Exact bytes, content type, encoding, and source |
| Decode | JSON/string escaping, Unicode normalization, control removal, newline handling |
| Preprocess | Truncation, chunking, deduplication, templating, retrieval formatting |
| Tokenizer | Name/version, token IDs, token count, round-trip behavior |
| Prompt | Exact message roles, ordering, delimiters, hidden wrappers, tools/schema |
| Router/filter | Rejection, rewrite, fallback, model selection, moderation state |
| Model | Snapshot/configuration, output/plan, finish reason, latency |
| Consumer | Parser, tool dispatcher, RAG query, policy engine, backend action |

Do not compare only character counts. Record bytes, Unicode code points, tokens,
and positions. Repetition may be mono-token, multi-token, control-character,
space-character, or created only after normalization or templating.

### Authority map

| Stage | Required observation |
|---|---|
| Attacker | Account, tenant, content ownership, allowed input channel |
| Victim context | Researcher-owned second account/workspace and realistic state |
| Model | No authority by itself; records only output or plan |
| Tool dispatcher | Tool allowlist, schema, argument validation, confirmation |
| Credential | Subject, tenant, scope, audience, expiry, revocation |
| Backend | Object ownership and authorization decision |
| Effect | Authoritative read-back or state change |

The maps must meet at the same action. Never replace a missing authorization
edge with the statement that the model was manipulated.

## 5. Candidate classes and hard verdicts

### Repeated input changes only the response

Examples include forgotten context, instruction betrayal, nonsense,
hallucination, or out-of-context answers. Verdict: **KILL** unless the official
program explicitly rewards that exact model-safety behavior.

### Repeated input reveals prompt text

Prove the text is truly hidden, non-public, current, and protected. Generic
instructions are normally **KILL**. Retain only actual secrets or a disclosure
that enables a separate proven boundary bypass.

### Repeated input influences a tool or agent action

Retain only when the backend accepts an unauthorized action or read under a
principal that the attacker should not control. Capture tool name, arguments,
credential subject/scope, policy decision, confirmation state, and state diff.

### Repeated input bypasses RAG or memory isolation

Use researcher-owned A/B documents and unique canaries. Prove source ACL,
ingestion/index state, retrieval identity, unauthorized principal, exact chunk,
and state before/after. A hallucinated canary-like string is not retrieval.

### Repeated input manipulates an authorization decision

Authorization must be deterministic and server-side. If the model itself is
trusted to decide access, prove the server executed that decision without an
independent policy check. Mere model classification disagreement is **WEAK**.

### Memorized training-data extraction

Pursue only when explicitly eligible. Require a protected data definition,
statistical evidence, public-source and common-sequence controls, independent
verification, and data minimization. Stop immediately if real third-party PII,
credentials, or sensitive text appears. Prefer a synthetic memorization fixture
in an owned local or fine-tuned model.

### Long output, latency, or cost

Treat as availability/resource-exhaustion research. It is **KILL** when DoS,
rate-limit, quota, or cost findings are excluded. Never run high-volume or
unbounded-output experiments merely to prove this class.

## 6. Controlled experiment design

Do not run a live experiment until the user supplies:

- exact authorized target/model/API;
- eligible vulnerability class;
- request, token, output, time, and cost limits;
- maximum concurrency (default one);
- stop conditions for unsafe output, third-party data, or unexpected actions;
- evidence storage and cleanup rules.

Record this matrix for every trial:

| Trial | Raw input hash | Tokenizer/version | Token IDs/hash | Repeat structure/count | Prompt roles/position | Model/router | Filter result | Output class | Tool/RAG/backend effect |
|---|---|---|---|---|---|---|---|---|---|
| Baseline | | | | none | | | | | |
| Length control | | | | matched tokens | | | | | |
| Structure control | | | | non-repeated | | | | | |
| Candidate | | | | repeated | | | | | |
| Tool-disabled | | | | repeated | | | | | |
| Credential/ACL control | | | | repeated | | | | | |

Use at least these controls:

1. ordinary semantic baseline;
2. token-budget-matched but non-repeated input;
3. repeated input that preserves the same task but lacks the suspected
   representation feature;
4. tool disabled or no-op tool;
5. credential removed/revoked or A/B ownership changed;
6. exact same request repeated enough times to measure stochastic behavior;
7. current and sibling model/router comparisons only when scope permits.

Use deterministic task assertions where possible. Do not let the same model
serve as the sole judge of whether it was compromised. If semantic review is
needed, preserve blinded manual criteria and raw output hashes.

Use synthetic assets:

- unique random canary in an owned private document;
- no-op or reversible tool action;
- empty test repository/calendar/object;
- synthetic secret present only in an owned fixture;
- local model fine-tuned on synthetic memorization samples.

## 7. Evidence and proof levels

- **T0 — Pattern:** public research or a suspicious prompt is similar.
- **T1 — Representation:** raw input, normalization, tokenizer, token IDs, and
  prompt roles are observed on the current path.
- **T2 — Differential:** repeated behavior is reproducible against matched
  token-budget and semantic controls.
- **T3 — Bridge:** model output reaches an actual tool, RAG, memory, policy, or
  API consumer.
- **T4 — Boundary:** researcher-owned A/B assets show unauthorized disclosure
  or mutation.
- **T5 — Backend:** logs/read-back prove acting identity, policy decision,
  effect, negative control, and cleanup.
- **T6 — Reality:** current deployment, scope eligibility, repeated trials,
  prior-art novelty, and manual reproduction pass.

Only T6 is report-ready. An impressive completion at T2 remains **KILL** or
**WEAK** for ordinary product-security programs.

## 8. Prior-art and novelty workflow

Search before expensive experiments:

- exact repeated-token/character language;
- instruction blackout, prompt injection, divergence, memorization, training
  data extraction, and repetition-filter bypass;
- target model cards, security/safety docs, known limitations, release notes,
  API changes, and vendor comments;
- public issues, discussions, PRs, advisories, papers, evaluations, and bounty
  known issues;
- target-specific tool, RAG, authorization, or tenant-isolation root causes.

Separate lineages:

1. historical model robustness or privacy issue;
2. application prompt-construction weakness;
3. missing deterministic tool/backend authorization;
4. RAG/memory ACL defect;
5. current filter/parser/tokenizer regression.

Do not rename a public repeated-token model behavior as a new application
finding. A candidate survives novelty only when the current product contributes
a distinct missing invariant and concrete protected-boundary impact.

## 9. Remediation and regression strategy

Apply defense in depth:

1. keep authorization, tenant checks, and confirmation outside model reasoning;
2. preserve provenance and untrusted-content labels through RAG, memory, tool
   results, prompt construction, and retries;
3. inspect repetitions after relevant normalization and tokenization, including
   multi-token n-grams and local/global concentration rather than one literal;
4. cap input/output tokens, time, retries, tool calls, recursion, and spend;
5. require strict tool schemas, action/object allowlists, scope-bound
   credentials, and authoritative server-side checks;
6. recheck retrieval ACLs at query and read/use time; include tenant, user,
   model, policy, and ACL version in cache keys;
7. separate model-generated content from executable instructions and sensitive
   policy decisions;
8. maintain model/tokenizer/version-specific regression evaluations with
   matched controls and backend boundary assertions;
9. treat provider filters as one layer, not the security boundary.

## 10. KILL rules

KILL when:

- only jailbreak, refusal bypass, hallucination, instruction betrayal,
  divergence, or wrong answers are shown;
- a one-user prompt template inside one `user` message is mislabeled as a
  system-role bypass;
- prompt disclosure contains no secret or enabling security information;
- alleged memorization lacks independent/public-source controls;
- model output never reaches a protected consumer;
- the tool/backend authorizes the action correctly or the same user already
  had equivalent authority;
- RAG data is public, attacker-owned, or legitimately accessible;
- only latency, token burn, or DoS remains and the class is excluded;
- the model/version/filter evidence is historical, unknown, or one-off;
- the issue is public, fixed, documented, known, duplicate, or out of scope;
- proof requires unsafe token search, unbounded cost, third-party data,
  credentials, destructive actions, or unauthorized testing.

If nothing survives, return **NO VALID FINDING**.
