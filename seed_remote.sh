#!/usr/bin/env bash
set -euo pipefail

BASE="http://localhost:8000"

for file in data/soap_*.txt; do
  title=$(basename "$file")
  echo "Seeding $title…"
  # Read entire file as a JSON string
  content=$(jq -Rs . < "$file")
  # Build the payload
  payload=$(jq -n --arg t "$title" --argjson c "$content" '{title: $t, content: $c}')
  # POST to /documents
  curl -s -X POST "$BASE/documents" \
    -H "Content-Type: application/json" \
    -d "$payload" \
  | jq
done
