#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="$(basename "$ROOT")"
OUT="${1:-$ROOT/dist/$NAME.zip}"

mkdir -p "$(dirname "$OUT")"
rm -f "$OUT" "$OUT.sha256"

(
  cd "$(dirname "$ROOT")"
  zip -r "$OUT" "$NAME" \
    -x "$NAME/.git/*" \
       "$NAME/dist/*" \
       "$NAME/__pycache__/*" \
       "$NAME/*/__pycache__/*" \
       "$NAME/*/*/__pycache__/*" \
       "*.pyc" \
       "*.DS_Store" \
       "$NAME/report.json" \
       "$NAME/report.md"
)

sha256sum "$OUT" > "$OUT.sha256"
echo "ZIP: $OUT"
echo "SHA256: $(cut -d' ' -f1 "$OUT.sha256")"
ls -lh "$OUT"
