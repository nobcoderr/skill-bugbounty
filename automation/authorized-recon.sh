#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'HELP'
Authorized passive/active reconnaissance wrapper.

Usage:
  authorized-recon.sh --domain example.com --scope scope.txt [options]

Required:
  --domain DOMAIN       Seed domain to inventory.
  --scope FILE          Allowlist file. Exact host lines or .example.com suffix lines.

Options:
  --mode MODE           passive|active|all (default: passive)
  --out DIR             Output directory (default: ./recon-DOMAIN-TIMESTAMP)
  --rate N              Maximum requests/second for supported tools (default: 5)
  --concurrency N       Low concurrency default (default: 5)
  --enable-port-scan    Run a bounded top-ports naabu scan.
  --enable-nuclei       Run non-intrusive exposure/misconfiguration templates.
  --i-am-authorized     Required for active/all mode and active opt-ins.
  -h, --help            Show this help.

This wrapper does not authorize testing. Stop if program rules prohibit automation.
HELP
}

DOMAIN=''
SCOPE_FILE=''
MODE='passive'
OUT_DIR=''
RATE=5
CONCURRENCY=5
ENABLE_PORT_SCAN=0
ENABLE_NUCLEI=0
AUTHORIZED=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="${2:-}"; shift 2 ;;
    --scope) SCOPE_FILE="${2:-}"; shift 2 ;;
    --mode) MODE="${2:-}"; shift 2 ;;
    --out) OUT_DIR="${2:-}"; shift 2 ;;
    --rate) RATE="${2:-}"; shift 2 ;;
    --concurrency) CONCURRENCY="${2:-}"; shift 2 ;;
    --enable-port-scan) ENABLE_PORT_SCAN=1; shift ;;
    --enable-nuclei) ENABLE_NUCLEI=1; shift ;;
    --i-am-authorized) AUTHORIZED=1; shift ;;
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
[[ "$RATE" -le 50 ]] || fail 'Refusing rate above 50 requests/second.'
[[ "$CONCURRENCY" -le 25 ]] || fail 'Refusing concurrency above 25.'

DOMAIN="${DOMAIN,,}"
DOMAIN="${DOMAIN%.}"
[[ "$DOMAIN" =~ ^([a-z0-9-]+\.)+[a-z]{2,63}$ ]] || fail 'Domain format is invalid.'

scope_allows() {
  local host="${1,,}"
  local entry
  while IFS= read -r entry || [[ -n "$entry" ]]; do
    entry="${entry%%#*}"
    entry="${entry//[[:space:]]/}"
    [[ -z "$entry" ]] && continue
    entry="${entry,,}"
    entry="${entry%.}"
    if [[ "$entry" == .* ]]; then
      local suffix="${entry#.}"
      [[ "$host" == "$suffix" || "$host" == *".$suffix" ]] && return 0
    else
      [[ "$host" == "$entry" ]] && return 0
    fi
  done < "$SCOPE_FILE"
  return 1
}

scope_allows "$DOMAIN" || fail "Seed domain is not permitted by scope file: $DOMAIN"

if [[ "$MODE" != passive || $ENABLE_PORT_SCAN -eq 1 || $ENABLE_NUCLEI -eq 1 ]]; then
  [[ $AUTHORIZED -eq 1 ]] || fail 'Active operations require --i-am-authorized.'
fi

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="${OUT_DIR:-./recon-${DOMAIN}-${TIMESTAMP}}"
[[ -n "$OUT_DIR" && "$OUT_DIR" != '/' ]] || fail 'Refusing unsafe output directory.'
mkdir -p "$OUT_DIR/passive" "$OUT_DIR/active" "$OUT_DIR/meta"
cp "$SCOPE_FILE" "$OUT_DIR/meta/scope.txt"

