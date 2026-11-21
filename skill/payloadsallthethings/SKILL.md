---
name: payloadsallthethings
description: "Use swisskyrepo/PayloadsAllTheThings methodology on the current in-scope bounty target: map the class folder, steal the exploit method, and land a B-specific payload. Use automatically during bug bounty for SQLi, XSS, SSTI, SSRF, LFI, upload, WAF bypass, and related classes. Ordinary coding does not enter this skill."
---

# PayloadsAllTheThings methodology

Authorized offensive-first. The local clone is program-neutral
methodology. The authorized host under test is program B. Read the
class chapter, rebuild the method for B, and prove a protected effect.

Index: `https://github.com/swisskyrepo/PayloadsAllTheThings` pinned in
`PINNED.json`. Web display: `https://swisskyrepo.github.io/PayloadsAllTheThings/`.
Read local files only. Do not clone again. Do not fire the whole
Intruder directory.

```bash
python3 /home/kali/.codex/skills/payloadsallthethings/scripts/query-patt.py \
  --skill HUNT_SKILL --format markdown
```

## Attack loop

1. After `target-system-model` names a reachable class, query the
   matching PATT folder. Open `README.md` methodology headings first
   (entry detection, DBMS/engine ID, WAF bypass), not the Intruder
   dump.
2. Steal the invariant: how to detect the entry, how to identify the
   backend, which payload family fits that backend.
3. Forge a B-specific payload with `payload-forge`. Unique canary.
   Rebuild for B's parameter, content-type, and WAF oracle.
4. Test on the named in-scope host through the matching `hunt-*`
   skill. One family at a time.
5. Hit: `hunt-severity-climb`. Miss: next PATT family, then
   `adaptive-plan-check-loop`.
6. Spawn `agents/patt-method-tester.md` for one folder at a time.

Skip Internal/AD/Windows persistence, Mimikatz, reverse-shell
cheatsheets, and CVE exploit folders unless the official scope is
that platform and the program allows that proof. Prefer the web
class directories.

## Mapping

`scripts/query-patt.py` maps `hunt-*` names onto folders such as
`SQL Injection`, `XSS Injection`, `Server Side Template Injection`,
`Command Injection`, `Directory Traversal`, `File Inclusion`,
`Server Side Request Forgery`, `XXE Injection`, `Upload Insecure Files`,
`Cross-Site Request Forgery`, `JSON Web Token`, `GraphQL Injection`,
`NoSQL Injection`, `OAuth Misconfiguration`, `SAML Injection`,
`Request Smuggling`, `Insecure Direct Object References`,
`Account Takeover`, `Encoding Transformations`.

## Limits

Stay on the named in-scope host. Harmless owned-account proof only.
A copied PATT string is not a finding. The clone does not authorize
a target. Do not DoS with time-based floods. `sqlmap` only after a
confirmed injectable parameter, inside program rate limits.
