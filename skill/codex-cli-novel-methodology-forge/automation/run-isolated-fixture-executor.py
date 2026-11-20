#!/usr/bin/env python3
"""Network-free development executor for the authority-epoch fixture only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _v13lib import file_digest, load_json, object_digest


ALLOWLIST = [
    "factual_target_brief",
    "architecture_map",
    "methodology_definition",
    "authorized_source_snapshot",
    "scope_safety_card",
]


def execute(method: dict, gap: dict, target: dict, child_id: str, run_mode: str) -> dict:
    target_gap_ids = set(method.get("target_gap_ids", []))
    material_gap_ids = {item["gap_id"] for item in gap.get("gaps", []) if item.get("status") == "MATERIAL"}
    if not target_gap_ids.issubset(material_gap_ids):
        raise ValueError("methodology does not target a material gap")

    decision = target["authority_decision"]
    consumer = target["consumer"]
    mutable = set(target["mutable_authorizing_facts"])
    encoded = set(decision["encoded_into_capability"])
    revalidated = set(consumer["revalidates_current_facts"])
    projection = target.get("revocation_projection", {})
    relevant_unbound = sorted(
        field for field in mutable
        if field not in encoded
        and field not in revalidated
        and projection.get(field) not in encoded
        and projection.get(field) not in revalidated
    )

    facts = []
    atoms = []
    if target.get("documented_revocation_contract") == "retroactive_before_later_consumption" and relevant_unbound:
        fact = "Later consumer does not encode or revalidate mutable authority facts: " + ", ".join(relevant_unbound)
        facts.append({"classification": "FACT", "statement": fact, "artifact_pointer": "consumer.revalidates_current_facts"})
        atoms.append({
            "evidence_id": "EVID-SYNTHETIC-AUTHORITY-EPOCH",
            "semantic_identity": "authority_epoch:consumer:unbound_mutable_fact",
            "fact": fact,
            "artifact_pointer": "consumer.revalidates_current_facts",
            "artifact_sha256": object_digest(consumer),
            "snapshot_digest": object_digest(target),
            "oracle_result": "PASS"
        })
    else:
        facts.append({"classification": "FACT", "statement": "Consumer binds or revalidates the mutable authority epoch.", "artifact_pointer": "consumer.revalidates_current_facts"})

    capsule = {
        "methodology_id": method["methodology_id"],
        "target_gap_ids": sorted(target_gap_ids),
        "source_snapshot_digest": object_digest(target),
        "allowlist": ALLOWLIST,
    }
    semantic_output = {"facts": facts, "atoms": atoms, "result": "MATERIAL_GAIN" if atoms else "NO_MATERIAL_GAIN"}
    return {
        "record_type": "METHODOLOGY_EXECUTION",
        "execution_id": "EXEC-SYNTHETIC-" + child_id.upper().replace("_", "-"),
        "methodology_id": method["methodology_id"],
        "gap_id": sorted(target_gap_ids)[0],
        "run_mode": run_mode,
        "target_family": "synthetic_authority_lifetime",
        "blind_seed_digest": "0" * 64,
        "independent_executor": True,
        "child_context": {"fresh_context": True, "child_id": child_id, "assignment_token_digest": object_digest({"child": child_id, "capsule": capsule})},
        "source_snapshot_digest": object_digest(target),
        "input_capsule_digest": object_digest(capsule),
        "output_digest": object_digest(semantic_output),
        "capsule_allowlist": ALLOWLIST,
        "forbidden_inputs_present": False,
        "observations": facts,
        "new_material_evidence_count": len(atoms),
        "new_material_evidence": atoms,
        "new_research_paths": ["trace mutable authority facts from issuer to protected consumer"] if atoms else [],
        "new_candidates": [],
        "duplicate_existing_candidates": [],
        "killed_observations": [] if atoms else ["authority epoch omission absent"],
        "blocked_observations": [],
        "methodology_execution_result": "MATERIAL_GAIN" if atoms else "NO_MATERIAL_GAIN",
        "registry_mutation": False,
        "transcript_digest": object_digest([node["operator"] for node in method["procedure_graph"]["nodes"]]),
        "root_receipt_digest": object_digest({"child": child_id, "output": semantic_output})
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--methodology", type=Path, required=True)
    parser.add_argument("--gap-packet", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--child-id", required=True)
    parser.add_argument("--run-mode", choices=["DISCOVERY", "REPRODUCTION", "BLIND", "PATCHED_CONTROL"], default="DISCOVERY")
    args = parser.parse_args()
    result = execute(load_json(args.methodology), load_json(args.gap_packet), load_json(args.target), args.child_id, args.run_mode)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
