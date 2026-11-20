# Expert Safe Test Design Matrix

| Dimension | Baseline | Candidate test | Negative control | Evidence | Abort condition | Cleanup |
|---|---|---|---|---|---|---|
| Identity/role | | | | | | |
| Tenant/object | | | | | | |
| State transition | | | | | | |
| Parser/canonicalization | | | | | | |
| Cache/replay/timing | | | | | | |
| Signature/integrity | | | | | | |
| Release/deployment | | | | | | |
| Privilege/sandbox | | | | | | |
| Credential/capability | | | | | | |
| Auth control absent/nil/default/error | | | | | | |
| Authorized resource vs consumed resource | | | | | | |
| Checked value/node vs consumed value/node | | | | | | |
| Arithmetic/library error domain | | | | | | |
| Validator vs downstream protocol capability | | | | | | |
| Critical lifecycle error propagation | | | | | | |
| Dynamic object method/coercion surface | | | | | | |
| Protocol length versus exact transmitted bytes | | | | | | |
| Import attribute provenance to persisted/queued state | | | | | | |
| Fixed argv/data versus shell-bearing command string | | | | | | |
| Optional dependency and interpreter activation | | | | | | |
| Intermediate primitive versus terminal execution edge | | | | | | |
| Archive member type and extracted object identity | | | | | | |
| Canonical root/origin/namespace at final consumer | | | | | | |
| Browser normalization, CSRF, and method override | | | | | | |
| Upload metadata to markup and secondary loader | | | | | | |
| Inline option to class/constructor/loader capability | | | | | | |
| Request parameter to framework-reserved option | | | | | | |
| Regex/path capture versus final canonical object | | | | | | |
| Argv operand versus child option grammar | | | | | | |
| Option termination and per-subcommand behavior | | | | | | |
| Working directory and mode-expanded object namespace | | | | | | |
| Static sanitizer output versus shipped JavaScript gadget | | | | | | |
| Base file/DOM primitive versus capability and terminal bridge | | | | | | |

## Rules

- Use researcher-owned accounts, data, infrastructure, packages, contracts, and devices.
- Change one variable at a time whenever possible.
- Preserve exact timestamps, IDs, versions, headers, state, and raw artifacts.
- Define success and failure before testing.
- Stop on third-party impact, unexpected data exposure, instability, or scope drift.
- Do not escalate beyond the minimum benign primitive needed to prove the boundary.

## Codex CLI verification fields

Before any candidate test, record explicit attacker condition, server condition, security impact, independent verifier results, and manual status. For authorization tests, record subject, action, target resource, tenant/org, object state, policy arguments, and authoritative final state. Agent agreement cannot replace baseline, positive evidence, or negative control.

For auth candidates, include explicit-no-op and implicit-missing-control states
separately. A decision value is insufficient: record whether the protected
handler or authoritative sink ran.

For decode/reparse, generated-document, secondary-config-grammar, multipart
provenance, and import virtual-setter candidates, include the ordered parser and
decode ledger, exact representation validated and consumed, output/config
grammar, trusted signed carrier, ambient collision control, generated-setter
inventory, scalar-versus-nested assignment order, and a fake authority
consumer. Treat a later-assigned header/config setter that cannot affect the
first request as a required negative control, not as evidence for a broader
claim.

For path/CLI/gadget-chain candidates, include the exact admitted, normalized,
validated, and consumed value; final object/token/DOM identity; root or option
terminator; every subcommand, scope, renderer, and gadget; explicit working
directory/platform/release evidence; and separate controls for the base
file/DOM effect and each secret, signing, serializer/gadget, or terminal-impact
bridge. Use synthetic roots, fake argv consumers, and inert DOM fixtures only.
