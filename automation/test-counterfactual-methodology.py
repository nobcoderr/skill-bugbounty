#!/usr/bin/env python3
"""Network-free regression tests for counterfactual methodology synthesis."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "COUNTERFACTUAL_METHODOLOGY_REGRESSION_CASES.json"

COSMETIC_AXES = {
    "payload_spelling",
    "filename_only",
    "endpoint_alias",
    "encoding_decoration",
    "numeric_constant",
    "vulnerability_label",
    "actor_label",
}


def classify(case: dict[str, object], limits: dict[str, int]) -> str:
    if case.get("prior_result") != "NO_VALID_FINDING":
        return "DEFERRED_CURRENT_METHOD_ACTIVE"
    if not case.get("target_eligible"):
        return "BLOCKED_BY_SCOPE"
    if int(case.get("cycle", 0)) > int(limits["max_cycles"]):
        return "STOP_BUDGET_EXHAUSTED"
    if case.get("pattern_replay"):
        return "METHOD_REJECTED"

    axes = set(case.get("changed_axes", []))
    if not axes:
        return "NO_MATERIAL_NEW_METHODOLOGY"
    architecture_change = bool(case.get("architecture_level_change"))
    if (
        axes.issubset(COSMETIC_AXES)
        or (len(axes) < 2 and not architecture_change)
        or not case.get("new_oracle_or_consumer")
    ):
        return "MUTATION_ONLY"

    required_design = (
        int(case.get("fact_anchor_count", 0)) >= int(limits["min_fact_anchors"])
        and bool(case.get("deterministic_oracle"))
        and bool(case.get("baseline"))
        and bool(case.get("negative_control"))
        and bool(case.get("falsifier"))
    )
    if not required_design:
        return "METHOD_REJECTED"
    if case.get("evaluated") and case.get("full_finding_proof"):
        return "VALID_FINDING_GENERATED"
    if case.get("evaluated"):
        return "METHOD_GENERATED_NO_VALID_FINDING"
    return "METHOD_READY_FOR_SAFE_EVALUATION"


def main() -> int:
    errors: list[str] = []
    data = json.loads(CASES.read_text(encoding="utf-8"))
    limits = data["limits"]
    cases = data["cases"]
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        errors.append("regression case IDs are not unique")
    if limits != {
        "max_cycles": 2,
        "max_method_cards_per_cycle": 3,
        "min_fact_anchors": 2,
    }:
        errors.append(f"unexpected limits: {limits}")

    for case in cases:
        actual = classify(case, limits)
        if actual != case.get("expected_state"):
            errors.append(
                f"{case.get('id')}: expected {case.get('expected_state')}, got {actual}"
            )

    required_text = {
        ROOT / "skill" / "counterfactual-methodology-synthesizer" / "SKILL.md": (
            "NO VALID FINDING",
            "MUTATION_ONLY",
            "maximum two",
            "STRONG + MANUALLY_CONFIRMED",
        ),
        ROOT / "references" / "COUNTERFACTUAL_METHODOLOGY_SYNTHESIS_METHOD.md": (
            "What if A becomes B",
            "prior_method_exclusion_digest",
            "two post-`NO VALID FINDING` cycles",
            "VALID_FINDING_GENERATED",
        ),
        ROOT / "prompts" / "MASTER_PROMPT_COUNTERFACTUAL_METHODOLOGY_SYNTHESIS.md": (
            "no more than three method cards",
            "METHOD_GENERATED_NO_VALID_FINDING",
            "Run at most two",
            "AUTHORIZED_OFFENSIVE_PROMPT:v1",
        ),
    }
    for path, phrases in required_text.items():
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{path.relative_to(ROOT)} missing: {phrase}")

    # Exercise a structurally valid validator ledger without network access.
    ledger = {
        "prior_result": "NO_VALID_FINDING",
        "target_eligible": True,
        "cycle": 1,
        "prior_method_exclusion_digest": "sha256:test-fixture",
        "methods": [
            {
                "method_id": "M1",
                "parent_method_id": "P0",
                "fact_anchors": ["src/a:10", "src/b:20"],
                "changed_axes": ["representation", "consumer"],
                "architecture_level_change": True,
                "protected_invariant": "untrusted representation cannot gain authority",
                "counterfactual_question": "What if raw becomes decoded before the consumer?",
                "attacker_variable": "owned object metadata",
                "authority_consumer": "privileged delayed worker",
                "oracle": "authoritative state remains unchanged",
                "baseline": "canonical metadata is rejected",
                "safe_sibling": "same request with a canonical value",
                "negative_control": "unowned object is denied",
                "falsifier": "worker revalidates canonical identity",
                "release_reachability": "current shipped worker path",
                "impact_plan": "low privilege to protected mutation",
                "safety": "owned object, inert canary, cleanup",
                "stop_condition": "one local attempt then stop",
                "independence_explanation": "new delayed consumer and oracle",
                "status": "METHOD_READY_FOR_SAFE_EVALUATION",
            }
        ],
    }
    # tempfile usage is local test isolation, not package mutation.
    with tempfile.TemporaryDirectory(prefix="counterfactual-method-test-") as tmp:
        ledger_path = Path(tmp) / "ledger.json"
        ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
        from importlib.util import module_from_spec, spec_from_file_location

        validator_path = ROOT / "automation" / "validate-counterfactual-methodology.py"
        spec = spec_from_file_location("counterfactual_validator", validator_path)
        if spec is None or spec.loader is None:
            errors.append("cannot load counterfactual validator")
        else:
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            validation_errors = module.validate_ledger(ledger)
            errors.extend(f"validator fixture: {item}" for item in validation_errors)

    if errors:
        print("COUNTERFACTUAL METHODOLOGY TESTS FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"COUNTERFACTUAL_METHODOLOGY_CASES={len(cases)}")
    print("COUNTERFACTUAL METHODOLOGY TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

