#!/usr/bin/env python3
"""Validate V13 registry integrity without mutating it."""

from __future__ import annotations

import argparse
import json
import tarfile
from pathlib import Path
from typing import Any

from _v13lib import (
    FORBIDDEN_EXECUTOR_INPUT_FRAGMENTS,
    ensure_hex_digest,
    file_digest,
    load_json,
    load_jsonl,
    object_digest,
)


REQUIRED_DEFINITION_FIELDS = {
    "record_type",
    "methodology_id",
    "name",
    "origin",
    "status",
    "target_gap_ids",
    "security_reasoning_principle",
    "core_question",
    "procedure_graph",
    "reasoning_signature",
    "required_inputs",
    "expected_signal",
    "negative_signal",
    "oracle",
    "falsification_strategy",
    "termination_condition",
    "overlaps_existing_methodologies",
    "why_this_is_materially_distinct",
    "potential_false_positive_modes",
    "definition_digest",
    "definition_frozen",
}

REQUIRED_CAPSULE_INPUTS = {
    "factual_target_brief",
    "architecture_map",
    "methodology_definition",
    "authorized_source_snapshot",
    "scope_safety_card",
}


def validate_ledger_chain(records: list[dict[str, Any]], ledger_name: str) -> None:
    if not records or records[0].get("record_type") != "LEDGER_INITIALIZED":
        raise ValueError(f"{ledger_name}: missing initialization record")
    previous = None
    for expected_sequence, record in enumerate(records):
        if record.get("sequence") != expected_sequence:
            raise ValueError(f"{ledger_name}: non-contiguous sequence")
        if record.get("previous_record_digest") != previous:
            raise ValueError(f"{ledger_name}: previous-record digest mismatch")
        ensure_hex_digest(record.get("record_digest"), "record_digest")
        actual = object_digest(record, {"record_digest"})
        if actual != record["record_digest"]:
            raise ValueError(f"{ledger_name}: record digest mismatch at sequence {expected_sequence}")
        previous = record["record_digest"]


def validate_gap_packet(packet: dict[str, Any]) -> None:
    if packet.get("record_type") != "COVERAGE_GAP_PACKET":
        raise ValueError("unexpected coverage gap packet type")
    ensure_hex_digest(packet.get("audit_snapshot_digest"), "audit_snapshot_digest")
    gaps = packet.get("gaps", [])
    ids = [gap.get("gap_id") for gap in gaps]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate coverage gap ID")
    material_count = 0
    for gap in gaps:
        basis = gap.get("factual_basis", [])
        for anchor in basis:
            ensure_hex_digest(anchor.get("artifact_digest"), "artifact_digest")
        is_material = gap.get("status") == "MATERIAL"
        if is_material:
            if len(basis) < 2:
                raise ValueError("material gap lacks two factual anchors")
            if gap.get("coverage_dimension") not in {"UNSEEN", "PARTIAL"}:
                raise ValueError("material gap is already fully covered")
            if gap.get("evidence_availability") != "LOCAL":
                raise ValueError("blocked evidence cannot be a material executable gap")
            material_count += 1
    if packet.get("coverage_gap_count") != material_count:
        raise ValueError("coverage_gap_count is not derived from material records")


