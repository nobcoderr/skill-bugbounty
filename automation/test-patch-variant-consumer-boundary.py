#!/usr/bin/env python3
"""Deterministic regressions for patch-variant and consumer-boundary KILL logic."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "PATCH_VARIANT_CONSUMER_BOUNDARY_REGRESSION_CASES.json"
METHOD = ROOT / "references" / "PATCH_VARIANT_CONSUMER_BOUNDARY_METHOD.md"


def decide(case: dict[str, object]) -> str:
    if not bool(case["evidence_complete"]):
        return "NEEDS_CONSUMER_PROOF"

    invariant_preserved = all(
        bool(case[field])
        for field in (
            "checked_matches_consumed",
            "operation_error_domain_complete",
            "downstream_protocol_capability_bounded",
            "failure_rejected_before_critical_consumer",
        )
    )
    effect = bool(case["protected_effect_observed"])
    if not invariant_preserved and effect:
        return "DO_NOT_KILL"
    if invariant_preserved and not effect:
        return "KILL_ALLOWED"
    return "NEEDS_CONSUMER_PROOF"


def main() -> int:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if data.get("package_version") != version:
        failures.append(
            f"package version mismatch: cases={data.get('package_version')!r}, VERSION={version!r}"
        )

    required_ids = {
        "zero-only-guard-leaves-decimal-error-domain",
        "all-arithmetic-errors-rejected-before-state",
        "selector-validates-child-consumer-uses-parent",
        "selected-node-used-with-typed-dom-construction",
        "url-validator-accepts-file-protocol-consumer",
        "explicit-scheme-set-matches-client-capability",
        "async-consumer-placement-not-yet-proven",
    }
    actual_ids = [str(case.get("id")) for case in data.get("cases", [])]
    if len(actual_ids) != len(set(actual_ids)):
        failures.append("duplicate case id")
    if set(actual_ids) != required_ids:
        failures.append(
            f"case inventory mismatch: missing={sorted(required_ids - set(actual_ids))}, "
            f"extra={sorted(set(actual_ids) - required_ids)}"
        )

    required_fields = {
        "id",
        "checked_matches_consumed",
        "operation_error_domain_complete",
        "downstream_protocol_capability_bounded",
        "failure_rejected_before_critical_consumer",
        "protected_effect_observed",
        "evidence_complete",
        "expected",
    }
    for case in data.get("cases", []):
        missing = sorted(required_fields - set(case))
        if missing:
            failures.append(f"{case.get('id', '<missing-id>')}: missing {missing}")
            continue
        actual = decide(case)
        if actual != case["expected"]:
            failures.append(f"{case['id']}: expected {case['expected']}, got {actual}")

    method_text = METHOD.read_text(encoding="utf-8")
    for marker in (
        "PATCH_VARIANT_CONSUMER_BOUNDARY:v1",
        "NEEDS_CONSUMER_PROOF",
        "Patch-variant failure-domain sweep",
        "Eligible value versus consumed value",
        "Validator versus protocol consumer",
    ):
        if marker not in method_text:
            failures.append(f"method missing marker: {marker}")

    schema = json.loads(
        (ROOT / "config" / "CODEX_CLI_CANDIDATE_SCHEMA.json").read_text(encoding="utf-8")
    )
    if "consumer_boundary_challenge" not in schema.get("required", []):
        failures.append("candidate schema does not require consumer_boundary_challenge")

    if failures:
        print("PATCH-VARIANT CONSUMER-BOUNDARY REGRESSION FAILED")
        for failure in failures:
            print("- " + failure)
        return 1
    print(f"PATCH-VARIANT CONSUMER-BOUNDARY REGRESSION PASSED: {len(actual_ids)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
