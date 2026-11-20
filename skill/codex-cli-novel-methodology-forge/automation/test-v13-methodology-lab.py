#!/usr/bin/env python3
"""Deterministic, network-free engineering tests for V13-METHODOLOGY-LAB."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path


AUTOMATION = Path(__file__).resolve().parent
SKILL_ROOT = AUTOMATION.parent
LAB_ROOT = SKILL_ROOT.parent
REGISTRY = LAB_ROOT / "registry"
FIXTURES = SKILL_ROOT / "fixtures"
sys.path.insert(0, str(AUTOMATION))

from _v13lib import file_digest, load_json, material_gap_ids, object_digest  # noqa: E402


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NOVELTY = load_module("v13_novelty", AUTOMATION / "validate-methodology-novelty.py")
TERMINATION = load_module("v13_termination", AUTOMATION / "validate-forge-termination.py")
SCORING = load_module("v13_scoring", AUTOMATION / "score-methodology-value.py")
REGISTRY_VALIDATOR = load_module("v13_registry", AUTOMATION / "validate-methodology-registry.py")
FIXTURE_EXECUTOR = load_module("v13_fixture_executor", AUTOMATION / "run-isolated-fixture-executor.py")


def assert_json_and_toml_parse() -> None:
    for path in LAB_ROOT.rglob("*.json"):
        load_json(path)
    for path in SKILL_ROOT.rglob("*.toml"):
        with path.open("rb") as handle:
            tomllib.load(handle)
    with (SKILL_ROOT / "agents" / "openai.yaml").open("r", encoding="utf-8") as handle:
        text = handle.read()
    assert "allow_implicit_invocation: false" in text


def assert_no_network_primitives() -> None:
    forbidden = ("requests.", "urllib.request", "urlopen(", "socket.connect", "http.client")
    for path in AUTOMATION.glob("*.py"):
        if path.resolve() == Path(__file__).resolve():
            continue
        source = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in source, f"network primitive {needle!r} in {path.name}"


def assert_coverage_packets() -> None:
    material = load_json(FIXTURES / "coverage-material.json")
    none = load_json(FIXTURES / "coverage-none.json")
    blocked = load_json(FIXTURES / "coverage-blocked.json")
    REGISTRY_VALIDATOR.validate_gap_packet(material)
    REGISTRY_VALIDATOR.validate_gap_packet(none)
    REGISTRY_VALIDATOR.validate_gap_packet(blocked)
    assert material["coverage_gap_count"] == len(material_gap_ids(material)) == 1
    assert none["coverage_gap_count"] == len(material_gap_ids(none)) == 0
    assert blocked["coverage_gap_count"] == len(material_gap_ids(blocked)) == 0


def assert_novelty_gate() -> None:
    gap = load_json(FIXTURES / "coverage-material.json")
    distinct = load_json(FIXTURES / "methodology-distinct.json")
    renamed = load_json(FIXTURES / "methodology-renamed-duplicate.json")
    result = NOVELTY.evaluate(distinct, REGISTRY, gap)
    assert result["DECISION"] == "EXECUTE", result
    assert result["EXPECTED_COVERAGE_DELTA"] in {"MEDIUM", "HIGH"}
    result = NOVELTY.evaluate(renamed, REGISTRY, gap)
    assert result["DECISION"] == "KILL", result
    assert result["CLOSEST_EXISTING_METHODOLOGY"]["methodology_id"] == "METH-V12-STATE-MACHINE"
    blocked = NOVELTY.evaluate(distinct, REGISTRY, load_json(FIXTURES / "coverage-blocked.json"))
    assert blocked["DECISION"] == "KILL" and blocked["EXECUTABLE"] == "FAIL"


def assert_definition_integrity() -> None:
    definition = load_json(FIXTURES / "methodology-distinct.json")
    definition.update({
        "record_type": "METHODOLOGY_DEFINITION",
        "origin": "GENERATED",
        "status": "EXPERIMENTAL",
        "definition_frozen": True,
    })
    definition["definition_digest"] = object_digest(definition, {"definition_digest"})
    REGISTRY_VALIDATOR.validate_definition(definition)
    tampered = dict(definition)
    tampered["core_question"] = tampered["core_question"] + " tampered"
    try:
        REGISTRY_VALIDATOR.validate_definition(tampered)
    except ValueError as exc:
        assert "digest mismatch" in str(exc)
    else:
        raise AssertionError("tampered methodology definition was accepted")


def assert_termination_gate() -> None:
    cases = load_json(FIXTURES / "termination-cases.json")
    for case in cases["cases"]:
        result = TERMINATION.decide(case["state"])
        assert result["STATE_VALID"] is True, (case["name"], result)
        assert result["NEXT_ACTION"] == case["expected"], (case["name"], result)
    for case in cases["invalid_cases"]:
        result = TERMINATION.decide(case["state"])
        assert result["STATE_VALID"] is False, (case["name"], result)


def execute_fixture(target_name: str, child: str, mode: str = "DISCOVERY") -> dict:
    return FIXTURE_EXECUTOR.execute(
        load_json(FIXTURES / "methodology-distinct.json"),
        load_json(FIXTURES / "coverage-material.json"),
        load_json(FIXTURES / "hidden-family" / target_name),
        child,
        mode,
    )


def assert_hidden_family_and_patched_control() -> tuple[list[dict], int, int]:
    hidden = execute_fixture("target.json", "development_child_1")
    reproduced = execute_fixture("target.json", "development_child_2", "REPRODUCTION")
    patched = execute_fixture("patched-control.json", "patched_child", "PATCHED_CONTROL")
    assert hidden["new_material_evidence_count"] == 1
    assert hidden["new_candidates"] == []
    assert reproduced["new_material_evidence"][0]["semantic_identity"] == hidden["new_material_evidence"][0]["semantic_identity"]
    assert patched["new_material_evidence_count"] == 0
    assert patched["methodology_execution_result"] == "NO_MATERIAL_GAIN"
    allowed_methods = {"METH-2026-AUTHORITY-EPOCH-LINEAGE"}
    for result in (hidden, reproduced, patched):
        REGISTRY_VALIDATOR.validate_execution(result, allowed_methods)
    return [hidden, reproduced], 1, 0


def assert_promotion_gate(base_runs: list[dict]) -> None:
    method_id = "METH-2026-AUTHORITY-EPOCH-LINEAGE"
    blind_a = execute_fixture("target.json", "blind_child_a", "BLIND")
    blind_a["target_family"] = "family_a"
    blind_a["blind_seed_digest"] = "1" * 64
    blind_b = execute_fixture("target.json", "blind_child_b", "BLIND")
    blind_b["target_family"] = "family_b"
    blind_b["blind_seed_digest"] = "2" * 64
    base_runs[0]["blind_seed_digest"] = "3" * 64
    base_runs[1]["blind_seed_digest"] = "4" * 64
    runs = base_runs + [blind_a, blind_b]
    events = [
        {"record_type": "METHODOLOGY_VALIDATION_EVENT", "methodology_id": method_id, "full_pipeline_pass": True, "duplicate_or_known": False, "report_ready_outcome": "VALID"},
        {"record_type": "METHODOLOGY_BLIND_GENERALIZATION", "methodology_id": method_id, "result": "PASS", "sealed_before_execution": True, "curator_independent": True, "answer_unsealed_after_output": True, "ground_truth_leakage": 0, "curator_manifest_digest": "c" * 64},
        {"record_type": "METHODOLOGY_REGRESSION_RESULT", "methodology_id": method_id, "exact_root_regression": 0, "patched_control_false_positive": 0, "ground_truth_leakage": 0, "runaway": 0},
        {"record_type": "METHODOLOGY_PROMOTION_DECISION", "methodology_id": method_id, "to_status": "PROMOTED", "human_approved": True, "decision_digest": "d" * 64},
    ]
    promoted = SCORING.derive(method_id, runs, events, 0.0)
    assert promoted["PROMOTION_ELIGIBLE"] is True, promoted
    assert promoted["RECOMMENDED_STATUS"] == "PROMOTED"
    no_human = SCORING.derive(method_id, runs, events[:-1], 0.0)
    assert no_human["PROMOTION_ELIGIBLE"] is False
    assert no_human["RECOMMENDED_STATUS"] == "BLIND_VALIDATED"
    duplicate_only = [dict(events[0], duplicate_or_known=True), events[1], events[2], events[3]]
    duplicate_result = SCORING.derive(method_id, runs, duplicate_only, 0.0)
    assert duplicate_result["PROMOTION_ELIGIBLE"] is False


def assert_registry_cli() -> None:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, str(AUTOMATION / "validate-methodology-registry.py"), "--lab-root", str(LAB_ROOT)],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    result = json.loads(completed.stdout)
    assert result["REGISTRY_VALID"] is True
    assert result["V12_METHOD_COUNT"] == 21
    assert result["BLIND_BENCHMARK_STATUS"] == "NOT_RUN"


def assert_blind_placeholders() -> None:
    for benchmark in ("B11", "B12", "B13"):
        record = load_json(LAB_ROOT / "validation" / "blind" / f"{benchmark}.json")
        assert record["status"] == "NOT_RUN"
        assert record["fixture_material_present"] is False
        assert record["sealed_fixture_digest"] is None
        assert record["ground_truth_available_to_executor"] is False


def assert_isolated_forward_receipt() -> None:
    receipt = load_json(LAB_ROOT / "validation" / "runs" / "isolated-forward-root-receipt.json")
    executor = LAB_ROOT / "validation" / "runs" / "isolated-forward-executor-result.json"
    falsifier = LAB_ROOT / "validation" / "runs" / "isolated-forward-falsifier-result.json"
    assert receipt["executor_output_sha256"] == file_digest(executor)
    assert receipt["falsifier_output_sha256"] == file_digest(falsifier)
    assert receipt["new_candidate_count"] == 0
    assert receipt["valid_finding_count"] == 0
    assert receipt["isolation_strength"] == "CONTEXT_AND_INPUT_ALLOWLIST_NOT_OS_FILESYSTEM_ISOLATION"


def main() -> int:
    assert_json_and_toml_parse()
    assert_no_network_primitives()
    assert_coverage_packets()
    assert_novelty_gate()
    assert_definition_integrity()
    assert_termination_gate()
    runs, recall_gain, patched_false_positive = assert_hidden_family_and_patched_control()
    assert_promotion_gate(runs)
    assert_registry_cli()
    assert_blind_placeholders()
    assert_isolated_forward_receipt()
    result = {
        "V13_ENGINEERING_TESTS": "PASS",
        "SYNTHETIC_DEVELOPMENT_RECALL_GAIN": recall_gain,
        "PATCHED_CONTROL_FALSE_POSITIVE": patched_false_positive,
        "DUPLICATE_METHODOLOGY_REJECTED": True,
        "BLOCKED_GAP_EXECUTION_REJECTED": True,
        "RUNAWAY": 0,
        "BLIND_B11_B12_B13": "NOT_RUN",
        "GENERALIZATION_PROVEN": False,
        "PROMOTION_PERFORMED": False,
        "V13_LAB_READY_FOR_BLIND_EVALUATION": True,
        "CAVEAT": "Synthetic development fixtures validate plumbing only; they are not blind efficacy evidence."
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
