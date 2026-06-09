# Real-World Demo: End-to-End InterceptIQ Workflow

This walkthrough demonstrates using InterceptIQ to convert a browser capture into a fully functional scraper, step by step.

## Prerequisites

```bash
pip install interceptiq
# or: git clone ... && cd interceptiq && pip install -e .
```

## Step 1: Obtain a Capture

Record traffic from your target site using Playwright, browser DevTools (Network tab → "Save all as HAR"), or a proxy like mitmproxy. Save the capture as `capture.json`.

InterceptIQ expects a JSON file with this structure:

```json
{
  "ok": true,
  "target": "https://example.test",
  "dom_snapshot": { "url": "https://example.test", "html": "<html>...</html>" },
  "frames": [],
  "endpoints": [
    {
      "request": {
        "method": "POST",
        "url": "https://example.test/api/search",
        "headers": { "content-type": "application/json", "authorization": "Bearer ..." },
        "body": { "q": "search term" }
      },
      "response": { "status": 200, "content_type": "application/json", "body": { "items": [] } }
    }
  ],
  "entries": []
}
```

## Step 2: Analyze Payloads

```bash
interceptiq payload-analyze capture.json -o payload-analysis.json
```

This classifies every request/response body (JSON, form-urlencoded, base64, hex, crypto signatures) and flags endpoints that may need special replay handling.

**Key output fields:**
- `findings[].labels` — detected payload formats
- `findings[].replayability` — `"likely-replayable"` or `"needs-review"`
- `summary.crypto_labels` — crypto/signature clues found

## Step 3: Extract DOM Structure

```bash
interceptiq dom-analyze capture.json -o dom-analysis.json
```

Parses captured HTML and extracts:
- Forms with action URLs and methods
- Links and images
- Input fields with name/type
- Selector hints (`data-testid`, `id`, `aria-label`, `name`)
- Visible text sample

## Step 4: Generate Agent Brief

```bash
interceptiq agent-brief capture.json -o agent-brief.json
```

Creates a machine-readable brief containing:
- Endpoint cards with method, URL, status
- Agent workflow with recommended steps
- Ready-to-paste agent prompt for Codex/Claude Code
- List of expected output artifacts

**Paste this into your AI agent:**
> "You are given InterceptIQ JSON artifacts. Decide whether API replay, WebSocket replay, or DOM automation is the best strategy. Produce a safe scraper/bot plan..."

## Step 5: Generate Replay Plan

```bash
interceptiq replay-generate capture.json --out-dir ./replay
```

Produces:
- `replay/replay-plan.json` — endpoint details, notes
- `replay/replay_scraper.py` — ready-to-run Python script using `urllib`

The generated scraper uses only stdlib (`urllib.request`) and writes output to `items.jsonl`. Sensitive headers are automatically stripped.

## Step 6: Run and Deduplicate

```bash
# Run the generated scraper
python replay/replay_scraper.py

# Deduplicate output
interceptiq jsonl-dedupe replay/items.jsonl --key id --out replay/clean.jsonl
```

## Complete Pipeline (One-Liner)

```bash
interceptiq payload-analyze capture.json | jq .summary
interceptiq dom-analyze capture.json | jq .summary
interceptiq agent-brief capture.json -o agent-brief.json
interceptiq replay-generate capture.json --out-dir ./replay
# ... run scraper ...
interceptiq jsonl-dedupe replay/items.jsonl --key id --out replay/clean.jsonl
```

## Using with AI Agents

The recommended workflow with Codex, Claude Code, or Hermes Agent:

1. **Capture** traffic and save as JSON
2. **Run all InterceptIQ commands** to produce analysis JSON files
3. **Paste the agent-brief.json** into your AI agent's context
4. **Let the agent** decide replay vs. DOM automation strategy
5. **Refine** using the generated replay plan and scraper as a starting point
6. **Iterate** — re-run with updated captures as the site changes

All InterceptIQ output is JSON — machine-readable, diffable, and composable with other tools in your pipeline.
