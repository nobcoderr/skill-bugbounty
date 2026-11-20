#!/usr/bin/env bash
set -Eeuo pipefail

# Installs a bounded web/recon research toolkit. Installation does not grant
# authorization to scan any target. Do not run this script from an untrusted copy.

usage() {
  cat <<'HELP'
Install/update the authorized black-box research toolkit.

Usage:
  install-authorized-blackbox-tools.sh

Optional environment variables:
  TOOLS_DIR   Git/reference checkout directory (default: ~/tools)
  BIN_DIR     User-local binary symlink directory (default: ~/.local/bin)
  LOG_DIR     Installation logs/manifests (default: ~/.local/state/authorized-blackbox-tools)

Supported systems: Kali/Debian/Ubuntu with apt, and macOS with Homebrew.
The script installs tools but never launches a scan.
HELP
}

case "${1:-}" in
  -h|--help) usage; exit 0 ;;
  '') ;;
  *) printf 'Unknown argument: %s\n' "$1" >&2; usage; exit 2 ;;
esac

TOOLS_DIR="${TOOLS_DIR:-$HOME/tools}"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"
LOG_DIR="${LOG_DIR:-$HOME/.local/state/authorized-blackbox-tools}"
PATT_DIR="$TOOLS_DIR/PayloadsAllTheThings"

mkdir -p "$TOOLS_DIR" "$BIN_DIR" "$LOG_DIR"
LOG_FILE="$LOG_DIR/install-$(date -u +%Y%m%dT%H%M%SZ).log"
MANIFEST="$LOG_DIR/versions-$(date -u +%Y%m%dT%H%M%SZ).txt"
exec > >(tee -a "$LOG_FILE") 2>&1

say() { printf '[+] %s\n' "$*"; }
warn() { printf '[!] %s\n' "$*" >&2; }
fail() { printf '[-] %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

install_linux() {
  have apt-get || fail 'Supported Linux installer requires apt-get (Kali/Debian/Ubuntu).'
  local sudo_cmd=()
  if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
    have sudo || fail 'sudo is required for system packages.'
    sudo_cmd=(sudo)
  fi

  say 'Installing required base packages with apt.'
  "${sudo_cmd[@]}" apt-get update
  "${sudo_cmd[@]}" apt-get install -y \
    ca-certificates curl wget git jq unzip zip make gcc \
    python3 python3-pip pipx python3-venv \
    golang-go ripgrep nmap libpcap-dev

  say 'Installing optional distribution packages.'
  "${sudo_cmd[@]}" apt-get install -y masscan || warn 'masscan package unavailable; continuing.'
  "${sudo_cmd[@]}" apt-get install -y whatweb || warn 'whatweb package unavailable; continuing.'
  "${sudo_cmd[@]}" apt-get install -y dnsutils \
    || "${sudo_cmd[@]}" apt-get install -y bind9-dnsutils \
    || warn 'DNS utility package unavailable; continuing.'

  if [[ -r /etc/os-release ]] && grep -qi '^ID=kali' /etc/os-release; then
    "${sudo_cmd[@]}" apt-get install -y burpsuite \
      || warn 'Optional Burp Suite package unavailable; continuing.'
  fi
}

install_macos() {
  have brew || fail 'Homebrew is required on macOS: https://brew.sh/'
  say 'Installing required base packages with Homebrew.'
  brew update
  brew install git curl wget jq unzip zip python pipx go ripgrep nmap libpcap
  say 'Installing optional Homebrew tools.'
  brew install masscan || warn 'masscan formula unavailable; continuing.'
  brew install bind || warn 'bind formula unavailable; continuing.'
  brew install whatweb || warn 'whatweb formula unavailable; continuing.'
  brew install --cask owasp-zap || warn 'OWASP ZAP cask install failed; install it manually if needed.'
  brew install --cask burp-suite || warn 'Burp Suite cask install failed; install it manually if needed.'
}

case "$(uname -s)" in
  Linux) install_linux ;;
  Darwin) install_macos ;;
  *) fail "Unsupported OS: $(uname -s)" ;;
esac

export PATH="$BIN_DIR:$(go env GOPATH 2>/dev/null || printf '%s' "$HOME/go")/bin:$PATH"

have go || fail 'Go is not available after package installation.'
have pipx || fail 'pipx is not available after package installation.'

say 'Installing/updating Go-based tools.'
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/ffuf/ffuf/v2@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/tomnomnom/anew@latest

GOBIN_PATH="$(go env GOPATH)/bin"
for binary in subfinder dnsx httpx naabu nuclei katana ffuf gau waybackurls anew; do
  if [[ -x "$GOBIN_PATH/$binary" ]]; then
    ln -sfn "$GOBIN_PATH/$binary" "$BIN_DIR/$binary"
  fi
done

say 'Installing/updating user-local Python tools.'
pipx install --force arjun
pipx install --force uro
pipx ensurepath >/dev/null 2>&1 || true

say 'Cloning/updating PayloadsAllTheThings.'
if [[ -d "$PATT_DIR/.git" ]]; then
  git -C "$PATT_DIR" fetch --prune origin
  git -C "$PATT_DIR" pull --ff-only
else
  git clone --depth 1 https://github.com/swisskyrepo/PayloadsAllTheThings.git "$PATT_DIR"
fi

say 'Updating nuclei templates without running a scan.'
if have nuclei; then
  nuclei -update-templates || warn 'Nuclei template update failed; review manually.'
fi

say 'Recording tool versions.'
{
  printf 'timestamp_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'os=%s\n' "$(uname -a)"
  printf 'tools_dir=%s\n' "$TOOLS_DIR"
  printf 'bin_dir=%s\n' "$BIN_DIR"
  printf '\n'
  for binary in git curl jq python3 pipx go rg nmap masscan whatweb \
                subfinder dnsx httpx naabu nuclei katana ffuf gau \
                waybackurls anew arjun uro; do
    if have "$binary"; then
      printf '## %s\n' "$binary"
      ("$binary" -version 2>&1 || "$binary" --version 2>&1 || true) | head -n 3
    else
      printf 'MISSING=%s\n' "$binary"
    fi
  done
  if [[ -d "$PATT_DIR/.git" ]]; then
    printf 'PayloadsAllTheThings_commit=%s\n' "$(git -C "$PATT_DIR" rev-parse HEAD)"
  fi
} > "$MANIFEST"

missing=0
for binary in subfinder dnsx httpx naabu nuclei katana ffuf gau waybackurls anew arjun uro; do
  if ! have "$binary" && [[ ! -x "$BIN_DIR/$binary" ]]; then
    warn "Missing expected binary: $binary"
    missing=1
  fi
done

cat <<MSG

Installation finished.
Log:      $LOG_FILE
Manifest: $MANIFEST
Payloads: $PATT_DIR

Ensure this directory is in PATH:
  export PATH="$BIN_DIR:\$PATH"

No scan has been launched. Use only against explicitly authorized scope.
MSG

[[ $missing -eq 0 ]] || fail 'One or more expected tools are missing; inspect the log.'
