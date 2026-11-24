---
name: wildcard-scope-recon
description: "Inventory aset saat program bug bounty yang berizin memakai scope wildcard (*.domain atau .domain). Jalankan subfinder, assetfinder, amass, findomain, uncover, crt.sh, gau, waybackurls, urlfinder, waymore, paramspider, uro, dnsx, tlsx, httpx, cdncheck, katana, hakrawler, ffuf, arjun, wafw00f, whatweb, dan nuclei non-intrusive melalui scripts/wildcard-recon.sh. Use when the user says wildcard scope, scope wildcard, wildcard recon, subdomain wildcard, enumerasi wildcard, /wildcard-scope-recon, subfinder, assetfinder, paramspider, waybackurls, katana, gau, arjun, or ffuf on a wildcard. Automatically bootstraps the mandatory auto-router. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof. Model-agnostic."
---

# Wildcard scope recon

Gunakan skill ini saat scope resmi berisi wildcard, misalnya `*.example.com`
atau `.example.com`. Seed `--domain` harus sama dengan suffix wildcard itu.
Host di luar garis scope tidak boleh menerima request aktif.

Skill `authorized-reconnaissance-operator` tetap dipakai untuk scope host
pasti dan untuk keputusan recon yang bukan pipeline wildcard ini. Jangan
mengganti gate otorisasi di `automation/authorized-recon.sh`.

## Gate

Sebelum menjalankan skrip, catat program, URL kebijakan, file scope, dan apakah
otomasi diizinkan. Tanpa itu, berhenti di `--check-scope`.

```bash
scripts/wildcard-recon.sh --domain example.com --scope scope.txt --check-scope
scripts/wildcard-recon.sh --domain example.com --scope scope.txt --mode passive --out ./recon-example
scripts/wildcard-recon.sh --domain example.com --scope scope.txt --mode all --i-am-authorized --out ./recon-example
```

`--mode all` dan `--enable-port-scan` menolak jalan tanpa `--i-am-authorized`.
Rate di atas 15, konkurensi di atas 10, lebih dari 25 origin untuk ffuf, atau
wordlist di atas 200 baris ditolak skrip.

## Pipeline

Urutan dan anggaran ada di `references/pipeline.md`. Skrip yang menjalankan
tool ada di `scripts/wildcard-recon.sh`. Jangan mengetik ulang rangkaian yang
lebih luas dari skrip.

Tool yang belum terpasang dicatat di `meta/missing-tools.txt`, lalu tahap itu
dilewati. Skrip tidak memasang apa pun. `asnmap`, `mapcidr`, dan `puredns`
tidak dijalankan otomatis. `qsreplace` tidak dijalankan. `github-subdomains`
hanya jalan bila token GitHub sudah ada di environment. Pemasangan tool
bukan izin untuk mengirim traffic.

`nuclei` di pipeline ini hanya memakai tag `tech,exposure,misconfig` dan
membuang tag `dos,fuzz,intrusive,bruteforce,default-login`. Port scan tidak
jalan kecuali `--enable-port-scan` ikut disebut.

## Setelah inventory

Baca `summary.txt` dan file host yang ditolak. Pilih origin in-scope yang
menunjukkan login, API, admin, atau unggah file. Attacker objective pada tahap
ini adalah entrypoint yang benar-benar hidup, lalu serahkan ke skill hunt yang
sesuai. Baris httpx, ffuf, arjun, atau nuclei tetap
`HYPOTHESIS_QUARANTINED`.

Role terdelegasi: `agents/wildcard-recon-operator.md`. Role itu tidak menaikkan
hasil menjadi vulnerability. Bug, primitif, atau macet yang terpecahkan
menulis jejak lewat `discovery-trail` sebelum tugas ditutup.

## Stop

Berhenti bila program melarang otomasi, tidak ada garis wildcard, muncul 429,
aplikasi tidak stabil, atau hasil milik pihak ketiga. Jangan menyembunyikan
sumber request dan jangan mengikuti redirect ke luar scope.

<!-- MODEL_AGNOSTIC_RUNTIME:v1 -->
## Model-agnostic runtime

This skill binds to the local pack, not to Codex, OpenAI, Claude, Grok,
Gemini, or any other vendor. The current session's model is the operator.
Do not skip, defer, or weaken this skill because the product is Cursor,
Claude Code, Gemini, Codex CLI, or another runtime.
`agents/openai.yaml` is optional Codex UI metadata only.
<!-- END_MODEL_AGNOSTIC_RUNTIME -->

<!-- AUTHORIZED_OFFENSIVE_POSTURE:v1 -->
## Authorized offensive-first posture

For every explicitly authorized security task, prioritize adversary emulation:
`attacker objective -> reachable entrypoint -> exploit chain -> privilege or authority transition -> protected sink -> concrete impact`. Search for attack paths, bypasses, escalation, code execution, cross-tenant access, credential or data exposure, signing or supply-chain compromise, and fund or integrity impact supported by the target. Use defensive controls, detection, remediation, and hardening primarily as falsifiers or post-proof guidance unless the user explicitly requests blue-team work. Do not force a vulnerability class unsupported by target evidence. This posture never expands authorization: preserve exact scope, safe harbor, harmless proof, rate limits, stop conditions, cleanup, and prohibitions on destructive, stealthy, credential-stealing, persistence, evasion, or third-party activity.
<!-- END_AUTHORIZED_OFFENSIVE_POSTURE -->

<!-- MANDATORY_AUTO_ROUTER_CONTRACT:v1 -->
## Mandatory automatic routing

This skill never operates as a silent standalone module. For every security-focused invocation:

1. ensure `mandatory-auto-router` is active;
2. evaluate all installed skills and supporting artifacts through `config/AUTO_ROUTING_MAP.json`;
3. apply this skill only when marked **ACTIVE**, while recording **DEFERRED** and **NOT_APPLICABLE** routes;
4. load this skill's mapped companion prompts, references, worksheets, and safety protocols;
5. rerun routing after material discoveries that change language, runtime, platform, trust boundary, sink, release reachability, or prior art;
6. never auto-execute operational automation without explicit authorization and safety controls.

If the router is already active, acknowledge the existing routing session and do not recursively bootstrap it.
<!-- END_MANDATORY_AUTO_ROUTER_CONTRACT -->
