# Project Description

I built InterceptIQ, a JSON-first AI-agent workflow toolkit that converts browser and network capture artifacts into practical scraper and bot-building assets.

The project focuses on a real agent automation workflow: analyzing endpoints, classifying payload formats, extracting DOM selector candidates, generating AI-agent briefs, generating replay plans, and keeping all output in JSON/JSONL for easy debugging and reuse. It includes payload analysis, DOM analysis, agent brief generation, replay generation, and JSONL deduplication utilities.

I designed it so Codex/Hermes-style agents can consume structured JSON context, decide whether API replay or DOM automation is better, and generate safe implementation plans without leaking credentials. Sensitive headers such as cookies, authorization tokens, and API keys are omitted or redacted from generated artifacts.
