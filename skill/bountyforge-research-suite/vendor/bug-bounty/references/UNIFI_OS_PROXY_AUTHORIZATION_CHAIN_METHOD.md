# UniFi OS Proxy Authorization and Root-Chain Method

## Purpose and prior-art status

Use this method for authorized review of consolidated appliances and service
platforms where one reverse proxy authenticates requests and dispatches them to
multiple loopback-only applications. It distills the methodology from
Catchify's July 2026 UniFi OS research covering CVE-2026-34909,
CVE-2026-50747, and CVE-2026-50748.

The disclosed UniFi paths, vulnerable route families, payload shapes, and
privilege-escalation wrapper are public prior art. The article reports fixes in
UniFi OS 5.1.11/Server 5.0.8 with the relevant root-cause fix in 5.1.15,
Access 4.2.29, and Talk 5.2.2. Re-check the official advisories and the exact
deployed build before relying on these version statements. Treat the published
roots as duplicate-burn entries; retain only a distinct root, incomplete fix,
or materially different protected consumer in a current in-scope release.

This reference is a reasoning method, not authorization to test an appliance,
Internet host, or downstream service. Prefer extracted firmware, a local
emulator, or researcher-owned hardware. Keep live proof within the current
program's explicit scope and stop conditions.

## Core model: one request, multiple representations

Do not model a proxy request as one path. Maintain a representation ledger:

```text
client request line
  -> raw request URI seen by authentication exemptions and regex maps
  -> percent-decoded/canonical path
  -> normalized URI used for location selection and proxy routing
  -> service selector or target-runnable identity
  -> forwarded identity/host headers
  -> backend route and its local authorization assumptions
```

The protected invariant is:

> Every component making an authorization decision must bind that decision to
> the same canonical destination, service identity, and caller identity that
> the enforcement and backend layers ultimately use.

A successful request is not enough. Prove which representation each gate saw
and which backend handled the normalized request.

## Procedure

### 1. Reconstruct the real perimeter

For firmware or an appliance image, identify generated configuration as well as
shipped placeholders. Record:

- TLS listener and externally reachable locations;
- authentication subrequests and exemption logic;
- maps from path to application/service identity;
- normalization, rewrite, and `proxy_pass` behavior;
- headers stripped, overwritten, preserved, or synthesized;
- loopback services, ports, process users, and installed application set;
- setup-state, model, and version conditions affecting generated policy.

Do not infer runtime policy from a disabled or template nginx file when the
application generates the active configuration.

### 2. Build a gate-to-route matrix

For each external route family, capture:

| Field | Evidence |
|---|---|
| raw URI at auth gate | exact variable/function |
| auth decision | allow, deny, exempt, or target-specific |
| extracted target service | value and parser/regex |
| normalized routing URI | canonical result |
| selected backend | service and port |
| forwarded caller attributes | source and overwrite rules |
| backend-local checks | identity, role, trust-host, or loopback |

The key question is not whether the nominal exempted handler is safe. Ask what
other route the same raw string can become after later normalization.

### 3. Test representation equivalence with controlled differentials

Use a harmless endpoint and researcher-owned data. Compare:

1. direct protected route, expected denial;
2. ordinary public/exempt route, expected public behavior;
3. one path-changing input that preserves the raw exemption but changes the
   canonical destination;
4. canonicalized-at-entry or exact-route patched control.

Record both raw and normalized paths. A response-code change alone is weak;
bind the result to a backend-specific benign marker or log. Reject the
candidate if every layer resolves to the same protected target and policy.

### 4. Audit authentication gates before endpoint handlers

For literal allowlists, prefix exemptions, and regex exclusions, test whether
the rule is bound to an exact method and canonical route. Flag patterns where:

- a prefix is treated as an entire route family;
- percent-decoding or dot-segment removal happens after the decision;
- the route parameter grammar is not anchored;
- the auth layer authorizes a service name extracted differently from routing;
- an unmatched service identifier becomes an empty or default policy value.

An authenticated handler does not repair an exemption that routes elsewhere.
Conversely, an unsafe-looking exemption is not a finding if canonical routing
cannot escape the intended handler.

### 5. Model forwarded-header and local-peer trust separately

When the backend is loopback-only, distinguish:

```text
TCP peer identity
forwarded client address
forwarded host or original host
proxy-synthesized application identity
client-controlled headers that survive the proxy
```

Prove which field the backend actually uses. A local TCP peer plus an
attacker-influenced forwarded host can create a second gate failure, but only
if the production proxy preserves or reconstructs that value as observed.
Include a strict control in which the proxy overwrites the field from a trusted
constant or validated upstream identity.

### 6. Carry confirmed route-family roots forward

After a valid root appears in one service, enumerate the same semantic route
family across sibling applications and versions. Examples include backup,
export, import, restore, diagnostics, and support tooling. For each sibling,
re-prove:

- external reachability through the current proxy;
- role/permission middleware;
- parameter-to-sink trace;
- process identity and filesystem authority;
- whether the historical fix protected only one route or the shared root.

