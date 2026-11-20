# Expert Bug Bounty & Authorized Hacker Skill Pack — Audit Only

Paket ini berisi **84 skill expert** dan **36 prompt expert**, termasuk system-prompt overlay lokal yang selalu aktif, untuk riset bug bounty dan pengujian keamanan yang sah. Default seluruh model adalah **authorized offensive red-team first**: mulai dari attacker objective, entrypoint, exploit chain, privilege transition, protected sink, dan impact konkret. Defensive control, detection, remediation, serta hardening dipakai sebagai falsifier atau panduan setelah proof, kecuali pengguna secara eksplisit meminta blue-team work.

Postur ini berlaku model-agnostic untuk Cursor (Grok, GPT, Claude, dan model lain di picker), Codex CLI, Claude Code, Gemini, Terra, Luna, dan runtime mana pun yang membaca paket lokal. Skill dan agent tidak terikat Codex. `agents/openai.yaml` hanyalah metadata UI Codex. Ia tidak memperluas authorization: scope, safe harbor, harmless proof, stop condition, cleanup, dan larangan aktivitas destruktif atau pihak ketiga tetap berlaku.


## Mandatory automatic routing

Semua tugas keamanan wajib dimulai dari `skill/mandatory-auto-router/SKILL.md`. Router membaca `config/AUTO_ROUTING_MAP.json`, mengevaluasi **seluruh 84 skill** termasuk wrapper tingkat atas `authorized-security-autopilot`, dan semua prompt/reference/config/automation pendukung. Router, autopilot, `program-impact-boundary-gate`, `novel-vulnerability-hypothesis-engine`, dan `autonomous-research-cascade-engine` aktif sebagai core tanpa aktivasi manual, lalu router mengaktifkan spesialis yang relevan dan melakukan routing ulang ketika muncul bukti baru.

- Default non-bounty menggunakan satu agent dengan tahap discovery, semi-triage, security-model/reachability/prior-art verification, final judgment, dan reproduksi manual yang terpisah secara logis. Saat kerja **bug bounty / VRP / hunt resmi**, `codex-cli-multi-agent-audit-orchestrator` nyala sendiri dan men-spawn specialist lewat Cursor Task, Codex `spawn_agent`, atau Claude Code `Agent`.
- Tidak ada skill yang boleh diam-diam dilewati: setiap skill ditandai **ACTIVE**, **DEFERRED**, atau **NOT_APPLICABLE** dengan alasan konkret.
- Sebelum membaca body skill conditional, **agent yang sedang berjalan** (model apa pun) membuat target/scope evidence card dari program resmi, exact asset, exclusions, testing mode, repository/artifact, runtime, platform, trust boundary, primitive, dan sink. Hanya core pack dan specialist yang didukung bukti tersebut yang dimuat.
- Kata umum seperti `agent`, `token`, `service`, `browser`, `package`, `oracle`, `node`, atau `workflow` tidak cukup untuk mengaktifkan specialist. Out-of-scope evidence selalu menang; sinyal yang belum cukup tetap **DEFERRED**.
- Skill bahasa dipilih dari file, manifest, dependency, build system, runtime import, dan native boundary yang benar-benar ditemukan.
- Prompt, reference, worksheet, dan safety protocol pendamping otomatis dimuat saat skill terkait aktif.
- Script di `automation/` dapat dipilih otomatis sebagai resource, tetapi **tidak pernah dijalankan otomatis**. Eksekusi aktif tetap memerlukan izin eksplisit, scope, allowlist, rate limit, abort condition, dan cleanup.
- Seluruh file `SKILL.md` memiliki kontrak bootstrap balik ke router, sehingga memulai dari skill spesialis tetap mengaktifkan routing global.
- Gunakan `python automation/validate-auto-routing.py` untuk membuktikan tidak ada skill atau artifact pendukung yang orphan.
- Gunakan `python3 automation/route-security-task.py --task "..." --target "..." --scope "..." --observed path/to/file` untuk melihat bootstrap routing deterministik. `--scope-file` menerima snapshot kebijakan lokal dan `--json` menghasilkan ledger lengkap. Selector ini read-only dan network-free; scope resmi, arsitektur, serta call path nyata tetap menjadi sumber kebenaran.
- Gunakan `python3 automation/test-route-security-task.py` untuk regression test routing lintas source/API, Web3, Windows binary, AI agent, cloud, scope exclusions, WordPress XSS2Shell seven-boundary dan patched-login negative control, GraphQL dynamic-filter evaluator, Ruby-to-JavaScript generated-script injection, V8/Gin native-binding lifetime UAF, repeated-token LLM-to-tool boundary, Slack/Jira dan Slack/Mastodon staging credential-to-capability review, public-CI-log ke selected-site Netlify capability, Docker Hub/OCI image-layer AWS/database credential exposure, GitHub Actions fork-to-runner dan same-job workspace-to-secret trust, serta patch-variant Cosmos, Kroki checked-versus-consumed, dan repository-import protocol-boundary controls.
- Gunakan `python3 automation/validate-agentic-security-research-harness.py`
  untuk memvalidasi katalog 11 sumber harness secara network-free, commit dan
  digest artifact yang dipin, status `REFERENCE_ONLY`, serta kontrak finding
  quarantine, demotion, low-privilege, memory provenance, dan zero execution.
- Gunakan `python3 automation/test-patch-variant-consumer-boundary.py` untuk tujuh regression case abstrak yang memastikan incomplete guard, selector/consumer mismatch, dan protocol expansion tidak di-KILL prematur, sementara closest-safe sibling tetap dapat di-KILL.
- Gunakan `python3 automation/test-dynamic-data-execution-consumer.py` untuk 11
  regression case abstrak yang mencakup dynamic-method protocol framing,
  import-metadata-to-worker provenance, optional-dependency interpreter
  activation, closest-safe siblings, dan terminal-impact gating.
- Gunakan `python3 automation/test-archive-renderer-framework.py` untuk 16
  regression case abstrak tentang archive link/object identity, browser-to-
  delete routing, upload-to-secondary-renderer chains, inline-option dynamic
  loading, dan request-param-to-framework-option boundaries.
- Gunakan `python3 automation/test-reparse-config-provenance.py` untuk 18
  regression case network-free tentang decode/reparse markup, stored metadata
  menjadi dokumen HTML, data masuk ke grammar konfigurasi, signed multipart
  provenance lintas parser, dan import virtual-setter assignment order.
- Gunakan `python3 automation/test-path-cli-gadget-chain.py` untuk 17 regression
  case network-free tentang path capture versus canonical object identity,
  argv operand versus child option grammar, per-subcommand/working-directory
  patch variants, sanitizer-to-JavaScript gadget activation, dan pemisahan
  primitive file/DOM dari capability serta terminal impact.
- Gunakan `python3 automation/test-novel-vulnerability-frontier.py` untuk rule
  regression invariant mining, state-machine, differential equivalence,
  resource amplification, composition KILL gate, novelty embargo, safe
  repository, dan larangan zero-day certainty. Hasil ini bukan held-out
  discovery benchmark.
