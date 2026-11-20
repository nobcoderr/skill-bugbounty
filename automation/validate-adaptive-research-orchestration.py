#!/usr/bin/env python3
"""Validate adaptive multi-agent research registries and candidate gates.

Network-free and read-only. This validator checks orchestration invariants that
JSON Schema alone cannot conveniently express.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PATH_STATUSES = {"ACTIVE", "PROMISING", "BLOCKED", "EXHAUSTED", "KILLED", "VALIDATED"}
TERMINAL_DISCOVERY_STATUSES = {"BLOCKED", "EXHAUSTED", "KILLED"}
REOPEN_SOURCE_STATUSES = {"BLOCKED", "EXHAUSTED", "KILLED"}
REOPEN_TARGET_STATUSES = {"ACTIVE", "PROMISING", "VALIDATED"}
CORE_LANES = {"AUTHORITY_CAPABILITY", "REPRESENTATION_CONSUMER", "STATE_COMPOSITION"}
MATERIAL_LAUNCH_CONDITIONS = {
    "UNCOVERED_ATTACK_SURFACE",
    "NEW_TRUST_BOUNDARY",
    "NEW_IMPLEMENTATION_EVIDENCE",
    "UNTESTED_DOWNSTREAM_TRANSITION",
}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "audit_id",
        "package_version",
        "paths",
        "waves",
        "coverage_analysis",
        "convergence_checks",
        "adaptive_execution",
        "termination",
    }
    missing = sorted(required - set(data))
    if missing:
        return [f"REGISTRY_MISSING:{','.join(missing)}"]

    paths = data.get("paths")
    waves = data.get("waves")
    if not isinstance(paths, list) or not isinstance(waves, list) or not waves:
        return ["REGISTRY_PATHS_OR_WAVES_INVALID"]

    path_by_id: dict[str, dict[str, Any]] = {}
    for index, path in enumerate(paths):
        if not isinstance(path, dict):
            errors.append(f"PATH_NOT_OBJECT:{index}")
            continue
        path_id = path.get("path_id")
        if not _nonempty(path_id):
            errors.append(f"PATH_ID_MISSING:{index}")
            continue
        if path_id in path_by_id:
            errors.append(f"PATH_ID_DUPLICATE:{path_id}")
        path_by_id[path_id] = path
        status = path.get("status")
        if status not in PATH_STATUSES:
            errors.append(f"PATH_STATUS_INVALID:{path_id}")
        if status in TERMINAL_DISCOVERY_STATUSES and path.get("assigned_roles"):
            errors.append(f"TERMINAL_PATH_ASSIGNED:{path_id}")
        if status in TERMINAL_DISCOVERY_STATUSES and not _nonempty(path.get("status_reason")):
            errors.append(f"TERMINAL_PATH_REASON_MISSING:{path_id}")
        if status == "BLOCKED" and not path.get("unblock_evidence"):
            errors.append(f"BLOCKED_UNBLOCK_EVIDENCE_MISSING:{path_id}")

        history = path.get("status_history")
        if not isinstance(history, list) or not history:
            errors.append(f"PATH_HISTORY_MISSING:{path_id}")
            continue
        for previous, current in zip(history, history[1:]):
            if not isinstance(previous, dict) or not isinstance(current, dict):
                errors.append(f"PATH_HISTORY_INVALID:{path_id}")
                continue
            if previous.get("status") in REOPEN_SOURCE_STATUSES and current.get("status") in REOPEN_TARGET_STATUSES:
                if not current.get("materially_new_evidence") or not path.get("material_new_evidence"):
                    errors.append(f"PATH_REOPEN_WITHOUT_NEW_EVIDENCE:{path_id}")
        if isinstance(history[-1], dict) and history[-1].get("status") != status:
            errors.append(f"PATH_HISTORY_STATUS_MISMATCH:{path_id}")

    wave_ids: set[str] = set()
    core_waves = 0
    adaptive_waves = 0
    for index, wave in enumerate(waves):
        if not isinstance(wave, dict):
            errors.append(f"WAVE_NOT_OBJECT:{index}")
            continue
        wave_id = wave.get("wave_id")
        if not _nonempty(wave_id):
            errors.append(f"WAVE_ID_MISSING:{index}")
            continue
        if wave_id in wave_ids:
            errors.append(f"WAVE_ID_DUPLICATE:{wave_id}")
        wave_ids.add(wave_id)
        wave_type = wave.get("wave_type")
        conditions = set(wave.get("launch_conditions") or [])
        specialists = wave.get("specialists") or []
        if wave_type == "CORE":
            core_waves += 1
            if set(wave.get("core_lanes") or []) != CORE_LANES:
                errors.append(f"CORE_LANES_INCOMPLETE:{wave_id}")
            if "INITIAL_AUTHORIZED_WAVE" not in conditions:
                errors.append(f"CORE_WAVE_AUTHORIZATION_MISSING:{wave_id}")
        elif wave_type == "ADAPTIVE":
            adaptive_waves += 1
            if not conditions.intersection(MATERIAL_LAUNCH_CONDITIONS):
                errors.append(f"ADAPTIVE_WAVE_NO_MATERIAL_CONDITION:{wave_id}")
            if len(specialists) > 3:
                errors.append(f"ADAPTIVE_SPECIALIST_CAP_EXCEEDED:{wave_id}")
            if not specialists:
                errors.append(f"ADAPTIVE_WAVE_EMPTY:{wave_id}")
            for specialist in specialists:
                path_id = specialist.get("path_id") if isinstance(specialist, dict) else None
                path = path_by_id.get(path_id)
                if path is None:
                    errors.append(f"SPECIALIST_UNKNOWN_PATH:{wave_id}:{path_id}")
                elif path.get("status") in TERMINAL_DISCOVERY_STATUSES and not path.get("material_new_evidence"):
                    errors.append(f"SPECIALIST_TERMINAL_PATH:{wave_id}:{path_id}")
        else:
            errors.append(f"WAVE_TYPE_INVALID:{wave_id}")

    if core_waves != 1:
        errors.append("CORE_WAVE_COUNT_INVALID")

    execution = data.get("adaptive_execution") or {}
    planned_specialists = sum(
        len(wave.get("specialists") or [])
        for wave in waves
        if isinstance(wave, dict) and wave.get("wave_type") == "ADAPTIVE"
    )
    numeric_fields = (
        "spawn_attempts",
        "spawn_successes",
        "spawn_failures",
        "unique_specialist_ids",
        "separate_specialist_inputs",
        "separate_specialist_outputs",
        "root_consumed_specialist_outputs",
        "executed_specialist_count",
    )
    if not isinstance(execution, dict):
        errors.append("ADAPTIVE_EXECUTION_INVALID")
        execution = {}
    for field in numeric_fields:
        value = execution.get(field)
        if not isinstance(value, int) or value < 0:
            errors.append(f"ADAPTIVE_EXECUTION_FIELD_INVALID:{field}")

    if adaptive_waves:
        if execution.get("triggered") is not True:
            errors.append("ADAPTIVE_WAVE_WITHOUT_EXECUTION_TRIGGER")
        if not _nonempty(execution.get("provenance_file")):
            errors.append("ADAPTIVE_EXECUTION_PROVENANCE_MISSING")
        transcript_sha = execution.get("transcript_sha256")
        if not isinstance(transcript_sha, str) or len(transcript_sha) != 64:
            errors.append("ADAPTIVE_EXECUTION_TRANSCRIPT_HASH_MISSING")
    else:
        if execution.get("triggered") is not False:
            errors.append("CORE_ONLY_EXECUTION_TRIGGERED")
        if any(execution.get(field, 0) for field in numeric_fields):
            errors.append("CORE_ONLY_EXECUTION_NONZERO")
        if execution.get("execution_proven") is not False:
            errors.append("CORE_ONLY_EXECUTION_PROVEN")

    attempts = execution.get("spawn_attempts", 0)
    successes = execution.get("spawn_successes", 0)
    failures = execution.get("spawn_failures", 0)
    unique_ids = execution.get("unique_specialist_ids", 0)
    inputs = execution.get("separate_specialist_inputs", 0)
    outputs = execution.get("separate_specialist_outputs", 0)
    consumed = execution.get("root_consumed_specialist_outputs", 0)
    executed = execution.get("executed_specialist_count", 0)
    if isinstance(attempts, int) and isinstance(successes, int) and successes > attempts:
        errors.append("ADAPTIVE_SUCCESS_EXCEEDS_ATTEMPTS")
    if isinstance(successes, int) and isinstance(executed, int) and executed > successes:
        errors.append("ADAPTIVE_EXECUTED_EXCEEDS_SUCCESS")
    if isinstance(successes, int):
        for field, value in (
            ("unique_specialist_ids", unique_ids),
            ("separate_specialist_inputs", inputs),
            ("separate_specialist_outputs", outputs),
            ("root_consumed_specialist_outputs", consumed),
        ):
            if isinstance(value, int) and value > successes:
                errors.append(f"ADAPTIVE_PROVENANCE_COUNT_EXCEEDS_SUCCESS:{field}")

    if execution.get("execution_proven") is True:
        if not adaptive_waves:
            errors.append("ADAPTIVE_EXECUTION_PROVEN_WITHOUT_WAVE")
        proof_counts = (attempts, successes, failures, unique_ids, inputs, outputs, consumed, executed)
        if not all(isinstance(value, int) for value in proof_counts) or (
            attempts < 1
            or successes != attempts
            or failures != 0
            or unique_ids != successes
            or inputs != successes
            or outputs != successes
            or consumed != successes
            or executed != successes
            or successes != planned_specialists
        ):
            errors.append("ADAPTIVE_EXECUTION_PROOF_INCONSISTENT")
    elif adaptive_waves and not _nonempty(execution.get("failure_reason")):
        errors.append("ADAPTIVE_EXECUTION_FAILURE_REASON_MISSING")

    for path_id, path in path_by_id.items():
        if path.get("wave_id") not in wave_ids:
            errors.append(f"PATH_UNKNOWN_WAVE:{path_id}")

    for index, check in enumerate(data.get("convergence_checks") or []):
        if not isinstance(check, dict):
            errors.append(f"CONVERGENCE_NOT_OBJECT:{index}")
            continue
        candidates = check.get("candidate_ids") or []
        retained = check.get("retained_candidate_id")
        if check.get("agreement_counted_as_evidence") is not False:
            errors.append(f"CONVERGENCE_AGREEMENT_AS_EVIDENCE:{index}")
        if retained not in candidates:
            errors.append(f"CONVERGENCE_RETAINED_NOT_MEMBER:{index}")
        if len(candidates) >= 2 and not (check.get("redirected_roles") or check.get("neglected_surfaces")):
            errors.append(f"CONVERGENCE_NO_REDIRECTION:{index}")

    coverage = data.get("coverage_analysis") or {}
    gaps = set(coverage.get("coverage_gaps") or [])
    material = set(coverage.get("material_surfaces") or [])
    covered = set(coverage.get("covered_surfaces") or [])
    if not covered.issubset(material):
        errors.append("COVERED_SURFACE_NOT_MATERIAL")
    if not gaps.issubset(material):
        errors.append("COVERAGE_GAP_NOT_MATERIAL")

    termination = data.get("termination") or {}
    decision = termination.get("decision")
    another_wave = termination.get("another_wave_authorized")
    if decision == "STOP" and another_wave is not False:
        errors.append("STOP_WITH_ANOTHER_WAVE")
    if decision == "CONTINUE":
        adaptive_conditions = {
            condition
            for wave in waves
            if isinstance(wave, dict) and wave.get("wave_type") == "ADAPTIVE"
            for condition in (wave.get("launch_conditions") or [])
        }
        if another_wave is not True or not (gaps or adaptive_conditions.intersection(MATERIAL_LAUNCH_CONDITIONS)):
            errors.append("CONTINUE_WITHOUT_MATERIAL_REASON")
    elif decision != "STOP":
        errors.append("TERMINATION_DECISION_INVALID")

    return errors


def validate_candidate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("research_path_id", "discovery_wave", "root_cause_family", "primitive_chain", "implementation_escalation"):
        if field not in data:
            errors.append(f"CANDIDATE_MISSING:{field}")
    if errors:
        return errors

    chain = data.get("primitive_chain") or {}
    chain_status = chain.get("chain_status")
    verdict = data.get("verdict", "UNRATED")
    stage = data.get("stage", "CODE_DERIVED_HYPOTHESIS")
    bounty_grade = verdict == "STRONG" or stage == "STRONG_CANDIDATE"
    if bounty_grade:
        if chain_status not in {"VALIDATED", "NOT_REQUIRED"}:
            errors.append("BOUNTY_GRADE_WITHOUT_VALIDATED_CHAIN")
        if not _nonempty(chain.get("concrete_security_impact")):
            errors.append("BOUNTY_GRADE_WITHOUT_CONCRETE_IMPACT")
    if chain_status == "VALIDATED":
        for index, transition in enumerate(chain.get("transitions") or []):
            if transition.get("status") != "PROVEN" or not _nonempty(transition.get("evidence")):
                errors.append(f"VALIDATED_CHAIN_UNPROVEN_TRANSITION:{index}")
    if chain_status in {"BLOCKED", "EXHAUSTED", "KILLED"} and not _nonempty(chain.get("stop_reason")):
        errors.append("TERMINAL_CHAIN_STOP_REASON_MISSING")

    escalation = data.get("implementation_escalation") or {}
    if escalation.get("required"):
        components = escalation.get("components") or []
        if escalation.get("documentation_only"):
            errors.append("REQUIRED_IMPLEMENTATION_DOCUMENTATION_ONLY")
        if not components:
            errors.append("REQUIRED_IMPLEMENTATION_COMPONENT_MISSING")
        for index, component in enumerate(components):
            if not _nonempty(component.get("exact_target_version")):
                errors.append(f"IMPLEMENTATION_VERSION_MISSING:{index}")
            if not _nonempty(component.get("source_revision")):
                errors.append(f"IMPLEMENTATION_REVISION_MISSING:{index}")
            if component.get("implementation_source_inspected") is not True:
                errors.append(f"IMPLEMENTATION_SOURCE_NOT_INSPECTED:{index}")
            if not component.get("implementation_anchors"):
                errors.append(f"IMPLEMENTATION_ANCHOR_MISSING:{index}")
            if not _nonempty(component.get("conclusion")):
                errors.append(f"IMPLEMENTATION_CONCLUSION_MISSING:{index}")
        if bounty_grade and errors:
            errors.append("BOUNTY_GRADE_WITH_UNPROVEN_IMPLEMENTATION")

    return errors


def load_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--require-adaptive-execution", action="store_true")
    args = parser.parse_args()
    if args.registry is None and args.candidate is None:
        parser.error("provide --registry and/or --candidate")

    errors: list[str] = []
    if args.registry is not None:
        registry = load_object(args.registry)
        errors.extend(validate_registry(registry))
        if args.require_adaptive_execution:
            if not (registry.get("adaptive_execution") or {}).get("execution_proven"):
                errors.append("ADAPTIVE_EXECUTION_REQUIRED_NOT_PROVEN")
    if args.candidate is not None:
        errors.extend(validate_candidate(load_object(args.candidate)))

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("ADAPTIVE_RESEARCH_ORCHESTRATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
