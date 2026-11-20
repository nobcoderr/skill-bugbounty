#!/usr/bin/env python3
"""Create a local multi-agent audit workspace without running an agent or network actions.

The `.codex-security/` folder name is a stable schema id. Use it on Cursor,
Codex CLI, Claude Code, Gemini, or any other runtime.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_SOURCE = PACKAGE_ROOT / "config" / "CODEX_CLI_CANDIDATE_SCHEMA.json"
REGISTRY_SCHEMA_SOURCE = PACKAGE_ROOT / "config" / "CODEX_CLI_RESEARCH_PATH_REGISTRY_SCHEMA.json"
EXECUTION_SCHEMA_SOURCE = PACKAGE_ROOT / "config" / "CODEX_CLI_ADAPTIVE_EXECUTION_PROVENANCE_SCHEMA.json"

TEMPLATES = {
    "00-authorization-scope.md": """# Authorization and Scope\n\n- Program / owner:\n- Rules source:\n- In-scope asset/repository/component:\n- Eligible classes:\n- Exclusions:\n- Allowed methods and automation:\n- Rate/concurrency limits:\n- Researcher-owned accounts/data/environment:\n- Stop conditions:\n- Unresolved scope facts:\n""",
    "01-target-reality.md": """# Target Reality Map\n\n- Repository URL/path:\n- Commit/tag/branch:\n- Dirty state:\n- Build/package/artifact:\n- Production/mainnet/stable-release consumer:\n- Default/realistic configuration:\n- Feature flags/plugins/platform prerequisites:\n- Source-to-release chain:\n- Unresolved reachability facts:\n""",
    "02-security-model.md": """# Security Model\n\n## Principals, roles, tenants, and objects\n\n## Permission/action/resource-scope matrix\n\n| Route/call | Subject | Action | Target identifier | Tenant/org | State | Policy helper | Parameters passed | Downstream filter |\n|---|---|---|---|---|---|---|---|---|\n\n## Credential/capability lifecycle\n\n## State-machine invariants\n\n## Trusted roles and intended behavior\n\n## Sensitive sinks and protected assets\n""",
    "03-routing-ledger.md": """# Mandatory Routing Ledger\n\n| Module | State | Trigger/evidence | Companions | Re-evaluate when |\n|---|---|---|---|---|\n""",
    "04-research-path-registry.json": """{
  "audit_id": "replace-me",
  "package_version": "2026.09.03-chromium-v8-variant-hunter-v1-live-audit-only",
  "paths": [],
  "waves": [
    {
      "wave_id": "wave-1",
      "wave_type": "CORE",
      "core_lanes": ["AUTHORITY_CAPABILITY", "REPRESENTATION_CONSUMER", "STATE_COMPOSITION"],
      "launch_conditions": ["INITIAL_AUTHORIZED_WAVE"],
      "specialists": [],
      "stop_conditions": ["core coverage and convergence analysis completed"]
    }
  ],
  "coverage_analysis": {
    "material_surfaces": [],
    "covered_surfaces": [],
    "coverage_gaps": [],
    "analysis": "not yet assessed"
  },
  "convergence_checks": [],
  "adaptive_execution": {
    "triggered": false,
    "provenance_file": "",
    "transcript_sha256": "",
    "spawn_attempts": 0,
    "spawn_successes": 0,
    "spawn_failures": 0,
    "unique_specialist_ids": 0,
    "separate_specialist_inputs": 0,
    "separate_specialist_outputs": 0,
    "root_consumed_specialist_outputs": 0,
    "executed_specialist_count": 0,
    "execution_proven": false,
    "failure_reason": ""
  },
  "termination": {
    "decision": "STOP",
    "reasons": ["audit not started"],
    "unavailable_evidence": [],
    "another_wave_authorized": false
  }
}
""",
    "evidence/INDEX.md": """# Evidence Index\n\nRecord exact repository revision, file/symbol/range, command/log path, timestamp/timezone, environment, and what each item proves. Do not record inferred evidence.\n""",
    "commands/README.md": """# Command Log\n\nStore commands that were actually authorized and executed, their working directory, time, exit status, and output artifact. This workspace initializer does not run commands for you.\n""",
    "candidates/README.md": """# Candidates\n\nStore one JSON candidate per file using `../candidate.schema.json`. Discovery starts at `CODE_DERIVED_HYPOTHESIS`; advance only through the v10-compatible proof states. Bind each candidate to a registered research path, primitive-impact chain, and exact implementation source when material. Only independent final triage may assign STRONG/MEDIUM/WEAK/KILL.\n""",
    "reviews/README.md": """# Independent Reviews\n\nKeep semi-triage, reachability, security-model, prior-art, end-to-end trace, test-design, and final-judge outputs separate. Use PASS/FAIL/BLOCKED with evidence.\n""",
    "final/README.md": """# Final Technical Handoff\n\nInclude only candidates that survived the required gates. Manual reproduction status is separate from the source-review verdict. If none survive, record `NO VALID FINDING`.\n""",
}


def write_file(path: Path, content: str, force: bool, dry_run: bool) -> str:
    if path.exists() and not force:
        return f"SKIP existing {path}"
    if dry_run:
        return f"CREATE {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"CREATED {path}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Target repository/workspace root")
    parser.add_argument("--dir-name", default=".codex-security", help="Audit directory name")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")
    parser.add_argument("--dry-run", action="store_true", help="Show planned files without writing")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    workspace = root / args.dir_name

    if not SCHEMA_SOURCE.is_file() or not REGISTRY_SCHEMA_SOURCE.is_file() or not EXECUTION_SCHEMA_SOURCE.is_file():
        raise SystemExit(
            f"Missing package schema: {SCHEMA_SOURCE}, {REGISTRY_SCHEMA_SOURCE}, or {EXECUTION_SCHEMA_SOURCE}"
        )
    json.loads(SCHEMA_SOURCE.read_text(encoding="utf-8"))
    json.loads(REGISTRY_SCHEMA_SOURCE.read_text(encoding="utf-8"))
    json.loads(EXECUTION_SCHEMA_SOURCE.read_text(encoding="utf-8"))

    actions = []
    for rel, content in TEMPLATES.items():
        actions.append(write_file(workspace / rel, content, args.force, args.dry_run))

    schema_target = workspace / "candidate.schema.json"
    if schema_target.exists() and not args.force:
        actions.append(f"SKIP existing {schema_target}")
    elif args.dry_run:
        actions.append(f"CREATE {schema_target}")
    else:
        schema_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SCHEMA_SOURCE, schema_target)
        actions.append(f"CREATED {schema_target}")

    registry_schema_target = workspace / "research-path-registry.schema.json"
    if registry_schema_target.exists() and not args.force:
        actions.append(f"SKIP existing {registry_schema_target}")
    elif args.dry_run:
        actions.append(f"CREATE {registry_schema_target}")
    else:
        registry_schema_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REGISTRY_SCHEMA_SOURCE, registry_schema_target)
        actions.append(f"CREATED {registry_schema_target}")

    execution_schema_target = workspace / "adaptive-execution-provenance.schema.json"
    if execution_schema_target.exists() and not args.force:
        actions.append(f"SKIP existing {execution_schema_target}")
    elif args.dry_run:
        actions.append(f"CREATE {execution_schema_target}")
    else:
        execution_schema_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(EXECUTION_SCHEMA_SOURCE, execution_schema_target)
        actions.append(f"CREATED {execution_schema_target}")

    print("\n".join(actions))
    print("No Codex process, network request, scanner, fuzzer, or PoC was executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
