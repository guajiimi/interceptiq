<div align="center">

# ⚡ InterceptIQ

**JSON-first web interception toolkit for AI coding agents**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)
[![Zero Dependencies](https://img.shields.io/badge/deps-zero-ff69b4.svg)](pyproject.toml)

Turn messy browser captures → structured JSON briefs, replay plans, and scraper scaffolds.

*Designed for [Codex](https://openai.com/index/codex/), [Claude Code](https://claude.ai), [Hermes Agent](https://github.com/nousresearch/hermes-agent), and any AI coding agent that needs structured context before building automation.*

</div>

---

## Why InterceptIQ?

When you intercept a website's traffic (HAR, Playwright traces, WebSocket frames), you get **megabytes of raw noise**. AI agents can't work with that — they need structured context.

InterceptIQ bridges the gap:

```
Browser capture (HAR/JSON) → InterceptIQ → Agent-ready JSON brief
                                     ├── Endpoint cards with payload analysis
                                     ├── DOM selector candidates
                                     ├── Replay plan + starter scraper
                                     └── JSONL data pipeline
```

## Features

| Command | What it does |
|---------|-------------|
| `payload-analyze` | Decode JSON, form data, base64, gzip hints, hex values, crypto signatures from request/response payloads |
| `dom-analyze` | Extract links, forms, inputs, tables, iframes, selector hints from captured HTML |
| `replay-generate` | Generate `replay-plan.json` + starter Python scraper with safe header templates |
| `agent-brief` | Create an `agent-brief.json` with goals, endpoint cards, next steps, and a ready-to-use AI agent prompt |
| `jsonl-dedupe` | Key-based deduplication for JSONL record streams |

## Quick Start

```bash
# Install (zero dependencies — pure Python)
pip install interceptiq

# Or from source
git clone https://github.com/guajiimi/interceptiq.git
cd interceptiq && pip install -e .
```

### CLI Usage

```bash
# Analyze request/response payloads
interceptiq payload-analyze capture.json

# Extract DOM structure and selector hints
interceptiq dom-analyze capture.json

# Generate replay plan + starter scraper
interceptiq replay-generate capture.json --out-dir ./replay

# Create AI agent brief
interceptiq agent-brief capture.json -o agent-brief.json

# Deduplicate JSONL records
interceptiq jsonl-dedupe data.jsonl --key id --out clean.jsonl
```

### Python API

```python
from interceptiq.payload_analyze import analyze_intercept as payload_analyze
from interceptiq.dom_analyze import analyze_intercept as dom_analyze
from interceptiq.agent_report import build_agent_brief
import json

capture = json.loads(open("capture.json").read())

# Get structured payload analysis
payload_result = payload_analyze(capture)

# Get DOM selectors and structure
dom_result = dom_analyze(capture)

# Generate agent-ready brief
brief = build_agent_brief(capture)
```

## AI Agent Workflow

InterceptIQ is built for the **capture → analyze → build** loop:

1. **Capture** — Record traffic with Playwright, browser DevTools, or a HAR proxy
2. **Analyze** — Run `interceptiq payload-analyze` and `interceptiq dom-analyze`
3. **Brief** — Generate `agent-brief.json` with `interceptiq agent-brief`
4. **Build** — Paste the brief into Codex / Claude Code / Hermes Agent as structured context
5. **Iterate** — The agent writes a scraper; refine with `replay-generate` output

See [`docs/agent-workflow.md`](docs/agent-workflow.md) for the full guide.

## Project Structure

```
interceptiq/
├── src/interceptiq/
│   ├── cli.py              # CLI entry point
│   ├── payload_analyze.py  # Request/response payload decoder
│   ├── dom_analyze.py      # HTML DOM structure extractor
│   ├── replay_generate.py  # Replay plan + scraper generator
│   ├── agent_report.py     # AI agent brief builder
│   ├── jsonl_pipeline.py   # JSONL dedup + append pipeline
│   └── __init__.py
├── examples/
│   ├── intercept.example.json
│   └── items.raw.jsonl
├── docs/
│   ├── agent-workflow.md
│   └── demo/index.html     # Visual dashboard demo
├── tests/
│   └── test_pipeline.py
├── pyproject.toml
└── LICENSE
```

## Demo Dashboard

Open [`docs/demo/index.html`](docs/demo/index.html) in a browser to see a visual summary of the analysis pipeline.

![Dashboard Screenshot](docs/screenshots/dashboard.png)

## Design Philosophy

- **Zero dependencies** — Pure Python 3.10+, no `pip install` bloat
- **JSON in, JSON out** — Every command reads JSON and writes JSON
- **Agent-first** — Output is structured for AI consumption, not human eyeballs
- **Privacy-aware** — Sensitive headers are redacted by default; no credentials in generated code
- **JSONL for streams** — Append-friendly, deduplication-ready data pipeline

## Contributing

PRs welcome! See the [issues](https://github.com/guajiimi/interceptiq/issues) for planned work.

```bash
# Development setup
git clone https://github.com/guajiimi/interceptiq.git
cd interceptiq
pip install -e ".[dev]"

# Run tests
pytest
```

## License

[MIT](LICENSE) — use it however you want.

---

<div align="center">

**Built for the AI agent era** ⚡

</div>
