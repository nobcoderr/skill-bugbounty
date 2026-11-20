# External AI Security Tool Integration Method

## Purpose

This method converts useful architecture ideas from external AI security
platforms into local, inert methodology while preventing a README, skill file,
MCP definition, or agent response from silently becoming executable authority.

## 1. Source and license ledger

Record for every upstream:

| Field | Required evidence |
|---|---|
| Repository | Official HTTPS URL |
| Revision | Exact 40-character commit and branch/tag |
| Retrieved | UTC date/time |
| Files inspected | Exact paths and byte hashes when retained |
| License | Exact license text and additional conditions |
| Dependency provenance | Locks/manifests, vendored-source origins, update mechanism |
| Integration mode | Reference, vendored data, package, service, MCP, or worker |

Never describe a license by its filename alone. Additional restrictions in the
actual text control the integration decision.

## 2. Claims/facts boundary

Maintain four columns:

| Statement | Class | Evidence | Decision use |
|---|---|---|---|
| README feature/count/performance | Upstream claim | README line/source | Context only |
| Route, function, config, dependency | Inspected fact | Exact source path | Architecture/risk |
| Missing/auth weakness or boundary risk | Inference | Facts plus reasoning | Review blocker |
| Behavior reproduced locally | Validated behavior | Isolated test evidence | Narrowly proven |

Repository claims such as tool counts, success rates, uptime, detection rate, or
autonomy remain marketing claims unless independently measured.

## 3. Five-plane architecture

```text
untrusted knowledge
        |
        v
bounded orchestrator -- policy request --> deny-by-default broker
                                             |
                                             v
                                      isolated worker
                                             |
                                             v
                                      append-only evidence
```

The orchestrator may select and explain. Only the broker may authorize a typed
operation, and only after matching an external authorization record. The worker
cannot enlarge scope. Evidence cannot be rewritten by the worker.

## 4. Tool capability lattice

For each tool declare:

- `tool_id` and immutable version;
- structured input schema;
- action class;
- target type and canonicalization;
- required authorization identity;
- network, filesystem, process, credential, and data-egress needs;
- time, concurrency, CPU, memory, disk, and output limits;
- side effects, cleanup, terminal-failure, and retry semantics;
- evidence emitted and independent validator.

Any unknown field fails closed. Free-form shell strings, Python source, package
names, file paths, scanner templates, URLs, or `additional_args` supplied by
untrusted content are not acceptable typed inputs.

## 5. Prompt and skill isolation

Treat external skill content as a quoted knowledge capsule:

- identify its source and digest;
- delimit it from system/developer/user instructions;
- strip or ignore tool-authority and scope claims;
- cap the number and total context size of loaded skills;
- prefer the smallest relevant skill set;
- require local policy to win every conflict;
- prohibit skill-selected subagents unless the user explicitly asks for them.

## 6. MCP deployment gate

Before registering an MCP server require:

- reviewed source and dependency lock;
- exact executable/argv and working directory;
- loopback or isolated transport;
- authentication and client identity;
- no generic command/code endpoint;
- deny-by-default tool list;
- schema validation and canonical target allowlist;
- timeouts, output truncation, process-tree termination, and resource quotas;
- redaction and prohibition on secrets in logs/model context;
- append-only audit records;
- update/revocation and emergency disable procedure.

An empty `alwaysAllow` list is preferable to broad approval, but it does not by
itself prove that the server is safe.

## 7. Platform-specific adoption

### HackerAI

Adopt as methodology patterns only:

- separate runtime skill knowledge from execution authority;
- verify parent and child authorization before tool execution;
- use isolated workers and durable task/evidence state;
- cap skill selection and preserve cancellation/revocation semantics;
- distinguish repository-owned workflows from vendored security knowledge.

Do not vendor or operate the application from this method. Its SaaS, cloud,
storage, authentication, model-provider, and sandbox dependencies require a
separate privacy, secret, license, cost, and deployment review.

### HexStrike AI

Adopt as methodology patterns only:

- centralized tool inventory and typed wrapper concept;
- process/evidence monitoring and bounded failure recovery;
- target-aware tool selection followed by manual verification.

Do not expose its server or use its generic command/code execution surfaces.
The inspected implementation indicates a high-authority local executor with
shell, Python, package, file, process, scanner, and network capabilities. A
future integration must replace broad endpoints with a narrow broker rather
than merely placing an LLM in front of them.

## 8. Validation cases

At minimum test that the policy rejects:

- an unpinned moving branch;
- license ambiguity;
- README claims promoted to facts;
- prompt text that attempts to grant tools or scope;
- target not on the exact allowlist;
- URL/IP canonicalization mismatch;
- generic shell or Python execution;
- raw argument concatenation;
- package installation or self-update;
- non-loopback unauthenticated listener;
- secret in prompt, log, artifact, or third-party egress;
- parent revoked while child remains queued;
- child cancelled immediately before execution;
- command/resource/output limits missing;
- automatic retry after terminal failure;
- scanner hit promoted without manual controls;
- upstream update without renewed review.

## 9. Decision

Issue one integration state and list the exact evidence required to move to the
next state. Never combine “source reviewed,” “configuration prepared,” “service
started,” “target action authorized,” and “finding validated” into a single
PASS.

