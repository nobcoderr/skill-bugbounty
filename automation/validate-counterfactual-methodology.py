#!/usr/bin/env python3
"""Validate a counterfactual methodology ledger without executing any probe."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MAX_CYCLES = 2
MAX_METHODS = 3
MIN_FACT_ANCHORS = 2

REQUIRED_METHOD_FIELDS = (
    "method_id",
    "parent_method_id",
    "fact_anchors",
    "changed_axes",
    "protected_invariant",
    "counterfactual_question",
    "attacker_variable",
    "authority_consumer",
    "oracle",
    "baseline",
    "safe_sibling",
    "negative_control",
    "falsifier",
    "release_reachability",
    "impact_plan",
    "safety",
    "stop_condition",
    "independence_explanation",
    "status",
)

FINDING_PROOF_FIELDS = (
    "source_to_sink_proven",
    "runtime_effect_proven",
    "negative_control_pass",
    "independent_reproduction",
    "authoritative_readback",
    "production_reachable",
    "impact_gate_pass",
    "prior_art_clear",
    "manual_confirmation",
)

PROHIBITED_CLAIMS = ("ZERO_DAY", "GUARANTEED_VULNERABILITY", "UNIVERSAL_DISCOVERY")


def nonempty(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    return value is not None


def validate_ledger(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("prior_result") != "NO_VALID_FINDING":
        errors.append("prior_result must be NO_VALID_FINDING")
    if data.get("target_eligible") is not True:
        errors.append("target_eligible must be true")
    cycle = data.get("cycle")
    if not isinstance(cycle, int) or isinstance(cycle, bool) or not 1 <= cycle <= MAX_CYCLES:
        errors.append(f"cycle must be an integer from 1 to {MAX_CYCLES}")
    if not nonempty(data.get("prior_method_exclusion_digest")):
        errors.append("prior_method_exclusion_digest is required")

    methods = data.get("methods")
    if not isinstance(methods, list) or not methods:
        errors.append("methods must be a non-empty list")
        return errors
    if len(methods) > MAX_METHODS:
        errors.append(f"methods exceeds the per-cycle limit of {MAX_METHODS}")

    seen: set[str] = set()
    for index, method in enumerate(methods):
        label = f"methods[{index}]"
        if not isinstance(method, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in REQUIRED_METHOD_FIELDS:
            if not nonempty(method.get(field)):
                errors.append(f"{label}.{field} is required")

        method_id = method.get("method_id")
        if isinstance(method_id, str):
            if method_id in seen:
                errors.append(f"duplicate method_id: {method_id}")
            seen.add(method_id)

        anchors = method.get("fact_anchors")
        if not isinstance(anchors, list) or len(anchors) < MIN_FACT_ANCHORS:
            errors.append(f"{label}.fact_anchors requires at least {MIN_FACT_ANCHORS} anchors")
        axes = method.get("changed_axes")
        if not isinstance(axes, list) or not axes:
            errors.append(f"{label}.changed_axes must identify a material axis")
        if not method.get("architecture_level_change") and isinstance(axes, list) and len(axes) < 2:
            errors.append(f"{label} needs an architecture-level change or at least two axes")

        question = method.get("counterfactual_question")
        if isinstance(question, str) and "what if" not in question.lower():
            errors.append(f"{label}.counterfactual_question must use an explicit What if form")

        status = method.get("status")
        if status == "VALID_FINDING_GENERATED":
            proof = method.get("finding_proof")
            if not isinstance(proof, dict):
                errors.append(f"{label}.finding_proof is required for VALID_FINDING_GENERATED")
            else:
                for field in FINDING_PROOF_FIELDS:
                    if proof.get(field) is not True:
                        errors.append(f"{label}.finding_proof.{field} must be true")

        serialized = json.dumps(method, sort_keys=True).upper()
        for claim in PROHIBITED_CLAIMS:
            if claim in serialized:
                errors.append(f"{label} contains prohibited certainty claim: {claim}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path, help="Counterfactual methodology ledger JSON")
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"COUNTERFACTUAL METHODOLOGY VALIDATION FAILED: {exc}")
        return 1
    if not isinstance(data, dict):
        print("COUNTERFACTUAL METHODOLOGY VALIDATION FAILED: root must be an object")
        return 1
    errors = validate_ledger(data)
    if errors:
        print("COUNTERFACTUAL METHODOLOGY VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"COUNTERFACTUAL METHODOLOGY VALIDATION PASSED: {len(data['methods'])} method(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

