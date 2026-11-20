#!/usr/bin/env python3
"""Build and query a bounded corpus of public vulnerability disclosures.

The corpus is an index, not an exploit runner and not target authorization.  It
stores public metadata and short summaries from automatic public sources plus
reviewer-supplied exports from sources that require an ordinary browser session:

* Google Bug Hunters public reports
* Disclosure Index (bug-bounty-disclosures.vercel.app)
* Bug Bounty Daily
* RedLimit BBRD (wu.redlimit.id), through an explicit JSON/CSV/HAR import

Full third-party articles are deliberately not mirrored.  Open the canonical
source and create a reviewed semantic card before treating a record as an
exact-root prior-art match.
"""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import hashlib
import html
import json
import os
import re
import sqlite3
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable


DISCLOSURE_INDEX_URL = "https://bug-bounty-disclosures.vercel.app/data/catalog.js"
GOOGLE_SEARCH_URL = "https://bughunters.google.com/rest/v1/reports/search"
GOOGLE_REPORT_URL = "https://bughunters.google.com/report/reports/{report_id}"
BUG_BOUNTY_DAILY_URL = "https://bugbountydaily.com/"
REDLIMIT_BBRD_URL = "https://wu.redlimit.id/database"
DEFAULT_TIMEOUT = 45
DEFAULT_LIMIT = 12
MAX_CONTEXT_RECORDS = 12
USER_AGENT = "Codex-Public-Disclosure-Corpus/1.0"
CARD_STATUSES = {
    "DEEPLY_REVIEWED",
    "EXACT_ROOT_EXTRACTED",
    "STALE_NEEDS_REVIEW",
    "REJECTED_INSUFFICIENT_EVIDENCE",
}
CARD_REQUIRED = {
    "source",
    "source_id",
    "canonical_url",
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
REDLIMIT_URL_FIELDS = (
    "url",
    "URL",
    "link",
    "writeup_url",
    "writeupUrl",
    "report_url",
    "reportUrl",
    "source_url",
    "sourceUrl",
)
REDLIMIT_SUMMARY_FIELDS = (
    "Impact",
    "Root cause",
    "Functionality",
    "BugClass",
    "Type",
    "Attack vector",
    "Attack Vector",
    "Escalation Type",
    "Required permissions",
    "Bypass method",
    "Technique",
    "Reason",
    "Target Type",
    "Dos Type",
    "Parameter Location",
    "GQL operation type",
)
REDLIMIT_ATTRIBUTE_FIELDS = {
    "category": ("_category", "category", "Category"),
    "bug_class": ("BugClass",),
    "attack_vector": ("Attack vector", "Attack Vector", "attack vector"),
    "blind": ("blind?",),
    "csp_bypass": ("csp bypass",),
    "filter_bypass": ("filter bypass?", "Filter bypass"),
    "user_interaction": ("user-interaction",),
    "reason": ("reason", "Reason"),
    "type": ("type", "Type"),
    "functionality": ("Functionality",),
    "root_cause": ("Root cause",),
    "attacker_knowledge": ("Attacker's knowledge about a victim",),
    "takeover_method": ("The way to takeover account",),
    "victim_interaction": ("Victim's interaction",),
    "side": ("Side",),
    "csrf_prevention": ("CSRF prevention mechanism",),
    "http_method": ("HTTP Method",),
    "same_site": ("SameSite",),
    "identifier_type": ("ID Type",),
    "identifier_prediction": ("Way to predict the identifier",),
    "parameter_location": ("Parameter Location", "parameter name", "Parameter", "Parameter name"),
    "bypass": ("Bypass method", "Bypass"),
    "dos_type": ("Dos Type",),
    "cache_poisoning_vector": ("Cache poisoning vector",),
    "target_type": ("Target Type",),
    "db_engine": ("DB engine",),
    "exfiltration_optimisation": ("Exfiltration optimisation",),
    "tool": ("Tool",),
    "file_written": ("File wrote",),
    "read_file": ("Read file",),
    "rce_escalation": ("RCE escalation method",),
    "gql_operation": ("GQL operation type",),
    "introspection": ("Introspection",),
    "technique": ("Technique",),
    "escalation_type": ("Escalation Type",),
    "identifier_knowledge": ("How does the attacker know the identifier?",),
    "required_permissions": ("Required permissions",),
    "affected_version": ("Affected Version",),
    "browser": ("Browser",),
    "cve": ("CVE",),
    "source_severity": ("Severity",),
    "impact": ("Impact", "impact"),
}
REDLIMIT_INSIGHT_ATTRIBUTES = (
    "root_cause",
    "attack_vector",
    "functionality",
    "required_permissions",
    "victim_interaction",
    "bypass",
    "filter_bypass",
    "technique",
    "rce_escalation",
    "impact",
)


def default_db_path() -> Path:
    data_home = os.environ.get("XDG_DATA_HOME")
    root = Path(data_home) if data_home else Path.home() / ".local" / "share"
    return root / "codex" / "public-disclosures" / "corpus.sqlite3"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def json_list(value: Any) -> str:
    if not value:
        return "[]"
    if isinstance(value, list):
        values = value
    else:
        values = [value]
    return json.dumps([text(item) for item in values if text(item)], ensure_ascii=False)


def short_summary(value: Any, limit: int = 900) -> str:
    raw = html.unescape(text(value))
    raw = re.sub(r"```.*?```", " ", raw, flags=re.DOTALL)
    raw = re.sub(r"`([^`]*)`", r"\1", raw)
    raw = re.sub(r"!\[[^]]*]\([^)]*\)", " ", raw)
    raw = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"[#>*_|~-]+", " ", raw)
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw[:limit]


def bounded_attribute_value(value: Any, limit: int = 320) -> str:
    """Bound an already-structured value without changing identifiers."""
    raw = html.unescape(text(value))
    raw = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", raw)
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw[:limit]


def markdown_field(body: Any, label: str) -> str:
    match = re.search(
        rf"(?im)^\s*(?:\*\*)?{re.escape(label)}(?:\*\*)?\s*:\s*(.+?)\s*$",
        text(body),
    )
    return short_summary(match.group(1), 240) if match else ""


def canonical_url(value: Any) -> str:
    raw = text(value)
    if not raw:
        return ""
    try:
        parsed = urllib.parse.urlsplit(raw)
    except ValueError:
        return raw
    host = (parsed.hostname or "").lower()
    port = parsed.port
    netloc = host
    if port and not ((parsed.scheme == "https" and port == 443) or (parsed.scheme == "http" and port == 80)):
        netloc = f"{host}:{port}"
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    return urllib.parse.urlunsplit((parsed.scheme.lower(), netloc, path, parsed.query, ""))


