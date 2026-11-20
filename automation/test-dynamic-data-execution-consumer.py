#!/usr/bin/env python3
"""Deterministic regressions for dynamic-data execution-consumer KILL logic."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "DYNAMIC_DATA_EXECUTION_CONSUMER_REGRESSION_CASES.json"
METHOD = ROOT / "references" / "DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md"


def decide(case: dict[str, object]) -> str:
    if not bool(case["evidence_complete"]):
        return "NEEDS_EXECUTION_CONSUMER_PROOF"

    if bool(case["terminal_impact_claimed"]) and not bool(case["terminal_edge_proven"]):
        return "NEEDS_EXECUTION_CONSUMER_PROOF"

    reaches = bool(case["untrusted_value_reaches_consumer"])
    invariant_preserved = (not reaches) or all(
        bool(case[field])
        for field in (
            "data_only_normalized_before_consumer",
            "protocol_length_and_bytes_share_buffer",
            "attribute_allowlist_closes_delayed_state",
            "feature_activation_explicit_and_fail_closed",
        )
    )
    effect = bool(case["protected_effect_observed"])

    if reaches and not invariant_preserved and effect:
        return "DO_NOT_KILL"
    if invariant_preserved and not effect:
        return "KILL_ALLOWED"
    return "NEEDS_EXECUTION_CONSUMER_PROOF"


def main() -> int:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if data.get("package_version") != version:
        failures.append(
            f"package version mismatch: cases={data.get('package_version')!r}, VERSION={version!r}"
        )

    required_ids = {
        "dynamic-resource-methods-control-protocol-frame",
        "resource-flattened-and-framed-from-one-buffer",
        "protocol-effect-proven-terminal-session-edge-missing",
        "protocol-state-and-terminal-consumer-independently-proven",
        "remote-import-attribute-survives-to-shell-consumer",
        "strict-import-allowlist-and-fixed-argv",
        "ui-feature-gate-bypassed-by-direct-source-type",
        "optional-interpreter-dependency-absent-from-release",
        "dependency-presence-auto-enables-unsafe-interpreter",
        "optional-interpreter-explicitly-disabled-fail-closed",
        "optional-runtime-presence-and-release-reachability-unproven",
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
        "evidence_complete",
        "untrusted_value_reaches_consumer",
        "data_only_normalized_before_consumer",
        "protocol_length_and_bytes_share_buffer",
        "attribute_allowlist_closes_delayed_state",
        "feature_activation_explicit_and_fail_closed",
        "protected_effect_observed",
        "terminal_impact_claimed",
        "terminal_edge_proven",
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
        "DYNAMIC_DATA_EXECUTION_CONSUMER:v1",
        "NEEDS_EXECUTION_CONSUMER_PROOF",
        "Dynamic object methods become protocol control",
        "Import metadata becomes delayed execution state",
        "Optional dependency silently enables an interpreter",
        "Mandatory execution-consumer KILL challenge",
    ):
        if marker not in method_text:
            failures.append(f"method missing marker: {marker}")

    schema = json.loads(
        (ROOT / "config" / "CODEX_CLI_CANDIDATE_SCHEMA.json").read_text(encoding="utf-8")
    )
    if "execution_consumer_challenge" not in schema.get("required", []):
        failures.append("candidate schema does not require execution_consumer_challenge")

    if failures:
        print("DYNAMIC-DATA EXECUTION-CONSUMER REGRESSION FAILED")
        for failure in failures:
            print("- " + failure)
        return 1
    print(f"DYNAMIC-DATA EXECUTION-CONSUMER REGRESSION PASSED: {len(actual_ids)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

