#!/usr/bin/env python3
"""Build and query a local corpus of public HackerOne Hacktivity metadata.

The sync command uses HackerOne's documented Hacker API. It stores only the
public Hacktivity fields needed for research and never stores credentials or a
full report body. Semantic analyst cards are imported separately after a human
or agent reviews a publicly disclosed report.
"""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import hashlib
import json
import os
import sqlite3
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable


API_ENDPOINT = "https://api.hackerone.com/v1/hackers/hacktivity"
ALLOWED_STATUSES = {
    "DEEPLY_REVIEWED",
    "EXACT_ROOT_EXTRACTED",
    "STALE_NEEDS_REVIEW",
    "REJECTED_INSUFFICIENT_EVIDENCE",
}
CARD_FIELDS = {
    "report_id",
    "analysis_status",
    "attacker_start",
    "attacker_control",
    "entry_point",
    "primitive",
    "boundary",
    "enforcing_component",
    "sink",
    "capability_delta",
    "prerequisites",
    "proof_oracle",
    "root_cause",
    "chain_edges",
    "negative_controls",
    "patch_or_fix",
    "duplicate_signature",
    "evidence_urls",
    "analyst_notes",
}
REQUIRED_CARD_FIELDS = {
    "report_id",
    "analysis_status",
    "attacker_start",
    "attacker_control",
    "entry_point",
    "primitive",
    "boundary",
    "sink",
    "capability_delta",
    "prerequisites",
    "proof_oracle",
    "root_cause",
    "duplicate_signature",
    "evidence_urls",
}


