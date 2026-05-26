# Project Description

I built InterceptIQ, a JSON-first web interception analysis toolkit that converts browser and network capture artifacts into practical scraper and bot-building assets.

The project focuses on a real automation workflow: analyzing endpoints, classifying payload formats, extracting DOM selector candidates, generating replay plans, and keeping all output in JSON/JSONL for easy debugging and reuse. It includes payload analysis, DOM analysis, replay generation, and JSONL deduplication utilities.

I designed it to be useful for legitimate debugging and automation development while avoiding credential leakage: sensitive headers such as cookies, authorization tokens, and API keys are omitted or redacted from generated artifacts.
