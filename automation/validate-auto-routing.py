#!/usr/bin/env python3
"""Validate complete mandatory auto-routing coverage and package references."""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
map_path = ROOT / "config" / "AUTO_ROUTING_MAP.json"
try:
    data = json.loads(map_path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"FAIL: cannot read routing map: {exc}")
    raise SystemExit(1)


version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
if data.get("package_version") != version:
    errors.append(f"package version mismatch map={data.get('package_version')!r} VERSION={version!r}")
policy = data.get("policy", {})
for key, expected in {
    "mandatory_entrypoint": "mandatory-auto-router",
    "evaluate_every_skill": True,
    "activate_all_relevant": True,
    "load_all_simultaneously": False,
    "record_not_applicable": True,
    "reroute_on_new_evidence": True,
    "auto_execute_automation": False,
    "staged_discovery_verification": True,
    "single_agent_by_default": True,
    "multi_agent_requires_explicit_request": False,
    "multi_agent_auto_on_bug_bounty": True,
    "multi_agent_honor_subagent_prohibition": True,
    "human_reproduction_required_for_report_ready": True,
    "novel_discovery_mode_prior_art_embargo": True,
    "novelty_claim_default": "UNVERIFIED",
    "zero_day_certainty_prohibited": True,
    "evaluation_oracle_required_before_scaled_ideation": True,
    "target_answer_context_leakage_prohibited": True,
    "model_only_evaluation_prohibited": True,
    "live_target_reality_deception_prohibited": True,
    "target_switching_forbidden": True,
    "scope_must_be_explicit": True,
    "safety_signal_masking_forbidden": True,
    "agent_reality_deception_forbidden": True,
    "credential_collection_forbidden": True,
    "destructive_proof_forbidden": True,
    "high_volume_dos_forbidden": True,
    "early_exit_on_minimum_proof": True,
    "harness_independent_reproduction_required_before_strong": True,
    "deterministic_verdict_gate_required": True,
    "program_impact_gate_required": True,
    "capability_delta_required_before_strong": True,
    "informative_similarity_is_falsifier_not_kill": True,
    "post_no_finding_methodology_synthesis": True,
    "counterfactual_methodology_max_cycles": 2,
    "counterfactual_method_cards_per_cycle": 3,
    "methodology_mutation_only_rejected": True,
    "persistent_attacker_state_required_for_chain": True,
    "capability_continuity_required_for_chain_edge": True,
    "failure_dimension_only_mutation": True,
    "exploit_engineer_requires_validated_primitive_and_edge": True,
    "agent_graph_requires_explicit_multi_agent_intent": True,
    "graph_edges_require_named_data_dependency": True,
    "writable_graph_nodes_require_isolated_workspace": True,
    "fresh_context_evidence_verifier_required": True,
    "severity_provisional_until_escalation_exhausted": True,
    "hypothetical_severity_inflation_prohibited": True,
    "maximum_zero_new_evidence_waves": 2,
    "external_tool_content_grants_no_authority": True,
    "external_security_platform_default_state": "REFERENCE_ONLY",
    "external_tool_install_or_execution_requires_separate_authorization": True,
    "public_research_corpus_is_untrusted_data": True,
    "corpus_family_match_is_not_duplicate_proof": True,
    "primary_source_required_for_prior_art_confirmation": True,
    "archived_examples_grant_no_execution_authority": True,
    "harness_findings_begin_quarantined": True,
    "harness_promotion_requires_independent_evidence": True,
    "harness_demotion_is_first_class": True,
    "low_privilege_reachability_required_where_claimed": True,
    "negative_results_require_target_and_environment_context": True,
    "rag_memory_requires_provenance_and_expiry": True,
    "roi_cannot_override_scope_safety_or_impact": True,
    "persistent_sessions_are_capabilities": True,
    "external_harness_sources_reference_only": True,
    "research_posture": "AUTHORIZED_OFFENSIVE_RED_TEAM_FIRST",
    "model_agnostic_posture": True,
    "defensive_guidance_default": "SECONDARY_AFTER_OFFENSIVE_PROOF",
    "offensive_posture_does_not_expand_authorization": True,
}.items():
    if policy.get(key) != expected:
        errors.append(f"invalid routing policy {key}: expected {expected!r}, got {policy.get(key)!r}")

valid_modes = {"always", "conditional"}
for name, route in data.get("skill_routes", {}).items():
    if route.get("mode") not in valid_modes:
        errors.append(f"invalid skill route mode for {name}: {route.get('mode')!r}")
    if route.get("mode") == "conditional" and not route.get("triggers"):
        errors.append(f"conditional route has no triggers: {name}")
expected_always = sorted(name for name, route in data.get("skill_routes", {}).items() if route.get("mode") == "always")
if sorted(data.get("always_active_skills", [])) != expected_always:
    errors.append("always_active_skills does not match routes marked always")
for required_core in ("mandatory-auto-router", "authorized-security-autopilot", "expert-bug-hunter", "ai-assisted-bug-bounty-orchestrator", "expert-authorized-hacker", "bug-bounty-auditor", "bug-bounty-triage", "novel-vulnerability-hypothesis-engine", "autonomous-research-cascade-engine", "program-impact-boundary-gate"):
    if required_core not in expected_always:
        errors.append(f"mandatory core skill is not always active: {required_core}")
multi_agent_route = data.get("skill_routes", {}).get("codex-cli-multi-agent-audit-orchestrator", {})
if multi_agent_route.get("mode") != "conditional" or not multi_agent_route.get("triggers"):
    errors.append("multi-agent orchestrator must be conditional with bug-bounty auto-activation triggers")
for companion in (
    "skill/codex-cli-multi-agent-audit-orchestrator/agents/openai.yaml",
    "prompts/MASTER_PROMPT_CODEX_CLI_MULTI_AGENT_AUDIT.md",
    "references/CODEX_CLI_MULTI_AGENT_WORKFLOW.md",
):
    if companion not in multi_agent_route.get("companions", []):
        errors.append(f"multi-agent orchestrator route is missing companion: {companion}")
for trigger in (
    "bug bounty",
    "vrp",
    "hackerone",
    "buruan bug",
    "cursor subagents",
    "cursor task agents",
    "use subagents",
    "delegasi",
    "parallel agents",
    "multi-agent review",
    "multi-agent audit",
):
    if trigger not in multi_agent_route.get("triggers", []):
        errors.append(f"multi-agent orchestrator is missing auto-activation trigger: {trigger}")
apex_route = data.get("skill_routes", {}).get("apex-black", {})
if apex_route.get("mode") != "conditional":
    errors.append("APEX BLACK must use evidence-conditional implicit routing")
if "apex-black" in data.get("selection_policy", {}).get("explicit_intent_skills", []):
    errors.append("APEX BLACK must not require explicit name-based invocation")
for trigger in ("authorized security audit", "audit keamanan aplikasi", "autonomous pentest"):
    if trigger not in apex_route.get("triggers", []):
        errors.append(f"APEX BLACK implicit route is missing trigger: {trigger}")
for companion in (
    "skill/apex-black/prompts/APEX_BLACK_ROOT_PROMPT.md",
    "skill/apex-black/references/APEX_BLACK_METHOD.md",
    "skill/apex-black/agents/openai.yaml",
):
    if companion not in apex_route.get("companions", []):
        errors.append(f"APEX BLACK route is missing companion: {companion}")
dynamic_filter_skill = "dynamic-filter-evaluator-rce-hunter"
dynamic_filter_route = data.get("skill_routes", {}).get(dynamic_filter_skill, {})
if dynamic_filter_route.get("mode") != "conditional":
    errors.append("dynamic-filter evaluator RCE skill must be conditional")
for trigger in ("graphql filter", "filter: json", "$where", "sift", "new function"):
    if trigger not in dynamic_filter_route.get("triggers", []):
        errors.append(f"dynamic-filter evaluator route is missing trigger: {trigger}")
dynamic_filter_method = "skill/dynamic-filter-evaluator-rce-hunter/references/dynamic-filter-evaluator-rce-method.md"
if dynamic_filter_method not in dynamic_filter_route.get("companions", []):
    errors.append("dynamic-filter evaluator route does not load its method reference")
cross_runtime_skill = "cross-language-script-injection-hunter"
cross_runtime_route = data.get("skill_routes", {}).get(cross_runtime_skill, {})
if cross_runtime_route.get("mode") != "conditional":
    errors.append("cross-language script injection skill must be conditional")
for trigger in (
    "cross-language script injection",
    "generated javascript",
    "ruby heredoc javascript",
    "open3.capture3",
):
    if trigger not in cross_runtime_route.get("triggers", []):
        errors.append(f"cross-language script injection route is missing trigger: {trigger}")
cross_runtime_method = "skill/cross-language-script-injection-hunter/references/cross-language-script-injection-rce-method.md"
if cross_runtime_method not in cross_runtime_route.get("companions", []):
    errors.append("cross-language script injection route does not load its method reference")
llm_token_skill = "llm-tokenization-boundary-hunter"
llm_token_route = data.get("skill_routes", {}).get(llm_token_skill, {})
if llm_token_route.get("mode") != "conditional":
    errors.append("LLM tokenization boundary skill must be conditional")
for trigger in (
    "repeated token attack",
    "repeated tokens",
    "instruction blackout",
    "model divergence",
    "llm-security",
):
    if trigger not in llm_token_route.get("triggers", []):
        errors.append(f"LLM tokenization boundary route is missing trigger: {trigger}")
llm_token_method = "skill/llm-tokenization-boundary-hunter/references/repeated-token-llm-security-method.md"
if llm_token_method not in llm_token_route.get("companions", []):
    errors.append("LLM tokenization boundary route does not load its method reference")
credential_skill = "credential-exposure-capability-hunter"
credential_route = data.get("skill_routes", {}).get(credential_skill, {})
if credential_route.get("mode") != "conditional":
    errors.append("credential exposure capability skill must be conditional")
for trigger in (
    "credential exposure",
    "credential disclosure",
    "hard-coded api token",
    "secret in slack",
    "jira api token",
    "mastodon admin api token",
    "admin api token in slack",
    "staging admin token",
    "aws access key exposure",
    "database credentials exposed",
    "credentials in docker image",
    "credential in image layer",
    "effective permissions",
):
    if trigger not in credential_route.get("triggers", []):
        errors.append(f"credential exposure capability route is missing trigger: {trigger}")
credential_method = "skill/credential-exposure-capability-hunter/references/credential-exposure-capability-method.md"
if credential_method not in credential_route.get("companions", []):
    errors.append("credential exposure capability route does not load its method reference")
native_lifetime_skill = "native-js-binding-lifetime-hunter"
native_lifetime_route = data.get("skill_routes", {}).get(native_lifetime_skill, {})
if native_lifetime_route.get("mode") != "conditional":
    errors.append("native JavaScript binding lifetime skill must be conditional")
for trigger in (
    "native javascript binding lifetime",
    "v8 binding uaf",
    "gin::wrappable",
    "base::unretained provider",
    "renderer use-after-free",
    "jsethereumprovider",
):
    if trigger not in native_lifetime_route.get("triggers", []):
        errors.append(f"native JavaScript binding lifetime route is missing trigger: {trigger}")
native_lifetime_method = "skill/native-js-binding-lifetime-hunter/references/native-js-binding-lifetime-uaf-method.md"
if native_lifetime_method not in native_lifetime_route.get("companions", []):
    errors.append("native JavaScript binding lifetime route does not load its method reference")
github_actions_fork_skill = "github-actions-fork-trust-hunter"
github_actions_fork_route = data.get("skill_routes", {}).get(github_actions_fork_skill, {})
if github_actions_fork_route.get("mode") != "conditional":
    errors.append("GitHub Actions fork trust skill must be conditional")
for trigger in (
    "github actions fork trust",
    "fork pr npm ci",
    "actions checkout persist-credentials",
    "github token in git config",
    "workflow_run untrusted artifact",
    "fork pr supply chain",
    "same job workspace tampering",
    "trusted script after untrusted build",
    "semver-label.yml",
):
    if trigger not in github_actions_fork_route.get("triggers", []):
        errors.append(f"GitHub Actions fork trust route is missing trigger: {trigger}")
github_actions_fork_method = "skill/github-actions-fork-trust-hunter/references/github-actions-fork-trust-method.md"
if github_actions_fork_method not in github_actions_fork_route.get("companions", []):
    errors.append("GitHub Actions fork trust route does not load its method reference")
deadlock_skill = "deadlock-lock-graph-dos-hunter"
deadlock_route = data.get("skill_routes", {}).get(deadlock_skill, {})
if deadlock_route.get("mode") != "conditional":
    errors.append("deadlock lock-graph DoS skill must be conditional")
for trigger in (
    "remote rpc deadlock",
    "logging lock deadlock",
    "lock-order inversion",
    "circular wait",
    "wait-for graph",
    "thread dump deadlock",
    "monero 3307874",
):
    if trigger not in deadlock_route.get("triggers", []):
        errors.append(f"deadlock lock-graph route is missing trigger: {trigger}")
deadlock_method = "skill/deadlock-lock-graph-dos-hunter/references/deadlock-lock-graph-dos-method.md"
if deadlock_method not in deadlock_route.get("companions", []):
    errors.append("deadlock lock-graph route does not load its method reference")
xss2shell_skill = "compositional-exploit-chain-hunter"
xss2shell_route = data.get("skill_routes", {}).get(xss2shell_skill, {})
for trigger in (
    "xss2shell",
    "cve-2026-64638",
    "ghsa-52p2-r8wf-jcrf",
    "wordpress login xss to rce",
    "dom clobbering to application password",
    "application password to plugin upload",
):
    if trigger not in xss2shell_route.get("triggers", []):
        errors.append(f"XSS2Shell compositional route is missing trigger: {trigger}")
