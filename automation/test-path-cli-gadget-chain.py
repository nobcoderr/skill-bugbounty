#!/usr/bin/env python3
"""Network-free regressions for path, CLI grammar, and gadget-chain KILL logic."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "PATH_CLI_GADGET_CHAIN_REGRESSION_CASES.json"
METHOD = ROOT / "references" / "PATH_CLI_GADGET_CHAIN_METHOD.md"


def decide(case: dict[str, object]) -> str:
    reaches = bool(case["untrusted_reaches_secondary_grammar"])
    invariant = bool(case["exact_consumer_identity_preserved"])
    effect = bool(case["protected_effect_observed"])
    terminal_claim = bool(case["terminal_impact_claimed"])
    terminal_proven = bool(case["terminal_edge_proven"])

    if not bool(case["evidence_complete"]):
        return "NEEDS_PATH_CLI_GADGET_PROOF"
    if reaches and effect and terminal_claim and not terminal_proven:
        return "NEEDS_PATH_CLI_GADGET_PROOF"
    if reaches and not invariant and effect:
        return "DO_NOT_KILL"
    if (not reaches or invariant) and not effect:
        return "KILL_ALLOWED"
    return "NEEDS_PATH_CLI_GADGET_PROOF"


def main() -> int:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if data.get("package_version") != version:
        failures.append("regression package_version does not match VERSION")

    cases = data.get("cases", [])
    ids = [str(case.get("id")) for case in cases]
    if len(cases) != 17 or len(ids) != len(set(ids)):
        failures.append("expected 17 unique regression cases")
    required = {
        "id", "evidence_complete", "untrusted_reaches_secondary_grammar",
        "exact_consumer_identity_preserved", "protected_effect_observed",
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
        "PATH_CLI_GADGET_CHAIN:v1",
        "Family A: path capture is not path authorization",
        "Family B: argv data can become downstream option grammar",
        "Family C: sanitizer output can activate through a shipped gadget",
        "Patch-variant and sibling sweep",
        "NEEDS_PATH_CLI_GADGET_PROOF",
        "Cross-family KILL challenge",
    ):
        if marker not in method:
            failures.append(f"method missing marker: {marker}")

    schema = json.loads((ROOT / "config" / "CODEX_CLI_CANDIDATE_SCHEMA.json").read_text(encoding="utf-8"))
    if "path_cli_gadget_chain_challenge" not in schema.get("required", []):
        failures.append("candidate schema does not require path_cli_gadget_chain_challenge")

    if failures:
        print("PATH/CLI/GADGET REGRESSION FAILED")
        for failure in failures:
            print("- " + failure)
        return 1
    print(f"PATH/CLI/GADGET REGRESSION PASSED: {len(cases)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