def sha256_json(value: Any) -> str:
    blob = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def request_bytes(
    url: str,
    *,
    timeout: int,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[bytes, dict[str, str]]:
    merged = {"User-Agent": USER_AGENT, "Accept": "application/json,text/html,*/*"}
    if headers:
        merged.update(headers)
    req = urllib.request.Request(url, data=data, headers=merged)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read()
        response_headers = {key.lower(): value for key, value in response.headers.items()}
    return body, response_headers


def request_json(
    url: str,
    *,
    timeout: int,
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[Any, dict[str, str]]:
    data = None
    merged = dict(headers or {})
    if payload is not None:
        data = json.dumps(payload).encode()
        merged["Content-Type"] = "application/json"
    body, response_headers = request_bytes(url, timeout=timeout, data=data, headers=merged)
    return json.loads(body.decode("utf-8")), response_headers


SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS reports (
  source TEXT NOT NULL,
  source_id TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  normalized_url TEXT NOT NULL,
  program TEXT NOT NULL DEFAULT '',
  researcher TEXT NOT NULL DEFAULT '',
  platform TEXT NOT NULL DEFAULT '',
  vulnerability_class TEXT NOT NULL DEFAULT '',
  weakness TEXT NOT NULL DEFAULT '',
  severity TEXT NOT NULL DEFAULT '',
  bounty TEXT NOT NULL DEFAULT '',
  published_at TEXT NOT NULL DEFAULT '',
  kind TEXT NOT NULL DEFAULT '',
  cves_json TEXT NOT NULL DEFAULT '[]',
  tags_json TEXT NOT NULL DEFAULT '[]',
  summary TEXT NOT NULL DEFAULT '',
  evidence_tier TEXT NOT NULL DEFAULT 'METADATA_ONLY',
  indexed_via TEXT NOT NULL DEFAULT '',
  source_digest TEXT NOT NULL,
  synced_at TEXT NOT NULL,
  PRIMARY KEY (source, source_id)
);
CREATE INDEX IF NOT EXISTS reports_program_idx ON reports(program);
CREATE INDEX IF NOT EXISTS reports_severity_idx ON reports(severity);
CREATE INDEX IF NOT EXISTS reports_class_idx ON reports(vulnerability_class);
CREATE INDEX IF NOT EXISTS reports_url_idx ON reports(normalized_url);
CREATE TABLE IF NOT EXISTS sync_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  started_at TEXT NOT NULL,
  finished_at TEXT NOT NULL,
  status TEXT NOT NULL,
  received INTEGER NOT NULL,
  upserted INTEGER NOT NULL,
  declared_total INTEGER,
  note TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS analyst_cards (
  source TEXT NOT NULL,
  source_id TEXT NOT NULL,
  canonical_url TEXT NOT NULL,
  analysis_status TEXT NOT NULL,
  attacker_start TEXT NOT NULL,
  attacker_control TEXT NOT NULL,
  entry_point TEXT NOT NULL,
  primitive TEXT NOT NULL,
  boundary TEXT NOT NULL,
  enforcing_component TEXT NOT NULL DEFAULT '',
  sink TEXT NOT NULL,
  capability_delta TEXT NOT NULL,
  prerequisites TEXT NOT NULL,
  proof_oracle TEXT NOT NULL,
  root_cause TEXT NOT NULL,
  chain_edges_json TEXT NOT NULL DEFAULT '[]',
  negative_controls_json TEXT NOT NULL DEFAULT '[]',
  patch_or_fix TEXT NOT NULL DEFAULT '',
  current_reachability TEXT NOT NULL DEFAULT '',
  duplicate_signature TEXT NOT NULL,
  evidence_urls_json TEXT NOT NULL,
  analyst_notes TEXT NOT NULL DEFAULT '',
  updated_at TEXT NOT NULL,
  PRIMARY KEY (source, source_id),
  FOREIGN KEY (source, source_id) REFERENCES reports(source, source_id)
);
CREATE INDEX IF NOT EXISTS cards_signature_idx ON analyst_cards(duplicate_signature);
CREATE TABLE IF NOT EXISTS report_attributes (
  source TEXT NOT NULL,
  source_id TEXT NOT NULL,
  attribute TEXT NOT NULL,
  value TEXT NOT NULL,
  normalized_value TEXT NOT NULL,
  PRIMARY KEY (source, source_id, attribute),
  FOREIGN KEY (source, source_id) REFERENCES reports(source, source_id)
);
CREATE INDEX IF NOT EXISTS report_attributes_name_idx
  ON report_attributes(attribute, normalized_value);
CREATE INDEX IF NOT EXISTS report_attributes_record_idx
  ON report_attributes(source, source_id);
"""


def connect(db_path: Path | str) -> sqlite3.Connection:
    if str(db_path) != ":memory:":
        Path(db_path).expanduser().parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def normalized_record(source: str, raw: dict[str, Any]) -> dict[str, str]:
    url = canonical_url(raw.get("url"))
    record = {
        "source": source,
        "source_id": text(raw.get("source_id")),
        "title": text(raw.get("title")) or "Untitled public disclosure",
        "url": url,
        "normalized_url": url,
        "program": text(raw.get("program")),
        "researcher": text(raw.get("researcher")),
        "platform": text(raw.get("platform")),
        "vulnerability_class": text(raw.get("vulnerability_class")),
        "weakness": text(raw.get("weakness")),
        "severity": text(raw.get("severity")) or "Unrated",
        "bounty": text(raw.get("bounty")),
        "published_at": text(raw.get("published_at")),
        "kind": text(raw.get("kind")),
        "cves_json": json_list(raw.get("cves")),
        "tags_json": json_list(raw.get("tags")),
        "summary": short_summary(raw.get("summary")),
        "evidence_tier": text(raw.get("evidence_tier")) or "METADATA_ONLY",
        "indexed_via": text(raw.get("indexed_via")),
        "synced_at": now_iso(),
    }
    digest_basis = {key: value for key, value in record.items() if key not in {"synced_at", "source_digest"}}
    record["source_digest"] = sha256_json(digest_basis)
    return record


UPSERT = """
INSERT INTO reports (
  source, source_id, title, url, normalized_url, program, researcher,
  platform, vulnerability_class, weakness, severity, bounty, published_at,
  kind, cves_json, tags_json, summary, evidence_tier, indexed_via,
  source_digest, synced_at
) VALUES (
  :source, :source_id, :title, :url, :normalized_url, :program, :researcher,
  :platform, :vulnerability_class, :weakness, :severity, :bounty,
  :published_at, :kind, :cves_json, :tags_json, :summary, :evidence_tier,
  :indexed_via, :source_digest, :synced_at
)
ON CONFLICT(source, source_id) DO UPDATE SET
  title=excluded.title, url=excluded.url, normalized_url=excluded.normalized_url,
  program=excluded.program, researcher=excluded.researcher,
  platform=excluded.platform, vulnerability_class=excluded.vulnerability_class,
  weakness=excluded.weakness, severity=excluded.severity, bounty=excluded.bounty,
  published_at=excluded.published_at, kind=excluded.kind,
  cves_json=excluded.cves_json, tags_json=excluded.tags_json,
  summary=excluded.summary, indexed_via=excluded.indexed_via,
  source_digest=excluded.source_digest, synced_at=excluded.synced_at
"""


def upsert_records(con: sqlite3.Connection, records: Iterable[dict[str, str]]) -> int:
    count = 0
    for record in records:
        if not record["source_id"]:
            continue
        con.execute(UPSERT, record)
        count += 1
    con.commit()
    return count


def sync_disclosure_index(timeout: int) -> tuple[list[dict[str, str]], int, str]:
    body, _ = request_bytes(DISCLOSURE_INDEX_URL, timeout=timeout)
    payload = body.decode("utf-8")
    prefix = "window.DISCLOSURE_REPORTS="
    if not payload.startswith(prefix):
        raise ValueError("Disclosure Index catalog wrapper changed")
    raw_records = json.loads(payload[len(prefix) :].strip().rstrip(";"))
    if not isinstance(raw_records, list):
        raise ValueError("Disclosure Index catalog is not a list")
    records = []
    for item in raw_records:
        records.append(
            normalized_record(
                "disclosure-index",
                {
                    "source_id": item.get("id"),
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "program": item.get("program"),
                    "researcher": item.get("researcher"),
                    "platform": item.get("platform"),
                    "vulnerability_class": item.get("vulnerabilityClass"),
                    "weakness": item.get("weakness"),
                    "severity": item.get("severity"),
                    "bounty": item.get("bounty"),
                    "published_at": item.get("disclosedAt"),
                    "kind": item.get("kind"),
                    "cves": item.get("cves"),
                    "summary": item.get("outcome") or item.get("sourceOutcome"),
                    "indexed_via": item.get("indexedVia"),
                },
            )
        )
    return records, len(raw_records), "static catalog fully parsed"


def sync_google(timeout: int, page_size: int = 100) -> tuple[list[dict[str, str]], int, str]:
    seen: dict[str, dict[str, str]] = {}
    declared_total = 0
    page_index = 0
    while True:
        payload = {
            "pageSize": page_size,
            "pageIndex": page_index,
            "sort": "created",
            "order": "DESC",
        }
        result, _ = request_json(GOOGLE_SEARCH_URL, timeout=timeout, payload=payload)
        items = result.get("items") or []
        declared_total = max(declared_total, int(result.get("totalSize") or 0))
        for item in items:
            report_id = text(item.get("id"))
            body = text(item.get("body"))
            metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
            record = normalized_record(
                "google-bughunters",
                {
                    "source_id": report_id,
                    "title": item.get("title"),
                    "url": GOOGLE_REPORT_URL.format(report_id=report_id),
                    "program": markdown_field(body, "Program") or item.get("program"),
                    "researcher": item.get("authorName"),
                    "platform": "Google Bug Hunters",
                    "vulnerability_class": markdown_field(body, "Vulnerability type")
                    or metadata.get("category"),
                    "weakness": metadata.get("subcategory"),
                    "severity": metadata.get("severity"),
                    "bounty": item.get("reward"),
                    "published_at": item.get("created"),
                    "kind": "Vendor-published report",
                    "summary": body,
                    "indexed_via": "Google Bug Hunters public reports API",
                    "evidence_tier": "PUBLIC_REPORT_SUMMARY",
                },
            )
            seen[report_id] = record
        page_index += 1
        if not items or page_index > 1000:
            break
    note = f"public walk terminal page reached; API declared {declared_total}, exposed {len(seen)}"
    return list(seen.values()), declared_total, note


def extract_bbd_client_config(homepage: str) -> tuple[str, str]:
    match = re.search(r'<script type="importmap">(.*?)</script>', homepage, re.DOTALL)
    if not match:
        raise ValueError("Bug Bounty Daily import map not found")
    imports = json.loads(match.group(1)).get("imports", {})
    module_url = imports.get("@/lib/supabase", "")
    if not module_url.startswith("data:application/javascript;base64,"):
        raise ValueError("Bug Bounty Daily Supabase module missing")
    module = base64.b64decode(module_url.split(",", 1)[1]).decode("utf-8")
    url_match = re.search(r"supabaseUrl\s*=\s*['\"]([^'\"]+)", module)
    key_match = re.search(r"supabaseAnonKey\s*=\s*['\"]([^'\"]+)", module)
    if not url_match or not key_match:
        raise ValueError("Bug Bounty Daily public client configuration changed")
    return url_match.group(1), key_match.group(1)


def sync_bug_bounty_daily(timeout: int, page_size: int = 1000) -> tuple[list[dict[str, str]], int, str]:
    home, _ = request_bytes(BUG_BOUNTY_DAILY_URL, timeout=timeout)
    supabase_url, anon_key = extract_bbd_client_config(home.decode("utf-8"))
    records: list[dict[str, str]] = []
    offset = 0
    declared_total = 0
    while True:
        query = urllib.parse.urlencode(
            {
                "select": "id,title,url,created_at,original_created_at,description",
                "order": "created_at.desc",
                "limit": page_size,
                "offset": offset,
            }
        )
        items, headers = request_json(
            f"{supabase_url}/rest/v1/links?{query}",
            timeout=timeout,
            headers={"apikey": anon_key, "Prefer": "count=exact"},
        )
        content_range = headers.get("content-range", "")
        total_match = re.search(r"/(\d+)$", content_range)
        if total_match:
            declared_total = max(declared_total, int(total_match.group(1)))
        for item in items:
            host = urllib.parse.urlsplit(text(item.get("url"))).hostname or ""
            records.append(
                normalized_record(
                    "bug-bounty-daily",
                    {
                        "source_id": item.get("id"),
                        "title": item.get("title"),
                        "url": item.get("url"),
                        "program": host,
                        "platform": "Bug Bounty Daily",
                        "published_at": item.get("original_created_at") or item.get("created_at"),
                        "kind": "Curated security article",
                        "summary": item.get("description"),
                        "indexed_via": "Bug Bounty Daily public links table",
                    },
                )
            )
        offset += len(items)
        if not items or len(items) < page_size:
            break
    if not declared_total:
        declared_total = len(records)
    return records, declared_total, "public table walk reached terminal page"


def first_present(item: dict[str, Any], *names: str) -> Any:
    for name in names:
        value = item.get(name)
        if value is not None and text(value):
            return value
    return ""


def imported_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [text(item) for item in value if text(item)]
    raw = text(value)
    if not raw:
        return []
    if raw.startswith("["):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [text(item) for item in parsed if text(item)]
        except json.JSONDecodeError:
            pass
    return [part.strip() for part in re.split(r"[,;|]", raw) if part.strip()]


def redlimit_summary(item: dict[str, Any]) -> str:
    explicit = first_present(item, "summary", "Summary", "description", "Description", "outcome", "excerpt")
    if explicit:
        return text(explicit)
    parts = []
    for field in REDLIMIT_SUMMARY_FIELDS:
        value = short_summary(item.get(field), 240)
        if value:
            parts.append(f"{field}: {value}")
    return "; ".join(parts)


def redlimit_source_id(item: dict[str, Any], url: str) -> str:
    source_id = text(first_present(item, "id", "ID", "_id", "report_id", "reportId", "uuid", "slug"))
    if source_id:
        return source_id
    identity = {
        "url": url,
        "title": first_present(item, "title", "Title", "name", "Name"),
        "category": first_present(item, "_category", "category", "Category", "BugClass"),
        "date": first_present(item, "date", "Date", "Year", "_year"),
        "program": first_present(item, "program", "Program", "Browser"),
    }
    return sha256_json(identity)[:24]


def redlimit_structured_attributes(item: dict[str, Any]) -> dict[str, str]:
    """Return bounded analytical metadata; never retain payload/proof/comment fields."""
    attributes: dict[str, str] = {}
    for canonical_name, aliases in REDLIMIT_ATTRIBUTE_FIELDS.items():
        values = []
        for alias in aliases:
            value = bounded_attribute_value(item.get(alias), 320)
            if value and value not in values:
                values.append(value)
        if values:
            attributes[canonical_name] = " | ".join(values)
    return attributes


def replace_report_attributes(
    con: sqlite3.Connection,
    source: str,
    attributes_by_source_id: dict[str, dict[str, str]],
) -> int:
    count = 0
    for source_id, attributes in attributes_by_source_id.items():
        con.execute(
            "DELETE FROM report_attributes WHERE source=? AND source_id=?",
            (source, source_id),
        )
        for attribute, value in attributes.items():
            normalized_value = re.sub(r"\s+", " ", value).strip().lower()
            con.execute(
                """INSERT INTO report_attributes
                   (source, source_id, attribute, value, normalized_value)
                   VALUES (?, ?, ?, ?, ?)""",
                (source, source_id, attribute, value, normalized_value),
            )
            count += 1
    con.commit()
    return count


def record_attributes(con: sqlite3.Connection, source: str, source_id: str) -> dict[str, str]:
    rows = con.execute(
        """SELECT attribute, value FROM report_attributes
           WHERE source=? AND source_id=? ORDER BY attribute""",
        (source, source_id),
    )
    return {row["attribute"]: row["value"] for row in rows}


def redlimit_records_in_payload(payload: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict) and (
                any(text(item.get(name)) for name in REDLIMIT_URL_FIELDS)
                or (
                    text(first_present(item, "title", "Title"))
                    and text(first_present(item, "_category", "category", "Category"))
                )
            ):
                found.append(item)
            elif isinstance(item, (dict, list)):
                found.extend(redlimit_records_in_payload(item))
    elif isinstance(payload, dict):
        for value in payload.values():
            if isinstance(value, (dict, list)):
                found.extend(redlimit_records_in_payload(value))
    return found


def load_redlimit_har(input_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    entries = payload.get("log", {}).get("entries", []) if isinstance(payload, dict) else []
    if not isinstance(entries, list):
        raise ValueError("RedLimit HAR has no log.entries list")
    found: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        request_url = text(entry.get("request", {}).get("url"))
        if (urllib.parse.urlsplit(request_url).hostname or "").lower() != "wu.redlimit.id":
            continue
        content = entry.get("response", {}).get("content", {})
        body = text(content.get("text")) if isinstance(content, dict) else ""
        if not body:
            continue
        if text(content.get("encoding")).lower() == "base64":
            try:
                body = base64.b64decode(body).decode("utf-8")
            except (ValueError, UnicodeDecodeError):
                continue
        try:
            response_payload = json.loads(body)
        except json.JSONDecodeError:
            continue
        found.extend(redlimit_records_in_payload(response_payload))
    if not found:
        raise ValueError("RedLimit HAR contains no JSON response records with canonical write-up URLs")
    return found


def load_redlimit_export(input_path: Path) -> list[dict[str, Any]]:
    suffix = input_path.suffix.lower()
    if suffix == ".har":
        return load_redlimit_har(input_path)
    if suffix == ".csv":
        with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
            items = [dict(row) for row in csv.DictReader(handle)]
        if not items:
            raise ValueError("RedLimit CSV export contains no records")
        return items
    if suffix != ".json":
        raise ValueError("RedLimit import accepts only .json, .csv, or .har exports")
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        items = None
        for key in ("reports", "items", "results", "records", "data"):
            candidate = payload.get(key)
            if isinstance(candidate, list):
                items = candidate
                break
            if isinstance(candidate, dict):
                for nested in ("reports", "items", "results", "records", "docs"):
                    if isinstance(candidate.get(nested), list):
                        items = candidate[nested]
                        break
            if items is not None:
                break
        if items is None:
            raise ValueError("RedLimit JSON export has no reports/items/results/records/data list")
    else:
        raise ValueError("RedLimit JSON export must be a list or object containing a record list")
    if not all(isinstance(item, dict) for item in items):
        raise ValueError("RedLimit export records must be objects")
    if not items:
        raise ValueError("RedLimit export contains no records")
    return items


def normalize_redlimit_export(
    raw_records: list[dict[str, Any]],
) -> tuple[list[dict[str, str]], dict[str, dict[str, str]], list[dict[str, Any]]]:
    records: dict[str, dict[str, str]] = {}
    attributes_by_source_id: dict[str, dict[str, str]] = {}
    rejected: list[dict[str, Any]] = []
    for index, item in enumerate(raw_records, start=1):
        raw_url = first_present(item, *REDLIMIT_URL_FIELDS)
        url = canonical_url(raw_url)
        parsed = urllib.parse.urlsplit(url)
        has_canonical_url = parsed.scheme in {"http", "https"} and bool(parsed.hostname)
        if not has_canonical_url:
            url = ""
            if not (
                text(first_present(item, "title", "Title"))
                and text(first_present(item, "_category", "category", "Category"))
            ):
                rejected.append(
                    {"record": index, "reason": "missing canonical URL and source category identity"}
                )
                continue
        source_id = redlimit_source_id(item, url)
        vulnerability_class = first_present(
            item,
            "vulnerability_class",
            "vulnerabilityClass",
            "category",
            "type",
            "bug_type",
            "bugType",
            "_category",
            "Category",
            "BugClass",
        )
        tags = imported_list(first_present(item, "tags", "Tags", "labels", "Labels"))
        for tag_field in ("_category", "BugClass", "Type", "Status"):
            tag = text(item.get(tag_field))
            if tag and tag not in tags:
                tags.append(tag)
        if not has_canonical_url:
            tags.append("NO_CANONICAL_SOURCE_URL")
        cves = imported_list(first_present(item, "cves", "CVEs", "cve", "CVE", "cve_ids", "cveIds"))
        record = normalized_record(
            "redlimit-bbrd",
            {
                "source_id": source_id,
                "title": first_present(item, "title", "Title", "name", "Name", "report_title", "reportTitle"),
                "url": url,
                "program": first_present(item, "program", "Program", "target", "Target", "company", "vendor"),
                "researcher": first_present(
                    item,
                    "researcher",
                    "Researcher",
                    "author",
                    "Author",
                    "Authors",
                    "hunter",
                    "reported_by",
                ),
                "platform": first_present(item, "platform", "source_platform", "sourcePlatform")
                or "RedLimit BBRD",
                "vulnerability_class": vulnerability_class,
                "weakness": first_present(item, "weakness", "Weakness", "cwe", "CWE", "cwe_id", "cweId"),
                "severity": first_present(item, "severity", "Severity", "priority", "Priority", "rating"),
                "bounty": first_present(item, "bounty", "Bounty", "reward", "Reward", "amount", "payout"),
                "published_at": first_present(
                    item,
                    "published_at",
                    "publishedAt",
                    "disclosed_at",
                    "disclosedAt",
                    "date",
                    "Date",
                    "Year",
                    "created_at",
                    "createdAt",
                ),
                "kind": first_present(item, "kind", "source_type", "sourceType")
                or "Curated public bug-bounty write-up",
                "cves": cves,
                "tags": tags,
                "summary": redlimit_summary(item),
                "indexed_via": (
                    "RedLimit BBRD reviewer-supplied JSON/CSV/HAR export"
                    if has_canonical_url
                    else "RedLimit BBRD source metadata without a canonical external write-up URL"
                ),
                "evidence_tier": "METADATA_ONLY",
            },
        )
        records[source_id] = record
        attributes_by_source_id[source_id] = redlimit_structured_attributes(item)
    return list(records.values()), attributes_by_source_id, rejected


def import_redlimit_export(
    con: sqlite3.Connection,
    input_path: Path,
    declared_total: int | None,
) -> dict[str, Any]:
    started = now_iso()
    raw_records = load_redlimit_export(input_path)
    records, attributes_by_source_id, rejected = normalize_redlimit_export(raw_records)
    upserted = upsert_records(con, records)
    attribute_facts = replace_report_attributes(con, "redlimit-bbrd", attributes_by_source_id)
    status = "PASS" if not rejected else ("PARTIAL" if records else "FAIL")
    note = (
        "authorized browser/export import; request headers/cookies ignored; no login, anti-bot, or Cloudflare bypass; "
        f"rejected={len(rejected)}"
    )
    con.execute(
        """INSERT INTO sync_runs
           (source, started_at, finished_at, status, received, upserted, declared_total, note)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            "redlimit-bbrd",
            started,
            now_iso(),
            status,
            len(raw_records),
            upserted,
            declared_total,
            note,
        ),
    )
    con.commit()
    return {
        "source": "redlimit-bbrd",
        "status": status,
        "received": len(raw_records),
        "upserted": upserted,
        "rejected": rejected[:20],
        "rejected_count": len(rejected),
        "declared_total": declared_total,
        "structured_rows": len(attributes_by_source_id),
        "attribute_facts": attribute_facts,
        "source_url": REDLIMIT_BBRD_URL,
        "note": note,
    }


