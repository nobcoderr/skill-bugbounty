#!/usr/bin/env python3
"""Validate the Informative/N/A negative-control corpus and impact-gate contract."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "PROGRAM_IMPACT_NEGATIVE_CONTROL_CASES.json"
POSITIVE_CASES = ROOT / "config" / "PROGRAM_IMPACT_POSITIVE_CONTROL_CASES.json"
METHOD = ROOT / "references" / "PROGRAM_IMPACT_BOUNDARY_GATE.md"
PROMPT = ROOT / "prompts" / "MASTER_PROMPT_PROGRAM_IMPACT_BOUNDARY_GATE.md"
SKILL = ROOT / "skill" / "program-impact-boundary-gate" / "SKILL.md"

EXPECTED_IDS = {
    "3975775", "3973303", "3973467", "3971480", "3972786", "3972687",
    "3968095", "3624130", "3926585", "3955537", "3923008", "3950679",
    "3857254", "3948952", "3948366", "3948342", "3934602", "3934184",
    "3910136", "3933799", "3930172", "3929882",
    "3924650", "3925580", "3919124", "3885945", "3646244", "3905967",
    "3887461", "3894878", "3896366", "3895960", "3895989", "3885565",
    "3820783",
    "3849097", "3867328", "3849853", "3857175", "3847712", "3830857",
    "3799781", "3808838", "3803376",
    "3803950", "3792094", "3680070", "3797857", "3796714", "3968729",
    "3970639", "3972196", "3971496", "3972316",
    "3739926", "3800002", "3862436", "3863692", "3863048", "3816519",
    "3810858", "3802645", "3728070",
    "3983944", "3977820", "3975896", "3973127", "3971585", "3973158",
    "3973093", "3948506", "3928810",
}
EXPECTED_NA_IDS = {
    "3739926", "3800002", "3862436", "3863692", "3863048", "3816519",
    "3810858", "3802645", "3728070", "3977820",
}
VALID_RESULTS = {
    "IMPACT_GATE_BLOCKED",
    "INFORMATIVE_LIKELY",
    "KILL_NO_CAPABILITY_DELTA",
    "KILL_TRUSTED_DOMAIN",
    "KILL_BY_DESIGN",
    "KILL_NON_PRODUCTION_TARGET",
    "KILL_THREAT_MODEL",
    "KILL_KNOWN_OR_DUPLICATE",
    "KILL_NO_PRODUCTION_REACHABILITY",
    "KILL_PROGRAM_SEVERITY",
    "KILL_ENVIRONMENT_MISMATCH",
}

EXPECTED_NA_DECISIONS = {
    "3739926": ("IMPACT_GATE_BLOCKED", "IMPACT_AND_EXPLOIT_REALISM"),
    "3800002": ("IMPACT_GATE_BLOCKED", "PROCEDURAL_INACTIVITY"),
    "3862436": ("KILL_ENVIRONMENT_MISMATCH", "ENVIRONMENTAL_MISMATCH"),
    "3863692": ("KILL_TRUSTED_DOMAIN", "CONSENTED_TRUST_AND_SCOPE"),
    "3863048": ("IMPACT_GATE_BLOCKED", "NO_CAPABILITY_DELTA_DISPUTE"),
    "3816519": ("KILL_ENVIRONMENT_MISMATCH", "CONSENSUS_ENVIRONMENT_MISMATCH"),
    "3810858": ("KILL_PROGRAM_SEVERITY", "EXPLICIT_OUT_OF_SCOPE_IMPACT"),
    "3802645": ("KILL_BY_DESIGN", "SECURITY_PROPERTY_AND_TRUST_ANCHOR"),
    "3728070": ("KILL_BY_DESIGN", "INTENDED_PUBLIC_BEHAVIOR_AND_SEVERITY"),
    "3977820": ("KILL_PROGRAM_SEVERITY", "EXPLICIT_PROGRAM_EXCLUSION"),
}

EXPECTED_NEW_DECISIONS = {
    "3983944": ("KILL_KNOWN_OR_DUPLICATE", "DUPLICATE", "KNOWN_OR_DUPLICATE"),
    "3977820": ("KILL_PROGRAM_SEVERITY", "NOT_APPLICABLE", "EXPLICIT_PROGRAM_EXCLUSION"),
    "3975896": ("IMPACT_GATE_BLOCKED", "INFORMATIVE", "SYNTHETIC_CONSUMER_AND_UNVERIFIED_RESULT"),
    "3973127": ("KILL_THREAT_MODEL", "INFORMATIVE", "UNSECURED_TRANSPORT_THREAT_MODEL"),
    "3971585": ("KILL_THREAT_MODEL", "INFORMATIVE", "APPLICATION_CONTROLLED_API_MISUSE"),
    "3973158": ("KILL_THREAT_MODEL", "INFORMATIVE", "LOCAL_LAUNCH_CONFIGURATION_AND_EXPLOIT_REALISM"),
    "3973093": ("KILL_NO_PRODUCTION_REACHABILITY", "INFORMATIVE", "NO_PRODUCTION_DEPLOYMENT_EVIDENCE"),
    "3948506": ("KILL_TRUSTED_DOMAIN", "INFORMATIVE", "TRUSTED_WORKSPACE_EQUIVALENT_AUTHORITY"),
    "3928810": ("KILL_NO_CAPABILITY_DELTA", "INFORMATIVE", "EXISTING_BUILD_TIME_EXECUTION_AUTHORITY"),
}

EXPECTED_POSITIVE_IDS = {"3931777", "3931771"}
POSITIVE_REQUIRED_FIELDS = {
    "report_id", "program", "adjudication_status", "reward_status", "pattern",
    "starting_authority", "attacker_input", "consumer_chain", "protected_sink",
    "resulting_capability", "capability_delta", "production_reachability",
    "negative_controls", "manual_proof", "safe_proof_rule", "future_disposition",
}


def adjudicate(facts: dict[str, bool | str]) -> str:
    """Small deterministic oracle for the gate's decisive invariants."""
    if facts.get("closure_basis") == "PROCEDURAL_INACTIVITY":
        return "IMPACT_GATE_BLOCKED"
    if facts.get("known_or_duplicate"):
        return "KILL_KNOWN_OR_DUPLICATE"
    if facts.get("excluded_impact") or not facts.get("program_eligible", True):
        return "KILL_PROGRAM_SEVERITY"
    if facts.get("outside_threat_model"):
        return "KILL_THREAT_MODEL"
    if not facts.get("production_stack_equivalent", True):
        return "KILL_ENVIRONMENT_MISMATCH"
    if facts.get("consensus_required") and not facts.get("canonical_consensus"):
        return "KILL_ENVIRONMENT_MISMATCH"
    if not facts.get("production_reachable", True):
        return "KILL_NO_PRODUCTION_REACHABILITY"
    if facts.get("intended_public_or_by_design"):
        return "KILL_BY_DESIGN"
    if facts.get("consented_trust") and not facts.get("explicit_isolation_promise"):
        return "KILL_TRUSTED_DOMAIN"
    if facts.get("equivalent_path_proven"):
        return "KILL_NO_CAPABILITY_DELTA"
    required_proof = (
        "scope_verified",
        "severity_verified",
        "security_promise_proven",
        "protected_consumer_proven",
        "capability_delta_proven",
        "exact_negative_control_passed",
        "manual_confirmation",
        "report_ready",
    )
    if not all(facts.get(field) for field in required_proof):
        return "IMPACT_GATE_BLOCKED"
    return "IMPACT_GATE_PASS"


