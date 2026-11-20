#!/usr/bin/env python3
"""Network-free rule regressions for the autonomous research cascade."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "AUTONOMOUS_RESEARCH_CASCADE_CASES.json"
VALIDATOR = ROOT / "automation" / "validate-autonomous-research-cascade.py"
LINEAGE = ROOT / "config" / "NOVEL_DEVELOPMENT_LINEAGE_EXCLUSIONS.json"


def load_validator() -> Any:
    spec = importlib.util.spec_from_file_location("cascade_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def deep_merge(target: dict[str, Any], patch: dict[str, Any]) -> None:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = copy.deepcopy(value)


def base_candidate() -> dict[str, Any]:
    return {
        "candidate_id": "cascade-rule-fixture",
        "stage": "CODE_DERIVED_HYPOTHESIS",
        "research_objective": "test whether delayed consumption preserves checked identity",
        "derivation_origin": "TARGET_NATIVE",
        "novel_discovery_mode": True,
        "micro_inspiration_id": "fixture:identity-contract",
        "micro_inspiration_scope": "one target-native ownership rule",
        "known_attack_terms_withheld": True,
        "hypothesis": "replacement before consumption may change resolved identity",
        "falsifier": "the consumer resolves the generation captured during validation",
        "security_invariant": "checked and consumed identity remain equal",
        "probe_cleanliness": "CLEAN",
        "probe_semantic_proof": "the owned fixture API documents replacement as a valid transition",
        "evaluation_primitive": "compare checked and consumed identity counters",
        "baseline_fingerprint": "baseline:identity-a",
        "anomaly_fingerprint": "",
        "harness_independent_reproduction": False,
        "independent_runners": [],
        "anomaly_origin": "UNKNOWN",
        "shared_semantic_domains": [],
        "counterfactuals": ["replace an unrelated fixture identity"],
        "composition_paths": [],
        "cascade_parent": None,
        "observation_parent": None,
        "invariant_parent": None,
        "cascade_depth": 0,
        "second_order_questions": [
            "where else is the same handle consumed",
            "which other protected effects trust this identity",
        ],
        "derived_detection_strategy": "",
        "deterministic_validator": "CODE:automation/fixture-validator.py#sha256:" + "a" * 64,
        "authoritative_readback": "",
        "negative_controls": ["replace an unrelated fixture object"],
        "proof_gates": {
            "hypothesis_created": True,
            "source_to_sink_proven": False,
            "runtime_effect_proven": False,
            "negative_control_pass": False,
        },
        "prior_art_embargo_respected": True,
        "prior_art_checked_after_proof": False,
        "prior_art": {"status": "NOT_CHECKED", "sources_checked": []},
        "novelty_status": "UNVERIFIED",
        "research_cascade": {
            "inspiration_fragments": [
                {"contains_vulnerability_ground_truth": False}
            ],
            "stage_isolation": {"target_answer_leakage": False},
        },
        "scope": {"scope_status": "PROVEN"},
        "authorized_scope": "researcher-owned fixture only",
        "impact_ceiling": "harmless identity mismatch counter",
        "cleanup_status": "NOT_REQUIRED",
        "verdict": "UNRATED",
        "manual_status": "NOT_TESTED",
    }


def check_methodology_contamination(failures: list[str]) -> None:
    paths = [
        ROOT / "skill" / "autonomous-research-cascade-engine" / "SKILL.md",
        ROOT / "references" / "MICRO_INSPIRATION_RESEARCH_METHOD.md",
        ROOT / "references" / "GENERIC_ANOMALY_EVALUATION_METHOD.md",
        ROOT / "references" / "CLEAN_PROBE_REASONING_METHOD.md",
        ROOT / "references" / "DISCOVERY_CASCADE_METHOD.md",
        ROOT / "references" / "SHARED_SEMANTIC_REUSE_METHOD.md",
        ROOT / "references" / "HARNESS_FALSIFICATION_METHOD.md",
    ]
    forbidden = re.compile(
        r"CVE-\d|GHSA-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+|HackerOne\s*#|"
        r"response queue poisoning|dangling-byte|shared-parser confusion|"
        r"multipart/byteranges|dual-matching",
        re.IGNORECASE,
    )
    for path in paths:
        match = forbidden.search(path.read_text(encoding="utf-8"))
        if match:
            failures.append(f"technical lineage leaked into {path}: {match.group(0)}")


def main() -> int:
    validator = load_validator()
    data = json.loads(CASES.read_text(encoding="utf-8"))
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    failures: list[str] = []
    pattern_replay = 0
    prior_art_leakage = 0
    false_positive_bounty_grade = 0
    context_contamination = 0
    deterministic_validator_bypass = 0
    target_native_hypotheses = 0
    cascade_generated_leads = 0
    harness_false_anomalies = 0

    if data.get("package_version") != version:
        failures.append("cascade regression package version mismatch")

    tracks = data.get("external_blind_tracks", [])
    if [track.get("id") for track in tracks] != ["V9-A", "V9-B", "V9-C", "V9-D", "V9-E"]:
        failures.append("external tracks must be exactly V9-A through V9-E")
    for track in tracks:
        if track.get("seed_location") != "EXTERNAL_EVALUATOR_ONLY":
            failures.append(f"{track.get('id')} seed is not evaluator-isolated")
        if track.get("ground_truth_in_package") is not False:
            failures.append(f"{track.get('id')} leaks ground truth")

    held_out = data.get("historical_held_out_protocol", {})
    if held_out.get("family_count_min") != 3 or held_out.get("family_count_max") != 5:
        failures.append("held-out protocol must require 3-5 families")
    if held_out.get("exclude_all_v1_v9_development_lineages") is not True:
        failures.append("held-out protocol must exclude all development lineages")
    if held_out.get("status") != "NOT_STARTED":
        failures.append("packaged regression cannot claim a held-out result")

    for case in data.get("rule_cases", []):
        candidate = base_candidate()
        deep_merge(candidate, case.get("overrides", {}))
        errors, _warnings = validator.validate_candidate(candidate)
        actual_valid = not errors
        expected_valid = case.get("expected_valid")
        if actual_valid != expected_valid:
            failures.append(
                f"{case.get('id')}: expected valid={expected_valid}, got valid={actual_valid}, errors={errors}"
            )
            continue
        fragment = case.get("expected_error")
        if fragment and not any(fragment in error for error in errors):
            failures.append(f"{case.get('id')}: missing error {fragment!r}; errors={errors}")
        if case.get("pattern_replay_probe") and actual_valid:
            pattern_replay += 1
        if case.get("prior_art_leakage_probe") and actual_valid:
            prior_art_leakage += 1
        if case.get("context_contamination_probe") and actual_valid:
            context_contamination += 1
        if case.get("deterministic_validator_bypass_probe") and actual_valid:
            deterministic_validator_bypass += 1
        if case.get("harness_false_anomaly_probe") and actual_valid:
            harness_false_anomalies += 1
        if case.get("safe_repository_case") and candidate.get("verdict") == "STRONG":
            false_positive_bounty_grade += 1
        if actual_valid and candidate.get("derivation_origin") == "TARGET_NATIVE" and candidate.get(
            "stage"
        ) not in {"KILLED", "BLOCKED"}:
            target_native_hypotheses += 1
        if actual_valid and candidate.get("stage") == "CASCADE_LEAD":
            cascade_generated_leads += 1

    check_methodology_contamination(failures)

    lineage = json.loads(LINEAGE.read_text(encoding="utf-8"))
    if lineage.get("package_version") != version:
        failures.append("development-lineage package version mismatch")
    if lineage.get("auditor_auto_load") is not False:
        failures.append("development lineages must not auto-load for blind auditors")
    sources = lineage.get("sources", [])
    if not sources or sources[0].get("exclude_entire_technical_lineage") is not True:
        failures.append("methodology source technical lineage is not excluded")

    schema = json.loads(
        (ROOT / "config" / "CODEX_CLI_CANDIDATE_SCHEMA.json").read_text(encoding="utf-8")
    )
    if schema.get("$id") != "urn:codex-cli-security-audit:candidate:v10":
        failures.append("candidate schema is not v10")
    required = set(schema.get("required", []))
    for field in validator.REQUIRED_FIELDS:
        if field not in required:
            failures.append(f"candidate schema does not require cascade field: {field}")
    if schema.get("properties", {}).get("derivation_origin", {}).get("const") != "TARGET_NATIVE":
        failures.append("candidate schema does not enforce TARGET_NATIVE derivation")
    if "CASCADE_LEAD" not in schema.get("properties", {}).get("stage", {}).get("enum", []):
        failures.append("candidate schema does not include CASCADE_LEAD")

    targets = data.get("acceptance_targets", {})
    metrics = {
        "pattern_replay": pattern_replay,
        "prior_art_leakage": prior_art_leakage,
        "false_positive_bounty_grade": false_positive_bounty_grade,
        "context_contamination": context_contamination,
        "deterministic_validator_bypass": deterministic_validator_bypass,
        "harness_false_anomalies": harness_false_anomalies,
    }
    for name, value in metrics.items():
        if value != targets.get(name):
            failures.append(f"{name} target failed: {value}")
    if target_native_hypotheses < targets.get("target_native_hypotheses_min", 1):
        failures.append("no valid target-native hypotheses")
    if cascade_generated_leads < targets.get("cascade_generated_leads_min", 1):
        failures.append("no valid cascade-generated leads")

    if failures:
        print("AUTONOMOUS RESEARCH CASCADE REGRESSION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "AUTONOMOUS RESEARCH CASCADE REGRESSION PASSED: "
        f"cases={len(data['rule_cases'])} pattern_replay={pattern_replay} "
        f"prior_art_leakage={prior_art_leakage} "
        f"false_positive_bounty_grade={false_positive_bounty_grade} hard_failure=0 "
        f"context_contamination={context_contamination} "
        f"deterministic_validator_bypass={deterministic_validator_bypass} "
        f"target_native_hypotheses={target_native_hypotheses} "
        f"cascade_generated_leads={cascade_generated_leads} "
        f"harness_false_anomalies={harness_false_anomalies} held_out=NOT_RUN"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