{
  printf 'timestamp_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'domain=%s\nmode=%s\nrate=%s\nconcurrency=%s\n' "$DOMAIN" "$MODE" "$RATE" "$CONCURRENCY"
  printf 'enable_port_scan=%s\nenable_nuclei=%s\n' "$ENABLE_PORT_SCAN" "$ENABLE_NUCLEI"
} > "$OUT_DIR/meta/run.env"

filter_scope() {
  local input="$1" output="$2"
  : > "$output"
  while IFS= read -r host || [[ -n "$host" ]]; do
    host="${host,,}"
    host="${host%.}"
    [[ "$host" =~ ^([a-z0-9-]+\.)+[a-z]{2,63}$ ]] || continue
    if scope_allows "$host"; then
      printf '%s\n' "$host" >> "$output"
    else
      printf '%s\n' "$host" >> "$OUT_DIR/meta/rejected-out-of-scope-hosts.txt"
    fi
  done < "$input"
  sort -u "$output" -o "$output"
}

filter_url_scope() {
  local input="$1" accepted="$2" rejected="$3"
  have python3 || fail 'python3 is required to validate URL scope.'
  python3 - "$SCOPE_FILE" "$input" "$accepted" "$rejected" <<'PYURL'
from pathlib import Path
from urllib.parse import urlsplit
import sys

scope_path, input_path, accepted_path, rejected_path = map(Path, sys.argv[1:])
entries = []
for raw in scope_path.read_text(errors="replace").splitlines():
    raw = raw.split("#", 1)[0].strip().lower().rstrip(".")
    if raw:
        entries.append(raw)

def allowed(host: str) -> bool:
    host = host.lower().rstrip(".")
    for entry in entries:
        if entry.startswith("."):
            suffix = entry[1:]
            if host == suffix or host.endswith("." + suffix):
                return True
        elif host == entry:
            return True
    return False

accepted = set()
rejected = set()
if input_path.exists():
    for raw in input_path.read_text(errors="replace").splitlines():
        url = raw.strip()
        if not url:
            continue
        try:
            host = urlsplit(url).hostname
        except ValueError:
            host = None
        (accepted if host and allowed(host) else rejected).add(url)

accepted_path.write_text("".join(f"{url}\n" for url in sorted(accepted)))
rejected_path.write_text("".join(f"{url}\n" for url in sorted(rejected)))
PYURL
}

run_passive() {
  say 'Running passive inventory.'
  local raw="$OUT_DIR/passive/subdomains-raw.txt"
  : > "$raw"

  if have subfinder; then
    subfinder -silent -d "$DOMAIN" -all -o "$OUT_DIR/passive/subfinder.txt" || true
    cat "$OUT_DIR/passive/subfinder.txt" >> "$raw"
  else
    printf 'subfinder missing\n' >> "$OUT_DIR/meta/missing-tools.txt"
  fi

  printf '%s\n' "$DOMAIN" >> "$raw"
  filter_scope "$raw" "$OUT_DIR/passive/subdomains-in-scope.txt"

  if have gau; then
    gau "$DOMAIN" --subs 2>/dev/null | sort -u > "$OUT_DIR/passive/gau-urls.txt" || true
  else
    printf 'gau missing\n' >> "$OUT_DIR/meta/missing-tools.txt"
  fi

  if have waybackurls; then
    printf '%s\n' "$DOMAIN" | waybackurls 2>/dev/null | sort -u > "$OUT_DIR/passive/wayback-urls.txt" || true
  else
    printf 'waybackurls missing\n' >> "$OUT_DIR/meta/missing-tools.txt"
  fi

  cat "$OUT_DIR/passive/gau-urls.txt" "$OUT_DIR/passive/wayback-urls.txt" 2>/dev/null \
    | sort -u > "$OUT_DIR/passive/historical-urls-all.txt" || true

  filter_url_scope \
    "$OUT_DIR/passive/historical-urls-all.txt" \
    "$OUT_DIR/passive/historical-urls-in-scope.txt" \
    "$OUT_DIR/meta/rejected-out-of-scope-urls.txt"
}

