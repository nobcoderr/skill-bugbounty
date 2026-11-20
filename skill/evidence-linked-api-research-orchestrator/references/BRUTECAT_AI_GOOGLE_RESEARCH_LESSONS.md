# Sanitized Lessons from “Hacking Google with A.I. for $500,000”

Source: <https://brutecat.com/articles/hacking-google-with-ai/>

This reference distills the user-supplied article into reusable engineering
methods. Historical claims and bounty amounts are public prior art, not target
ground truth for a new assessment. No API key, cookie, credential, live exploit
payload, private identifier, or reproduction recipe is retained here.

## Methodology atoms retained

1. **Machine-readable descriptions scale coverage.** Discovery documents,
   OpenAPI, protobuf descriptors, and GraphQL SDL turn undocumented breadth into
   typed methods that can be grouped and tracked.
2. **Group before testing.** Resource-centered groups keep model context small
   while allowing verified IDs and architecture facts to flow to later groups.
3. **Enforce a completion contract.** A dedicated finish gate can prevent early
   exit, but it must allow scoped `BLOCKED` and `NOT_APPLICABLE` states rather
   than forcing unsafe probes.
4. **Narrow the tool interface.** Let a sealed backend own hostname, version,
   verb, schema, auth material, and restrictions. Let the model choose only the
   typed values relevant to the security hypothesis.
5. **Normalize platform errors empirically.** Classifying which rejection stage
   produced a response is useful for navigation, but only when calibrated with
   target-native one-variable controls.
6. **Preserve variant identity.** When approved credentials or configurations
   legitimately produce different results, execute the same operation across
   the allowlisted variants and group equal bodies by hash without losing
   provenance.
7. **Operation IDs convert model output into reviewable evidence.** Every claim
   points to immutable request/response records that a human can inspect and
   replay. This sharply separates hallucination from observation.
8. **Filter noise with impact rules.** Introspection, endpoint discovery,
   existence enumeration, generic errors, and 2xx responses without protected
   data or state are research signals, not vulnerabilities.
9. **Schemas can expose more than REST paths.** For GraphQL, derive bounded
   query paths and validate syntax/types before sending requests. Coverage must
   reflect the graph paths actually exercised.
10. **Staging labels do not define data trust.** Determine whether a test host
    reaches production data or authorization through harmless owned markers;
    do not assume either equivalence or separation from naming.
11. **Read and write need distinct proof.** A readable object does not prove a
    mutation path. A mutation response, including a server error, does not prove
    a side effect without authoritative read-back and cleanup.
12. **AI value is tireless consistency, not authority.** The harness supplies
    typing, routing, coverage, and traceability. Human/manual reproduction and
    the program-impact gate decide whether a finding is real.

## Explicitly rejected transplantations

- collecting keys from apps, binaries, browser traffic, or public artifacts;
- replaying historical credentials or requests;
- broad hostname discovery, label brute force, or high-volume matrices without
  a program-approved allowlist and rate plan;
- using personal or third-party accounts as victims;
- assuming provider-specific authentication or error behavior applies elsewhere;
- reproducing public fixed bugs against live services.

The transferable lesson is evidence-linked orchestration: schema coverage,
bounded typed execution, operation-backed claims, replay, and strict impact
controls.
