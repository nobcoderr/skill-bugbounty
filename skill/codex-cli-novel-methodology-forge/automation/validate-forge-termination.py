#!/usr/bin/env python3
"""Validate the bounded V13 forge state machine and return its next action."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _v13lib import load_json


MAX_FORGE_WAVES = 2
MAX_METHODS_PER_WAVE = 4
MAX_EXECUTED_METHODS_TOTAL = 6


def decide(state: dict) -> dict:
    violations: list[str] = []
    waves = state.get("forge_waves", [])
    executions = state.get("executions", [])
    material_gaps = [gap for gap in state.get("coverage_gaps", []) if gap.get("status") == "MATERIAL"]

    if len(waves) > MAX_FORGE_WAVES:
        violations.append("MAX_FORGE_WAVES exceeded")
    if any(int(wave.get("method_count", 0)) > MAX_METHODS_PER_WAVE for wave in waves):
        violations.append("MAX_METHODS_PER_WAVE exceeded")
    if len(executions) > MAX_EXECUTED_METHODS_TOTAL:
        violations.append("MAX_EXECUTED_METHODS_TOTAL exceeded")

    wave_numbers = [wave.get("wave") for wave in waves]
    if wave_numbers != sorted(set(wave_numbers)):
        violations.append("forge wave numbering is duplicated or unordered")

    if len(waves) >= 2:
        first_evidence = set(waves[0].get("new_evidence_ids", []))
        second_parent_evidence: set[str] = set()
        for gap in material_gaps:
            if gap.get("introduced_in_wave") == 2:
                second_parent_evidence.update(gap.get("parent_new_evidence_ids", []))
        if not first_evidence or not first_evidence.intersection(second_parent_evidence):
            violations.append("wave two lacks a new factual coverage gap derived from wave-one evidence")

    consecutive_zero: dict[str, int] = {}
    exhausted_gaps: set[str] = set()
    for execution in executions:
        gap_id = execution.get("gap_id")
        gained = int(execution.get("new_material_evidence_count", 0)) > 0
        consecutive_zero[gap_id] = 0 if gained else consecutive_zero.get(gap_id, 0) + 1
        if consecutive_zero[gap_id] >= 2:
            exhausted_gaps.add(gap_id)
        elif gap_id in exhausted_gaps and gained:
            violations.append(f"execution continued after gap exhaustion: {gap_id}")
    for gap_id in exhausted_gaps:
        later = False
        zero_seen = 0
        for execution in executions:
            if execution.get("gap_id") != gap_id:
                continue
            if int(execution.get("new_material_evidence_count", 0)) == 0:
                zero_seen += 1
                if zero_seen > 2:
                    later = True
            else:
                zero_seen = 0
        if later:
            violations.append(f"more than two consecutive zero-gain executions for {gap_id}")

    if violations:
        return {"STATE_VALID": False, "NEXT_ACTION": "STOP_INVALID_STATE", "VIOLATIONS": violations, "EXHAUSTED_GAPS": sorted(exhausted_gaps)}

    if int(state.get("surviving_count", 0)) > 0 or int(state.get("valid_finding_count", 0)) > 0 or int(state.get("pending_verification_count", 0)) > 0:
        action = "RETURN_TO_NORMAL_VERIFICATION"
    elif state.get("normal_audit_frozen") is not True:
        action = "FREEZE_NORMAL_AUDIT_STATE"
    elif not material_gaps:
        action = "TERMINATE_NO_VALID_FINDING"
    elif any(int(item.get("new_material_evidence_count", 0)) > 0 for item in executions):
        action = "POOL_AND_AGGRESSIVELY_FALSIFY_NEW_EVIDENCE"
    else:
        active_gaps = [gap for gap in material_gaps if gap.get("gap_id") not in exhausted_gaps]
        approved_remaining = sum(int(wave.get("approved_not_executed", 0)) for wave in waves)
        if approved_remaining and len(executions) < MAX_EXECUTED_METHODS_TOTAL and active_gaps:
            action = "EXECUTE_NEXT_APPROVED_METHODOLOGY"
        elif not waves and active_gaps:
            action = "RUN_METHODOLOGY_FORGE_WAVE_1"
        elif len(waves) == 1 and waves[0].get("new_evidence_ids"):
            action = "ANALYZE_NEW_FACTUAL_GAP_BEFORE_OPTIONAL_WAVE_2"
        else:
            action = "NOVEL_METHODOLOGY_EXPANSION_EXHAUSTED"

    return {
        "STATE_VALID": True,
        "NEXT_ACTION": action,
        "VIOLATIONS": [],
        "EXHAUSTED_GAPS": sorted(exhausted_gaps),
        "LIMITS": {
            "MAX_FORGE_WAVES": MAX_FORGE_WAVES,
            "MAX_METHODS_PER_WAVE": MAX_METHODS_PER_WAVE,
            "MAX_EXECUTED_METHODS_TOTAL": MAX_EXECUTED_METHODS_TOTAL,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("state", type=Path)
    parser.add_argument("--require-valid", action="store_true")
    args = parser.parse_args()
    result = decide(load_json(args.state))
    print(json.dumps(result, sort_keys=True, indent=2))
    return int(args.require_valid and not result["STATE_VALID"])


if __name__ == "__main__":
    raise SystemExit(main())
