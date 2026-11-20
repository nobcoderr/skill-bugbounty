#!/usr/bin/env python3
"""Validate target-native autonomous research-cascade ledgers offline."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


STAGES = {
    "MICRO_INSPIRATION",
    "CODE_DERIVED_HYPOTHESIS",
    "TESTABILITY_GATE",
    "SAFE_PROBE",
    "GENERIC_EVALUATION",
    "ANOMALY",
    "HARNESS_FALSIFICATION",
    "ROOT_CAUSE_HYPOTHESES",
    "INVARIANT_PROOF",
    "NEEDS_INVARIANT_PROOF",
    "NEEDS_CONSUMER_PROOF",
    "NEEDS_STATE_PROOF",
    "NEEDS_RUNTIME_PROOF",
    "NEEDS_REACHABILITY_PROOF",
    "DISCOVERY_CASCADE",
    "AUTHORITATIVE_READBACK",
    "NEEDS_PRIOR_ART_CHECK",
    "CASCADE_LEAD",
    "STRONG_CANDIDATE",
    "KILLED",
    "BLOCKED",
}
PROMOTED_NON_CLEAN_STAGES = {
    "INVARIANT_PROOF",
    "NEEDS_INVARIANT_PROOF",
    "NEEDS_CONSUMER_PROOF",
    "NEEDS_STATE_PROOF",
    "NEEDS_RUNTIME_PROOF",
    "NEEDS_REACHABILITY_PROOF",
    "DISCOVERY_CASCADE",
    "AUTHORITATIVE_READBACK",
    "NEEDS_PRIOR_ART_CHECK",
    "CASCADE_LEAD",
    "STRONG_CANDIDATE",
}
ANOMALY_STAGES = {
    "ANOMALY",
    "HARNESS_FALSIFICATION",
    "ROOT_CAUSE_HYPOTHESES",
    "INVARIANT_PROOF",
    "NEEDS_INVARIANT_PROOF",
    "NEEDS_CONSUMER_PROOF",
    "NEEDS_STATE_PROOF",
    "NEEDS_RUNTIME_PROOF",
    "NEEDS_REACHABILITY_PROOF",
    "DISCOVERY_CASCADE",
    "AUTHORITATIVE_READBACK",
    "NEEDS_PRIOR_ART_CHECK",
    "CASCADE_LEAD",
    "STRONG_CANDIDATE",
}
READBACK_STAGES = {"AUTHORITATIVE_READBACK", "NEEDS_PRIOR_ART_CHECK", "STRONG_CANDIDATE"}
ORIGINS = {"TARGET_CONFIRMED", "HARNESS_CONFIRMED", "MIXED", "UNKNOWN"}
VALIDATOR_PATTERN = re.compile(
    r"^(?:CODE:[^#]+#sha256:[0-9a-f]{64}|RULESET:[A-Za-z0-9_.-]+@[A-Za-z0-9_.-]+)$"
)
REQUIRED_FIELDS = (
    "candidate_id",
    "stage",
    "research_objective",
    "derivation_origin",
    "novel_discovery_mode",
    "micro_inspiration_id",
    "micro_inspiration_scope",
    "known_attack_terms_withheld",
    "hypothesis",
    "falsifier",
    "security_invariant",
    "probe_cleanliness",
    "probe_semantic_proof",
    "evaluation_primitive",
    "baseline_fingerprint",
    "anomaly_fingerprint",
    "harness_independent_reproduction",
    "independent_runners",
    "anomaly_origin",
    "shared_semantic_domains",
    "counterfactuals",
    "composition_paths",
    "cascade_parent",
    "observation_parent",
    "invariant_parent",
    "cascade_depth",
    "second_order_questions",
    "derived_detection_strategy",
    "deterministic_validator",
    "authoritative_readback",
    "negative_controls",
    "proof_gates",
    "prior_art_embargo_respected",
    "prior_art_checked_after_proof",
    "prior_art",
    "novelty_status",
    "research_cascade",
    "scope",
    "authorized_scope",
    "impact_ceiling",
    "cleanup_status",
    "verdict",
    "manual_status",
)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, minimum: int = 0) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= minimum
        and all(_nonempty(item) for item in value)
    )


def _find_zero_day_claim(value: Any, path: str = "candidate") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower().replace("-", "_") == "zero_day":
                errors.append(f"{path}.{key} is forbidden; use novelty_status")
            errors.extend(_find_zero_day_claim(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_find_zero_day_claim(child, f"{path}[{index}]"))
    elif isinstance(value, str) and value.strip().upper() == "ZERO_DAY":
        errors.append(f"{path} cannot claim ZERO_DAY")
    return errors


def _validate_context_isolation(candidate: dict[str, Any], errors: list[str]) -> None:
    research = candidate.get("research_cascade")
    if not isinstance(research, dict):
        errors.append("research_cascade must be an object")
        return
    isolation = research.get("stage_isolation")
    if not isinstance(isolation, dict) or isolation.get("target_answer_leakage") is not False:
        errors.append("research cascade context is contaminated")
    fragments = research.get("inspiration_fragments")
    if not isinstance(fragments, list) or not fragments:
        errors.append("research_cascade.inspiration_fragments must not be empty")
        return
    for index, fragment in enumerate(fragments):
        if not isinstance(fragment, dict):
            errors.append(f"research_cascade.inspiration_fragments[{index}] must be an object")
        elif fragment.get("contains_vulnerability_ground_truth") is not False:
            errors.append(
                f"research_cascade.inspiration_fragments[{index}] contains vulnerability ground truth"
            )


def _validate_prior_art(candidate: dict[str, Any], errors: list[str]) -> None:
    prior_art = candidate.get("prior_art")
    gates = candidate.get("proof_gates")
    if not isinstance(prior_art, dict) or not isinstance(gates, dict):
        errors.append("prior_art and proof_gates must be objects")
        return
    status = prior_art.get("status")
    sources = prior_art.get("sources_checked")
    if not isinstance(sources, list):
        errors.append("prior_art.sources_checked must be a list")
        sources = []
    performed = status != "NOT_CHECKED" or bool(sources)
    unlocked = all(
        gates.get(field) is True
        for field in (
            "hypothesis_created",
            "source_to_sink_proven",
            "runtime_effect_proven",
            "negative_control_pass",
        )
    )
    if candidate.get("novel_discovery_mode") is True and performed and not unlocked:
        errors.append("prior art embargo violated before proof gate")
    if candidate.get("prior_art_embargo_respected") is not True:
        errors.append("prior_art_embargo_respected must be true")
    if candidate.get("prior_art_checked_after_proof") is True and not unlocked:
        errors.append("prior_art_checked_after_proof cannot precede proof gate")


def validate_candidate(candidate: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(candidate, dict):
        return ["candidate must be a JSON object"], warnings

    missing = [field for field in REQUIRED_FIELDS if field not in candidate]
    if missing:
        errors.append(f"missing required cascade fields: {missing}")
    errors.extend(_find_zero_day_claim(candidate))

    if candidate.get("stage") not in STAGES:
        errors.append(f"invalid cascade stage: {candidate.get('stage')!r}")
    if candidate.get("derivation_origin") != "TARGET_NATIVE":
        errors.append("derivation_origin must be TARGET_NATIVE; PATTERN_REPLAY is rejected")
    if candidate.get("known_attack_terms_withheld") is not True:
        errors.append("known attack terms and vulnerability ground truth must be withheld")

    for field in (
        "candidate_id",
        "research_objective",
        "micro_inspiration_id",
        "micro_inspiration_scope",
        "hypothesis",
        "falsifier",
        "security_invariant",
        "evaluation_primitive",
        "baseline_fingerprint",
        "authorized_scope",
        "impact_ceiling",
    ):
        if not _nonempty(candidate.get(field)):
            errors.append(f"{field} must be non-empty")

    inspiration_scope = candidate.get("micro_inspiration_scope")
    if isinstance(inspiration_scope, str) and len(inspiration_scope) > 600:
        errors.append("micro_inspiration_scope must remain atomic and at most 600 characters")

    cleanliness = candidate.get("probe_cleanliness")
    if cleanliness not in {"CLEAN", "DIRTY", "UNKNOWN"}:
        errors.append("probe_cleanliness must be CLEAN, DIRTY, or UNKNOWN")
    semantic_proof = candidate.get("probe_semantic_proof")
    if not isinstance(semantic_proof, str):
        errors.append("probe_semantic_proof must be a string")
    if cleanliness == "CLEAN" and not _nonempty(semantic_proof):
        errors.append("CLEAN probe requires governing-grammar semantic proof")
    if cleanliness in {"DIRTY", "UNKNOWN"} and candidate.get("stage") in PROMOTED_NON_CLEAN_STAGES:
        if not _nonempty(semantic_proof):
            errors.append("non-clean probe cannot advance without semantic proof")

    validator = candidate.get("deterministic_validator")
    if not isinstance(validator, str) or not VALIDATOR_PATTERN.fullmatch(validator):
        errors.append("deterministic_validator must identify versioned code or a ruleset digest")

    for field, minimum in (
        ("negative_controls", 1),
        ("counterfactuals", 1),
        ("independent_runners", 0),
        ("shared_semantic_domains", 0),
        ("composition_paths", 0),
    ):
        if not _string_list(candidate.get(field), minimum=minimum):
            errors.append(f"{field} must be a string list with at least {minimum} entries")
    domains = candidate.get("shared_semantic_domains")
    if isinstance(domains, list) and len(domains) == 1:
        errors.append("shared semantic reuse requires at least two distinct domains")
    if isinstance(domains, list) and len(domains) != len(set(domains)):
        errors.append("shared_semantic_domains must be unique")

    anomaly_origin = candidate.get("anomaly_origin")
    if anomaly_origin not in ORIGINS:
        errors.append("anomaly_origin is invalid")
    anomaly_fingerprint = candidate.get("anomaly_fingerprint")
    if not isinstance(anomaly_fingerprint, str):
        errors.append("anomaly_fingerprint must be a string")
    if candidate.get("stage") in ANOMALY_STAGES and not _nonempty(anomaly_fingerprint):
        errors.append(f"stage {candidate.get('stage')} requires an anomaly fingerprint")
    if anomaly_origin == "HARNESS_CONFIRMED" and candidate.get("stage") not in {"KILLED", "BLOCKED"}:
        errors.append("harness-confirmed anomaly cannot advance as target behavior")

    independent = candidate.get("harness_independent_reproduction")
    runners = candidate.get("independent_runners")
    if not isinstance(independent, bool):
        errors.append("harness_independent_reproduction must be boolean")
    if independent is True and (not isinstance(runners, list) or len(set(runners)) < 2):
        errors.append("independent reproduction requires two distinct runner identities")
    if anomaly_origin == "TARGET_CONFIRMED" and independent is not True:
        errors.append("TARGET_CONFIRMED requires harness-independent reproduction")

    depth = candidate.get("cascade_depth")
    parent_fields = (
        candidate.get("cascade_parent"),
        candidate.get("observation_parent"),
        candidate.get("invariant_parent"),
    )
    if not isinstance(depth, int) or isinstance(depth, bool) or not 0 <= depth <= 8:
        errors.append("cascade_depth must be an integer from 0 through 8")
    elif depth == 0 and any(value is not None for value in parent_fields):
        errors.append("root cascade node cannot claim parent provenance")
    elif depth > 0:
        if not all(_nonempty(value) for value in parent_fields):
            errors.append("cascade child must preserve observation and invariant parent provenance")
        if not _nonempty(candidate.get("derived_detection_strategy")):
            errors.append("cascade child requires a derived detection strategy")
    questions = candidate.get("second_order_questions")
    if not _string_list(questions, minimum=2) or len(questions) != 2:
        errors.append("second_order_questions must contain exactly two questions")

    if candidate.get("stage") == "CASCADE_LEAD":
        if not isinstance(depth, int) or depth < 1:
            errors.append("CASCADE_LEAD requires a parent and positive cascade depth")
        if anomaly_origin != "TARGET_CONFIRMED" or independent is not True:
            errors.append("CASCADE_LEAD requires target-confirmed independent reproduction")
        if candidate.get("verdict") == "STRONG":
            errors.append("CASCADE_LEAD cannot self-certify as STRONG")

    if candidate.get("stage") in READBACK_STAGES and not _nonempty(
        candidate.get("authoritative_readback")
    ):
        errors.append(f"stage {candidate.get('stage')} requires authoritative read-back")
    if candidate.get("cleanup_status") not in {
        "NOT_REQUIRED",
        "PLANNED",
        "PASS",
        "FAILED",
        "BLOCKED",
    }:
        errors.append("cleanup_status is invalid")
    if candidate.get("cleanup_status") == "FAILED" and candidate.get("stage") not in {
        "KILLED",
        "BLOCKED",
    }:
        errors.append("candidate cannot advance after cleanup failure")

    scope = candidate.get("scope")
    if not isinstance(scope, dict) or scope.get("scope_status") != "PROVEN":
        errors.append("SCOPE_MUST_BE_EXPLICIT: scope.scope_status must be PROVEN")
    _validate_context_isolation(candidate, errors)
    _validate_prior_art(candidate, errors)

    novelty = candidate.get("novelty_status")
    if novelty not in {
        "UNVERIFIED",
        "NO_OVERLAP_FOUND",
        "OVERLAP_FOUND",
        "PUBLIC_KNOWN",
        "DUPLICATE",
        "FIXED",
    }:
        errors.append("novelty_status is invalid")
    if candidate.get("stage") != "STRONG_CANDIDATE" and novelty != "UNVERIFIED":
        errors.append("novelty_status must remain UNVERIFIED before final proof")
    if candidate.get("stage") == "STRONG_CANDIDATE":
        if anomaly_origin != "TARGET_CONFIRMED" or independent is not True:
            errors.append("STRONG_CANDIDATE requires target-confirmed independent reproduction")
        if candidate.get("cleanup_status") not in {"PASS", "NOT_REQUIRED"}:
            errors.append("STRONG_CANDIDATE requires successful cleanup")
        if novelty != "NO_OVERLAP_FOUND":
            errors.append("STRONG_CANDIDATE requires completed post-proof novelty checks")
        if candidate.get("verdict") != "STRONG" or candidate.get("manual_status") != "MANUALLY_CONFIRMED":
            errors.append("STRONG_CANDIDATE requires STRONG plus MANUALLY_CONFIRMED")

    return errors, warnings


def _self_test_candidate() -> dict[str, Any]:
    return {
        "candidate_id": "cascade-self-test",
        "stage": "CODE_DERIVED_HYPOTHESIS",
        "research_objective": "test whether a delayed consumer preserves checked identity",
        "derivation_origin": "TARGET_NATIVE",
        "novel_discovery_mode": True,
        "micro_inspiration_id": "fixture:identity-contract",
        "micro_inspiration_scope": "one target-native ownership rule",
        "known_attack_terms_withheld": True,
        "hypothesis": "replacement before consumption may change the resolved identity",
        "falsifier": "the consumer resolves the generation captured at validation",
        "security_invariant": "checked and consumed identity remain equal",
        "probe_cleanliness": "CLEAN",
        "probe_semantic_proof": "fixture API accepts replacement as a documented transition",
        "evaluation_primitive": "compare the checked and consumed identity counters",
        "baseline_fingerprint": "baseline:identity-a",
        "anomaly_fingerprint": "",
        "harness_independent_reproduction": False,
        "independent_runners": [],
        "anomaly_origin": "UNKNOWN",
        "shared_semantic_domains": [],
        "counterfactuals": ["replace an unrelated identity"],
        "composition_paths": [],
        "cascade_parent": None,
        "observation_parent": None,
        "invariant_parent": None,
        "cascade_depth": 0,
        "second_order_questions": [
            "where else is the handle consumed",
            "which other protected effects trust this identity",
        ],
        "derived_detection_strategy": "",
        "deterministic_validator": "CODE:automation/self-test-validator.py#sha256:"
        + "a" * 64,
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        errors, _warnings = validate_candidate(_self_test_candidate())
        if errors:
            print("AUTONOMOUS RESEARCH CASCADE VALIDATOR SELF-TEST FAILED")
            for error in errors:
                print(f"- {error}")
            return 1
        print("AUTONOMOUS RESEARCH CASCADE VALIDATOR SELF-TEST PASSED")
        return 0

    if args.candidate is None:
        parser.error("candidate path or --self-test is required")
    data = json.loads(args.candidate.read_text(encoding="utf-8"))
    errors, warnings = validate_candidate(data)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("AUTONOMOUS RESEARCH CASCADE CANDIDATE VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