SYNCERS = {
    "disclosure-index": sync_disclosure_index,
    "google-bughunters": sync_google,
    "bug-bounty-daily": sync_bug_bounty_daily,
}


def sync_sources(con: sqlite3.Connection, sources: list[str], timeout: int) -> int:
    failures = 0
    for source in sources:
        started = now_iso()
        received = upserted = 0
        declared_total: int | None = None
        note = ""
        status = "PASS"
        try:
            records, declared_total, note = SYNCERS[source](timeout)
            received = len(records)
            upserted = upsert_records(con, records)
        except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError) as exc:
            failures += 1
            status = "FAIL"
            note = f"{type(exc).__name__}: {exc}"
        con.execute(
            """INSERT INTO sync_runs
               (source, started_at, finished_at, status, received, upserted, declared_total, note)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (source, started, now_iso(), status, received, upserted, declared_total, note),
        )
        con.commit()
        print(
            json.dumps(
                {
                    "source": source,
                    "status": status,
                    "received": received,
                    "upserted": upserted,
                    "declared_total": declared_total,
                    "note": note,
                },
                ensure_ascii=False,
            )
        )
    return failures


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    value = dict(row)
    for key in (
        "cves_json",
        "tags_json",
        "chain_edges_json",
        "negative_controls_json",
        "evidence_urls_json",
    ):
        if key in value:
            value[key.removesuffix("_json")] = json.loads(value.pop(key) or "[]")
    return value


def search(con: sqlite3.Connection, args: argparse.Namespace) -> list[dict[str, Any]]:
    clauses = []
    params: list[Any] = []
    filters = [
        ("source", args.source),
        ("program", args.program),
        ("severity", args.severity),
        ("vulnerability_class", args.vulnerability_class),
    ]
    for column, value in filters:
        if value:
            clauses.append(f"lower(r.{column}) LIKE ?")
            params.append(f"%{value.lower()}%")
    searchable = (
        "r.title || ' ' || r.program || ' ' || r.researcher || ' ' || r.platform || ' ' || "
        "r.vulnerability_class || ' ' || r.weakness || ' ' || r.summary || ' ' || r.cves_json || ' ' || "
        "COALESCE(c.primitive, '') || ' ' || COALESCE(c.boundary, '') || ' ' || "
        "COALESCE(c.sink, '') || ' ' || COALESCE(c.root_cause, '') || ' ' || "
        "COALESCE(c.duplicate_signature, '') || ' ' || COALESCE(a.attributes_text, '')"
    )
    for term in re.findall(r'"[^"]+"|\S+', args.terms or ""):
        clean = term.strip('"').lower()
        if clean:
            clauses.append(f"lower({searchable}) LIKE ?")
            params.append(f"%{clean}%")
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    limit = min(max(1, args.limit), MAX_CONTEXT_RECORDS)
    sql = (
        "SELECT r.source, r.source_id, r.title, r.url, r.program, r.researcher, r.platform, "
        "r.vulnerability_class, r.weakness, r.severity, r.bounty, r.published_at, r.kind, "
        "r.cves_json, r.tags_json, r.summary, r.evidence_tier, r.indexed_via, "
        "COALESCE(c.analysis_status, 'METADATA_ONLY') analysis_status, "
        "COALESCE(c.duplicate_signature, '') duplicate_signature "
        "FROM reports r LEFT JOIN analyst_cards c "
        "ON r.source=c.source AND r.source_id=c.source_id "
        "LEFT JOIN (SELECT source, source_id, "
        "GROUP_CONCAT(attribute || ' ' || value, ' ') attributes_text "
        "FROM report_attributes GROUP BY source, source_id) a "
        "ON r.source=a.source AND r.source_id=a.source_id"
        f"{where} ORDER BY CASE COALESCE(c.analysis_status, '') "
        "WHEN 'EXACT_ROOT_EXTRACTED' THEN 0 WHEN 'DEEPLY_REVIEWED' THEN 1 ELSE 2 END, "
        "r.published_at DESC, r.source, r.source_id LIMIT ?"
    )
    params.append(limit)
    results = [row_to_dict(row) for row in con.execute(sql, params)]
    for result in results:
        attributes = record_attributes(con, result["source"], result["source_id"])
        if attributes:
            result["structured_attributes"] = attributes
    return results


def redlimit_insights(con: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    clauses = ["r.source='redlimit-bbrd'"]
    params: list[Any] = []
    if args.category:
        clauses.append(
            "EXISTS (SELECT 1 FROM report_attributes c WHERE c.source=r.source "
            "AND c.source_id=r.source_id AND c.attribute='category' "
            "AND c.normalized_value=?)"
        )
        params.append(args.category.strip().lower())
    for term in re.findall(r'"[^"]+"|\S+', args.terms or ""):
        clean = term.strip('"').lower()
        if clean:
            clauses.append(
                "(lower(r.title || ' ' || r.program || ' ' || r.vulnerability_class || ' ' || r.summary) LIKE ? "
                "OR EXISTS (SELECT 1 FROM report_attributes t WHERE t.source=r.source "
                "AND t.source_id=r.source_id AND (t.normalized_value LIKE ? OR lower(t.attribute) LIKE ?)))"
            )
            params.extend((f"%{clean}%", f"%{clean}%", f"%{clean}%"))
    where = " AND ".join(clauses)
    coverage = dict(
        con.execute(
            f"""SELECT COUNT(*) reports,
                       SUM(CASE WHEN r.normalized_url != '' THEN 1 ELSE 0 END) canonical_source_rows,
                       COUNT(DISTINCT CASE WHEN a.source_id IS NOT NULL THEN r.source_id END)
                         rows_with_structured_attributes,
                       COUNT(a.attribute) attribute_facts
                FROM reports r LEFT JOIN report_attributes a
                ON r.source=a.source AND r.source_id=a.source_id
                WHERE {where}""",
            params,
        ).fetchone()
    )
    # The join above multiplies report rows by attributes, so count report facts
    # with scalar subqueries for the two report-level values.
    report_counts = con.execute(
        f"""SELECT COUNT(*) reports,
                   SUM(CASE WHEN r.normalized_url != '' THEN 1 ELSE 0 END) canonical_source_rows
            FROM reports r WHERE {where}""",
        params,
    ).fetchone()
    coverage["reports"] = report_counts["reports"]
    coverage["canonical_source_rows"] = report_counts["canonical_source_rows"] or 0
    category_rows = con.execute(
        f"""SELECT c.value, COUNT(*) count
            FROM reports r JOIN report_attributes c
            ON r.source=c.source AND r.source_id=c.source_id
            WHERE {where} AND c.attribute='category'
            GROUP BY c.value ORDER BY count DESC, c.value""",
        params,
    )
    requested_attributes = [args.attribute] if args.attribute else list(REDLIMIT_INSIGHT_ATTRIBUTES)
    limit = min(max(1, args.limit), 25)
    top_values: dict[str, list[dict[str, Any]]] = {}
    for attribute in requested_attributes:
        if attribute not in REDLIMIT_ATTRIBUTE_FIELDS:
            continue
        rows = con.execute(
            f"""SELECT a.value, COUNT(*) count
                FROM reports r JOIN report_attributes a
                ON r.source=a.source AND r.source_id=a.source_id
                WHERE {where} AND a.attribute=?
                GROUP BY a.normalized_value, a.value
                ORDER BY count DESC, a.value LIMIT ?""",
            [*params, attribute, limit],
        )
        values = [dict(row) for row in rows]
        if values:
            top_values[attribute] = values
    global_rows = con.execute(
        "SELECT COUNT(*) FROM reports WHERE source='redlimit-bbrd'"
    ).fetchone()[0]
    global_structured = con.execute(
        "SELECT COUNT(DISTINCT source_id) FROM report_attributes WHERE source='redlimit-bbrd'"
    ).fetchone()[0]
    return {
        "status": "PASS",
        "learning_level": "STRUCTURED_METADATA",
        "all_structured_records_processed": global_rows > 0 and global_rows == global_structured,
        "global_redlimit_records": global_rows,
        "global_rows_with_structured_attributes": global_structured,
        "scope": {
            "category": args.category,
            "terms": args.terms,
            **coverage,
        },
        "categories": [dict(row) for row in category_rows],
        "top_values": top_values,
        "excluded_untrusted_fields": ["Payload", "Proof", "comment", "comments"],
        "interpretation": (
            "All matching rows were processed as bounded secondary metadata. "
            "Canonical articles and primary fix/source evidence still require relevance-driven deep review."
        ),
    }


def stats(con: sqlite3.Connection) -> dict[str, Any]:
    def grouped(column: str, limit: int = 30) -> list[dict[str, Any]]:
        rows = con.execute(
            f"SELECT {column} AS value, COUNT(*) AS count FROM reports "
            f"GROUP BY {column} ORDER BY count DESC, value LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in rows]

    total = con.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    unique_urls = con.execute(
        "SELECT COUNT(DISTINCT normalized_url) FROM reports WHERE normalized_url != ''"
    ).fetchone()[0]
    summaries = con.execute("SELECT COUNT(*) FROM reports WHERE evidence_tier != 'METADATA_ONLY'").fetchone()[0]
    cards = con.execute("SELECT COUNT(*) FROM analyst_cards").fetchone()[0]
    exact_cards = con.execute(
        "SELECT COUNT(*) FROM analyst_cards WHERE analysis_status='EXACT_ROOT_EXTRACTED'"
    ).fetchone()[0]
    redlimit_records = con.execute(
        "SELECT COUNT(*) FROM reports WHERE source='redlimit-bbrd'"
    ).fetchone()[0]
    redlimit_structured_rows = con.execute(
        "SELECT COUNT(DISTINCT source_id) FROM report_attributes WHERE source='redlimit-bbrd'"
    ).fetchone()[0]
    redlimit_attribute_facts = con.execute(
        "SELECT COUNT(*) FROM report_attributes WHERE source='redlimit-bbrd'"
    ).fetchone()[0]
    latest_runs = [
        dict(row)
        for row in con.execute(
            """SELECT s.* FROM sync_runs s
               JOIN (SELECT source, MAX(id) id FROM sync_runs GROUP BY source) x
               ON s.id=x.id ORDER BY s.source"""
        )
    ]
    return {
        "records": total,
        "unique_urls": unique_urls,
        "public_report_summaries": summaries,
        "deep_review_cards": cards,
        "exact_root_cards": exact_cards,
        "all_public_reports_deeply_learned": False,
        "redlimit_structured_learning": {
            "records": redlimit_records,
            "rows_with_structured_attributes": redlimit_structured_rows,
            "attribute_facts": redlimit_attribute_facts,
            "all_structured_records_processed": (
                redlimit_records > 0 and redlimit_records == redlimit_structured_rows
            ),
            "all_external_articles_deeply_reviewed": False,
        },
        "by_source": grouped("source"),
        "by_severity": grouped("severity"),
        "by_platform": grouped("platform"),
        "latest_sync": latest_runs,
    }


def duplicates(con: sqlite3.Connection, limit: int) -> list[dict[str, Any]]:
    rows = con.execute(
        """SELECT normalized_url, COUNT(*) count,
                  GROUP_CONCAT(source || ':' || source_id, ' | ') records
           FROM reports WHERE normalized_url != ''
           GROUP BY normalized_url HAVING COUNT(*) > 1
           ORDER BY count DESC, normalized_url LIMIT ?""",
        (min(max(1, limit), 100),),
    )
    return [dict(row) for row in rows]


def validate_card(con: sqlite3.Connection, card: dict[str, Any]) -> list[str]:
    errors = []
    missing = CARD_REQUIRED - set(card)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    status = text(card.get("analysis_status"))
    if status not in CARD_STATUSES:
        errors.append(f"analysis_status must be one of {sorted(CARD_STATUSES)}")
    source = text(card.get("source"))
    source_id = text(card.get("source_id"))
    row = con.execute(
        "SELECT normalized_url FROM reports WHERE source=? AND source_id=?",
        (source, source_id),
    ).fetchone()
    if not row:
        errors.append("source/source_id is not present in the metadata corpus")
    elif not row["normalized_url"]:
        errors.append("indexed record has no canonical source URL; deep review requires primary evidence first")
    elif canonical_url(card.get("canonical_url")) != row["normalized_url"]:
        errors.append("canonical_url does not match the indexed record")
    evidence_urls = card.get("evidence_urls")
    if not isinstance(evidence_urls, list) or not evidence_urls:
        errors.append("evidence_urls must be a non-empty list")
    reviewed = status in {"DEEPLY_REVIEWED", "EXACT_ROOT_EXTRACTED"}
    if reviewed:
        for field in CARD_REQUIRED - {"source", "source_id", "canonical_url", "analysis_status", "evidence_urls"}:
            if not text(card.get(field)):
                errors.append(f"{field} is required for a reviewed card")
    if status == "EXACT_ROOT_EXTRACTED":
        parts = [part.strip() for part in text(card.get("duplicate_signature")).split("|")]
        if len(parts) != 5 or any(not part for part in parts):
            errors.append("EXACT_ROOT_EXTRACTED requires a complete five-part duplicate_signature")
    for field in ("chain_edges", "negative_controls", "evidence_urls"):
        if field in card and not isinstance(card[field], list):
            errors.append(f"{field} must be a list")
    return errors


def upsert_cards(con: sqlite3.Connection, input_path: Path) -> tuple[int, list[dict[str, Any]]]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    cards = payload if isinstance(payload, list) else [payload]
    failures = []
    for card in cards:
        errors = validate_card(con, card)
        if errors:
            failures.append({"source": card.get("source"), "source_id": card.get("source_id"), "errors": errors})
    if failures:
        return 0, failures
    sql = """
    INSERT INTO analyst_cards (
      source, source_id, canonical_url, analysis_status, attacker_start,
      attacker_control, entry_point, primitive, boundary, enforcing_component,
      sink, capability_delta, prerequisites, proof_oracle, root_cause,
      chain_edges_json, negative_controls_json, patch_or_fix,
      current_reachability, duplicate_signature, evidence_urls_json,
      analyst_notes, updated_at
    ) VALUES (
      :source, :source_id, :canonical_url, :analysis_status, :attacker_start,
      :attacker_control, :entry_point, :primitive, :boundary,
      :enforcing_component, :sink, :capability_delta, :prerequisites,
      :proof_oracle, :root_cause, :chain_edges_json,
      :negative_controls_json, :patch_or_fix, :current_reachability,
      :duplicate_signature, :evidence_urls_json, :analyst_notes, :updated_at
    ) ON CONFLICT(source, source_id) DO UPDATE SET
      canonical_url=excluded.canonical_url, analysis_status=excluded.analysis_status,
      attacker_start=excluded.attacker_start, attacker_control=excluded.attacker_control,
      entry_point=excluded.entry_point, primitive=excluded.primitive,
      boundary=excluded.boundary, enforcing_component=excluded.enforcing_component,
      sink=excluded.sink, capability_delta=excluded.capability_delta,
      prerequisites=excluded.prerequisites, proof_oracle=excluded.proof_oracle,
      root_cause=excluded.root_cause, chain_edges_json=excluded.chain_edges_json,
      negative_controls_json=excluded.negative_controls_json,
      patch_or_fix=excluded.patch_or_fix,
      current_reachability=excluded.current_reachability,
      duplicate_signature=excluded.duplicate_signature,
      evidence_urls_json=excluded.evidence_urls_json,
      analyst_notes=excluded.analyst_notes, updated_at=excluded.updated_at
    """
    for card in cards:
        values = {field: text(card.get(field)) for field in CARD_REQUIRED if field != "evidence_urls"}
        for optional in (
            "enforcing_component",
            "patch_or_fix",
            "current_reachability",
            "analyst_notes",
        ):
            values[optional] = text(card.get(optional))
        values["chain_edges_json"] = json_list(card.get("chain_edges"))
        values["negative_controls_json"] = json_list(card.get("negative_controls"))
        values["evidence_urls_json"] = json_list(card.get("evidence_urls"))
        values["updated_at"] = now_iso()
        con.execute(sql, values)
    con.commit()
    return len(cards), []


def self_test() -> None:
    assert canonical_url("HTTPS://Example.COM:443/a//b/#frag") == "https://example.com/a/b"
    assert short_summary("# Hi\n\n`code` [label](https://example.test)") == "Hi code label"
    fixture = {
        "source_id": "1",
        "title": "Cross-tenant authorization bypass",
        "url": "https://example.test/report/1",
        "program": "Example",
        "severity": "High",
        "summary": "Tenant A reads tenant B data.",
    }
    with tempfile.TemporaryDirectory(prefix="public-disclosure-corpus-test-") as directory:
        con = connect(Path(directory) / "test.sqlite3")
        upsert_records(con, [normalized_record("fixture", fixture)])
        args = argparse.Namespace(
            source="fixture",
            program="Example",
            severity="High",
            vulnerability_class="",
            terms="tenant authorization",
            limit=12,
        )
        results = search(con, args)
        assert len(results) == 1 and results[0]["source_id"] == "1"
        card = {
            "source": "fixture",
            "source_id": "1",
            "canonical_url": "https://example.test/report/1",
            "analysis_status": "EXACT_ROOT_EXTRACTED",
            "attacker_start": "tenant user",
            "attacker_control": "object ID",
            "entry_point": "GET /object/{id}",
            "primitive": "IDOR",
            "boundary": "tenant ownership",
            "sink": "object reader",
            "capability_delta": "reads another tenant",
            "prerequisites": "valid low-privilege account",
            "proof_oracle": "foreign canary returned",
            "root_cause": "ownership guard omitted",
            "duplicate_signature": "object reader | object ID | missing ownership guard | read handler | cross-tenant read",
            "evidence_urls": ["https://example.test/report/1"],
        }
        card_path = Path(directory) / "card.json"
        card_path.write_text(json.dumps(card), encoding="utf-8")
        count, failures = upsert_cards(con, card_path)
        assert count == 1 and not failures
        assert stats(con)["records"] == 1
        assert stats(con)["exact_root_cards"] == 1
        redlimit_path = Path(directory) / "redlimit.json"
        redlimit_path.write_text(
            json.dumps(
                {
                    "reports": [
                        {
                            "_id": "rl-1",
                            "title": "Authorization boundary bypass",
                            "writeupUrl": "https://research.example/report/rl-1",
                            "program": "Example",
                            "category": "IDOR",
                            "Root cause": "Missing ownership check",
                            "Required permissions": "Low-privilege account",
                            "Impact": "Cross-tenant record read",
                            "Payload": "must not be retained",
                            "Proof": "must not be retained",
                            "reward": "$1,000",
                            "tags": ["authorization", "idor"],
                        },
                        {"_id": "invalid", "title": "No URL"},
                    ]
                }
            ),
            encoding="utf-8",
        )
        imported = import_redlimit_export(con, redlimit_path, 2)
        assert imported["status"] == "PARTIAL"
        assert imported["upserted"] == 1 and imported["rejected_count"] == 1
        assert imported["structured_rows"] == 1 and imported["attribute_facts"] == 4
        assert con.execute(
            "SELECT vulnerability_class FROM reports WHERE source='redlimit-bbrd' AND source_id='rl-1'"
        ).fetchone()[0] == "IDOR"
        attributes = record_attributes(con, "redlimit-bbrd", "rl-1")
        assert attributes["root_cause"] == "Missing ownership check"
        assert "payload" not in attributes and "proof" not in attributes
        insight_args = argparse.Namespace(category="IDOR", attribute="root_cause", terms="", limit=10)
        insight = redlimit_insights(con, insight_args)
        assert insight["scope"]["reports"] == 1
        assert insight["top_values"]["root_cause"][0]["value"] == "Missing ownership check"
        redlimit_har_path = Path(directory) / "redlimit.har"
        redlimit_har_path.write_text(
            json.dumps(
                {
                    "log": {
                        "entries": [
                            {
                                "request": {"url": "https://wu.redlimit.id/api/reports?page=1"},
                                "response": {
                                    "content": {
                                        "mimeType": "application/json",
                                        "text": json.dumps(
                                            {"data": {"docs": [{"id": "rl-2", "title": "XSS", "link": "https://research.example/report/rl-2", "_category": "xss"}]}}
                                        ),
                                    }
                                },
                            },
                            {
                                "request": {"url": "https://unrelated.example/api"},
                                "response": {"content": {"text": "{}"}},
                            },
                        ]
                    }
                }
            ),
            encoding="utf-8",
        )
        imported_har = import_redlimit_export(con, redlimit_har_path, None)
        assert imported_har["status"] == "PASS" and imported_har["upserted"] == 1
        assert stats(con)["redlimit_structured_learning"]["all_structured_records_processed"] is True
        con.close()
    print(json.dumps({"status": "PASS", "tests": 17}))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=default_db_path())
    sub = parser.add_subparsers(dest="command", required=True)

    sync_parser = sub.add_parser("sync", help="refresh public source indexes")
    sync_parser.add_argument(
        "--source",
        action="append",
        choices=sorted(SYNCERS),
        help="source to refresh; repeatable; defaults to all",
    )
    sync_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    redlimit_parser = sub.add_parser(
        "import-redlimit",
        help="import an authorized RedLimit BBRD JSON/CSV/HAR export without bypassing browser controls",
    )
    redlimit_parser.add_argument("--input", type=Path, required=True)
    redlimit_parser.add_argument("--declared-total", type=int)

    search_parser = sub.add_parser("search", help="retrieve a bounded context pack")
    search_parser.add_argument("--terms", default="")
    search_parser.add_argument("--source", default="")
    search_parser.add_argument("--program", default="")
    search_parser.add_argument("--severity", default="")
    search_parser.add_argument("--class", dest="vulnerability_class", default="")
    search_parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)

    insight_parser = sub.add_parser(
        "redlimit-insights",
        help="summarize bounded structured RedLimit metadata without loading the corpus into context",
    )
    insight_parser.add_argument("--category", default="")
    insight_parser.add_argument("--attribute", choices=sorted(REDLIMIT_ATTRIBUTE_FIELDS), default="")
    insight_parser.add_argument("--terms", default="")
    insight_parser.add_argument("--limit", type=int, default=10)

    show_parser = sub.add_parser("show", help="show one indexed record")
    show_parser.add_argument("source")
    show_parser.add_argument("source_id")

    dup_parser = sub.add_parser("duplicates", help="show exact canonical-URL overlap")
    dup_parser.add_argument("--limit", type=int, default=20)

    card_parser = sub.add_parser("upsert-cards", help="validate and store semantic review cards")
    card_parser.add_argument("--input", type=Path, required=True)

    sub.add_parser("stats", help="show corpus and source coverage")
    sub.add_parser("self-test", help="run offline tests")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "self-test":
        self_test()
        return 0
    con = connect(args.db.expanduser())
    try:
        if args.command == "sync":
            sources = args.source or list(SYNCERS)
            failures = sync_sources(con, sources, args.timeout)
            print(json.dumps({"status": "PASS" if not failures else "PARTIAL", "db": str(args.db)}))
            return 1 if failures else 0
        if args.command == "import-redlimit":
            result = import_redlimit_export(con, args.input.expanduser(), args.declared_total)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["status"] in {"PASS", "PARTIAL"} else 1
        if args.command == "search":
            print(json.dumps(search(con, args), ensure_ascii=False, indent=2))
            return 0
        if args.command == "redlimit-insights":
            print(json.dumps(redlimit_insights(con, args), ensure_ascii=False, indent=2))
            return 0
        if args.command == "show":
            row = con.execute(
                """SELECT r.*, c.analysis_status, c.attacker_start, c.attacker_control,
                          c.entry_point, c.primitive, c.boundary, c.enforcing_component,
                          c.sink, c.capability_delta, c.prerequisites, c.proof_oracle,
                          c.root_cause, c.chain_edges_json, c.negative_controls_json,
                          c.patch_or_fix, c.current_reachability, c.duplicate_signature,
                          c.evidence_urls_json, c.analyst_notes, c.updated_at
                   FROM reports r LEFT JOIN analyst_cards c
                   ON r.source=c.source AND r.source_id=c.source_id
                   WHERE r.source=? AND r.source_id=?""",
                (args.source, args.source_id),
            ).fetchone()
            if not row:
                print(json.dumps({"status": "NOT_FOUND"}))
                return 1
            result = row_to_dict(row)
            attributes = record_attributes(con, args.source, args.source_id)
            if attributes:
                result["structured_attributes"] = attributes
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "duplicates":
            print(json.dumps(duplicates(con, args.limit), ensure_ascii=False, indent=2))
            return 0
        if args.command == "upsert-cards":
            count, failures = upsert_cards(con, args.input)
            if failures:
                print(json.dumps({"status": "FAIL", "cards": failures}, ensure_ascii=False, indent=2))
                return 1
            print(json.dumps({"status": "PASS", "cards_upserted": count}, indent=2))
            return 0
        if args.command == "stats":
            print(json.dumps(stats(con), ensure_ascii=False, indent=2))
            return 0
    finally:
        con.close()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
