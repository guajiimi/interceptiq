# InterceptIQ — Codex for Open Source Submission

## What It Is

InterceptIQ is a zero-dependency, pure Python 3.10+ CLI toolkit that converts raw browser/network captures (HAR, Playwright traces, WebSocket frames) into structured JSON artifacts optimized for AI coding agents.

## The Problem

When building web scrapers, bots, or automation scripts, the first step is understanding the target site's API structure, payload encoding, DOM selectors, and data flow. This requires manually sifting through megabytes of raw browser capture data — a task that's tedious for humans and incomprehensible to AI agents without preprocessing.

## How InterceptIQ Solves It

InterceptIQ provides five focused commands that form a **capture → analyze → build** pipeline:

| Command | Input | Output | Purpose |
|---------|-------|--------|---------|
| `payload-analyze` | Capture JSON | Endpoint classification JSON | Decodes JSON, form data, base64, hex, gzip hints, and flags crypto signatures |
| `dom-analyze` | Capture JSON | DOM structure JSON | Extracts forms, links, inputs, images, and CSS selector candidates |
| `replay-generate` | Capture JSON | Replay plan + Python script | Generates a ready-to-run scraper with safe header templates |
| `agent-brief` | Capture JSON | Agent context JSON | Produces a machine-readable brief with endpoint cards and an agent prompt |
| `jsonl-dedupe` | JSONL file | Deduplicated JSONL | Key-based deduplication for data pipelines |

## Technical Design Decisions

**Zero dependencies.** The entire toolkit uses only Python stdlib (`json`, `re`, `base64`, `gzip`, `urllib`, `argparse`, `pathlib`). No `pip install` bloat, no supply-chain risk, no version conflicts. This matters for AI agents that need to use the tool immediately without environment setup.

**JSON in, JSON out.** Every command reads a JSON file and writes a JSON result. This makes InterceptIQ composable — outputs can be piped into `jq`, consumed by other tools, or directly pasted into an AI agent's context window.

**Privacy by default.** Sensitive headers (authorization, cookies, API keys) are automatically redacted from analysis output and stripped from generated scraper code. No credentials leak into agent prompts or logs.

**Agent-first output.** The `agent-brief` command doesn't just summarize — it produces a structured prompt with endpoint cards, recommended workflow steps, and a copy-paste agent prompt that works with Codex, Claude Code, and Hermes Agent.

## Why This Matters for AI Coding Agents

AI agents like Codex and Claude Code are powerful but context-limited. They can't parse a 50MB HAR file or visually inspect browser DevTools. InterceptIQ bridges this gap by:

1. **Reducing context size** — From megabytes of raw capture to kilobytes of focused JSON
2. **Providing actionable structure** — Endpoint cards, selector hints, replay plans instead of raw data
3. **Enabling autonomous workflows** — Agents can run InterceptIQ commands, read the JSON output, and make implementation decisions without human intervention
4. **Safe by construction** — Generated code never includes credentials, so agents can iterate without supervision

## Project Health

- **Tests:** 4 tests covering all core modules, run via `pytest`
- **CI:** GitHub Actions testing on Python 3.10, 3.11, 3.12, 3.13
- **Documentation:** README, contributing guide, agent workflow guide, real-world demo
- **Zero external dependencies:** Nothing to break or maintain
- **Active development:** Regular releases with changelog

## Repository

https://github.com/guajiimi/interceptiq
