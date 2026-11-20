# Control-bypass variation families

Use with `control-bypass-variation-engine`. Each family is an **axis catalog**, not a payload pack. Pick axes that change which component keys the control. Encoding-only rows are last and usually `MUTATION_ONLY`.

Browser-reachable means a real cross-site or low-privilege browser can send it (HTML form, simple `Content-Type`, image/iframe GET). Raw Repeater spoofing of `Origin` is a header-check probe, not browser CSRF/CORS proof.

## Cross-cutting axes

Apply these before specializing:

1. **Method** — POST, GET, PUT, PATCH, DELETE, HEAD, OPTIONS; `_method`; `X-HTTP-Method-Override`; query `?_method=`.
2. **Location** — JSON body, form body, multipart, query, path, header, cookie.
3. **Content-Type** — json, `x-www-form-urlencoded`, `text/plain`, multipart, xml, charset extras.
4. **Parser pair** — middleware vs controller, REST vs GraphQL, `/v1` vs `/v2`, mobile vs web.
5. **Identity material** — cookie, bearer, CSRF token, HMAC, Origin/Referer. Change **one**.
6. **Path shape** — trailing slash, `;`, extra extension, case, alias prefix. Only if routing/middleware split is plausible.

## Family A — CSRF / SameSite (verb + location)

**Control key:** state-changing POST/PUT with CSRF token, custom header, or non-simple Content-Type.  
**Sink key:** same handler also binds fields from query/path or accepts GET.  
**Canonical mismatch:** POST without token → CSRF 403; GET same route with former body fields in the query → action runs.

Axes:

- POST → GET/HEAD (SameSite=Lax allows top-level GET).
- Body → query or path params.
- JSON → urlencoded / `text/plain` / multipart (simple request, no preflight).
- Omit token vs empty token vs token from another page vs token in cookie only.
- Drop `X-CSRF-Token` / `X-Requested-With` while keeping cookies.
- GraphQL mutation over GET.
- Alternate route that skips CSRF middleware (`/internal`, RPC, batch, webhook that still uses the session cookie).

**Observable:** protected state change on a researcher account; CSRF error absent.  
**Negative control:** same GET without cookies, or with a non-victim object id.  
**Hunt skill:** `hunt-csrf`.

## Family B — CORS (read, not state-change)

Use when the goal is a **credentialed cross-origin read**. Do not spend the whole budget here.

Axes: reflected Origin, `null`, unanchored regex, unescaped dot, prefix-only match, preflight vs simple request, `ACAC` without matching `ACAO`, postMessage origin.  
**Observable:** attacker origin reads authed body in a real browser.  
**Hunt skill:** `hunt-cors`.

## Family C — Authn / session

**Control key:** 401/login middleware on one verb or path.  
**Sink key:** handler still runs on another verb, trailing-slash alias, or optional auth.

Axes: verb swap, path alias, missing `Authorization` vs bad token vs cookie-only, optional middleware on `/graphql`, unauth batch, verb tunneling.  
**Observable:** protected action or data without the login the control demanded.  
**Hunt skill:** `expert-authentication-authorization-hunter`.

## Family D — Authz / IDOR

**Control key:** object check on POST body `id`.  
**Sink key:** same object from query, path, JSON wrap, array, or GET.

Axes: id in another location, HTTP parameter pollution, wrap `{user:{id}}`, method change, create-vs-update, sign-off vs sign-on.  
**Observable:** researcher B affects researcher A's object.  
**Hunt skill:** `hunt-idor`.

## Family E — Edge 403 / WAF / path gate

**Control key:** reverse-proxy or WAF on exact path+method+UA.  
**Sink key:** origin app route still mounted under an alias.

Axes: trailing slash, `/.`, `;jsessionid`, `%2e`, extra `/./`, `X-Original-URL` / `X-Rewrite-URL` **only if that front-end is in evidence**, HTTP/2 vs 1.1, content-type the WAF skips.  
Do not spray header lists without a named proxy product.  
**Observable:** origin 200/action vs edge 403 HTML.  
**Negative control:** random path still 403.

## Family F — CSP / XSS sink

Axes: nonce reuse, JSONP, gadget in allowed origin, iframe `srcdoc`, `unsafe-hashes` sibling, bypass via redirect to allowed host.  
**Hunt skill:** `hunt-xss`.

## Family G — Open redirect

Axes: `//`, `\`, `@`, encoded slash, nested redirect, parser vs validator URL.  
**Hunt skill:** `hunt-open-redirect`.

## Family H — Clickjacking

Axes: missing/weak `frame-ancestors`, nested frames, sandbox, `X-Frame-Options` vs CSP conflict.  
**Hunt skill:** `hunt-clickjacking`.

## Family I — SSRF

Axes: parser pair (URL vs fetch), redirect, DNS rebinding **only if in scope**, scheme alias. No metadata-cloud payloads unless that cloud is the authorized asset.  
**Hunt skill:** `hunt-ssrf`.

## Family J — Rate limit / lockout

Axes: other verb, other path alias, `X-Forwarded-For` only if the app keys on it, other account-id field.  
**Observable:** extra allowed attempt after the control should have locked.

## Family K — Cache / CDN

Axes: unkeyed header, method, `Origin`, `X-Forwarded-Host`, path normalization vs cache key.  
**Hunt skill:** `hunt-cache-poison`.

## Ranking reminder

State-changing, browser-reachable, one-axis cards first. CORS read-oracles second. WAF/path header spray last. If two cards share the same invariant, keep one.