xss2shell_method = "skill/compositional-exploit-chain-hunter/references/wordpress-xss2shell-seven-boundary-method.md"
if xss2shell_method not in xss2shell_route.get("companions", []):
    errors.append("XSS2Shell route does not load its seven-boundary method")

xchain_skill = "exploit-chain-research-orchestrator"
xchain_route = data.get("skill_routes", {}).get(xchain_skill, {})
if xchain_route.get("mode") != "conditional":
    errors.append("exploit-chain research orchestrator must be conditional")
for trigger in (
    "full exploit chain",
    "attacker state transition",
    "primitive to capability",
    "capability expander",
    "chain edge validation",
    "failure driven mutation",
    "xchain-lab-v1",
):
    if trigger not in xchain_route.get("triggers", []):
        errors.append(f"exploit-chain research route is missing trigger: {trigger}")
xchain_companions = (
    "skill/exploit-chain-research-orchestrator/prompts/CHAIN_ROOT_PROMPT.md",
    "skill/exploit-chain-research-orchestrator/prompts/PRIMITIVE_HUNTER_PROMPT.md",
    "skill/exploit-chain-research-orchestrator/prompts/CAPABILITY_ANALYZER_PROMPT.md",
    "skill/exploit-chain-research-orchestrator/prompts/CHAIN_LINKER_PROMPT.md",
    "skill/exploit-chain-research-orchestrator/prompts/EXPLOIT_ENGINEER_PROMPT.md",
    "skill/exploit-chain-research-orchestrator/prompts/CHAIN_FALSIFIER_PROMPT.md",
    "skill/exploit-chain-research-orchestrator/references/ATTACKER_STATE_TRANSITION_METHOD.md",
    "skill/exploit-chain-research-orchestrator/references/PRIMITIVE_TO_CAPABILITY_METHOD.md",
    "skill/exploit-chain-research-orchestrator/references/CHAIN_COMPOSITION_METHOD.md",
    "skill/exploit-chain-research-orchestrator/references/EXPLOITABILITY_ESCALATION_METHOD.md",
    "skill/exploit-chain-research-orchestrator/references/RUNTIME_CHAIN_VALIDATION.md",
    "skill/exploit-chain-research-orchestrator/config/ATTACKER_STATE_SCHEMA.json",
    "skill/exploit-chain-research-orchestrator/config/PRIMITIVE_SCHEMA.json",
    "skill/exploit-chain-research-orchestrator/config/CHAIN_GRAPH_SCHEMA.json",
    "skill/exploit-chain-research-orchestrator/scripts/xchain_engine.py",
    "skill/exploit-chain-research-orchestrator/scripts/test_xchain_engine.py",
)
for companion in xchain_companions:
    if companion not in xchain_route.get("companions", []):
        errors.append(f"exploit-chain research route missing companion: {companion}")

v8_chain_prompts = (
    "skill/chromium-v8-variant-hunter/prompts/v8-type-reasoning-agent.md",
    "skill/chromium-v8-variant-hunter/prompts/v8-representation-agent.md",
    "skill/chromium-v8-variant-hunter/prompts/v8-jit-assumption-agent.md",
    "skill/chromium-v8-variant-hunter/prompts/v8-gc-lifetime-agent.md",
    "skill/chromium-v8-variant-hunter/prompts/v8-sandbox-boundary-agent.md",
    "skill/chromium-v8-variant-hunter/prompts/v8-exploitability-agent.md",
    "skill/chromium-v8-variant-hunter/prompts/chrome-chain-linker.md",
)
v8_route = data.get("skill_routes", {}).get("chromium-v8-variant-hunter", {})
for companion in v8_chain_prompts:
    if companion not in v8_route.get("companions", []):
        errors.append(f"Chromium/V8 route missing chain-role prompt: {companion}")

selection = data.get("selection_policy", {})
for key, expected in {
    "strategy": "target-scope-evidence-first",
    "keyword_only_is_hint": True,
    "scope_exclusions_override_positive_matches": True,
}.items():
    if selection.get(key) != expected:
        errors.append(f"invalid selection policy {key}: expected {expected!r}, got {selection.get(key)!r}")
if not isinstance(selection.get("minimum_independent_weak_signals"), int) or selection.get("minimum_independent_weak_signals", 0) < 2:
    errors.append("selection policy must require at least two independent weak signals")
surface_terms = selection.get("surface_terms", {})
if not isinstance(surface_terms, dict) or not surface_terms or any(not terms for terms in surface_terms.values()):
    errors.append("selection policy surface_terms must define non-empty target profiles")
route_names = set(data.get("skill_routes", {}))
explicit_intent = set(selection.get("explicit_intent_skills", []))
explicit_phrases = selection.get("explicit_intent_phrases", {})
if "codex-cli-multi-agent-audit-orchestrator" in explicit_intent:
    errors.append("multi-agent orchestrator must auto-activate on bug bounty and must not remain explicit-intent")
if set(explicit_phrases) != explicit_intent:
    errors.append("explicit-intent skills and explicit-intent phrase maps must match exactly")
for name in explicit_intent:
    if name not in route_names:
        errors.append(f"explicit-intent selection references unknown skill: {name}")
    elif data["skill_routes"][name].get("mode") != "conditional":
        errors.append(f"explicit-intent skill must be conditional: {name}")
    if not explicit_phrases.get(name):
        errors.append(f"explicit-intent skill has no explicit request phrases: {name}")
for surface, names in selection.get("primary_surface_skills", {}).items():
    if surface not in surface_terms:
        errors.append(f"primary skill map references unknown surface: {surface}")
    for name in names:
        if name not in route_names:
            errors.append(f"primary skill map references unknown skill: {name}")
for name, surfaces in selection.get("skill_surface_requirements", {}).items():
    if name not in route_names:
        errors.append(f"surface requirement references unknown skill: {name}")
    for surface in surfaces:
        if surface not in surface_terms:
            errors.append(f"surface requirement for {name} references unknown surface: {surface}")
if not selection.get("ambiguous_single_triggers"):
    errors.append("selection policy must enumerate ambiguous single triggers")

skill_files = {
    p.parent.name: p
    for p in [
        *(ROOT / "skill").glob("*/SKILL.md"),
        *ROOT.glob("*/SKILL.md"),
    ]
}
skills = sorted(skill_files)
routed = sorted(data.get("skill_routes", {}))
unmapped_skills = sorted(set(skills) - set(routed))
extra_routes = sorted(set(routed) - set(skills))
if unmapped_skills or extra_routes:
    errors.append(f"skill coverage mismatch missing={unmapped_skills} extra={extra_routes}")
if len(skills) != 84 or len(routed) != 84:
    errors.append(f"expected 84 installed and routed skills, got installed={len(skills)} routed={len(routed)}")
orch_skill = skill_files.get("codex-cli-multi-agent-audit-orchestrator")
if orch_skill is None:
    errors.append("missing installed skill: codex-cli-multi-agent-audit-orchestrator")
else:
    orch_text = orch_skill.read_text(encoding="utf-8")
    if "not Codex-CLI-only" not in orch_text:
        errors.append("multi-agent orchestrator must declare it is not Codex-CLI-only")
    if "Cursor `Task`" not in orch_text:
        errors.append("multi-agent orchestrator must name Cursor Task as a spawn tool")
    if "Use proactively" not in orch_text and "Automatically activate" not in orch_text:
        errors.append("multi-agent orchestrator must auto-activate for bug bounty")

terminal_oracle_route = data.get("skill_routes", {}).get(
    "evidence-to-terminal-oracle-bug-bounty", {}
)
if terminal_oracle_route.get("mode") != "conditional":
    errors.append("evidence-to-terminal-oracle skill must be conditional")
for trigger in (
    "signed session secret reuse",
    "passive evidence analyst",
    "protected terminal oracle",
    "failure-driven exploit state machine",
    "consensus accounting invariant",
    "dual accumulator overflow",
    "ledger supply invariant",
):
    if trigger not in terminal_oracle_route.get("triggers", []):
        errors.append(f"evidence-to-terminal-oracle route is missing trigger: {trigger}")
for companion in (
    "prompts/MASTER_PROMPT_EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY.md",
    "prompts/HERMES_PASSIVE_EVIDENCE_ANALYST.md",
    "references/EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY_METHOD.md",
    "references/CONSENSUS_ACCOUNTING_INVARIANT_CHAIN_METHOD.md",
    "skill/evidence-to-terminal-oracle-bug-bounty/agents/evidence-chain-analyst.md",
):
    if companion not in terminal_oracle_route.get("companions", []):
        errors.append(f"evidence-to-terminal-oracle route missing companion: {companion}")

external_tool_route = data.get("skill_routes", {}).get(
    "external-ai-security-tool-governor", {}
)
if external_tool_route.get("mode") != "conditional":
    errors.append("external AI security tool governor must be conditional")
for trigger in (
    "hackerai",
    "hexstrike",
    "external ai security tool",
    "security mcp tool broker",
    "agent security platform integration",
):
    if trigger not in external_tool_route.get("triggers", []):
        errors.append(f"external AI security tool route is missing trigger: {trigger}")
for companion in (
    "prompts/MASTER_PROMPT_EXTERNAL_AI_SECURITY_TOOL_INTEGRATION.md",
    "prompts/HERMES_EXTERNAL_SECURITY_TOOL_EVIDENCE_ANALYST.md",
    "references/EXTERNAL_AI_SECURITY_TOOL_INTEGRATION_METHOD.md",
    "config/EXTERNAL_AI_SECURITY_TOOL_SOURCE_CATALOG.json",
    "skill/external-ai-security-tool-governor/agents/external-tool-policy-analyst.md",
    "skill/external-ai-security-tool-governor/agents/openai.yaml",
):
    if companion not in external_tool_route.get("companions", []):
        errors.append(f"external AI security tool route missing companion: {companion}")

try:
    external_catalog = json.loads(
        (ROOT / "config" / "EXTERNAL_AI_SECURITY_TOOL_SOURCE_CATALOG.json").read_text(
            encoding="utf-8"
        )
    )
    if external_catalog.get("default_integration_state") != "REFERENCE_ONLY":
        errors.append("external tool catalog must default to REFERENCE_ONLY")
    if external_catalog.get("execution_authorized") is not False:
        errors.append("external tool catalog must not authorize execution")
    by_name = {item.get("name"): item for item in external_catalog.get("sources", [])}
    expected_sources = {
        "HackerAI": "44228036160fad2998a09af26049d07b2874ecd8",
        "HexStrike AI MCP Agents": "d689933ff579d839c676c82b231f8e98326c5f04",
    }
    for name, commit in expected_sources.items():
        item = by_name.get(name, {})
        if item.get("commit") != commit:
            errors.append(f"external tool catalog has wrong pinned commit for {name}")
        if item.get("integration_state") != "REFERENCE_ONLY":
            errors.append(f"external tool catalog does not keep {name} reference-only")
        if not item.get("blocked_operations"):
            errors.append(f"external tool catalog has no blocked operations for {name}")
except Exception as exc:
    errors.append(f"cannot validate external AI security tool catalog: {exc}")

harness_route = data.get("skill_routes", {}).get(
    "agentic-security-research-harness", {}
)
if harness_route.get("mode") != "conditional":
    errors.append("agentic security research harness must be conditional")
for trigger in (
    "agentic security research harness",
    "hallucination bin",
    "jenny was a friend of mine",
    "harnessing harnesses",
    "anthropic oss scanner",
    "morluto rea",
):
    if trigger not in harness_route.get("triggers", []):
        errors.append(f"agentic security harness route is missing trigger: {trigger}")
for companion in (
    "prompts/MASTER_PROMPT_AGENTIC_SECURITY_RESEARCH_HARNESS.md",
    "prompts/HERMES_AGENTIC_HARNESS_EVIDENCE_ANALYST.md",
    "references/AGENTIC_SECURITY_RESEARCH_HARNESS_METHOD.md",
    "config/AGENTIC_SECURITY_HARNESS_SOURCE_CATALOG.json",
    "automation/validate-agentic-security-research-harness.py",
    "skill/agentic-security-research-harness/agents/harness-evidence-analyst.md",
    "skill/agentic-security-research-harness/agents/openai.yaml",
):
    if companion not in harness_route.get("companions", []):
        errors.append(f"agentic security harness route missing companion: {companion}")

