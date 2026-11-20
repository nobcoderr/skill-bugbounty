#!/usr/bin/env python3
"""Small, network-free helpers shared by the V13 methodology lab."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


FORBIDDEN_EXECUTOR_INPUT_FRAGMENTS = {
    "candidate_conclusion",
    "ground_truth",
    "patch_identity",
    "sibling_output",
    "other_methodology",
    "expected_bug",
}

OPERATOR_ALIASES = {
    "find": "locate",
    "identify": "locate",
    "discover": "locate",
    "follow": "trace",
    "traverse": "trace",
    "walk": "trace",
    "list": "enumerate",
    "inventory": "enumerate",
    "diff": "compare",
    "contrast": "compare",
    "check": "verify",
    "validate": "verify",
    "prove": "verify",
    "exercise": "test",
    "simulate": "model",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(item, dict):
                raise ValueError(f"{path}:{line_number}: JSONL record must be an object")
            records.append(item)
    return records


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def object_digest(value: Any, excluded: Iterable[str] = ()) -> str:
    if isinstance(value, dict):
        clean = {key: val for key, val in value.items() if key not in set(excluded)}
    else:
        clean = value
    return hashlib.sha256(canonical_bytes(clean)).hexdigest()


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_operator(operator: str) -> str:
    pieces = operator.lower().replace("-", "_").split("_")
    return "_".join(OPERATOR_ALIASES.get(piece, piece) for piece in pieces if piece)


def jaccard(left: Iterable[str], right: Iterable[str]) -> float:
    a, b = set(left), set(right)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def signature_values(method: dict[str, Any]) -> list[str]:
    signature = method.get("reasoning_signature", {})
    if isinstance(signature, dict):
        order = (
            "start_point",
            "traversal_direction",
            "temporal_model",
            "authority_model",
            "representation_model",
            "failure_model",
            "composition_arity",
            "oracle_class",
        )
        return [str(signature.get(key, "")) for key in order]
    if isinstance(signature, list):
        return [str(value) for value in signature]
    return []


def method_operators(method: dict[str, Any]) -> list[str]:
    if isinstance(method.get("procedure_operators"), list):
        return [normalize_operator(str(item)) for item in method["procedure_operators"]]
    graph = method.get("procedure_graph", {})
    nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    return [normalize_operator(str(node.get("operator", ""))) for node in nodes if isinstance(node, dict)]


def method_oracle(method: dict[str, Any]) -> str:
    graph = method.get("procedure_graph", {})
    if isinstance(graph, dict) and graph.get("oracle_class"):
        return str(graph["oracle_class"])
    if method.get("oracle_class"):
        return str(method["oracle_class"])
    signature = signature_values(method)
    return signature[-1] if signature else ""


def load_all_methods(registry_root: Path) -> list[dict[str, Any]]:
    baseline = load_json(registry_root / "v12-methodology-baseline.json")
    methods = list(baseline.get("methods", []))
    for record in load_jsonl(registry_root / "generated-methodology-definitions.jsonl"):
        if record.get("record_type") == "METHODOLOGY_DEFINITION":
            methods.append(record)
    return methods


def classify_coverage_delta(points: int) -> str:
    if points >= 6:
        return "HIGH"
    if points >= 3:
        return "MEDIUM"
    if points >= 1:
        return "LOW"
    return "NONE"


def ensure_hex_digest(value: Any, field: str) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise ValueError(f"{field} must be a lowercase SHA-256 hex digest")


def material_gap_ids(packet: dict[str, Any]) -> set[str]:
    return {
        str(gap["gap_id"])
        for gap in packet.get("gaps", [])
        if gap.get("status") == "MATERIAL"
        and gap.get("coverage_dimension") in {"UNSEEN", "PARTIAL"}
        and gap.get("evidence_availability") == "LOCAL"
        and len(gap.get("factual_basis", [])) >= 2
    }

