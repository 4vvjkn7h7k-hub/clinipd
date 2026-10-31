#!/usr/bin/env bash
# deploy.sh — put the site live, with the checks that stop you shipping
# the wrong folder. Run it from anywhere:   ./_build/deploy.sh
set -euo pipefail

SITE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SITE"

echo
echo "  Folder    $SITE"

# --- is this actually the site? ---------------------------------------
if [ ! -f index.html ]; then
  echo "  ERROR     no index.html here. This is not the site folder."; echo; exit 1
fi
if grep -q "Physio Atlas" index.html; then
  echo "  ERROR     index.html is the OLD Physio Atlas build."
  echo "            You are in a stale folder. Unzip the latest build."; echo; exit 1
fi
if ! grep -q "for physios" index.html; then
  echo "  ERROR     index.html is not the current CliniPD home page."; echo; exit 1
fi

# --- enough files to be the whole site? -------------------------------
find . -name ".DS_Store" -delete 2>/dev/null || true
N=$(find . -type f -not -path './_build/*' | wc -l | tr -d ' ')
echo "  Files     $N"
if [ "$N" -lt 1000 ]; then
  echo "  ERROR     only $N files — the site has ~1100."
  echo "            You are deploying a partial or empty folder. Stopping."; echo; exit 1
fi

# --- how much is actually written? ------------------------------------
if [ -f content/index.json ]; then
  W=$(python3 -c "import json,io;d=json.load(io.open('content/index.json'));print(sum(1 for v in d.values() if v.get('sections')))" 2>/dev/null || echo "?")
  echo "  Written   $W page(s) have content"
fi

echo "  Target    clinipd  ·  branch main  ·  PRODUCTION"
echo
read -r -p "  Deploy? [y/N] " ok
[ "$ok" = "y" ] || [ "$ok" = "Y" ] || { echo "  Cancelled."; echo; exit 0; }

# --- keep the build scripts out of the public site --------------------
TMP="$(mktemp -d)"
[ -d _build ] && mv _build "$TMP/_build"
restore() { [ -d "$TMP/_build" ] && mv "$TMP/_build" "$SITE/_build" || true; rmdir "$TMP" 2>/dev/null || true; }
trap restore EXIT

npx wrangler pages deploy . --project-name clinipd --branch main

echo
echo "  Done. Check https://clinipd.com  (Cmd+Shift+R to beat the cache)"
echo