run_active() {
  say 'Running active low-touch verification.'
  local hosts="$OUT_DIR/passive/subdomains-in-scope.txt"
  [[ -s "$hosts" ]] || { printf '%s\n' "$DOMAIN" > "$hosts"; }

  have dnsx || fail 'dnsx is required for active mode.'
  have httpx || fail 'httpx is required for active mode.'

  dnsx -silent -no-color -l "$hosts" -a -aaaa -cname -resp -rl "$RATE" \
    -o "$OUT_DIR/active/dnsx.txt"

  httpx -silent -no-color -l "$hosts" -rl "$RATE" -threads "$CONCURRENCY" \
    -status-code -title -tech-detect -server -ip -cname -location \
    -o "$OUT_DIR/active/httpx.txt"

  awk '{print $1}' "$OUT_DIR/active/httpx.txt" | sed 's/[[:space:]].*$//' \
    | sort -u > "$OUT_DIR/active/live-urls.txt"
  filter_url_scope \
    "$OUT_DIR/active/live-urls.txt" \
    "$OUT_DIR/active/live-urls-in-scope.txt" \
    "$OUT_DIR/meta/rejected-httpx-out-of-scope-urls.txt"

  if have katana && [[ -s "$OUT_DIR/active/live-urls-in-scope.txt" ]]; then
    katana -silent -no-color -list "$OUT_DIR/active/live-urls-in-scope.txt" -depth 2 \
      -concurrency "$CONCURRENCY" -parallelism 2 -rate-limit "$RATE" \
      -field-scope fqdn -disable-redirects -max-domain-pages 200 \
      -o "$OUT_DIR/active/katana-urls-all.txt" || true
    filter_url_scope \
      "$OUT_DIR/active/katana-urls-all.txt" \
      "$OUT_DIR/active/katana-urls-in-scope.txt" \
      "$OUT_DIR/meta/rejected-katana-out-of-scope-urls.txt"
  else
    printf 'katana missing or no live in-scope URL\n' >> "$OUT_DIR/meta/missing-tools.txt"
  fi

  if [[ $ENABLE_PORT_SCAN -eq 1 ]]; then
    have naabu || fail 'naabu is required for --enable-port-scan.'
    say 'Running explicitly enabled bounded top-port scan.'
    naabu -silent -no-color -list "$hosts" -top-ports 100 -rate "$RATE" \
      -c "$CONCURRENCY" -exclude-cdn -o "$OUT_DIR/active/naabu-top100.txt"
  fi

  if [[ $ENABLE_NUCLEI -eq 1 ]]; then
    have nuclei || fail 'nuclei is required for --enable-nuclei.'
    [[ -s "$OUT_DIR/active/live-urls-in-scope.txt" ]] || fail 'No live in-scope URLs for nuclei.'
    say 'Running explicitly enabled non-intrusive nuclei subset.'
    nuclei -silent -no-color -list "$OUT_DIR/active/live-urls-in-scope.txt" \
      -rate-limit "$RATE" -bulk-size "$CONCURRENCY" -concurrency "$CONCURRENCY" \
      -tags tech,exposure,misconfig \
      -exclude-tags dos,fuzz,intrusive,bruteforce,default-login \
      -o "$OUT_DIR/active/nuclei-non-intrusive.txt" || true
  fi
}

run_passive
if [[ "$MODE" == active || "$MODE" == all ]]; then
  run_active
fi

{
  for binary in subfinder gau waybackurls dnsx httpx katana naabu nuclei; do
    if have "$binary"; then
      printf '## %s\n' "$binary"
      ("$binary" -version 2>&1 || "$binary" --version 2>&1 || true) | head -n 3
    fi
  done
} > "$OUT_DIR/meta/tool-versions.txt"

say "Finished. Review scope rejections and results under: $OUT_DIR"
printf '%s\n' 'Recon output is inventory, not a vulnerability. Manually validate every candidate.'
