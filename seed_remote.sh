#!/usr/bin/env bash
set -euo pipefail

BASE=http://localhost:8000
URLS=(
  "https://file.notion.so/f/f/…/soap_01.txt?downloadName=soap_01.txt"
  "https://file.notion.so/f/f/…/soap_02.txt?downloadName=soap_02.txt"
  "https://file.notion.so/f/f/…/soap_03.txt?downloadName=soap_03.txt"
  "https://file.notion.so/f/f/…/soap_04.txt?downloadName=soap_04.txt"
  "https://file.notion.so/f/f/…/soap_05.txt?downloadName=soap_05.txt"
  "https://file.notion.so/f/f/…/soap_06.txt?downloadName=soap_06.txt"
)

for url in "${URLS[@]}"; do
  # pull the raw text
  raw=$(curl -s "$url")
  # escape newlines for JSON
  content=$(printf "%s" "$raw" | sed ':a;N;$!ba;s/\n/\\n/g')
  # derive a title from the final downloadName parameter
  title=$(echo "$url" | sed -E 's/.*downloadName=([^&]+).*/\1/')
  echo "→ Seeding $title"
  curl -s -X POST "$BASE/documents" \
    -H "Content-Type: application/json" \
    -d "{\"title\":\"$title\",\"content\":\"$content\"}" \
    && echo "  ✔ OK" || echo "  ✘ FAIL"
done
