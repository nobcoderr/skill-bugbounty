#!/usr/bin/env python3
"""Deterministic regression checks for authorization KILL reasoning contracts."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "config" / "AUTHORIZATION_REASONING_REGRESSION_CASES.json"


def decide(case: dict[str, object]) -> str:
    protected = bool(case["protected_operation"])
    reachable = bool(case["attacker_reaches_operation"])
    same_resource = case["authorized_resource"] == case["consumed_resource"]
    control_state = str(case["control_state"])
    decision = str(case["decision"])
    dispatched = bool(case["handler_dispatched"])
    intentional = bool(case["intent_documented"])
    no_transition = bool(case["no_authority_transition_proven"])

    if reachable and protected and not same_resource and dispatched:
        return "DO_NOT_KILL"
    if reachable and protected and control_state in {
        "absent_implicit_success",
        "empty_implicit_success",
        "unknown_fail_open",
        "error_fail_open",
    } and decision == "ALLOW" and dispatched:
        return "DO_NOT_KILL"
    if (not protected or decision == "DENY" or not dispatched) and intentional and no_transition:
        return "KILL_ALLOWED"
    return "NEEDS_INVARIANT_PROOF"


def main() -> int:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    failures: list[str] = []
    for case in data["cases"]:
        actual = decide(case)
        if actual != case["expected"]:
            failures.append(f"{case['id']}: expected {case['expected']}, got {actual}")

    required_markers = {
        "references/AUTHORIZATION_INVARIANT_KILL_CHALLENGE.md": "AUTHORIZATION_KILL_CHALLENGE:v1",
        "skill/expert-authentication-authorization-hunter/SKILL.md": "AUTHORIZATION_KILL_CHALLENGE:v1",
        "skill/bug-bounty-triage/SKILL.md": "AUTHORIZATION_KILL_CHALLENGE:v1",
        "skill/expert-source-code-bug-hunter/SKILL.md": "AUTHORIZATION_KILL_CHALLENGE:v1",
        "skill/expert-web-api-business-logic-hunter/SKILL.md": "AUTHORIZATION_KILL_CHALLENGE:v1",
        "skill/secure-code-reviewer/SKILL.md": "AUTHORIZATION_KILL_CHALLENGE:v1",
        "authorized-security-autopilot/SKILL.md": "AUTHORIZATION_KILL_CHALLENGE:v1",
    }
    for rel, marker in required_markers.items():
        path = ROOT / rel
        if marker not in path.read_text(encoding="utf-8"):
            failures.append(f"missing {marker} in {rel}")

    schema = json.loads((ROOT / "config" / "CODEX_CLI_CANDIDATE_SCHEMA.json").read_text(encoding="utf-8"))
    if "authorization_kill_challenge" not in schema.get("required", []):
        failures.append("candidate schema does not require authorization_kill_challenge")

    if failures:
        print("AUTHORIZATION INVARIANT REGRESSION FAILED")
        for failure in failures:
            print("- " + failure)
        return 1
    print(f"AUTHORIZATION INVARIANT REGRESSION PASSED: {len(data['cases'])} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