- Gunakan `python3 automation/test-autonomous-research-cascade.py` untuk 12
  regression V9 tentang anchoring trap, pattern replay, generic evaluator,
  clean-vs-dirty probes, shared semantic reuse, second-order cascade, harness
  false anomalies, deterministic-validator bypass, context contamination, dan
  safe repository. Gunakan
  `python3 automation/validate-autonomous-research-cascade.py` untuk ledger.
  Keduanya network-free dan bukan bukti blind generalization.
- Gunakan `python3 automation/test-program-impact-boundary-gate.py` untuk
  memverifikasi 70 negative control Informative/Not Applicable/Duplicate, dua
  positive control Resolved/rewarded, dan kontrak capability-delta,
  trusted-domain, equivalent-path, severity-floor, synthetic-proof, serta
  fail-closed BLOCKED/KILL. Kasus historis adalah falsifier, bukan pattern
  blacklist.
- Setelah kampanye bounded menghasilkan `NO VALID FINDING`, gunakan
  `counterfactual-methodology-synthesizer` bila target masih current, in-scope,
  dan mempunyai arsitektur yang belum diuji. Skill ini membuat paling banyak
  tiga method card per siklus dan dua siklus total dengan pertanyaan
  `What if A becomes B while invariant P remains true?`. Ia menolak perubahan
  kosmetik sebagai `MUTATION_ONLY` dan tidak menganggap metode baru sebagai
  temuan. Jalankan `python3 automation/test-counterfactual-methodology.py` untuk
  14 regresi network-free dan
  `python3 automation/validate-counterfactual-methodology.py <ledger.json>`
  untuk memvalidasi desain metode tanpa menjalankan probe.
- Untuk audit multi-agent yang diminta secara eksplisit, gunakan
  `python3 automation/validate-adaptive-research-orchestration.py` untuk
  memvalidasi research-path registry dan primitive/dependency gates, serta
  `python3 automation/test-adaptive-research-orchestration.py` untuk 15
  regression network-free tentang exhausted-path reuse, adaptive-wave launch,
  specialist cap, anti-convergence, primitive chaining, exact implementation
  binding, dan termination. Tes ini tidak mengaktifkan subagent.

Entry point ringkas juga tersedia di `AUTOLOAD.md`, dengan master prompt `prompts/MASTER_PROMPT_MANDATORY_AUTO_ROUTER.md` dan protokol `references/AUTO_ROUTING_PROTOCOL.md`.

Untuk riset exploit chain yang stateful, router mengaktifkan
`skill/exploit-chain-research-orchestrator/SKILL.md` secara kondisional setelah
sebuah primitive tervalidasi menghasilkan capability delta atau ketika mode
full-chain diminta. Modul ini mempertahankan attacker state, primitive,
failed-assumption, exploit-attempt, dan chain graph secara persisten; edge hanya
valid jika capability keluaran memenuhi prasyarat tahap berikutnya dengan
continuity yang terbukti. Controlled benchmark awal berada di
`XCHAIN-LAB-v1`, terpisah dari seluruh lineage frozen V9–V15.

Untuk permintaan BountyForge atau bukti target yang cocok dengan lane Web2,
Web3, Solidity, property fuzzing, triage, maupun report, router dapat
mengaktifkan `skill/bountyforge-research-suite/SKILL.md`. Integrasi ini
mempertahankan corpus upstream pada commit terpin sebagai referensi vendored,
memuat hanya satu slice relevan, dan menempatkan semua command, installer, MCP,
payload, serta arahan subagent di belakang authorization dan execution gate
lokal. Entry `godmod` kini berupa metadata valid yang dikarantina tanpa
capability operasional, dan duplikasi Fizz tidak diaktifkan dua kali.

Untuk audit keamanan aplikasi yang sah, router dapat memilih
`skill/apex-black/SKILL.md` secara implicit berdasarkan task plus bukti surface
target; pengguna tidak perlu menyebut nama APEX BLACK. Pemilihan ini memuat
metode dan prompt-nya, tetapi tidak otomatis memberi otorisasi atau menjalankan
aksi live. Runtime di `/home/nobcoder/APEX-BLACK` hanya berinteraksi live setelah
manifest bertanda tangan lolos exact-scope gate. Hasil synthetic atau
`VULNERABILITY_VALID` belum `REPORT_READY` tanpa `TRIAGER_PROOF=PASS`.
Registry live APEX sekarang memiliki **180 capability/lens workers**, termasuk
family native media decoder, dependency/backport provenance, process-sandbox
authority, SSO identity binding, dan connected-integration authority.

Ketika bukti target menunjukkan HEIC/HEIF/AVIF atau media lain mencapai native
decoder lalu berpotensi menyeberangi worker, aplikasi, SSO/session, atau
connector, router memuat
`references/IMAGE_DECODER_SSO_CONNECTOR_CHAIN_METHOD.md`. Metode ini memisahkan
exact artifact/backport, format dispatch, memory primitive, process authority,
application authority, identity authority, connector scope, dan terminal
action. Artikel Hacktron tentang OpenAI/Discourse/libheif beserta advisory
Discourse, Debian, dan rilis libheif dipakai sebagai prior-art/patch-lineage
seed; bukan otorisasi atau resep eksploit. Menyamarkan target live sebagai CTF
atau menyembunyikan identitas target/safety signal dari agent dilarang.

Untuk agent graph yang diminta eksplisit, router mengaktifkan
`skill/offensive-research-graph-engineer/SKILL.md` bersama orchestrator
multi-agent. Modul ini membedakan dependency nyata dari urutan naratif,
menjalankan hanya ready nodes secara paralel, mengisolasi writable worktree,
menggunakan verifier dengan konteks bersih dan frozen oracle, serta membatasi
node, concurrency, retry, waktu, dan biaya. Klaim skala vendor tidak dianggap
sebagai kapasitas runtime lokal atau izin eksekusi.

Severity Low, Medium, dan High tetap provisional sampai attacker post-state dan
seluruh newly reachable protected surface diperiksa untuk edge eskalasi yang
realistis. Severity dikunci pada maksimum yang benar-benar terbukti setelah
terminal impact, falsifikasi lengkap, atau batas program/scope/safety/environment
tercatat; dampak hipotetis tidak dapat menaikkan label.

Router juga selalu memuat `references/BUGBOUNTY_INFO_ATTACK_SURFACE_CHAIN_TOOLING_METHOD.md`, sebuah sintesis orisinal dari taksonomi Attack Surface, Chains, dan Tooling BugBounty.info. Metode ini memaksa pemetaan `attack surface -> attacker position -> primitive -> bridge -> protected boundary -> impact`, membuktikan setiap edge chain pada release path yang sama, dan memilih tool hanya untuk menjawab kebutuhan bukti tertentu. Referensi ini tidak menyalin payload situs dan tidak mengizinkan scanner, fuzzer, PoC, atau subagent berjalan otomatis.