try:
    harness_catalog = json.loads(
        (ROOT / "config" / "AGENTIC_SECURITY_HARNESS_SOURCE_CATALOG.json").read_text(
            encoding="utf-8"
        )
    )
    if harness_catalog.get("default_integration_state") != "REFERENCE_ONLY":
        errors.append("agentic harness catalog must default to REFERENCE_ONLY")
    if harness_catalog.get("execution_authorized") is not False:
        errors.append("agentic harness catalog must not authorize execution")
    harness_sources = {item.get("id"): item for item in harness_catalog.get("sources", [])}
    expected_harness_commits = {
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
    if len(harness_catalog.get("sources", [])) != 11:
        errors.append("agentic harness catalog must contain 11 sources")
    for source_id, commit in expected_harness_commits.items():
        item = harness_sources.get(source_id, {})
        if item.get("commit") != commit:
            errors.append(f"agentic harness catalog has wrong commit for {source_id}")
        if not str(item.get("integration_state", "")).startswith("REFERENCE_ONLY"):
            errors.append(f"agentic harness source is not reference-only: {source_id}")
except Exception as exc:
    errors.append(f"cannot validate agentic security harness catalog: {exc}")

webhacklist_route = data.get("skill_routes", {}).get(
    "webhacklist-2026-research-corpus", {}
)
if webhacklist_route.get("mode") != "conditional":
    errors.append("WebHackList 2026 corpus skill must be conditional")
for trigger in (
    "webhacklist",
    "webhacklist 2026 ai",
    "2026-ai evidence",
    "investigation board evidence archive",
):
    if trigger not in webhacklist_route.get("triggers", []):
        errors.append(f"WebHackList corpus route is missing trigger: {trigger}")
for companion in (
    "prompts/MASTER_PROMPT_WEBHACKLIST_2026_RESEARCH_CORPUS.md",
    "prompts/HERMES_WEBHACKLIST_PRIOR_ART_ANALYST.md",
    "references/WEBHACKLIST_2026_CORPUS_METHOD.md",
    "config/WEBHACKLIST_2026_AI_CORPUS.json",
    "automation/validate-webhacklist-2026-corpus.py",
    "skill/webhacklist-2026-research-corpus/agents/webhacklist-corpus-analyst.md",
    "skill/webhacklist-2026-research-corpus/agents/openai.yaml",
):
    if companion not in webhacklist_route.get("companions", []):
        errors.append(f"WebHackList corpus route missing companion: {companion}")

try:
    webhacklist_catalog = json.loads(
        (ROOT / "config" / "WEBHACKLIST_2026_AI_CORPUS.json").read_text(
            encoding="utf-8"
        )
    )
    if webhacklist_catalog.get("status") != (
        "PRELIMINARY_UNRANKED_AI_COLLECTED_NOT_COMMUNITY_VETTED_REFERENCE_ONLY"
    ):
        errors.append("WebHackList catalog lost preliminary/reference-only status")
    if webhacklist_catalog.get("snapshot", {}).get("commit") != (
        "2f17d6249c178f9b895d2c00536a3009df117afa"
    ):
        errors.append("WebHackList catalog has wrong pinned commit")
    coverage = webhacklist_catalog.get("coverage", {})
    if coverage.get("records_total") != 299:
        errors.append("WebHackList catalog must contain 299 records")
    if coverage.get("archived_records_fully_read") != 298:
        errors.append("WebHackList catalog must preserve 298 full archive reads")
    if coverage.get("live_primary_records_read") != 1:
        errors.append("WebHackList catalog must preserve one indexed primary read")
    if coverage.get("archive_path_digest_root") != (
        "4f24ca8755c30916491b579d300915e058c975bb8cc318ce354098e26e2a9476"
    ):
        errors.append("WebHackList catalog has wrong archive digest root")
    if len(webhacklist_catalog.get("records", [])) != 299:
        errors.append("WebHackList record ledger length mismatch")
except Exception as exc:
    errors.append(f"cannot validate WebHackList 2026 corpus catalog: {exc}")

try:
    consensus_method_text = (
        ROOT / "references" / "CONSENSUS_ACCOUNTING_INVARIANT_CHAIN_METHOD.md"
    ).read_text(encoding="utf-8").lower()
    for required_phrase in (
        "consensus_accounting_invariant_chain:v1",
        "arbitrary-precision",
        "commit -> finality",
        "spendability",
        "official release artifact",
        "public networks",
        "user-supplied prior art",
    ):
        if required_phrase not in consensus_method_text:
            errors.append(
                "consensus-accounting method missing contract: "
                f"{required_phrase}"
            )
except Exception as exc:
    errors.append(f"cannot validate consensus-accounting method: {exc}")

manual_activation_required = sorted(
    set(unmapped_skills)
    | ({"authorized-security-autopilot"} if data.get("skill_routes", {}).get("authorized-security-autopilot", {}).get("mode") != "always" else set())
)

for name in skills:
    p = skill_files[name]
    text = p.read_text(encoding="utf-8")
    if "MANDATORY_AUTO_ROUTER_CONTRACT:v1" not in text:
        errors.append(f"missing router contract: {p.relative_to(ROOT)}")
    if name != "mandatory-auto-router" and "mandatory auto-router" not in text.split("---", 2)[1].lower():
        errors.append(f"frontmatter description does not advertise router bootstrap: {p.relative_to(ROOT)}")
    prohibited_skill_terms = ("writeup", "write-up", "report-writer", "report_writer", "submission-writer")
    if any(term in name.lower() for term in prohibited_skill_terms):
        errors.append(f"prohibited writing/report skill present: {name}")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append(f"invalid frontmatter boundary: {p.relative_to(ROOT)}")
    if not re.search(r"^name:\s*", text, re.M) or not re.search(r"^description:\s*", text, re.M):
        errors.append(f"missing frontmatter keys: {p.relative_to(ROOT)}")
    if "AUTHORIZED_OFFENSIVE_POSTURE:v1" not in text:
        errors.append(f"missing authorized offensive posture: {p.relative_to(ROOT)}")
    if "MODEL_AGNOSTIC_RUNTIME:v1" not in text:
        errors.append(f"missing model-agnostic runtime contract: {p.relative_to(ROOT)}")
    if "attacker objective -> reachable entrypoint -> exploit chain" not in text:
        errors.append(f"offensive posture lacks attack-path sequence: {p.relative_to(ROOT)}")
    if "offensive-first posture" not in text.split("---", 2)[1].lower():
        errors.append(f"frontmatter description lacks offensive-first default: {p.relative_to(ROOT)}")
    if "model-agnostic" not in text.lower() and "not to Codex" not in text:
        errors.append(f"skill does not declare model-agnostic runtime: {p.relative_to(ROOT)}")

prompt_files = sorted((ROOT / "prompts").glob("*.md"))
for p in prompt_files:
    text = p.read_text(encoding="utf-8")
    if "AUTHORIZED_OFFENSIVE_PROMPT:v1" not in text:
        errors.append(f"missing authorized offensive prompt contract: {p.relative_to(ROOT)}")
    if "produce those defensive outputs after offensive proof" not in text:
        errors.append(f"prompt does not keep defensive analysis secondary: {p.relative_to(ROOT)}")

agent_files = sorted(
    p for p in ROOT.glob("**/agents/openai.yaml")
    if "vendor" not in p.relative_to(ROOT).parts
)
for p in agent_files:
    text = p.read_text(encoding="utf-8")
    if "default_prompt:" not in text:
        errors.append(f"agent metadata has no default prompt: {p.relative_to(ROOT)}")
    if "offensive-first" not in text.lower():
        errors.append(f"agent metadata lacks offensive-first default: {p.relative_to(ROOT)}")
    if "model-agnostic" not in text.lower():
        errors.append(f"agent metadata is not model-agnostic: {p.relative_to(ROOT)}")

for name, route in data.get("skill_routes", {}).items():
    for rel in route.get("companions", []):
        if not (ROOT / rel).is_file():
            errors.append(f"missing companion for {name}: {rel}")

actual_support = sorted(
    [p.relative_to(ROOT).as_posix()
     for top in ("prompts", "references", "config", "automation")
     for p in (ROOT / top).glob("*") if p.is_file()]
    + [rel for rel in ("AUTOLOAD.md", "README.md", "CHANGELOG.md", "VERSION", "PACKAGE_MANIFEST.sha256") if (ROOT / rel).is_file()]
)
routed_support = sorted(data.get("artifact_routes", {}))
if len(actual_support) != 142 or len(routed_support) != 142:
    errors.append(
        f"expected 142 shared supporting artifacts, got actual={len(actual_support)} routed={len(routed_support)}"
    )
for rel in actual_support:
    lowered = rel.lower()
    if any(term in lowered for term in ("writeup", "write-up", "report-writer", "submission-writer")):
        errors.append(f"prohibited writing/report artifact present: {rel}")
for rel, route in data.get("artifact_routes", {}).items():
    if route.get("mode") not in valid_modes:
        errors.append(f"invalid artifact route mode for {rel}: {route.get('mode')!r}")
    if not (ROOT / rel).is_file():
        errors.append(f"routed artifact does not exist: {rel}")
if actual_support != routed_support:
    errors.append(f"support artifact coverage mismatch missing={sorted(set(actual_support)-set(routed_support))} extra={sorted(set(routed_support)-set(actual_support))}")

for required in [
    "AUTOLOAD.md",
    "authorized-security-autopilot/SKILL.md",
    "skill/codex-cli-multi-agent-audit-orchestrator/SKILL.md",
    "skill/codex-cli-multi-agent-audit-orchestrator/agents/openai.yaml",
    "prompts/MASTER_PROMPT_CODEX_CLI_MULTI_AGENT_AUDIT.md",
    "references/CODEX_CLI_MULTI_AGENT_WORKFLOW.md",
    "config/CODEX_CLI_CANDIDATE_SCHEMA.json",
    "prompts/MASTER_PROMPT_MANDATORY_AUTO_ROUTER.md",
    "prompts/SYSTEM_PROMPT_AUTHORIZED_OFFENSIVE_IMPACT_GATE.md",
    "references/AUTO_ROUTING_PROTOCOL.md",
    "references/BUGBOUNTY_INFO_ATTACK_SURFACE_CHAIN_TOOLING_METHOD.md",
    "references/IMAGE_DECODER_SSO_CONNECTOR_CHAIN_METHOD.md",
    "skill/evidence-to-terminal-oracle-bug-bounty/SKILL.md",
    "skill/evidence-to-terminal-oracle-bug-bounty/agents/openai.yaml",
    "skill/evidence-to-terminal-oracle-bug-bounty/agents/evidence-chain-analyst.md",
    "prompts/MASTER_PROMPT_EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY.md",
    "prompts/HERMES_PASSIVE_EVIDENCE_ANALYST.md",
    "references/EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY_METHOD.md",
    "references/CONSENSUS_ACCOUNTING_INVARIANT_CHAIN_METHOD.md",
    "skill/external-ai-security-tool-governor/SKILL.md",
    "skill/external-ai-security-tool-governor/agents/openai.yaml",
    "skill/external-ai-security-tool-governor/agents/external-tool-policy-analyst.md",
    "prompts/MASTER_PROMPT_EXTERNAL_AI_SECURITY_TOOL_INTEGRATION.md",
    "prompts/HERMES_EXTERNAL_SECURITY_TOOL_EVIDENCE_ANALYST.md",
    "references/EXTERNAL_AI_SECURITY_TOOL_INTEGRATION_METHOD.md",
    "config/EXTERNAL_AI_SECURITY_TOOL_SOURCE_CATALOG.json",
    "skill/agentic-security-research-harness/SKILL.md",
    "skill/agentic-security-research-harness/agents/openai.yaml",
    "skill/agentic-security-research-harness/agents/harness-evidence-analyst.md",
    "prompts/MASTER_PROMPT_AGENTIC_SECURITY_RESEARCH_HARNESS.md",
    "prompts/HERMES_AGENTIC_HARNESS_EVIDENCE_ANALYST.md",
    "references/AGENTIC_SECURITY_RESEARCH_HARNESS_METHOD.md",
    "config/AGENTIC_SECURITY_HARNESS_SOURCE_CATALOG.json",
    "automation/validate-agentic-security-research-harness.py",
    "skill/webhacklist-2026-research-corpus/SKILL.md",
    "skill/webhacklist-2026-research-corpus/agents/openai.yaml",
    "skill/webhacklist-2026-research-corpus/agents/webhacklist-corpus-analyst.md",
    "prompts/MASTER_PROMPT_WEBHACKLIST_2026_RESEARCH_CORPUS.md",
    "prompts/HERMES_WEBHACKLIST_PRIOR_ART_ANALYST.md",
    "references/WEBHACKLIST_2026_CORPUS_METHOD.md",
    "config/WEBHACKLIST_2026_AI_CORPUS.json",
    "automation/validate-webhacklist-2026-corpus.py",
    "skill/program-impact-boundary-gate/SKILL.md",
    "skill/program-impact-boundary-gate/agents/openai.yaml",
    "prompts/MASTER_PROMPT_PROGRAM_IMPACT_BOUNDARY_GATE.md",
    "references/PROGRAM_IMPACT_BOUNDARY_GATE.md",
    "config/PROGRAM_IMPACT_NEGATIVE_CONTROL_CASES.json",
    "config/PROGRAM_IMPACT_POSITIVE_CONTROL_CASES.json",
    "automation/test-program-impact-boundary-gate.py",
    "skill/counterfactual-methodology-synthesizer/SKILL.md",
    "skill/counterfactual-methodology-synthesizer/agents/openai.yaml",
    "prompts/MASTER_PROMPT_COUNTERFACTUAL_METHODOLOGY_SYNTHESIS.md",
    "references/COUNTERFACTUAL_METHODOLOGY_SYNTHESIS_METHOD.md",
    "config/COUNTERFACTUAL_METHODOLOGY_REGRESSION_CASES.json",
    "automation/validate-counterfactual-methodology.py",
    "automation/test-counterfactual-methodology.py",
    "config/AUTO_ROUTING_MAP.json",
    "skill/bountyforge-research-suite/SKILL.md",
    "skill/bountyforge-research-suite/agents/openai.yaml",
    "skill/bountyforge-research-suite/agents/bountyforge-evidence-agent.md",
    "prompts/MASTER_PROMPT_BOUNTYFORGE_RESEARCH_SUITE.md",
    "references/BOUNTYFORGE_ADAPTIVE_RESEARCH_METHOD.md",
    "config/BOUNTYFORGE_SOURCE_CATALOG.json",
    "skill/apex-black/SKILL.md",
    "skill/apex-black/agents/openai.yaml",
    "skill/apex-black/prompts/APEX_BLACK_ROOT_PROMPT.md",
    "skill/apex-black/references/APEX_BLACK_METHOD.md",
    "skill/offensive-research-graph-engineer/SKILL.md",
    "skill/offensive-research-graph-engineer/agents/openai.yaml",
    "skill/offensive-research-graph-engineer/agents/graph-worker-node.md",
    "skill/offensive-research-graph-engineer/agents/fresh-evidence-verifier-node.md",
    "skill/offensive-research-graph-engineer/agents/severity-escalation-node.md",
    "prompts/MASTER_PROMPT_OFFENSIVE_RESEARCH_GRAPH_ENGINEERING.md",
    "references/OFFENSIVE_RESEARCH_GRAPH_ENGINEERING_METHOD.md",
    "references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md",
    "config/OFFENSIVE_RESEARCH_GRAPH_SCHEMA.json",
    "config/SEVERITY_ESCALATION_SCHEMA.json",
    "automation/route-security-task.py",
    "automation/test-route-security-task.py",
    "automation/test-authorization-invariant-gate.py",
    "config/AUTHORIZATION_REASONING_REGRESSION_CASES.json",
    "references/AUTHORIZATION_INVARIANT_KILL_CHALLENGE.md",
    "references/PATCH_VARIANT_CONSUMER_BOUNDARY_METHOD.md",
    "automation/test-patch-variant-consumer-boundary.py",
    "config/PATCH_VARIANT_CONSUMER_BOUNDARY_REGRESSION_CASES.json",
    "references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md",
    "automation/test-dynamic-data-execution-consumer.py",
    "config/DYNAMIC_DATA_EXECUTION_CONSUMER_REGRESSION_CASES.json",
    "references/ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md",
    "automation/test-archive-renderer-framework.py",
    "config/ARCHIVE_RENDERER_FRAMEWORK_REGRESSION_CASES.json",
    "references/REPARSE_CONFIG_PROVENANCE_METHOD.md",
    "automation/test-reparse-config-provenance.py",
    "config/REPARSE_CONFIG_PROVENANCE_REGRESSION_CASES.json",
    "references/PATH_CLI_GADGET_CHAIN_METHOD.md",
    "automation/test-path-cli-gadget-chain.py",
    "config/PATH_CLI_GADGET_CHAIN_REGRESSION_CASES.json",
    "skill/novel-vulnerability-hypothesis-engine/SKILL.md",
    "skill/novel-vulnerability-hypothesis-engine/agents/openai.yaml",
    "prompts/MASTER_PROMPT_NOVEL_INVARIANT_FRONTIER.md",
    "references/NOVEL_INVARIANT_FRONTIER_METHOD.md",
    "references/STATE_MACHINE_SECURITY_METHOD.md",
    "references/METAMORPHIC_DIFFERENTIAL_METHOD.md",
    "references/RESOURCE_AMPLIFICATION_METHOD.md",
    "references/CROSS_FEATURE_COMPOSITION_METHOD.md",
    "references/EVALUATION_FIRST_RESEARCH_CASCADE_METHOD.md",
    "config/NOVEL_DEVELOPMENT_LINEAGE_EXCLUSIONS.json",
    "automation/validate-novel-vulnerability-frontier.py",
    "automation/test-novel-vulnerability-frontier.py",
    "config/NOVEL_FRONTIER_REGRESSION_CASES.json",
    "skill/autonomous-research-cascade-engine/SKILL.md",
    "skill/autonomous-research-cascade-engine/agents/openai.yaml",
    "references/MICRO_INSPIRATION_RESEARCH_METHOD.md",
    "references/GENERIC_ANOMALY_EVALUATION_METHOD.md",
    "references/CLEAN_PROBE_REASONING_METHOD.md",
    "references/DISCOVERY_CASCADE_METHOD.md",
    "references/SHARED_SEMANTIC_REUSE_METHOD.md",
    "references/HARNESS_FALSIFICATION_METHOD.md",
    "automation/validate-autonomous-research-cascade.py",
    "automation/test-autonomous-research-cascade.py",
    "config/AUTONOMOUS_RESEARCH_CASCADE_CASES.json",
    "skill/dynamic-filter-evaluator-rce-hunter/SKILL.md",
    "skill/dynamic-filter-evaluator-rce-hunter/agents/openai.yaml",
    "skill/dynamic-filter-evaluator-rce-hunter/references/dynamic-filter-evaluator-rce-method.md",
    "skill/cross-language-script-injection-hunter/SKILL.md",
    "skill/cross-language-script-injection-hunter/agents/openai.yaml",
    "skill/cross-language-script-injection-hunter/references/cross-language-script-injection-rce-method.md",
    "skill/llm-tokenization-boundary-hunter/SKILL.md",
    "skill/llm-tokenization-boundary-hunter/agents/openai.yaml",
    "skill/llm-tokenization-boundary-hunter/references/repeated-token-llm-security-method.md",
    "skill/credential-exposure-capability-hunter/SKILL.md",
    "skill/credential-exposure-capability-hunter/agents/openai.yaml",
    "skill/credential-exposure-capability-hunter/references/credential-exposure-capability-method.md",
    "skill/native-js-binding-lifetime-hunter/SKILL.md",
    "skill/native-js-binding-lifetime-hunter/agents/openai.yaml",
    "skill/native-js-binding-lifetime-hunter/references/native-js-binding-lifetime-uaf-method.md",
    "prompts/MASTER_PROMPT_NATIVE_JS_BINDING_LIFETIME.md",
    "skill/github-actions-fork-trust-hunter/SKILL.md",
    "skill/github-actions-fork-trust-hunter/agents/openai.yaml",
    "skill/github-actions-fork-trust-hunter/references/github-actions-fork-trust-method.md",
    "prompts/MASTER_PROMPT_GITHUB_ACTIONS_FORK_TRUST.md",
    "skill/deadlock-lock-graph-dos-hunter/SKILL.md",
    "skill/deadlock-lock-graph-dos-hunter/agents/openai.yaml",
    "skill/deadlock-lock-graph-dos-hunter/references/deadlock-lock-graph-dos-method.md",
    "prompts/MASTER_PROMPT_DEADLOCK_LOCK_GRAPH_DOS.md",
    "skill/compositional-exploit-chain-hunter/references/wordpress-xss2shell-seven-boundary-method.md",
    "references/CROSS_BOUNDARY_COMPOSITION_METHOD.md",
    "skill/exploit-chain-research-orchestrator/SKILL.md",
    "skill/exploit-chain-research-orchestrator/agents/openai.yaml",
    *xchain_companions,
    *v8_chain_prompts,
]:
    if not (ROOT / required).is_file():
        errors.append(f"missing required bootstrap artifact: {required}")

try:
    xchain_text = (ROOT / "skill" / xchain_skill / "SKILL.md").read_text(encoding="utf-8")
    normalized_xchain = " ".join(xchain_text.split()).lower()
    for required_phrase in (
        "kill_no_capability_delta",
        "attacker_state_registry",
        "primitive_registry",
        "chain_graph",
        "failed_assumption_registry",
        "exploit_attempt_registry",
        "primitive_valid=yes",
        "chain_edge_valid=yes",
        "fail_representation",
        "retry_blocked_no_new_evidence",
        "xchain-lab-v1",
    ):
        if required_phrase not in normalized_xchain:
            errors.append(f"exploit-chain research skill missing contract: {required_phrase}")
    for schema_name in (
        "ATTACKER_STATE_SCHEMA.json",
        "PRIMITIVE_SCHEMA.json",
        "CHAIN_GRAPH_SCHEMA.json",
    ):
        schema = json.loads((ROOT / "skill" / xchain_skill / "config" / schema_name).read_text(encoding="utf-8"))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"XCHAIN schema has wrong dialect: {schema_name}")
    for prompt_rel in v8_chain_prompts:
        prompt_text = (ROOT / prompt_rel).read_text(encoding="utf-8").lower()
        for required_phrase in ("primitive=", "post_exploit_capability=", "next_question="):
            if required_phrase not in prompt_text:
                errors.append(f"V8 chain-role prompt {prompt_rel} missing: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate exploit-chain research package: {exc}")

