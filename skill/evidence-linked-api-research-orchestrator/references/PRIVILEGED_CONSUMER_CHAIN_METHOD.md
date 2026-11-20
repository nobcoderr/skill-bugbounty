# Privileged Consumer Chain Method

## Purpose

Evaluate API chains where an information disclosure, workflow primitive, or
identifier mismatch may unlock a higher-authority backend consumer. The method
separates representation knowledge from resource authority and execution
authority.

## 1. Capability-producing disclosures

Classify disclosures by what they newly enable:

- a descriptor can enable exact decoding or typed request construction;
- queue/runtime metadata can reveal a required namespace or workflow selector;
- task catalogs can reveal a privileged consumer class;
- error details can reveal a parameter, handler, or policy boundary;
- a list/filter surface can make an otherwise unguessable child identifier
  obtainable.

Record a capability only when the artifact is usable in the same authorized
environment. If the post-state adds no reachable surface, use
`KILL_NO_CAPABILITY_DELTA`.

## 2. Representation ledger

For every value or response, record:

```text
WIRE_REPRESENTATION=
DECLARED_CONTENT_TYPE=
ACTUAL_ENCODING=
SCHEMA_SOURCE_AND_HASH=
DECODER=
DECODED_OBJECT=
CANONICAL_RESOURCE_IDENTITY=
CONSUMER=
```

Alternative representations may expose data hidden by a failed JSON mapping,
but a transport-format difference is not an authorization bypass by itself.
Use only documented or explicitly permitted negotiation in owned fixtures.

## 3. Semantic counterpart inventory

Security fixes often attach to one route, service name, or frontend while a
semantically equivalent handler remains reachable elsewhere. Inventory
counterparts from target-native evidence:

- service and method descriptors;
- frontend or SDK call sites;
- shared request/response types;
- identical backend error identities;
- patch or deployment metadata.

Require handler/security-policy equivalence before calling two routes variants.
A similar name is only a hypothesis. Public fixed counterparts are prior art,
not live targets.

## 4. Deployment consistency

When otherwise identical probes produce alternating authorization decisions,
freeze all client-controlled inputs and record timestamps, connection/backend
metadata available to the researcher, and operation IDs. Distinguish cache,
eventual state, account propagation, and heterogeneous deployment.

Do not retry until success. Bounded cohort sampling must be explicitly allowed,
rate-limited, and stopped once inconsistency is demonstrated. Reconfirm against
the patched control rather than relying on a transient success.

## 5. Parent-child authorization binding

For hierarchical resources, keep separate:

- parent named in the request path;
- child identifier used by lookup;
- canonical parent stored with the child;
- parent against which authorization is evaluated;
- parent reflected in the response.

The invariant is:

`AUTHORIZED_PARENT == CANONICAL_PARENT(CONSUMED_CHILD)`

A response constructed with the caller's parent can conceal a cross-parent
lookup. Prove canonical ownership through researcher-owned cross-account
fixtures and an authoritative read-back.

## 6. Identifier exploitability

High-entropy identifiers may make a real authorization flaw impractical from
the starting state. Record entropy, prior knowledge, lifetime, source, request
budget, and measured obtainability. A separate list, error, log, or ordered
predicate oracle can create the missing capability, but that edge must be
proved on owned identifiers under an approved request budget.

Do not provide or run enumeration against third-party namespaces. If the
identifier remains unobtainable, use
`KILL_HIGH_ENTROPY_IDENTIFIER_NOT_RECOVERABLE` for the claimed cross-tenant
path while preserving the underlying authorization defect separately if the
program recognizes it.

## 7. Workflow and approval state

Model draft, ACL update, request-for-approval, publish, execute, test, and log
download as separate state transitions. Record which principal performs each
action. If two researcher-owned accounts are required, define the attacker's
starting authority as an authorized principal set and prove that the first
primitive legitimately enables the second principal's action.

Never collapse an approval workflow into “same attacker” without principal-set
and ACL evidence.

## 8. Alternate execution consumers

Normal execution, test-case execution, asynchronous execution, preview, and
debug paths may use different workers or policies. An internal task accepted at
save time may be rejected or time out in one path while reaching a deeper
consumer in another. Record each as a distinct consumer and compare only
otherwise-identical owned workflows.

Exceptions, disk errors, or policy traces establish reachability. They do not
prove arbitrary code execution, successful RPC, or protected data access.

## 9. Service identity and method policy

For a privileged RPC-style task, separate:

- caller/end-user identity;
- frontend service identity;
- workflow execution identity;
- target service and method;
- credential-forwarding mode;
- per-method authentication/authorization policy;
- protected operation actually performed.

An “arbitrary RPC” shape expands attack surface but does not mean every method
is callable. Prove only the minimum harmless method authorized by scope. If the
provider confirms the production-compromise boundary and requests a stop,
record confirmation and stop; do not seek additional reach.

Use `KILL_SERVICE_IDENTITY_AUTHORITY_INFERRED` when identity or policy is only
guessed, and `KILL_PRIVILEGED_CONSUMER_NOT_PROVEN` when configuration never
reaches an authority-bearing consumer.

## 10. Valid chain contract

A chain edge requires:

```text
OUTPUT_CAPABILITY(previous) satisfies REQUIRED_CAPABILITY(next)
IDENTITY_OR_PRINCIPAL_SET_CONTINUITY=PROVEN
ENVIRONMENT_CONTINUITY=PROVEN
PRIVILEGE_CONTINUITY=PROVEN
STATE_CONTINUITY=PROVEN
REPRESENTATION_CONTINUITY=PROVEN
DEPLOYMENT_CONTINUITY=PROVEN
```

Promote terminal impact only after a protected action or provider-authoritative
confirmation. Public bounty severity is historical context and must not be
borrowed by a new candidate.
