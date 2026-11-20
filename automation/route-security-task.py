#!/usr/bin/env python3
"""Select only target- and scope-relevant skills from the local security pack.

This helper is advisory, deterministic, read-only, and network-free. It never runs
recon, scanners, fuzzers, installers, hooks, or exploit code. Architecture,
official scope, and current call-path evidence always override routing hints.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "config" / "AUTO_ROUTING_MAP.json"

SOURCE_MARKERS = (
    ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".c", ".cc",
    ".cpp", ".h", ".hpp", ".java", ".kt", ".kts", ".cs", ".php",
    ".rb", ".sh", ".ps1", ".sql", ".sol", "package.json",
    "pyproject.toml", "requirements.txt", "go.mod", "go.sum", "cargo.toml",
    "cargo.lock", "pom.xml", "build.gradle", "build.gradle.kts", ".csproj",
    ".sln", "composer.json", "gemfile", "makefile", "cmakelists.txt",
)

LANGUAGE_RULES = {
    "expert-c-cpp-engineer": {
        "terms": ("c++", "cpp", "cmake", "native code"),
        "markers": (".c", ".cc", ".cpp", ".h", ".hpp", "cmakelists.txt", "makefile"),
    },
    "expert-dotnet-csharp-engineer": {
        "terms": ("c#", "csharp", "dotnet", "asp.net", "clr"),
        "markers": (".cs", ".csproj", ".sln"),
    },
    "expert-go-engineer": {
        "terms": ("golang",),
        "markers": (".go", "go.mod", "go.sum"),
    },
    "expert-java-kotlin-engineer": {
        "terms": ("java", "kotlin", "gradle", "maven", "jvm", "spring"),
        "markers": (".java", ".kt", ".kts", "build.gradle", "build.gradle.kts", "pom.xml"),
    },
    "expert-javascript-typescript-engineer": {
        "terms": ("javascript", "typescript", "node.js", "nodejs", "deno", "bun", "react", "next.js"),
        "markers": (".js", ".jsx", ".ts", ".tsx", "package.json"),
    },
    "expert-php-ruby-engineer": {
        "terms": ("php", "laravel", "wordpress", "ruby", "rails"),
        "markers": (".php", ".rb", "composer.json", "gemfile"),
    },
    "expert-python-engineer": {
        "terms": ("python", "django", "flask", "fastapi"),
        "markers": (".py", "pyproject.toml", "requirements.txt"),
    },
    "expert-rust-engineer": {
        "terms": ("rust",),
        "markers": (".rs", "cargo.toml", "cargo.lock"),
    },
    "expert-shell-powershell-engineer": {
        "terms": ("bash", "shell", "powershell", "cmd.exe", "batch file", "workflow script"),
        "markers": (".sh", ".ps1"),
    },
    "expert-sql-database-engineer": {
        "terms": ("sql", "postgres", "mysql", "sqlite", "sql server", "orm", "query builder"),
        "markers": (".sql",),
    },
}

NEGATIVE_SCOPE_MARKERS = (
    "out of scope", "out-of-scope", "not in scope", "excluded", "ineligible",
    "do not test", "must not test", "prohibited", "refrain from",
)

NEGATED_INTENT_PREFIXES = (
    "do not", "don't", "never", "without", "must not", "jangan", "tidak boleh",
    "dilarang untuk",
)
NEGATED_INTENT_SUFFIXES = (
    "is prohibited", "are prohibited", "not allowed", "out of scope", "dilarang",
    "tidak diizinkan",
)


def contains_term(text: str, term: str) -> bool:
    """Match a phrase without turning short language tokens into substrings."""
    text = text.lower()
    term = term.lower().strip()
    if not term:
        return False
    if term.startswith(".") or "/" in term or "://" in term or "(" in term:
        return term in text
    pattern = re.escape(term).replace(r"\ ", r"\s+")
    return re.search(rf"(?<![a-z0-9]){pattern}(?![a-z0-9])", text) is not None


def contains_non_negated_intent(text: str, phrase: str) -> bool:
    """Require an explicit request phrase that is not locally negated."""
    lowered = text.lower()
    pattern = re.escape(phrase.lower()).replace(r"\ ", r"\s+")
    for match in re.finditer(rf"(?<![a-z0-9]){pattern}(?![a-z0-9])", lowered):
        prefix = lowered[max(0, match.start() - 48):match.start()]
        suffix = lowered[match.end():match.end() + 40]
        if re.search(r"(?:^|[^a-z0-9])no\s*$", prefix):
            continue
        if any(marker in prefix for marker in NEGATED_INTENT_PREFIXES):
            continue
        if any(marker in suffix for marker in NEGATED_INTENT_SUFFIXES):
            continue
        return True
    return False


def marker_matches(value: str, marker: str) -> bool:
    value = value.lower().strip()
    marker = marker.lower()
    basename = Path(value).name
    if marker.startswith("."):
        return basename.endswith(marker)
    return basename == marker or value.endswith("/" + marker)


def unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def read_scope_files(paths: list[str]) -> list[str]:
    contents: list[str] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        if not path.is_file():
            raise SystemExit(f"scope file does not exist or is not a file: {path}")
        contents.append(path.read_text(encoding="utf-8", errors="replace"))
    return contents


def split_scope(scope_values: list[str], surface_terms: dict[str, list[str]]) -> tuple[list[str], dict[str, list[str]]]:
    positive: list[str] = []
    excluded: dict[str, list[str]] = {name: [] for name in surface_terms}
    for value in scope_values:
        chunks = [chunk.strip() for chunk in re.split(r"[\n;]+", value) if chunk.strip()]
        for chunk in chunks:
            lowered = chunk.lower()
            if any(marker in lowered for marker in NEGATIVE_SCOPE_MARKERS):
                for surface, terms in surface_terms.items():
                    if any(contains_term(lowered, term) for term in terms):
                        excluded[surface].append(chunk)
            else:
                positive.append(chunk)
    return positive, {name: unique(lines) for name, lines in excluded.items() if lines}


def detect_profile(
    task: str,
    targets: list[str],
    positive_scope: list[str],
    observed: list[str],
    surface_terms: dict[str, list[str]],
    excluded: dict[str, list[str]],
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    evidence: dict[str, list[str]] = {name: [] for name in surface_terms}
    sources = [("task", task), *[("target", x) for x in targets], *[("scope", x) for x in positive_scope]]
    for label, text in sources:
        for surface, terms in surface_terms.items():
            hits = [term for term in terms if contains_term(text, term)]
            if hits:
                evidence[surface].append(f"{label}: {', '.join(hits[:4])}")

    observed_lower = [value.lower() for value in observed]
    for value in observed_lower:
        for surface, terms in surface_terms.items():
            hits = [term for term in terms if contains_term(value, term)]
            if hits:
                evidence[surface].append(f"observed: {value}")
        if any(marker_matches(value, marker) for marker in SOURCE_MARKERS):
            evidence.setdefault("source", []).append(f"observed source/build artifact: {value}")
        if marker_matches(value, ".sol"):
            evidence.setdefault("web3", []).append(f"observed Solidity artifact: {value}")
        if any(marker_matches(value, marker) for marker in (".apk", ".ipa", "androidmanifest.xml")):
            evidence.setdefault("mobile", []).append(f"observed mobile artifact: {value}")
        if any(marker_matches(value, marker) for marker in (".exe", ".dll", ".sys", ".msi", ".elf", ".so", ".dylib")):
            evidence.setdefault("binary", []).append(f"observed executable artifact: {value}")
        if any(marker_matches(value, marker) for marker in (".exe", ".dll", ".sys", ".msi", ".ps1")):
            evidence.setdefault("windows", []).append(f"observed Windows artifact: {value}")
        if any(term in value for term in (".github/workflows/", ".gitlab-ci.yml", "azure-pipelines.yml", "jenkinsfile")):
            evidence.setdefault("ci-cd", []).append(f"observed CI/CD artifact: {value}")
        if any(term in value for term in ("dockerfile", "docker-compose", "kubernetes", "helm", "terraform", ".tf")):
            evidence.setdefault("cloud", []).append(f"observed cloud/deployment artifact: {value}")

    active = {
        name: unique(reasons)
        for name, reasons in evidence.items()
        if reasons and name not in excluded
    }
    return active, {name: unique(reasons) for name, reasons in evidence.items() if reasons}


def detect_languages(task_and_target: str, observed: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for skill, rule in LANGUAGE_RULES.items():
        reasons: list[str] = []
        term_hits = [term for term in rule["terms"] if contains_term(task_and_target, term)]
        if term_hits:
            reasons.append("language/runtime: " + ", ".join(term_hits[:4]))
        for value in observed:
            matched = [marker for marker in rule["markers"] if marker_matches(value, marker)]
            if matched:
                reasons.append(f"observed {matched[0]} artifact: {value}")
        if reasons:
            result[skill] = unique(reasons)
    return result


def subagents_suppressed(text: str) -> bool:
    """Honor explicit task/scope bans on subagents even during bounty auto-on."""
    lowered = text.lower()
    return any(
        re.search(pattern, lowered)
        for pattern in (
            r"\bno subagents?\b",
            r"\bwithout subagents?\b",
            r"\bdo not use subagents?\b",
            r"\bsubagents? (are )?prohibited\b",
            r"\bor subagents?\b",
            r"\bsubagent execution\b",
        )
    )


def trigger_matches(trigger: str, text: str, observed: list[str]) -> bool:
    trigger = trigger.lower().strip()
    if trigger.startswith(".") and " " not in trigger:
        return any(marker_matches(value, trigger) for value in observed)
    if trigger in {"package.json", "pyproject.toml", "go.mod", "go.sum", "cargo.toml", "cargo.lock", "pom.xml", "composer.json", "gemfile", "makefile", "cmakelists.txt"}:
        return any(marker_matches(value, trigger) for value in observed)
    return contains_non_negated_intent(text, trigger)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Requested authorized security task")
    parser.add_argument("--target", action="append", default=[], help="Target/product/repository evidence; repeatable")
    parser.add_argument("--scope", action="append", default=[], help="Official in-scope or out-of-scope text; repeatable")
    parser.add_argument("--scope-file", action="append", default=[], help="Local official scope text file; repeatable")
    parser.add_argument("--observed", action="append", default=[], help="Observed file/path/runtime/sink; repeatable")
    parser.add_argument("--json", action="store_true", help="Emit the complete routing ledger as JSON")
    args = parser.parse_args()

    data = json.loads(MAP.read_text(encoding="utf-8"))
    policy = data["selection_policy"]
    surface_terms: dict[str, list[str]] = policy["surface_terms"]
    scope_values = [*args.scope, *read_scope_files(args.scope_file)]
    positive_scope, excluded = split_scope(scope_values, surface_terms)
    active_surfaces, all_surface_evidence = detect_profile(
        args.task, args.target, positive_scope, args.observed, surface_terms, excluded
    )

    positive_text = "\n".join([args.task, *args.target, *positive_scope, *args.observed]).lower()
    task_text = args.task.lower()
    suppression_text = "\n".join([args.task, *args.target, *scope_values, *args.observed]).lower()
    language_evidence = detect_languages("\n".join([args.task, *args.target, *positive_scope]).lower(), args.observed)
    ambiguous = {term.lower() for term in policy["ambiguous_single_triggers"]}
    explicit_intent = set(policy["explicit_intent_skills"])
    explicit_phrases: dict[str, list[str]] = policy["explicit_intent_phrases"]
    primary_surface_skills: dict[str, list[str]] = policy["primary_surface_skills"]
    requirements: dict[str, list[str]] = policy["skill_surface_requirements"]
    minimum_weak = int(policy["minimum_independent_weak_signals"])

    selected: list[dict[str, object]] = []
    deferred: list[dict[str, str]] = []
    not_applicable: list[dict[str, str]] = []

    for name, route in data["skill_routes"].items():
        companions = route.get("companions", [])
        if route["mode"] == "always":
            selected.append({"skill": name, "state": "ACTIVE", "reason": "mandatory core", "companions": companions})
            continue

        all_hits = [trigger for trigger in route.get("triggers", []) if trigger_matches(trigger, positive_text, args.observed)]
        task_hits = [phrase for phrase in explicit_phrases.get(name, []) if contains_non_negated_intent(task_text, phrase)]
        if name == "codex-cli-multi-agent-audit-orchestrator" and subagents_suppressed(suppression_text):
            not_applicable.append({
                "skill": name,
                "state": "NOT_APPLICABLE",
                "reason": "task or scope prohibits subagents",
            })
            continue
        strong_hits = [hit for hit in all_hits if hit.lower() not in ambiguous]
        weak_hits = [hit for hit in all_hits if hit.lower() in ambiguous]
        required_surfaces = set(requirements.get(name, []))
        matched_surfaces = sorted(required_surfaces.intersection(active_surfaces))
        excluded_required = sorted(required_surfaces.intersection(excluded))
        primary_hits = sorted(
            surface for surface in active_surfaces
            if name in primary_surface_skills.get(surface, [])
        )

        if name in explicit_intent:
            if task_hits and (not required_surfaces or matched_surfaces):
                selected.append({
                    "skill": name,
                    "state": "ACTIVE",
                    "reason": "explicit user intent: " + ", ".join(task_hits[:5]),
                    "companions": companions,
                })
            elif task_hits:
                deferred.append({
                    "skill": name,
                    "state": "DEFERRED",
                    "reason": "explicit intent found but compatible target/scope evidence is missing",
                    "activate_when": "confirm one of: " + ", ".join(sorted(required_surfaces)),
                })
            else:
                not_applicable.append({"skill": name, "state": "NOT_APPLICABLE", "reason": "no explicit user request for this capability"})
            continue

        if name in language_evidence:
            selected.append({
                "skill": name,
                "state": "ACTIVE",
                "reason": "; ".join(language_evidence[name]),
                "companions": companions,
            })
            continue

        if required_surfaces and excluded_required and not matched_surfaces:
            not_applicable.append({
                "skill": name,
                "state": "NOT_APPLICABLE",
                "reason": "required surface excluded by scope: " + ", ".join(excluded_required),
            })
            continue

        if primary_hits:
            evidence = [reason for surface in primary_hits for reason in active_surfaces[surface]]
            selected.append({
                "skill": name,
                "state": "ACTIVE",
                "reason": "target/scope surface " + ", ".join(primary_hits) + "; " + "; ".join(evidence[:3]),
                "companions": companions,
            })
            continue

        surface_compatible = not required_surfaces or bool(matched_surfaces)
        if surface_compatible and strong_hits:
            selected.append({
                "skill": name,
                "state": "ACTIVE",
                "reason": "strong evidence: " + ", ".join(strong_hits[:5]),
                "companions": companions,
            })
            continue
        if surface_compatible and len(set(weak_hits)) >= minimum_weak:
            selected.append({
                "skill": name,
                "state": "ACTIVE",
                "reason": "corroborating signals: " + ", ".join(unique(weak_hits)[:5]),
                "companions": companions,
            })
            continue
        if surface_compatible and weak_hits and matched_surfaces:
            selected.append({
                "skill": name,
                "state": "ACTIVE",
                "reason": "target/scope surface " + ", ".join(matched_surfaces) + " corroborates: " + ", ".join(unique(weak_hits)[:5]),
                "companions": companions,
            })
            continue

        if all_hits:
            missing = sorted(required_surfaces.difference(active_surfaces))
            deferred.append({
                "skill": name,
                "state": "DEFERRED",
                "reason": "keyword hint is insufficient: " + ", ".join(unique(all_hits)[:5]),
                "activate_when": "observe compatible target/scope evidence" + ((": " + ", ".join(missing)) if missing else " or a second independent signal"),
            })
        elif required_surfaces.intersection(active_surfaces):
            not_applicable.append({
                "skill": name,
                "state": "NOT_APPLICABLE",
                "reason": "surface is compatible but no specialist-specific primitive, artifact, or boundary is evidenced",
            })
        else:
            not_applicable.append({
                "skill": name,
                "state": "NOT_APPLICABLE",
                "reason": "no matching target, scope, runtime, trust-boundary, or primitive evidence",
            })

    output = {
        "policy": "All skills evaluated; mandatory core plus target/scope-evidenced specialists only.",
        "target_profile": {
            "active_surfaces": active_surfaces,
            "excluded_surfaces": excluded,
            "all_detected_surface_evidence": all_surface_evidence,
            "language_runtime_evidence": language_evidence,
            "scope_supplied": bool(scope_values),
        },
        "selected": selected,
        "deferred": deferred,
        "not_applicable": not_applicable,
        "deferred_or_not_applicable": [item["skill"] for item in [*deferred, *not_applicable]],
        "warning": "Routing is a bootstrap decision, not exploit evidence. Re-route after architecture, call-path, release, or scope discoveries. Never auto-execute operational automation.",
    }

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        active_names = ", ".join(sorted(active_surfaces)) or "none confirmed"
        excluded_names = ", ".join(sorted(excluded)) or "none"
        print(f"TARGET PROFILE: {active_names}")
        print(f"SCOPE-EXCLUDED SURFACES: {excluded_names}")
        print("ACTIVE")
        for item in selected:
            print(f"- {item['skill']}: {item['reason']}")
            for companion in item["companions"]:
                print(f"    companion: {companion}")
        print("\nDEFERRED")
        if deferred:
            for item in deferred:
                print(f"- {item['skill']}: {item['reason']} [{item['activate_when']}]")
        else:
            print("- none")
        print(f"\nNOT_APPLICABLE: {len(not_applicable)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
