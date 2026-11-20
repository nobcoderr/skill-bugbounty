#!/usr/bin/env python3
"""Route pinned local HackerOne report titles to specialist hunt skills."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
from typing import Iterable


REDDELEXC = Path("/home/kali/security-research/hackerone-reports")
CODEBYGK = Path("/home/kali/security-research/hackerone-bug-bounty-reports")

RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("hunt-idor", (r"\bidor\b", r"direct object reference", r"object reference.*(?:owner|tenant|user|account)", r"cross.tenant.*object")),
    ("hunt-xss", (r"cross.?site scripting", r"\bxss\b", r"script.related html", r"headers for scripting syntax")),
    ("hunt-dom", (r"\bdom\b.*(?:xss|injection)", r"client.side.*(?:script|enforcement)")),
    ("hunt-sqli", (r"sql injection", r"blind sql")),
    ("hunt-nosqli", (r"nosql", r"query selector injection")),
    ("hunt-csrf", (r"cross.?site request forgery", r"\bcsrf\b")),
    ("hunt-ssrf", (r"server.side request forgery", r"\bssrf\b")),
    ("hunt-file-upload", (r"unrestricted upload", r"arbitrary file upload", r"dangerous type", r"upload.*file")),
    ("hunt-lfi", (r"local file inclusion", r"remote file inclusion", r"path traversal", r"file name or path", r"file reading")),
    ("hunt-rce", (r"remote code execution", r"\brce\b", r"code injection", r"command injection", r"os command", r"dangerous function", r"format string", r"untrusted search path")),
    ("hunt-xxe", (r"xml external entit", r"\bxxe\b", r"xml entity", r"xml injection")),
    ("hunt-deserialization", (r"deserializ", r"type confusion")),
    ("hunt-http-smuggling", (r"request smuggling", r"response splitting", r"\bcrlf\b")),
    ("hunt-cache-poison", (r"cache poison", r"cache deception", r"cache containing sensitive")),
    ("hunt-race-condition", (r"race condition", r"time.?of.?check", r"\btoctou\b", r"improper synchron", r"concurrent execution")),
    ("hunt-open-redirect", (r"open redirect",)),
    ("hunt-clickjacking", (r"clickjacking", r"ui redressing")),
    ("hunt-oauth", (r"\boauth\b", r"\bopenid\b")),
    ("hunt-saml", (r"\bsaml\b",)),
    ("hunt-jwt-crypto", (r"\bjwt\b", r"cryptograph", r"signature", r"\bnonce\b", r"random value", r"encryption strength", r"hard.coded.*key")),
    ("hunt-session", (r"session fixation", r"session expiration", r"cookie.*integrity", r"session.*(?:logout|revo|rotation)")),
    ("hunt-auth-bypass", (r"authentication bypass", r"improper authentication", r"missing authentication", r"missing critical step", r"alternate path or channel", r"default credentials", r"improper access control", r"improper authorization", r"incorrect authorization", r"missing authorization", r"forced browsing", r"privilege escalation")),
    ("hunt-ato", (r"account takeover", r"\bato\b")),
    ("hunt-mfa-bypass", (r"\bmfa\b", r"multi.factor", r"two.factor", r"2fa")),
    ("hunt-forgot-password", (r"password recovery", r"forgotten password", r"password reset", r"unverified password change")),
    ("hunt-brute-force", (r"brute force", r"authentication attempts")),
    ("hunt-business-logic", (r"business logic", r"expected behavior violation", r"secure design", r"documented design", r"critical state data")),
    ("hunt-graphql", (r"graphql",)),
    ("hunt-api-misconfig", (r"\bapi\b", r"misconfiguration", r"dangerous method", r"unsafe default")),
    ("hunt-ldap", (r"ldap injection",)),
    ("hunt-exceptional-conditions", (r"exceptional condition", r"unchecked error", r"null pointer", r"uncontrolled recursion")),
    ("hunt-source-leak", (r"information disclosure", r"information exposure", r"sensitive information", r"hard.coded (?:credential|password)", r"password in configuration", r"debug information", r"directory listing")),
    ("hunt-tls-network", (r"certificate validation", r"certificate revocation", r"host mismatch", r"cleartext transmission", r"unprotected transport", r"man.in.the.middle")),
    ("hunt-html-injection", (r"content spoofing", r"ui misrepresentation", r"html injection")),
    ("hunt-cicd", (r"download of code without integrity", r"software.*integrity", r"supply.chain", r"build pipeline")),
    ("hunt-llm-ai", (r"\bllm0[0-9]\b", r"large language model", r"prompt injection")),
    ("hunt-subdomain", (r"subdomain takeover",)),
)

EXPLICIT_STATUS = re.compile(
    r"^\s*(?:\[(?:n/?a|informative|not applicable|by design|duplicate|spam)\]|"
    r"(?:n/?a|informative|not applicable|by design|duplicate|spam)\s*[:\-])|"
    r"\b(?:closed|marked|resolved)\s+as\s+(?:informative|not applicable|n/?a|by design|duplicate|spam)\b",
    re.IGNORECASE,
)

IMPACT_FREE = tuple(re.compile(value, re.IGNORECASE) for value in (
    r"\bmissing (?:security )?headers?\b",
    r"\bversion (?:banner |number )?(?:disclosure|exposure)\b",
    r"\bself[- ]xss\b",
    r"\blogout csrf\b",
    r"\bexpired (?:ssl |tls )?certificate\b",
    r"\bweak (?:ssl |tls )?cipher\b",
    r"\brobots\.txt\b.*\bdisclos",
))


def clean_url(value: str) -> str:
    value = value.strip()
    if value and not value.startswith(("http://", "https://")):
        value = "https://" + value
    return value


def report_id(url: str) -> str:
    match = re.search(r"/reports/(\d+)", url)
    return match.group(1) if match else url


def number(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def reddelexc_records() -> Iterable[dict[str, object]]:
    with (REDDELEXC / "data.csv").open(newline="", encoding="utf-8", errors="replace") as handle:
        for row in csv.DictReader(handle):
            yield {
                "program_a": row.get("program", ""),
                "title": row.get("title", ""),
                "url": clean_url(row.get("link", "")),
                "vulnerability_type": row.get("vuln_type", ""),
                "severity": "",
                "bounty": number(row.get("bounty")),
                "upvotes": int(number(row.get("upvotes"))),
                "state": "",
                "sources": ["reddelexc@4c279ab"],
            }


def codebygk_records() -> Iterable[dict[str, object]]:
    payload = json.loads((CODEBYGK / "data" / "reports.json").read_text(encoding="utf-8"))
    for row in payload.get("reports", ()):
        yield {
            "program_a": row.get("program", ""),
            "title": row.get("title", ""),
            "url": clean_url(row.get("url", "")),
            "vulnerability_type": row.get("vulnerability_type", ""),
            "severity": row.get("severity", ""),
            "bounty": number(row.get("bounty")),
            "upvotes": int(number(row.get("upvotes"))),
            "state": row.get("state", ""),
            "sources": ["codebygk@cb5d63c"],
        }


def excluded(title: str) -> str:
    if EXPLICIT_STATUS.search(title):
        return "explicit N/A/informative/by-design/duplicate/spam status"
    for pattern in IMPACT_FREE:
        if pattern.search(title):
            return f"impact-free title shape: {pattern.pattern}"
    return ""


def routes(record: dict[str, object]) -> list[str]:
    text = f'{record["vulnerability_type"]} {record["title"]}'
    found = [skill for skill, patterns in RULES if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)]
    return sorted(set(found)) or ["hunt-misc"]


def merged_records() -> tuple[list[dict[str, object]], int]:
    merged: dict[str, dict[str, object]] = {}
    excluded_count = 0
    for incoming in (*reddelexc_records(), *codebygk_records()):
        title = str(incoming["title"]).strip()
        reason = excluded(title)
        if reason:
            excluded_count += 1
            continue
        key = report_id(str(incoming["url"]))
        if key not in merged:
            incoming["report_id"] = key
            merged[key] = incoming
            continue
        current = merged[key]
        current["sources"] = sorted(set(current["sources"]) | set(incoming["sources"]))
        for field in ("program_a", "title", "url", "vulnerability_type", "severity", "state"):
            if not current.get(field) and incoming.get(field):
                current[field] = incoming[field]
        current["bounty"] = max(number(current["bounty"]), number(incoming["bounty"]))
        current["upvotes"] = max(int(number(current["upvotes"])), int(number(incoming["upvotes"])))
    output = []
    for record in merged.values():
        record["skill_routes"] = routes(record)
        record["candidate_state"] = "HYPOTHESIS_QUARANTINED"
        record["eligibility"] = "REQUIRES_NA_INFORMATIVE_AND_TARGET_SHAPE_REVIEW"
        output.append(record)
    output.sort(key=lambda item: (number(item["bounty"]), int(number(item["upvotes"]))), reverse=True)
    return output, excluded_count


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Query offline HackerOne report cards by hunt skill.")
    result.add_argument("--skill", required=True, help="Exact hunt-* skill name")
    result.add_argument("--program-b", default="", help="Exclude reports already naming program B")
    result.add_argument("--format", choices=("jsonl", "markdown"), default="jsonl")
    result.add_argument("--limit", type=int, default=0, help="0 returns every matching card")
    result.add_argument("--stats", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    valid_skills = {skill for skill, _ in RULES} | {"hunt-misc"}
    if args.skill not in valid_skills:
        raise SystemExit(f"unknown skill: {args.skill}")
    records, excluded_count = merged_records()
    program_b = args.program_b.strip().casefold()
    selected = [
        record for record in records
        if args.skill in record["skill_routes"]
        and (not program_b or str(record["program_a"]).strip().casefold() != program_b)
    ]
    if args.limit > 0:
        selected = selected[:args.limit]
    if args.stats:
        print(json.dumps({
            "skill": args.skill,
            "cards": len(selected),
            "excluded_before_routing": excluded_count,
            "merged_eligible_for_review": len(records),
        }, sort_keys=True))
    for record in selected:
        if args.format == "jsonl":
            print(json.dumps(record, ensure_ascii=False, sort_keys=True))
        else:
            print(f'- [{record["title"]}]({record["url"]}) — {record["program_a"]} — {record["vulnerability_type"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
