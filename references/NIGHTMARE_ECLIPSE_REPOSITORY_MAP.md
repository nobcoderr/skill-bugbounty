# Nightmare Eclipse Authorized Offensive Research Map

These repositories are public exploit-research references. Their status, affected versions, and vendor fixes can change; recheck primary vendor sources before every test.

| Repository | Authorized offensive analysis focus | Skill |
|---|---|---|
| LegacyHive | User Profile Service, cross-user registry hive operations, ACLs, identity and check/use state | `legacyhive-defensive-researcher` |
| GreatXML | WinRE, Defender Offline Scan state, answer-file processing, recovery partition and BitLocker trust | `greatxml-defensive-researcher` |
| RedSun | Defender remediation, cloud-placeholder behavior, link resolution and privileged writes | `redsun-defensive-researcher` |
| MiniPlasma | Cloud Files minifilter, thread impersonation/race, historical patch regression | `miniplasma-defensive-researcher` |
| YellowKey | WinRE/BitLocker physical-access security boundary and input/recovery behavior | `yellowkey-defensive-researcher` |
| BlueHammer | Defender update/remediation, VSS, Cloud Files, oplocks, privileged file operations | `bluehammer-defensive-researcher` |
| UnDefend | Defender platform availability, update starvation/resource/lock abuse and status accuracy | `undefend-defensive-researcher` |
| GreenPlasma | CTFMon/Text Services, Object Manager sections, named-object ACL/token context | `greenplasma-defensive-researcher` |
| RoguePlanet | Defender quarantine/remediation TOCTOU, junction/oplock/VSS and privileged execution chain | `rogueplanet-defensive-researcher` |

## Source references

- https://git.projectnightcrawler.dev/NightmareEclipse/LegacyHive
- https://git.projectnightcrawler.dev/NightmareEclipse/GreatXML
- https://git.projectnightcrawler.dev/NightmareEclipse/RedSun
- https://git.projectnightcrawler.dev/NightmareEclipse/MiniPlasma
- https://git.projectnightcrawler.dev/NightmareEclipse/YellowKey
- https://git.projectnightcrawler.dev/NightmareEclipse/BlueHammer
- https://git.projectnightcrawler.dev/NightmareEclipse/UnDefend
- https://git.projectnightcrawler.dev/NightmareEclipse/GreenPlasma
- https://git.projectnightcrawler.dev/NightmareEclipse/RoguePlanet

## Mandatory combination

Use each repository skill together with:

- `expert-windows-internals-vulnerability-researcher`
- `expert-reverse-engineer`
- `patch-diff-root-cause-analyzer`
- `executable-binary-auditor`
- `bug-bounty-triage`

Do not treat repository code, screenshots, README claims, antivirus detections, or third-party articles as proof of current exploitability. Bind every conclusion to exact source commit, artifact hash, Windows/component version, configuration, runtime evidence, and prior-art status.