try:
    selector_text = (ROOT / "automation" / "route-security-task.py").read_text(encoding="utf-8")
    for required_flag in ("--target", "--scope", "--scope-file", "--observed"):
        if required_flag not in selector_text:
            errors.append(f"target/scope router is missing required input: {required_flag}")
    for required_state in ("ACTIVE", "DEFERRED", "NOT_APPLICABLE"):
        if required_state not in selector_text:
            errors.append(f"target/scope router is missing state: {required_state}")
except Exception as exc:
    errors.append(f"cannot validate target/scope router: {exc}")

methodology_rel = "references/BUGBOUNTY_INFO_ATTACK_SURFACE_CHAIN_TOOLING_METHOD.md"
methodology_route = data.get("artifact_routes", {}).get(methodology_rel, {})
if methodology_route.get("mode") != "always":
    errors.append("attack-surface/chain/tooling methodology must be always active")
router_companions = data.get("skill_routes", {}).get("mandatory-auto-router", {}).get("companions", [])
if methodology_rel not in router_companions:
    errors.append("mandatory router does not load attack-surface/chain/tooling methodology")
try:
    methodology_text = (ROOT / methodology_rel).read_text(encoding="utf-8")
    normalized_methodology = " ".join(methodology_text.split())
    for required_phrase in (
        "Attack-surface map",
        "Primitive-to-chain method",
        "Tool selection discipline",
        "KILL rules",
        "MANUALLY_CONFIRMED",
        "Tool execution is never automatic",
    ):
        if required_phrase not in normalized_methodology:
            errors.append(f"methodology missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate attack-surface/chain/tooling methodology: {exc}")

impact_skill = "program-impact-boundary-gate"
impact_route = data.get("skill_routes", {}).get(impact_skill, {})
impact_method = "references/PROGRAM_IMPACT_BOUNDARY_GATE.md"
impact_prompt = "prompts/MASTER_PROMPT_PROGRAM_IMPACT_BOUNDARY_GATE.md"
impact_cases = "config/PROGRAM_IMPACT_NEGATIVE_CONTROL_CASES.json"
impact_positive_cases = "config/PROGRAM_IMPACT_POSITIVE_CONTROL_CASES.json"
if impact_route.get("mode") != "always":
    errors.append("program impact boundary gate must be always active")
for companion in (impact_method, impact_prompt, impact_cases, impact_positive_cases):
    if companion not in impact_route.get("companions", []):
        errors.append(f"program impact route is missing companion: {companion}")
try:
    impact_text = (ROOT / impact_method).read_text(encoding="utf-8")
    normalized_impact = " ".join(impact_text.split()).lower()
    for required_phrase in (
        "starting capability -> exploit transition -> resulting capability",
        "program-impact card",
        "equivalent path",
        "severity floor",
        "negative controls",
        "similarity creates a falsification obligation",
        "authoritative read-back",
        "production product versus demo",
        "program impact ceiling",
        "defense-in-depth hygiene",
        "kill_known_or_duplicate",
        "kill_no_production_reachability",
        "attacker-controlled timing",
        "lifecycle contract",
        "promised security property",
        "collision feasibility",
        "counterfactual defense",
        "control plane",
        "authorization issuance time",
        "derived credential lineage",
        "temporal trust equivalence",
        "protected consumer",
        "environmental mismatch",
        "procedural inactivity",
        "production stack equivalence",
        "canonical consensus",
        "top-level navigation",
        "submission-time",
        "privacy promise",
        "report readiness",
        "validated positive-control patterns",
        "low-privilege owned data",
        "downstream consumer",
        "public and fixed",
    ):
        if required_phrase.lower() not in normalized_impact:
            errors.append(f"program impact method missing required contract: {required_phrase}")
    impact_data = json.loads((ROOT / impact_cases).read_text(encoding="utf-8"))
    if len(impact_data.get("cases", [])) != 72:
        errors.append("program impact negative-control corpus must contain 72 cases")
    impact_positive_data = json.loads((ROOT / impact_positive_cases).read_text(encoding="utf-8"))
    if len(impact_positive_data.get("cases", [])) != 2:
        errors.append("program impact positive-control corpus must contain 2 cases")
    positive_ids = {str(case.get("report_id")) for case in impact_positive_data.get("cases", [])}
    if positive_ids != {"3931777", "3931771"}:
        errors.append(f"program impact positive-control IDs mismatch: {sorted(positive_ids)}")
except Exception as exc:
    errors.append(f"cannot validate program impact boundary gate: {exc}")

system_impact_prompt = "prompts/SYSTEM_PROMPT_AUTHORIZED_OFFENSIVE_IMPACT_GATE.md"
system_impact_route = data.get("artifact_routes", {}).get(system_impact_prompt, {})
if system_impact_route.get("mode") != "always":
    errors.append("authorized offensive impact system prompt must be always active")
for core_skill in ("mandatory-auto-router", "authorized-security-autopilot"):
    if system_impact_prompt not in data.get("skill_routes", {}).get(core_skill, {}).get("companions", []):
        errors.append(f"{core_skill} must load the authorized offensive impact system prompt")
try:
    system_impact_text = (ROOT / system_impact_prompt).read_text(encoding="utf-8").lower()
    for required_phrase in (
        "kill_known_or_duplicate",
        "synthetic application",
        "dependency updater",
        "unusual application lifecycle",
        "exotic compiler/platform combinations",
        "transport mode",
        "strong + manually_confirmed",
        "low-privilege data",
        "downstream filesystem",
        "public resolved roots",
        "counterfactual-methodology-synthesizer",
        "at most two cycles",
        "method_generated_no_valid_finding",
    ):
        if required_phrase not in system_impact_text:
            errors.append(f"authorized offensive impact system prompt missing: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate authorized offensive impact system prompt: {exc}")

