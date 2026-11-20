#!/usr/bin/env python3
"""Derive V13 methodology value and promotion readiness from event ledgers."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from _v13lib import load_jsonl


STATE_ORDER = ["EXPERIMENTAL", "SOURCE_USEFUL", "REPRODUCIBLE", "BLIND_VALIDATED", "PROMOTED"]


def derive(methodology_id: str, executions: list[dict[str, Any]], events: list[dict[str, Any]], baseline_false_positive_rate: float) -> dict[str, Any]:
    method_runs = [item for item in executions if item.get("record_type") == "METHODOLOGY_EXECUTION" and item.get("methodology_id") == methodology_id]
    method_events = [item for item in events if item.get("methodology_id") == methodology_id]

    unique_runs = {
        (
            item.get("source_snapshot_digest"),
            item.get("blind_seed_digest", item.get("input_capsule_digest")),
            item.get("target_family", ""),
        )
        for item in method_runs
    }
    discovery_blind = [item for item in method_runs if item.get("run_mode") in {"DISCOVERY", "BLIND"}]
    material_runs = [item for item in discovery_blind if int(item.get("new_material_evidence_count", 0)) > 0]
    material_rate = len(material_runs) / len(discovery_blind) if discovery_blind else 0.0

    evidence_executors: dict[str, set[str]] = defaultdict(set)
    for run in method_runs:
        child = str(run.get("child_context", {}).get("child_id", ""))
        for atom in run.get("new_material_evidence", []):
            evidence_executors[str(atom.get("semantic_identity"))].add(child)
    reproducible = any(len(children - {""}) >= 2 for children in evidence_executors.values())

    validation_events = [item for item in method_events if item.get("record_type") == "METHODOLOGY_VALIDATION_EVENT"]
    valid_findings = [
        item for item in validation_events
        if item.get("full_pipeline_pass") is True and item.get("duplicate_or_known") is False
    ]
    report_ready = [item for item in validation_events if item.get("report_ready_outcome") in {"VALID", "FALSE_POSITIVE"}]
    false_positives = [item for item in report_ready if item.get("report_ready_outcome") == "FALSE_POSITIVE"]
    false_positive_rate = len(false_positives) / len(report_ready) if report_ready else 0.0

    blind_families = {
        str(item.get("target_family"))
        for item in method_runs
        if item.get("run_mode") == "BLIND" and int(item.get("new_material_evidence_count", 0)) > 0 and item.get("target_family")
    }
    blind_pass = any(
        item.get("record_type") == "METHODOLOGY_BLIND_GENERALIZATION"
        and item.get("result") == "PASS"
        and item.get("sealed_before_execution") is True
        and item.get("curator_independent") is True
        and item.get("answer_unsealed_after_output") is True
        and item.get("ground_truth_leakage") == 0
        and isinstance(item.get("curator_manifest_digest"), str)
        and len(item["curator_manifest_digest"]) == 64
        for item in method_events
    )
    regression_pass = any(
        item.get("record_type") == "METHODOLOGY_REGRESSION_RESULT"
        and item.get("exact_root_regression") == 0
        and item.get("patched_control_false_positive") == 0
        and item.get("ground_truth_leakage") == 0
        and item.get("runaway") == 0
        for item in method_events
    )
    human_promotion = any(
        item.get("record_type") == "METHODOLOGY_PROMOTION_DECISION"
        and item.get("to_status") == "PROMOTED"
        and item.get("human_approved") is True
        for item in method_events
    )

    state = "EXPERIMENTAL"
    if any(item.get("new_material_evidence") for item in method_runs):
        state = "SOURCE_USEFUL"
    if reproducible:
        state = "REPRODUCIBLE"
    if reproducible and blind_pass and len(blind_families) >= 2:
        state = "BLIND_VALIDATED"

    promotion_checks = {
        "METHODOLOGY_EXECUTIONS_GTE_3": len(unique_runs) >= 3,
        "NEW_MATERIAL_EVIDENCE_RATE_GTE_50_PERCENT": material_rate >= 0.50,
        "NON_DUPLICATE_VALID_FINDING_GTE_1": len(valid_findings) >= 1,
        "FALSE_POSITIVE_RATE_LE_BASELINE": false_positive_rate <= baseline_false_positive_rate,
        "BLIND_GENERALIZATION_PASS": blind_pass and len(blind_families) >= 2,
        "REGRESSION_CONTROLS_PASS": regression_pass,
        "HUMAN_PROMOTION_APPROVAL": human_promotion,
    }
    eligible = all(promotion_checks.values())
    if eligible:
        state = "PROMOTED"

    return {
        "METHODOLOGY_ID": methodology_id,
        "RECOMMENDED_STATUS": state,
        "PROMOTION_ELIGIBLE": eligible,
        "EXECUTION_COUNT": len(unique_runs),
        "DISCOVERY_BLIND_EXECUTION_COUNT": len(discovery_blind),
        "MATERIAL_GAIN_EXECUTION_COUNT": len(material_runs),
        "NEW_MATERIAL_EVIDENCE_RATE": round(material_rate, 6),
        "REPRODUCIBLE_EVIDENCE_IDENTITIES": sorted(identity for identity, children in evidence_executors.items() if len(children - {""}) >= 2),
        "VALID_FINDING_COUNT": len(valid_findings),
        "FALSE_POSITIVE_COUNT": len(false_positives),
        "FALSE_POSITIVE_RATE": round(false_positive_rate, 6),
        "BLIND_TARGET_FAMILY_COUNT": len(blind_families),
        "PROMOTION_CHECKS": promotion_checks,
        "NOTE": "Derived only; this helper never mutates status or the default stack.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("methodology_id")
    parser.add_argument("--executions", type=Path, required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--baseline-false-positive-rate", type=float, default=0.0)
    args = parser.parse_args()
    result = derive(
        args.methodology_id,
        load_jsonl(args.executions),
        load_jsonl(args.events),
        args.baseline_false_positive_rate,
    )
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