BASE_PASS = {
    "scope_verified": True,
    "severity_verified": True,
    "security_promise_proven": True,
    "protected_consumer_proven": True,
    "capability_delta_proven": True,
    "exact_negative_control_passed": True,
    "manual_confirmation": True,
    "report_ready": True,
    "production_stack_equivalent": True,
    "production_reachable": True,
    "program_eligible": True,
}

ADVERSARIAL_SCENARIOS = (
    ("nmi_inactivity_is_not_merits", {**BASE_PASS, "closure_basis": "PROCEDURAL_INACTIVITY"}, "IMPACT_GATE_BLOCKED"),
    ("local_acl_skips_host_stack", {**BASE_PASS, "production_stack_equivalent": False}, "KILL_ENVIRONMENT_MISMATCH"),
    ("single_node_with_consensus_stub", {**BASE_PASS, "consensus_required": True, "canonical_consensus": False}, "KILL_ENVIRONMENT_MISMATCH"),
    ("real_crypto_gap_only_for_excluded_dos", {**BASE_PASS, "excluded_impact": True}, "KILL_PROGRAM_SEVERITY"),
    ("approved_attacker_endpoint_without_redirect_promise", {**BASE_PASS, "consented_trust": True, "explicit_isolation_promise": False}, "KILL_TRUSTED_DOMAIN"),
    ("browser_claim_missing_top_level_control", {**BASE_PASS, "exact_negative_control_passed": False}, "IMPACT_GATE_BLOCKED"),
    ("public_metadata_outside_exact_privacy_promise", {**BASE_PASS, "intended_public_or_by_design": True}, "KILL_BY_DESIGN"),
    ("archived_source_without_live_consumer", {**BASE_PASS, "production_reachable": False}, "KILL_NO_PRODUCTION_REACHABILITY"),
    ("technically_valid_public_duplicate", {**BASE_PASS, "known_or_duplicate": True}, "KILL_KNOWN_OR_DUPLICATE"),
    ("current_cross_tenant_write_with_readback", dict(BASE_PASS), "IMPACT_GATE_PASS"),
    ("live_at_submission_then_patched", {**BASE_PASS, "submission_time_live": True, "currently_patched": True}, "IMPACT_GATE_PASS"),
    ("strong_source_without_protected_consumer", {**BASE_PASS, "protected_consumer_proven": False}, "IMPACT_GATE_BLOCKED"),
    ("updater_sandbox_execution_is_excluded", {**BASE_PASS, "program_eligible": False}, "KILL_PROGRAM_SEVERITY"),
    ("unverified_sdk_result_only_accepted_by_synthetic_consumer", {**BASE_PASS, "protected_consumer_proven": False}, "IMPACT_GATE_BLOCKED"),
    ("caller_manufactures_unusual_raw_io_lifecycle", {**BASE_PASS, "outside_threat_model": True}, "KILL_THREAT_MODEL"),
    ("plaintext_proxy_route_without_secure_boundary", {**BASE_PASS, "outside_threat_model": True}, "KILL_THREAT_MODEL"),
    ("niche_build_without_deployed_consumer", {**BASE_PASS, "production_reachable": False}, "KILL_NO_PRODUCTION_REACHABILITY"),
    ("reapproved_trusted_workspace_server_change", {**BASE_PASS, "consented_trust": True, "explicit_isolation_promise": False}, "KILL_TRUSTED_DOMAIN"),
    ("locked_malicious_crate_already_has_build_script_execution", {**BASE_PASS, "equivalent_path_proven": True}, "KILL_NO_CAPABILITY_DELTA"),
    ("author_owned_metadata_reaches_arbitrary_file_delete", dict(BASE_PASS), "IMPACT_GATE_PASS"),
    ("author_owned_metadata_reaches_admin_browser_execution", dict(BASE_PASS), "IMPACT_GATE_PASS"),
    ("exact_fixed_finalize_root_replayed", {**BASE_PASS, "known_or_duplicate": True}, "KILL_KNOWN_OR_DUPLICATE"),
)