counterfactual_skill = "counterfactual-methodology-synthesizer"
counterfactual_route = data.get("skill_routes", {}).get(counterfactual_skill, {})
counterfactual_companions = (
    "prompts/MASTER_PROMPT_COUNTERFACTUAL_METHODOLOGY_SYNTHESIS.md",
    "references/COUNTERFACTUAL_METHODOLOGY_SYNTHESIS_METHOD.md",
    "config/COUNTERFACTUAL_METHODOLOGY_REGRESSION_CASES.json",
    "automation/validate-counterfactual-methodology.py",
    "automation/test-counterfactual-methodology.py",
)
if counterfactual_route.get("mode") != "conditional":
    errors.append("counterfactual methodology synthesizer must be conditional")
for trigger in (
    "no valid finding",
    "new methodology",
    "counterfactual methodology",
    "what if",
    "bagaimana jika",
    "ganti ini menjadi",
):
    if trigger not in counterfactual_route.get("triggers", []):
        errors.append(f"counterfactual methodology route missing trigger: {trigger}")
for companion in counterfactual_companions:
    if companion not in counterfactual_route.get("companions", []):
        errors.append(f"counterfactual methodology route missing companion: {companion}")
    artifact_route = data.get("artifact_routes", {}).get(companion, {})
    if artifact_route.get("mode") != "conditional":
        errors.append(f"counterfactual methodology artifact must be conditional: {companion}")
try:
    counterfactual_text = (ROOT / "references" / "COUNTERFACTUAL_METHODOLOGY_SYNTHESIS_METHOD.md").read_text(encoding="utf-8")
    normalized_counterfactual = " ".join(counterfactual_text.split()).lower()
    for required_phrase in (
        "counterfactual_methodology_synthesis:v1",
        "what if a becomes b",
        "prior_method_exclusion_digest",
        "mutation_only",
        "two post-`no valid finding` cycles",
        "valid_finding_generated",
        "strong + manually_confirmed",
        "do not prove generalization",
    ):
        if required_phrase not in normalized_counterfactual:
            errors.append(f"counterfactual methodology missing required contract: {required_phrase}")
    counterfactual_cases = json.loads((ROOT / "config" / "COUNTERFACTUAL_METHODOLOGY_REGRESSION_CASES.json").read_text(encoding="utf-8"))
    if len(counterfactual_cases.get("cases", [])) != 14:
        errors.append("counterfactual methodology corpus must contain 14 cases")
    if counterfactual_cases.get("limits") != {
        "max_cycles": 2,
        "max_method_cards_per_cycle": 3,
        "min_fact_anchors": 2,
    }:
        errors.append("counterfactual methodology limits are invalid")
except Exception as exc:
    errors.append(f"cannot validate counterfactual methodology: {exc}")

novel_skill = "novel-vulnerability-hypothesis-engine"
novel_route = data.get("skill_routes", {}).get(novel_skill, {})
novel_method = "references/NOVEL_INVARIANT_FRONTIER_METHOD.md"
novel_state_method = "references/STATE_MACHINE_SECURITY_METHOD.md"
novel_differential_method = "references/METAMORPHIC_DIFFERENTIAL_METHOD.md"
novel_resource_method = "references/RESOURCE_AMPLIFICATION_METHOD.md"
novel_composition_method = "references/CROSS_FEATURE_COMPOSITION_METHOD.md"
novel_evaluation_method = "references/EVALUATION_FIRST_RESEARCH_CASCADE_METHOD.md"
novel_prompt = "prompts/MASTER_PROMPT_NOVEL_INVARIANT_FRONTIER.md"
novel_validator = "automation/validate-novel-vulnerability-frontier.py"
if novel_route.get("mode") != "always":
    errors.append("novel vulnerability hypothesis engine must be always active")
for companion in (
    novel_method,
    novel_state_method,
    novel_differential_method,
    novel_resource_method,
    novel_composition_method,
    novel_evaluation_method,
    novel_prompt,
    novel_validator,
    "config/CODEX_CLI_CANDIDATE_SCHEMA.json",
):
    if companion not in novel_route.get("companions", []):
        errors.append(f"novel vulnerability hypothesis route is missing companion: {companion}")
try:
    novel_text = (ROOT / novel_method).read_text(encoding="utf-8")
    normalized_novel = " ".join(novel_text.split())
    for required_phrase in (
        "NOVEL_DISCOVERY_MODE=true",
        "The embargo opens only",
        "complete source-to-sink path",
        "harmless runtime effect",
        "target-derived negative control",
        "novelty_status=UNVERIFIED",
        "zero-day",
        "Generalization boundary",
    ):
        if required_phrase.lower() not in normalized_novel.lower():
            errors.append(f"novel invariant method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate novel invariant frontier methodology: {exc}")

try:
    evaluation_text = (ROOT / novel_evaluation_method).read_text(encoding="utf-8")
    normalized_evaluation = " ".join(evaluation_text.split())
    for required_phrase in (
        "Design evaluation before ideation",
        "The deterministic evaluator must record",
        "target_answer_leakage=false",
        "Never disguise a real target as a simulator",
        "Preserve benchmark integrity",
    ):
        if required_phrase.lower() not in normalized_evaluation.lower():
            errors.append(f"evaluation-first cascade method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate evaluation-first cascade methodology: {exc}")

for always_novel_artifact in (
    novel_prompt,
    novel_method,
    novel_state_method,
    novel_differential_method,
    novel_resource_method,
    novel_composition_method,
    novel_evaluation_method,
    novel_validator,
):
    if data.get("artifact_routes", {}).get(always_novel_artifact, {}).get("mode") != "always":
        errors.append(f"novel frontier artifact must be always active: {always_novel_artifact}")
for novel_regression in (
    "automation/test-novel-vulnerability-frontier.py",
    "config/NOVEL_FRONTIER_REGRESSION_CASES.json",
):
    if data.get("artifact_routes", {}).get(novel_regression, {}).get("mode") != "conditional":
        errors.append(f"novel frontier regression artifact must be conditional: {novel_regression}")

cascade_skill = "autonomous-research-cascade-engine"
cascade_route = data.get("skill_routes", {}).get(cascade_skill, {})
cascade_methods = (
    "references/MICRO_INSPIRATION_RESEARCH_METHOD.md",
    "references/GENERIC_ANOMALY_EVALUATION_METHOD.md",
    "references/CLEAN_PROBE_REASONING_METHOD.md",
    "references/DISCOVERY_CASCADE_METHOD.md",
    "references/SHARED_SEMANTIC_REUSE_METHOD.md",
    "references/HARNESS_FALSIFICATION_METHOD.md",
)
cascade_validator = "automation/validate-autonomous-research-cascade.py"
if cascade_route.get("mode") != "always":
    errors.append("autonomous research cascade engine must be always active")
for companion in (*cascade_methods, novel_evaluation_method, cascade_validator, "config/CODEX_CLI_CANDIDATE_SCHEMA.json"):
    if companion not in cascade_route.get("companions", []):
        errors.append(f"autonomous research cascade route is missing companion: {companion}")
for artifact in (*cascade_methods, cascade_validator):
    if data.get("artifact_routes", {}).get(artifact, {}).get("mode") != "always":
        errors.append(f"autonomous research cascade artifact must be always active: {artifact}")
for artifact in (
    "automation/test-autonomous-research-cascade.py",
    "config/AUTONOMOUS_RESEARCH_CASCADE_CASES.json",
):
    if data.get("artifact_routes", {}).get(artifact, {}).get("mode") != "conditional":
        errors.append(f"autonomous research cascade regression must be conditional: {artifact}")
try:
    cascade_skill_text = (ROOT / "skill" / cascade_skill / "SKILL.md").read_text(encoding="utf-8")
    normalized_cascade_skill = " ".join(cascade_skill_text.split())
    for required_phrase in (
        "OBJECTIVE_COMPILER",
        "MICRO_INSPIRATION_ENGINE",
        "HYPOTHESIS_FACTORY",
        "GENERIC_EVALUATOR",
        "CLEAN_PROBE_CLASSIFIER",
        "PERMUTATION_SYNTHESIZER",
        "ANOMALY_LEDGER",
        "EXPLANATION_ENGINE",
        "DISCOVERY_CASCADE",
        "SHARED_SEMANTIC_REUSE",
        "HARNESS_SELF_AUDITOR",
        "DETERMINISTIC_VERDICT_GATE",
        "HUMAN_AMPLIFIER_GATE",
        "TARGET_SWITCHING=FORBIDDEN",
        "SCOPE_MUST_BE_EXPLICIT=true",
        "SAFETY_SIGNAL_MASKING=FORBIDDEN",
        "AGENT_REALITY_DECEPTION=FORBIDDEN",
        "CREDENTIAL_COLLECTION=FORBIDDEN",
        "DESTRUCTIVE_PROOF=FORBIDDEN",
        "HIGH_VOLUME_DOS=FORBIDDEN",
        "EARLY_EXIT_ON_MINIMUM_PROOF=true",
        "CASCADE_LEAD",
    ):
        if required_phrase not in normalized_cascade_skill:
            errors.append(f"autonomous research cascade skill missing contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate autonomous research cascade skill: {exc}")

cascade_reference_contracts = {
    "references/MICRO_INSPIRATION_RESEARCH_METHOD.md": (
        "one to three sentences", "Every hypothesis requires a falsifier", "context as an experimental variable",
    ),
    "references/GENERIC_ANOMALY_EVALUATION_METHOD.md": (
        "baseline satisfies I", "ANOMALY", "Prevent evaluator gaming",
    ),
    "references/CLEAN_PROBE_REASONING_METHOD.md": (
        "CLEAN", "DIRTY", "UNKNOWN", "Synthesize target-derived permutations",
    ),
    "references/DISCOVERY_CASCADE_METHOD.md": (
        "Ask the two cascade questions", "CASCADE_LEAD", "cannot inherit",
    ),
    "references/SHARED_SEMANTIC_REUSE_METHOD.md": (
        "shared component -> domain A consumers -> domain B consumers", "domain-specific rules", "safe sibling",
    ),
    "references/HARNESS_FALSIFICATION_METHOD.md": (
        "TARGET_CONFIRMED", "HARNESS_CONFIRMED", "Require independent reproduction", "deterministic verdict gates",
    ),
}
for rel, phrases in cascade_reference_contracts.items():
    try:
        normalized = " ".join((ROOT / rel).read_text(encoding="utf-8").split())
        for phrase in phrases:
            if phrase.lower() not in normalized.lower():
                errors.append(f"autonomous research cascade method {rel} missing contract: {phrase}")
    except Exception as exc:
        errors.append(f"cannot validate autonomous research cascade method {rel}: {exc}")

lineage_exclusions = "config/NOVEL_DEVELOPMENT_LINEAGE_EXCLUSIONS.json"
if data.get("artifact_routes", {}).get(lineage_exclusions, {}).get("mode") != "conditional":
    errors.append("development-lineage exclusions must be curator-only conditional data")
try:
    lineage_data = json.loads((ROOT / lineage_exclusions).read_text(encoding="utf-8"))
    if lineage_data.get("package_version") != version:
        errors.append("development-lineage exclusion package version mismatch")
    if lineage_data.get("auditor_auto_load") is not False:
        errors.append("development-lineage exclusions must not auto-load for blind auditors")
except Exception as exc:
    errors.append(f"invalid development-lineage exclusion config: {exc}")

try:
    dynamic_method_text = (ROOT / dynamic_filter_method).read_text(encoding="utf-8")
    normalized_dynamic_method = " ".join(dynamic_method_text.split())
    for required_phrase in (
        "control/data confusion",
        "GHSA-ccv5-c45x-2q38",
        "CVE-2026-11892",
        "100.3.0",
        "deterministic non-empty",
        "Do not begin with shell commands",
        "typed replacement",
        "KILL rules",
    ):
        if required_phrase not in normalized_dynamic_method:
            errors.append(f"dynamic-filter evaluator method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate dynamic-filter evaluator methodology: {exc}")

try:
    cross_runtime_text = (ROOT / cross_runtime_method).read_text(encoding="utf-8")
    normalized_cross_runtime = " ".join(cross_runtime_text.split())
    for required_phrase in (
        "cross-language code generation",
        "GHSA-r27j-xxgx-f5vr",
        "CVE-2026-41512",
        "1.4.1",
        "URL validation is not JavaScript string encoding",
        "backslashes before quotes",
        "Do not begin with shell commands",
        "typed data channel",
        "KILL rules",
    ):
        if required_phrase not in normalized_cross_runtime:
            errors.append(f"cross-language script injection method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate cross-language script injection methodology: {exc}")

try:
    llm_token_text = (ROOT / llm_token_method).read_text(encoding="utf-8")
    normalized_llm_token = " ".join(llm_token_text.split())
    for required_phrase in (
        "experimental research code",
        "d5cd5615de671f2461ce542669aec0e9a881b00a",
        "arXiv:2311.17035",
        "token-budget-matched",
        "one `user` message",
        "Do not run a live experiment",
        "sole judge",
        "protected-boundary",
        "KILL rules",
    ):
        if required_phrase not in normalized_llm_token:
            errors.append(f"LLM tokenization boundary method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate LLM tokenization boundary methodology: {exc}")

try:
    credential_text = (ROOT / credential_method).read_text(encoding="utf-8")
    normalized_credential = " ".join(credential_text.split())
    for required_phrase in (
        "Jira Credential Disclosure within Mozilla Slack",
        "HackerOne #2137154",
        "Mozilla Mastodon Staging Instance Admin API Key Disclosure Through Slack",
        "admin:read:accounts",
        "admin:write:accounts",
        "PII_EXPOSED_STOP",
        "Will be included",
        "staging is not production",
        "one successful read endpoint does not prove",
        "scope exception",
        "A payout is not scope precedent",
        "Mozilla Common Voice container image",
        "Netlify Authentication Token Exposed in Public Mozilla CI Logs",
        "no stable HackerOne report ID was independently identified",
        "Taskcluster live.log",
        "role: Developer",
        "site_access: selected",
        "selected_access_site_ids",
        "roles_allowed",
        "function-list request",
        "Netlify-managed function runtime",
        "not automatically RCE on",
        "crash-pings.mozilla.org",
        "content/configuration integrity",
        "PUBLIC / FIXED / DUPLICATE",
        "two AWS access-key pairs",
        "database credentials",
        "immutable digest",
        "multi-platform",
        "lower layer",
        "No observed use",
        "image deletion",
        "credential rotation",
        "AWS user removal",
        "Never store the raw credential",
        "Do not authenticate with a disclosed credential",
        "effective permissions",
        "revocation",
        "residual copies",
        "E0",
        "E6",
        "KILL rules",
    ):
        if required_phrase not in normalized_credential:
            errors.append(f"credential exposure capability method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate credential exposure capability methodology: {exc}")

