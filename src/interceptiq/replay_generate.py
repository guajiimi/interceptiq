import json
from pathlib import Path

DROP_HEADERS = {"authorization", "cookie", "set-cookie", "x-api-key", "x-csrf-token"}


def safe_headers(headers):
    out = {}
    for k, v in (headers or {}).items():
        if k.lower() not in DROP_HEADERS:
            out[k] = v
    return out


def pick_endpoint(data):
    entries = data.get("endpoints", []) + data.get("entries", [])
    if not entries:
        return None
    return sorted(
        entries,
        key=lambda e: (0 if (e.get("request", e).get("method") or "GET") != "GET" else 1),
    )[0]


def generate(data, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    item = pick_endpoint(data)
    if not item:
        plan = {"ok": False, "error": "no endpoints found"}
        (out / "replay-plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
        return plan

    req = item.get("request", item)
    url = req.get("url", data.get("target"))
    method = req.get("method", "GET")
    headers = safe_headers(req.get("headers", {}))

    script = f'''#!/usr/bin/env python3
import json
from pathlib import Path
import urllib.request

URL = {url!r}
OUT = Path("items.jsonl")


def main():
    req = urllib.request.Request(URL, method={method!r})
    for k, v in {headers!r}.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", "replace")
    try:
        data = json.loads(body)
        records = data if isinstance(data, list) else [data]
        with OUT.open("a", encoding="utf-8") as f:
            for item in records:
                f.write(json.dumps(item, ensure_ascii=False) + "\\n")
        print(json.dumps({{"ok": True, "count": len(records), "output": str(OUT)}}))
    except Exception:
        print(json.dumps({{"ok": True, "text_preview": body[:1000]}}))


if __name__ == "__main__":
    main()
'''
    plan = {
        "ok": True,
        "source": "interceptiq.replay_generate",
        "target": data.get("target"),
        "selected_endpoint": {"method": method, "url": url},
        "outputs": {"script": str(out / "replay_scraper.py"), "items_jsonl": str(out / "items.jsonl")},
        "notes": [
            "Authorization/cookie headers are intentionally omitted.",
            "Use JSON for debug artifacts and JSONL for records.",
        ],
    }
    (out / "replay-plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    sp = out / "replay_scraper.py"
    sp.write_text(script, encoding="utf-8")
    sp.chmod(0o755)
    return plan
