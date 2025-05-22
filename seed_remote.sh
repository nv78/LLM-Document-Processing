# # #!/usr/bin/env bash
# # set -euo pipefail

# # BASE="http://localhost:8000"

# # files = [
# #   "data/soap_01.txt",
# #   "data/soap_02.txt"
# # ]

# # for file in data/soap_*.txt; do
# #   title=$(basename "$file")
# #   echo "Seeding $title…"
# #   # Read entire file as a JSON string
# #   content=$(jq -Rs . < "$file")
# #   # Build the payload
# #   payload=$(jq -n --arg t "$title" --argjson c "$content" '{title: $t, content: $c}')
# #   # POST to /documents
# #   curl -s -X POST "$BASE/documents" \
# #     -H "Content-Type: application/json" \
# #     -d "$payload" \
# #   | jq
# # done

# #!/usr/bin/env bash
# set -euo pipefail

# BASE="http://localhost:8000"

# # Hard-coded list of files
# files=(
#   "data/soap_01.txt"
#   "data/soap_02.txt"
#   "data/soap_03.txt"
#   "data/soap_04.txt"
#   "data/soap_05.txt"
#   "data/soap_06.txt"
# )

# for file in "${files[@]}"; do
#   title=$(basename "$file")
#   echo "Seeding $title…"
#   # Read entire file as a JSON-escaped string
#   content=$(jq -Rs . < "$file")
#   # Build the JSON payload
#   payload=$(jq -n --arg t "$title" --argjson c "$content" '{title: $t, content: $c}')
#   # POST to /documents
#   curl -s -X POST "$BASE/documents" \
#     -H "Content-Type: application/json" \
#     -d "$payload" \
#   | jq
# done

#!/usr/bin/env bash
set -euo pipefail

BASE="http://localhost:8000"

# 1) Proper Bash array — no spaces around =, no Python-style brackets
files=(
  "data/soap_01.txt"
  "data/soap_02.txt"
  "data/soap_03.txt"
  "data/soap_04.txt"
  "data/soap_05.txt"
  "data/soap_06.txt"
)

# 2) Loop over that array
for file in "${files[@]}"; do
  # Make sure the file actually exists
  if [[ ! -f "$file" ]]; then
    echo "⚠️  File not found: $file" >&2
    continue
  fi

  title="$(basename "$file")"
  echo "Seeding $title…"

  # Read entire file as a JSON-escaped string
  content=$(jq -Rs . < "$file")

  # Build the JSON payload
  payload=$(jq -n --arg t "$title" --argjson c "$content" \
    '{title: $t, content: $c}')

  # POST to /documents and pretty-print response
  curl -s -X POST "$BASE/documents" \
    -H "Content-Type: application/json" \
    -d "$payload" \
  | jq
done
