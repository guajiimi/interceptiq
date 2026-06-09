#!/usr/bin/env bash
# Set GitHub repository topics for interceptiq
# Requires: gh CLI authenticated (gh auth login)
# Usage: bash scripts/set-github-topics.sh [owner/repo]

set -euo pipefail

REPO="${1:-guajiimi/interceptiq}"

echo "Setting topics for $REPO ..."

gh api -X PUT "repos/$REPO/topics" \
  -f topics[]='ai-agents' \
  -f topics[]='web-scraping' \
  -f topics[]='json' \
  -f topics[]='automation' \
  -f topics[]='playwright' \
  -f topics[]='har' \
  -f topics[]='websocket' \
  -f topics[]='cli' \
  -f topics[]='developer-tools' \
  -f topics[]='codex' \
  -f topics[]='openai' \
  -f topics[]='agent-toolkit' \
  -f topics[]='web-interception' \
  -f topics[]='scraper-generator'

echo "Done. Topics set:"
gh api "repos/$REPO/topics" --jq '.names[]'
