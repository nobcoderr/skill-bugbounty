# Payload mutation axes

Use after a baseline is blocked. Cap eight cards. Pair with
`payloadsallthethings` for DBMS- or class-specific syntax.

## SQL injection

- Quote/comment: `'`, `"`, `` ` ``, `--`, `#`, `/**/`
- Boolean pair: true vs false with the same parameter
- Union only after column count is proven
- WAF: no-space, no-comma (`FROM 1 OFFSET`), no-equal (`LIKE`, `BETWEEN`)
- DBMS swap from fingerprint: `SLEEP` / `WAITFOR` / `pg_sleep`

## XSS / HTML

- Tag vs attribute vs JS-string vs URL vs SVG vs template
- Encoding: HTML entity, unicode, JS `\u`, mixed case tags
- Event handlers when `<script>` is stripped
- Unique numeric canary; encoded `&lt;` is not XSS

## Command / SSTI / LFI / SSRF

- Command: `;` `&&` `|` `` ` `` `$()` newline; prove with `id` only
- SSTI: `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`, then engine-specific
- LFI: `../`, wrappers, encoding, null, extra slashes
- SSRF: http, 302, decimal IP, IPv6, file/gopher only if in scope

## Auth / filter bypass strings

- Login SQLi is still SQLi: tautology after fingerprint
- JSON type juggling / mass assignment: change type, not only string
- JWT: alg/none and kid tricks belong to `hunt-jwt-crypto`
