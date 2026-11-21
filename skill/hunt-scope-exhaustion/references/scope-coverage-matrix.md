# Per-asset coverage matrix

Fill one table per official in-scope asset. Skip a class only with
system-model evidence that this asset has no consumer for it
(`UNREACHABLE`). A miss is `KILLED` or `EXHAUSTED`, not a skip.

Stack routers (`hunt-nodejs`, `hunt-laravel`, `hunt-nextjs`,
`hunt-aspnet`, `hunt-springboot`, `hunt-sharepoint`,
`hunt-fintech-graphql`, `hunt-dispatch`) are not classes. They only
point at a class skill.

## Features

List every reachable feature on the current asset before testing:

| Feature | Entry | Actor | Protected object | Classes that can consume it |
|---|---|---|---|---|

## Classes

Run each reachable class against every matching feature:

| Family | Specialist | State | Evidence |
|---|---|---|---|
| Access control / IDOR | `hunt-idor`, `hunt-auth-bypass` | | |
| XSS / DOM | `hunt-xss`, `hunt-dom` | | |
| CSRF | `hunt-csrf` | | |
| SQLi / NoSQLi / LDAP | `hunt-sqli`, `hunt-nosqli`, `hunt-ldap` | | |
| File include / path | `hunt-lfi` | | |
| RCE / SSTI / deser / CI | `hunt-rce`, `hunt-ssti`, `hunt-deserialization`, `hunt-cicd` | | |
| SSRF | `hunt-ssrf` | | |
| Upload | `hunt-file-upload` | | |
| XXE | `hunt-xxe` | | |
| HTTP / cache / host | `hunt-http-smuggling`, `hunt-cache-poison`, `hunt-host-header` | | |
| Identity | `hunt-forgot-password`, `hunt-mfa-bypass`, `hunt-oauth`, `hunt-saml`, `hunt-jwt-crypto`, `hunt-session`, `hunt-ato` | | |
| API / realtime | `hunt-api-misconfig`, `hunt-graphql`, `hunt-grpc`, `hunt-websocket`, `hunt-shadow-api`, `hunt-spa-api` | | |
| Logic / race | `hunt-business-logic`, `hunt-logic-vulnerability`, `hunt-race-condition`, `hunt-exceptional-conditions`, `hunt-reentrancy` | | |
| Browser boundary | `hunt-cors`, `hunt-open-redirect`, `hunt-clickjacking`, `hunt-html-injection` | | |
| Config / leak | `hunt-cloud-misconfig`, `hunt-k8s`, `hunt-source-leak`, `hunt-subdomain`, `hunt-tls-network`, `hunt-api-misconfig` | | |
| Other reachable | `hunt-captcha-bypass`, `hunt-brute-force`, `hunt-llm-ai`, `hunt-rag-vector`, `hunt-ntlm-info`, `hunt-misc` | | |

Writeup transfer on this same asset:

| Source | Skill | State |
|---|---|---|
| `github.com/nobcoderr/writeup` | `nobcoder-writeup-transfer` | |
| reddelexc / codebygk | `corpus-writeup-transfer` | |

Asset terminal state: `UNMAPPED` / `ACTIVE` / `PROMISING` / `BLOCKED` / `EXHAUSTED` / `VALIDATED`.
Rotate only from `EXHAUSTED`, `BLOCKED` (whole asset unreachable), or
`VALIDATED` after remaining cells on this asset are also terminal.
