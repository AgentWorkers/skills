#!/usr/bin/env bash
# clicky.sh — Fetch analytics from Clicky API
# Usage: clicky.sh <site_name|--id ID --key KEY> <type> [options]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SITES_FILE="$SCRIPT_DIR/../references/sites.json"
API_URL="https://api.clicky.com/api/stats/4"

SITE_ID=""
SITEKEY=""
TYPE=""
DATE="today"
LIMIT="50"
DAILY=""
OUTPUT="json"
PAGE=""

# Parse first arg — site name or --id
if [[ "${1:-}" == "--id" ]]; then
  SITE_ID="$2"
  shift 2
  if [[ "${1:-}" == "--key" ]]; then
    SITEKEY="$2"
    shift 2
  else
    echo "Error: --id requires --key" >&2; exit 1
  fi
else
  # Look up site by name
  SITE_NAME="${1:?Usage: clicky.sh <site_name> <type> [options]}"
  shift
  if [[ -f "$SITES_FILE" ]]; then
    SITE_ID=$(python3 -c "
import json, sys
sites = json.load(open('$SITES_FILE'))
for s in sites:
    if s['name'] == '$SITE_NAME' or s.get('domain','').startswith('$SITE_NAME'):
        print(s['site_id']); sys.exit(0)
print(''); sys.exit(1)
" 2>/dev/null) || true
    SITEKEY=$(python3 -c "
import json, sys
sites = json.load(open('$SITES_FILE'))
for s in sites:
    if s['name'] == '$SITE_NAME' or s.get('domain','').startswith('$SITE_NAME'):
        print(s['sitekey']); sys.exit(0)
print(''); sys.exit(1)
" 2>/dev/null) || true
  fi
  if [[ -z "$SITE_ID" || -z "$SITEKEY" ]]; then
    echo "Error: Site '$SITE_NAME' not found in $SITES_FILE" >&2
    echo "Available sites:" >&2
    python3 -c "import json; [print(f\"  {s['name']} ({s.get('domain','')})\") for s in json.load(open('$SITES_FILE'))]" 2>/dev/null
    exit 1
  fi
fi

TYPE="${1:?Missing type (e.g. visitors,pages,countries)}"
shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --date)    DATE="$2"; shift 2 ;;
    --limit)   LIMIT="$2"; shift 2 ;;
    --daily)   DAILY="1"; shift ;;
    --output)  OUTPUT="$2"; shift 2 ;;
    --page)    PAGE="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

URL="${API_URL}?site_id=${SITE_ID}&sitekey=${SITEKEY}&type=${TYPE}&date=${DATE}&limit=${LIMIT}&output=${OUTPUT}"
[[ -n "$DAILY" ]] && URL="${URL}&daily=1"
[[ -n "$PAGE" ]] && URL="${URL}&page=${PAGE}"

curl -s "$URL"
