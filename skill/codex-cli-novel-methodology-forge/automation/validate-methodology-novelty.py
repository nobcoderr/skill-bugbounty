#!/usr/bin/env python3
"""Deterministic pre-execution novelty critic for one generated methodology."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _v13lib import (
    classify_coverage_delta,
    jaccard,
    load_all_methods,
    load_json,
    material_gap_ids,
    method_operators,
    method_oracle,
    signature_values,
)


FORBIDDEN_FIELDS = {
    "specific_vulnerability",
    "vulnerable_file",
    "vulnerable_function",
    "payload",
    "desired_outcome",
    "expected_bug_class",
}


def compare(candidate: dict[str, Any], existing: dict[str, Any]) -> dict[str, Any]:
    candidate_ops = method_operators(candidate)
    existing_ops = method_operators(existing)
    op_similarity = jaccard(candidate_ops, existing_ops)

    candidate_signature = signature_values(candidate)
    existing_signature = signature_values(existing)
    size = max(len(candidate_signature), len(existing_signature), 1)
    padded_candidate = candidate_signature + [""] * (size - len(candidate_signature))
    padded_existing = existing_signature + [""] * (size - len(existing_signature))
    signature_matches = sum(left == right for left, right in zip(padded_candidate, padded_existing))
    signature_similarity = signature_matches / size
    changed_signature_fields = size - signature_matches

    oracle_same = method_oracle(candidate) == method_oracle(existing)
    candidate_start = set(candidate.get("procedure_graph", {}).get("start_fact_types", []))
    existing_start = set(existing.get("procedure_graph", {}).get("start_fact_types", []))
    start_similarity = jaccard(candidate_start, existing_start)
    weighted = 0.40 * op_similarity + 0.35 * signature_similarity + 0.15 * float(oracle_same) + 0.10 * start_similarity
    return {
        "methodology_id": existing.get("methodology_id"),
        "weighted_similarity": round(weighted, 6),
        "operator_similarity": round(op_similarity, 6),
        "signature_similarity": round(signature_similarity, 6),
        "changed_signature_fields": changed_signature_fields,
        "oracle_same": oracle_same,
    }


def evaluate(candidate: dict[str, Any], registry_root: Path, gap_packet: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    novelty = "PASS"
    executable = "PASS"

    if FORBIDDEN_FIELDS.intersection(candidate):
        novelty = "FAIL"
        reasons.append("target-specific vulnerability fields are forbidden")

    graph = candidate.get("procedure_graph", {})
    nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    if len(nodes) < 2:
        novelty = "FAIL"
        reasons.append("procedure graph has fewer than two reasoning steps")
    if len(nodes) > 12:
        novelty = "FAIL"
        reasons.append("procedure is excessively broad")
    if nodes and len(nodes) >= 5 and all(not node.get("depends_on") for node in nodes):
        novelty = "FAIL"
        reasons.append("flat checklist is not a reasoning procedure")

    material_ids = material_gap_ids(gap_packet)
    target_gaps = set(candidate.get("target_gap_ids", []))
    if not target_gaps or not target_gaps.issubset(material_ids):
        executable = "FAIL"
        reasons.append("target gap is not a locally executable material coverage gap")

    required_inputs = set(candidate.get("required_inputs", []))
    if not required_inputs:
        executable = "FAIL"
        reasons.append("required inputs are missing")
    if not candidate.get("falsification_strategy") or not candidate.get("termination_condition"):
        executable = "FAIL"
        reasons.append("falsifier or deterministic termination is missing")

    comparisons = [compare(candidate, method) for method in load_all_methods(registry_root)]
    closest = max(comparisons, key=lambda item: item["weighted_similarity"]) if comparisons else {
        "methodology_id": None,
        "weighted_similarity": 0.0,
        "operator_similarity": 0.0,
        "signature_similarity": 0.0,
        "changed_signature_fields": 8,
        "oracle_same": False,
    }
    novelty_score = round(1.0 - closest["weighted_similarity"], 6)

    semantic_duplicate = (
        closest["operator_similarity"] == 1.0 and closest["signature_similarity"] == 1.0
    ) or (
        closest["signature_similarity"] >= 0.875
        and closest["operator_similarity"] >= 0.50
        and closest["oracle_same"]
    ) or (
        closest["operator_similarity"] >= 0.80 and closest["oracle_same"]
    )
    if semantic_duplicate:
        novelty = "FAIL"
        reasons.append(f"semantic duplicate of {closest['methodology_id']}")
    if novelty_score < 0.35:
        novelty = "FAIL"
        reasons.append("marginal semantic novelty is below 0.35")

    signature = candidate.get("reasoning_signature", {})
    traversal_change = bool(signature.get("start_point")) and bool(signature.get("traversal_direction"))
    new_oracle_or_falsifier = not closest["oracle_same"] or bool(graph.get("falsifier_class"))
    distinct_relation = closest["changed_signature_fields"] >= 2 or (traversal_change and new_oracle_or_falsifier)
    if not distinct_relation:
        novelty = "FAIL"
        reasons.append("no materially changed reasoning relation")

    baseline_inputs: set[str] = set()
    for method in load_all_methods(registry_root):
        baseline_inputs.update(str(item) for item in method.get("required_inputs", []))
    new_input_count = len(required_inputs - baseline_inputs)
    points = 1 if target_gaps else 0
    points += min(3, int(closest["changed_signature_fields"]))
    points += int(not closest["oracle_same"])
    points += int(new_input_count > 0)
    delta = classify_coverage_delta(points)

    false_positive_risk = "LOW"
    if len(candidate.get("potential_false_positive_modes", [])) < 2:
        false_positive_risk = "MEDIUM"
    if "model" in str(candidate.get("oracle", "")).lower() or "judgment" in str(candidate.get("oracle", "")).lower():
        false_positive_risk = "HIGH"
        executable = "FAIL"
        reasons.append("model judgment is not an acceptable oracle")

    decision = "EXECUTE" if novelty == "PASS" and executable == "PASS" and delta in {"MEDIUM", "HIGH"} else "KILL"
    if not reasons:
        reasons.append("material procedure and evidence relation differ from the closest registered method")
    return {
        "NOVELTY": novelty,
        "EXECUTABLE": executable,
        "EXPECTED_COVERAGE_DELTA": delta,
        "FALSE_POSITIVE_RISK": false_positive_risk,
        "DECISION": decision,
        "RATIONALE": "; ".join(reasons),
        "NOVELTY_SCORE": novelty_score,
        "CLOSEST_EXISTING_METHODOLOGY": closest,
        "COVERAGE_DELTA_POINTS": points,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--registry-root", type=Path, required=True)
    parser.add_argument("--gap-packet", type=Path, required=True)
    parser.add_argument("--require-execute", action="store_true")
    args = parser.parse_args()
    result = evaluate(load_json(args.candidate), args.registry_root, load_json(args.gap_packet))
    print(json.dumps(result, sort_keys=True, indent=2))
    return int(args.require_execute and result["DECISION"] != "EXECUTE")


if __name__ == "__main__":
    raise SystemExit(main())
