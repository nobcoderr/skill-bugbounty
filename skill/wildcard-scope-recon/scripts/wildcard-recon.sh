#!/usr/bin/env bash
# Authorized wildcard-scope inventory. This script does not grant permission.
set -Eeuo pipefail

usage() {
  cat <<'HELP'
Wildcard-scope inventory for an authorized program.

Usage:
  wildcard-recon.sh --domain example.com --scope scope.txt [options]

Required:
  --domain DOMAIN       Registrable domain named by a wildcard scope line.
  --scope FILE          Allowlist. Use *.example.com, .example.com, or exact hosts.

Options:
  --mode MODE           passive|active|all (default: passive)
  --out DIR             Output directory (default: ./recon-DOMAIN-TIMESTAMP)
  --rate N              Max requests/second where the tool supports it (default: 5, max: 15)
  --concurrency N       Low concurrency (default: 5, max: 10)
  --host-budget N       Live origins sent to ffuf (default: 8, max: 25)
  --param-budget N      Live URLs sent to arjun (default: 5, max: 15)
  --wordlist FILE       Optional ffuf wordlist. Refused above 200 non-comment lines.
  --enable-port-scan    Bounded naabu top-100 scan. Requires active authorization.
  --i-am-authorized     Required for active/all and for the port scan.
  --check-scope         Validate the wildcard and exit. No tool traffic.
  -h, --help            Show this help.
HELP
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_WORDLIST="$SCRIPT_DIR/../references/content-paths.txt"

DOMAIN=''
SCOPE_FILE=''
MODE='passive'
OUT_DIR=''
RATE=5
CONCURRENCY=5
HOST_BUDGET=8
PARAM_BUDGET=5
WORDLIST="$DEFAULT_WORDLIST"
ENABLE_PORT_SCAN=0
AUTHORIZED=0
CHECK_SCOPE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="${2:-}"; shift 2 ;;
    --scope) SCOPE_FILE="${2:-}"; shift 2 ;;
    --mode) MODE="${2:-}"; shift 2 ;;
    --out) OUT_DIR="${2:-}"; shift 2 ;;
    --rate) RATE="${2:-}"; shift 2 ;;
    --concurrency) CONCURRENCY="${2:-}"; shift 2 ;;
    --host-budget) HOST_BUDGET="${2:-}"; shift 2 ;;
    --param-budget) PARAM_BUDGET="${2:-}"; shift 2 ;;
    --wordlist) WORDLIST="${2:-}"; shift 2 ;;
    --enable-port-scan) ENABLE_PORT_SCAN=1; shift ;;
    --i-am-authorized) AUTHORIZED=1; shift ;;
    --check-scope) CHECK_SCOPE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; usage; exit 2 ;;
  esac
done

