#!/usr/bin/env python3
"""Network-free regressions for reparse/config/provenance KILL logic."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "REPARSE_CONFIG_PROVENANCE_REGRESSION_CASES.json"
METHOD = ROOT / "references" / "REPARSE_CONFIG_PROVENANCE_METHOD.md"


def decide(case: dict[str, object]) -> str:
    reaches = bool(case["untrusted_reaches_authority_consumer"])
    effect = bool(case["protected_effect_observed"])
    invariant = bool(case["representation_provenance_preserved"])
    terminal_claim = bool(case["terminal_impact_claimed"])
    terminal_proven = bool(case["terminal_edge_proven"])

    if not bool(case["evidence_complete"]):
        return "NEEDS_REPARSE_PROVENANCE_PROOF"
    if reaches and effect and terminal_claim and not terminal_proven:
        return "NEEDS_REPARSE_PROVENANCE_PROOF"
    if reaches and not invariant and effect:
        return "DO_NOT_KILL"
    if (not reaches or invariant) and not effect:
        return "KILL_ALLOWED"
    return "NEEDS_REPARSE_PROVENANCE_PROOF"


def main() -> int:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if data.get("package_version") != version:
        failures.append("regression package_version does not match VERSION")

    cases = data.get("cases", [])
    ids = [str(case.get("id")) for case in cases]
    if len(cases) != 18 or len(ids) != len(set(ids)):
        failures.append("expected 18 unique regression cases")
    required = {
        "id", "evidence_complete", "untrusted_reaches_authority_consumer",
        "representation_provenance_preserved", "protected_effect_observed",
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
        "REPARSE_CONFIG_PROVENANCE:v1",
        "Family A: trusted recovery text is decoded and reparsed as markup",
        "Family B: stored metadata becomes a generated HTML document",
        "Family C: data enters a secondary configuration grammar",
        "Family D: signed multipart provenance is lost across parser namespaces",
        "Family E: import attributes invoke generated or virtual setters",
        "NEEDS_REPARSE_PROVENANCE_PROOF",
        "Cross-family reparse and provenance KILL challenge",
    ):
        if marker not in method:
            failures.append(f"method missing marker: {marker}")

    schema = json.loads((ROOT / "config" / "CODEX_CLI_CANDIDATE_SCHEMA.json").read_text(encoding="utf-8"))
    if "reparse_config_provenance_challenge" not in schema.get("required", []):
        failures.append("candidate schema does not require reparse_config_provenance_challenge")

    if failures:
        print("REPARSE/CONFIG/PROVENANCE REGRESSION FAILED")
        for failure in failures:
            print("- " + failure)
        return 1
    print(f"REPARSE/CONFIG/PROVENANCE REGRESSION PASSED: {len(cases)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
