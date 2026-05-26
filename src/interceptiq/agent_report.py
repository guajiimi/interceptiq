import json
from pathlib import Path


def build_agent_brief(data):
    """Create an AI-agent friendly project brief from an intercept artifact."""
    summary = data.get("summary", {})
    endpoints = data.get("endpoints", []) + data.get("entries", [])
    frames = data.get("frames", [])
    target = data.get("target")

    endpoint_cards = []
    for entry in endpoints[:10]:
        req = entry.get("request", entry)
        resp = entry.get("response", {})
        endpoint_cards.append({
            "method": req.get("method", "GET"),
            "url": req.get("url"),
            "status": resp.get("status"),
            "agent_task": "Classify whether this endpoint should be replayed directly or scraped through browser automation.",
        })

    return {
        "ok": True,
        "source": "interceptiq.agent_report",
        "target": target,
        "agent_workflow": {
            "goal": "Help an AI coding agent convert an intercept capture into a reliable scraper or bot implementation.",
            "recommended_steps": [
                "Run payload-analyze to classify request/response payload formats and signing clues.",
                "Run dom-analyze to identify selector candidates, forms, links, frames, and extraction targets.",
                "Run replay-generate for the most promising endpoint and review generated replay-plan.json.",
                "Use jsonl-dedupe for record streams and checkpoints.",
                "Iterate with an AI agent using the JSON outputs as machine-readable context.",
            ],
            "agent_prompt": (
                "You are given InterceptIQ JSON artifacts. Decide whether API replay, WebSocket replay, "
                "or DOM automation is the best strategy. Produce a safe scraper/bot plan using JSON for "
                "debug artifacts and JSONL for output records. Do not include secrets in code or logs."
            ),
        },
        "capture_summary": summary,
        "endpoint_cards": endpoint_cards,
        "frame_count": len(frames),
        "outputs_expected": [
            "payload-analysis.json",
            "dom-analysis.json",
            "replay-plan.json",
            "replay_scraper.py",
            "items.jsonl",
        ],
    }
