#!/usr/bin/env python3
"""Network-free validation for the agentic security harness source ledger."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config" / "AGENTIC_SECURITY_HARNESS_SOURCE_CATALOG.json"
METHOD = ROOT / "references" / "AGENTIC_SECURITY_RESEARCH_HARNESS_METHOD.md"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_COMMITS = {
    "zephrfish-harness-kit": "db3a53411fe3eff966d0f9061540bd4ee4342887",
    "gadievron-raptor": "17e4227b7797dbcd734b56706e5783e58a4ba62f",
    "anthropic-defending-code-reference-harness": "d3bea6b5793b5f3d59a75ebe69a58efa88383145",
    "faizann24-baby-naptime": "f54648d903c167660a18e15cde0523fd54cc425c",
    "evilsocket-audit": "d6ee73035f47d9b6ff3353e6fe030395d85e6e08",
    "visa-vulnerability-agentic-harness": "4128e870377850db16cb082115105cc8ee6f1a72",
    "anthropic-oss-scanner": "16e4101f1ca8678ae2122b9f11d8ec02f384c021",
    "sequester-bug-bounty-triage": "9684e1bfc876e841f9c789f0b258902b43d461e4",
    "morluto-rea": "428eee00fdd0406cdf2b734c9ea14a2bb02da279",
}


def main() -> int:
    errors: list[str] = []
    try:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"AGENTIC SECURITY HARNESS VALIDATION FAILED: {exc}")
        return 1

    if catalog.get("identity") != "AGENTIC_SECURITY_RESEARCH_HARNESS_SOURCE_CATALOG_V1":
        errors.append("wrong catalog identity")
    if catalog.get("default_integration_state") != "REFERENCE_ONLY":
        errors.append("catalog must default to REFERENCE_ONLY")
    if catalog.get("execution_authorized") is not False:
        errors.append("catalog must not authorize execution")

    sources = catalog.get("sources", [])
    if len(sources) != 11:
        errors.append(f"expected 11 sources, got {len(sources)}")
    ids = [item.get("id") for item in sources]
    if len(ids) != len(set(ids)):
        errors.append("source IDs are not unique")
    by_id = {item.get("id"): item for item in sources}
    for item in sources:
        if not str(item.get("integration_state", "")).startswith("REFERENCE_ONLY"):
            errors.append(f"source not reference-only: {item.get('id')}")
    for source_id, commit in EXPECTED_COMMITS.items():
        item = by_id.get(source_id, {})
        if item.get("commit") != commit:
            errors.append(f"wrong pinned commit for {source_id}")
        for path, digest in item.get("inspected_artifacts", {}).items():
            if not path or not SHA256_RE.fullmatch(str(digest)):
                errors.append(f"invalid artifact digest for {source_id}:{path}")

    for article_id in (
        "andy-gill-mcps-and-friends",
        "andy-gill-harnessing-harnesses",
    ):
        item = by_id.get(article_id, {})
        if item.get("claim_status") != "AUTHOR_CLAIMS_NOT_INDEPENDENTLY_VALIDATED":
            errors.append(f"article claim boundary missing: {article_id}")

    oss = by_id.get("anthropic-oss-scanner", {})
    if oss.get("user_supplied_legacy_url") != "https://github.com/carlini/oss-scanner":
        errors.append("OSS Scanner legacy source identity missing")
    if oss.get("legacy_url_status_on_retrieval") != "HTTP_404":
        errors.append("OSS Scanner legacy URL status missing")

    if not catalog.get("global_blocked_operations"):
        errors.append("global blocked operations missing")
    prohibited_keys = {"payload", "poc", "commands", "article_body"}
    if any(prohibited_keys.intersection(item) for item in sources):
        errors.append("catalog contains copied executable or article-body fields")

    try:
        method = METHOD.read_text(encoding="utf-8").lower()
        for phrase in (
            "agentic_security_research_harness:v1",
            "hypothesis_quarantined",
            "clean_snapshot_reproduced",
            "low_priv_reachable",
            "demoted",
            "provenance-bound",
            "persistent sessions are capabilities",
            "roi may rank authorized candidates",
        ):
            if phrase not in method:
                errors.append(f"method contract missing: {phrase}")
    except Exception as exc:
        errors.append(f"cannot read method: {exc}")

    if errors:
        print("AGENTIC SECURITY HARNESS VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("AGENTIC SECURITY HARNESS VALIDATION PASS (CATALOG_ONLY)")
    print("sources=11 repositories=9 articles=2 executable_actions=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
