#!/usr/bin/env python3
"""Scope filter for wildcard-scope-recon. No network."""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlsplit


def load_entries(path: Path) -> list[str]:
    entries: list[str] = []
    for raw in path.read_text(errors="replace").splitlines():
        raw = raw.split("#", 1)[0].strip().lower().rstrip(".")
        if raw:
            entries.append(raw)
    return entries


def allowed(host: str, entries: list[str]) -> bool:
    host = host.lower().rstrip(".")
    for entry in entries:
        if entry.startswith("*."):
            suffix = entry[2:]
            if host != suffix and host.endswith("." + suffix):
                return True
        elif entry.startswith("."):
            suffix = entry[1:]
            if host == suffix or host.endswith("." + suffix):
                return True
        elif host == entry:
            return True
    return False


def wildcard_suffixes(entries: list[str]) -> list[str]:
    suffixes: list[str] = []
    for entry in entries:
        if entry.startswith("*."):
            suffixes.append(entry[2:])
        elif entry.startswith("."):
            suffixes.append(entry[1:])
    return sorted(set(suffixes))


def valid_host(host: str) -> bool:
    if not host or "://" in host or "/" in host or "@" in host:
        return False
    return all(
        part and part != "-" and not part.startswith("-") and not part.endswith("-")
        for part in host.split(".")
    )


def filter_hosts(scope: Path, source: Path, output: Path, rejected: Path) -> None:
    entries = load_entries(scope)
    accepted, denied = set(), set()
    if source.exists():
        for raw in source.read_text(errors="replace").splitlines():
            host = raw.strip().lower().rstrip(".")
            if host.startswith("*."):
                host = host[2:]
            if not valid_host(host):
                continue
            (accepted if allowed(host, entries) else denied).add(host)
    output.write_text("".join(f"{host}\n" for host in sorted(accepted)))
    with rejected.open("a", encoding="utf-8") as handle:
        handle.write("".join(f"{host}\n" for host in sorted(denied)))


def filter_urls(scope: Path, source: Path, output: Path, rejected: Path) -> None:
    entries = load_entries(scope)
    accepted, denied = set(), set()
    if source.exists():
        for raw in source.read_text(errors="replace").splitlines():
            url = raw.strip()
            if not url:
                continue
            try:
                host = urlsplit(url if "://" in url else "http://" + url).hostname or ""
            except ValueError:
                host = ""
            (accepted if host and allowed(host, entries) else denied).add(url)
    output.write_text("".join(f"{url}\n" for url in sorted(accepted)))
    with rejected.open("a", encoding="utf-8") as handle:
        handle.write("".join(f"{url}\n" for url in sorted(denied)))


def check_seed(scope: Path, domain: str) -> list[str]:
    suffixes = wildcard_suffixes(load_entries(scope))
    if domain not in suffixes:
        raise SystemExit("Seed domain is not the suffix of a wildcard scope line.")
    return suffixes


def self_test() -> None:
    star = ["*.example.com"]
    dotted = [".example.com"]
    exact = ["example.com", "api.example.net"]
    assert allowed("a.example.com", star)
    assert allowed("a.b.example.com", star)
    assert not allowed("example.com", star)
    assert not allowed("notexample.com", star)
    assert not allowed("example.com.evil.test", star)
    assert allowed("example.com", dotted)
    assert allowed("a.example.com", dotted)
    assert allowed("example.com", exact)
    assert allowed("api.example.net", exact)
    assert not allowed("a.example.com", exact)
    assert wildcard_suffixes(star) == ["example.com"]
    assert wildcard_suffixes(exact) == []


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "self-test":
        self_test()
        print("scope-filter-ok")
        return 0
    if len(argv) == 4 and argv[1] == "check":
        suffixes = check_seed(Path(argv[2]), argv[3])
        print("wildcard_suffixes=" + ",".join(suffixes))
        return 0
    if len(argv) == 6 and argv[1] == "hosts":
        filter_hosts(Path(argv[2]), Path(argv[3]), Path(argv[4]), Path(argv[5]))
        return 0
    if len(argv) == 6 and argv[1] == "urls":
        filter_urls(Path(argv[2]), Path(argv[3]), Path(argv[4]), Path(argv[5]))
        return 0
    sys.stderr.write("usage: scope_filter.py self-test|check|hosts|urls\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
