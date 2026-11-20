---
name: gtm-recon
description: "During authorized bug bounty JavaScript reconnaissance, extract public Google Tag Manager IDs and analyze gtm.js for hidden subdomains, API endpoints, auth URLs, dataLayer config, and possible sensitive strings. Use when a site loads GTM-, googletagmanager, or gtm.js. A GTM ID or URL is not itself a vulnerability."
---

# GTM recon

Google Tag Manager memuat tag dan skrip JavaScript tanpa mengubah kode utama
situs. File `gtm.js` yang publik kadang menyebut subdomain, endpoint API,
konfigurasi, URL tersembunyi, atau string yang terlihat sensitif. Gunakan
skill ini pada situs yang sudah masuk cakupan program. ID GTM memang sengaja
publik. Menemukannya, atau menemukan sebuah URL di dalamnya, belum berarti
menemukan kerentanan.

## Langkah

1. Ambil HTML sumber dari aset yang masuk cakupan. Cari `GTM-`.
2. Unduh JavaScript publik untuk setiap ID:

```bash
curl -sL "$TARGET" | grep -oE 'GTM-[A-Z0-9]+' | sort -u
curl -sSL "https://www.googletagmanager.com/gtm.js?id=GTM-ID" -o gtm.js
```

Ganti `GTM-ID` dengan ID milik target. Jangan memakai ID contoh sebagai target.
Catat URL aset sumber, waktu pengambilan, GTM ID, URL `gtm.js`, dan SHA-256
artefak agar hasil dapat direproduksi. Jangan mengambil HTML atau JavaScript
dari host lain hanya karena namanya muncul di GTM.

3. File ini biasanya diminifikasi dan string-nya ter-escape. Pretty-print
   sebelum mencari. Indikator yang dicari:

`api`, `/api/`, `/graphql`, `admin`, `internal`, `staging`, `dev`, `token`,
`secret`, `authorization`, `webhook`

4. Keluarkan URL, lalu periksa ulang hasilnya:

```bash
grep -oE 'https?://[^"[:space:]\\]+' gtm.js | sort -u
```

5. Kelompokkan temuan menjadi subdomain tersembunyi, endpoint API, URL
   autentikasi, konfigurasi JavaScript, kredensial yang tertulis langsung,
   dan isi `dataLayer`.
6. Korelasikan dengan JavaScript situs, request di Burp atau tab Network,
   serta alur autentikasi dan otorisasi aplikasi. Domain yang hanya disebut
   belum terbukti hidup dan belum tentu masuk cakupan.
   URL layanan pihak ketiga tetap konteks saja kecuali program secara eksplisit
   memasukkannya ke scope. Verifikasi scope sebelum mengirim request aktif ke
   setiap subdomain atau endpoint yang baru ditemukan.
7. Validasi hanya di aset yang program mengizinkan, dengan akun pengujian
   milik sendiri, pengujian yang minimal dan tidak merusak, lalu bukti
   dampak. Ikuti `valid-bug-hunt`: sebuah string di GTM tetap
   `HYPOTHESIS_QUARANTINED` sampai ada bukti end-to-end.

Untuk kerja terdelegasi gunakan role
`agents/gtm-recon-analyst.md`. Role ini hanya menganalisis artefak yang sudah
diambil dari aset in-scope dan tidak boleh mengesahkan vulnerability. Gunakan
`references/evidence-schema.md` ketika hasil akan diteruskan ke lane validasi
atau `security-review`.

## Yang dicari dan untuk apa

- Subdomain tersembunyi memperluas permukaan yang harus dicek terhadap
  cakupan.
- Endpoint API menunjukkan fungsi yang perlu ditinjau.
- URL autentikasi menjelaskan alur login dan otorisasi.
- Konfigurasi JavaScript dapat menunjukkan pengaturan yang sensitif.
- Kredensial yang tertulis langsung hanya indikasi kebocoran sampai
  terbukti masih berlaku dan berdampak.
- `dataLayer` menunjukkan data yang diproses tag dan skrip.

Nilai teknik ini adalah memperluas pemahaman attack surface, lalu membuktikan
kelemahan yang benar-benar berdampak. Jangan melaporkan GTM ID, endpoint, atau
subdomain sebagai temuan hanya karena muncul di `gtm.js`.
