#!/usr/bin/env python3
"""Network-free regressions for archive/renderer/framework KILL logic."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "ARCHIVE_RENDERER_FRAMEWORK_REGRESSION_CASES.json"
METHOD = ROOT / "references" / "ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md"


def decide(case: dict[str, object]) -> str:
    if not bool(case["evidence_complete"]):
        return "NEEDS_ARCHIVE_RENDERER_PROOF"
    if bool(case["terminal_impact_claimed"]) and not bool(case["terminal_edge_proven"]):
        return "NEEDS_ARCHIVE_RENDERER_PROOF"
    reaches = bool(case["untrusted_reaches_authority_consumer"])
    invariant = (
        bool(case["root_origin_namespace_preserved"])
        and bool(case["object_identity_preserved_at_use"])
        and bool(case["feature_environment_reachable"])
    )
    effect = bool(case["protected_effect_observed"])
    if reaches and not invariant and effect:
        return "DO_NOT_KILL"
    if (not reaches or invariant or not bool(case["feature_environment_reachable"])) and not effect:
        return "KILL_ALLOWED"
    return "NEEDS_ARCHIVE_RENDERER_PROOF"


def main() -> int:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if data.get("package_version") != version:
        failures.append("regression package_version does not match VERSION")

    cases = data.get("cases", [])
    ids = [str(case.get("id")) for case in cases]
    if len(cases) != 16 or len(ids) != len(set(ids)):
        failures.append("expected 16 unique regression cases")
    required = {
        "id", "evidence_complete", "untrusted_reaches_authority_consumer",
        "root_origin_namespace_preserved", "object_identity_preserved_at_use",
        "feature_environment_reachable", "protected_effect_observed",
        "terminal_impact_claimed", "terminal_edge_proven", "expected",
    }
    for case in cases:
        missing = sorted(required - set(case))
        if missing:
            failures.append(f"{case.get('id', '<missing-id>')}: missing {missing}")
            continue
        actual = decide(case)
        if actual != case["expected"]:
            failures.append(f"{case['id']}: expected {case['expected']}, got {actual}")

    method = METHOD.read_text(encoding="utf-8")
    for marker in (
        "ARCHIVE_RENDERER_FRAMEWORK_CONSUMER:v1",
        "Family A: archive entry becomes a different filesystem object",
        "Family B: browser request reaches a destructive filesystem sink",
        "Family C: upload metadata becomes markup and a secondary resource load",
        "Family D: inline document options select runtime capability",
        "Family E: request parameters enter a framework-reserved option namespace",
        "NEEDS_ARCHIVE_RENDERER_PROOF",
        "Cross-family consumer-boundary KILL challenge",
    ):
        if marker not in method:
            failures.append(f"method missing marker: {marker}")

    schema = json.loads((ROOT / "config" / "CODEX_CLI_CANDIDATE_SCHEMA.json").read_text(encoding="utf-8"))
    if "archive_renderer_framework_challenge" not in schema.get("required", []):
        failures.append("candidate schema does not require archive_renderer_framework_challenge")

    if failures:
        print("ARCHIVE/RENDERER/FRAMEWORK REGRESSION FAILED")
        for failure in failures:
            print("- " + failure)
        return 1
    print(f"ARCHIVE/RENDERER/FRAMEWORK REGRESSION PASSED: {len(cases)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