def default_db_path() -> Path:
    data_root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return data_root / "codex" / "hacktivity" / "corpus.sqlite3"


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def connect_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS reports (
            report_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            disclosed_at TEXT,
            submitted_at TEXT,
            program_handle TEXT,
            program_name TEXT,
            program_url TEXT,
            cwe TEXT,
            cve_ids_json TEXT NOT NULL DEFAULT '[]',
            severity_rating TEXT,
            votes INTEGER NOT NULL DEFAULT 0,
            total_awarded_amount REAL NOT NULL DEFAULT 0,
            currency TEXT,
            reporter_username TEXT,
            reporter_name TEXT,
            hacktivity_summary TEXT,
            source_digest TEXT NOT NULL,
            source_updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS analyst_cards (
            report_id TEXT PRIMARY KEY REFERENCES reports(report_id) ON DELETE CASCADE,
            analysis_status TEXT NOT NULL,
            attacker_start TEXT NOT NULL,
            attacker_control TEXT NOT NULL,
            entry_point TEXT NOT NULL,
            primitive TEXT NOT NULL,
            boundary TEXT NOT NULL,
            enforcing_component TEXT,
            sink TEXT NOT NULL,
            capability_delta TEXT NOT NULL,
            prerequisites TEXT NOT NULL,
            proof_oracle TEXT NOT NULL,
            root_cause TEXT NOT NULL,
            chain_edges_json TEXT NOT NULL DEFAULT '[]',
            negative_controls_json TEXT NOT NULL DEFAULT '[]',
            patch_or_fix TEXT,
            duplicate_signature TEXT NOT NULL,
            evidence_urls_json TEXT NOT NULL DEFAULT '[]',
            analyst_notes TEXT,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS corpus_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_reports_program ON reports(program_handle);
        CREATE INDEX IF NOT EXISTS idx_reports_cwe ON reports(cwe);
        CREATE INDEX IF NOT EXISTS idx_reports_disclosed ON reports(disclosed_at);
        CREATE INDEX IF NOT EXISTS idx_cards_signature ON analyst_cards(duplicate_signature);
        """
    )
    return connection


def nested(mapping: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = mapping
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def clean_text(value: Any, maximum: int) -> str:
    if value is None:
        return ""
    text = " ".join(str(value).replace("\x00", " ").split())
    return text[:maximum]


def item_skip_reason(item: Any) -> str:
    if not isinstance(item, dict):
        return "item_not_object"
    item_type = str(item.get("type", "")).strip().lower()
    if item_type not in {"report", "hacktivity_item", "hacktivity-item"}:
        return f"unsupported_type:{item_type or 'missing'}"
    attrs = item.get("attributes") or {}
    if not isinstance(attrs, dict):
        return "attributes_not_object"
    disclosed = attrs.get("disclosed")
    disclosed_false = disclosed is False or str(disclosed).strip().lower() in {"false", "0", "no"}
    if disclosed_false:
        return "not_disclosed"
    if disclosed is not True and str(disclosed).strip().lower() not in {"true", "1", "yes"}:
        if not clean_text(attrs.get("disclosed_at"), 100):
            return "missing_disclosure_evidence"
    report_id = str(item.get("id", "")).strip()
    if not report_id.isdigit():
        return "invalid_report_id"
    return ""


def normalize_item(item: dict[str, Any]) -> dict[str, Any] | None:
    if item_skip_reason(item):
        return None
    attrs = item.get("attributes") or {}
    report_id = str(item.get("id", "")).strip()

    relationships = item.get("relationships") or {}
    program = nested(relationships, "program", "data", "attributes", default={}) or {}
    reporter = nested(relationships, "reporter", "data", "attributes", default={}) or {}
    generated = nested(
        relationships,
        "report_generated_content",
        "data",
        "attributes",
        default={},
    ) or {}
    url = clean_text(attrs.get("url"), 1000)
    canonical_url = f"https://hackerone.com/reports/{report_id}"
    if url != canonical_url:
        url = canonical_url

    record = {
        "report_id": report_id,
        "title": clean_text(attrs.get("title"), 1000) or f"HackerOne report {report_id}",
        "url": url,
        "disclosed_at": clean_text(attrs.get("disclosed_at"), 100),
        "submitted_at": clean_text(attrs.get("submitted_at"), 100),
        "program_handle": clean_text(program.get("handle"), 200),
        "program_name": clean_text(program.get("name"), 500),
        "program_url": clean_text(program.get("url"), 1000),
        "cwe": clean_text(attrs.get("cwe"), 500),
        "cve_ids_json": json.dumps(attrs.get("cve_ids") or [], sort_keys=True),
        "severity_rating": clean_text(attrs.get("severity_rating"), 50).lower(),
        "votes": int(attrs.get("votes") or 0),
        "total_awarded_amount": float(attrs.get("total_awarded_amount") or 0),
        "currency": clean_text(program.get("currency"), 20).lower(),
        "reporter_username": clean_text(reporter.get("username"), 200),
        "reporter_name": clean_text(reporter.get("name"), 500),
        "hacktivity_summary": clean_text(generated.get("hacktivity_summary"), 8000),
        "source_updated_at": now_utc(),
    }
    digest_material = {key: value for key, value in record.items() if key != "source_updated_at"}
    record["source_digest"] = hashlib.sha256(
        json.dumps(digest_material, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return record


def ingest_items(
    connection: sqlite3.Connection,
    items: Iterable[dict[str, Any]],
) -> tuple[int, int, dict[str, int]]:
    inserted_or_updated = 0
    skipped = 0
    skip_reasons: collections.Counter[str] = collections.Counter()
    columns = [
        "report_id", "title", "url", "disclosed_at", "submitted_at",
        "program_handle", "program_name", "program_url", "cwe", "cve_ids_json",
        "severity_rating", "votes", "total_awarded_amount", "currency",
        "reporter_username", "reporter_name", "hacktivity_summary", "source_digest",
        "source_updated_at",
    ]
    placeholders = ", ".join("?" for _ in columns)
    updates = ", ".join(f"{column}=excluded.{column}" for column in columns[1:])
    statement = (
        f"INSERT INTO reports ({', '.join(columns)}) VALUES ({placeholders}) "
        f"ON CONFLICT(report_id) DO UPDATE SET {updates}"
    )
    for item in items:
        reason = item_skip_reason(item)
        if reason:
            skipped += 1
            skip_reasons[reason] += 1
            continue
        record = normalize_item(item)
        if record is None:
            skipped += 1
            skip_reasons["normalization_failed"] += 1
            continue
        connection.execute(statement, [record[column] for column in columns])
        inserted_or_updated += 1
    connection.commit()
    return inserted_or_updated, skipped, dict(sorted(skip_reasons.items()))


def next_api_link(payload: dict[str, Any], current_url: str) -> str:
    links = payload.get("links") or {}
    candidate: Any = links.get("next") if isinstance(links, dict) else None
    if isinstance(candidate, dict):
        candidate = candidate.get("href") or candidate.get("url")
    if not candidate:
        return ""
    resolved = urllib.parse.urljoin(current_url, str(candidate))
    parsed = urllib.parse.urlparse(resolved)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "api.hackerone.com"
        or parsed.path != "/v1/hackers/hacktivity"
    ):
        raise RuntimeError("API returned an unexpected pagination URL; refusing to follow it")
    return resolved


def api_request(url: str, username: str, token: str, timeout: float, retries: int) -> dict[str, Any]:
    auth = base64.b64encode(f"{username}:{token}".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Basic {auth}",
            "User-Agent": "Codex-Hacktivity-Corpus/1.0 (+public research metadata)",
        },
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            if error.code == 429 or 500 <= error.code < 600:
                if attempt < retries:
                    time.sleep(min(2 ** attempt, 16))
                    continue
            detail = error.read(2048).decode("utf-8", errors="replace")
            raise RuntimeError(f"HackerOne API returned HTTP {error.code}: {detail}") from error
        except urllib.error.URLError as error:
            if attempt < retries:
                time.sleep(min(2 ** attempt, 16))
                continue
            raise RuntimeError(f"HackerOne API request failed: {error.reason}") from error
    raise RuntimeError("HackerOne API request exhausted retries")


def set_meta(connection: sqlite3.Connection, key: str, value: Any) -> None:
    connection.execute(
        "INSERT INTO corpus_meta(key, value) VALUES(?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, json.dumps(value, sort_keys=True)),
    )
    connection.commit()


def api_date_from_iso(value: str) -> str:
    try:
        parsed = dt.date.fromisoformat(value[:10])
    except (TypeError, ValueError) as error:
        raise RuntimeError(f"invalid disclosure timestamp for cursoring: {value!r}") from error
    return parsed.strftime("%m-%d-%Y")


def oldest_item_timestamp(items: Iterable[dict[str, Any]]) -> str:
    values = []
    for item in items:
        attrs = item.get("attributes") if isinstance(item, dict) else None
        if isinstance(attrs, dict):
            value = clean_text(attrs.get("disclosed_at"), 100)
            if value:
                values.append(value)
    return min(values) if values else ""


def date_filter_expression(style: str, cursor_date: str) -> str:
    cursor = dt.datetime.strptime(cursor_date, "%m-%d-%Y").date()
    iso_date = cursor.isoformat()
    expressions = {
        "lte_us": f"disclosed_at:<={cursor_date}",
        "lt_us_next": f"disclosed_at:<{(cursor + dt.timedelta(days=1)).strftime('%m-%d-%Y')}",
        "range_us": f"disclosed_at:[01-01-1970 TO {cursor_date}]",
        "range_star_us": f"disclosed_at:[* TO {cursor_date}]",
        "lte_iso": f"disclosed_at:<={iso_date}",
        "range_iso": f"disclosed_at:[1970-01-01 TO {iso_date}]",
        "lt_iso_next": f"disclosed_at:<{(cursor + dt.timedelta(days=1)).isoformat()}",
    }
    return expressions[style.removeprefix("only_")]


def query_with_date_filter(base_query_parts: list[str], style: str, cursor_date: str) -> str:
    expression = date_filter_expression(style, cursor_date)
    if style.startswith("only_"):
        return expression
    return " AND ".join([*base_query_parts, expression])


def choose_date_filter_style(
    base_query_parts: list[str],
    cursor_date: str,
    username: str,
    token: str,
    timeout: float,
    retries: int,
) -> str:
    candidates = (
        "lte_us", "lt_us_next", "range_us", "range_star_us",
        "lte_iso", "range_iso", "lt_iso_next",
        "only_lte_us", "only_range_us", "only_range_star_us",
        "only_lte_iso", "only_range_iso",
    )
    cursor_day = dt.datetime.strptime(cursor_date, "%m-%d-%Y").date()
    for style in candidates:
        query = query_with_date_filter(base_query_parts, style, cursor_date)
        parameters = urllib.parse.urlencode({
            "queryString": query,
            "sort": "-disclosed_at",
            "page[number]": 1,
            "page[size]": 1,
        })
        try:
            payload = api_request(
                f"{API_ENDPOINT}?{parameters}", username, token, timeout, retries
            )
        except RuntimeError as error:
            if "HTTP 400" in str(error):
                print(json.dumps({
                    "event": "DATE_FILTER_PROBE",
                    "style": style,
                    "result": "REJECTED_400",
                }), file=sys.stderr)
                continue
            raise
        items = payload.get("data") or []
        if not isinstance(items, list):
            raise RuntimeError("Unexpected HackerOne API response during date-filter probe")
        if items:
            oldest = oldest_item_timestamp(items)
            if not oldest:
                print(json.dumps({
                    "event": "DATE_FILTER_PROBE",
                    "style": style,
                    "result": "NO_DATED_ITEM",
                }), file=sys.stderr)
                continue
            if dt.date.fromisoformat(oldest[:10]) > cursor_day:
                print(json.dumps({
                    "event": "DATE_FILTER_PROBE",
                    "style": style,
                    "result": "FILTER_IGNORED",
                }), file=sys.stderr)
                continue
            print(json.dumps({
                "event": "DATE_FILTER_PROBE",
                "style": style,
                "result": "ACCEPTED",
            }), file=sys.stderr)
            return style
        print(json.dumps({
            "event": "DATE_FILTER_PROBE",
            "style": style,
            "result": "EMPTY",
        }), file=sys.stderr)
    raise RuntimeError(
        "HackerOne rejected or returned no records for all bounded disclosure-date filter forms; "
        "the public feed cannot be completed through this API query"
    )


def command_sync(args: argparse.Namespace) -> int:
    username = os.environ.get(args.username_env, "")
    token = os.environ.get(args.token_env, "")
    if not username or not token:
        raise SystemExit(
            f"Missing credentials. Set {args.username_env} and {args.token_env}; "
            "credentials are never accepted as CLI flags."
        )
    if args.resume_older and args.start_page != 1:
        raise SystemExit("--resume-older cannot be combined with --start-page")
    if args.window_page_limit < 2:
        raise SystemExit("--window-page-limit must be at least 2")

    base_query_parts = ["disclosed:true"]
    if args.query:
        base_query_parts.append(f"({args.query})")
    if args.since:
        base_query_parts.append(f"disclosed_at:>={args.since}")
    connection = connect_db(Path(args.db))
    cursor_date = ""
    if args.resume_older:
        oldest_stored = connection.execute(
            "SELECT MIN(disclosed_at) FROM reports WHERE disclosed_at IS NOT NULL AND disclosed_at != ''"
        ).fetchone()[0]
        if not oldest_stored:
            raise SystemExit("--resume-older requested but the corpus has no dated reports")
        cursor_date = api_date_from_iso(str(oldest_stored))
    date_filter_style = ""
    if cursor_date:
        date_filter_style = choose_date_filter_style(
            base_query_parts,
            cursor_date,
            username,
            token,
            args.timeout,
            args.retries,
        )

    def current_query() -> str:
        if cursor_date:
            return query_with_date_filter(base_query_parts, date_filter_style, cursor_date)
        return " AND ".join(base_query_parts)

    page = args.start_page
    pages_fetched = 0
    pages_in_window = 0
    window_index = 1
    total_ingested = 0
    total_skipped = 0
    complete = False
    seen_page_digests: set[str] = set()
    next_url = ""
    oldest_in_window = ""
    while True:
        if pages_fetched >= args.hard_page_cap:
            raise RuntimeError(
                f"hard page cap reached ({args.hard_page_cap}); resume with --start-page after review"
            )
        if not args.all_pages and pages_fetched >= args.max_pages:
            break
        if next_url:
            request_url = next_url
        else:
            parameters = urllib.parse.urlencode(
                {
                    "queryString": current_query(),
                    "sort": args.sort,
                    "page[number]": page,
                    "page[size]": args.page_size,
                }
            )
            request_url = f"{API_ENDPOINT}?{parameters}"
        payload = api_request(
            request_url,
            username,
            token,
            args.timeout,
            args.retries,
        )
        items = payload.get("data") or []
        if not isinstance(items, list):
            raise RuntimeError("Unexpected HackerOne API response: data is not a list")
        if cursor_date and items:
            cursor_day = dt.datetime.strptime(cursor_date, "%m-%d-%Y").date()
            newer_than_cursor = []
            for item in items:
                timestamp = oldest_item_timestamp([item])
                if timestamp and dt.date.fromisoformat(timestamp[:10]) > cursor_day:
                    newer_than_cursor.append(str(item.get("id", "")))
            if newer_than_cursor:
                raise RuntimeError(
                    "HackerOne did not honor the disclosure-date cursor; "
                    "refusing to repeat the newest result window"
                )
        page_digest = hashlib.sha256(
            json.dumps([item.get("id") for item in items], sort_keys=True).encode("utf-8")
        ).hexdigest()
        if items and page_digest in seen_page_digests:
            raise RuntimeError("repeated API page detected; aborting to prevent a runaway sync")
        seen_page_digests.add(page_digest)
        ingested, skipped, skip_reasons = ingest_items(connection, items)
        page_oldest = oldest_item_timestamp(items)
        if page_oldest and (not oldest_in_window or page_oldest < oldest_in_window):
            oldest_in_window = page_oldest
        total_ingested += ingested
        total_skipped += skipped
        pages_fetched += 1
        pages_in_window += 1
        query = current_query()
        set_meta(connection, "sync_checkpoint", {
            "at": now_utc(),
            "base_query": " AND ".join(base_query_parts),
            "active_query": query,
            "cursor_date": cursor_date,
            "date_filter_style": date_filter_style,
            "window_index": window_index,
            "page": page,
            "pages_fetched": pages_fetched,
            "oldest_in_window": oldest_in_window,
            "complete": False,
        })
        print(
            json.dumps(
                {
                    "page": page,
                    "received": len(items),
                    "ingested": ingested,
                    "skipped": skipped,
                    "skip_reasons": skip_reasons,
                    "pagination_next": bool(next_api_link(payload, request_url)),
                    "window": window_index,
                    "cursor_date": cursor_date or None,
                }
            ),
            file=sys.stderr,
        )
        if not items:
            complete = True
            break
        next_url = next_api_link(payload, request_url)
        if args.all_pages and pages_in_window >= args.window_page_limit:
            if args.sort != "-disclosed_at":
                raise RuntimeError(
                    "result-window rotation requires --sort=-disclosed_at"
                )
            if not oldest_in_window:
                raise RuntimeError(
                    "cannot rotate the API result window because no disclosure timestamp was returned"
                )
            new_cursor_date = api_date_from_iso(oldest_in_window)
            if cursor_date:
                current_cursor = dt.datetime.strptime(cursor_date, "%m-%d-%Y").date()
                new_cursor = dt.datetime.strptime(new_cursor_date, "%m-%d-%Y").date()
                if new_cursor >= current_cursor:
                    raise RuntimeError(
                        "date cursor made no backward progress; aborting to prevent a sync loop"
                    )
            cursor_date = new_cursor_date
            if not date_filter_style:
                date_filter_style = choose_date_filter_style(
                    base_query_parts,
                    cursor_date,
                    username,
                    token,
                    args.timeout,
                    args.retries,
                )
            window_index += 1
            page = 1
            pages_in_window = 0
            next_url = ""
            oldest_in_window = ""
            seen_page_digests.clear()
            print(json.dumps({
                "event": "RESULT_WINDOW_ROTATED",
                "next_window": window_index,
                "disclosed_at_lte": cursor_date,
            }), file=sys.stderr)
            time.sleep(args.min_interval)
            continue
        page += 1
        time.sleep(args.min_interval)

    set_meta(connection, "last_sync", {
        "at": now_utc(),
        "base_query": " AND ".join(base_query_parts),
        "final_query": current_query(),
        "sort": args.sort,
        "start_page": args.start_page,
        "last_page": page,
        "pages_fetched": pages_fetched,
        "windows": window_index,
        "resumed_older": bool(args.resume_older),
        "date_filter_style": date_filter_style,
        "complete": complete,
    })
    set_meta(connection, "sync_checkpoint", {
        "at": now_utc(),
        "base_query": " AND ".join(base_query_parts),
        "active_query": current_query(),
        "cursor_date": cursor_date,
        "date_filter_style": date_filter_style,
        "window_index": window_index,
        "page": page,
        "pages_fetched": pages_fetched,
        "oldest_in_window": oldest_in_window,
        "complete": complete,
    })
    unique_reports = connection.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    print(json.dumps({
        "status": "PASS",
        "pages_fetched": pages_fetched,
        "records_ingested": total_ingested,
        "records_skipped": total_skipped,
        "unique_reports_in_corpus": unique_reports,
        "result_windows": window_index,
        "complete_feed_walk": complete,
        "db": str(Path(args.db).resolve()),
    }, indent=2))
    return 0


def load_input_items(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = [json.loads(line) for line in text.splitlines() if line.strip()]
    if isinstance(parsed, dict) and isinstance(parsed.get("data"), list):
        return parsed["data"]
    if isinstance(parsed, list):
        return parsed
    if isinstance(parsed, dict):
        return [parsed]
    raise ValueError("Input must be a HackerOne API JSON object, JSON list, or JSONL")


def command_import(args: argparse.Namespace) -> int:
    connection = connect_db(Path(args.db))
    items = load_input_items(Path(args.input))
    ingested, skipped, skip_reasons = ingest_items(connection, items)
    print(json.dumps({
        "status": "PASS",
        "ingested": ingested,
        "skipped": skipped,
        "skip_reasons": skip_reasons,
    }, indent=2))
    return 0


def validate_card(card: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    unknown = set(card) - CARD_FIELDS
    missing = REQUIRED_CARD_FIELDS - set(card)
    if unknown:
        errors.append(f"unknown fields: {', '.join(sorted(unknown))}")
    if missing:
        errors.append(f"missing fields: {', '.join(sorted(missing))}")
    if str(card.get("analysis_status", "")) not in ALLOWED_STATUSES:
        errors.append(f"analysis_status must be one of {sorted(ALLOWED_STATUSES)}")
    if not str(card.get("report_id", "")).isdigit():
        errors.append("report_id must contain only digits")
    for field in ("chain_edges", "negative_controls", "evidence_urls"):
        if field in card and not isinstance(card[field], list):
            errors.append(f"{field} must be an array")
    evidence_urls = card.get("evidence_urls") or []
    canonical_url = f"https://hackerone.com/reports/{card.get('report_id', '')}"
    if isinstance(evidence_urls, list) and canonical_url not in evidence_urls:
        errors.append("evidence_urls must include the matching canonical public HackerOne report URL")
    if card.get("analysis_status") in {"DEEPLY_REVIEWED", "EXACT_ROOT_EXTRACTED"}:
        for field in REQUIRED_CARD_FIELDS - {"report_id", "analysis_status", "evidence_urls"}:
            if not clean_text(card.get(field), 20000):
                errors.append(f"{field} is required for a reviewed card")
    if card.get("analysis_status") == "EXACT_ROOT_EXTRACTED":
        signature_parts = [part.strip() for part in str(card.get("duplicate_signature", "")).split("|")]
        if len(signature_parts) != 5 or not all(signature_parts):
            errors.append("EXACT_ROOT_EXTRACTED requires a complete five-part duplicate_signature")
    return errors


def load_cards(path: Path) -> list[dict[str, Any]]:
    parsed = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(parsed, dict):
        return [parsed]
    if isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
        return parsed
    raise ValueError("Card input must be a JSON object or array of objects")


def command_upsert_cards(args: argparse.Namespace) -> int:
    connection = connect_db(Path(args.db))
    cards = load_cards(Path(args.input))
    failures: list[dict[str, Any]] = []
    for card in cards:
        errors = validate_card(card)
        report_exists = connection.execute(
            "SELECT 1 FROM reports WHERE report_id=?", (str(card.get("report_id", "")),)
        ).fetchone()
        if not report_exists:
            errors.append("report_id does not exist in the metadata corpus")
        if errors:
            failures.append({"report_id": card.get("report_id"), "errors": errors})
    if failures:
        print(json.dumps({"status": "FAIL", "cards": failures}, indent=2), file=sys.stderr)
        return 2

    columns = [
        "report_id", "analysis_status", "attacker_start", "attacker_control",
        "entry_point", "primitive", "boundary", "enforcing_component", "sink",
        "capability_delta", "prerequisites", "proof_oracle", "root_cause",
        "chain_edges_json", "negative_controls_json", "patch_or_fix",
        "duplicate_signature", "evidence_urls_json", "analyst_notes", "updated_at",
    ]
    placeholders = ", ".join("?" for _ in columns)
    updates = ", ".join(f"{column}=excluded.{column}" for column in columns[1:])
    statement = (
        f"INSERT INTO analyst_cards ({', '.join(columns)}) VALUES ({placeholders}) "
        f"ON CONFLICT(report_id) DO UPDATE SET {updates}"
    )
    for card in cards:
        record = {
            **{field: clean_text(card.get(field), 20000) for field in CARD_FIELDS},
            "chain_edges_json": json.dumps(card.get("chain_edges") or [], ensure_ascii=False),
            "negative_controls_json": json.dumps(card.get("negative_controls") or [], ensure_ascii=False),
            "evidence_urls_json": json.dumps(card.get("evidence_urls") or [], ensure_ascii=False),
            "updated_at": now_utc(),
        }
        connection.execute(statement, [record.get(column, "") for column in columns])
    connection.commit()
    print(json.dumps({"status": "PASS", "cards_upserted": len(cards)}, indent=2))
    return 0


def search_haystack(row: sqlite3.Row) -> str:
    return " ".join(
        str(row[key] or "")
        for key in (
            "title", "hacktivity_summary", "cwe", "program_handle", "primitive",
            "boundary", "sink", "root_cause", "duplicate_signature",
        )
    ).lower()


def report_score(row: sqlite3.Row, terms: list[str], program: str, cwe: str, severity: str) -> int:
    score = 0
    if program and row["program_handle"].lower() == program.lower():
        score += 20
    if cwe and cwe.lower() in row["cwe"].lower():
        score += 12
    if severity and row["severity_rating"].lower() == severity.lower():
        score += 6
    haystack = search_haystack(row)
    for term in terms:
        score += min(haystack.count(term.lower()), 4) * 4
    if row["analysis_status"] == "EXACT_ROOT_EXTRACTED":
        score += 8
    elif row["analysis_status"] == "DEEPLY_REVIEWED":
        score += 5
    return score


def command_search(args: argparse.Namespace) -> int:
    connection = connect_db(Path(args.db))
    rows = connection.execute(
        """
        SELECT r.*, COALESCE(c.analysis_status, 'METADATA_ONLY') AS analysis_status,
               COALESCE(c.attacker_start, '') AS attacker_start,
               COALESCE(c.attacker_control, '') AS attacker_control,
               COALESCE(c.entry_point, '') AS entry_point,
               COALESCE(c.primitive, '') AS primitive,
               COALESCE(c.boundary, '') AS boundary,
               COALESCE(c.sink, '') AS sink,
               COALESCE(c.capability_delta, '') AS capability_delta,
               COALESCE(c.prerequisites, '') AS prerequisites,
               COALESCE(c.proof_oracle, '') AS proof_oracle,
               COALESCE(c.root_cause, '') AS root_cause,
               COALESCE(c.duplicate_signature, '') AS duplicate_signature
        FROM reports r LEFT JOIN analyst_cards c USING(report_id)
        """
    ).fetchall()
    terms = [term for term in args.terms.split() if term]
    scored: list[tuple[int, sqlite3.Row]] = []
    for row in rows:
        if args.program and row["program_handle"].lower() != args.program.lower():
            continue
        if args.cwe and args.cwe.lower() not in row["cwe"].lower():
            continue
        if args.severity and row["severity_rating"].lower() != args.severity.lower():
            continue
        if terms:
            haystack = search_haystack(row)
            matched_terms = sum(term.lower() in haystack for term in terms)
            if matched_terms < min(2, len(terms)):
                continue
        score = report_score(row, terms, args.program, args.cwe, args.severity)
        scored.append((score, row))
    scored.sort(
        key=lambda pair: (
            pair[0], pair[1]["votes"], pair[1]["total_awarded_amount"], pair[1]["disclosed_at"] or ""
        ),
        reverse=True,
    )
    output = []
    for score, row in scored[: args.limit]:
        output.append({
            "score": score,
            "report_id": row["report_id"],
            "title": row["title"],
            "url": row["url"],
            "program": row["program_handle"],
            "cwe": row["cwe"],
            "severity": row["severity_rating"],
            "bounty": row["total_awarded_amount"],
            "currency": row["currency"],
            "disclosed_at": row["disclosed_at"],
            "summary": clean_text(row["hacktivity_summary"], args.summary_chars),
            "analysis_status": row["analysis_status"],
            "attacker_start": row["attacker_start"],
            "attacker_control": row["attacker_control"],
            "entry_point": row["entry_point"],
            "primitive": row["primitive"],
            "boundary": row["boundary"],
            "sink": row["sink"],
            "capability_delta": row["capability_delta"],
            "prerequisites": row["prerequisites"],
            "proof_oracle": row["proof_oracle"],
            "root_cause": row["root_cause"],
            "duplicate_signature": row["duplicate_signature"],
        })
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


def command_stats(args: argparse.Namespace) -> int:
    connection = connect_db(Path(args.db))
    report_count = connection.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    card_count = connection.execute("SELECT COUNT(*) FROM analyst_cards").fetchone()[0]
    exact_count = connection.execute(
        "SELECT COUNT(*) FROM analyst_cards WHERE analysis_status='EXACT_ROOT_EXTRACTED'"
    ).fetchone()[0]
    programs = connection.execute(
        "SELECT COUNT(DISTINCT program_handle) FROM reports WHERE program_handle != ''"
    ).fetchone()[0]
    meta_rows = connection.execute("SELECT key, value FROM corpus_meta ORDER BY key").fetchall()
    metadata = {row["key"]: json.loads(row["value"]) for row in meta_rows}
    print(json.dumps({
        "reports": report_count,
        "programs": programs,
        "deep_cards": card_count,
        "exact_root_cards": exact_count,
        "metadata_only": report_count - card_count,
        "meta": metadata,
    }, indent=2))
    return 0


def fixture_item(report_id: int, disclosed: bool = True) -> dict[str, Any]:
    return {
        "id": report_id,
        "type": "report",
        "attributes": {
            "title": "Cross-tenant project export lacks an ownership check",
            "url": f"https://hackerone.com/reports/{report_id}",
            "disclosed_at": "2026-01-02T00:00:00Z",
            "submitted_at": "2025-12-01T00:00:00Z",
            "cve_ids": [],
            "cwe": "CWE-639 Authorization Bypass Through User-Controlled Key",
            "severity_rating": "high",
            "votes": 10,
            "total_awarded_amount": 5000,
            "disclosed": disclosed,
        },
        "relationships": {
            "report_generated_content": {"data": {"attributes": {
                "hacktivity_summary": "A project identifier selected another tenant's export."
            }}},
            "reporter": {"data": {"attributes": {"name": "Researcher", "username": "researcher"}}},
            "program": {"data": {"attributes": {
                "handle": "fixture", "name": "Fixture", "currency": "usd",
                "url": "https://hackerone.com/fixture"
            }}},
        },
    }


def command_self_test(_: argparse.Namespace) -> int:
    with tempfile.TemporaryDirectory(prefix="hacktivity-corpus-") as directory:
        database = Path(directory) / "corpus.sqlite3"
        connection = connect_db(database)
        ingested, skipped, skip_reasons = ingest_items(
            connection, [fixture_item(123), fixture_item(124, False)]
        )
        if (ingested, skipped) != (1, 1):
            raise AssertionError((ingested, skipped))
        if skip_reasons != {"not_disclosed": 1}:
            raise AssertionError(skip_reasons)
        ingest_items(connection, [fixture_item(123)])
        if connection.execute("SELECT COUNT(*) FROM reports").fetchone()[0] != 1:
            raise AssertionError("report deduplication failed")
        current_shape = fixture_item(123)
        current_shape["type"] = "hacktivity-item"
        del current_shape["attributes"]["disclosed"]
        variant_ingested, variant_skipped, _ = ingest_items(connection, [current_shape])
        if (variant_ingested, variant_skipped) != (1, 0):
            raise AssertionError("current Hacktivity response shape was rejected")
        safe_next = next_api_link(
            {"links": {"next": "/v1/hackers/hacktivity?page%5Bnumber%5D=2"}},
            API_ENDPOINT,
        )
        if not safe_next.startswith(API_ENDPOINT):
            raise AssertionError("safe pagination link was not accepted")
        try:
            next_api_link({"links": {"next": "https://example.com/steal"}}, API_ENDPOINT)
        except RuntimeError:
            pass
        else:
            raise AssertionError("cross-origin pagination link was accepted")
        if api_date_from_iso("2017-05-04T13:31:51.254Z") != "05-04-2017":
            raise AssertionError("disclosure cursor date conversion failed")
        real_api_request = api_request
        def fake_api_request(url: str, *_args: Any) -> dict[str, Any]:
            query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get(
                "queryString", [""]
            )[0]
            if "disclosed_at:<=05-04-2017" in query:
                raise RuntimeError("HackerOne API returned HTTP 400: invalid query")
            if "disclosed_at:<05-05-2017" in query:
                older_item = fixture_item(125)
                older_item["attributes"]["disclosed_at"] = "2017-05-04T00:00:00Z"
                return {"data": [older_item]}
            raise AssertionError(f"unexpected date-filter probe: {query}")
        try:
            globals()["api_request"] = fake_api_request
            chosen = choose_date_filter_style(
                ["disclosed:true"], "05-04-2017", "fixture", "fixture", 1, 0
            )
        finally:
            globals()["api_request"] = real_api_request
        if chosen != "lt_us_next":
            raise AssertionError(f"date-filter fallback failed: {chosen}")
        card = {
            "report_id": "123",
            "analysis_status": "EXACT_ROOT_EXTRACTED",
            "attacker_start": "low-privileged user",
            "attacker_control": "project identifier",
            "entry_point": "export endpoint",
            "primitive": "cross-tenant object reference",
            "boundary": "tenant ownership",
            "enforcing_component": "authorization middleware",
            "sink": "project export",
            "capability_delta": "read another tenant's protected export",
            "prerequisites": "valid low-privileged account",
            "proof_oracle": "victim-owned canary appears only in the cross-tenant response",
            "root_cause": "the handler loads by ID without comparing tenant ownership",
            "chain_edges": [],
            "negative_controls": ["same request using an unowned random identifier returns not found"],
            "patch_or_fix": "bind lookup to the authenticated tenant",
            "duplicate_signature": "project export|project identifier|missing ownership guard|export handler|cross-tenant read",
            "evidence_urls": ["https://hackerone.com/reports/123"],
            "analyst_notes": "Synthetic fixture only.",
        }
        if validate_card(card):
            raise AssertionError(validate_card(card))
        wrong_url = {**card, "evidence_urls": ["https://hackerone.com/reports/999"]}
        if not any("matching canonical" in error for error in validate_card(wrong_url)):
            raise AssertionError("a different report URL passed card validation")
        incomplete_signature = {**card, "duplicate_signature": "export|missing-owner-check|cross-tenant-read"}
        if not any("five-part" in error for error in validate_card(incomplete_signature)):
            raise AssertionError("an incomplete exact-root signature passed card validation")
        card_path = Path(directory) / "card.json"
        card_path.write_text(json.dumps(card), encoding="utf-8")
        args = argparse.Namespace(db=str(database), input=str(card_path))
        if command_upsert_cards(args) != 0:
            raise AssertionError("card upsert failed")
        row = connection.execute("SELECT duplicate_signature FROM analyst_cards").fetchone()
        if row[0] != card["duplicate_signature"]:
            raise AssertionError("card persistence failed")
    print(json.dumps({"HACKTIVITY_CORPUS_SELF_TEST": "PASS"}))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.set_defaults(function=None)
    subparsers = parser.add_subparsers(dest="command")

    sync = subparsers.add_parser("sync", help="Sync disclosed metadata from the official HackerOne API")
    sync.add_argument("--db", default=str(default_db_path()))
    sync.add_argument("--username-env", default="HACKERONE_API_USERNAME")
    sync.add_argument("--token-env", default="HACKERONE_API_TOKEN")
    sync.add_argument("--query", default="", help="Additional documented Lucene filters")
    sync.add_argument("--since", default="", help="Only reports disclosed on/after YYYY-MM-DD")
    sync.add_argument("--sort", default="-disclosed_at", choices=[
        "latest_disclosable_activity_at", "-latest_disclosable_activity_at",
        "disclosed_at", "-disclosed_at", "total_awarded_amount",
        "-total_awarded_amount", "votes", "-votes",
    ])
    sync.add_argument("--page-size", type=int, default=100, choices=range(1, 101))
    sync.add_argument("--start-page", type=int, default=1)
    sync.add_argument("--max-pages", type=int, default=1)
    sync.add_argument("--all-pages", action="store_true", help="Walk the complete disclosed feed")
    sync.add_argument(
        "--resume-older",
        action="store_true",
        help="Continue backward from the oldest dated report already in the corpus",
    )
    sync.add_argument(
        "--window-page-limit",
        type=int,
        default=99,
        help="Rotate to an older disclosure-date window before the API result-window ceiling",
    )
    sync.add_argument("--hard-page-cap", type=int, default=10000)
    sync.add_argument("--min-interval", type=float, default=1.25)
    sync.add_argument("--timeout", type=float, default=30.0)
    sync.add_argument("--retries", type=int, default=4)
    sync.set_defaults(function=command_sync)

    import_parser = subparsers.add_parser("import", help="Import a saved official API response")
    import_parser.add_argument("--db", default=str(default_db_path()))
    import_parser.add_argument("--input", required=True)
    import_parser.set_defaults(function=command_import)

    cards = subparsers.add_parser("upsert-cards", help="Validate and store semantic learning cards")
    cards.add_argument("--db", default=str(default_db_path()))
    cards.add_argument("--input", required=True)
    cards.set_defaults(function=command_upsert_cards)

    search = subparsers.add_parser("search", help="Retrieve a small relevant context pack")
    search.add_argument("--db", default=str(default_db_path()))
    search.add_argument("--terms", default="")
    search.add_argument("--program", default="")
    search.add_argument("--cwe", default="")
    search.add_argument("--severity", default="")
    search.add_argument("--limit", type=int, default=12, choices=range(1, 51))
    search.add_argument("--summary-chars", type=int, default=1200)
    search.set_defaults(function=command_search)

    stats = subparsers.add_parser("stats", help="Show corpus coverage and sync state")
    stats.add_argument("--db", default=str(default_db_path()))
    stats.set_defaults(function=command_stats)

    self_test = subparsers.add_parser("self-test", help="Run an offline deterministic smoke test")
    self_test.set_defaults(function=command_self_test)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.function is None:
        parser.print_help()
        return 2
    try:
        return int(args.function(args))
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
