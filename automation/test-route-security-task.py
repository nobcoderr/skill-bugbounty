#!/usr/bin/env python3
"""Regression tests for target- and scope-aware skill routing."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "automation" / "route-security-task.py"
ROUTING_MAP = ROOT / "config" / "AUTO_ROUTING_MAP.json"


def route(case: dict[str, object]) -> dict[str, object]:
    command = [sys.executable, str(ROUTER), "--task", str(case["task"]), "--json"]
    for flag in ("target", "scope", "observed"):
        for value in case.get(flag, []):
            command.extend(["--" + flag, str(value)])
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def main() -> int:
    always = set(json.loads(ROUTING_MAP.read_text(encoding="utf-8"))["always_active_skills"])
    required_core = {
        "mandatory-auto-router",
        "authorized-security-autopilot",
        "program-impact-boundary-gate",
    }
    if not required_core.issubset(always):
        print(f"ROUTING REGRESSION TESTS FAILED: missing always-active core {sorted(required_core - always)}")
        return 1
    cases = [
        {
            "name": "dotnet-source-api-auth",
            "task": "Review authorized Bitwarden server source code for BOLA and object authorization",
            "target": ["GitHub repository for the current stable release"],
            "scope": ["Source code repositories and API components are in scope; live websites are out of scope"],
            "observed": ["server/src/Api/Controllers/CiphersController.cs", "server/src/Api/Server.csproj"],
            "required": {
                "api-security-reviewer", "expert-authentication-authorization-hunter",
                "expert-dotnet-csharp-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "expert-ai-model-bug-bounty-auditor", "expert-mobile-client-hunter",
                "expert-windows-internals-vulnerability-researcher", "web-target-auditor",
                "web3-smart-contract-auditor",
            },
        },
        {
            "name": "web3-solidity-replay",
            "task": "Audit an authorized Solidity DeFi staking contract for signature replay and nonce reuse",
            "target": ["Current EVM smart contract release"],
            "scope": ["Smart contracts are in scope"],
            "observed": ["contracts/Vault.sol"],
            "required": {
                "expert-crypto-signature-protocol-hunter", "expert-race-condition-state-machine-hunter",
                "expert-source-code-bug-hunter", "secure-code-reviewer", "web3-smart-contract-auditor",
            },
            "forbidden": {
                "bountyforge-research-suite",
                "expert-ai-model-bug-bounty-auditor", "expert-authentication-authorization-hunter",
                "expert-mobile-client-hunter", "expert-windows-internals-vulnerability-researcher",
            },
        },
        {
            "name": "windows-binary-token",
            "task": "Audit a Windows service for token impersonation and reparse point privilege boundaries",
            "target": ["Signed Windows desktop service executable"],
            "scope": ["Windows desktop client and service are in scope"],
            "observed": ["release/agent.exe"],
            "required": {
                "executable-binary-auditor", "expert-reverse-engineer",
                "expert-windows-internals-vulnerability-researcher",
            },
            "forbidden": {
                "expert-ai-model-bug-bounty-auditor", "expert-authentication-authorization-hunter",
                "web3-smart-contract-auditor",
            },
        },
        {
            "name": "ai-browser-chain",
            "task": "Audit an authorized indirect prompt injection exploit chain through an AI browser agent and email token oracle",
            "target": ["AI browser agent web application"],
            "scope": ["The AI agent and researcher-owned accounts are in scope"],
            "required": {
                "compositional-exploit-chain-hunter", "expert-ai-model-bug-bounty-auditor",
                "web-target-auditor",
            },
            "forbidden": {
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-windows-internals-vulnerability-researcher", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "ambiguous-generic-terms",
            "task": "Review an agent service token configuration",
            "target": ["Generic configuration"],
            "required": always,
            "exact": always,
            "forbidden": {
                "expert-ai-model-bug-bounty-auditor", "expert-authentication-authorization-hunter",
                "expert-windows-internals-vulnerability-researcher", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "scope-excludes-mobile",
            "task": "Audit the Android mobile app and server source repository",
            "target": ["GitHub repository"],
            "scope": ["Android and iOS mobile applications are out of scope; source code repositories are in scope"],
            "observed": ["server/app.ts"],
            "required": {
                "expert-javascript-typescript-engineer", "expert-source-code-bug-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {"expert-mobile-client-hunter"},
            "excluded_surface": "mobile",
        },
        {
            "name": "explicit-multi-agent-only",
            "task": "Use adaptive multi-agent audit with a research path registry for this authorized source code audit",
            "target": ["Current GitHub repository"],
            "scope": ["Source code is in scope"],
            "observed": ["service/app.py"],
            "required": {
                "codex-cli-multi-agent-audit-orchestrator", "expert-python-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "forbidden": {"expert-windows-internals-vulnerability-researcher"},
            "required_companions": {
                "references/ADAPTIVE_RESEARCH_PATH_ORCHESTRATION_METHOD.md",
                "config/CODEX_CLI_RESEARCH_PATH_REGISTRY_SCHEMA.json",
                "automation/validate-adaptive-research-orchestration.py",
                "config/ADAPTIVE_RESEARCH_ORCHESTRATION_CASES.json",
                "automation/test-adaptive-research-orchestration.py",
            },
        },
        {
            "name": "implicit-bug-bounty-multi-agent",
            "task": "Authorized bug bounty hunt against the in-scope web API on HackerOne",
            "target": ["Current production API"],
            "scope": ["The public API is in scope for the bounty program"],
            "observed": ["api/server.go"],
            "required": {
                "api-security-reviewer",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-go-engineer",
                "expert-source-code-bug-hunter",
                "secure-code-reviewer",
                "web-target-auditor",
            },
            "forbidden": {"expert-windows-internals-vulnerability-researcher"},
            "required_companions": {
                "prompts/MASTER_PROMPT_CODEX_CLI_MULTI_AGENT_AUDIT.md",
                "references/CODEX_CLI_MULTI_AGENT_WORKFLOW.md",
                "skill/codex-cli-multi-agent-audit-orchestrator/agents/openai.yaml",
            },
        },
        {
            "name": "cloud-metadata-chain",
            "task": "Audit SSRF to GCP metadata service and Kubernetes service account token",
            "target": ["Cloud API service"],
            "scope": ["The GCP workload and researcher-owned test project are in scope"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cloud-ci-cd-supply-chain-hunter",
            },
            "forbidden": {
                "expert-ai-model-bug-bounty-auditor",
                "expert-windows-internals-vulnerability-researcher", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "wordpress-parser-rce",
            "task": "Audit current WordPress source for parser differential XSS to RCE",
            "target": ["Current WordPress GitHub source repository"],
            "scope": ["Current source release is in scope"],
            "observed": ["src/wp-login.php"],
            "required": {
                "compositional-exploit-chain-hunter", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "modern-rce-chain-hunter", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {
                "expert-ai-model-bug-bounty-auditor", "expert-mobile-client-hunter",
                "expert-windows-internals-vulnerability-researcher", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "nodejs-not-web3-node",
            "task": "Audit an authorized Node.js REST API source repository for object authorization",
            "target": ["Current server-side GitHub repository"],
            "scope": ["Server source code and API are in scope"],
            "observed": ["services/api/package.json", "services/api/src/routes.ts"],
            "required": {
                "api-security-reviewer", "expert-authentication-authorization-hunter",
                "expert-javascript-typescript-engineer", "expert-source-code-bug-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {
                "wallet-node-bridge-reviewer", "web3-smart-contract-auditor",
                "expert-windows-internals-vulnerability-researcher",
            },
        },
        {
            "name": "wordpress-xss2shell-seven-boundary",
            "task": (
                "Audit the authorized WordPress XSS2Shell CVE-2026-64638 and "
                "GHSA-52p2-r8wf-jcrf chain from login HTML sanitizer differential, "
                "DOM clobbering, JSONP Same Origin Method Execution and browser-assisted "
                "Application Password approval through WordPress REST content mutation, "
                "business logic state transitions, and plugin upload to PHP execution; "
                "verify exact backports, patch diff, and detection"
            ),
            "target": ["Historical and current WordPress PHP and JavaScript source plus isolated local web/API lab"],
            "scope": [
                "Source, web, API, advisory, patch history, and an isolated researcher-owned WordPress lab are in scope",
                "Public sites, passive version scanning, real administrator interaction, credential collection, shells, persistence, destructive upload, and subagents are prohibited",
            ],
            "observed": [
                "wp-includes/user.php",
                "wp-admin/js/user-profile.js",
                "wp-admin/authorize-application.php",
                "wp-admin/update.php",
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-authentication-authorization-hunter",
                "expert-cache-proxy-parser-differential-hunter",
                "expert-javascript-typescript-engineer", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {
                "authorized-black-box-web-tester", "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-mobile-client-hunter",
                "expert-windows-internals-vulnerability-researcher",
                "web3-smart-contract-auditor",
            },
        },
        {
            "name": "wordpress-patched-login-rendering-only",
            "task": "Review a patched WordPress authentication error input parser and HTML encoding regression without a multi-stage chain",
            "target": ["Current patched WordPress 7.0.3 PHP source repository and local web fixture"],
            "scope": ["Source and local web regression testing are in scope; active exploitation is prohibited"],
            "observed": ["wp-includes/user.php", "wp-login.php"],
            "required": always | {
                "expert-cache-proxy-parser-differential-hunter",
                "expert-authentication-authorization-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer",
                "web-target-auditor",
            },
            "exact": always | {
                "expert-cache-proxy-parser-differential-hunter",
                "expert-authentication-authorization-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer",
                "web-target-auditor",
            },
            "forbidden": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-javascript-typescript-engineer",
                "expert-web-api-business-logic-hunter", "modern-rce-chain-hunter",
            },
        },
        {
            "name": "negated-recon-is-not-intent",
            "task": "Audit the authorized web application. Do not run recon or enumerate subdomains",
            "target": ["Current production web application"],
            "scope": ["The website is in scope; subdomain enumeration is prohibited"],
            "required": {"web-target-auditor"},
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
            },
        },
        {
            "name": "indonesian-go-source-api",
            "task": "Audit kode sumber API Go untuk otorisasi objek pada repositori resmi",
            "target": ["Repositori GitHub rilis saat ini"],
            "scope": ["Kode sumber dan API termasuk scope bug bounty"],
            "observed": ["server/go.mod", "server/handlers/object.go"],
            "required": {
                "api-security-reviewer", "codex-cli-multi-agent-audit-orchestrator",
                "expert-authentication-authorization-hunter",
                "expert-go-engineer", "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator", "expert-ai-model-bug-bounty-auditor",
                "expert-windows-internals-vulnerability-researcher", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "graphql-dynamic-filter-evaluator-rce",
            "task": (
                "Audit an authorized Node.js GraphQL dynamic filter RCE chain where "
                "filter: JSON reaches sift $where and new Function"
            ),
            "target": ["Current server-side source repository and API"],
            "scope": [
                "Source code and API are in scope; live web testing and production exploitation are out of scope"
            ],
            "observed": [
                "services/web-server/package.json",
                "services/web-server/src/graphql/Scopes.graphql",
                "services/web-server/src/utils/sift.js",
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "dynamic-filter-evaluator-rce-hunter",
                "expert-cache-proxy-parser-differential-hunter",
                "expert-javascript-typescript-engineer", "expert-source-code-bug-hunter",
                "modern-rce-chain-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "ruby-playwright-generated-javascript-rce",
            "task": (
                "Audit an authorized cross-language script injection RCE path "
                "where a Rails PlaywrightService uses a Ruby heredoc to place "
                "user input into generated JavaScript before Open3.capture3 executes it, "
                "including authentication and authorization policy reachability"
            ),
            "target": ["Current server-side source repository and API release"],
            "scope": [
                "Source code and API are in scope; live web exploitation, recon, and secret extraction are out of scope"
            ],
            "observed": [
                "app/services/browser_automation/playwright_service.rb",
                "app/controllers/admin/targets_controller.rb",
                "app/policies/target_policy.rb",
                "package.json",
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "cross-language-script-injection-hunter",
                "expert-authentication-authorization-hunter",
                "expert-cache-proxy-parser-differential-hunter",
                "expert-javascript-typescript-engineer", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "modern-rce-chain-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "llm-repeated-token-to-tool-boundary",
            "task": (
                "Audit an authorized LLM agent API for a repeated token attack "
                "and tokenizer boundary that causes instruction blackout and "
                "unauthorized tool invocation against researcher-owned resources"
            ),
            "target": ["Current deployed AI agent, inference API, tokenizer, and tool dispatcher"],
            "scope": [
                "AI model, prompt injection, agent tools, API, and authorization are in scope; "
                "live web testing, model extraction, training-data collection, and denial of service are out of scope"
            ],
            "observed": [
                "Current model and tokenizer version metadata",
                "Prompt role trace and token IDs",
                "Tool arguments, acting principal, policy decision, and state read-back",
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-ai-model-bug-bounty-auditor",
                "expert-authentication-authorization-hunter",
                "expert-cache-proxy-parser-differential-hunter",
                "llm-tokenization-boundary-hunter",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "authorized-universal-jailbreak-evaluator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "public-ci-netlify-selected-site-token",
            "task": (
                "Triage an authorized public CI log to SaaS control plane and public CI log credential bridge: a Netlify authentication token "
                "was echoed in a Taskcluster live.log; distinguish role Developer, roles_allowed, "
                "site_access: selected, selected_access_site_ids, read-only function metadata, "
                "selected-site deployment authority, and provider-managed function execution"
            ),
            "target": [
                "Named historical Mozilla Taskcluster log, Netlify API account, and crash-pings.mozilla.org selected site"
            ],
            "scope": [
                "The supplied public report, official architecture and API documentation, and sanitized vendor confirmation are in scope",
                "Retrieving unrelated logs, token replay, account enumeration, deployment, function upload or execution, environment reads, mutation, raw-secret retention, live recon, and subagents are prohibited",
            ],
            "observed": [
                "Exact CI task/run/job/step and live.log metadata, anonymous access observation, and one-way token fingerprint only",
                "Sanitized historical role Developer, site_access selected, selected_access_site_ids, GET account/function metadata, revocation, and log-remediation evidence",
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "credential-exposure-capability-hunter",
                "expert-authentication-authorization-hunter",
                "expert-cloud-ci-cd-supply-chain-hunter",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-sql-database-engineer",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "public-ci-log-redaction-without-credential",
            "task": "Review an authorized public CI log redaction policy using synthetic canaries; no exposed secret is suspected",
            "target": ["Named Taskcluster CI logging configuration and synthetic test fixture"],
            "scope": ["Static configuration and isolated synthetic verification tests are in scope"],
            "observed": ["Raw and rendered log pipeline configuration plus retention metadata"],
            "required": always | {"expert-cloud-ci-cd-supply-chain-hunter"},
            "exact": always | {"expert-cloud-ci-cd-supply-chain-hunter"},
            "forbidden": {
                "credential-exposure-capability-hunter",
                "expert-authentication-authorization-hunter",
                "expert-sql-database-engineer",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "dockerhub-aws-db-credential-exposure",
            "task": (
                "Triage an authorized artifact credential bridge where a Docker Hub container image layer "
                "contains credentials in docker image: two AWS access key pairs and database credentials exposed; "
                "require vendor-side credential validity and effective permissions evidence"
            ),
            "target": ["Named Docker Hub OCI image and AWS cloud control plane"],
            "scope": [
                "The named image digest, cloud IAM credential exposure, and authentication capability validation are in scope",
                "Image pulling, broad artifact-store scanning, credential replay by the researcher, database connections, raw secret retention, mutation, and subagents are prohibited",
            ],
            "observed": [
                "OCI multi-platform manifest, immutable image digest, layer index, and secret-bearing path metadata",
                "Vendor confirmation of AWS principal and effective permissions, key rotation, AWS user removal, database credential rotation, and image deletion",
            ],
            "required": {
                "compositional-exploit-chain-hunter",
                "credential-exposure-capability-hunter",
                "expert-authentication-authorization-hunter",
                "expert-cloud-ci-cd-supply-chain-hunter",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-sql-database-engineer",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "container-image-without-credential-exposure",
            "task": "Review an authorized Docker image packaging flow; no credentials or secrets are suspected",
            "target": ["Named Docker Hub OCI image build"],
            "scope": ["The named container image build and supply-chain configuration are in scope"],
            "required": always | {"expert-cloud-ci-cd-supply-chain-hunter"},
            "exact": always | {"expert-cloud-ci-cd-supply-chain-hunter"},
            "forbidden": {
                "credential-exposure-capability-hunter",
                "expert-authentication-authorization-hunter",
                "expert-sql-database-engineer",
                "expert-windows-internals-vulnerability-researcher",
            },
        },
        {
            "name": "slack-mastodon-staging-admin-token",
            "task": (
                "Triage an authorized credential exposure to control plane where a Slack file contains "
                "a Mastodon admin API token for a staging instance; prove admin:read:accounts separately "
                "from unproven admin:write:accounts and stop on third-party PII"
            ),
            "target": ["Authorized Slack artifact and Mastodon staging Admin API"],
            "scope": [
                "The named Slack file, staging Mastodon API, OAuth scope, and authentication capability validation are in scope",
                "Using the token, listing or paginating accounts, collecting email or IP data, write or delete actions, live recon, mutation, and subagents are prohibited",
            ],
            "observed": [
                "One-way token fingerprint, staging instance identity, and PII_EXPOSED_STOP metadata only",
                "Vendor-side confirmation of admin:read:accounts, Manage Users permission, token rotation, and sanitized audit evidence",
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "credential-exposure-capability-hunter",
                "expert-authentication-authorization-hunter",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-sql-database-engineer",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "slack-jira-credential-capability",
            "task": (
                "Triage an authorized credential disclosure where an internal Slack file contains "
                "a hard-coded Jira admin API token and trace the credential to control plane, "
                "current validity, principal, and effective permissions safely"
            ),
            "target": ["Authorized internal collaboration artifact and Jira API control plane"],
            "scope": [
                "The named Slack channel file, Jira API, and authentication capability validation are in scope",
                "Using the credential, Jira user or project enumeration, mutation, live recon, and subagents are prohibited",
            ],
            "observed": [
                "Shared artifact metadata and a one-way secret fingerprint only",
                "Vendor-side confirmation of the principal, effective admin permission, and revocation",
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "credential-exposure-capability-hunter",
                "expert-authentication-authorization-hunter",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-crypto-signature-protocol-hunter",
                "expert-race-condition-state-machine-hunter",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "brave-v8-gin-provider-lifetime-uaf",
            "task": (
                "Audit an authorized renderer use-after-free in JSEthereumProvider where JavaScript "
                "retains ethereum._metamask while a base::Unretained provider may be collected; "
                "compare the ownership invariant restored by patch PR #18411"
            ),
            "target": [
                "Current brave-core source repository and Brave desktop executable"
            ],
            "scope": [
                "The named desktop renderer component, source, and isolated researcher-owned profile are in scope",
                "Live third-party browsing, real wallet data, heap grooming, code execution, sandbox escape, denial of service against others, and subagents are prohibited",
            ],
            "observed": [
                "components/brave_wallet/renderer/js_ethereum_provider.cc",
                "v8::Proxy, gin::Wrappable, JavaScript property descriptors, ASan allocation/free/use stack, and patched-build control",
            ],
            "required": {
                "executable-binary-auditor", "expert-c-cpp-engineer",
                "expert-javascript-typescript-engineer", "expert-reverse-engineer",
                "expert-source-code-bug-hunter", "native-js-binding-lifetime-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-sql-database-engineer",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "desktop-js-wrapper-without-lifetime-evidence",
            "task": (
                "Review an authorized JavaScript wrapper naming and documentation change; "
                "no ownership, callback, GC, or memory-safety issue is suspected"
            ),
            "target": ["Current desktop source repository and desktop executable"],
            "scope": ["Source and desktop release documentation are in scope"],
            "observed": ["src/renderer/js_wrapper.cc"],
            "required": always | {
                "executable-binary-auditor", "expert-c-cpp-engineer",
                "expert-javascript-typescript-engineer", "expert-reverse-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "exact": always | {
                "executable-binary-auditor", "expert-c-cpp-engineer",
                "expert-javascript-typescript-engineer", "expert-reverse-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "native-js-binding-lifetime-hunter",
                "patch-diff-root-cause-analyzer",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "slack-without-credential-exposure",
            "task": "Review an authorized Slack notification integration; no credential exposure is suspected",
            "target": ["Internal collaboration platform configuration"],
            "scope": ["The named Slack integration configuration is in scope"],
            "required": always,
            "exact": always,
            "forbidden": {
                "credential-exposure-capability-hunter",
                "expert-cloud-ci-cd-supply-chain-hunter",
            },
        },
        {
            "name": "github-actions-fork-persisted-credential",
            "task": (
                "Audit an authorized GitHub Actions Node.js fork trust chain: a fork PR runs npm ci, "
                "actions checkout persisted credentials, and a postinstall may reach a fork PR runner token; "
                "trace the fork runner credential supply chain and patch diff without exposing a live token"
            ),
            "target": ["Current and historical GitHub source repository CI workflows"],
            "scope": [
                "Source, CI/CD, and supply-chain configuration are in scope in disposable researcher-owned base and fork repositories",
                "Vendor pull requests, external callbacks, raw token capture, vendor mutation, releases, deployments, and subagents are prohibited",
            ],
            "observed": [
                ".github/workflows/tests.yml, package.json, actions/checkout@v5, npm postinstall",
                "Sanitized Git credential-location evidence, actual GITHUB_TOKEN permissions, owned canary read-back, and patched controls",
            ],
            "required": {
                "compositional-exploit-chain-hunter",
                "credential-exposure-capability-hunter",
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-javascript-typescript-engineer",
                "expert-source-code-bug-hunter",
                "github-actions-fork-trust-hunter",
                "patch-diff-root-cause-analyzer",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-sql-database-engineer",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "pull-request-target-trusted-action-only",
            "task": (
                "Review an authorized GitHub Actions metadata-only pull request target workflow "
                "that invokes a pinned trusted base action; no fork checkout, artifact download, "
                "local action, install, build, or test is performed"
            ),
            "target": ["Current GitHub source repository CI configuration"],
            "scope": ["The named source repository and CI/CD workflow are in scope"],
            "observed": [".github/workflows/metadata.yml and pinned base-repository action"],
            "required": always | {
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-source-code-bug-hunter",
                "secure-code-reviewer",
            },
            "exact": always | {
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-source-code-bug-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {
                "credential-exposure-capability-hunter",
                "github-actions-fork-trust-hunter",
                "patch-diff-root-cause-analyzer",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "github-actions-cross-step-workspace-secret-bridge",
            "task": (
                "Audit authorized content-scope-scripts HackerOne 3619287: pull_request_target "
                "checks out fork code, Node.js npm install executes an untrusted build before secret step, "
                "and the same job workspace tampering creates a workspace to secret authority bridge with cross-step secret exposure; "
                "separate runner code execution, ANTHROPIC_API_KEY reachability, pull-request label authority, "
                "release dispatch, and downstream multi-client supply-chain impact"
            ),
            "target": ["Historical GitHub source and CI workflow semver-label.yml at exact commits"],
            "scope": [
                "Source, CI/CD, patch history, and owned disposable reproduction are in scope",
                "No vendor fork PR, outbound proof collection, raw credential, token replay, label mutation, release, deployment, or subagents",
            ],
            "observed": [
                ".github/workflows/semver-label.yml, semver-release.yml, build.yml, package.json, and base/.github/scripts/semver-analysis.mjs",
                "Historical commit b5066fbcf6, mitigation eb01151209, report #3619287 execution-evidence metadata, step-scoped secret, and shared GITHUB_WORKSPACE",
            ],
            "required": {
                "compositional-exploit-chain-hunter",
                "credential-exposure-capability-hunter",
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-javascript-typescript-engineer",
                "expert-source-code-bug-hunter",
                "github-actions-fork-trust-hunter",
                "patch-diff-root-cause-analyzer",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-sql-database-engineer",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "monero-rpc-logging-deadlock-lock-graph",
            "task": (
                "Audit authorized Monero HackerOne 3307874 API endpoint remote RPC deadlock and concurrency prior art: "
                "trace an easylogging Writer lock-order inversion and circular wait, reconstruct "
                "the wait-for graph from thread dumps, and verify STACK_TRACE, log-level, public RPC, "
                "official release versus custom build, PR 10065, PR 10066, and v0.18.4.3"
            ),
            "target": [
                "Historical and current Monero C++ CMake source repository, API, plus locally built monerod ELF binary"
            ],
            "scope": [
                "Source, RPC, patch history, and an isolated local disposable node are in scope",
                "Public-node testing, live denial of service, floods, adaptive batches, rate-limit bypass, spoofed headers, external binding, and subagents are prohibited",
            ],
            "observed": [
                "external/easylogging++/easylogging++.h, src/common/stack_trace.cpp, CMakeLists.txt, and all-thread debugger snapshots",
                "Fix commits 179c924 and 36b12ed, merge commits b591866 and 2d19722, and release v0.18.4.3",
            ],
            "required": {
                "api-security-reviewer", "deadlock-lock-graph-dos-hunter",
                "executable-binary-auditor", "expert-c-cpp-engineer",
                "expert-race-condition-state-machine-hunter", "expert-reverse-engineer",
                "expert-source-code-bug-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-sql-database-engineer",
                "expert-windows-internals-vulnerability-researcher",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "rpc-latency-without-deadlock-evidence",
            "task": (
                "Review an authorized API response-timeout documentation spelling change"
            ),
            "target": ["Current C++ CMake server source repository and API documentation"],
            "scope": ["Source code and API documentation are in scope; availability testing is prohibited"],
            "observed": ["CMakeLists.txt, src/rpc/timeout_config.cpp, and docs/rpc-timeouts.md"],
            "required": always | {
                "api-security-reviewer", "expert-c-cpp-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "exact": always | {
                "api-security-reviewer", "expert-c-cpp-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "deadlock-lock-graph-dos-hunter",
                "expert-race-condition-state-machine-hunter",
                "patch-diff-root-cause-analyzer",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "go-api-missing-auth-provider-fail-open",
            "task": (
                "Audit an authorized Go API source package where a protected handler may use "
                "a nil authentication callback, missing authentication provider, optional middleware, "
                "or no-op authentication default; verify fail-open behavior and authorization invariants"
            ),
            "target": ["Current stable Go API library source and owned localhost integration fixture"],
            "scope": [
                "Source, API, authentication, authorization, and controlled local runtime verification are in scope; live targets are prohibited"
            ],
            "observed": [
                "go.mod",
                "validation middleware, authentication callback initialization, protected handler dispatch, and authoritative state read-back"
            ],
            "required": {
                "api-security-reviewer", "expert-authentication-authorization-hunter",
                "expert-go-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-black-box-web-tester", "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor",
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-windows-internals-vulnerability-researcher",
                "web3-smart-contract-auditor",
            },
        },
        {
            "name": "cosmos-group-patch-variant-critical-consumer",
            "task": (
                "Audit an authorized historical Cosmos SDK x/group source release after a prior divide-by-zero patch: "
                "perform a patch variant and error domain review for malicious group weights, decimal exponent failure, "
                "and consensus error to chain halt through EndBlocker and FinalizeBlock; compare the official advisory and fixed version"
            ),
            "target": ["Historical Cosmos SDK Go source repository and a disposable isolated local blockchain"],
            "scope": [
                "Source, patch history, and bounded local validator-node testing are in scope; public nodes, mainnet, flooding, and external effects are prohibited"
            ],
            "observed": [
                "go.mod",
                "x/group/types.go and the group tally call path into EndBlocker",
            ],
            "required": {
                "compositional-exploit-chain-hunter", "expert-go-engineer",
                "expert-source-code-bug-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "wallet-node-bridge-reviewer",
                "web3-smart-contract-auditor",
            },
            "forbidden": {
                "authorized-black-box-web-tester", "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator", "deadlock-lock-graph-dos-hunter",
                "expert-ai-model-bug-bounty-auditor", "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-windows-internals-vulnerability-researcher", "web-target-auditor",
            },
        },
        {
            "name": "go-arithmetic-fails-before-persistence",
            "task": (
                "Review an authorized current Go arithmetic library source where every calculation error is returned "
                "during input validation before state is saved; verify the narrow safe behavior without active availability testing"
            ),
            "target": ["Current Go library source repository"],
            "scope": ["Source review and unit tests are in scope; service and network testing are prohibited"],
            "observed": ["go.mod", "internal/decimal/validate.go"],
            "required": always | {
                "expert-go-engineer", "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "exact": always | {
                "expert-go-engineer", "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "compositional-exploit-chain-hunter", "deadlock-lock-graph-dos-hunter",
                "expert-cache-proxy-parser-differential-hunter", "patch-diff-root-cause-analyzer",
                "wallet-node-bridge-reviewer", "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "gitlab-kroki-selector-consumer-stored-xss",
            "task": (
                "Audit an authorized historical GitLab Kroki filter stored XSS gadget chain: a child code language "
                "satisfies the allowlist while a parent language is consumed by string-built HTML, followed by an "
                "evidence-gated same-origin CSP data-attribute gadget; compare the advisory and patch"
            ),
            "target": ["Historical GitLab Ruby and JavaScript web application source plus an isolated local fixture"],
            "scope": [
                "Source, browser rendering, and bounded local proof are in scope; vendor-hosted deployment, real users, persistence, and external callbacks are prohibited"
            ],
            "observed": [
                "lib/banzai/filter/kroki_filter.rb",
                "app/assets/javascripts/single_file_diff.js",
            ],
            "required": {
                "compositional-exploit-chain-hunter", "expert-cache-proxy-parser-differential-hunter",
                "expert-javascript-typescript-engineer", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {
                "authorized-reconnaissance-operator", "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor", "expert-cloud-ci-cd-supply-chain-hunter",
                "wallet-node-bridge-reviewer", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "gitlab-kroki-typed-selected-node-safe",
            "task": (
                "Review an authorized current GitLab Kroki filter implementation where the exact selected node's "
                "allowlisted format is retained and image attributes are set through typed DOM construction calls; verify only this narrow safe behavior"
            ),
            "target": ["Current GitLab Ruby and JavaScript web application source"],
            "scope": ["Source review and local browser rendering unit tests are in scope; remote deployment testing is prohibited"],
            "observed": [
                "lib/banzai/filter/kroki_filter.rb",
                "app/assets/javascripts/kroki_renderer.js",
            ],
            "required": always | {
                "expert-cache-proxy-parser-differential-hunter",
                "expert-javascript-typescript-engineer", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "secure-code-reviewer", "web-target-auditor",
            },
            "exact": always | {
                "expert-cache-proxy-parser-differential-hunter",
                "expert-javascript-typescript-engineer", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {
                "compositional-exploit-chain-hunter", "patch-diff-root-cause-analyzer",
                "wallet-node-bridge-reviewer", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "gitlab-bulk-import-validator-protocol-consumer",
            "task": (
                "Audit an authorized historical GitLab API repository import local transport: BulkImports accepts "
                "attacker-controlled repository metadata, a URL validator protocol consumer omits an explicit scheme boundary, "
                "and Git fetch can read a researcher-owned local repository; compare the advisory and patch"
            ),
            "target": ["Historical GitLab Ruby API and worker source plus owned disposable A/B repositories"],
            "scope": [
                "Source, API, patch history, and one local A/B canary are in scope; production path enumeration, third-party data access, and remote worker testing are prohibited"
            ],
            "observed": ["lib/bulk_imports/projects/pipelines/repository_pipeline.rb", "Gemfile"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator", "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor", "expert-cloud-ci-cd-supply-chain-hunter",
                "wallet-node-bridge-reviewer", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "repository-import-explicit-scheme-boundary-safe",
            "task": (
                "Review an authorized current Ruby API repository import where an exact URL scheme allowlist permits "
                "only HTTPS, Git, and SSH before a fixed-argument client, while local and file transports are rejected; "
                "verify the narrow safe behavior using owned fixtures"
            ),
            "target": ["Current Ruby API source repository and owned localhost unit fixture"],
            "scope": ["Source, API, and bounded local unit tests are in scope; production imports are prohibited"],
            "observed": ["lib/import/repository_importer.rb", "Gemfile"],
            "required": always | {
                "api-security-reviewer", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer",
            },
            "exact": always | {
                "api-security-reviewer", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "compositional-exploit-chain-hunter", "patch-diff-root-cause-analyzer",
                "wallet-node-bridge-reviewer", "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "gitlab-dynamic-resource-resp-session-chain",
            "task": (
                "Audit authorized historical GitLab Ruby source for a dynamic object to protocol injection chain: "
                "a Sawyer Resource API response permits a dynamic resource method override and to_s bytesize mismatch, "
                "Redis RESP framing reaches protected session state, then a separately evidenced session deserialization consumer; "
                "compare the advisory and fixed release"
            ),
            "target": ["Historical GitLab Ruby API/import worker source and isolated local mock Redis/session fixture"],
            "scope": [
                "Source, API, patch history, mock protocol framing, and inert owned-state canaries are in scope; live Redis, credentials, gadgets, commands, and subagents are prohibited"
            ],
            "observed": [
                "lib/gitlab/github_import/importer/repository_importer.rb",
                "lib/gitlab/repository_cache_adapter.rb, Sawyer::Resource, and redis-rb command framing",
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-authentication-authorization-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer", "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator", "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "ruby-protocol-one-immutable-buffer-safe",
            "task": (
                "Review an authorized current Ruby source serializer where remote values are recursively flattened "
                "to primitives and one immutable byte buffer supplies both frame length and transmitted bytes; "
                "verify this narrow safe invariant with unit tests"
            ),
            "target": ["Current Ruby library source repository"],
            "scope": ["Source review and local network-free unit tests are in scope"],
            "observed": ["Gemfile", "lib/protocol/encoder.rb"],
            "required": always | {
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "exact": always | {
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "compositional-exploit-chain-hunter", "modern-rce-chain-hunter",
                "patch-diff-root-cause-analyzer", "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "gitlab-bulk-import-metadata-delayed-shell-consumer",
            "task": (
                "Audit authorized historical GitLab bulk import metadata to delayed execution: remote import metadata "
                "crosses broad project attributes through import metadata attribute confusion, persistence, and a queued importer before archive path shell interpolation "
                "reaches an Open3.popen3 string command; compare CVE-2022-2185 and the patch"
            ),
            "target": ["Historical GitLab Ruby API, model, Sidekiq worker, and isolated local process fixture"],
            "scope": [
                "Source, API, worker, patch history, and inert local markers are in scope; live imports, shell payloads, external callbacks, and subagents are prohibited"
            ],
            "observed": [
                "lib/bulk_imports/projects/pipelines/project_pipeline.rb",
                "lib/gitlab/import_export/decompressed_archive_size_validator.rb and Open3.popen3",
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "cross-language-script-injection-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer", "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator", "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "ruby-import-strict-allowlist-fixed-argv-safe",
            "task": (
                "Review an authorized current Ruby API repository import whose remote metadata passes a strict "
                "business-field allowlist before persistence and whose worker uses a fixed program argv with a separate data channel"
            ),
            "target": ["Current Ruby API and worker source repository"],
            "scope": ["Source, API, and local network-free tests are in scope; production imports are prohibited"],
            "observed": ["Gemfile", "lib/import/attribute_projector.rb", "app/workers/import_worker.rb"],
            "required": always | {
                "api-security-reviewer", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "secure-code-reviewer",
            },
            "exact": always | {
                "api-security-reviewer", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {
                "compositional-exploit-chain-hunter", "cross-language-script-injection-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "gitlab-wikicloth-optional-dependency-interpreter",
            "task": (
                "Audit authorized historical GitLab WikiCloth Lua sandbox: optional dependency interpreter activation and "
                "optional dependency sandbox escape allow untrusted wiki markup to reach host authority; compare the advisory and patch"
            ),
            "target": ["Historical GitLab Ruby web source, WikiCloth integration, and isolated local renderer fixture"],
            "scope": [
                "Source, patch history, and an inert local capability canary are in scope; installing dependencies on a live target, commands, callbacks, and subagents are prohibited"
            ],
            "observed": ["Gemfile", "gitlab-markup mediawiki integration", "WikiCloth optional extension registration"],
            "required": {
                "compositional-exploit-chain-hunter", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "modern-rce-chain-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {
                "authorized-reconnaissance-operator", "codex-cli-multi-agent-audit-orchestrator",
                "expert-ai-model-bug-bounty-auditor", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "ruby-renderer-dependency-absent-disabled-safe",
            "task": (
                "Review an authorized current Ruby web renderer where the optional dependency interpreter is absent "
                "from shipped artifacts and explicit configuration remains disabled and fail-closed"
            ),
            "target": ["Current Ruby web application source and release artifact"],
            "scope": ["Source, package inventory, and local renderer unit tests are in scope"],
            "observed": ["Gemfile.lock", "lib/renderers/wiki_renderer.rb"],
            "required": always | {
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer", "web-target-auditor",
            },
            "exact": always | {
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {
                "compositional-exploit-chain-hunter", "modern-rce-chain-hunter",
                "patch-diff-root-cause-analyzer", "web3-smart-contract-auditor",
            },
        },
        {
            "name": "gitlab-bulk-import-archive-link-file-consumer",
            "task": (
                "Audit authorized historical GitLab bulk import uploads pipeline for archive symlink to file read: "
                "an extracted symlink is globbed and later causes a symlink followed by file open; compare GitLab issue 349524 and the fixed release"
            ),
            "target": ["Historical GitLab Ruby API source and isolated synthetic archive fixture"],
            "scope": ["Source, patch history, and disposable local fixtures are in scope; real file reads and live imports are prohibited"],
            "observed": ["lib/bulk_imports/common/pipelines/uploads_pipeline.rb", "Gemfile"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "archive-links-rejected-nofollow-safe",
            "task": "Review current Ruby source for archive entry type differential where links and special entries are rejected and final opens use a root-bound nofollow handle",
            "target": ["Current Ruby source repository"],
            "scope": ["Source and network-free synthetic archive tests are in scope"],
            "observed": ["Gemfile", "lib/import/archive_extractor.rb"],
            "required": always | {
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gdk-browser-route-destructive-sink",
            "task": (
                "Audit authorized historical Ruby web development route for browser route to file deletion: "
                "encoded path browser differential, simple cross-origin request, method override, missing CSRF, and recursive delete; compare GDK issue 1314"
            ),
            "target": ["Historical GDK Ruby web source and mocked delete receiver"],
            "scope": ["Source and inert local route fixtures are in scope; deletion and drive-by requests are prohibited"],
            "observed": ["config/routes/development.rb", "letter_opener_web/letters_controller.rb", "Gemfile"],
            "required": {
                "compositional-exploit-chain-hunter", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "destructive-route-auth-csrf-root-bound-safe",
            "task": "Review a current Ruby web route whose mutation has object authorization, is authenticated, CSRF protected, method override restricted, and delete target root-bound",
            "target": ["Current Ruby web source repository"],
            "scope": ["Source and mocked local route tests are in scope; destructive testing is prohibited"],
            "observed": ["Gemfile", "app/controllers/files_controller.rb"],
            "required": always | {
                "expert-authentication-authorization-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitlab-upload-markup-secondary-renderer-chain",
            "task": (
                "Audit authorized historical GitLab web application DesignReferenceFilter stored XSS gadget chain, upload filename markup injection, and upload metadata to secondary renderer through ReferenceRedactor "
                "and a notification resource loader business logic path; compare CVE-2021-22238 and prove each secondary renderer edge separately"
            ),
            "target": ["Historical GitLab Ruby web source and isolated renderer fixture"],
            "scope": ["Source, patch history, and inert local markup fixtures are in scope; public testing, external callbacks, and real file reads are prohibited"],
            "observed": ["lib/banzai/filter/references/design_reference_filter.rb", "lib/banzai/reference_redactor.rb", "Gemfile"],
            "required": {
                "compositional-exploit-chain-hunter", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "typed-dom-no-secondary-loader-safe",
            "task": "Review a current Ruby renderer for upload filename markup injection controls with strict filename grammar, typed DOM construction, and secondary network/filesystem loaders disabled",
            "target": ["Current Ruby web source repository"],
            "scope": ["Source and local renderer tests are in scope"],
            "observed": ["Gemfile", "lib/renderers/design_reference.rb"],
            "required": always | {
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitlab-inline-option-dynamic-loader-chain",
            "task": (
                "Audit authorized historical GitLab Kramdown wiki renderer for inline option dynamic class loader and inline document option to dynamic loader: "
                "inline Kramdown options select a formatter class, constructor options, and nested loader; compare GitLab issue 324452"
            ),
            "target": ["Historical GitLab Ruby web source and inert local constructor/loader spies"],
            "scope": ["Source, patch history, and network-free renderer tests are in scope; commands and reverse shells are prohibited"],
            "observed": ["Gemfile", "lib/gitlab/other_markup.rb", "kramdown rouge formatter integration"],
            "required": {
                "compositional-exploit-chain-hunter", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "inline-options-closed-class-map-safe",
            "task": "Review current Ruby Kramdown rendering for inline Kramdown options where sensitive inline options are forbidden and formatter selection uses a closed non-inheriting class map",
            "target": ["Current Ruby renderer source repository"],
            "scope": ["Source and inert local renderer tests are in scope"],
            "observed": ["Gemfile", "lib/renderers/markdown.rb"],
            "required": always | {
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "secure-code-reviewer",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitlab-safe-params-framework-option-boundary",
            "task": (
                "Audit authorized historical GitLab web application SafeParamsHelper business logic where an incomplete denylist creates a framework URL option to HTML consumer "
                "through a reserved URL option namespace and framework URL option namespace, altering redirect or async viewer consumers; compare GitLab issue 232829"
            ),
            "target": ["Historical GitLab Ruby web/API source and local URL-builder fixture"],
            "scope": ["Source, patch history, and network-free URL tests are in scope; public interaction and external navigation are prohibited"],
            "observed": ["app/helpers/safe_params_helper.rb", "Gemfile"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "business-param-allowlist-relative-url-safe",
            "task": "Review a current Ruby web helper for a reserved URL option namespace and framework URL option namespace where it positively allows business params and constructs only final relative same-origin URLs",
            "target": ["Current Ruby web source repository"],
            "scope": ["Source and network-free URL-builder tests are in scope"],
            "observed": ["Gemfile", "app/helpers/url_helper.rb"],
            "required": always | {
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitlab-reference-redactor-reparse-lineage",
            "task": (
                "Audit authorized historical GitLab Ruby web source for stored xss reference redaction where reference redactor decoded markup and "
                "decoded recovery text to markup reparse; compare GitLab issue 213273"
            ),
            "target": ["Historical GitLab Rails source and inert local DOM parser fixture"],
            "scope": ["Source, patch history, and network-free markup tests are in scope; live script execution is prohibited"],
            "observed": ["Gemfile", "lib/banzai/reference_redactor.rb"],
            "required": {
                "compositional-exploit-chain-hunter", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "reference-redactor-text-node-safe",
            "task": "Review current Ruby web business logic source and parser behavior where decoded recovery content is inserted only through a typed text-node API",
            "target": ["Current Rails renderer source repository"],
            "scope": ["Source and inert local DOM tests are in scope"],
            "observed": ["Gemfile", "lib/rendering/reference_recovery.rb"],
            "required": always | {
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitlab-pypi-generated-html-lineage",
            "task": (
                "Audit authorized historical GitLab API and Ruby web business logic source where stored metadata to generated html document, a generated html api response, "
                "and pypi simple html presenter cross an attribute grammar; compare GitLab issue 215640"
            ),
            "target": ["Historical GitLab package API source and inert HTML parser fixture"],
            "scope": ["Source, patch history, and network-free document tests are in scope; public package upload is prohibited"],
            "observed": ["Gemfile", "app/presenters/packages/pypi/package_presenter.rb"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "pypi-typed-html-builder-safe",
            "task": "Review a current Ruby web package API business logic and parser for a generated html api response where every stored field uses a context-aware typed HTML builder",
            "target": ["Current package API source repository"],
            "scope": ["Source and network-free HTML tests are in scope"],
            "observed": ["Gemfile", "app/presenters/package_index.rb"],
            "required": always | {
                "api-security-reviewer", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitaly-url-config-grammar-lineage",
            "task": (
                "Audit authorized historical Gitaly Go web API repository import where url data to configuration grammar and git config key grammar alter a network client; "
                "compare GitLab issue 215212"
            ),
            "target": ["Historical Gitaly Go source and inert Git-config parser fixture"],
            "scope": ["Source, patch history, and loopback-only config tests are in scope; live SSRF is prohibited"],
            "observed": ["go.mod", "internal/service/repository/create_from_url.go"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-go-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitaly-fixed-config-key-safe",
            "task": "Review current Go API business logic source and parser handling for git config key grammar where repository import keeps a fixed trusted key and URL only as a typed value",
            "target": ["Current Go repository import source"],
            "scope": ["Source and loopback-free parser tests are in scope"],
            "observed": ["go.mod", "internal/importer/config.go"],
            "required": always | {
                "api-security-reviewer", "expert-cache-proxy-parser-differential-hunter",
                "expert-go-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitlab-workhorse-signed-provenance-lineage",
            "task": (
                "Audit authorized historical GitLab Ruby web API business logic multipart path where signed multipart provenance to ambient parameter and signed multipart nested parser collision "
                "reach a file consumer; compare GitLab issue 214636"
            ),
            "target": ["Historical GitLab middleware source and mocked file opener"],
            "scope": ["Source, patch history, and synthetic parser fixtures are in scope; real file reads and special-path enumeration are prohibited"],
            "observed": ["Gemfile", "lib/gitlab/middleware/multipart.rb"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "workhorse-exact-signed-carrier-safe",
            "task": "Review a current Ruby API business logic signed multipart field provenance design where nested parser collisions are rejected and only the typed signed carrier reaches a mocked opener",
            "target": ["Current Ruby upload middleware source"],
            "scope": ["Source and synthetic parser fixtures are in scope"],
            "observed": ["Gemfile", "lib/middleware/trusted_upload.rb"],
            "required": always | {
                "api-security-reviewer", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitlab-carrierwave-virtual-setter-lineage",
            "task": (
                "Audit authorized historical GitLab Ruby web API business logic and parser differential import where import attribute to virtual setter, remote attachment virtual setter, and carrierwave remote setter "
                "cause a network side effect; compare GitLab issue 212089 and CVE-2020-10956"
            ),
            "target": ["Historical GitLab Rails import source and fake network adapter"],
            "scope": ["Source, patch history, and loopback-free setter spies are in scope; live SSRF is prohibited"],
            "observed": ["Gemfile", "lib/gitlab/import_export/attribute_cleaner.rb", "app/models/note.rb"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "import-attribute-allowlist-setter-order-safe",
            "task": "Review current Ruby web API business logic and parser differential for a carrierwave remote setter where a strict import allowlist excludes generated setters and assignment order is unit tested",
            "target": ["Current Rails import source repository"],
            "scope": ["Source and fake-setter tests are in scope"],
            "observed": ["Gemfile", "lib/import/attribute_allowlist.rb"],
            "required": always | {
                "api-security-reviewer", "expert-cache-proxy-parser-differential-hunter",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitlab-uploadsrewriter-path-capability-lineage",
            "task": (
                "Audit authorized historical GitLab Ruby web API business logic for uploads rewriter issue move, uploads rewriter path capture, "
                "regex path capture authorization, path read to signing capability, canonical path copy sink, and file read to signing capability; "
                "compare GitLab issue 212175"
            ),
            "target": ["Historical GitLab Rails source and synthetic root-bound file fixture"],
            "scope": ["Source, patch history, disposable fixture files, and test-only capability canaries are in scope; real file or credential access is prohibited"],
            "observed": ["Gemfile", "app/uploaders/uploads_rewriter.rb"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "uploadsrewriter-root-bound-copy-safe",
            "task": (
                "Review current Ruby web API business logic source for uploads rewriter path capture, regex path capture authorization, "
                "path capture canonical root, path regex to file copy, and canonical path copy sink; prove path read to signing capability is unreachable"
            ),
            "target": ["Current Rails source and synthetic root-bound file fixture"],
            "scope": ["Source and disposable fixture files are in scope"],
            "observed": ["Gemfile", "app/services/uploads_rewriter.rb"],
            "required": always | {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-php-ruby-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitaly-wiki-ref-option-lineage",
            "task": (
                "Audit authorized historical Gitaly Go web API for git ref option grammar, argv operand option differential, child argv option injection, "
                "git subcommand grammar, git ref flag injection, cli overwrite to protected capability, file overwrite to capability, and git argv option grammar sink; "
                "compare Gitaly issue 1801 and CVE-2019-14944"
            ),
            "target": ["Historical Gitaly Go source and fake child-process argv recorder"],
            "scope": ["Source, patch history, and network-free argv fixtures are in scope; file overwrite and process execution are prohibited"],
            "observed": ["go.mod", "internal/service/search/wiki.go"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-go-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "git-ref-terminator-and-validator-safe",
            "task": (
                "Review current Go web API business logic for git ref option grammar, argv operand option differential, child argv option injection, "
                "git subcommand grammar, git ref flag injection, and git argv option grammar sink; verify cli overwrite to protected capability and "
                "file overwrite to capability are blocked by a path cli gadget chain patch"
            ),
            "target": ["Current Go source and fake child-process argv recorder"],
            "scope": ["Source and network-free argv fixtures are in scope"],
            "observed": ["go.mod", "internal/git/ref.go"],
            "required": always | {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-go-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitaly-commits-multi-subcommand-lineage",
            "task": (
                "Audit authorized historical Gitaly Go web API Commits path for git ref option grammar, argv operand option differential, "
                "git subcommand grammar, cli overwrite to protected capability, file overwrite to capability, and git argv option grammar sink; "
                "compare Gitaly issue 1799"
            ),
            "target": ["Historical Gitaly Go source and fake multi-command recorder"],
            "scope": ["Source, patch history, and network-free command-order fixtures are in scope; destructive or race testing is prohibited"],
            "observed": ["go.mod", "internal/service/commit/find_commits.go"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-go-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "git-multi-subcommand-central-validation-safe",
            "task": (
                "Review current Go web API business logic where git ref option grammar, argv operand option differential, child argv option injection, "
                "git subcommand grammar, and git argv option grammar sink are controlled centrally; verify cli overwrite to protected capability and "
                "file overwrite to capability remain blocked by a path cli gadget chain patch"
            ),
            "target": ["Current Go source and fake multi-command recorder"],
            "scope": ["Source and network-free command-order fixtures are in scope"],
            "observed": ["go.mod", "internal/git/validated_ref.go"],
            "required": always | {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-go-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitlab-rdoc-shipped-javascript-gadget-lineage",
            "task": (
                "Audit authorized historical GitLab Ruby and JavaScript web API renderer for rdoc javascript gadget, sanitizer to javascript gadget, "
                "sanitizer javascript gadget, rdoc wiki gadget, rdoc sanitizer gadget, sanitizer to shipped gadget, rdoc wiki stored xss gadget, "
                "sanitizer gadget to terminal action, and shipped javascript gadget sink; compare GitLab issue 65335"
            ),
            "target": ["Historical GitLab Rails and JavaScript source with inert local DOM fixture"],
            "scope": ["Source, patch history, and network-free DOM tests are in scope; live script execution is prohibited"],
            "observed": ["Gemfile", "package.json", "app/assets/javascripts/gl_field_error.js"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-javascript-typescript-engineer",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "modern-rce-chain-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "rdoc-text-only-gadget-consumer-safe",
            "task": (
                "Review current Ruby and JavaScript web API renderer for rdoc javascript gadget, sanitizer to javascript gadget, sanitizer javascript gadget, "
                "rdoc wiki gadget, rdoc sanitizer gadget, sanitizer to shipped gadget, rdoc wiki stored xss gadget, sanitizer gadget to terminal action, "
                "and shipped javascript gadget sink; verify a path cli gadget chain patch uses text-only DOM handling"
            ),
            "target": ["Current Rails and JavaScript source with inert local DOM fixture"],
            "scope": ["Source and network-free DOM tests are in scope"],
            "observed": ["Gemfile", "package.json", "app/javascript/field_error.js"],
            "required": always | {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-javascript-typescript-engineer",
                "expert-php-ruby-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "modern-rce-chain-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "gitaly-blobs-sibling-scope-lineage",
            "task": (
                "Audit authorized historical Gitaly Go web API for search api sibling scope, git ref option grammar, working directory mode expansion, "
                "git subcommand grammar, argv data to option grammar, search scope patch variant, cli overwrite to protected capability, "
                "git argv option grammar sink, and path cli gadget chain patch; compare Gitaly issue 1892"
            ),
            "target": ["Historical Gitaly Go source and synthetic working-directory fixture"],
            "scope": ["Source, patch history, and network-free fixture reads are in scope; real configuration or credential access is prohibited"],
            "observed": ["go.mod", "internal/service/search/blobs.go"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-go-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "search-scopes-central-typed-ref-safe",
            "task": (
                "Review current Go web API business logic for search api sibling scope, git ref option grammar, working directory mode expansion, "
                "git subcommand grammar, argv data to option grammar, search scope patch variant, cli overwrite to protected capability, "
                "git argv option grammar sink, and path cli gadget chain patch; prove centralized typed refs cover every scope"
            ),
            "target": ["Current Go source and synthetic working-directory fixture"],
            "scope": ["Source and network-free fixture reads are in scope"],
            "observed": ["go.mod", "internal/service/search/validated_scope.go"],
            "required": always | {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter", "expert-go-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "patch-diff-root-cause-analyzer", "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
        },
        {
            "name": "workflow-context-identity-collision",
            "task": (
                "Audit an authorized API workflow context poisoning path with "
                "shared context identity overwrite and credential resolver fallback"
            ),
            "target": ["Current .NET authentication and tenant-authorization workflow API source"],
            "scope": [
                "Source, API, authentication, and researcher-owned tenant fixtures are in scope; third-party sends are prohibited"
            ],
            "observed": ["src/Workflow/Context.cs", "src/Workflow/Engine.csproj"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-authentication-authorization-hunter",
                "expert-dotnet-csharp-engineer", "expert-source-code-bug-hunter",
                "expert-web-api-business-logic-hunter", "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-mobile-client-hunter", "web3-smart-contract-auditor",
            },
            "companion_skill": "compositional-exploit-chain-hunter",
            "required_companions": {"references/CROSS_BOUNDARY_COMPOSITION_METHOD.md"},
        },
        {
            "name": "jint-newtonsoft-interop-coercion",
            "task": (
                "Audit an authorized Jint Newtonsoft serializer coercion TypeNameHandling RCE "
                "patch variant through managed interop coercion"
            ),
            "target": ["Current .NET workflow API source and isolated local fixture"],
            "scope": ["Source, patch history, and local non-command canary tests are in scope"],
            "observed": ["src/Templates/Evaluator.cs", "src/Templates/Templates.csproj"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-cache-proxy-parser-differential-hunter",
                "expert-dotnet-csharp-engineer", "expert-javascript-typescript-engineer",
                "expert-source-code-bug-hunter", "expert-web-api-business-logic-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-mobile-client-hunter", "web3-smart-contract-auditor",
            },
            "companion_skill": "compositional-exploit-chain-hunter",
            "required_companions": {"references/CROSS_BOUNDARY_COMPOSITION_METHOD.md"},
        },
        {
            "name": "jwt-legacy-verifier-drift",
            "task": (
                "Audit an authorized authentication web API for JWT algorithm confusion, "
                "RS256 to HS256, and legacy verifier drift using two researcher-owned tenants"
            ),
            "target": ["Current legacy and modern authentication API verifier deployment"],
            "scope": ["API authentication and owned-account read-only identity validation are in scope"],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-authentication-authorization-hunter",
                "expert-crypto-signature-protocol-hunter", "web-target-auditor",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-mobile-client-hunter", "web3-smart-contract-auditor",
            },
            "companion_skill": "compositional-exploit-chain-hunter",
            "required_companions": {"references/CROSS_BOUNDARY_COMPOSITION_METHOD.md"},
        },
        {
            "name": "active-directory-acl-chain",
            "task": (
                "Audit an authorized isolated Active Directory ACL chain with GenericAll machine account, "
                "Shadow Credentials, cluster name object, and gPCFileSysPath"
            ),
            "target": ["Researcher-owned Windows Active Directory lab"],
            "scope": ["Isolated lab DACL review and reversible tests are in scope; third-party domains are prohibited"],
            "required": {
                "compositional-exploit-chain-hunter",
                "expert-windows-internals-vulnerability-researcher",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-mobile-client-hunter", "web3-smart-contract-auditor",
            },
            "companion_skill": "compositional-exploit-chain-hunter",
            "required_companions": {"references/CROSS_BOUNDARY_COMPOSITION_METHOD.md"},
        },
        {
            "name": "mobile-layered-request-signing",
            "task": (
                "Reverse engineer an authorized Android APK binary layered mobile request signing stack "
                "including X-Khronos, X-Gorgon, X-Ladon, TicketGuard device-bound signing, and TTEncrypt"
            ),
            "target": ["Researcher-owned current Android mobile binary application artifact"],
            "scope": ["Offline mobile binary reverse engineering and owned-device traffic are in scope"],
            "observed": ["release/app.apk"],
            "required": {
                "compositional-exploit-chain-hunter", "executable-binary-auditor",
                "expert-crypto-signature-protocol-hunter", "expert-mobile-client-hunter",
                "expert-reverse-engineer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
            "companion_skill": "compositional-exploit-chain-hunter",
            "required_companions": {"references/CROSS_BOUNDARY_COMPOSITION_METHOD.md"},
        },
        {
            "name": "ai-nl-to-sql-data-authority",
            "task": (
                "Audit an authorized AI analytics web app endpoint for natural language to SQL IDOR, "
                "AI query confused deputy, dataset entitlement bypass, cross-user AI memory, "
                "and SAS export authorization result fan-out"
            ),
            "target": ["Current deployed AI analytics API and database tool"],
            "scope": [
                "API, AI tool, auth, database, and owned A/B tenant synthetic datasets are in scope; "
                "third-party PII, downloads, enumeration, and state-changing tests are prohibited"
            ],
            "required": {
                "api-security-reviewer", "compositional-exploit-chain-hunter",
                "expert-ai-model-bug-bounty-auditor",
                "expert-authentication-authorization-hunter",
                "expert-sql-database-engineer",
                "expert-web-api-business-logic-hunter", "web-target-auditor",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "expert-mobile-client-hunter",
                "expert-windows-internals-vulnerability-researcher",
                "web3-smart-contract-auditor",
            },
            "companion_skill": "compositional-exploit-chain-hunter",
            "required_companions": {"references/CROSS_BOUNDARY_COMPOSITION_METHOD.md"},
        },
        {
            "name": "native-media-decoder-sso-connector-chain",
            "task": (
                "Authorized security audit of a current HEIF image upload chain: "
                "libheif backport and native image decoder RCE in an image worker, "
                "then SSO relying party compromise and SSO to connected integration authority"
            ),
            "target": [
                "Current Linux web application authentication/SSO source and container image"
            ],
            "scope": [
                "Local exact-revision native harness and researcher-owned A/B SSO and connector fixtures are in scope; "
                "third-party accounts, target-reality deception, and live exploit payloads are prohibited"
            ],
            "observed": ["src/image/heif_decoder.cc", "container/sbom.spdx.json"],
            "required": {
                "apex-black", "compositional-exploit-chain-hunter",
                "expert-authentication-authorization-hunter", "expert-c-cpp-engineer",
                "expert-cloud-ci-cd-supply-chain-hunter", "expert-source-code-bug-hunter",
                "modern-rce-chain-hunter", "patch-diff-root-cause-analyzer",
                "secure-code-reviewer", "web-target-auditor",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "web3-smart-contract-auditor",
            },
            "companion_skill": "compositional-exploit-chain-hunter",
            "required_companions": {
                "references/IMAGE_DECODER_SSO_CONNECTOR_CHAIN_METHOD.md"
            },
        },
        {
            "name": "xchain-controlled-two-stage",
            "task": (
                "Run XCHAIN-LAB-v1 full exploit chain research on an authorized controlled source fixture: "
                "persist attacker state transition, primitive to capability, capability expander output, "
                "failure driven mutation, and exact chain edge validation"
            ),
            "target": ["Researcher-owned synthetic Python source fixture"],
            "scope": ["Network-free local evidence validation is in scope; live targets and subagents are prohibited"],
            "observed": ["automation/xchain_engine.py", "fixtures/two-stage-controlled-chain.json"],
            "required": {
                "compositional-exploit-chain-hunter",
                "exploit-chain-research-orchestrator",
                "expert-python-engineer",
                "expert-source-code-bug-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "web-target-auditor", "web3-smart-contract-auditor",
            },
            "companion_skill": "exploit-chain-research-orchestrator",
            "required_companions": {
                "skill/exploit-chain-research-orchestrator/prompts/CHAIN_ROOT_PROMPT.md",
                "skill/exploit-chain-research-orchestrator/config/ATTACKER_STATE_SCHEMA.json",
                "skill/exploit-chain-research-orchestrator/scripts/xchain_engine.py",
            },
        },
        {
            "name": "chromium-v8-runtime-chain",
            "task": (
                "Audit an authorized Chromium V8 variant as full exploit chain research: build exact revision, "
                "classify an out-of-bounds primitive, compute attacker state and newly reachable sandbox surfaces, "
                "then perform capability continuity and runtime chain validation"
            ),
            "target": ["Current Chromium and V8 C++ source in a researcher-owned local build"],
            "scope": ["Source, binary, patch history, and harmless local d8 instrumentation are in scope; live browsers and weaponization are prohibited"],
            "observed": ["src/compiler/turbofan.cc", "src/sandbox/external-pointer-table.cc"],
            "required": {
                "chromium-v8-variant-hunter",
                "compositional-exploit-chain-hunter",
                "exploit-chain-research-orchestrator",
                "expert-c-cpp-engineer",
                "expert-source-code-bug-hunter",
                "patch-diff-root-cause-analyzer",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "web3-smart-contract-auditor",
            },
            "companion_skill": "chromium-v8-variant-hunter",
            "required_companions": {
                "skill/chromium-v8-variant-hunter/prompts/v8-type-reasoning-agent.md",
                "skill/chromium-v8-variant-hunter/prompts/v8-representation-agent.md",
                "skill/chromium-v8-variant-hunter/prompts/v8-jit-assumption-agent.md",
                "skill/chromium-v8-variant-hunter/prompts/v8-gc-lifetime-agent.md",
                "skill/chromium-v8-variant-hunter/prompts/v8-sandbox-boundary-agent.md",
                "skill/chromium-v8-variant-hunter/prompts/v8-exploitability-agent.md",
                "skill/chromium-v8-variant-hunter/prompts/chrome-chain-linker.md",
            },
        },
        {
            "name": "explicit-bountyforge-solidity-fuzzing",
            "task": (
                "Use BountyForge to review an authorized Solidity repository with property fuzzing "
                "and evidence-backed triage"
            ),
            "target": ["Researcher-owned local Solidity repository"],
            "scope": ["Local source audit and network-free tests only; no live chain activity"],
            "observed": ["foundry.toml", "contracts/test.t.sol"],
            "required": {
                "bountyforge-research-suite",
                "expert-source-code-bug-hunter",
                "secure-code-reviewer",
                "web3-smart-contract-auditor",
            },
            "forbidden": {
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "web-target-auditor",
            },
            "companion_skill": "bountyforge-research-suite",
            "required_companions": {
                "prompts/MASTER_PROMPT_BOUNTYFORGE_RESEARCH_SUITE.md",
                "references/BOUNTYFORGE_ADAPTIVE_RESEARCH_METHOD.md",
                "config/BOUNTYFORGE_SOURCE_CATALOG.json",
                "skill/bountyforge-research-suite/agents/bountyforge-evidence-agent.md",
            },
        },
        {
            "name": "explicit-offensive-security-agent-graph",
            "task": (
                "Run a parallel agent audit and build an offensive security agent graph for an authorized "
                "source audit, then perform multi-agent severity escalation using capability continuity"
            ),
            "target": ["Researcher-owned current local web API source repository"],
            "scope": ["Read-only source analysis and network-free tests are in scope; live targets are prohibited"],
            "observed": ["src/routes/auth.ts", "src/policy/authorize.ts"],
            "required": {
                "codex-cli-multi-agent-audit-orchestrator",
                "offensive-research-graph-engineer",
                "exploit-chain-research-orchestrator",
                "expert-javascript-typescript-engineer",
                "expert-source-code-bug-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-black-box-web-tester",
                "authorized-reconnaissance-operator",
                "web3-smart-contract-auditor",
            },
            "companion_skill": "offensive-research-graph-engineer",
            "required_companions": {
                "prompts/MASTER_PROMPT_OFFENSIVE_RESEARCH_GRAPH_ENGINEERING.md",
                "references/OFFENSIVE_RESEARCH_GRAPH_ENGINEERING_METHOD.md",
                "references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md",
                "config/OFFENSIVE_RESEARCH_GRAPH_SCHEMA.json",
                "config/SEVERITY_ESCALATION_SCHEMA.json",
            },
        },
        {
            "name": "severity-escalation-without-agent-graph",
            "task": (
                "For a validated Medium vulnerability, recompute the attacker capability delta, inspect newly "
                "reachable protected surfaces, test severity escalation toward High or Critical, and lock only "
                "the maximum proven severity; do not use subagents or parallel execution"
            ),
            "target": ["Researcher-owned current local web API source repository"],
            "scope": ["Read-only source analysis and network-free tests are in scope; live targets are prohibited"],
            "observed": ["src/routes/auth.ts"],
            "required": always | {
                "exploit-chain-research-orchestrator",
                "expert-javascript-typescript-engineer",
                "expert-source-code-bug-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {
                "codex-cli-multi-agent-audit-orchestrator",
                "offensive-research-graph-engineer",
                "authorized-black-box-web-tester",
                "authorized-reconnaissance-operator",
            },
            "companion_skill": "exploit-chain-research-orchestrator",
            "required_companions": {
                "references/SEVERITY_ESCALATION_AND_LOCK_METHOD.md",
                "config/SEVERITY_ESCALATION_SCHEMA.json",
            },
        },
        {
            "name": "post-no-finding-counterfactual-methodology",
            "task": (
                "The authorized source audit ended in NO VALID FINDING. Create a new methodology: "
                "bagaimana jika the delayed consumer replaces the direct consumer while the invariant remains true?"
            ),
            "target": ["Current supported source release"],
            "scope": ["Source review and network-free local tests are in scope"],
            "observed": ["src/worker.py"],
            "required": always | {
                "counterfactual-methodology-synthesizer",
                "expert-python-engineer",
                "expert-source-code-bug-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {"codex-cli-multi-agent-audit-orchestrator", "web3-smart-contract-auditor"},
            "companion_skill": "counterfactual-methodology-synthesizer",
            "required_companions": {
                "prompts/MASTER_PROMPT_COUNTERFACTUAL_METHODOLOGY_SYNTHESIS.md",
                "references/COUNTERFACTUAL_METHODOLOGY_SYNTHESIS_METHOD.md",
                "config/COUNTERFACTUAL_METHODOLOGY_REGRESSION_CASES.json",
                "automation/validate-counterfactual-methodology.py",
                "automation/test-counterfactual-methodology.py",
            },
        },
        {
            "name": "signed-client-state-to-terminal-oracle",
            "task": (
                "Review an authorized Flask signed session for OAuth client secret in cookie, "
                "signed session secret reuse, pickle.loads forged session, and a protected terminal oracle"
            ),
            "target": ["Current in-scope Python web API release and captured session artifact"],
            "scope": [
                "Offline source and captured-evidence analysis are in scope; live credential replay and target execution are prohibited"
            ],
            "observed": ["service/session.py", "evidence/issued-cookie.txt"],
            "required": always | {
                "compositional-exploit-chain-hunter",
                "credential-exposure-capability-hunter",
                "evidence-to-terminal-oracle-bug-bounty",
                "expert-authentication-authorization-hunter",
                "expert-python-engineer",
                "expert-source-code-bug-hunter",
                "modern-rce-chain-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-black-box-web-tester",
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
            },
            "companion_skill": "evidence-to-terminal-oracle-bug-bounty",
            "required_companions": {
                "prompts/MASTER_PROMPT_EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY.md",
                "prompts/HERMES_PASSIVE_EVIDENCE_ANALYST.md",
                "references/EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY_METHOD.md",
            },
        },
        {
            "name": "consensus-accounting-invariant-chain",
            "task": (
                "Audit an authorized local rippled C++ source snapshot and its fixed-version patch "
                "for a dual accumulator overflow where BookStep aggregation and the ledger supply "
                "invariant use the same bounded arithmetic domain; validate only offline with an "
                "arbitrary-precision oracle and no public-network transaction"
            ),
            "target": [
                "Current in-scope Web3 validator/node release and local source artifact"
            ],
            "scope": [
                "Offline source, patch, and synthetic local-fixture analysis only; mainnet, public "
                "network, package installation, Docker, and exploit execution are prohibited"
            ],
            "observed": [
                "src/ripple/app/paths/impl/BookStep.cpp",
                "src/ripple/app/misc/InvariantCheck.cpp",
            ],
            "required": always | {
                "compositional-exploit-chain-hunter",
                "evidence-to-terminal-oracle-bug-bounty",
                "expert-c-cpp-engineer",
                "expert-source-code-bug-hunter",
                "patch-diff-root-cause-analyzer",
                "secure-code-reviewer",
                "wallet-node-bridge-reviewer",
                "web3-smart-contract-auditor",
            },
            "forbidden": {
                "authorized-black-box-web-tester",
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
            },
            "companion_skill": "evidence-to-terminal-oracle-bug-bounty",
            "required_companions": {
                "prompts/MASTER_PROMPT_EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY.md",
                "prompts/HERMES_PASSIVE_EVIDENCE_ANALYST.md",
                "references/EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY_METHOD.md",
                "references/CONSENSUS_ACCOUNTING_INVARIANT_CHAIN_METHOD.md",
            },
        },
        {
            "name": "passive-evidence-analyst-no-live-route",
            "task": (
                "Use a passive evidence analyst for blind evidence review of already-captured HTTP responses; "
                "identify hypotheses and missing proof only"
            ),
            "target": ["Captured artifacts from an authorized web application assessment"],
            "scope": ["Passive offline review only; no target requests, proxy actions, credentials, or execution"],
            "observed": ["evidence/http-history.json"],
            "required": always | {
                "evidence-to-terminal-oracle-bug-bounty",
                "web-target-auditor",
            },
            "forbidden": {
                "authorized-black-box-web-tester",
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
            },
        },
        {
            "name": "external-ai-security-platform-reference-only",
            "task": (
                "Add HackerAI and HexStrike AI to the authorized bug-bounty methodology as "
                "pinned reference-only external AI security platforms; review their MCP, "
                "agent runtime, cloud and supply-chain execution boundaries without installing "
                "or running either project"
            ),
            "target": [
                "https://github.com/hackerai-tech/hackerai",
                "https://github.com/0x4m4/hexstrike-ai",
            ],
            "scope": [
                "Read-only official-repository and source review only; external mutations, "
                "dependency setup, service startup, tool execution, target interaction, and "
                "credential use are prohibited"
            ],
            "observed": [
                "hackerai/package.json",
                "hackerai/trigger/ai/runtime/authorization.ts",
                "hexstrike-ai/hexstrike_mcp.py",
                "hexstrike-ai/hexstrike_server.py",
            ],
            "required": always | {
                "external-ai-security-tool-governor",
                "expert-ai-model-bug-bounty-auditor",
                "expert-cloud-ci-cd-supply-chain-hunter",
                "expert-javascript-typescript-engineer",
                "expert-python-engineer",
                "expert-source-code-bug-hunter",
                "secure-code-reviewer",
            },
            "forbidden": {
                "authorized-black-box-web-tester",
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "security-automation-tool-installer",
            },
            "companion_skill": "external-ai-security-tool-governor",
            "required_companions": {
                "prompts/MASTER_PROMPT_EXTERNAL_AI_SECURITY_TOOL_INTEGRATION.md",
                "prompts/HERMES_EXTERNAL_SECURITY_TOOL_EVIDENCE_ANALYST.md",
                "references/EXTERNAL_AI_SECURITY_TOOL_INTEGRATION_METHOD.md",
                "config/EXTERNAL_AI_SECURITY_TOOL_SOURCE_CATALOG.json",
                "skill/external-ai-security-tool-governor/agents/external-tool-policy-analyst.md",
            },
        },
        {
            "name": "agentic-security-research-harness-reference-only",
            "task": (
                "Add the Jenny was a Friend of Mine and Harnessing Harnesses methods, "
                "Harness Kit, RAPTOR, Defending Code Reference Harness, Baby Naptime, "
                "evilsocket Audit, Visa Vulnerability Agentic Harness, Anthropic OSS Scanner, "
                "Sequester-AG bug-bounty-triage, and morluto REA to an agentic security "
                "research harness with a hallucination bin and evidence promotion gates"
            ),
            "target": ["Pinned public articles and official repository documentation"],
            "scope": [
                "Reference-only local methodology edits; no clone, install, MCP registration, "
                "scanner, reverse-engineering tool, target, credential, external model, or subagent execution"
            ],
            "observed": ["config/AGENTIC_SECURITY_HARNESS_SOURCE_CATALOG.json"],
            "required": always | {
                "agentic-security-research-harness",
                "external-ai-security-tool-governor",
            },
            "forbidden": {
                "authorized-black-box-web-tester",
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "security-automation-tool-installer",
            },
            "companion_skill": "agentic-security-research-harness",
            "required_companions": {
                "prompts/MASTER_PROMPT_AGENTIC_SECURITY_RESEARCH_HARNESS.md",
                "prompts/HERMES_AGENTIC_HARNESS_EVIDENCE_ANALYST.md",
                "references/AGENTIC_SECURITY_RESEARCH_HARNESS_METHOD.md",
                "config/AGENTIC_SECURITY_HARNESS_SOURCE_CATALOG.json",
                "automation/validate-agentic-security-research-harness.py",
                "skill/agentic-security-research-harness/agents/harness-evidence-analyst.md",
            },
        },
        {
            "name": "webhacklist-2026-ai-preliminary-corpus",
            "task": (
                "Use the WebHackList 2026 AI evidence archive as a pinned, untrusted, "
                "reference-only prior-art corpus; compare mechanisms and derive methodology "
                "without executing article examples or testing a target"
            ),
            "target": ["Pinned WebHackList preliminary research metadata and archived prose"],
            "scope": [
                "Read-only corpus analysis only; live targets, scanners, PoCs, credentials, "
                "installers, and subagents are prohibited"
            ],
            "observed": ["config/WEBHACKLIST_2026_AI_CORPUS.json"],
            "required": always | {"webhacklist-2026-research-corpus"},
            "forbidden": {
                "authorized-black-box-web-tester",
                "authorized-reconnaissance-operator",
                "codex-cli-multi-agent-audit-orchestrator",
                "security-automation-tool-installer",
            },
            "companion_skill": "webhacklist-2026-research-corpus",
            "required_companions": {
                "prompts/MASTER_PROMPT_WEBHACKLIST_2026_RESEARCH_CORPUS.md",
                "prompts/HERMES_WEBHACKLIST_PRIOR_ART_ANALYST.md",
                "references/WEBHACKLIST_2026_CORPUS_METHOD.md",
                "config/WEBHACKLIST_2026_AI_CORPUS.json",
                "automation/validate-webhacklist-2026-corpus.py",
            },
        },
    ]

    failures: list[str] = []
    for case in cases:
        result = route(case)
        selected = {item["skill"] for item in result["selected"]}
        selected_by_name = {item["skill"]: item for item in result["selected"]}
        required = set(case.get("required", set()))
        forbidden = set(case.get("forbidden", set()))
        missing = sorted(required - selected)
        unexpected = sorted(forbidden.intersection(selected))
        if missing:
            failures.append(f"{case['name']}: missing {missing}")
        if unexpected:
            failures.append(f"{case['name']}: unexpectedly active {unexpected}")
        required_companions = set(case.get("required_companions", set()))
        if required_companions:
            companion_skill = str(case.get("companion_skill", "codex-cli-multi-agent-audit-orchestrator"))
            actual_companions = set(
                selected_by_name.get(companion_skill, {}).get("companions", [])
            )
            missing_companions = sorted(required_companions - actual_companions)
            if missing_companions:
                failures.append(f"{case['name']}: missing companions {missing_companions}")
        if "exact" in case and selected != set(case["exact"]):
            failures.append(f"{case['name']}: expected exactly {sorted(case['exact'])}, got {sorted(selected)}")
        excluded_surface = case.get("excluded_surface")
        if excluded_surface and excluded_surface not in result["target_profile"]["excluded_surfaces"]:
            failures.append(f"{case['name']}: missing scope exclusion {excluded_surface}")
        explicit_multi_agent_cases = {
            "explicit-multi-agent-only",
            "explicit-offensive-security-agent-graph",
            "implicit-bug-bounty-multi-agent",
            "indonesian-go-source-api",
        }
        blob = " ".join(
            [
                str(case.get("task", "")),
                " ".join(str(item) for item in case.get("target", [])),
                " ".join(str(item) for item in case.get("scope", [])),
            ]
        ).lower()
        bounty_auto = any(
            term in blob
            for term in (
                "bug bounty",
                "bugbounty",
                "bounty program",
                "hackerone",
                "bugcrowd",
                "intigriti",
                "yeswehack",
                "vulnerability research",
                "authorized hunt",
                "live hunt",
                "buruan bug",
                "cari bug",
                "cari celah",
                "google vrp",
                "vulnerability hunt",
            )
        )
        forbids_subagents = any(
            marker in blob
            for marker in (
                "no subagents",
                "without subagents",
                "do not use subagents",
                "subagents are prohibited",
                "subagents prohibited",
                "or subagents",
                "subagent execution",
            )
        )
        orch = "codex-cli-multi-agent-audit-orchestrator"
        if forbids_subagents:
            if orch in selected:
                failures.append(f"{case['name']}: multi-agent route activated despite subagent prohibition")
        elif bounty_auto or case["name"] in explicit_multi_agent_cases:
            if orch not in selected:
                failures.append(f"{case['name']}: multi-agent route missing on bug-bounty or explicit task")
        elif orch in selected:
            failures.append(f"{case['name']}: multi-agent route activated without bug-bounty or explicit request")
        if not required_core.issubset(selected):
            failures.append(f"{case['name']}: self-contained core missing {sorted(required_core - selected)}")

    if failures:
        print("ROUTING REGRESSION TESTS FAILED")
        for failure in failures:
            print("- " + failure)
        return 1
    print(f"ROUTING REGRESSION TESTS PASSED: {len(cases)} target/scope profiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
