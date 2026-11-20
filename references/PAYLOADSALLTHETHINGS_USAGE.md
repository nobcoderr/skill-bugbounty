# PayloadsAllTheThings — Controlled Usage Guide

Repository:

- `https://github.com/swisskyrepo/PayloadsAllTheThings`
- Local default path after installer: `~/tools/PayloadsAllTheThings`

The upstream project is a broad web-application-security payload and bypass reference. Its sections commonly include vulnerability explanations, example payloads, Burp Intruder lists, images, and supporting files.

## Correct use in this skill pack

1. Start with a confirmed in-scope workflow and a specific hypothesis.
2. Identify the exact parser, sink, authorization boundary, or state transition being tested.
3. Open only the relevant chapter.
4. Select the smallest harmless test case.
5. Replace destructive/external effects with a researcher-controlled canary.
6. Send a minimal number of requests at a program-compliant rate.
7. Verify server-side behavior and concrete impact with a control request.
8. Preserve evidence and clean up synthetic data.

## Do not

- spray entire payload lists against production;
- run DoS, resource-exhaustion, data-destruction, or credential attacks;
- test third-party integrations outside scope;
- treat WAF/error differences as proof of vulnerability;
- copy a payload without understanding its encoding and parser context;
- publish target-specific secrets, tokens, private data, or exploit chains;
- retain a payload-reflection candidate without an impact-bearing execution or trust-boundary break.

## Suggested mapping

| Hypothesis | Reference family | Minimum evidence |
|---|---|---|
| authorization bypass | IDOR/BAC/API sections | cross-account unauthorized server-side read/write with control |
| SSRF | SSRF section | controlled callback or protected-boundary access allowed by rules |
| path traversal | Directory Traversal section | unauthorized file/object read/write, not an error string |
| XSS | XSS/CSP sections | execution in a meaningful victim/privileged context |
| template injection | SSTI sections | harmless server-side evaluation plus concrete impact path |
| deserialization | Insecure Deserialization sections | reachable unsafe type/gadget behavior in an approved environment |
| parser differential | request smuggling/upload/URL sections | demonstrable frontend/backend or validator/sink disagreement |
| OAuth/session | OAuth/JWT sections | account/session/authorization impact, not cosmetic deviation |

## Version evidence

Record before use:

```bash
cd "$HOME/tools/PayloadsAllTheThings"
git rev-parse HEAD
git status --short
```

The upstream repository uses the MIT License. Preserve attribution when redistributing substantial upstream content. This pack links/clones the repository and does not vendor its payload collection.