try:
    native_lifetime_text = (ROOT / native_lifetime_method).read_text(encoding="utf-8")
    normalized_native_lifetime = " ".join(native_lifetime_text.split())
    for required_phrase in (
        "JavaScript-reachable callable",
        "base::Unretained",
        "property descriptors",
        "allocation, free, and use stacks",
        "No stable HackerOne report ID was provided",
        "Brave Wallet",
        "Extensions (wallet fallback)",
        "PR #18411",
        "a8e497b",
        "renderer code execution",
        "KILL rules",
    ):
        if required_phrase not in normalized_native_lifetime:
            errors.append(f"native JavaScript binding lifetime method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate native JavaScript binding lifetime methodology: {exc}")

try:
    github_actions_fork_text = (ROOT / github_actions_fork_method).read_text(encoding="utf-8")
    normalized_github_actions_fork = " ".join(github_actions_fork_text.split())
    for required_phrase in (
        "step-scoped",
        "actions/checkout@v5",
        "persist-credentials",
        ".git/config",
        "No stable HackerOne report ID was provided",
        "PR #5002",
        "defense in depth",
        "trusted base-repository",
        "requested permissions",
        "PRIVACY_CONFIG_PAT",
        "HackerOne #3619287",
        "content-scope-scripts",
        "b5066fbcf6",
        "eb01151209",
        "same-job workspace",
        "ANTHROPIC_API_KEY",
        "callback contained no secret proof",
        "merged == true",
        "label authority alone",
        "G0",
        "G6",
        "KILL rules",
    ):
        if required_phrase not in normalized_github_actions_fork:
            errors.append(f"GitHub Actions fork trust method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate GitHub Actions fork trust methodology: {exc}")

try:
    deadlock_text = (ROOT / deadlock_method).read_text(encoding="utf-8")
    normalized_deadlock = " ".join(deadlock_text.split())
    for required_phrase in (
        "HackerOne #3307874",
        "179c924",
        "36b12ed",
        "b591866",
        "2d19722",
        "v0.18.4.3",
        "STACK_TRACE",
        "50 threads",
        "batch size 500",
        "One request",
        "only Linux",
        "release binaries",
        "Database corruption",
        "confidentiality",
        "Medium",
        "5 XMR",
        "wait-for graph",
        "circular wait",
        "D0",
        "D7",
        "KILL",
    ):
        if required_phrase not in normalized_deadlock:
            errors.append(f"deadlock lock-graph method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate deadlock lock-graph methodology: {exc}")

try:
    xss2shell_text = (ROOT / xss2shell_method).read_text(encoding="utf-8")
    normalized_xss2shell = " ".join(xss2shell_text.split())
    for required_phrase in (
        "CVE-2026-64638",
        "GHSA-52p2-r8wf-jcrf",
        "PUBLIC / FIXED / DUPLICATE",
        "High 8.9",
        "active user interaction",
        "Do not call this a zero-click or purely unauthenticated RCE",
        "Seven-boundary evidence ledger",
        "Application Passwords",
        "_method",
        "_envelope",
        "_jsonp",
        "direct PHP execution",
        "W0",
        "W7",
        "Detection and forensic correlation",
        "WP2Shell",
        "KILL",
    ):
        if required_phrase not in normalized_xss2shell:
            errors.append(f"XSS2Shell seven-boundary method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate XSS2Shell seven-boundary methodology: {exc}")

try:
    schema = json.loads((ROOT / "config" / "CODEX_CLI_CANDIDATE_SCHEMA.json").read_text(encoding="utf-8"))
    for required_field in (
        "attacker_condition", "server_condition", "security_impact", "source_trace",
        "authorization_kill_challenge", "consumer_boundary_challenge",
        "execution_consumer_challenge", "archive_renderer_framework_challenge",
        "reparse_config_provenance_challenge", "path_cli_gadget_chain_challenge",
        "derivation_origin", "research_cascade", "security_invariant",
        "attacker_control", "trust_boundary", "equivalent_paths_compared",
        "state_sequence", "representation_changes", "resource_amplification",
        "assumption_under_test", "counterfactuals_tested", "consumer_identity",
        "composition_candidates", "negative_controls", "runtime_proof",
        "production_reachability", "prior_art_embargo_respected",
        "prior_art_checked_after_proof", "novelty_status", "prior_art", "verdict",
        "manual_status", "research_objective", "micro_inspiration_id",
        "micro_inspiration_scope", "known_attack_terms_withheld", "hypothesis",
        "falsifier", "probe_cleanliness", "probe_semantic_proof",
        "evaluation_primitive", "baseline_fingerprint", "anomaly_fingerprint",
        "harness_independent_reproduction", "independent_runners",
        "anomaly_origin", "shared_semantic_domains", "counterfactuals",
        "composition_paths", "cascade_parent", "observation_parent",
        "invariant_parent", "cascade_depth", "second_order_questions",
        "derived_detection_strategy", "deterministic_validator",
        "authoritative_readback", "authorized_scope", "impact_ceiling",
        "cleanup_status", "research_path_id", "discovery_wave",
        "root_cause_family", "primitive_chain", "implementation_escalation",
    ):
        if required_field not in schema.get("required", []):
            errors.append(f"Codex CLI candidate schema missing required field: {required_field}")
    if schema.get("$id") != "urn:codex-cli-security-audit:candidate:v10":
        errors.append("Codex CLI candidate schema must use the v10 identifier")
    if len(schema.get("required", [])) != 79:
        errors.append("Codex CLI candidate schema must require 79 top-level fields")
    if schema.get("properties", {}).get("derivation_origin", {}).get("const") != "TARGET_NATIVE":
        errors.append("Codex CLI candidate schema must require TARGET_NATIVE derivation")
    stage_enum = schema.get("properties", {}).get("stage", {}).get("enum", [])
    if "CASCADE_LEAD" not in stage_enum:
        errors.append("Codex CLI candidate schema must support CASCADE_LEAD")
except Exception as exc:
    errors.append(f"invalid Codex CLI candidate schema: {exc}")

try:
    registry_schema = json.loads(
        (ROOT / "config" / "CODEX_CLI_RESEARCH_PATH_REGISTRY_SCHEMA.json").read_text(encoding="utf-8")
    )
    if registry_schema.get("$id") != "urn:codex-cli-security-audit:research-path-registry:v11":
        errors.append("research-path registry schema must use the v11 identifier")
    required_registry_fields = {
        "audit_id", "package_version", "paths", "waves", "coverage_analysis",
        "convergence_checks", "adaptive_execution", "termination",
    }
    if not required_registry_fields.issubset(set(registry_schema.get("required", []))):
        errors.append("research-path registry schema is missing required top-level fields")
    path_properties = (
        registry_schema.get("properties", {}).get("paths", {}).get("items", {}).get("properties", {})
    )
    statuses = set(path_properties.get("status", {}).get("enum", []))
    if statuses != {"ACTIVE", "PROMISING", "BLOCKED", "EXHAUSTED", "KILLED", "VALIDATED"}:
        errors.append("research-path registry status enum is incomplete")
    specialist_cap = (
        registry_schema.get("properties", {}).get("waves", {}).get("items", {})
        .get("properties", {}).get("specialists", {}).get("maxItems")
    )
    if specialist_cap != 3:
        errors.append("adaptive research wave must cap specialists at three")
except Exception as exc:
    errors.append(f"invalid research-path registry schema: {exc}")

try:
    execution_schema = json.loads(
        (ROOT / "config" / "CODEX_CLI_ADAPTIVE_EXECUTION_PROVENANCE_SCHEMA.json")
        .read_text(encoding="utf-8")
    )
    if execution_schema.get("$id") != "urn:codex-cli-security-audit:adaptive-execution-provenance:v11":
        errors.append("adaptive execution provenance schema must use the v11 identifier")
    required_execution_fields = {
        "adaptive_triggered", "spawn_attempts", "spawn_successes",
        "spawn_failures", "unique_specialist_ids", "separate_specialist_input",
        "separate_specialist_output", "root_consumed_specialist_output",
        "specialists", "adaptive_execution_proven",
    }
    if not required_execution_fields.issubset(set(execution_schema.get("required", []))):
        errors.append("adaptive execution provenance schema is missing required fields")
except Exception as exc:
    errors.append(f"invalid adaptive execution provenance schema: {exc}")

try:
    adaptive_method = " ".join(
        (ROOT / "references" / "ADAPTIVE_RESEARCH_PATH_ORCHESTRATION_METHOD.md")
        .read_text(encoding="utf-8").split()
    ).lower()
    for phrase in (
        "research-path registry",
        "do not assign discovery capacity",
        "agreement does not change proof quality",
        "zero to three",
        "primitive-to-impact chaining",
        "exact implementation escalation",
        "execution-plane proof",
        "specialist_result_token",
        "adaptive_execution_proven",
        "termination rule",
    ):
        if phrase not in adaptive_method:
            errors.append(f"adaptive orchestration method missing contract: {phrase}")
except Exception as exc:
    errors.append(f"cannot validate adaptive orchestration method: {exc}")

for policy_key, expected in (
    ("research_path_registry_required_for_multi_agent", True),
    ("anti_convergence_required_for_multi_agent", True),
    ("adaptive_specialist_cap_per_wave", 3),
    ("primitive_to_impact_chain_required", True),
    ("exact_implementation_binding_when_material", True),
    ("evidence_based_termination_required", True),
):
    if data.get("policy", {}).get(policy_key) != expected:
        errors.append(f"routing policy missing adaptive orchestration contract: {policy_key}")

auth_kill_method = "references/AUTHORIZATION_INVARIANT_KILL_CHALLENGE.md"
auth_kill_route = data.get("artifact_routes", {}).get(auth_kill_method, {})
if auth_kill_route.get("mode") != "always":
    errors.append("authorization invariant KILL challenge must be always active")
for owner in (
    "mandatory-auto-router",
    "bug-bounty-triage",
    "expert-authentication-authorization-hunter",
    "expert-source-code-bug-hunter",
    "expert-web-api-business-logic-hunter",
    "secure-code-reviewer",
):
    if auth_kill_method not in data.get("skill_routes", {}).get(owner, {}).get("companions", []):
        errors.append(f"authorization KILL challenge is not a companion of {owner}")
try:
    auth_kill_text = (ROOT / auth_kill_method).read_text(encoding="utf-8")
    normalized_auth_kill = " ".join(auth_kill_text.split())
    for required_phrase in (
        "protected operation",
        "absent / omitted",
        "nil / null",
        "explicit success-returning no-op",
        "implicit fallback to success/no-op",
        "Resource A",
        "Resource B",
        "Mandatory KILL challenge",
        "NEEDS_INVARIANT_PROOF",
        "AUTHORIZATION_KILL_CHALLENGE:v1",
    ):
        if required_phrase not in normalized_auth_kill:
            errors.append(f"authorization invariant method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate authorization invariant methodology: {exc}")

consumer_method = "references/PATCH_VARIANT_CONSUMER_BOUNDARY_METHOD.md"
consumer_route = data.get("artifact_routes", {}).get(consumer_method, {})
if consumer_route.get("mode") != "conditional":
    errors.append("patch-variant consumer-boundary method must be conditional")
for owner in (
    "api-security-reviewer",
    "compositional-exploit-chain-hunter",
    "expert-cache-proxy-parser-differential-hunter",
    "expert-source-code-bug-hunter",
    "expert-web-api-business-logic-hunter",
    "patch-diff-root-cause-analyzer",
    "secure-code-reviewer",
    "wallet-node-bridge-reviewer",
):
    if consumer_method not in data.get("skill_routes", {}).get(owner, {}).get("companions", []):
        errors.append(f"consumer-boundary method is not a companion of {owner}")
for skill, triggers in {
    "compositional-exploit-chain-hunter": (
        "selector consumer mismatch",
        "repository import local transport",
        "consensus error to chain halt",
    ),
    "expert-cache-proxy-parser-differential-hunter": (
        "validated node differs from consumed node",
        "url scheme allowlist",
        "repository import file scheme",
    ),
    "patch-diff-root-cause-analyzer": (
        "patch variant",
        "incomplete guard",
        "error domain",
    ),
    "wallet-node-bridge-reviewer": (
        "cosmos sdk",
        "endblocker",
        "finalizeblock",
        "group weights",
        "chain halt",
    ),
}.items():
    available = data.get("skill_routes", {}).get(skill, {}).get("triggers", [])
    for trigger in triggers:
        if trigger not in available:
            errors.append(f"{skill} route is missing consumer-boundary trigger: {trigger}")
