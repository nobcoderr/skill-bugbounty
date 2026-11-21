#!/usr/bin/env python3
"""Query the local nobcoderr/writeup corpus for transferable hunt cards."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path("/home/kali/security-research/writeup/programs")

RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("hunt-idor", (r"\bidor\b", r"direct object reference", r"broken access control", r"improper authorization", r"improper access control")),
    ("hunt-xss", (r"cross.?site scripting", r"\bxss\b")),
    ("hunt-dom", (r"\bdom\b.*(?:xss|injection)", r"dom-based xss")),
    ("hunt-sqli", (r"sql injection", r"blind sql", r"\bsqli\b")),
    ("hunt-nosqli", (r"nosql",)),
    ("hunt-csrf", (r"cross.?site request forgery", r"\bcsrf\b")),
    ("hunt-ssrf", (r"server.side request forgery", r"\bssrf\b")),
    ("hunt-file-upload", (r"unrestricted upload", r"arbitrary file upload", r"file upload")),
    ("hunt-lfi", (r"local file inclusion", r"path traversal", r"file read")),
    ("hunt-rce", (r"remote code execution", r"\brce\b", r"code injection", r"command injection", r"os command")),
    ("hunt-xxe", (r"xml external entit", r"\bxxe\b")),
    ("hunt-deserialization", (r"deserializ",)),
    ("hunt-http-smuggling", (r"request smuggling", r"\bcrlf\b")),
    ("hunt-cache-poison", (r"cache poison", r"cache deception")),
    ("hunt-race-condition", (r"race condition", r"\btoctou\b")),
    ("hunt-open-redirect", (r"open redirect",)),
    ("hunt-clickjacking", (r"clickjacking",)),
    ("hunt-oauth", (r"\boauth\b", r"\bopenid\b")),
    ("hunt-saml", (r"\bsaml\b",)),
    ("hunt-jwt-crypto", (r"\bjwt\b",)),
    ("hunt-session", (r"session fixation", r"session expiration")),
    ("hunt-auth-bypass", (r"authentication bypass", r"improper authentication", r"missing authentication", r"privilege escalation")),
    ("hunt-ato", (r"account takeover", r"\bato\b")),
    ("hunt-mfa-bypass", (r"\bmfa\b", r"two.factor", r"\b2fa\b")),
    ("hunt-forgot-password", (r"password reset", r"forgotten password")),
    ("hunt-brute-force", (r"brute force",)),
    ("hunt-business-logic", (r"business logic", r"payment pin", r"workflow")),
    ("hunt-graphql", (r"graphql",)),
    ("hunt-api-misconfig", (r"\bapi\b", r"misconfiguration")),
    ("hunt-html-injection", (r"html injection",)),
    ("hunt-subdomain", (r"subdomain takeover",)),
    ("hunt-source-leak", (r"information disclosure", r"source code disclosure")),
    ("hunt-ssti", (r"template injection", r"\bsti\b", r"\bssti\b")),
    ("hunt-cors", (r"\bcors\b",)),
    ("hunt-websocket", (r"websocket",)),
    ("hunt-cloud-misconfig", (r"\bs3\b", r"bucket", r"cloud misconfig")),
)

EXPLICIT_STATUS = re.compile(
    r"^\s*(?:\[(?:n/?a|informative|not applicable|by design|duplicate|spam)\]|"
    r"(?:n/?a|informative|not applicable|by design|duplicate|spam)\s*[:\-])",
    re.IGNORECASE,
)
IMPACT_FREE = tuple(
    re.compile(value, re.IGNORECASE)
    for value in (
        r"\bmissing (?:security )?headers?\b",
        r"\bself[- ]xss\b",
        r"\blogout csrf\b",
        r"\bexpired (?:ssl |tls )?certificate\b",
        r"\bweak (?:ssl |tls )?cipher\b",
    )
)
LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
BOUNTY = re.compile(r"[\d.]+")
VALID_SKILLS = {skill for skill, _ in RULES} | {"hunt-misc"}


def money(value: str) -> float:
    match = BOUNTY.search((value or "").replace(",", ""))
    try:
        return float(match.group(0)) if match else 0.0
    except ValueError:
        return 0.0


def excluded(title: str) -> bool:
    if EXPLICIT_STATUS.search(title or ""):
        return True
    return any(pattern.search(title or "") for pattern in IMPACT_FREE)


def routes(text: str) -> list[str]:
    found = [
        skill
        for skill, patterns in RULES
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)
    ]
    return sorted(set(found)) or ["hunt-misc"]


def split_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def parse_readme(readme: Path) -> list[dict[str, object]]:
    text = readme.read_text(encoding="utf-8", errors="replace")
    program = readme.parent.name
    lines = text.splitlines()
    header_i = None
    cols: list[str] = []
    for index, line in enumerate(lines):
        lower = line.lower()
        if "|" in line and "id" in lower and ("temuan" in lower or "writeup" in lower or "finding" in lower):
            cols = [part.strip().lower() for part in split_row(line)]
            header_i = index
            break
    if header_i is None:
        return []

    def cell(parts: list[str], *names: str) -> str:
        for name in names:
            if name in cols:
                position = cols.index(name)
                if position < len(parts):
                    return parts[position]
        return ""

    cards: list[dict[str, object]] = []
    for line in lines[header_i + 2 :]:
        if not line.strip().startswith("|"):
            if cards:
                break
            continue
        parts = split_row(line)
        if len(parts) < 3:
            continue
        report_id = cell(parts, "id")
        if not report_id.isdigit():
            continue
        weakness = cell(parts, "temuan", "weakness", "finding")
        severity = cell(parts, "severity")
        bounty = cell(parts, "bounty")
        writeup = cell(parts, "writeup")
        link = LINK.search(writeup or "")
        title = (link.group(1) if link else writeup) or weakness or report_id
        rel = link.group(2) if link else ""
        local = (readme.parent / rel).resolve() if rel else Path()
        if excluded(title):
            continue
        blob = f"{weakness} {title}"
        cards.append(
            {
                "report_id": report_id,
                "program_a": program,
                "title": title,
                "vulnerability_type": weakness,
                "severity": severity,
                "bounty": money(bounty),
                "url": f"https://hackerone.com/reports/{report_id}",
                "local_path": str(local) if local.is_file() else str(readme.parent / f"{report_id}.md"),
                "skill_routes": routes(blob),
                "candidate_state": "HYPOTHESIS_QUARANTINED",
                "source": "nobcoderr/writeup@b9433b58",
            }
        )
    return cards


def all_cards() -> list[dict[str, object]]:
    merged: dict[str, dict[str, object]] = {}
    if not ROOT.is_dir():
        raise SystemExit(f"missing corpus: {ROOT}")
    for readme in sorted(ROOT.glob("*/README.md")):
        for card in parse_readme(readme):
            merged[str(card["report_id"])] = card
    output = list(merged.values())
    output.sort(key=lambda item: float(item["bounty"]), reverse=True)
    return output


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Query local nobcoderr/writeup cards.")
    result.add_argument("--skill", required=True, help="Exact hunt-* skill name")
    result.add_argument("--program-b", default="", help="Exclude that program folder (duplicate gate)")
    result.add_argument("--q", default="", help="Optional title/weakness substring")
    result.add_argument("--format", choices=("jsonl", "markdown"), default="jsonl")
    result.add_argument("--limit", type=int, default=8)
    result.add_argument("--stats", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.skill not in VALID_SKILLS:
        raise SystemExit(f"unknown skill: {args.skill}")
    program_b = args.program_b.strip().casefold().replace(" ", "_")
    query = args.q.strip().casefold()
    selected = []
    for card in all_cards():
        if args.skill not in card["skill_routes"]:
            continue
        if program_b and str(card["program_a"]).casefold() == program_b:
            continue
        blob = f"{card['title']} {card['vulnerability_type']}".casefold()
        if query and query not in blob:
            continue
        selected.append(card)
    if args.limit > 0:
        selected = selected[: args.limit]
    if args.stats:
        print(json.dumps({"skill": args.skill, "cards": len(selected)}, sort_keys=True))
    for card in selected:
        if args.format == "jsonl":
            print(json.dumps(card, ensure_ascii=False, sort_keys=True))
        else:
            print(
                f'- [{card["title"]}]({card["url"]}) — {card["program_a"]} — '
                f'{card["vulnerability_type"]} — ${card["bounty"]:g}'
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
