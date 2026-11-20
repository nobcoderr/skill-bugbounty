#!/usr/bin/env python3
"""Validate the pinned WebHackList 2026 AI metadata/read-coverage ledger.

The default mode is network-free and validates the local catalog. Optional
collection/archive arguments reproduce record and byte bindings from a pinned
WebHackList checkout without executing any archived example.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "config" / "WEBHACKLIST_2026_AI_CORPUS.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_COMMIT = "2f17d6249c178f9b895d2c00536a3009df117afa"
EXPECTED_COLLECTION_SHA256 = "3003a015550d9fca47c8843eb6a7f9ec9d2ac3321c59d9873080a5a82ce84dc9"
EXPECTED_SOURCES_SHA256 = "3f0db6d47e830ef79c6da8d7b794e9d51bbc19ba95bb21a9cda31c8f6cfe3018"
EXPECTED_ARCHIVE_ROOT = "4f24ca8755c30916491b579d300915e058c975bb8cc318ce354098e26e2a9476"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_catalog(catalog: dict) -> list[str]:
    errors: list[str] = []
    if catalog.get("identity") != "WEBHACKLIST_2026_AI_PRELIMINARY_PRIOR_ART_CORPUS_V1":
        errors.append("wrong catalog identity")
    if catalog.get("status") != "PRELIMINARY_UNRANKED_AI_COLLECTED_NOT_COMMUNITY_VETTED_REFERENCE_ONLY":
        errors.append("catalog status does not preserve preliminary boundary")
    snapshot = catalog.get("snapshot", {})
    if snapshot.get("commit") != EXPECTED_COMMIT:
        errors.append("wrong pinned repository commit")
    if snapshot.get("collection_sha256") != EXPECTED_COLLECTION_SHA256:
        errors.append("wrong collection digest")
    if snapshot.get("sources_sha256") != EXPECTED_SOURCES_SHA256:
        errors.append("wrong sources digest")
    coverage = catalog.get("coverage", {})
    for key, expected in {
        "records_total": 299,
        "archived_records_fully_read": 298,
        "live_primary_records_read": 1,
        "archive_bytes_read": 12121660,
        "archive_path_digest_root": EXPECTED_ARCHIVE_ROOT,
        "untrusted_source_marker_missing": 0,
    }.items():
        if coverage.get(key) != expected:
            errors.append(f"coverage mismatch {key}: {coverage.get(key)!r} != {expected!r}")
    if coverage.get("parse_issues") != []:
        errors.append("catalog reports parse issues")

    records = catalog.get("records", [])
    if len(records) != 299:
        errors.append(f"expected 299 records, got {len(records)}")
        return errors
    ids = [record.get("id") for record in records]
    if len(set(ids)) != len(ids):
        errors.append("record IDs are not unique")
    archived = 0
    indexed = 0
    allowed_families = set(catalog.get("classification", {}).get("family_counts", {}))
    for ordinal, record in enumerate(records, 1):
        if record.get("ordinal") != ordinal:
            errors.append(f"record ordinal mismatch at {ordinal}")
        if not str(record.get("source_url", "")).startswith("https://"):
            errors.append(f"record {ordinal} has non-HTTPS source URL")
        if not record.get("method_families"):
            errors.append(f"record {ordinal} has no routing family")
        elif not set(record["method_families"]).issubset(allowed_families):
            errors.append(f"record {ordinal} has unknown routing family")
        status = record.get("read_status")
        if status == "READ_ARCHIVED_MARKDOWN_FULL":
            archived += 1
            if not SHA256_RE.fullmatch(str(record.get("archive_sha256", ""))):
                errors.append(f"record {ordinal} has invalid archive digest")
            if not str(record.get("archived_markdown", "")).startswith(
                "archived-references/md/2026-ai/"
            ):
                errors.append(f"record {ordinal} has invalid archive path")
            if record.get("untrusted_source_marker") is not True:
                errors.append(f"record {ordinal} lacks source marker evidence")
        elif status == "READ_PRIMARY_URL_VIA_INDEXED_RENDER_NOT_BYTE_CAPTURED":
            indexed += 1
            if record.get("live_direct_fetch") != "HTTP_403":
                errors.append("indexed-only record does not preserve direct-fetch limitation")
        else:
            errors.append(f"record {ordinal} has invalid read status {status!r}")
        if any(key in record for key in ("article_body", "payload", "poc", "commands")):
            errors.append(f"record {ordinal} contains prohibited source-body/executable field")
    if archived != 298 or indexed != 1:
        errors.append(f"read-state totals mismatch archived={archived} indexed={indexed}")
    actual_family_counts = Counter(
        family for record in records for family in record.get("method_families", [])
    )
    if dict(actual_family_counts.most_common()) != catalog.get("classification", {}).get(
        "family_counts"
    ):
        errors.append("derived family counts do not match the record ledger")
    return errors


def reproduce(
    catalog: dict,
    collection_path: Path,
    archive_root: Path,
    sources_path: Path | None,
) -> list[str]:
    errors: list[str] = []
    collection_bytes = collection_path.read_bytes()
    if sha256_bytes(collection_bytes) != EXPECTED_COLLECTION_SHA256:
        errors.append("supplied collection bytes do not match pinned digest")
        return errors
    if sources_path is not None and sha256_bytes(sources_path.read_bytes()) != EXPECTED_SOURCES_SHA256:
        errors.append("supplied sources bytes do not match pinned digest")
    collection = json.loads(collection_bytes)
    items = collection.get("items", [])
    if len(items) != 299:
        errors.append(f"supplied collection has {len(items)} records")
        return errors
    records = catalog["records"]
    root = hashlib.sha256()
    for item, record in zip(items, records):
        for key, catalog_key in (("id", "id"), ("t", "title"), ("u", "source_url")):
            if item.get(key) != record.get(catalog_key):
                errors.append(f"collection/catalog mismatch for {catalog_key} at {record['ordinal']}")
        rel = item.get("m")
        if not rel:
            if record.get("read_status") != "READ_PRIMARY_URL_VIA_INDEXED_RENDER_NOT_BYTE_CAPTURED":
                errors.append("unarchived record has wrong status")
            continue
        path = archive_root / rel
        if not path.is_file():
            errors.append(f"missing archive file: {rel}")
            continue
        raw = path.read_bytes()
        digest = sha256_bytes(raw)
        if digest != record.get("archive_sha256"):
            errors.append(f"archive digest mismatch: {rel}")
        if b"UNTRUSTED SOURCE TEXT" not in raw:
            errors.append(f"archive marker missing: {rel}")
        root.update(rel.encode("utf-8") + b"\0" + digest.encode("ascii") + b"\n")
    if root.hexdigest() != EXPECTED_ARCHIVE_ROOT:
        errors.append("reproduced archive root mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--collection", type=Path)
    parser.add_argument("--archive-root", type=Path)
    parser.add_argument("--sources", type=Path)
    args = parser.parse_args()
    if (args.collection is None) != (args.archive_root is None):
        parser.error("--collection and --archive-root must be supplied together")
    catalog = load_json(args.catalog)
    errors = validate_catalog(catalog)
    if args.collection is not None:
        errors.extend(reproduce(catalog, args.collection, args.archive_root, args.sources))
    if errors:
        print("WEBHACKLIST 2026 CORPUS VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    mode = "CATALOG_AND_ARCHIVE" if args.collection is not None else "CATALOG_ONLY"
    print(f"WEBHACKLIST 2026 CORPUS VALIDATION PASS ({mode})")
    print("records=299 archived_full_read=298 indexed_primary_read=1 executable_actions=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

