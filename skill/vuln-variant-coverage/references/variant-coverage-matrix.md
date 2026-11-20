# Reachability-driven vulnerability variant matrix

Open only the families supported by the target model. These are hypothesis
families, not payload lists and not a requirement to force every class.

| Family | Representative variants to distinguish | Specialist |
|---|---|---|
| SQL injection | error, union, boolean blind, time blind, stacked query, out-of-band, second-order, ORM/query-builder context | `hunt-sqli` |
| XSS | reflected, stored, DOM, blind, mutation/DOM rewrite, client-template, server-template-to-browser, cross-context encoding | `hunt-xss`, `hunt-dom` |
| CSRF | form/simple-request, state-changing GET, JSON or multipart confusion, login CSRF, token binding failure, SameSite/top-navigation, method override, GraphQL mutation | `hunt-csrf` |
| IDOR/access control | horizontal, vertical, cross-tenant, nested object, batch/export, property-level, indirect reference, signed-ID replay, object lifecycle transition | `hunt-idor`, `hunt-auth-bypass` |
| File inclusion/read | local/remote inclusion, wrapper/scheme confusion, traversal-to-include, language loader/include path, second-order stored path | `hunt-lfi` |
| RCE | command argument/shell injection, expression/template execution, unsafe deserialization, dynamic loader/plugin, upload-to-execution, build/CI execution | `hunt-rce`, `hunt-ssti`, `hunt-deserialization`, `hunt-cicd` |
| SSRF | direct, blind, redirect-following, URL parser differential, DNS rebinding, alternate protocol, cloud metadata, webhook/import/preview/PDF consumer | `hunt-ssrf` |
| Arbitrary upload | extension/MIME/content mismatch, polyglot, path control, archive extraction, overwrite, public ACL, stored active content, downstream parser, upload-to-execution | `hunt-file-upload` |
| XML/parser | in-band/blind XXE, external parameter entity, XInclude, stylesheet/import consumer, parser feature mismatch | `hunt-xxe` |
| HTTP/cache | request smuggling/parser differential, cache key confusion, poisoning/deception, host-header trust | `hunt-http-smuggling`, `hunt-cache-poison`, `hunt-host-header` |
| Identity/session | password reset, MFA, OAuth/OIDC, SAML, JWT, session fixation/rotation/revocation, account takeover | `hunt-forgot-password`, `hunt-mfa-bypass`, `hunt-oauth`, `hunt-saml`, `hunt-jwt-crypto`, `hunt-session`, `hunt-ato` |
| API/realtime | REST object/function authorization, GraphQL resolver/batching, gRPC metadata/method auth, WebSocket handshake/message auth, shadow API | `hunt-api-misconfig`, `hunt-graphql`, `hunt-grpc`, `hunt-websocket`, `hunt-shadow-api` |
| State/business logic | race/TOCTOU, duplicate action, workflow/order bypass, quota/payment/entitlement invariant, exceptional-condition fail-open | `hunt-race-condition`, `hunt-business-logic`, `hunt-exceptional-conditions` |
| Browser boundary | CORS, open redirect with protected bridge, clickjacking on protected action, HTML injection, CSP/DOM gadget composition | `hunt-cors`, `hunt-open-redirect`, `hunt-clickjacking`, `hunt-html-injection`, `hunt-dom` |
| Platform/configuration | cloud/Kubernetes/API misconfiguration, source leak, subdomain lifecycle, TLS/network boundary, framework-specific reachable consumers | `hunt-cloud-misconfig`, `hunt-k8s`, `hunt-source-leak`, `hunt-subdomain`, `hunt-tls-network`, matching stack skill |

Map each family back to OWASP Top 10 categories for coverage reporting, but
test the concrete variant and protected consumer rather than the category
label. Record skipped families with the system-model evidence showing why they
are unreachable.

## OWASP Top 10 coverage ledger

| OWASP category | Evidence-supported routes |
|---|---|
| A01 Broken Access Control | IDOR, auth bypass, tenant/object/function/property authorization, CORS or host trust only when it bridges a protected action |
| A02 Cryptographic Failures | JWT/signature/key handling, sensitive-data exposure, transport boundary, token or secret lifecycle |
| A03 Injection | SQL/NoSQL/LDAP/command/template/HTML/DOM/XML and downstream interpreter consumers |
| A04 Insecure Design | business-logic, workflow, entitlement, payment/quota, state-machine, and race invariants |
| A05 Security Misconfiguration | API/cloud/Kubernetes/framework configuration, exposed administrative surface, source leak, unsafe defaults |
| A06 Vulnerable and Outdated Components | current fingerprint plus CVE/advisory reachability on the in-scope release; a version or banner match alone is killed |
| A07 Identification and Authentication Failures | password reset, MFA, OAuth/OIDC/SAML, sessions, account takeover, credential lifecycle |
| A08 Software and Data Integrity Failures | CI/CD and supply-chain trust, unsafe update/import, deserialization, signature or provenance failure |
| A09 Security Logging and Monitoring Failures | retain only when a reachable failure creates a program-recognized protected effect; missing logs alone are informative |
| A10 Server-Side Request Forgery | direct/blind SSRF and every evidenced server-side URL consumer variant |

For A06, check official advisories, dependency manifests, GitHub issues and
PRs, commit/release history, and the deployed or shipped version. Then prove
the affected code path and protected effect on the current in-scope build.
