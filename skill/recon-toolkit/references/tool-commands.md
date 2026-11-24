# Recon tool commands

One command shape per tool. The script or the operator fills `URL`, `HOST`,
and `DOMAIN` from the scope file. Do not raise the thread, rate, or list size
shown here. A hit is inventory until a hunt skill proves impact.

Wildcard inventory stays in `wildcard-scope-recon` and
`scripts/wildcard-recon.sh`. Use the commands below when that pipeline is the
wrong tool, or when one named tool is the next step.

## Names

```bash
subfinder -silent -d "$DOMAIN" -o subfinder.txt
assetfinder --subs-only "$DOMAIN"
/usr/lib/amass/amass enum -d "$DOMAIN" -silent -rigid -timeout 2 -dir amass-dir
findomain -t "$DOMAIN" -q -u findomain.txt
```

Call `/usr/lib/amass/amass`, not `/usr/bin/amass`. The Kali wrapper asks for
root to download libpostal. Do not add `-active` or `-brute`.

OneForAll collects names and can brute-force DNS. Run it only with brute
force disabled:

```bash
oneforall --target "$DOMAIN" --brute False run
```

If that flag is rejected, do not run the default `run` mode. Use subfinder,
assetfinder, amass, and findomain instead.

## Live hosts and fingerprint

```bash
httpx -silent -l hosts.txt -rl 5 -threads 5 -status-code -title -tech-detect -o httpx.txt
webanalyze -hosts hosts.txt -worker 5 -output json -crawl 0 -apps "$HOME/.local/share/webanalyze/technologies.json"
eyewitness --web -f live.txt --no-prompt --timeout 15 --threads 5 -d eyewitness-out
wpscan --url "$URL" --enumerate vp,vt --plugins-detection passive --random-user-agent --format cli-no-colour
testssl --quiet --color 0 "$HOST"
```

`webanalyze` is the local CLI for Wappalyzer. Cap EyeWitness input at 25 URLs.
Run wpscan only after the page is WordPress. Do not pass a password list.
`testssl` is the installed name of testssl.sh. It takes one in-scope host.

## URLs, parameters, secrets in JavaScript

```bash
printf '%s\n' "$DOMAIN" | waybackurls
gau "$DOMAIN" --subs
katana -list live.txt -depth 2 -rate-limit 5 -concurrency 5 -field-scope fqdn -disable-redirects
paramspider -d "$DOMAIN"
arjun -u "$URL" -oJ arjun.json -q
uro -i urls.txt -o urls-deduped.txt
GF_PATTERNS="$HOME/.gf" gf xss < urls-deduped.txt
secretfinder -i "$JS_URL" -o cli
linkfinder -i "$JS_FILE_OR_URL" -o cli
```

`gf`, SecretFinder, and LinkFinder read URLs or files that are already
collected. They do not get a new target list. `qsreplace` stays unused.

## Content discovery

Use the short list at
`wildcard-scope-recon/references/content-paths.txt` unless the program allows
a larger list. Keep the list at or under 200 lines.

```bash
ffuf -noninteractive -s -ac -ic -u "$ORIGIN/FUZZ" -w content-paths.txt -rate 5 -t 5 -timeout 10 -maxtime-job 120 -mc 200,204,301,302,401,403
feroxbuster -u "$ORIGIN" -w content-paths.txt -t 5 --rate-limit 5 --no-recursion --quiet
dirsearch -u "$ORIGIN" -w content-paths.txt -t 5 --random-agent -q
```

One origin at a time. Stop on HTTP 429.

## One confirmed request, not a crawl

```bash
dalfox url "$URL" -w 5 --delay 200 --skip-bav -S
sqlmap -u "$URL" --batch --smart --level=1 --risk=1 --threads=1 --output-dir sqlmap-out
xsser -u "$URL" -g "$PARAM"
gobypass403 -u "$URL" -cr 5 -delay 200 -m headers_ip,http_methods,case_substitution
```

Pick the URL from an in-scope reflection, a parameter, or a 403 response.
Do not point these four tools at the whole historical URL list. sqlmap does
not get `--os-shell`, `--os-pwn`, `--file-write`, or a dump of every database.
wpscan does not get a password wordlist. xsser is the fallback when dalfox is
missing.

## Dorks

Write the query and open it in the browser. Do not scrape Google, Bing, or
GitHub with a request loop.

```text
site:*.example.com
site:example.com ext:log | ext:env | ext:json
site:example.com inurl:admin | inurl:graphql
site:github.com "example.com" (api_key OR secret OR password)
```

A result from search is a lead. Fetch it only when the host is in scope.

## Base tools

`curl`, `jq`, `git`, `python3`, and `go` are already on this machine. Use
them to fetch one in-scope URL, read JSON, and inspect a repository. They are
not a scanner.
