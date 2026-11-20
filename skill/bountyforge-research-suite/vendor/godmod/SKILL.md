---
name: godmod
description: "Quarantined compatibility metadata for the malformed BountyForge godmod source. Use only when explicitly inspecting its provenance; it provides no autonomous security capability and never authorizes tools, scanning, exploitation, or target access."
---

# Godmod Quarantine Adapter

This entry replaces an upstream shell heredoc that was stored under the name
`SKILL.md` and therefore could not be parsed as a Codex skill. The upstream
content remains represented only by its provenance record in the BountyForge
source catalog.

Do not use this adapter as an operating prompt. It grants no expertise,
authorization, target scope, tool access, execution permission, severity, or
evidence status. Route real work through `bountyforge-research-suite`, the
mandatory auto-router, and target-specific authorized security skills.

Required result when explicitly invoked:

```text
STATUS=QUARANTINED_METADATA_ONLY
AUTONOMOUS_EXECUTION=NO
AUTHORIZATION_GRANTED=NO
```

