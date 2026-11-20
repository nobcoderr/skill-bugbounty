# Local installation notes

- Installed on 2026-11-14 from `/home/kali/Downloads/skill-pack-codex-cli-2026-11-14.zip`.
- Source ZIP SHA-256: `da51ce7b19b7bc87f54cd764088710812115b5eea640dcbc8a8c55a3c8243f8b`.
- The ZIP container passed `unzip -t` and contained no absolute or parent-traversal paths.
- The bundled `PACKAGE_MANIFEST.sha256` did not match 121 bundled files, so it is retained only as upstream metadata and is not treated as a verified integrity baseline.
- For Codex compatibility, unsupported top-level frontmatter fields were moved under `metadata`, one unquoted YAML description was repaired, one oversized description was shortened, forbidden angle brackets in five descriptions were replaced with square brackets, and Windows home paths were mapped to `/home/kali`.
- The bundled `.system` directory was not installed over Codex's built-in system skills.
- Final validation: 195 user skills passed the Codex skill validator; all 84 primary security skills and 142 routing artifacts are mapped; 94 routing regression profiles passed.