try:
    consumer_text = (ROOT / consumer_method).read_text(encoding="utf-8")
    normalized_consumer = " ".join(consumer_text.split())
    for required_phrase in (
        "PATCH_VARIANT_CONSUMER_BOUNDARY:v1",
        "Patch-variant failure-domain sweep",
        "eligible value versus consumed value",
        "Validator versus protocol consumer",
        "HackerOne report `#3018307`",
        "GHSA-47ww-ff84-4jrg",
        "GHSA-x5vx-95h7-rv4p",
        "HackerOne report `#1731349`",
        "CVE-2023-0050",
        "HackerOne report `#1685822`",
        "GitLab BulkImports",
        "NEEDS_CONSUMER_PROOF",
        "STRONG + MANUALLY_CONFIRMED",
        "Never test denial of service on public nodes or mainnet",
    ):
        if required_phrase.lower() not in normalized_consumer.lower():
            errors.append(f"patch-variant consumer-boundary method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate patch-variant consumer-boundary methodology: {exc}")

for consumer_regression in (
    "automation/test-patch-variant-consumer-boundary.py",
    "config/PATCH_VARIANT_CONSUMER_BOUNDARY_REGRESSION_CASES.json",
):
    route = data.get("artifact_routes", {}).get(consumer_regression, {})
    if route.get("mode") != "conditional":
        errors.append(f"consumer-boundary regression artifact must be conditional: {consumer_regression}")

execution_method = "references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md"
execution_route = data.get("artifact_routes", {}).get(execution_method, {})
if execution_route.get("mode") != "conditional":
    errors.append("dynamic-data execution-consumer method must be conditional")
for owner in (
    "api-security-reviewer",
    "compositional-exploit-chain-hunter",
    "cross-language-script-injection-hunter",
    "expert-authentication-authorization-hunter",
    "expert-cache-proxy-parser-differential-hunter",
    "expert-php-ruby-engineer",
    "expert-source-code-bug-hunter",
    "expert-web-api-business-logic-hunter",
    "modern-rce-chain-hunter",
    "patch-diff-root-cause-analyzer",
    "secure-code-reviewer",
):
    if execution_method not in data.get("skill_routes", {}).get(owner, {}).get("companions", []):
        errors.append(f"dynamic-data execution-consumer method is not a companion of {owner}")
for skill, triggers in {
    "compositional-exploit-chain-hunter": (
        "dynamic object to protocol injection",
        "import metadata to delayed execution",
        "optional dependency to interpreter",
    ),
    "expert-cache-proxy-parser-differential-hunter": (
        "dynamic resource method override",
        "to_s bytesize mismatch",
        "optional dependency interpreter activation",
    ),
    "modern-rce-chain-hunter": (
        "redis command injection to deserialization",
        "open3.popen3 string command",
        "optional dependency sandbox escape",
    ),
    "patch-diff-root-cause-analyzer": (
        "cve-2022-2185",
        "dynamic data execution consumer patch",
    ),
}.items():
    available = data.get("skill_routes", {}).get(skill, {}).get("triggers", [])
    for trigger in triggers:
        if trigger not in available:
            errors.append(f"{skill} route is missing dynamic-data trigger: {trigger}")
try:
    execution_text = (ROOT / execution_method).read_text(encoding="utf-8")
    normalized_execution = " ".join(execution_text.split())
    for required_phrase in (
        "DYNAMIC_DATA_EXECUTION_CONSUMER:v1",
        "Dynamic object methods become protocol control",
        "Import metadata becomes delayed execution state",
        "Optional dependency silently enables an interpreter",
        "HackerOne `#1679624`",
        "GitLab issue `#371884`",
        "HackerOne `#1609965`",
        "CVE-2022-2185",
        "HackerOne `#1401444`",
        "GitLab issue `#345892`",
        "same immutable buffer",
        "strict attribute allowlists",
        "fixed executable plus argv/stdin",
        "NEEDS_EXECUTION_CONSUMER_PROOF",
        "Never write an operational Redis/session injection payload",
        "STRONG + MANUALLY_CONFIRMED",
    ):
        if required_phrase.lower() not in normalized_execution.lower():
            errors.append(f"dynamic-data execution-consumer method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate dynamic-data execution-consumer methodology: {exc}")

for execution_regression in (
    "automation/test-dynamic-data-execution-consumer.py",
    "config/DYNAMIC_DATA_EXECUTION_CONSUMER_REGRESSION_CASES.json",
):
    route = data.get("artifact_routes", {}).get(execution_regression, {})
    if route.get("mode") != "conditional":
        errors.append(f"dynamic-data execution-consumer regression artifact must be conditional: {execution_regression}")

cross_boundary_method = "references/CROSS_BOUNDARY_COMPOSITION_METHOD.md"
cross_boundary_route = data.get("artifact_routes", {}).get(cross_boundary_method, {})
if cross_boundary_route.get("mode") != "conditional":
    errors.append("cross-boundary composition method must be conditional")
composition_route = data.get("skill_routes", {}).get("compositional-exploit-chain-hunter", {})
if cross_boundary_method not in composition_route.get("companions", []):
    errors.append("cross-boundary composition method is not a companion of compositional-exploit-chain-hunter")
for skill, triggers in {
    "compositional-exploit-chain-hunter": (
        "workflow context poisoning",
        "jint newtonsoft serializer coercion",
        "jwt algorithm confusion",
        "active directory acl chain",
        "layered mobile request signing",
        "ai to database authorization",
        "dataset entitlement bypass",
        "cross-user ai memory",
        "sas export authorization",
    ),
    "expert-ai-model-bug-bounty-auditor": (
        "natural language to sql",
        "ai query confused deputy",
        "dataset entitlement bypass",
        "ai result fan-out",
    ),
    "expert-authentication-authorization-hunter": (
        "shared context identity overwrite",
        "credential resolver fallback",
        "rs256 to hs256",
        "legacy verifier drift",
        "dataset entitlement bypass",
        "ai query confused deputy",
        "cross-user ai memory",
    ),
    "expert-sql-database-engineer": (
        "natural language to sql",
        "ai generated sql",
        "dataset entitlement bypass",
    ),
    "expert-web-api-business-logic-hunter": (
        "natural language to sql idor",
        "dataset entitlement bypass",
        "sas export authorization",
    ),
    "api-security-reviewer": (
        "natural language to sql",
        "dataset entitlement bypass",
        "sas export authorization",
    ),
    "expert-dotnet-csharp-engineer": (
        "jint",
        "newtonsoft",
        "typenamehandling",
        "managed interop coercion",
    ),
    "expert-crypto-signature-protocol-hunter": (
        "jwt algorithm confusion",
        "rs256 to hs256",
        "device-bound signing",
    ),
    "expert-mobile-client-hunter": (
        "layered mobile request signing",
        "x-khronos",
        "ticketguard",
    ),
    "expert-windows-internals-vulnerability-researcher": (
        "active directory acl chain",
        "shadow credentials",
        "gpcfilesyspath",
        "cluster name object",
    ),
}.items():
    available = data.get("skill_routes", {}).get(skill, {}).get("triggers", [])
    for trigger in triggers:
        if trigger not in available:
            errors.append(f"{skill} route is missing cross-boundary trigger: {trigger}")
try:
    cross_boundary_text = (ROOT / cross_boundary_method).read_text(encoding="utf-8")
    normalized_cross_boundary = " ".join(cross_boundary_text.split())
    for required_phrase in (
        "CROSS_BOUNDARY_COMPOSITION_METHOD:v1",
        "Shared-context identity collision",
        "Interop coercion and serializer construction",
        "Legacy/current JWT verifier drift",
        "Active Directory ACL chain reconstruction",
        "Layered mobile request-signing reconstruction",
        "AI-to-data authorization and result fan-out",
        "one-variable `S/C/P` control triad",
        "Enumerate actual runtime members",
        "A narrow gadget fix is a new architecture lead",
        "Recoverability or publication of an RSA public key is not a vulnerability",
        "A writable share or modified attribute alone is not Domain Admin",
        "It does not bypass an ECDSA/private-key layer",
        "Listing a user's accessible datasets is discovery, not enforcement",
        "signed object-storage URLs as bearer capabilities",
        "unexpected third-party PII or business data",
        "STRONG + MANUALLY_CONFIRMED",
    ):
        if required_phrase.lower() not in normalized_cross_boundary.lower():
            errors.append(f"cross-boundary composition method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate cross-boundary composition methodology: {exc}")

for required_path, required_phrase in (
    ("skill/compositional-exploit-chain-hunter/SKILL.md", cross_boundary_method),
    ("skill/compositional-exploit-chain-hunter/agents/openai.yaml", "cross-boundary composition method"),
    ("skill/compositional-exploit-chain-hunter/references/pattern-atlas.md", "AI-to-data authority and result fan-out patterns"),
    ("skill/expert-ai-model-bug-bounty-auditor/SKILL.md", "AI/NL-to-SQL data authority and export fan-out"),
    ("skill/expert-authentication-authorization-hunter/SKILL.md", "AI/NL-to-SQL and analytics tools"),
    ("skill/expert-sql-database-engineer/SKILL.md", "AI/NL-to-SQL execution"),
    ("prompts/MASTER_PROMPT_EXPERT_AI_MODEL_AUDIT.md", "AI/NL-to-SQL dataset authority"),
    ("prompts/MASTER_PROMPT_AI_BUG_BOUNTY.md", "AI/NL-to-SQL confused-deputy paths"),
    ("prompts/MASTER_PROMPT_COMPOSITIONAL_EXPLOIT_CHAIN_AUDIT.md", cross_boundary_method),
    ("prompts/MASTER_PROMPT_MANDATORY_AUTO_ROUTER.md", cross_boundary_method),
    ("prompts/SYSTEM_PROMPT_AUTHORIZED_OFFENSIVE_IMPACT_GATE.md", "CROSS_BOUNDARY_COMPOSITION:v1"),
    ("authorized-security-autopilot/SKILL.md", cross_boundary_method),
    ("AUTOLOAD.md", cross_boundary_method),
    ("README.md", cross_boundary_method),
):
    try:
        if required_phrase not in (ROOT / required_path).read_text(encoding="utf-8"):
            errors.append(f"cross-boundary composition integration missing from {required_path}")
    except Exception as exc:
        errors.append(f"cannot validate cross-boundary integration in {required_path}: {exc}")

image_decoder_chain_method = "references/IMAGE_DECODER_SSO_CONNECTOR_CHAIN_METHOD.md"
image_decoder_chain_route = data.get("artifact_routes", {}).get(image_decoder_chain_method, {})
if image_decoder_chain_route.get("mode") != "conditional":
    errors.append("image-decoder/SSO/connector method must be conditional")
composition_route = data.get("skill_routes", {}).get("compositional-exploit-chain-hunter", {})
if image_decoder_chain_method not in composition_route.get("companions", []):
    errors.append("image-decoder/SSO/connector method is not a companion of compositional-exploit-chain-hunter")
for skill, triggers in {
    "compositional-exploit-chain-hunter": (
        "libheif image upload chain",
        "native image decoder to sso",
        "sso to connected integration",
        "heif heist",
    ),
    "expert-authentication-authorization-hunter": (
        "sso relying party compromise",
        "connected integration authority",
    ),
    "modern-rce-chain-hunter": (
        "native image decoder rce",
        "libheif rce",
        "image worker sandbox escape",
    ),
    "patch-diff-root-cause-analyzer": (
        "libheif backport",
        "ghsa-vhm9-85gw-x335",
        "cve-2026-32882",
        "dsa-6417-1",
    ),
}.items():
    available = data.get("skill_routes", {}).get(skill, {}).get("triggers", [])
    for trigger in triggers:
        if trigger not in available:
            errors.append(f"{skill} route is missing image-decoder chain trigger: {trigger}")
try:
    image_decoder_chain_text = (ROOT / image_decoder_chain_method).read_text(encoding="utf-8")
    normalized_image_decoder_chain = " ".join(image_decoder_chain_text.split())
    for required_phrase in (
        "IMAGE_DECODER_SSO_CONNECTOR_CHAIN:v1",
        "Artifact and patch ledger",
        "Representation ledger",
        "Process-authority ledger",
        "Identity and SSO ledger",
        "Connected-integration ledger",
        "EXACT_ROOT_IDENTITY=PROVEN|UNRESOLVED|DIFFERENT",
        "KILL_SANDBOX_CONTAINS_CAPABILITY",
        "Never disguise a live target as a CTF",
        "TRIAGER_PROOF=PASS",
    ):
        if required_phrase.lower() not in normalized_image_decoder_chain.lower():
            errors.append(f"image-decoder/SSO/connector method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate image-decoder/SSO/connector methodology: {exc}")

for required_path, required_phrase in (
    ("skill/mandatory-auto-router/SKILL.md", image_decoder_chain_method),
    ("authorized-security-autopilot/SKILL.md", image_decoder_chain_method),
    ("prompts/SYSTEM_PROMPT_AUTHORIZED_OFFENSIVE_IMPACT_GATE.md", "IMAGE_DECODER_SSO_CONNECTOR_CHAIN:v1"),
    ("prompts/MASTER_PROMPT_MANDATORY_AUTO_ROUTER.md", image_decoder_chain_method),
    ("prompts/MASTER_PROMPT_COMPOSITIONAL_EXPLOIT_CHAIN_AUDIT.md", image_decoder_chain_method),
    ("skill/compositional-exploit-chain-hunter/SKILL.md", "Native media decoder to SSO and connected-integration chains"),
    ("skill/compositional-exploit-chain-hunter/agents/openai.yaml", "native media-decoder"),
    ("skill/apex-black/SKILL.md", image_decoder_chain_method),
    ("skill/apex-black/prompts/APEX_BLACK_ROOT_PROMPT.md", "native image/media chains"),
    ("skill/apex-black/references/APEX_BLACK_METHOD.md", image_decoder_chain_method),
    ("AUTOLOAD.md", image_decoder_chain_method),
    ("README.md", image_decoder_chain_method),
):
    try:
        if required_phrase not in (ROOT / required_path).read_text(encoding="utf-8"):
            errors.append(f"image-decoder/SSO/connector integration missing from {required_path}")
    except Exception as exc:
        errors.append(f"cannot validate image-decoder/SSO/connector integration in {required_path}: {exc}")