def main() -> int:
    errors: list[str] = []
    data = json.loads(CASES.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    positive_data = json.loads(POSITIVE_CASES.read_text(encoding="utf-8"))
    positive_cases = positive_data.get("cases", [])
    ids = {str(case.get("report_id")) for case in cases}

    if ids != EXPECTED_IDS:
        errors.append(f"report corpus mismatch missing={sorted(EXPECTED_IDS - ids)} extra={sorted(ids - EXPECTED_IDS)}")
    if len(cases) != len(EXPECTED_IDS):
        errors.append(f"expected {len(EXPECTED_IDS)} unique cases, got {len(cases)}")

    required = {
        "report_id", "pattern", "technical_behavior", "starting_authority",
        "missing_security_proof", "gate_result", "unblock",
    }
    for case in cases:
        missing = required - set(case)
        if missing:
            errors.append(f"case {case.get('report_id')} missing fields {sorted(missing)}")
        if case.get("gate_result") not in VALID_RESULTS:
            errors.append(f"case {case.get('report_id')} has invalid gate result {case.get('gate_result')!r}")
        for field in required - {"report_id"}:
            if not isinstance(case.get(field), str) or not case.get(field, "").strip():
                errors.append(f"case {case.get('report_id')} has empty {field}")
        if str(case.get("report_id")) in EXPECTED_NA_IDS:
            if case.get("adjudication_status") != "NOT_APPLICABLE":
                errors.append(f"case {case.get('report_id')} must preserve NOT_APPLICABLE status")
            if not isinstance(case.get("closure_basis"), str) or not case.get("closure_basis", "").strip():
                errors.append(f"case {case.get('report_id')} must preserve closure basis")

    by_id = {str(case["report_id"]): case for case in cases}
    for report_id, (expected_result, expected_basis) in EXPECTED_NA_DECISIONS.items():
        case = by_id[report_id]
        if case.get("gate_result") != expected_result:
            errors.append(
                f"case {report_id} expected {expected_result}, got {case.get('gate_result')}"
            )
        if case.get("closure_basis") != expected_basis:
            errors.append(
                f"case {report_id} expected closure {expected_basis}, got {case.get('closure_basis')}"
            )
    for report_id, (expected_result, expected_status, expected_basis) in EXPECTED_NEW_DECISIONS.items():
        case = by_id[report_id]
        if case.get("gate_result") != expected_result:
            errors.append(f"case {report_id} expected {expected_result}, got {case.get('gate_result')}")
        if case.get("adjudication_status") != expected_status:
            errors.append(f"case {report_id} expected status {expected_status}, got {case.get('adjudication_status')}")
        if case.get("closure_basis") != expected_basis:
            errors.append(f"case {report_id} expected closure {expected_basis}, got {case.get('closure_basis')}")
    for case in cases:
        if case.get("gate_result") == "IMPACT_GATE_PASS":
            errors.append(f"negative-control case {case.get('report_id')} must not pass the impact gate")
        if case.get("closure_basis") == "PROCEDURAL_INACTIVITY" and case.get("gate_result") != "IMPACT_GATE_BLOCKED":
            errors.append(f"procedural case {case.get('report_id')} must remain blocked rather than killed")

    positive_ids = {str(case.get("report_id")) for case in positive_cases}
    if positive_ids != EXPECTED_POSITIVE_IDS:
        errors.append(
            f"positive-control corpus mismatch missing={sorted(EXPECTED_POSITIVE_IDS - positive_ids)} "
            f"extra={sorted(positive_ids - EXPECTED_POSITIVE_IDS)}"
        )
    if len(positive_cases) != len(EXPECTED_POSITIVE_IDS):
        errors.append(f"expected {len(EXPECTED_POSITIVE_IDS)} unique positive controls, got {len(positive_cases)}")
    for case in positive_cases:
        missing = POSITIVE_REQUIRED_FIELDS - set(case)
        if missing:
            errors.append(f"positive case {case.get('report_id')} missing fields {sorted(missing)}")
        for field in POSITIVE_REQUIRED_FIELDS:
            if not isinstance(case.get(field), str) or not case.get(field, "").strip():
                errors.append(f"positive case {case.get('report_id')} has empty {field}")
        if case.get("adjudication_status") != "RESOLVED":
            errors.append(f"positive case {case.get('report_id')} must preserve RESOLVED status")
        if case.get("reward_status") != "PAID":
            errors.append(f"positive case {case.get('report_id')} must preserve PAID reward status")
        if "KILL_KNOWN_OR_DUPLICATE" not in case.get("future_disposition", ""):
            errors.append(f"positive case {case.get('report_id')} must burn its exact public/fixed root")

    for name, facts, expected in ADVERSARIAL_SCENARIOS:
        actual = adjudicate(facts)
        if actual != expected:
            errors.append(f"adversarial case {name} expected {expected}, got {actual}")

    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in (METHOD, PROMPT, SKILL)
    ).lower()
    for phrase in (
        "starting capability -> exploit transition -> resulting capability",
        "equivalent intended path",
        "severity floor",
        "informative_likely",
        "kill_no_capability_delta",
        "kill_trusted_domain",
        "impact_gate_blocked",
        "negative controls",
        "do not kill by pattern resemblance alone",
        "localhost",
        "patched control",
        "production product versus demo",
        "program impact ceiling",
        "defense-in-depth hygiene",
        "kill_known_or_duplicate",
        "kill_non_production_target",
        "kill_threat_model",
        "kill_no_production_reachability",
        "attacker-controlled timing",
        "lifecycle contract",
        "lab-only",
        "promised security property",
        "collision feasibility",
        "counterfactual",
        "control plane",
        "signing",
        "authorization issuance time",
        "derived credential lineage",
        "temporal trust equivalence",
        "protected consumer",
        "operation-specific",
        "environmental mismatch",
        "procedural inactivity",
        "production stack equivalence",
        "canonical consensus",
        "top-level navigation",
        "submission-time",
        "privacy promise",
        "report readiness",
        "positive controls",
        "downstream consumer",
        "low-privilege",
        "authoritative read-back",
        "public and fixed",
        "authorization-server binding",
        "build-time code execution",
    ):
        if phrase not in combined:
            errors.append(f"impact-gate contract missing phrase: {phrase}")

    if errors:
        print("PROGRAM IMPACT GATE REGRESSION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PROGRAM_IMPACT_NEGATIVE_CONTROLS={len(cases)}/{len(EXPECTED_IDS)}")
    print(f"PROGRAM_IMPACT_POSITIVE_CONTROLS={len(positive_cases)}/{len(EXPECTED_POSITIVE_IDS)}")
    print(f"PROGRAM_IMPACT_ADVERSARIAL_SCENARIOS={len(ADVERSARIAL_SCENARIOS)}/{len(ADVERSARIAL_SCENARIOS)}")
    print("PROGRAM_IMPACT_GATE_REGRESSION=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