Router juga selalu mengaktifkan `skill/program-impact-boundary-gate/SKILL.md`.
Gate ini dijalankan sebelum PoC mahal dan sebelum report-ready untuk membuktikan
`starting capability -> exploit transition -> resulting capability`, current
program severity floor, intended trust/consent boundary, unauthorized protected
recipient/action, dan tidak adanya equivalent supported path. Gate juga
memeriksa waktu penerbitan authorization, retroactive-policy contract,
parent/derived credential lineage, temporal trust equivalence, serta jalur dari
primitive ke protected production consumer. Tujuh puluh keputusan Informative,
Not Applicable, dan Duplicate disimpan sebagai negative control, sedangkan dua
laporan Resolved/rewarded disimpan sebagai positive control;
alasan penutupannya dipisahkan menjadi merits, environmental mismatch,
procedural inactivity, explicit exclusion, intended behavior, atau prior
knowledge. N/A karena inactivity bukan bukti teknis.
kemiripan hanya memicu falsifikasi dan tidak otomatis membunuh kandidat baru.

Router juga selalu mengaktifkan
`skill/novel-vulnerability-hypothesis-engine/SKILL.md`. Baseline V8 ini menurunkan
hypothesis dari invariant dan assumption source code, equivalent paths,
state-machine, representation changes, resource amplification, serta
cross-feature consumers. V9 menambahkan top-level
`skill/autonomous-research-cascade-engine/SKILL.md` sebagai research-cascade
layer terpisah: objective compiler, atomic micro-inspiration, falsifiable
hypothesis factory, clean-probe classifier, generic anomaly evaluator,
target-derived permutation, anomaly ledger, shared-semantic-reuse explorer,
harness self-audit, deterministic verdict gate, dan second-order cascade.
Dalam `NOVEL_DISCOVERY_MODE=true`, pencarian prior art kerentanan diblokir sampai
hypothesis, source-to-sink, runtime effect, dan negative control terbukti.
Candidate bergerak melalui state frontier secara monotonik, memakai
`novelty_status=UNVERIFIED`, dan tidak boleh mengklaim zero-day otomatis.
`CASCADE_LEAD` menyimpan lompatan konseptual yang belum mempunyai security impact
tanpa mengubahnya menjadi finding. Validator network-free menegakkan kontrak,
termasuk harness-independent reproduction sebelum `STRONG`; blind
generalization tetap memerlukan held-out evaluator terpisah. Layer ini tidak
memuat payload HTTP Terminator atau rule teknik desync, dan secara eksplisit
melarang target switching, safety-signal masking, agent-reality deception,
credential collection, destructive proof, serta high-volume DoS.

Untuk authentication/authorization dan business logic, router juga selalu
memuat `references/AUTHORIZATION_INVARIANT_KILL_CHALLENGE.md`. Sebelum kandidat
di-KILL, metode ini mewajibkan invariant protected operation, enforcing
component, state configured/absent/nil/empty/no-op/default/unknown/error,
resource yang diotorisasi versus resource yang dipakai sink, bukti intent, dan
hasil dispatch end-to-end. `Looks intentional` atau nama helper no-op tidak
cukup. Bukti yang belum lengkap tetap hypothesis non-reportable, bukan finding
dan bukan KILL.

Untuk patch yang hanya menutup satu literal, selector/allowlist yang memeriksa
objek A tetapi consumer memakai objek B, markup yang dibangun lewat interpolasi,
atau URL importer yang divalidasi lebih sempit daripada kemampuan Git/HTTP/
package client, router memuat secara kondisional
`references/PATCH_VARIANT_CONSUMER_BOUNDARY_METHOD.md`. Metode ini menyatukan
error-domain sweep, checked-versus-consumed identity, protocol-capability
matrix, critical lifecycle propagation, closest one-variable sibling, patched
control, authoritative read-back, dan cleanup. Cosmos SDK HackerOne #3018307 /
`GHSA-x5vx-95h7-rv4p` / `GHSA-47ww-ff84-4jrg`, GitLab Kroki HackerOne #1731349 /
`CVE-2023-0050`, dan GitLab HackerOne #1685822 / issue #372165 dipertahankan
sebagai prior art public/fixed—bukan signature
sempit, temuan baru, atau izin untuk menguji chain/public worker/third-party
repository.

Untuk remote object yang membuat method/atribut dinamis, serializer yang dapat
mengambil ukuran dan byte dari representasi berbeda, import metadata yang
bertahan sampai worker, string process command, atau optional dependency yang
diam-diam menyalakan interpreter, router memuat secara kondisional
`references/DYNAMIC_DATA_EXECUTION_CONSUMER_METHOD.md`. Metode ini memaksa
method-surface inventory, same-immutable-buffer framing, attribute-provenance
matrix, strict allowlist sebelum persistence, fixed argv/data separation,
activation matrix, sandbox completeness, intermediate-versus-terminal impact,
safe sibling, dan patched control. GitLab HackerOne #1679624/#1609965/#1401444
dipertahankan sebagai prior art public/fixed, bukan payload library atau klaim
temuan baru.

Untuk workflow context yang mencampur data pengguna dengan identity/credential
engine, live CLR object dan serializer coercion, perbedaan JWT verifier lama dan
baru, rantai ACL Active Directory, beberapa lapisan request-signing mobile,
atau AI/NL-to-SQL yang memilih dataset/space sebelum database, memory, event
stream, dan signed export,
router memuat `references/CROSS_BOUNDARY_COMPOSITION_METHOD.md` secara
kondisional. Metode ini memisahkan representation ledger dari authority ledger,
mewajibkan enum member/overload/fallback atau edge ACL yang nyata, memakai
kontrol satu-variabel `S/C/P`, dan menolak status sukses, graph path, public-key
recovery, regenerasi header, jawaban AI, atau SAS URL sebagai impact tanpa
protected consumer serta authoritative read-back. HackerOne #3858504, #3861550,
dan #3800870 adalah prior art public; contoh AD/mobile/AI analytics yang
diberikan pengguna adalah seed metode, bukan izin live testing.

Untuk archive entry yang diekstrak lalu dibuka, route browser yang mencapai
delete, metadata upload yang berubah menjadi markup atau resource load,
document inline options yang memilih class/loader, atau request params yang
masuk ke namespace opsi framework, router memuat secara kondisional
`references/ARCHIVE_RENDERER_FRAMEWORK_CONSUMER_METHOD.md`. Metode ini memaksa
entry-type inventory, canonical-root dan open-time identity, browser/framework
normalization, secondary-consumer tracing, runtime-capability allowlisting,
terminal-impact separation, closest-safe sibling, dan patched control. GitLab
issues `#349524`, `#332420`, `#324452`, `#232829`, GDK issue `#1314`, dan
`CVE-2021-22238` dipertahankan sebagai public/fixed prior art. Tidak ada delete,
real file read, live SSRF, secret/metadata access, atau command execution yang
diotomatisasi.

