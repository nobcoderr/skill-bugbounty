#!/usr/bin/env python3
"""Map hunt-* skills to local PayloadsAllTheThings chapters."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path("/home/kali/security-research/PayloadsAllTheThings")

SKILL_FOLDERS: dict[str, tuple[str, ...]] = {
    "hunt-sqli": ("SQL Injection",),
    "hunt-xss": ("XSS Injection", "DOM Clobbering", "CSS Injection"),
    "hunt-dom": ("XSS Injection", "DOM Clobbering"),
    "hunt-html-injection": ("XSS Injection", "CSS Injection"),
    "hunt-ssti": ("Server Side Template Injection", "Server Side Include Injection", "XSLT Injection"),
    "hunt-rce": ("Command Injection", "Insecure Deserialization", "Prototype Pollution"),
    "hunt-deserialization": ("Insecure Deserialization",),
    "hunt-ssrf": ("Server Side Request Forgery", "DNS Rebinding"),
    "hunt-lfi": ("Directory Traversal", "File Inclusion", "Client Side Path Traversal"),
    "hunt-file-upload": ("Upload Insecure Files", "Zip Slip"),
    "hunt-xxe": ("XXE Injection",),
    "hunt-csrf": ("Cross-Site Request Forgery",),
    "hunt-cors": ("CORS Misconfiguration",),
    "hunt-open-redirect": ("Open Redirect",),
    "hunt-http-smuggling": ("Request Smuggling", "CRLF Injection"),
    "hunt-cache-poison": ("Web Cache Deception",),
    "hunt-jwt-crypto": ("JSON Web Token",),
    "hunt-oauth": ("OAuth Misconfiguration",),
    "hunt-saml": ("SAML Injection",),
    "hunt-ldap": ("LDAP Injection",),
    "hunt-nosqli": ("NoSQL Injection", "ORM Leak"),
    "hunt-graphql": ("GraphQL Injection",),
    "hunt-idor": ("Insecure Direct Object References", "Mass Assignment", "Hidden Parameters"),
    "hunt-ato": ("Account Takeover",),
    "hunt-auth-bypass": ("Account Takeover", "Type Juggling", "Mass Assignment"),
    "hunt-race-condition": ("Race Condition",),
    "hunt-business-logic": ("Business Logic Errors",),
    "hunt-clickjacking": ("Clickjacking",),
    "hunt-websocket": ("Web Sockets",),
    "hunt-brute-force": ("Brute Force Rate Limit",),
    "hunt-llm-ai": ("Prompt Injection",),
    "hunt-source-leak": ("API Key Leaks", "Insecure Source Code Management"),
    "hunt-subdomain": ("Virtual Hosts",),
    "hunt-cloud-misconfig": ("Methodology and Resources",),
    "hunt-k8s": ("Methodology and Resources",),
    "payload-forge": ("Encoding Transformations", "HTTP Parameter Pollution"),
}

HEADING = re.compile(r"^(#{2,3})\s+(.*)")
SKIP_HEADING = re.compile(r"^(tools|labs|references|books|sponsors|contributions)$", re.I)


def headings(readme: Path, limit: int = 24) -> list[str]:
    if not readme.is_file():
        return []
    found: list[str] = []
    for line in readme.read_text(encoding="utf-8", errors="replace").splitlines():
        match = HEADING.match(line.strip())
        if not match:
            continue
        title = match.group(2).strip()
        if SKIP_HEADING.match(re.sub(r"[^A-Za-z ]", "", title).strip()):
            continue
        found.append(title)
        if len(found) >= limit:
            break
    return found


def chapter(folder: str) -> dict[str, object]:
    path = ROOT / folder
    readme = path / "README.md"
    extras = []
    if path.is_dir():
        extras = sorted(
            str(item.relative_to(ROOT))
            for item in path.iterdir()
            if item.is_file() and item.suffix.lower() in {".md", ".txt"} and item.name != "README.md"
        )[:12]
    return {
        "folder": folder,
        "path": str(path),
        "readme": str(readme) if readme.is_file() else "",
        "headings": headings(readme),
        "extra_markdown": extras,
        "exists": path.is_dir(),
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Query local PayloadsAllTheThings chapters.")
    result.add_argument("--skill", required=True, help="hunt-* skill or payload-forge")
    result.add_argument("--format", choices=("jsonl", "markdown"), default="markdown")
    result.add_argument("--list-skills", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.list_skills:
        for skill in sorted(SKILL_FOLDERS):
            print(skill)
        return 0
    if not ROOT.is_dir():
        raise SystemExit(f"missing clone: {ROOT}")
    folders = SKILL_FOLDERS.get(args.skill)
    if not folders:
        raise SystemExit(f"unknown skill: {args.skill}")
    for folder in folders:
        card = chapter(folder)
        if args.format == "jsonl":
            print(json.dumps(card, ensure_ascii=False, sort_keys=True))
            continue
        print(f"## {card['folder']}")
        print(f"- path: `{card['path']}`")
        print(f"- exists: {card['exists']}")
        if card["readme"]:
            print(f"- readme: `{card['readme']}`")
        if card["headings"]:
            print("- methodology headings:")
            for heading in card["headings"]:
                print(f"  - {heading}")
        if card["extra_markdown"]:
            print("- extra markdown:")
            for extra in card["extra_markdown"]:
                print(f"  - `{extra}`")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