Similarity is a lead, not proof. Kill exact public roots and fixed builds.

### 7. Infer shell context from operator behavior, then confirm safely

When user input reaches a command builder, the behavior of syntax classes can
reveal quoting context. Record the constructed command from local source or
instrumentation rather than spraying payloads. A failure of command separators
alongside evaluation of substitution syntax may indicate interpolation inside
double quotes.

Use a benign local canary that records a nonce and process identity. Require:

- safe input baseline;
- one syntax-changing input;
- command-construction trace;
- canary read-back;
- patched control using argument arrays or strict path validation;
- cleanup of the canary.

HTTP 500, reflected text, or a changed filename is not command execution.

### 8. Treat service execution and root as separate findings states

After proving code execution, enumerate only locally available privilege
transitions supported by package manifests and policy files:

```text
request authority
  -> service process identity
  -> permitted sudo command or helper
  -> helper argument handling
  -> root-side harmless canary
```

Review exact sudoers command matching and every permitted wrapper. A wrapper
that delegates arbitrary arguments may erase the apparent restriction, but
root impact is proven only by an independent root-identity oracle. Do not add
persistence, rewrite credentials, or alter real device controls for proof.

### 9. Verify sanitizer semantics instead of trusting its name

For SQL helpers and formatters, record whether untrusted values are supplied as
data or embedded into an already assembled query. A formatter called without
value or identifier specifiers may return its input unchanged; manually adding
quotes before calling it does not create parameterization.

Use a local database fixture and three independent oracles when warranted:

- boolean differential;
- error behavior tied to a harmless constant;
- bounded timing differential.

Then determine whether the caller's role is intended to perform the observed
read or write. Do not extract production SIP credentials, messages, calls, or
other user data as routine validation.

### 10. Prove the chain edge by edge

Keep separate ledgers for:

```text
AUTH_EXEMPTION
NORMALIZED_ROUTE_CHANGE
BACKEND_REACHABILITY
BACKEND_LOCAL_TRUST_BYPASS
SERVICE_COMMAND_EXECUTION
ROOT_PRIVILEGE_TRANSITION
DATABASE_READ_OR_WRITE
SESSION_OR_IDENTITY_AUTHORITY
```

Severity is the highest program-eligible state actually demonstrated. Do not
infer owner-session minting from root, root from service execution, or WAN
reachability from LAN proof. Each transition needs current-release evidence
and a harmless oracle.

## Evidence matrix

```text
CURRENT_ARTIFACT_AND_MODEL          = PASS / FAIL
ACTIVE_GENERATED_PROXY_CONFIG      = PASS / FAIL
RAW_URI_CAPTURED                   = PASS / FAIL
NORMALIZED_URI_CAPTURED            = PASS / FAIL
AUTH_ROUTE_DESTINATION_MISMATCH    = PASS / FAIL
DIRECT_PROTECTED_BASELINE          = PASS / FAIL
BACKEND_SPECIFIC_READBACK          = PASS / FAIL
FORWARDED_TRUST_BOUNDARY           = PASS / FAIL / NOT_APPLICABLE
SERVICE_EXECUTION_CANARY           = PASS / FAIL / NOT_APPLICABLE
ROOT_TRANSITION_CANARY             = PASS / FAIL / NOT_APPLICABLE
DATABASE_CAPABILITY_DELTA          = PASS / FAIL / NOT_APPLICABLE
PATCHED_CANONICALIZATION_CONTROL   = PASS / FAIL
PUBLIC_EXACT_ROOT_PRIOR_ART        = FOUND / NOT_FOUND
PROGRAM_IMPACT_GATE                = PASS / BLOCKED / KILL
REPORT_READY                       = YES / NO
```

## Falsifiers and kill conditions

- Authentication and routing consume the same canonical path and service ID.
- The exemption is an exact method-and-route match after normalization.
- Client-supplied identity and host headers are unconditionally overwritten
  with trusted values before the backend.
- The backend independently authenticates the final destination and caller.
- The apparent command sink uses an argument vector without a shell, or the
  input is constrained to a safe canonical directory.
- The service account has no proven privilege transition beyond its intended
  authority.
- The SQL layer uses true parameter binding at the final database call.
- The behavior exists only in a fixed, archived, unsupported, or out-of-scope
  build.
- The exact root is already covered by the public CVEs, vendor advisories, or a
  known incomplete-fix remediation.
- The claimed external, root, owner-session, or cross-product impact lacks a
  separately demonstrated bridge.

## Sources

- Abdulaziz Alruwaybikh, "Pre-Auth RCE in UniFi OS - CVE-2026-34909: One
  Request to Root Behind Seven Products ($42,751)," July 30, 2026:
  https://www.catchify.sa/post/pre-auth-rce-unifi-os-one-request-to-root
- Public identifiers: CVE-2026-34909, CVE-2026-50747, CVE-2026-50748.