Untuk recovery text atau stored metadata yang didecode/reparse menjadi markup,
URL/data yang masuk ke grammar configuration key, signed multipart metadata
yang kehilangan provenance setelah nested parsing, atau import attribute yang
memanggil generated/virtual setter dengan side effect, router memuat secara
kondisional `references/REPARSE_CONFIG_PROVENANCE_METHOD.md`. Metode ini
mewajibkan decode-depth dan parser ledger, validated-versus-consumed
representation, output/config grammar, exact signed carrier, ambient namespace
collision, generated-setter inventory, assignment order, terminal-impact
separation, safe sibling, dan patched control. GitLab issues `#213273`,
`#215640`, `#215212`, `#214636`, dan `#212089` / `CVE-2020-10956` adalah
public/fixed prior art. Tidak ada live XSS/SSRF, real file read, special-path
enumeration, metadata access, credential access, atau destructive test yang
diotomatisasi.

Untuk path/reference yang ditangkap regex lalu dibuka/disalin, ref/path operand
yang dapat masuk ke option grammar child process, mode yang memperluas working
directory/object namespace, atau markup tersanitasi yang diaktifkan oleh
JavaScript gadget bawaan aplikasi, router memuat secara kondisional
`references/PATH_CLI_GADGET_CHAIN_METHOD.md`. Metode ini mengikat validasi ke
canonical object, argv token, atau final DOM yang benar-benar dikonsumsi;
menyapu seluruh subcommand/scope/renderer/gadget; dan memisahkan primitive
file/DOM dari secret, signing/authentication, serializer/gadget, serta terminal
RCE/account impact. GitLab issue `#212175`, Gitaly issues `#1801`, historical
`#1799`, historical GitLab FOSS issue `#65335`, dan Gitaly issue `#1892` adalah
public/fixed prior art. Tidak ada traversal, protected-file access, flag
payload, cookie forging, unsafe deserialization, SSH/internal API, live XSS,
destructive action, race/flood, atau DoS yang diotomatisasi.

Untuk kandidat yang dampaknya baru muncul setelah beberapa primitive, parser, agent, origin, recovery flow, credential, atau service dikomposisikan, router mengaktifkan `compositional-exploit-chain-hunter`. Skill ini memetakan representation gap, authority bridge, soft-versus-hard controls, confused deputy antar-agent/service, parser-to-consumer differential, SSRF-to-workload-identity, recovery-channel takeover, dan web-origin-to-RCE. Pattern atlas-nya berasal dari analisis orisinal terhadap riset publik Zenity, PwnAI XSS2Shell, HackerOne #341876, dan indeks prior-art Immunefi; payload publik tidak disalin dan reproduksi publik tidak dianggap temuan baru.

Untuk signed-but-readable client state yang membawa credential atau objek
terserialisasi, dugaan secret reuse lintas trust role, review pasif atas traffic
atau source yang sudah dikumpulkan, serta kampanye sistem panjang yang harus
berakhir pada protected terminal oracle, router memuat
`evidence-to-terminal-oracle-bug-bounty`. Metode ini memisahkan representation,
authority, state-machine, reliability, dan terminal proof; setiap edge harus
memiliki baseline, negative control, provenance, serta capability delta.
`prompts/HERMES_PASSIVE_EVIDENCE_ANALYST.md` memberi Hermes peran analisis pasif
saja: ia boleh meranking lead tetapi tidak boleh menyentuh target live,
menjalankan payload, atau mempromosikan hipotesis menjadi temuan. Seluruh nama
vendor, reward, tanggal, flag, CVE, dan klaim “pertama” dari corpus pengguna
disimpan sebagai prior art yang belum diverifikasi independen.

Untuk ledger, node, payment engine, bridge, atau smart contract yang memakai
bounded arithmetic pada state transition sekaligus invariant pengamannya,
router memuat `references/CONSENSUS_ACCOUNTING_INVARIANT_CHAIN_METHOD.md`.
Metode ini memulai dari konservasi matematis arbitrary-precision, lalu
membandingkan domain producer dan checker, continuous transaction flow,
rollback, exact release-binary semantics, commit/finality, spendability, serta
feature/amendment dan validator cohort. Standalone/localnet bukan otomatis
bukti mainnet. Corpus XRPL/rippled yang diberikan pengguna dipertahankan sebagai
prior art belum terverifikasi; konstanta transaksi dan PoC tidak dijadikan
default pengujian atau izin public-network execution.

Untuk HackerAI, HexStrike AI, platform AI pentest eksternal, security MCP
server, agent skill pack, atau autonomous scanner orchestrator, router memuat
`external-ai-security-tool-governor`. Skill ini memisahkan knowledge,
orchestration, execution broker, isolated worker, dan append-only evidence;
mem-pin repository/commit/license; serta membedakan klaim upstream, fakta source
yang diperiksa, inference, dan perilaku yang benar-benar divalidasi. Status
default adalah `REFERENCE_ONLY`. Tidak ada clone, install, dependency setup,
MCP registration, server startup, scanner/tool execution, cloud resource,
credential, target interaction, atau external evidence egress yang dilakukan
atau diotorisasi oleh penambahan referensi ini.

Untuk metodologi agentic vulnerability research, finding quarantine atau
"hallucination bin", knowledge loop, dan harness yang menggabungkan MCP,
scanner, RE, fuzzer, debugger, atau model, router memuat
`agentic-security-research-harness`. Katalognya mem-pin dua artikel Andy Gill
serta Harness Kit, RAPTOR, Defending Code Reference Harness, Baby Naptime,
evilsocket Audit, Visa VVAH, Anthropic OSS Scanner, Sequester
bug-bounty-triage, dan REA. Setiap lead dimulai sebagai
`HYPOTHESIS_QUARANTINED` dan hanya dapat dipromosikan melalui clean snapshot,
primitive konkret, low-privilege reachability, impact gate, manual confirmation,
dan `TRIAGER_PROOF=PASS`. Demotion, negative results yang terikat target/rilis,
RAG provenance/expiry, session revocation, context budget, dan ROI setelah
eligibility adalah bagian eksplisit dari metode. Semua sumber tetap
`REFERENCE_ONLY`; tidak ada install, MCP registration, scanner/RE execution,
model/cloud call, target interaction, atau subagent yang diotorisasi.

Untuk WebHackList dan board `2026-ai`, router memuat
`webhacklist-2026-research-corpus`. Catalog lokal mengikat commit resmi
`2f17d6249c178f9b895d2c00536a3009df117afa`, 299 record, 298 arsip Markdown
yang dibaca byte penuh, dan satu primary URL yang dibaca melalui indexed
render karena direct fetch menghasilkan HTTP 403. Status koleksi tetap
preliminary, unranked, AI-collected, incomplete, not community-vetted, dan
`REFERENCE_ONLY`. Record-level family adalah routing hint, bukan novelty
judgment, duplicate proof, finding, atau izin menjalankan command/PoC artikel.

