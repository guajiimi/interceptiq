# InterceptIQ Agent Workflow

InterceptIQ is intentionally built for AI-agent workflows, not just manual scraping.

## Problem

Browser interception produces noisy artifacts: endpoints, frames, payloads, scripts, forms, WebSocket messages, and DOM snapshots. An AI coding agent needs this context in a structured format before it can decide how to build a reliable scraper or bot.

## Agent Loop

1. Capture browser/network behavior with an intercept tool.
2. Save the result as JSON.
3. Run InterceptIQ analyzers:
   - `payload-analyze`
   - `dom-analyze`
   - `agent-brief`
   - `replay-generate`
4. Feed the resulting JSON files back into a coding agent.
5. The agent chooses API replay, DOM automation, or a hybrid approach.
6. The generated bot/scraper writes item streams as JSONL.

## Why This Is AI/Agent-Oriented

- Every command outputs machine-readable JSON for agent context.
- `agent-brief` turns intercept artifacts into a task brief an AI coding agent can use directly.
- Replay plans avoid credential leakage and give the agent explicit implementation boundaries.
- JSONL output supports incremental monitoring, dedupe, and future agent review.

## Example

```bash
interceptiq payload-analyze examples/intercept.example.json -o /tmp/payload-analysis.json
interceptiq dom-analyze examples/intercept.example.json -o /tmp/dom-analysis.json
interceptiq agent-brief examples/intercept.example.json -o /tmp/agent-brief.json
interceptiq replay-generate examples/intercept.example.json --out-dir /tmp/replay
```

The generated `agent-brief.json` contains:

- agent goal
- recommended next steps
- agent prompt
- endpoint cards
- expected outputs
