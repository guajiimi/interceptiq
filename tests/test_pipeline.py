import json
from pathlib import Path
from interceptiq.payload_analyze import analyze_intercept as payload
from interceptiq.dom_analyze import analyze_intercept as dom
from interceptiq.jsonl_pipeline import dedupe_jsonl
from interceptiq.agent_report import build_agent_brief


def test_payload_analysis_detects_endpoint():
    data = json.loads(Path("examples/intercept.example.json").read_text())
    result = payload(data)
    assert result["ok"] is True
    assert result["summary"]["endpoints_analyzed"] >= 1


def test_dom_analysis_extracts_form_and_link():
    data = json.loads(Path("examples/intercept.example.json").read_text())
    result = dom(data)
    assert result["summary"]["forms"] == 1
    assert result["summary"]["links"] == 1


def test_agent_brief_contains_agent_prompt():
    data = json.loads(Path("examples/intercept.example.json").read_text())
    result = build_agent_brief(data)
    assert result["ok"] is True
    assert "agent_prompt" in result["agent_workflow"]
    assert result["endpoint_cards"]


def test_jsonl_dedupe(tmp_path):
    out = tmp_path / "clean.jsonl"
    result = dedupe_jsonl("examples/items.raw.jsonl", "id", out)
    assert result["input_count"] == 3
    assert result["output_count"] == 2