fail() { printf '[-] %s\n' "$*" >&2; exit 1; }
say() { printf '[+] %s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

[[ -n "$DOMAIN" ]] || fail '--domain is required.'
[[ -f "$SCOPE_FILE" ]] || fail '--scope must point to a readable file.'
[[ "$MODE" =~ ^(passive|active|all)$ ]] || fail '--mode must be passive, active, or all.'
[[ "$RATE" =~ ^[1-9][0-9]*$ ]] || fail '--rate must be a positive integer.'
[[ "$CONCURRENCY" =~ ^[1-9][0-9]*$ ]] || fail '--concurrency must be a positive integer.'
[[ "$HOST_BUDGET" =~ ^[1-9][0-9]*$ ]] || fail '--host-budget must be a positive integer.'
[[ "$PARAM_BUDGET" =~ ^[1-9][0-9]*$ ]] || fail '--param-budget must be a positive integer.'
[[ "$RATE" -le 15 ]] || fail 'Refusing rate above 15 requests/second.'
[[ "$CONCURRENCY" -le 10 ]] || fail 'Refusing concurrency above 10.'
[[ "$HOST_BUDGET" -le 25 ]] || fail 'Refusing host budget above 25.'
[[ "$PARAM_BUDGET" -le 15 ]] || fail 'Refusing parameter budget above 15.'
[[ -f "$WORDLIST" ]] || fail "Wordlist not found: $WORDLIST"

DOMAIN="${DOMAIN,,}"
DOMAIN="${DOMAIN%.}"
[[ "$DOMAIN" =~ ^([a-z0-9-]+\.)+[a-z]{2,63}$ ]] || fail 'Domain format is invalid.'

word_count="$(grep -cEv '^[[:space:]]*(#|$)' "$WORDLIST" || true)"
[[ "${word_count:-0}" -le 200 ]] || fail 'Wordlist has more than 200 entries. Keep content discovery bounded.'

if [[ "$MODE" != passive || "$ENABLE_PORT_SCAN" -eq 1 ]]; then
  [[ "$AUTHORIZED" -eq 1 ]] || fail 'Active operations require --i-am-authorized.'
fi

python3 "$SCRIPT_DIR/scope_filter.py" check "$SCOPE_FILE" "$DOMAIN" || fail 'Scope rejected.'

if [[ "$CHECK_SCOPE" -eq 1 ]]; then
  say "Scope check passed for $DOMAIN. No tools were run."
  exit 0
fi

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="${OUT_DIR:-./recon-${DOMAIN}-${TIMESTAMP}}"
[[ -n "$OUT_DIR" && "$OUT_DIR" != '/' ]] || fail 'Refusing unsafe output directory.'
mkdir -p "$OUT_DIR/passive" "$OUT_DIR/active/arjun" "$OUT_DIR/meta"
cp "$SCOPE_FILE" "$OUT_DIR/meta/scope.txt"
: > "$OUT_DIR/meta/missing-tools.txt"
: > "$OUT_DIR/meta/rejected-out-of-scope-hosts.txt"
: > "$OUT_DIR/meta/rejected-out-of-scope-urls.txt"
{
  printf 'timestamp_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'domain=%s\nmode=%s\nrate=%s\nconcurrency=%s\n' "$DOMAIN" "$MODE" "$RATE" "$CONCURRENCY"
  printf 'host_budget=%s\nparam_budget=%s\nport_scan=%s\n' "$HOST_BUDGET" "$PARAM_BUDGET" "$ENABLE_PORT_SCAN"
} > "$OUT_DIR/meta/run.env"

filter_hosts() {
  python3 "$SCRIPT_DIR/scope_filter.py" hosts "$SCOPE_FILE" "$1" "$2" "$OUT_DIR/meta/rejected-out-of-scope-hosts.txt"
}

filter_urls() {
  python3 "$SCRIPT_DIR/scope_filter.py" urls "$SCOPE_FILE" "$1" "$2" "$OUT_DIR/meta/rejected-out-of-scope-urls.txt"
}

note_missing() { printf '%s\n' "$1" >> "$OUT_DIR/meta/missing-tools.txt"; }

say 'Collecting passive names.'
raw_hosts="$OUT_DIR/passive/subdomains-raw.txt"
: > "$raw_hosts"
if have subfinder; then
  subfinder -silent -d "$DOMAIN" -all -o "$OUT_DIR/passive/subfinder.txt" || true
  cat "$OUT_DIR/passive/subfinder.txt" >> "$raw_hosts" 2>/dev/null || true
else
  note_missing subfinder
fi
if have assetfinder; then
  assetfinder --subs-only "$DOMAIN" > "$OUT_DIR/passive/assetfinder.txt" || true
  cat "$OUT_DIR/passive/assetfinder.txt" >> "$raw_hosts" || true
else
  note_missing assetfinder
fi
python3 - "$DOMAIN" "$OUT_DIR/passive/crtsh.txt" <<'PY' || true
import json, sys, urllib.request
domain, output = sys.argv[1], sys.argv[2]
url = f"https://crt.sh/?q=%25.{domain}&output=json"
try:
    with urllib.request.urlopen(url, timeout=25) as response:
        payload = json.loads(response.read().decode("utf-8", "replace") or "[]")
except Exception as exc:
    open(output, "w", encoding="utf-8").write("")
    sys.stderr.write(f"crt.sh skipped: {exc}\n")
    sys.exit(0)
names = set()
for row in payload if isinstance(payload, list) else []:
    for piece in str(row.get("name_value", "")).splitlines():
        piece = piece.strip().lower().lstrip("*.")
        if piece:
            names.add(piece)
        if len(names) >= 5000:
            break
open(output, "w", encoding="utf-8").write("".join(f"{name}\n" for name in sorted(names)))
PY
cat "$OUT_DIR/passive/crtsh.txt" >> "$raw_hosts" 2>/dev/null || true
append_lines() {
  local source="$1"
  [[ -f "$source" ]] || return 0
  cat "$source" >> "$2" || true
}
amass_bin=""
if [[ -x /usr/lib/amass/amass ]]; then
  amass_bin=/usr/lib/amass/amass
elif have amass; then
  amass_bin="$(command -v amass)"
fi
if [[ -n "$amass_bin" ]]; then
  mkdir -p "$OUT_DIR/passive/amass-dir"
  timeout 180 "$amass_bin" enum -d "$DOMAIN" -silent -rigid -timeout 2 \
    -dir "$OUT_DIR/passive/amass-dir" > "$OUT_DIR/meta/amass.log" 2>&1 || true
  find "$OUT_DIR/passive/amass-dir" -type f -print0 2>/dev/null | while IFS= read -r -d '' amass_file; do
    cat "$amass_file" >> "$OUT_DIR/passive/amass.txt"
  done
  append_lines "$OUT_DIR/passive/amass.txt" "$raw_hosts"
else
  note_missing amass
fi
if have findomain; then
  findomain -t "$DOMAIN" -q -u "$OUT_DIR/passive/findomain.txt" \
    > "$OUT_DIR/meta/findomain.log" 2>&1 || true
  append_lines "$OUT_DIR/passive/findomain.txt" "$raw_hosts"
else
  note_missing findomain
fi
if have uncover; then
  uncover -silent -f host -q "$DOMAIN" -o "$OUT_DIR/passive/uncover.txt" \
    > "$OUT_DIR/meta/uncover.log" 2>&1 || true
  append_lines "$OUT_DIR/passive/uncover.txt" "$raw_hosts"
else
  note_missing uncover
fi
if have github-subdomains && [[ -n "${GITHUB_TOKEN:-${GH_TOKEN:-}}" ]]; then
  if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    GITHUB_TOKEN="${GH_TOKEN}" github-subdomains -d "$DOMAIN" -q -o "$OUT_DIR/passive/github-subdomains.txt" \
      > "$OUT_DIR/meta/github-subdomains.log" 2>&1 || true
  else
    github-subdomains -d "$DOMAIN" -q -o "$OUT_DIR/passive/github-subdomains.txt" \
      > "$OUT_DIR/meta/github-subdomains.log" 2>&1 || true
  fi
  append_lines "$OUT_DIR/passive/github-subdomains.txt" "$raw_hosts"
elif have github-subdomains; then
  note_missing 'github-subdomains needs GITHUB_TOKEN'
else
  note_missing github-subdomains
fi
filter_hosts "$raw_hosts" "$OUT_DIR/passive/subdomains-in-scope.txt"

say 'Collecting passive URLs.'
: > "$OUT_DIR/passive/historical-urls-all.txt"
if have gau; then
  gau "$DOMAIN" --subs > "$OUT_DIR/passive/gau-urls.txt" 2>/dev/null || true
  cat "$OUT_DIR/passive/gau-urls.txt" >> "$OUT_DIR/passive/historical-urls-all.txt" || true
else
  note_missing gau
fi
if have waybackurls; then
  printf '%s\n' "$DOMAIN" | waybackurls > "$OUT_DIR/passive/wayback-urls.txt" 2>/dev/null || true
  cat "$OUT_DIR/passive/wayback-urls.txt" >> "$OUT_DIR/passive/historical-urls-all.txt" || true
else
  note_missing waybackurls
fi
: > "$OUT_DIR/passive/paramspider-raw.txt"
if have paramspider; then
  spider_dir="$OUT_DIR/active/paramspider-run"
  mkdir -p "$spider_dir"
  (cd "$spider_dir" && paramspider -d "$DOMAIN") > "$OUT_DIR/meta/paramspider.log" 2>&1 || true
  while IFS= read -r -d '' spider_file; do
    cat "$spider_file" >> "$OUT_DIR/passive/paramspider-raw.txt"
  done < <(find "$spider_dir" -type f -name '*.txt' -print0 2>/dev/null)
  cat "$OUT_DIR/passive/paramspider-raw.txt" >> "$OUT_DIR/passive/historical-urls-all.txt" || true
else
  note_missing paramspider
fi
if have urlfinder; then
  urlfinder -d "$DOMAIN" -silent -duc -rl "$RATE" -o "$OUT_DIR/passive/urlfinder.txt" \
    > "$OUT_DIR/meta/urlfinder.log" 2>&1 || true
  append_lines "$OUT_DIR/passive/urlfinder.txt" "$OUT_DIR/passive/historical-urls-all.txt"
else
  note_missing urlfinder
fi
if have waymore; then
  waymore -i "$DOMAIN" -mode U -oU "$OUT_DIR/passive/waymore.txt" \
    > "$OUT_DIR/meta/waymore.log" 2>&1 || true
  append_lines "$OUT_DIR/passive/waymore.txt" "$OUT_DIR/passive/historical-urls-all.txt"
else
  note_missing waymore
fi
sort -u "$OUT_DIR/passive/historical-urls-all.txt" -o "$OUT_DIR/passive/historical-urls-all.txt"
filter_urls "$OUT_DIR/passive/historical-urls-all.txt" "$OUT_DIR/passive/historical-urls-in-scope.txt"
filter_urls "$OUT_DIR/passive/paramspider-raw.txt" "$OUT_DIR/active/paramspider-urls-in-scope.txt"
if have uro; then
  if [[ -s "$OUT_DIR/passive/historical-urls-in-scope.txt" ]]; then
    uro -i "$OUT_DIR/passive/historical-urls-in-scope.txt" -o "$OUT_DIR/passive/urls-deduped.txt" || true
    if [[ -s "$OUT_DIR/passive/urls-deduped.txt" ]]; then
      mv "$OUT_DIR/passive/urls-deduped.txt" "$OUT_DIR/passive/historical-urls-in-scope.txt"
    fi
  fi
else
  note_missing uro
fi
if have unfurl; then
  if [[ -s "$OUT_DIR/passive/historical-urls-in-scope.txt" ]]; then
    unfurl keys < "$OUT_DIR/passive/historical-urls-in-scope.txt" | sort -u > "$OUT_DIR/passive/param-names.txt" || true
    unfurl paths < "$OUT_DIR/passive/historical-urls-in-scope.txt" | sort -u > "$OUT_DIR/passive/paths.txt" || true
  fi
else
  note_missing unfurl
fi

if [[ "$MODE" == passive ]]; then
  say 'Passive mode finished. Active tools were not run.'
else
  say 'Running active low-touch checks on in-scope names only.'
  hosts="$OUT_DIR/passive/subdomains-in-scope.txt"
  if have alterx && [[ -s "$hosts" ]]; then
    head -n 100 "$hosts" > "$OUT_DIR/active/alterx-input.txt"
    alterx -l "$OUT_DIR/active/alterx-input.txt" -silent -limit 500 > "$OUT_DIR/active/alterx-raw.txt" 2>/dev/null || true
    filter_hosts "$OUT_DIR/active/alterx-raw.txt" "$OUT_DIR/active/alterx-in-scope.txt"
    cat "$hosts" "$OUT_DIR/active/alterx-in-scope.txt" 2>/dev/null | sort -u > "$OUT_DIR/active/hosts-with-permutations.txt"
    hosts="$OUT_DIR/active/hosts-with-permutations.txt"
  else
    note_missing alterx
  fi
  if have dnsx; then
    dnsx -silent -no-color -l "$hosts" -a -aaaa -cname -resp -rl "$RATE" -o "$OUT_DIR/active/dnsx.txt" || true
  else
    note_missing dnsx
  fi
  if have tlsx && [[ -s "$hosts" ]]; then
    tlsx -l "$hosts" -san -cn -silent -duc -c "$CONCURRENCY" -o "$OUT_DIR/active/tlsx.txt" \
      > "$OUT_DIR/meta/tlsx.log" 2>&1 || true
    grep -oE '([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,63}' "$OUT_DIR/active/tlsx.txt" 2>/dev/null \
      | sort -u > "$OUT_DIR/active/tlsx-names.txt" || true
    filter_hosts "$OUT_DIR/active/tlsx-names.txt" "$OUT_DIR/active/tlsx-in-scope.txt"
    cat "$hosts" "$OUT_DIR/active/tlsx-in-scope.txt" 2>/dev/null | sort -u > "$OUT_DIR/active/hosts-final.txt"
    hosts="$OUT_DIR/active/hosts-final.txt"
  else
    note_missing tlsx
  fi
  if have cdncheck && [[ -s "$hosts" ]]; then
    cdncheck -i "$hosts" -silent -t "$CONCURRENCY" -o "$OUT_DIR/active/cdncheck.txt" \
      > "$OUT_DIR/meta/cdncheck.log" 2>&1 || true
  else
    note_missing cdncheck
  fi
  if have httpx; then
    httpx -silent -no-color -l "$hosts" -rl "$RATE" -threads "$CONCURRENCY" \
      -status-code -title -tech-detect -server -ip -cname -location \
      -o "$OUT_DIR/active/httpx.txt" || true
    awk '{print $1}' "$OUT_DIR/active/httpx.txt" | sed 's/[[:space:]].*$//' | sort -u > "$OUT_DIR/active/live-urls-raw.txt"
    filter_urls "$OUT_DIR/active/live-urls-raw.txt" "$OUT_DIR/active/live-urls-in-scope.txt"
  else
    note_missing httpx
    : > "$OUT_DIR/active/live-urls-in-scope.txt"
  fi

  if have katana && [[ -s "$OUT_DIR/active/live-urls-in-scope.txt" ]]; then
    head -n "$HOST_BUDGET" "$OUT_DIR/active/live-urls-in-scope.txt" > "$OUT_DIR/active/katana-input.txt"
    katana -silent -no-color -list "$OUT_DIR/active/katana-input.txt" -depth 2 \
      -concurrency "$CONCURRENCY" -parallelism 2 -rate-limit "$RATE" \
      -field-scope fqdn -disable-redirects -max-domain-pages 100 \
      -o "$OUT_DIR/active/katana-urls-all.txt" || true
    filter_urls "$OUT_DIR/active/katana-urls-all.txt" "$OUT_DIR/active/katana-urls-in-scope.txt"
  else
    note_missing 'katana or no live in-scope URL'
    : > "$OUT_DIR/active/katana-urls-in-scope.txt"
  fi

  if have hakrawler && [[ -s "$OUT_DIR/active/live-urls-in-scope.txt" ]]; then
    head -n "$HOST_BUDGET" "$OUT_DIR/active/live-urls-in-scope.txt" \
      | hakrawler -d 2 -insecure -t "$CONCURRENCY" > "$OUT_DIR/active/hakrawler-urls-all.txt" 2>"$OUT_DIR/meta/hakrawler.log" || true
    filter_urls "$OUT_DIR/active/hakrawler-urls-all.txt" "$OUT_DIR/active/hakrawler-urls-in-scope.txt"
  else
    note_missing hakrawler
  fi

  if [[ -s "$OUT_DIR/active/live-urls-in-scope.txt" ]]; then
    count=0
    : > "$OUT_DIR/active/fingerprint.txt"
    while IFS= read -r origin; do
      count=$((count + 1))
      [[ "$count" -le "$HOST_BUDGET" ]] || break
      if have wafw00f; then
        wafw00f "$origin" >> "$OUT_DIR/active/fingerprint.txt" 2>>"$OUT_DIR/meta/wafw00f.log" || true
      fi
      if have whatweb; then
        whatweb --no-errors -a 1 "$origin" >> "$OUT_DIR/active/fingerprint.txt" 2>>"$OUT_DIR/meta/whatweb.log" || true
      fi
    done < "$OUT_DIR/active/live-urls-in-scope.txt"
  fi
  have wafw00f || note_missing wafw00f
  have whatweb || note_missing whatweb

  if have ffuf && [[ -s "$OUT_DIR/active/live-urls-in-scope.txt" ]]; then
    : > "$OUT_DIR/active/ffuf-hits.txt"
    count=0
    while IFS= read -r origin; do
      count=$((count + 1))
      [[ "$count" -le "$HOST_BUDGET" ]] || break
      ffuf -noninteractive -s -ac -ic -u "${origin%/}/FUZZ" -w "$WORDLIST" \
        -rate "$RATE" -t "$CONCURRENCY" -timeout 10 -maxtime-job 120 \
        -mc 200,204,301,302,401,403 \
        -o "$OUT_DIR/active/ffuf-${count}.json" -of json || true
      python3 - "$OUT_DIR/active/ffuf-${count}.json" "$origin" "$OUT_DIR/active/ffuf-hits.txt" <<'PY' || true
import json, sys
source, origin, output = sys.argv[1:]
try:
    data = json.load(open(source, encoding="utf-8"))
except Exception:
    sys.exit(0)
rows = data.get("results", data if isinstance(data, list) else [])
with open(output, "a", encoding="utf-8") as handle:
    for row in rows:
        url = row.get("url") or origin
        status = row.get("status", "")
        handle.write(f"{status} {url}\n")
PY
    done < "$OUT_DIR/active/live-urls-in-scope.txt"
  else
    note_missing ffuf
  fi

  if have arjun && [[ -s "$OUT_DIR/active/live-urls-in-scope.txt" ]]; then
    count=0
    while IFS= read -r origin; do
      count=$((count + 1))
      [[ "$count" -le "$PARAM_BUDGET" ]] || break
      timeout 90 arjun -u "$origin" -oJ "$OUT_DIR/active/arjun/${count}.json" -q \
        > "$OUT_DIR/active/arjun/${count}.log" 2>&1 || true
    done < "$OUT_DIR/active/live-urls-in-scope.txt"
  else
    note_missing arjun
  fi

  if have nuclei && [[ -s "$OUT_DIR/active/live-urls-in-scope.txt" ]]; then
    nuclei -silent -no-color -list "$OUT_DIR/active/live-urls-in-scope.txt" \
      -rate-limit "$RATE" -bulk-size "$CONCURRENCY" -concurrency "$CONCURRENCY" \
      -tags tech,exposure,misconfig \
      -exclude-tags dos,fuzz,intrusive,bruteforce,default-login \
      -o "$OUT_DIR/active/nuclei-non-intrusive.txt" || true
  else
    note_missing nuclei
  fi

  if [[ "$ENABLE_PORT_SCAN" -eq 1 ]]; then
    if have naabu; then
      naabu -silent -no-color -list "$hosts" -top-ports 100 -rate "$RATE" \
        -c "$CONCURRENCY" -exclude-cdn -o "$OUT_DIR/active/naabu-top100.txt" || true
    else
      note_missing naabu
    fi
  fi
fi

{
  printf 'domain=%s\nmode=%s\n' "$DOMAIN" "$MODE"
  for file in \
    passive/subdomains-in-scope.txt \
    passive/historical-urls-in-scope.txt \
    active/live-urls-in-scope.txt \
    active/katana-urls-in-scope.txt \
    active/ffuf-hits.txt \
    active/nuclei-non-intrusive.txt
  do
    path="$OUT_DIR/$file"
    if [[ -f "$path" ]]; then
      printf '%s=%s\n' "$file" "$(grep -c . "$path" || true)"
    else
      printf '%s=not-run\n' "$file"
    fi
  done
  printf 'missing_tools=%s\n' "$(paste -sd, "$OUT_DIR/meta/missing-tools.txt" || true)"
} > "$OUT_DIR/summary.txt"

say "Finished. Inventory only, under: $OUT_DIR"
printf '%s\n' 'Tool output is not a vulnerability. Validate every candidate on an in-scope asset.'
