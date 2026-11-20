# Expert Scope and Reachability Checklist

## Scope

- [ ] Program and safe-harbor terms captured
- [ ] Asset/repository/package/contract/product explicitly eligible
- [ ] Vulnerability class eligible
- [ ] Testing method, automation, rate, and account rules satisfied
- [ ] Exclusions and third-party boundaries mapped
- [ ] For collaboration/internal artifacts, exact workspace/channel/file access
      and credential-validation method are explicitly authorized
- [ ] Historical out-of-scope exceptions or discretionary payouts were not
      treated as current scope precedent

## Codex CLI role separation

- [ ] Scope/reality, security-model, discovery, semi-triage, specialist verification, final judgment, and human reproduction were separated
- [ ] Discovery output remained hypothesis-only, started at `CODE_DERIVED_HYPOTHESIS`, and did not self-certify
- [ ] Attacker condition, server condition, and security impact are explicit
- [ ] Agent agreement was not treated as evidence
- [ ] Manual status recorded: NOT_TESTED / BLOCKED / MANUALLY_CONFIRMED

## Real-world reachability

- [ ] Exact production/mainnet/stable-release version identified
- [ ] Source maps to shipped/deployed artifact
- [ ] Feature/configuration is enabled or realistically reachable
- [ ] Attacker network position, starting privilege, role/tenant, controlled input/state, and interaction are explicit
- [ ] Exact version/artifact/deployment, config, feature/plugin/platform prerequisites, and real consumer are explicit
- [ ] Attacker can control the input without already holding equal privilege
- [ ] Victim/system reaches the sensitive sink on the same flow
- [ ] Security boundary and concrete impact are demonstrated
- [ ] For authorization, target resource/tenant/state reaches policy evaluation or an equivalent downstream filter

## Evidence quality

- [ ] Baseline and negative control
- [ ] Repeatable safe reproduction
- [ ] Exact state before/after
- [ ] Logs/requests/traces/tests preserved
- [ ] Cleanup complete
- [ ] Prior art and duplicate family checked
- [ ] Exposed credentials are retained only as a fingerprint/redaction, with
      principal, effective permissions, revocation, and residual copies tracked

Any unchecked critical item means **BLOCKED**, **WEAK**, or **KILL**—not a valid finding.
