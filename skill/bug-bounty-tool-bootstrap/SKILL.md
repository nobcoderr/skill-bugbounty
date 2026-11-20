---
name: bug-bounty-tool-bootstrap
description: "Plan and install a fixed allowlist of missing user-local tools for an already named and authorized bug-bounty program. Use only after the exact scope and analysis action are recorded; never accept arbitrary packages, launch scans, or treat installation as target authorization."
---

# Bug bounty tool bootstrap

Use this broker after `mandatory-auto-router` and `valid-bug-hunt` identify a
specific evidence-supported analysis lane. The official program name, a
non-empty scope file, and the intended action must already exist. Installation
permission does not authorize traffic or widen scope.

## Interface

Preview without changing the system:

```bash
bb-tools --plan web
```

Install only missing allowlisted tools:

```bash
bb-tools --apply web --program PROGRAM --scope-file SCOPE_FILE --action "ACTION"
```

Profiles are exactly `web`, `source`, `web3`, `supply-chain`, and `ci`.
`--apply` fails closed when the program, scope file, or action is missing. The
broker installs with `pipx` into the current user's isolated environment,
records the pinned package and result in
`~/.local/state/bb-tools/install-log.jsonl`, and never executes the installed
security tool.

The scope file is JSON, not arbitrary prose. It must contain the same
`program` value passed on the command line, an HTTPS `source_url`,
`source_kind` set to `official_program` or `official_repository`, a timezone-
aware ISO-8601 `captured_at` no older than seven days, `policy_file` plus its
matching `policy_sha256`, and a non-empty `assets` array. Every asset is an
object with `status: "in_scope"`. This binds the install decision to a current
local policy snapshot; it does not widen that policy. Use
`references/scope-schema.md` for the exact shape.

## Fixed catalog

- `web`: `arjun==2.2.7`, `uro==1.0.2`
- `source`: `semgrep==1.185.0`
- `web3`: `slither-analyzer==0.11.6`, `solc-select==1.2.0`
- `supply-chain`: `checkov==3.4.5`
- `ci`: `zizmor==1.32.0`

Do not translate arbitrary user text into a package name or shell command. Do
not use `latest`, force-upgrade an existing binary, alter the system proxy,
update scanner templates, or download an executable from an unverified release
URL. Prefer a user-local install. When the package has no user-local build and
apt asks for sudo, follow `local-sudo-install`. Do not use sudo for any other
change. A tool already on `PATH` is recorded as present and
left untouched. It counts as verified only when `pipx` identifies the expected
package at the exact pinned version; a name collision, unknown provenance, or
version mismatch fails closed. The broker downloads the pinned main package
from the explicit PyPI HTTPS index, matches its SHA-256 to PyPI release
metadata, installs that verified local artifact, and records both artifact and
resolved-executable SHA-256 values. Dependencies remain governed by the same
explicit index and TLS; this is not a full dependency lockfile.

Large, runtime-coupled, or target-specific suites such as CodeQL, Foundry,
Echidna, Mythril, Trivy, OSV-Scanner, Syft, Grype, mobile instrumentation, and
cloud CLIs require a concrete target lane and a separate provenance/version
decision. Do not silently substitute them into this catalog.

If a product needs a paid license, account, API credit, test funds, or wallet
balance, stop and tell the user. Never spend money. See
`references/tool-policy.md` for the installation boundary.