Untuk WordPress XSS2Shell `CVE-2026-64638` /
`GHSA-52p2-r8wf-jcrf`, paket memuat metode seven-boundary yang memisahkan
parser differential pada login, structural DOM, automatic core gadget,
REST JSONP/SOME, Application Password approval, REST content authority,
upload/extraction, dan direct PHP execution. Status resminya dipertahankan
sebagai `High 8.9` dengan high attack complexity dan active user interaction:
entry XSS bersifat pre-auth, tetapi terminal chain bukan zero-click atau purely
unauthenticated RCE. Metode mencakup exact branch/backport matrix, W0-W7 local
proof ladder, detection-confidence correlation, incident response, hardening,
serta pemisahan dari WP2Shell. Exact public lineage adalah fixed duplicate;
tidak ada scan situs, klik admin nyata, pengumpulan credential, shell, atau
persistence yang berjalan otomatis.

Untuk GraphQL/REST open filter, Mongo-like query object, `sift`, `$where`, `new Function`, atau predicate compiler, router mengaktifkan `dynamic-filter-evaluator-rce-hunter`. Metode ini memisahkan schema openness, raw-object forwarding, operator semantics, runtime gate, anonymous/resolver authorization, deterministic non-empty trigger, output channel, process authority, dan secret-to-capability impact. Taskcluster `GHSA-ccv5-c45x-2q38` / `CVE-2026-11892` diperlakukan sebagai prior art yang sudah diperbaiki di 100.3.0, bukan temuan baru atau payload untuk target live.

Untuk Ruby heredoc, generated JavaScript/shell/Python/PowerShell, Playwright wrapper, temporary script, `Open3.capture3`, atau runtime lain yang mengubah untrusted data menjadi source code, router mengaktifkan `cross-language-script-injection-hunter`. Metode ini memisahkan principal/policy, semantic validation, target-language grammar, emitted source, parse-clean execution, child-runtime authority, dan typed-data remediation. `ai-scanner` `GHSA-r27j-xxgx-f5vr` / `CVE-2026-41512` diperlakukan sebagai prior art yang sudah diperbaiki di 1.4.1; payload live dan secret harvesting tidak menjadi otomatisasi.

Untuk repeated tokens/characters, tokenizer boundary, instruction blackout, model divergence, memorization, atau repetition-filter gap, router mengaktifkan `llm-tokenization-boundary-hunter`. Metode ini memaksa pemetaan bytes → normalization → token IDs → prompt roles → model/router/filter → tool/RAG/policy/backend, matched token-budget controls, repeated trials, dan protected-boundary proof. `dropbox/llm-security` diperlakukan sebagai repository eksperimen dan prior art historis—bukan backend produksi, scanner, atau bukti bahwa model saat ini masih rentan. Harness token-search dan ekstraksi data tidak dijalankan otomatis.

Untuk credential yang terekspos atau hard-coded di source, Git history, CI log,
artifact, dokumentasi, ticket, Slack/Teams/chat, notebook, package, screenshot,
atau support bundle, router mengaktifkan
`credential-exposure-capability-hunter`. Metode ini memisahkan artifact audience,
credential type, current validity, principal, declared scope, effective
permissions, protected capability, revocation, artifact cleanup, dan residual
copies. Untuk Docker/OCI, bukti wajib mengikat tag yang mutable ke platform,
manifest/image/layer digest yang immutable dan exact in-layer path; lower layer,
multi-platform variant, registry cache/mirror, serta clean rebuild diperiksa
terpisah. Untuk OAuth/bearer admin API, bukti diikat ke exact instance,
environment, endpoint/action, OAuth scope, role permission, dan data class;
successful read tidak dianggap bukti write/delete, dan PII memicu
`PII_EXPOSED_STOP`. HackerOne #2467999, HackerOne #2137154, dan laporan historis Mozilla Common Voice tentang
dua AWS access-key pair plus database credentials di image Docker Hub
diperlakukan sebagai prior art yang resolved dan sebagai scope exception: bounty
diskresioner atau pernyataan “will be included” bukan preseden/current scope. Raw credential, image pull, AWS/database
replay, resource enumeration, dan mutation tidak menjadi bagian otomatis dari
PoC.

Untuk credential dalam public CI log, metodologi mengikat bukti ke exact
provider/task/run/job/step, raw versus rendered log, audience, timestamp,
retention/cache/mirror, dan command/configuration yang mengeluarkan secret.
Laporan historis “Netlify Authentication Token Exposed in Public Mozilla CI
Logs” diperlakukan sebagai prior art resolved tanpa mengarang report ID:
Taskcluster adalah carrier log, sedangkan boundary yang terpengaruh adalah token
Netlify ber-role `Developer` dengan `site_access: selected` pada site
`crash-pings.mozilla.org`. `roles_allowed` bukan role yang dimiliki;
function-list `GET` bukan bukti upload/deploy/execute; dan function yang benar-
benar berhasil dideploy berjalan pada runtime Netlify, bukan otomatis RCE pada
Taskcluster atau server Mozilla. Bounty/bonus out-of-scope tetap bukan preseden.

Untuk V8/Gin, Blink, Electron, Node/N-API, WebView, renderer, atau binding
JavaScript-to-native lain, router mengaktifkan
`native-js-binding-lifetime-hunter` hanya bila ada bukti bahwa objek/function
JavaScript dapat tetap reachable sementara native receiver dapat dihancurkan
oleh GC, context/frame teardown, navigation, disconnect, atau owner loss.
Metode ini memisahkan object graph JavaScript dan ownership graph native,
memeriksa property descriptor dan konfigurasi feature/provider, serta meminta
ASan/HWASan allocation-free-use stacks dengan baseline, negative control, dan
patched control. Laporan Brave “UAF on JSEthereumProvider” diperlakukan sebagai
prior art yang sudah diperbaiki melalui brave-core PR #18411/commit `a8e497b`;
tidak ada HackerOne report ID yang dikarang. Renderer crash/UAF tidak dianggap
renderer RCE atau sandbox escape.

Untuk GitHub Actions yang memproses fork PR, `pull_request_target`,
`workflow_run`, artifact/caches tak tepercaya, local action, atau npm lifecycle
script, router mengaktifkan `github-actions-fork-trust-hunter`. Metode ini
memisahkan provenance workflow, code/data, execution, dan authority; membedakan
step-scoped secrets dari `github.token`, checkout-persisted Git credentials,
OIDC, serta runner residue; dan mewajibkan effective runtime permission sebelum
mengklaim repository write atau supply-chain compromise. Ia juga memeriksa
write-then-execute lintas step: fork code yang berjalan lebih awal dapat
memodifikasi trusted-path script/dependency/tool di workspace yang sama sebelum
step berikutnya mengeksekusinya dengan secret.

