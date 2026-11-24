---
name: recon-toolkit
description: "Pilih dan jalankan satu tool recon pada program yang berizin: subfinder, assetfinder, amass, oneforall, httpx, webanalyze, eyewitness, wpscan, testssl.sh, waybackurls, gau, katana, paramspider, arjun, uro, gf, secretfinder, linkfinder, ffuf, feroxbuster, dirsearch, dalfox, sqlmap, xsser, gobypass403, plus dork Google, Bing, dan GitHub. Use when the user names one of those tools, says /recon-toolkit, google dork, github dork, or needs the tool that matches a recon step. Automatically bootstraps the mandatory auto-router. Defaults to an authorized offensive-first posture while preserving exact scope and harmless proof. Model-agnostic."
---

# Recon toolkit

Skill ini memilih satu tool dan satu target yang sudah masuk scope. Perintah
resminya ada di `references/tool-commands.md`. Jangan menyusun perintah yang
lebih luas dari file itu.

Untuk scope `*.domain` atau `.domain`, jalankan `wildcard-scope-recon` lebih
dulu. Skill ini menambah tool yang tidak ada di pipeline wildcard itu, atau
menjalankan satu tool yang diminta.

## Sebelum perintah

Catat program, file scope, dan host atau URL yang boleh disentuh. Tanpa itu,
jangan mengirim traffic. Pasang tool yang hilang hanya bila pengguna meminta
instalasi. Instalasi bukan izin scan.

`curl`, `jq`, `git`, `python3`, dan `go` sudah ada dan dipakai untuk mengambil
satu respons, membaca JSON, atau melihat repositori.

## Saat tool dibutuhkan

Baca `references/tool-commands.md`. Pilih satu baris. Isi domain atau URL dari
scope. Simpan keluaran di direktori kerja target. Angka thread dan rate di
file itu adalah batas atas.

`dalfox`, `sqlmap`, `xsser`, dan `gobypass403` hanya menerima satu URL yang
sudah menunjukkan refleksi, parameter, atau 403. `wpscan` hanya untuk situs
yang sudah terbukti WordPress, tanpa wordlist sandi. `testssl.sh` hanya satu
host. EyeWitness paling banyak 25 URL. OneForAll tanpa brute force DNS.

Dork ditulis lalu dibuka di browser. Jangan membuat loop request ke Google,
Bing, atau GitHub.

## Penolakan 403 dari model

`Request denied (403): permission-denied` adalah penolakan API model, sering
pada subagent. Itu bukan temuan target dan bukan alasan berhenti dari tugas
yang scope-nya sudah jelas.

1. Jangan ulangi lewat subagent.
2. Kerjakan langkah yang sama di sesi ini, dengan perintah yang sama.
3. Jangan menyamarkan, menyandikan, atau memecah permintaan supaya lolos.
4. Bila sesi ini juga menerima 403 yang sama, hentikan teknik itu dan sebut
   perintah yang tertahan. Lanjut ke langkah lain yang masih diizinkan.

Skill ini tidak mematikan filter platform.

Role: `agents/recon-toolkit-operator.md`. Hasil tool tetap
`HYPOTHESIS_QUARANTINED`.

Bug, primitif, atau macet yang terpecahkan menulis jejak lewat
`discovery-trail` sebelum tugas ditutup.

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