archive_renderer_method = "references/ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md"
archive_renderer_route = data.get("artifact_routes", {}).get(archive_renderer_method, {})
if archive_renderer_route.get("mode") != "conditional":
    errors.append("archive/renderer/framework method must be conditional")
for owner in (
    "api-security-reviewer",
    "compositional-exploit-chain-hunter",
    "expert-cache-proxy-parser-differential-hunter",
    "expert-php-ruby-engineer",
    "expert-source-code-bug-hunter",
    "expert-web-api-business-logic-hunter",
    "modern-rce-chain-hunter",
    "patch-diff-root-cause-analyzer",
    "secure-code-reviewer",
):
    route = data.get("skill_routes", {}).get(owner, {})
    if archive_renderer_method not in route.get("companions", []):
        errors.append(f"archive/renderer/framework method is not a companion of {owner}")
for skill, triggers in {
    "compositional-exploit-chain-hunter": (
        "archive symlink to file read",
        "browser route to file deletion",
        "inline document option to dynamic loader",
    ),
    "expert-cache-proxy-parser-differential-hunter": (
        "symlink followed by file open",
        "encoded path browser differential",
        "inline kramdown options",
    ),
    "modern-rce-chain-hunter": (
        "inline option dynamic class loader",
        "kramdown formatter class",
    ),
    "patch-diff-root-cause-analyzer": (
        "gitlab issue 349524",
        "cve-2021-22238",
        "archive renderer framework patch",
    ),
}.items():
    available = data.get("skill_routes", {}).get(skill, {}).get("triggers", [])
    for trigger in triggers:
        if trigger not in available:
            errors.append(f"{skill} route is missing archive/renderer trigger: {trigger}")
try:
    archive_renderer_text = (ROOT / archive_renderer_method).read_text(encoding="utf-8")
    normalized_archive_renderer = " ".join(archive_renderer_text.split())
    for required_phrase in (
        "ARCHIVE_RENDERER_FRAMEWORK_CONSUMER:v1",
        "GitLab issue `#349524`",
        "GDK issue `#1314`",
        "CVE-2021-22238",
        "GitLab issue `#324452`",
        "GitLab issue `#232829`",
        "archive entry becomes a different filesystem object",
        "browser request reaches a destructive filesystem sink",
        "upload metadata becomes markup and a secondary resource load",
        "inline document options select runtime capability",
        "framework-reserved option namespace",
        "NEEDS_ARCHIVE_RENDERER_PROOF",
        "Never test a real delete path",
        "STRONG + MANUALLY_CONFIRMED",
    ):
        if required_phrase.lower() not in normalized_archive_renderer.lower():
            errors.append(f"archive/renderer/framework method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate archive/renderer/framework methodology: {exc}")

for archive_renderer_regression in (
    "automation/test-archive-renderer-framework.py",
    "config/ARCHIVE_RENDERER_FRAMEWORK_REGRESSION_CASES.json",
):
    route = data.get("artifact_routes", {}).get(archive_renderer_regression, {})
    if route.get("mode") != "conditional":
        errors.append(f"archive/renderer/framework regression artifact must be conditional: {archive_renderer_regression}")

reparse_provenance_method = "references/REPARSE_CONFIG_PROVENANCE_METHOD.md"
reparse_provenance_route = data.get("artifact_routes", {}).get(reparse_provenance_method, {})
if reparse_provenance_route.get("mode") != "conditional":
    errors.append("reparse/config/provenance method must be conditional")
for owner in (
    "api-security-reviewer",
    "compositional-exploit-chain-hunter",
    "expert-cache-proxy-parser-differential-hunter",
    "expert-go-engineer",
    "expert-php-ruby-engineer",
    "expert-source-code-bug-hunter",
    "expert-web-api-business-logic-hunter",
    "patch-diff-root-cause-analyzer",
    "secure-code-reviewer",
):
    route = data.get("skill_routes", {}).get(owner, {})
    if reparse_provenance_method not in route.get("companions", []):
        errors.append(f"reparse/config/provenance method is not a companion of {owner}")
for skill, triggers in {
    "compositional-exploit-chain-hunter": (
        "decoded recovery text to markup reparse",
        "url data to configuration grammar",
        "import attribute to virtual setter",
    ),
    "expert-cache-proxy-parser-differential-hunter": (
        "decode depth markup reparse",
        "signed multipart nested parser collision",
        "virtual setter assignment order",
    ),
    "expert-go-engineer": (
        "git config key grammar",
    ),
    "patch-diff-root-cause-analyzer": (
        "gitlab issue 213273",
        "gitlab issue 215212",
        "cve-2020-10956",
    ),
}.items():
    available = data.get("skill_routes", {}).get(skill, {}).get("triggers", [])
    for trigger in triggers:
        if trigger not in available:
            errors.append(f"{skill} route is missing reparse/config/provenance trigger: {trigger}")
try:
    reparse_provenance_text = (ROOT / reparse_provenance_method).read_text(encoding="utf-8")
    normalized_reparse_provenance = " ".join(reparse_provenance_text.split())
    for required_phrase in (
        "REPARSE_CONFIG_PROVENANCE:v1",
        "GitLab issue `#213273`",
        "GitLab issue `#215640`",
        "GitLab issue `#215212`",
        "GitLab issue `#214636`",
        "GitLab issue `#212089`",
        "CVE-2020-10956",
        "trusted recovery text is decoded and reparsed as markup",
        "stored metadata becomes a generated HTML document",
        "data enters a secondary configuration grammar",
        "signed multipart provenance is lost across parser namespaces",
        "import attributes invoke generated or virtual setters",
        "NEEDS_REPARSE_PROVENANCE_PROOF",
        "never enumerate process identifiers or descriptors",
        "STRONG + MANUALLY_CONFIRMED",
    ):
        if required_phrase.lower() not in normalized_reparse_provenance.lower():
            errors.append(f"reparse/config/provenance method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate reparse/config/provenance methodology: {exc}")

for reparse_provenance_regression in (
    "automation/test-reparse-config-provenance.py",
    "config/REPARSE_CONFIG_PROVENANCE_REGRESSION_CASES.json",
):
    route = data.get("artifact_routes", {}).get(reparse_provenance_regression, {})
    if route.get("mode") != "conditional":
        errors.append(f"reparse/config/provenance regression artifact must be conditional: {reparse_provenance_regression}")

path_cli_gadget_method = "references/PATH_CLI_GADGET_CHAIN_METHOD.md"
path_cli_gadget_route = data.get("artifact_routes", {}).get(path_cli_gadget_method, {})
if path_cli_gadget_route.get("mode") != "conditional":
    errors.append("path/CLI/gadget-chain method must be conditional")
for owner in (
    "api-security-reviewer",
    "compositional-exploit-chain-hunter",
    "expert-cache-proxy-parser-differential-hunter",
    "expert-go-engineer",
    "expert-javascript-typescript-engineer",
    "expert-php-ruby-engineer",
    "expert-source-code-bug-hunter",
    "expert-web-api-business-logic-hunter",
    "modern-rce-chain-hunter",
    "patch-diff-root-cause-analyzer",
    "secure-code-reviewer",
):
    route = data.get("skill_routes", {}).get(owner, {})
    if path_cli_gadget_method not in route.get("companions", []):
        errors.append(f"path/CLI/gadget-chain method is not a companion of {owner}")
for skill, triggers in {
    "api-security-reviewer": (
        "uploads rewriter path capture",
        "git ref option grammar",
        "rdoc javascript gadget",
    ),
    "compositional-exploit-chain-hunter": (
        "path read to signing capability",
        "cli overwrite to protected capability",
        "sanitizer to javascript gadget",
    ),
    "expert-cache-proxy-parser-differential-hunter": (
        "regex path capture authorization",
        "argv operand option differential",
        "sanitizer javascript gadget",
    ),
    "expert-go-engineer": (
        "child argv option injection",
        "git subcommand grammar",
    ),
    "expert-javascript-typescript-engineer": (
        "attribute to dynamic html gadget",
        "rdoc wiki gadget",
    ),
    "patch-diff-root-cause-analyzer": (
        "gitlab issue 212175",
        "gitaly issue 1801",
        "gitaly issue 1799",
        "gitlab issue 65335",
        "gitaly issue 1892",
        "path cli gadget chain patch",
    ),
}.items():
    available = data.get("skill_routes", {}).get(skill, {}).get("triggers", [])
    for trigger in triggers:
        if trigger not in available:
            errors.append(f"{skill} route is missing path/CLI/gadget trigger: {trigger}")
try:
    path_cli_gadget_text = (ROOT / path_cli_gadget_method).read_text(encoding="utf-8")
    normalized_path_cli_gadget = " ".join(path_cli_gadget_text.split())
    for required_phrase in (
        "PATH_CLI_GADGET_CHAIN:v1",
        "GitLab issue #212175",
        "Gitaly issue #1801",
        "historical Gitaly issue `#1799`",
        "historical GitLab FOSS issue `#65335`",
        "Gitaly issue #1892",
        "path capture is not path authorization",
        "argv data can become downstream option grammar",
        "sanitizer output can activate through a shipped gadget",
        "Patch-variant and sibling sweep",
        "NEEDS_PATH_CLI_GADGET_PROOF",
        "Never upgrade a file read, file overwrite, truncation, malformed DOM, or stored markup primitive to RCE",
        "STRONG + MANUALLY_CONFIRMED",
    ):
        if required_phrase.lower() not in normalized_path_cli_gadget.lower():
            errors.append(f"path/CLI/gadget-chain method missing required contract: {required_phrase}")
except Exception as exc:
    errors.append(f"cannot validate path/CLI/gadget-chain methodology: {exc}")

for path_cli_gadget_regression in (
    "automation/test-path-cli-gadget-chain.py",
    "config/PATH_CLI_GADGET_CHAIN_REGRESSION_CASES.json",
):
    route = data.get("artifact_routes", {}).get(path_cli_gadget_regression, {})
    if route.get("mode") != "conditional":
        errors.append(f"path/CLI/gadget regression artifact must be conditional: {path_cli_gadget_regression}")

graph_skill = "offensive-research-graph-engineer"
graph_route = data.get("skill_routes", {}).get(graph_skill, {})
if graph_route.get("mode") != "conditional":
    errors.append("offensive research graph engineer must be conditional")
if graph_skill not in data.get("selection_policy", {}).get("explicit_intent_skills", []):
    errors.append("offensive research graph engineer must require explicit intent")
for phrase in (
    "offensive security agent graph",
    "parallel security agents",
    "multi-agent severity escalation",
):
    if phrase not in data.get("selection_policy", {}).get("explicit_intent_phrases", {}).get(graph_skill, []):
        errors.append(f"offensive research graph explicit-intent phrase missing: {phrase}")
for companion in (
    "prompts/MASTER_PROMPT_OFFENSIVE_RESEARCH_GRAPH_ENGINEERING.md",
    "references/OFFENSIVE_RESEARCH_GRAPH_ENGINEERING_METHOD.md",
    "references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md",
    "config/OFFENSIVE_RESEARCH_GRAPH_SCHEMA.json",
    "config/SEVERITY_ESCALATION_SCHEMA.json",
):
    if companion not in graph_route.get("companions", []):
        errors.append(f"offensive research graph companion missing: {companion}")
try:
    graph_skill_text = (ROOT / "skill" / graph_skill / "SKILL.md").read_text(encoding="utf-8")
    for phrase in (
        "The phrase “and then” is not an edge",
        "fresh verifier",
        "isolated worktree",
        "SEVERITY_LOCKED=YES",
        "maximum demonstrated impact",
    ):
        if phrase.lower() not in graph_skill_text.lower():
            errors.append(f"offensive research graph skill missing contract: {phrase}")
    graph_method_text = (ROOT / "references/OFFENSIVE_RESEARCH_GRAPH_ENGINEERING_METHOD.md").read_text(encoding="utf-8")
    severity_method_text = (ROOT / "references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md").read_text(encoding="utf-8")
    for phrase in ("dependency-ready", "frozen acceptance oracle", "Two zero-evidence waves"):
        if phrase.lower() not in graph_method_text.lower():
            errors.append(f"offensive graph method missing contract: {phrase}")
    for phrase in ("provisional floor", "LOCK_NO_CAPABILITY_EXPANDING_EDGE", "maximum proven severity"):
        if phrase.lower() not in severity_method_text.lower():
            errors.append(f"severity escalation method missing contract: {phrase}")
    for schema_name in ("OFFENSIVE_RESEARCH_GRAPH_SCHEMA.json", "SEVERITY_ESCALATION_SCHEMA.json"):
        schema = json.loads((ROOT / "config" / schema_name).read_text(encoding="utf-8"))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"offensive graph schema has wrong dialect: {schema_name}")
except Exception as exc:
    errors.append(f"cannot validate offensive research graph contracts: {exc}")

if errors:
    print("AUTO-ROUTING VALIDATION FAILED")
    for e in errors:
        print(f"- {e}")
    raise SystemExit(1)
print(f"TOP_LEVEL_SKILLS={len(skills)}")
print(f"ROUTED_SKILLS={len(routed)}")
print(f"UNMAPPED_SKILLS={len(unmapped_skills)}")
print(f"MANUAL_ACTIVATION_REQUIRED={len(manual_activation_required)}")
print(f"AUTHORIZED_OFFENSIVE_POSTURE=PASS skills={len(skills)} prompts={len(prompt_files)} agents={len(agent_files)}")
print(f"AUTO-ROUTING VALIDATION PASSED: {len(skills)} skills and {len(actual_support)} supporting artifacts covered")