Dua laporan publik DuckDuckGo 2026 dipertahankan secara presisi. Pada
privacy-configuration, primitive yang divalidasi vendor adalah fork
`npm postinstall` yang dapat menjangkau `GITHUB_TOKEN` yang dipersist oleh
`actions/checkout@v5`, bukan akses ambient ke PAT/Asana secrets. Pada HackerOne
#3619287 content-scope-scripts, callback mendukung fork runner RCE; key Anthropic
tidak ambient ke build step, tetapi source menunjukkan kandidat cross-step
workspace bridge ke `base/.github/scripts/semver-analysis.mjs` yang kemudian
dijalankan dengan key. Callback tanpa secret tidak dianggap bukti key theft.
Kemampuan label juga tidak otomatis berarti merge, poisoned release, atau
kompromi semua browser. PR #5002/PR #2659 tetap patch/prior-art evidence, bukan
pengganti exact runtime proof. Tidak ada fork PR, OAST, token extraction, vendor
mutation, release, atau deployment yang dijalankan otomatis.

Untuk deadlock, lock-order inversion, circular wait, recursive logging lock,
thread-dump freeze, atau RPC-triggered node/service paralysis, router
mengaktifkan `deadlock-lock-graph-dos-hunter`. Metode ini membedakan deadlock,
self-deadlock, livelock, starvation, resource exhaustion, slow path, dan crash;
mewajibkan static lock-order graph plus runtime wait-for graph; dan memverifikasi
official binary, build definitions, platform, log configuration, listener
exposure, minimum bounded trigger, recovery, state integrity, serta patched
control. Monero HackerOne #3307874 dipertahankan sebagai public/fixed prior art
yang diperbaiki lewat PR #10065/#10066 dan v0.18.4.3. Klaim satu request, semua
OS/release, permanen, DB corruption, confidentiality loss, dan CVSS 10 tidak
diwariskan tanpa bukti baru. Flood, adaptive batch, compression amplification,
header spoofing, rate-limit bypass, dan public-node DoS tidak dijalankan otomatis.

## Standar wajib

- Authorization, scope, rules of engagement, rate limit, dan exclusions diperiksa lebih dahulu.
- Repository/source harus dipetakan ke deployment, mainnet, package, artifact, atau stable release nyata.
- Prior art diperiksa melalui issues, PRs, advisories, CVEs, changelog, commits, release notes, docs, dan duplicate families; dalam novelty mode pemeriksaan kerentanan ini baru dibuka setelah proof gate embargo.
- Trace wajib end-to-end: attacker input -> parser/canonicalization -> validation -> state/cache/serialization -> auth/signature/policy -> privilege transition -> sensitive sink -> impact.
- Gunakan akun/data/artifact/infrastruktur milik peneliti, harmless canary, baseline, negative control, state before/after, dan cleanup.
- Scanner dan AI hanya menghasilkan hipotesis, bukan bukti.
- Chain hanya sah jika setiap edge terbukti pada deployment/release path nyata yang sama; temuan teoritis yang tidak terkait tidak boleh digabung untuk menaikkan severity.
- Kandidat teknis hanya dapat dipertahankan bila `program-impact-boundary-gate`
  membuktikan capability delta nonzero melintasi boundary yang diakui program
  dan memenuhi severity floor saat ini. Localhost/synthetic PoC atau patched
  control saja tidak cukup.
- Verdict: **STRONG / MEDIUM / WEAK / KILL**. Jika tidak ada yang bertahan: **NO VALID FINDING**.

## Multi-agent audit — auto-on for bug bounty (any runtime)

- `codex-cli-multi-agent-audit-orchestrator` — orkestrasi role-separated untuk Cursor, Codex CLI, Claude Code, Gemini, atau runtime lain. Nyala sendiri saat bug bounty, VRP, HackerOne/Bugcrowd/Intigriti, atau hunt kerentanan yang sah. Tidak perlu dipanggil. Lewati kerja produk/UI biasa. Prefix `codex-cli-` adalah id routing, bukan syarat Codex.
- `prompts/MASTER_PROMPT_CODEX_CLI_MULTI_AGENT_AUDIT.md` — prompt utama discovery-versus-verification.
- `references/CODEX_CLI_MULTI_AGENT_WORKFLOW.md` — handoff stages, correlated-error controls, dan human reproduction gate.
- `references/ADAPTIVE_RESEARCH_PATH_ORCHESTRATION_METHOD.md` — registry jalur, first-wave A/B/C, anti-convergence, adaptive second wave 0–3 specialist, primitive-to-impact chain, exact dependency/runtime source escalation, dan termination rule.
- `config/CODEX_CLI_RESEARCH_PATH_REGISTRY_SCHEMA.json` — schema status dan genealogy coverage setiap attack surface, wave, convergence check, serta termination decision.
- `config/CODEX_CLI_ADAPTIVE_EXECUTION_PROVENANCE_SCHEMA.json` — schema bukti spawn nyata, child/session ID unik, input/output terpisah, dan konsumsi output oleh root.
- `config/CODEX_CLI_CANDIDATE_SCHEMA.json` — schema kandidat v10 yang menambahkan research path, discovery wave, root-cause family, primitive chain, dan exact implementation binding di atas seluruh proof gate target-native V9.
- `automation/init-codex-cli-audit-workspace.py` — hanya membuat scaffold lokal; tidak menjalankan Codex, jaringan, scanner, fuzzer, atau PoC.
- `automation/validate-adaptive-research-orchestration.py` dan `automation/test-adaptive-research-orchestration.py` — validator serta 15 regression deterministik untuk kontrak orkestrasi adaptif.
- `automation/validate-adaptive-execution-provenance.py` dan `automation/test-adaptive-execution-provenance.py` — derivasi provenance dari persisted Codex rollout serta sepuluh regression fail-closed untuk execution plane V11. Stream `codex exec --json` disimpan untuk diagnostik, tetapi persisted rollout adalah evidence authority ketika stream tersebut menghilangkan event multi-agent.
- `automation/run-v11-adaptive-execution-smoke.py` — acceptance test sintetis yang benar-benar meminta satu child Codex, mengikat root thread ID ke persisted rollout, menyalin child rollout, dan memvalidasi output terpisah serta receipt root sebelum blind benchmark.

Prinsip utama: discovery mengoptimalkan recall, verification mengoptimalkan precision, agent consensus bukan bukti, dan reproduksi manual tetap menjadi sumber kebenaran. Untuk authorization, audit wajib memetakan `subject + action + target resource + tenant/org + object state` serta memastikan target identifier benar-benar mencapai policy engine atau downstream filter.

## Skill expert baru