def resolve_from(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def validate_baseline(lab_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    lock = load_json(lab_root / "BASELINE_LOCK.json")
    archive = resolve_from(lab_root, lock["baseline_archive"]["path"])
    status_file = resolve_from(lab_root, lock["engineering_status"]["path"])
    if file_digest(archive) != lock["baseline_archive"]["sha256"]:
        raise ValueError("frozen V12 archive hash mismatch")
    if file_digest(status_file) != lock["engineering_status"]["sha256"]:
        raise ValueError("frozen V12 engineering status hash mismatch")

    baseline = load_json(lab_root / "registry" / "v12-methodology-baseline.json")
    methods = baseline.get("methods", [])
    if baseline.get("archive_sha256") != lock["baseline_archive"]["sha256"]:
        raise ValueError("method baseline references a different V12 archive")
    if baseline.get("methodology_count") != len(methods):
        raise ValueError("V12 methodology_count does not match records")
    ids = [item.get("methodology_id") for item in methods]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate V12 methodology id")

    with tarfile.open(archive, "r:gz") as bundle:
        members = {member.name: member for member in bundle.getmembers()}
        for method in methods:
            reference = method["source_reference"]
            if reference not in members:
                raise ValueError(f"V12 source reference missing: {reference}")
            handle = bundle.extractfile(members[reference])
            if handle is None:
                raise ValueError(f"cannot read V12 source reference: {reference}")
            import hashlib

            actual = hashlib.sha256(handle.read()).hexdigest()
            if actual != method["source_sha256"]:
                raise ValueError(f"V12 source reference hash mismatch: {reference}")
    return lock, baseline


def validate_definition(record: dict[str, Any]) -> None:
    missing = REQUIRED_DEFINITION_FIELDS - set(record)
    if missing:
        raise ValueError(f"methodology definition missing fields: {sorted(missing)}")
    if record["record_type"] != "METHODOLOGY_DEFINITION":
        raise ValueError("unexpected definition record type")
    if record["origin"] != "GENERATED":
        raise ValueError("generated definition ledger may not redefine V12 methods")
    if record["status"] not in {"EXPERIMENTAL", "KILLED"}:
        raise ValueError("definition status is not an immutable definition state")
    if record["definition_frozen"] is not True:
        raise ValueError("methodology definition is not frozen")
    ensure_hex_digest(record["definition_digest"], "definition_digest")
    actual = object_digest(record, {"definition_digest", "sequence", "previous_record_digest", "record_digest"})
    if actual != record["definition_digest"]:
        raise ValueError(f"definition digest mismatch: {record['methodology_id']}")
    graph = record["procedure_graph"]
    nodes = graph.get("nodes", [])
    ids = {node.get("step_id") for node in nodes}
    if len(ids) != len(nodes) or None in ids:
        raise ValueError("procedure graph step IDs must be unique")
    for node in nodes:
        if not set(node.get("depends_on", [])).issubset(ids):
            raise ValueError("procedure graph dependency references an unknown step")
        if node.get("step_id") in node.get("depends_on", []):
            raise ValueError("procedure graph has a self dependency")


def validate_execution(record: dict[str, Any], known_methods: set[str]) -> None:
    methodology_id = record.get("methodology_id")
    if methodology_id not in known_methods:
        raise ValueError(f"execution references unknown methodology: {methodology_id}")
    if record.get("registry_mutation") is not False:
        raise ValueError("executor attempted registry mutation")
    if record.get("forbidden_inputs_present") is not False:
        raise ValueError("executor declared forbidden input")
    allowlist = {str(item) for item in record.get("capsule_allowlist", [])}
    if not REQUIRED_CAPSULE_INPUTS.issubset(allowlist):
        raise ValueError("executor capsule is missing mandatory isolated inputs")
    lowered = " ".join(allowlist).lower()
    if any(fragment in lowered for fragment in FORBIDDEN_EXECUTOR_INPUT_FRAGMENTS):
        raise ValueError("executor capsule contains forbidden cross-method context")
    if record.get("child_context", {}).get("fresh_context") is not True:
        raise ValueError("executor context was not fresh")

    atoms = record.get("new_material_evidence", [])
    if record.get("new_material_evidence_count") != len(atoms):
        raise ValueError("new_material_evidence_count mismatch")
    identities = [atom.get("semantic_identity") for atom in atoms]
    if len(identities) != len(set(identities)):
        raise ValueError("duplicate semantic evidence identity in one execution")
    for atom in atoms:
        ensure_hex_digest(atom.get("artifact_sha256"), "artifact_sha256")
        ensure_hex_digest(atom.get("snapshot_digest"), "snapshot_digest")
        if atom.get("oracle_result") != "PASS":
            raise ValueError("non-passing atom cannot enter new material evidence")
    expected_result = "MATERIAL_GAIN" if atoms else "NO_MATERIAL_GAIN"
    if record.get("methodology_execution_result") not in {expected_result, "EXECUTION_DEFERRED"}:
        raise ValueError("execution result disagrees with material evidence count")
    for field in (
        "source_snapshot_digest",
        "input_capsule_digest",
        "output_digest",
        "transcript_digest",
        "root_receipt_digest",
    ):
        ensure_hex_digest(record.get(field), field)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab-root", type=Path, required=True)
    args = parser.parse_args()
    lab_root = args.lab_root.resolve()
    lock, baseline = validate_baseline(lab_root)
    registry = lab_root / "registry"
    manifest = load_json(registry / "METHODOLOGY_REGISTRY.json")

    for relative in (
        manifest["definition_schema"],
        manifest["coverage_gap_schema"],
        manifest["execution_schema"],
        manifest["v12_baseline_definitions"],
        manifest["generated_definitions_ledger"],
        manifest["execution_ledger"],
        manifest["promotion_ledger"],
    ):
        if not resolve_from(registry, relative).exists():
            raise ValueError(f"registry component missing: {relative}")

    definition_records = load_jsonl(registry / manifest["generated_definitions_ledger"])
    validate_ledger_chain(definition_records, "generated-methodology-definitions")
    definitions = [item for item in definition_records if item.get("record_type") == "METHODOLOGY_DEFINITION"]
    for definition in definitions:
        validate_definition(definition)
    generated_ids = [item["methodology_id"] for item in definitions]
    if len(generated_ids) != len(set(generated_ids)):
        raise ValueError("duplicate generated methodology definition")

    known_methods = {item["methodology_id"] for item in baseline["methods"]} | set(generated_ids)
    execution_records = load_jsonl(registry / manifest["execution_ledger"])
    validate_ledger_chain(execution_records, "methodology-executions")
    executions = [item for item in execution_records if item.get("record_type") == "METHODOLOGY_EXECUTION"]
    execution_ids: set[str] = set()
    for execution in executions:
        if execution.get("execution_id") in execution_ids:
            raise ValueError("duplicate execution ID")
        execution_ids.add(execution.get("execution_id"))
        validate_execution(execution, known_methods)

    promotion_records = load_jsonl(registry / manifest["promotion_ledger"])
    validate_ledger_chain(promotion_records, "methodology-promotion-decisions")
    for decision in promotion_records:
        if decision.get("record_type") == "METHODOLOGY_PROMOTION_DECISION":
            if decision.get("methodology_id") not in known_methods:
                raise ValueError("promotion references unknown methodology")
            if decision.get("to_status") == "PROMOTED":
                if decision.get("human_approved") is not True:
                    raise ValueError("PROMOTED requires explicit human approval")
                ensure_hex_digest(decision.get("decision_digest"), "decision_digest")

    result = {
        "REGISTRY_VALID": True,
        "V12_BASELINE_HASH_VALID": True,
        "V12_METHOD_SOURCE_HASHES_VALID": True,
        "V12_METHOD_COUNT": len(baseline["methods"]),
        "GENERATED_DEFINITION_COUNT": len(definitions),
        "EXECUTION_COUNT": len(executions),
        "PROMOTION_DECISION_COUNT": sum(item.get("record_type") == "METHODOLOGY_PROMOTION_DECISION" for item in promotion_records),
        "DEFAULT_STACK_MUTATION": manifest["default_stack_mutation"],
        "BLIND_BENCHMARK_STATUS": manifest["blind_benchmark_status"],
        "V12_ARCHIVE_SHA256": lock["baseline_archive"]["sha256"],
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
