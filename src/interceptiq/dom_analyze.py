import re
from collections import Counter

TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9-]*)\b([^>]*)>")
ATTR_RE = re.compile(r"([:\w-]+)=[\"']([^\"']{1,160})[\"']")


def attrs(raw):
    return dict(ATTR_RE.findall(raw or ""))


def analyze_html(html):
    tags = []
    links = []
    images = []
    forms = []
    inputs = []
    selector_hints = []

    for tag, raw in TAG_RE.findall(html or ""):
        tag = tag.lower()
        a = attrs(raw)
        tags.append(tag)

        if tag == "a" and a.get("href"):
            links.append({"text": "", "href": a.get("href")})
        if tag == "img" and a.get("src"):
            images.append({"src": a.get("src"), "alt": a.get("alt", "")})
        if tag == "form":
            forms.append({"action": a.get("action", ""), "method": a.get("method", "GET")})
        if tag in ("input", "textarea", "select"):
            inputs.append({"tag": tag, "name": a.get("name", ""), "type": a.get("type", "")})

        for key in ("id", "data-testid", "data-test", "aria-label", "name"):
            if a.get(key):
                selector_hints.append({"selector": f'[{key}="{a[key]}"]', "reason": key})

    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text).strip()[:1200]
    return {
        "tag_counts": dict(Counter(tags).most_common(20)),
        "links": links[:50],
        "images": images[:50],
        "forms": forms[:20],
        "inputs": inputs[:50],
        "selector_hints": selector_hints[:80],
        "visible_text_sample": text,
    }


def analyze_intercept(data):
    dom = data.get("dom_snapshot") or {}
    frames = data.get("frames") or []
    main = analyze_html(dom.get("html", ""))
    frame_reports = []
    for frame in frames[:20]:
        frame_reports.append({
            "url": frame.get("url"),
            "name": frame.get("name"),
            "analysis": analyze_html(frame.get("html_preview", "")),
        })
    return {
        "ok": True,
        "source": "interceptiq.dom_analyze",
        "target": data.get("target"),
        "summary": {
            "frame_count": len(frames),
            "forms": len(main["forms"]),
            "links": len(main["links"]),
            "images": len(main["images"]),
        },
        "main_document": main,
        "frames": frame_reports,
        "selector_strategy": [
            "Prefer stable ids/data-testid/name/aria-label.",
            "Avoid generated hash classes when possible.",
            "Use repeated structures for list/card extraction.",
        ],
    }
