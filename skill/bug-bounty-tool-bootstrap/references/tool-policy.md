# Tool installation policy

The broker is a local capability installer, not an offensive executor.

- Require an official named program, a current JSON scope snapshot whose
  `program` matches, whose policy-file digest verifies, and whose assets are
  explicitly `in_scope`, plus a concrete analysis action before applying a
  profile.
- Accept only fixed profile names and pinned catalog entries.
- Install the fixed pipx catalog into a user-owned isolated environment without
  sudo. If a separately justified system package has no user-local path, use
  `local-sudo-install` only for that exact package installation.
- Treat an existing command as verified only when pipx reports the exact
  allowlisted package and pinned version. Do not overwrite conflicts.
- Download the pinned main artifact from the explicit
  `https://pypi.org/simple` index and require its SHA-256 to match the exact
  release metadata served by PyPI before installation. Record timestamp,
  program, profile, action, scope and policy digests, package, pinned version,
  status, resolved command path, artifact SHA-256, and executable SHA-256.
- Installation must not launch the tool, contact the target, update templates,
  modify proxy settings, create accounts, or spend money.
- A successful install changes no hypothesis state and proves no finding.
- If provenance or a compatible version cannot be established, fail closed and
  return the exact blocker.

For a sudo-backed system package, keep the password source out of command
arguments, output, and logs; leave sudoers, proxy settings, and unrelated root
state unchanged. The privileged step installs only the already resolved
package and does not launch a scanner or contact a target.
