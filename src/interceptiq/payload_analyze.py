import base64
import binascii
import gzip
import json
import re
from urllib.parse import parse_qs

SECRET_KEYS = re.compile(r"authorization|cookie|token|secret|api[-_]?key|password|session", re.I)
CRYPTO_HINTS = [
    "crypto.subtle", "CryptoJS", "AES", "RSA", "Hmac", "SHA256",
    "signature", "nonce", "timestamp", "btoa", "atob", "pako",
    "protobuf", "msgpack", "encrypt", "decrypt",
]


def redact(value):
    if isinstance(value, dict):
        return {
            k: ("[REDACTED]" if SECRET_KEYS.search(str(k)) else redact(v))
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def classify_text(text):
    labels = []
    sample = text[:5000] if isinstance(text, str) else ""
    stripped = sample.strip()
    if not stripped:
        return labels

    try:
        json.loads(stripped)
        labels.append("json")
    except Exception:
        pass

    if "=" in stripped and "&" in stripped:
        try:
            parse_qs(stripped)
            labels.append("form-urlencoded")
        except Exception:
            pass

    compact = re.sub(r"\s+", "", stripped)
    if len(compact) >= 16 and re.fullmatch(r"[A-Za-z0-9_\-/+=]+", compact):
        try:
            raw = base64.urlsafe_b64decode(compact + "=" * ((4 - len(compact) % 4) % 4))
            if raw:
                labels.append("base64/base64url")
            try:
                gzip.decompress(raw)
                labels.append("gzip-after-base64")
            except Exception:
                pass
        except (binascii.Error, ValueError):
            pass

    if re.fullmatch(r"[a-fA-F0-9]{32,}", compact):
        labels.append("hex-or-hash-like")

    for hint in CRYPTO_HINTS:
        if hint.lower() in sample.lower():
            labels.append(f"crypto-clue:{hint}")
    return sorted(set(labels))


def analyze_intercept(data):
    entries = data.get("entries", []) + data.get("endpoints", [])
    findings = []
    crypto = []

    for entry in entries:
        req = entry.get("request", entry)
        resp = entry.get("response", {})
        texts = []
        for side in (req, resp):
            body = side.get("body") or side.get("post_data") or side.get("text")
            if isinstance(body, (dict, list)):
                body = json.dumps(body, ensure_ascii=False)
            if isinstance(body, str):
                texts.append(body)

        labels = []
        for text in texts:
            labels.extend(classify_text(text))

        if labels:
            crypto.extend([x for x in labels if x.startswith("crypto-clue")])
            findings.append({
                "method": req.get("method"),
                "url": req.get("url"),
                "status": resp.get("status"),
                "labels": sorted(set(labels)),
                "replayability": "needs-review" if any("crypto" in x or "signature" in x for x in labels) else "likely-replayable",
            })

    return {
        "ok": True,
        "source": "interceptiq.payload_analyze",
        "target": data.get("target"),
        "summary": {
            "entries": len(entries),
            "endpoints_analyzed": len(findings),
            "crypto_labels": sorted(set(crypto)),
        },
        "findings": findings,
        "notes": ["Secrets are redacted; do not paste live credentials into reports."],
    }