- `expert-bug-hunter` — orkestrasi bug hunter expert lintas source, web/API, mobile, desktop, cloud, CI/CD, Web3, dan release.
- `expert-authorized-hacker` — adversarial systems thinking dengan batas izin yang keras.
- `expert-source-code-bug-hunter` — repo-to-production tracing dan source audit mendalam.
- `expert-web-api-business-logic-hunter` — BAC/IDOR, tenant isolation, workflow, async jobs, dan financial logic.
- `expert-authentication-authorization-hunter` — identity, session, OAuth/OIDC/SAML, capability, revocation, dan role/tenant boundaries.
- `expert-race-condition-state-machine-hunter` — race, TOCTOU, replay, idempotency, distributed state, dan business invariants.
- `expert-cache-proxy-parser-differential-hunter` — cache/CDN/proxy/routing/canonicalization/parser differential.
- `expert-cloud-ci-cd-supply-chain-hunter` — cloud IAM, workflows, runners, secrets, artifacts, signing, provenance, release, dan updater.
- `expert-mobile-client-hunter` — Android/iOS, deep links, exported components, WebView/native bridge, storage, dan backend trust.
- `expert-crypto-signature-protocol-hunter` — signature, nonce, replay, canonicalization, key lifecycle, transaction/message integrity.
- `expert-ai-model-bug-bounty-auditor` — audit AI model/API/agent/RAG/tool/memory/sandbox/model-supply-chain dengan hard gate yang membedakan security bug dari jailbreak atau quality issue.
- `autonomous-research-cascade-engine` — V9 target-native research loop dengan micro-inspiration, generic anomaly evaluation, clean-probe semantics, shared-component domain comparison, harness-independent reproduction, deterministic verdict, dan provenance-preserving second-order cascades.
- `codex-cli-multi-agent-audit-orchestrator` — V11 orchestration layer yang nyala sendiri saat bug bounty/VRP, mempertahankan V10 research controls, dan menambahkan real-spawn enforcement, unique specialist/session identity, separate output, root-consumption receipt, serta transcript-derived provenance.
- `compositional-exploit-chain-hunter` — audit chain lintas agent, parser, origin, auth/recovery, cloud identity, dan execution consumer dengan bukti per-edge serta hard duplicate gate.
- `dynamic-filter-evaluator-rce-hunter` — audit GraphQL/REST open filter dan query DSL yang dapat memilih executable operator, dengan principal/liveness/output/runtime gates serta safe canary.
- `cross-language-script-injection-hunter` — audit satu runtime yang menghasilkan source untuk runtime lain, dengan grammar/policy/artifact/interpreter gates dan typed-data remediation.
- `llm-tokenization-boundary-hunter` — audit repeated-token/tokenizer effects hanya ketika terhubung ke tool, RAG, tenant, authorization, confidentiality, atau privacy boundary yang benar-benar terbukti.
- `credential-exposure-capability-hunter` — audit exposed/hard-coded credentials dari artifact yang diakses secara sah, termasuk Docker/OCI image/layer, sampai principal dan effective capability terbukti dengan metode minimum-impact, lalu prioritaskan credential rotation, artifact purge, dan residual-copy review.
- `evidence-to-terminal-oracle-bug-bounty` — mengubah lead signed client state, secret reuse, unsafe deserialization, passive evidence review, atau exploit state machine menjadi verdict berbukti melalui edge ledger, one-variable controls, reliability accounting, dan protected terminal oracle.
- `external-ai-security-tool-governor` — mengintegrasikan HackerAI, HexStrike AI, dan platform keamanan AI/MCP eksternal sebagai sumber metodologi yang dipin dan inert; menegakkan license/provenance review, five-plane isolation, typed deny-by-default broker, per-call authorization, dan status `REFERENCE_ONLY` sebelum ada izin runtime terpisah.
- `agentic-security-research-harness` — mendesain dan mengaudit research harness berbasis finding quarantine, append-only promotion/demotion, clean-snapshot dan low-privilege proof, independent verifier, provenance-bound RAG, persistent-session capability control, context/cost budget, serta manual dan triager-proof gates; seluruh upstream tetap reference-only.
- `webhacklist-2026-research-corpus` — memakai seluruh 299 record preliminary pada board WebHackList 2026 AI sebagai ledger prior-art dan seed metodologi yang dipin; memisahkan metadata match dari primary-source verification, disclosure cutoff, current-release reachability, impact, dan report readiness, tanpa menyalin atau menjalankan PoC sumber.
- `native-js-binding-lifetime-hunter` — audit lifetime mismatch pada V8/Gin dan binding JavaScript-to-native lain dengan object/ownership graph, configuration matrix, sanitizer proof, serta hard crash-versus-RCE boundary.
- `chromium-v8-variant-hunter` — audit variant Chromium/V8 berbasis patch publik dengan equality/hash/cache/copy completeness matrix, protected-consumer trace, differential state pair, current-release gate, dan historical-root exclusion.
- `github-actions-fork-trust-hunter` — audit fork-to-runner GitHub Actions dengan provenance empat lapis, exact credential channel, effective token authority, G0-G6 proof ladder, dan hard runner-RCE-versus-supply-chain boundary.
- `deadlock-lock-graph-dos-hunter` — audit deadlock/RPC availability dengan build/configuration gate, lock-order dan wait-for graph, D0-D7 evidence ladder, bounded local controls, serta hard availability-versus-integrity/confidentiality boundary.


## Expert programming, reverse engineering, dan Windows internals baru

### Bahasa pemrograman

- `expert-python-engineer`
- `expert-javascript-typescript-engineer`
- `expert-go-engineer`
- `expert-rust-engineer`
- `expert-c-cpp-engineer`
- `expert-java-kotlin-engineer`
- `expert-dotnet-csharp-engineer`
- `expert-php-ruby-engineer`
- `expert-shell-powershell-engineer`
- `expert-sql-database-engineer`

Semua skill bahasa bekerja pada runtime/toolchain, build/package, concurrency, serialization, testing, deployment artifact, supply chain, dan security boundary nyata—bukan sekadar sintaks.

### Reverse engineering dan Windows internals

- `expert-reverse-engineer`
- `expert-windows-internals-vulnerability-researcher`

Keduanya mencakup PE/ELF/Mach-O/managed bytecode, static dan dynamic analysis, debugger, patch diff, ABI/calling convention, symbol provenance, token/impersonation, Object Manager, registry hives, NTFS/reparse points/oplocks, minifilters, Defender, WinRE, BitLocker, dan layanan/driver berprivilege. Analisis wajib dilakukan di lab terisolasi dan tidak boleh diubah menjadi malware atau eksploit operasional.

### Repository-specific authorized offensive skills

The following legacy `*-defensive-researcher` names remain unchanged for route
and discovery compatibility, but their operating posture is now adversarial
exploitability-first inside isolated authorized labs:

- `legacyhive-defensive-researcher`
- `greatxml-defensive-researcher`
- `redsun-defensive-researcher`
- `miniplasma-defensive-researcher`
- `yellowkey-defensive-researcher`
- `bluehammer-defensive-researcher`
- `undefend-defensive-researcher`
- `greenplasma-defensive-researcher`
- `rogueplanet-defensive-researcher`

Repository publik tersebut diperlakukan sebagai **prior art** dan bahan root-cause/patch/detection research. Reproduksi PoC publik saja otomatis bukan temuan baru. Kandidat hanya dipertahankan bila membuktikan root cause berbeda, patch bypass, sibling path, current-release reachability yang baru, atau security boundary terpisah.

## Skill yang ditingkatkan menjadi expert

