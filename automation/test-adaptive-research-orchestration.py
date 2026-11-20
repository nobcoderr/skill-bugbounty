#!/usr/bin/env python3
"""Network-free regressions for adaptive research orchestration gates."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "ADAPTIVE_RESEARCH_ORCHESTRATION_CASES.json"
VALIDATOR = ROOT / "automation" / "validate-adaptive-research-orchestration.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("adaptive_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def core_wave() -> dict[str, Any]:
    return {
        "wave_id": "wave-1",
        "wave_type": "CORE",
        "core_lanes": ["AUTHORITY_CAPABILITY", "REPRESENTATION_CONSUMER", "STATE_COMPOSITION"],
        "launch_conditions": ["INITIAL_AUTHORIZED_WAVE"],
        "specialists": [],
        "stop_conditions": ["core questions completed"],
    }


def path(status: str = "EXHAUSTED") -> dict[str, Any]:
    return {
        "path_id": "path-1",
        "attack_surface": "request to privileged consumer",
        "hypothesis_family": "authority mismatch",
        "trust_boundary": "caller to privileged consumer",
        "release_component": "release artifact",
        "status": status,
        "evidence_inspected": ["src/consumer.rs:10"],
        "status_reason": "bounded target-native variants completed",
        "unblock_evidence": ["new runtime consumer"] if status == "BLOCKED" else [],
        "material_new_evidence": [],
        "assigned_roles": [] if status in {"BLOCKED", "EXHAUSTED", "KILLED"} else ["authority-scout"],
        "wave_id": "wave-1",
        "root_cause_family": "authority mismatch",
        "status_history": [
            {"status": status, "evidence": "current evidence", "materially_new_evidence": False}
        ],
    }


def registry() -> dict[str, Any]:
    return {
        "audit_id": "audit-1",
        "package_version": "v11",
        "paths": [path()],
        "waves": [core_wave()],
        "coverage_analysis": {
            "material_surfaces": ["authority"],
            "covered_surfaces": ["authority"],
            "coverage_gaps": [],
            "analysis": "all material surfaces covered",
        },
        "convergence_checks": [],
        "adaptive_execution": {
            "triggered": False,
            "provenance_file": "",
            "transcript_sha256": "",
            "spawn_attempts": 0,
            "spawn_successes": 0,
            "spawn_failures": 0,
            "unique_specialist_ids": 0,
            "separate_specialist_inputs": 0,
            "separate_specialist_outputs": 0,
            "root_consumed_specialist_outputs": 0,
            "executed_specialist_count": 0,
            "execution_proven": False,
            "failure_reason": "",
        },
        "termination": {
            "decision": "STOP",
            "reasons": ["all material paths terminal"],
            "unavailable_evidence": [],
            "another_wave_authorized": False,
        },
    }


def candidate() -> dict[str, Any]:
    return {
        "research_path_id": "path-1",
        "discovery_wave": "CORE_A_AUTHORITY",
        "root_cause_family": "authority mismatch",
        "stage": "STRONG_CANDIDATE",
        "verdict": "STRONG",
        "primitive_chain": {
            "primitive": "direct unauthorized protected action",
            "next_security_boundary": "",
            "transitions": [],
            "capability_gain": "protected action",
            "protected_resource_or_action": "victim resource",
            "concrete_security_impact": "cross-boundary modification",
            "chain_status": "NOT_REQUIRED",
            "stop_reason": "primitive directly crosses protected boundary",
        },
        "implementation_escalation": {
            "required": False,
            "components": [],
            "documentation_only": False,
            "version_binding": "not material",
            "blocked_reason": "",
        },
    }


def apply_scenario(name: str) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    reg = registry()
    cand: dict[str, Any] | None = None
    if name == "VALID_CORE_STOP":
        return reg, None
    if name == "EXHAUSTED_REASSIGNMENT":
        reg["paths"][0]["assigned_roles"] = ["repeat-scout"]
    elif name == "VALID_ADAPTIVE_WAVE":
        reg["paths"][0] = path("ACTIVE")
        reg["paths"][0]["path_id"] = "path-gap"
        reg["paths"][0]["wave_id"] = "wave-2"
        reg["coverage_analysis"]["material_surfaces"].append("crypto")
        reg["coverage_analysis"]["coverage_gaps"] = ["crypto"]
        reg["waves"].append(adaptive_wave("path-gap", ["NEW_IMPLEMENTATION_EVIDENCE"]))
        reg["adaptive_execution"] = {
            "triggered": True,
            "provenance_file": "evidence/adaptive-execution.json",
            "transcript_sha256": "a" * 64,
            "spawn_attempts": 1,
            "spawn_successes": 1,
            "spawn_failures": 0,
            "unique_specialist_ids": 1,
            "separate_specialist_inputs": 1,
            "separate_specialist_outputs": 1,
            "root_consumed_specialist_outputs": 1,
            "executed_specialist_count": 1,
            "execution_proven": True,
            "failure_reason": "",
        }
        reg["termination"] = {
            "decision": "CONTINUE",
            "reasons": ["exact crypto implementation not covered"],
            "unavailable_evidence": [],
            "another_wave_authorized": True,
        }
    elif name == "ADAPTIVE_WITHOUT_GAP":
        reg["paths"][0] = path("ACTIVE")
        reg["paths"][0]["path_id"] = "path-gap"
        reg["paths"][0]["wave_id"] = "wave-2"
        reg["waves"].append(adaptive_wave("path-gap", []))
        reg["adaptive_execution"] = {
            "triggered": True,
            "provenance_file": "evidence/adaptive-execution.json",
            "transcript_sha256": "a" * 64,
            "spawn_attempts": 1,
            "spawn_successes": 0,
            "spawn_failures": 1,
            "unique_specialist_ids": 0,
            "separate_specialist_inputs": 0,
            "separate_specialist_outputs": 0,
            "root_consumed_specialist_outputs": 0,
            "executed_specialist_count": 0,
            "execution_proven": False,
            "failure_reason": "no material launch condition",
        }
    elif name == "ADAPTIVE_OVER_CAP":
        reg, _ = apply_scenario("VALID_ADAPTIVE_WAVE")
        assert reg is not None
        base = reg["waves"][1]["specialists"][0]
        reg["waves"][1]["specialists"] = [copy.deepcopy(base) for _ in range(4)]
        reg["adaptive_execution"]["spawn_attempts"] = 4
        reg["adaptive_execution"]["spawn_successes"] = 4
        reg["adaptive_execution"]["unique_specialist_ids"] = 4
        reg["adaptive_execution"]["separate_specialist_inputs"] = 4
        reg["adaptive_execution"]["separate_specialist_outputs"] = 4
        reg["adaptive_execution"]["root_consumed_specialist_outputs"] = 4
        reg["adaptive_execution"]["executed_specialist_count"] = 4
    elif name in {"CONVERGENCE_AS_EVIDENCE", "CONVERGENCE_NO_REDIRECT"}:
        reg["convergence_checks"] = [{
            "root_cause_family": "same-root",
            "candidate_ids": ["C1", "C2", "C3"],
            "retained_candidate_id": "C1",
            "agreement_counted_as_evidence": name == "CONVERGENCE_AS_EVIDENCE",
            "redirected_roles": [] if name == "CONVERGENCE_NO_REDIRECT" else ["B", "C"],
            "neglected_surfaces": [] if name == "CONVERGENCE_NO_REDIRECT" else ["lifecycle"],
        }]
    elif name in {"VALID_MATERIAL_REOPEN", "REOPEN_WITHOUT_NEW_EVIDENCE"}:
        reg["paths"][0] = path("ACTIVE")
        reg["paths"][0]["status_history"] = [
            {"status": "EXHAUSTED", "evidence": "old bounded search", "materially_new_evidence": False},
            {"status": "ACTIVE", "evidence": "new consumer found", "materially_new_evidence": name == "VALID_MATERIAL_REOPEN"},
        ]
        if name == "VALID_MATERIAL_REOPEN":
            reg["paths"][0]["material_new_evidence"] = ["new release consumer"]
    elif name == "CONTINUE_WITHOUT_MATERIAL_REASON":
        reg["termination"] = {
            "decision": "CONTINUE",
            "reasons": ["try again"],
            "unavailable_evidence": [],
            "another_wave_authorized": True,
        }
    elif name in {"VALID_DIRECT_IMPACT", "STRONG_BLOCKED_PRIMITIVE", "DEPENDENCY_DOCS_ONLY", "VALID_EXACT_DEPENDENCY", "FAILED_TRANSITION_VALIDATED"}:
        cand = candidate()
        reg = None
        if name == "STRONG_BLOCKED_PRIMITIVE":
            cand["primitive_chain"]["chain_status"] = "BLOCKED"
            cand["primitive_chain"]["concrete_security_impact"] = ""
        elif name in {"DEPENDENCY_DOCS_ONLY", "VALID_EXACT_DEPENDENCY"}:
            cand["implementation_escalation"] = {
                "required": True,
                "components": [{
                    "kind": "PARSER",
                    "name": "example-parser",
                    "exact_target_version": "" if name == "DEPENDENCY_DOCS_ONLY" else "1.2.3",
                    "source_revision": "" if name == "DEPENDENCY_DOCS_ONLY" else "sha256:abc",
                    "implementation_source_inspected": name == "VALID_EXACT_DEPENDENCY",
                    "implementation_anchors": [] if name == "DEPENDENCY_DOCS_ONLY" else ["src/parser.rs:parse"],
                    "conclusion": "" if name == "DEPENDENCY_DOCS_ONLY" else "target version preserves the observed branch",
                }],
                "documentation_only": name == "DEPENDENCY_DOCS_ONLY",
                "version_binding": "Cargo.lock" if name == "VALID_EXACT_DEPENDENCY" else "",
                "blocked_reason": "source not inspected" if name == "DEPENDENCY_DOCS_ONLY" else "",
            }
        elif name == "FAILED_TRANSITION_VALIDATED":
            cand["primitive_chain"]["chain_status"] = "VALIDATED"
            cand["primitive_chain"]["transitions"] = [{
                "from_capability": "primitive",
                "to_boundary": "protected resource",
                "status": "FAILED",
                "evidence": "negative control rejected transition",
            }]
    else:
        raise ValueError(f"unknown scenario: {name}")
    return reg, cand


def adaptive_wave(path_id: str, conditions: list[str]) -> dict[str, Any]:
    return {
        "wave_id": "wave-2",
        "wave_type": "ADAPTIVE",
        "core_lanes": [],
        "launch_conditions": conditions,
        "specialists": [{
            "role": "crypto-specialist",
            "path_id": path_id,
            "coverage_gap": "exact crypto implementation",
            "bounded_question": "does version-matched verification admit alternate identity",
            "falsifier": "same canonical identity is enforced",
            "required_evidence": "locked version and implementation branch",
            "stop_condition": "exact branch resolved",
        }],
        "stop_conditions": ["coverage gap resolved"],
    }


def main() -> int:
    validator = load_validator()
    suite = json.loads(CASES.read_text(encoding="utf-8"))
    failures = []
    for case in suite["cases"]:
        reg, cand = apply_scenario(case["scenario"])
        errors = []
        if reg is not None:
            errors.extend(validator.validate_registry(reg))
        if cand is not None:
            errors.extend(validator.validate_candidate(cand))
        valid = not errors
        if valid != case["expect_valid"]:
            failures.append(f"{case['id']}: expected={case['expect_valid']} errors={errors}")
        else:
            print(f"PASS {case['id']}")
    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures))
        return 1
    print(f"ADAPTIVE_RESEARCH_REGRESSIONS=PASS cases={len(suite['cases'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
