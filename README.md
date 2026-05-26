# InterceptIQ

InterceptIQ is a JSON-first analysis toolkit for turning browser/network capture artifacts into practical scraper and bot-building assets.

It focuses on the workflow developers actually need after intercepting a website:

1. Understand which endpoints matter.
2. Identify payload formats and signing/encryption clues.
3. Extract DOM selector candidates from captured HTML.
4. Generate a replay plan and starter scraper script.
5. Keep all debug artifacts in JSON and stream data records as JSONL.

> InterceptIQ is designed for legitimate debugging, automation prototyping, and data extraction on systems you are allowed to access. It redacts sensitive headers by default and avoids storing credentials in generated code.

## Features

- Payload analysis: JSON, form data, base64/base64url, gzip hints, hex/hash-like values, crypto/signature keywords.
- DOM analysis: links, images, forms, inputs, tables, iframe/frame previews, visible text, selector hints.
- Replay generation: produces a `replay-plan.json` and a starter Python scraper using safe header templates.
- JSONL utilities: append-friendly data pipeline with key-based deduplication.
- Zero database overhead: JSON for debug/config/analysis, JSONL for record streams.

## Quick Start

```bash
python -m pip install -e .
interceptiq payload-analyze examples/intercept.example.json
interceptiq dom-analyze examples/intercept.example.json
interceptiq replay-generate examples/intercept.example.json --out-dir /tmp/interceptiq-replay
interceptiq jsonl-dedupe examples/items.raw.jsonl --key id --out /tmp/items.clean.jsonl
```

## Demo Dashboard

Open `docs/demo/index.html` in a browser to see a static visual summary of the pipeline.

## Project Structure

```text
src/interceptiq/
  cli.py
  payload_analyze.py
  dom_analyze.py
  replay_generate.py
  jsonl_pipeline.py
examples/
  intercept.example.json
  items.raw.jsonl
docs/demo/index.html
```

## Submission Description

See `docs/submission/description.md` for a concise project description that can be used as proof text.
