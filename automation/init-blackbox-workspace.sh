#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'HELP'
Create a local evidence workspace for an authorized black-box engagement.

Usage:
  init-blackbox-workspace.sh --name NAME --scope FILE [--base DIR]

The workspace stores no passwords, cookies, tokens, MFA secrets, or API keys.
HELP
}

NAME=''
SCOPE_FILE=''
BASE_DIR="${BASE_DIR:-$PWD}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) NAME="${2:-}"; shift 2 ;;
    --scope) SCOPE_FILE="${2:-}"; shift 2 ;;
    --base) BASE_DIR="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; usage; exit 2 ;;
  esac
done

[[ -n "$NAME" ]] || { usage; exit 2; }
[[ -f "$SCOPE_FILE" ]] || { printf 'Scope file not found: %s\n' "$SCOPE_FILE" >&2; exit 2; }

SAFE_NAME="$(printf '%s' "$NAME" | tr -cs 'A-Za-z0-9._-' '-')"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ROOT="$BASE_DIR/${SAFE_NAME}-${STAMP}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PACK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

mkdir -p "$ROOT"/{scope,recon,traffic,requests,states,screenshots,video,notes,handoff,cleanup,meta}
mkdir -p "$ROOT/accounts"/{A-attacker,B-peer,C-control}
cp "$SCOPE_FILE" "$ROOT/scope/allowlist.txt"
cp "$PACK_ROOT/config/test-accounts.env.example" "$ROOT/meta/test-accounts.env.example"
cp "$PACK_ROOT/references/BLACKBOX_EVIDENCE_WORKSHEET.md" "$ROOT/notes/evidence-worksheet.md"

cat > "$ROOT/meta/ACCOUNT_BOUNDARIES.md" <<'DOC'
# Account boundaries

- A — argareksapatii+a@wearehackerone.com — attacker/low privilege.
- B — argareksapatii+b@wearehackerone.com — peer victim/second tenant.
- C — argareksapatii+c@wearehackerone.com — isolated control; privileged only if legitimately assigned.

Do not save passwords, MFA seeds, cookies, bearer tokens, API keys, recovery codes,
or unredacted third-party data in this workspace. Keep browser profiles and secret
material in a secure local secret store outside shared evidence directories.
DOC

cat > "$ROOT/meta/engagement.env" <<META
created_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
engagement_name=$NAME
workspace=$ROOT
scope_file=$ROOT/scope/allowlist.txt
META

{
  printf '# %s\n\n' "$NAME"
  printf 'Authorized black-box workspace created at %s UTC.\n\n' "$STAMP"
  cat <<'DOC'
Start here:

1. Confirm `scope/allowlist.txt` against current program rules.
2. Record authorization, exclusions, and rate limits in `notes/evidence-worksheet.md`.
3. Keep each account's captures under its separate `accounts/` directory.
4. Store passive/active inventory under `recon/`.
5. Store raw baseline/control/candidate requests under `requests/` and resulting state under `states/`.
6. Redact all secrets and third-party data before sharing evidence.
7. Record cleanup under `cleanup/`.
DOC
} > "$ROOT/README.md"

printf '%s\n' "$ROOT"
