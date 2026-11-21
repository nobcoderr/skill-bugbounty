---
name: payload-forge
description: "Create and mutate in-scope attack payloads for WAF/filter bypass, SQL injection, XSS, SSTI, command injection, LFI, SSRF, and related classes. Use automatically during bug bounty when a probe is blocked, encoded, or needs a new payload. Ordinary coding does not enter this skill."
---

# Payload forge

Authorized offensive-first. Build a payload for the current in-scope
entry, then mutate it when a filter or WAF kills the first shot. Do
not spray wordlists. Do not fire another program's payload bytes.

`control-bypass-variation-engine` owns HTTP verb/location/origin
swaps. This skill owns **payload syntax**: encoding, comments, keyword
split, alternative operators, context wrapping, and polyglots.

Use `payloadsallthethings` to pull methodology and seed families from
the local swisskyrepo clone. Then forge a B-specific payload here.

## When to fire

- A `hunt-*` class needs an injectable string (SQL, XSS, SSTI, RCE,
  LFI, SSRF, XXE, upload, JWT, GraphQL).
- The baseline payload is blocked, stripped, encoded, or reflected
  differently than sent.
- The user asks for bypass, payload, WAF, SQLi, or mutation.

## Forge loop

1. Freeze context: parameter location (query, body, JSON, header,
   cookie, path, filename), content-type, DB/framework fingerprint,
   exact reject oracle (WAF HTML, 403, encoded reflection, SQL error).
2. Write one **baseline canary** for the class. Unique marker. Harmless.
3. If it hits the sink, stop forging and hand to the class skill plus
   `hunt-severity-climb`.
4. If it is blocked, emit at most **8** mutations. Each mutation must
   change a named filter/parser dimension. Cosmetic case-only churn
   of the same string is `MUTATION_ONLY` unless case is the control.
5. Test one mutation at a time on the named in-scope host. Keep the
   rest of the request identical.
6. Miss: next mutation, then `payloadsallthethings` for a new family,
   then `adaptive-plan-check-loop`.

Spawn `agents/payload-mutator.md` for one blocked baseline.

## Mutation dimensions

Pick from evidence, not from a dump:

| Axis | When the oracle shows | Example move |
|---|---|---|
| Encoding | WAF matches raw keyword | URL, double-URL, unicode, HTML entity, hex |
| Comments / space | keyword or space blocked | `/**/`, `%0a`, `%09`, no-space concat |
| Operator swap | `OR`/`AND`/`=` blocked | `\|\|`, `&&`, `LIKE`, `BETWEEN`, `<>` |
| Keyword split | `SELECT`/`UNION`/`script` blocked | concat, case mix, nested comments |
| Function swap | `SLEEP`/`SUBSTRING` blocked | DBMS-native equivalent from PATT |
| Context wrap | query filtered, JSON/XML not | JSON string, multipart filename, header |
| Second-order | first request stored, later rendered | inject, then trigger the consumer |
| Polyglot | unknown parser | one string, several grammars |

Request-dimension bypass (GET vs POST, body vs query) goes to
`control-bypass-variation-engine`.

## Canary rules

- XSS: unique numeric canary, prove unescaped execution context.
- SQLi: boolean pair or error oracle first; dump only owned-test rows.
- SSTI: arithmetic canary, not a reverse shell.
- RCE: `id` only after the program allows command proof.
- SSRF: collaborator/canary host you own, not a third party.
- Stop at the first protected effect. No destructive payload.

## Output

```text
CLASS=
ENTRY=
BASELINE=
ORACLE=
MUTATION_ID=
AXIS=
PAYLOAD=
EXPECTED=
RESULT=
NEXT=
```

A payload is not a finding. `hunt-sqli` / `hunt-xss` / the matching
class still has to prove the sink. `hunt-terminal-verdict` still owns
the user-facing close.
