# Sanitized Lessons from “StubZero: $148,337 RCE in Google Cloud Production”

Source: <https://brutecat.com/articles/google-cloud-rce/>

Published 22 May 2026. The article describes public, fixed historical research
and identifies CVE-2026-2031. This file retains only transferable reasoning
patterns. It intentionally omits API keys, cookies, live hosts, internal
addresses, exact endpoint paths, task payloads, filter expressions, customer
identifiers, and reproduction commands.

## Chain shape retained

### Historical chain family A

```text
descriptor/debug disclosure
  -> exact typed request/response knowledge
runtime queue disclosure
  -> required workflow namespace/selector
workflow creation and controlled multi-principal approval
  -> published attacker-controlled workflow
privileged internal-RPC task consumer
  -> service-identity RPC capability
per-method policy and harmless invocation evidence
  -> provider-recognized production-compromise impact
```

The key lesson is that the first disclosures were not terminal. Each created a
specific capability that satisfied the next stage's prerequisite.

### Historical chain family B

```text
parent/child authorization mismatch
  + identifier initially impractical to guess
global test-artifact disclosure or predicate oracle
  -> child/version identifier becomes obtainable
cross-parent resource lookup
  -> full workflow configuration disclosure/control
internal task accepted through an alternate execution consumer
  -> deeper privileged-worker reachability
service-identity/policy confirmation
  -> production-compromise classification
```

This family demonstrates why exploitability and authorization correctness are
separate questions: a UUID-based IDOR may be real but initially unreachable,
then become practical only after a second primitive discloses or derives the
identifier.

## Engineering lessons

1. **Descriptor leakage changes attacker capability.** It can supply exact types
   needed to decode opaque responses and construct valid downstream requests.
2. **Representation failures can hide successful backend work.** A JSON mapping
   error may coexist with a structured binary response. Preserve wire format,
   decoder, and schema provenance rather than treating status 500 as terminal.
3. **Metadata can be the missing prerequisite.** A queue item or execution log
   may disclose a namespace, client selector, task name, or resource linkage
   needed by a later authorized test.
4. **Patch the semantic operation, not one route name.** Inventory aliases,
   versioned services, support/execution/auth counterparts, and shared handlers.
5. **Rollout drift is evidence, not a retry strategy.** Alternating authorization
   results require bounded, permitted cohort analysis and a patched control.
6. **Approval chains are multi-principal state machines.** Two owned accounts do
   not eliminate the need to prove ACL, role, identity, and state continuity.
7. **Service identity is a distinct authority plane.** A workflow worker may
   call internal RPCs under service authority while separately carrying end-user
   context. Model both identities and the actual per-method policy.
8. **Internal RPC is not automatically universal RPC.** The reachable method set
   is constrained by caller identity, credential-forwarding rules, and method
   authorization. Severity follows demonstrated authority, not primitive name.
9. **Canonical ownership beats reflected paths.** A response may splice the
   request's parent into an object name even when the looked-up child belongs to
   a different parent. Trace stored parentage at the lookup and policy check.
10. **Entropy is a prerequisite question.** A high-entropy child ID can block a
    practical chain until a separate disclosure or oracle supplies it.
11. **Alternate consumers deserve separate analysis.** Test, preview, debug,
    synchronous, and asynchronous paths can reach different workers and policy
    layers.
12. **Stack traces prove reachability, not RCE.** Disk, credential, or RPC-policy
    exceptions show which consumer ran; terminal impact still needs harmless
    execution evidence or provider confirmation.
13. **Stop signals are evidence.** When the program confirms critical impact and
    instructs the researcher to stop, preserve that confirmation as the terminal
    adjudication rather than seeking more blast radius.

## Non-transferable details

Do not reuse historical credentials, exact endpoints, internal hostnames,
workflow/task payloads, predicate-oracle syntax, or customer data. Do not probe
Google or any other provider merely because the article is public. New research
requires its own current authorization, scope, rate/concurrency limits, owned
fixtures, cleanup, and operation-linked evidence.

The reusable artifact is the reasoning architecture: capability-producing
disclosure, semantic counterpart enumeration, canonical resource binding,
multi-principal state, privileged-consumer proof, method-policy evidence, and
strict stop conditions.