- `ai-assisted-bug-bounty-orchestrator`
- `api-security-reviewer`
- `authorized-black-box-web-tester`
- `authorized-reconnaissance-operator`
- `authorized-offensive-tool-loop`
- `authorized-red-team-planner`
- `authorized-universal-jailbreak-evaluator`
- `bug-bounty-auditor`
- `bug-bounty-triage`
- `program-impact-boundary-gate`
- `executable-binary-auditor`
- `executable-rce-hunter`
- `patch-diff-root-cause-analyzer`
- `secure-code-reviewer`
- `security-automation-tool-installer`
- `software-engineer-copilot`
- `wallet-node-bridge-reviewer`
- `web-target-auditor`
- `web3-smart-contract-auditor`

## Master prompt expert

- `prompts/CHROMIUM_V8_VARIANT_HUNTER.md`
- `prompts/MASTER_PROMPT_MANDATORY_AUTO_ROUTER.md`
- `prompts/MASTER_PROMPT_CODEX_CLI_MULTI_AGENT_AUDIT.md`
- `prompts/MASTER_PROMPT_AI_BUG_BOUNTY.md`
- `prompts/MASTER_PROMPT_PROGRAM_IMPACT_BOUNDARY_GATE.md`
- `prompts/MASTER_PROMPT_AUTHORIZED_UNIVERSAL_JAILBREAK_EVAL.md`
- `prompts/MASTER_PROMPT_EXECUTABLE_RCE_AUDIT.md`
- `prompts/MASTER_PROMPT_EXPERT_AUTHORIZED_HACKER.md`
- `prompts/MASTER_PROMPT_EXPERT_AUTH_IDENTITY.md`
- `prompts/MASTER_PROMPT_EXPERT_BUG_HUNTER.md`
- `prompts/MASTER_PROMPT_EXPERT_CLOUD_SUPPLY_CHAIN.md`
- `prompts/MASTER_PROMPT_EXPERT_SOURCE_CODE_AUDIT.md`
- `prompts/MASTER_PROMPT_EXPERT_STATE_RACE_CACHE_PARSER.md`
- `prompts/MASTER_PROMPT_EXPERT_WEB_API_BUSINESS_LOGIC.md`
- `prompts/MASTER_PROMPT_EXPERT_AI_MODEL_AUDIT.md`
- `prompts/MASTER_PROMPT_EXPERT_PROGRAMMING_LANGUAGES.md`
- `prompts/MASTER_PROMPT_EXPERT_REVERSE_ENGINEERING.md`
- `prompts/MASTER_PROMPT_EXPERT_WINDOWS_INTERNALS_RESEARCH.md`
- `prompts/MASTER_PROMPT_NIGHTMARE_ECLIPSE_DEFENSIVE_ANALYSIS.md`
- `prompts/MASTER_PROMPT_NATIVE_JS_BINDING_LIFETIME.md`
- `prompts/MASTER_PROMPT_GITHUB_ACTIONS_FORK_TRUST.md`
- `prompts/MASTER_PROMPT_DEADLOCK_LOCK_GRAPH_DOS.md`
- `prompts/MASTER_PROMPT_EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY.md`
- `prompts/HERMES_PASSIVE_EVIDENCE_ANALYST.md`

## Referensi inti

- `references/CODEX_CLI_MULTI_AGENT_WORKFLOW.md`
- `references/EXPERT_CORE_PROTOCOL.md`
- `references/EXPERT_SCOPE_REACHABILITY_CHECKLIST.md`
- `references/EXPERT_CANDIDATE_LEDGER.md`
- `references/EXPERT_TEST_DESIGN_MATRIX.md`
- `references/EXPERT_AI_MODEL_AUDIT_MATRIX.md`
- `references/EXPERT_PROGRAMMING_LANGUAGE_MATRIX.md`
- `references/WINDOWS_EXPLOIT_RESEARCH_SAFETY_PROTOCOL.md`
- `references/NIGHTMARE_ECLIPSE_REPOSITORY_MAP.md`
- `references/EVIDENCE_TO_TERMINAL_ORACLE_BUG_BOUNTY_METHOD.md`
- `references/CONSENSUS_ACCOUNTING_INVARIANT_CHAIN_METHOD.md`
- Evidence worksheets khusus black-box, executable/RCE, dan AI safety tetap tersedia.

## Urutan penggunaan yang disarankan

1. Mulai wajib dengan `AUTOLOAD.md` atau `mandatory-auto-router`; router kemudian mengaktifkan `expert-bug-hunter` dan core pack secara otomatis. Multi-agent tetap nonaktif kecuali diminta secara eksplisit.
2. Terapkan `EXPERT_SCOPE_REACHABILITY_CHECKLIST.md`.
3. Pilih skill spesialis sesuai target dan attack surface. Gabungkan skill bahasa sesuai runtime aktual. Untuk binary gunakan `expert-reverse-engineer`; untuk Windows service/driver/Defender/WinRE gunakan `expert-windows-internals-vulnerability-researcher`; untuk model API, agent, RAG, tool use, connector, memory, multimodal, inference hosting, atau model supply chain gunakan `expert-ai-model-bug-bounty-auditor`.
4. Simpan setiap kandidat di `EXPERT_CANDIDATE_LEDGER.md`.
5. Rancang baseline, candidate test, negative control, abort condition, dan cleanup memakai `EXPERT_TEST_DESIGN_MATRIX.md`.
6. Jalankan `program-impact-boundary-gate` dan tolak kandidat tanpa capability
   delta nyata, program-recognized boundary, atau severity eligibility.
7. Gunakan triage keras. Jangan mempertahankan teori, best-practice-only, dev/test-only, by-design, known, public, duplicate, atau impact yang tidak konkret.
8. Berhenti pada technical evidence handoff setelah verdict dan remediation/test guidance.

## Automation

Untuk membuat scaffold audit lokal Codex CLI tanpa menjalankan Codex atau aktivitas jaringan:

```bash
python automation/init-codex-cli-audit-workspace.py --root /path/to/target-repo --dry-run
python automation/init-codex-cli-audit-workspace.py --root /path/to/target-repo
```

Installer tidak otomatis menjalankan scan. Recon aktif membutuhkan allowlist, batas rate/concurrency, dan flag authorization eksplisit.

```bash
chmod +x automation/install-authorized-blackbox-tools.sh
./automation/install-authorized-blackbox-tools.sh

./automation/init-blackbox-workspace.sh --name example-program --scope scope.txt

./automation/authorized-recon.sh \
  --domain example.com \
  --scope scope.txt \
  --mode passive
```

Active low-touch mode hanya dipakai bila program mengizinkan:

```bash
./automation/authorized-recon.sh \
  --domain example.com \
  --scope scope.txt \
  --mode all \
  --rate 5 \
  --concurrency 5 \
  --i-am-authorized
```

## Safety boundary

Jangan gunakan paket ini untuk unauthorized access, phishing, credential theft, spraying/brute force, malware, persistence, stealth/evasion, destructive action, DoS, third-party pivoting, public malicious package/update, atau pencurian data/aset. Pengujian harus dibatasi pada aset, akun, data, dan metode yang diizinkan.
