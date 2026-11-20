# WebHackList 2026 Corpus Method

## Provenance and status

`WEBHACKLIST_2026_CORPUS_METHOD:v1`

This method is derived from a complete metadata and byte-coverage pass over the
official WebHackList `2026-ai` collection at repository commit
`2f17d6249c178f9b895d2c00536a3009df117afa` on 2026-10-12.

- Official collection records: 299.
- Archived Markdown records read fully: 298.
- Archived bytes read: 12,121,660.
- Archived words tokenized for coverage accounting: 1,458,190.
- Local-copy gaps: one; its primary URL was reviewed through a fresh indexed
  render after direct retrieval returned HTTP 403. This is not a byte-exact
  capture.
- Archive status: preliminary, unranked, AI-collected, incomplete, not
  community-vetted, and subject to change.
- Rights: WebHackList tooling is MIT; preserved research keeps its original
  terms. No article body or executable PoC is vendored into this skill pack.

The authoritative record ledger and deterministic hashes are in
`config/WEBHACKLIST_2026_AI_CORPUS.json`.

## Why this corpus is useful

The archive spans browser, HTTP, identity, server, AI-agent, supply-chain,
native-runtime, cloud, Web3, and methodology research. Its useful contribution
to this pack is not a list of bug names. It is a set of recurring evidence
questions that expose where systems check one object and consume another, or
where two individually bounded behaviours compose into a larger capability.

## Cross-corpus method families

### 1. Representation ledger

For each candidate record:

| Stage | Required evidence |
|---|---|
| Input bytes/object | Attacker control and exact provenance |
| Transform | Decode, normalize, parse, serialize, translate, cache, or copy |
| Security check | Exact representation and policy applied |
| Selected object | Identity/path/field/member chosen by the check |
| Consumed object | Exact object used by the final component |
| Authority | Privilege held by that consumer |
| Effect | Authoritative protected-state change or read-back |

High-value hypotheses often appear when the checked and consumed rows diverge.

### 2. Authority ledger

Track issuer, subject, namespace/store, audience, scope, lifetime, revocation,
consumer, and protected action separately. A valid token or signature does not
prove that the correct identity, store, resource, or operation was bound.

### 3. Protocol and parser differentials

Compare every hop's framing and normalization. Require a byte-level or typed
model of what each parser accepts and forwards. A generic parser mismatch is a
hypothesis until the downstream consumer and cross-user/cross-boundary effect
are shown.

### 4. Browser and UI authority

Separate source origin, initiator, target origin, browsing context, extension
privilege, navigation semantics, user gesture, and final privileged channel.
Visual surprise alone is not an authority transition.

### 5. Agent context and tool authority

Treat retrieved content, rule files, chat templates, MCP descriptions, cached
model state, and tool output as untrusted data. Prove the exact path from
content to tool selection, approved arguments, worker authority, and protected
effect. Model compliance or refusal is not a security oracle.

### 6. Execution consumers

Inventory deserializers, template engines, dynamic evaluators, command
wrappers, package installers, test runners, built-in administrative actions,
and native bridges. Prove reachability and authority without assuming that a
dangerous primitive is exposed to the attacker.

### 7. File and secondary-consumer chains

Follow an artifact past initial upload or extraction into renderers, image and
document libraries, browser navigation, shell/CLI option grammars, loaders,
backup/restore, and scheduled jobs. Path existence and file creation are not
terminal impact without the protected consumer.

### 8. Supply-chain and release reachability

Bind repository, branch, workflow event, trust context, cache/artifact identity,
package/dependency authority, signing/publishing identity, and released
consumer. A CI primitive is not production compromise unless the exact release
path preserves the capability.

### 9. State, lifecycle, and retry

Model pre-state, transition, post-state, revocation, cleanup, retry, and
terminal failure. Missing current state does not prove an operation never
started. For races, measure attacker-controlled timing and reliability under a
realistic topology.

### 10. Arithmetic and invariant composition

Specify the property using arbitrary-precision math. Compare producer and
checker domains independently, including per-item versus aggregate effects,
rollback, commit, finality, and spendability. Matching overflow or truncation
in producer and safety checker is a composition hypothesis, never permission
to test a public ledger.

### 11. Evidence quality

Require a deterministic oracle, baseline, one-variable negative control,
falsifier, exact source/release digest, environment/topology, cleanup, and stop
condition. Status codes, crashes, timing anomalies, scanner hits, and model
assertions are leads until the protected effect is independently read back.

### 12. Prior-art and impact remain independent

Freeze the earliest public-disclosure cutoff and compare mechanisms under
equivalent constraints. Severity, bounty, fame, CVE assignment, target size,
and later adoption do not establish novelty. Conversely, a duplicate technique
can still be technically valid. Apply current-release reachability and the
program impact boundary separately.

## Candidate worksheet

```text
candidate_id:
target/release:
scope and exclusions:
attacker starting authority:
attacker-controlled input:
representation transforms:
checked object:
consumed object:
authority-bearing consumer:
protected effect:
closest intended path:
baseline:
one-variable negative control:
falsifier:
deterministic oracle:
current-release evidence:
novelty cutoff:
closest pre-cutoff source:
material distinction:
prior-art state:
program-impact state:
safe proof and stop condition:
```

## Fail-closed rules

- `UNKNOWN` is never `PASS`.
- A metadata or family match is never a duplicate decision.
- A missing source is never proof of novelty.
- A source claim is never a locally verified fact without independent evidence.
- A local or synthetic PoC is never automatic production reachability.
- An archived command or payload is never authorization.
- A corpus-derived method is never a finding.

