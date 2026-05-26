import json
from pathlib import Path


def dedupe_jsonl(src, key, out):
    src = Path(src)
    out = Path(out)
    seen = set()
    count_in = 0
    count_out = 0
    out.parent.mkdir(parents=True, exist_ok=True)
    with src.open(encoding="utf-8") as fin, out.open("w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            count_in += 1
            item = json.loads(line)
            ident = item.get(key) if isinstance(item, dict) else None
            if ident is None:
                ident = json.dumps(item, sort_keys=True, ensure_ascii=False)
            if ident in seen:
                continue
            seen.add(ident)
            count_out += 1
            fout.write(json.dumps(item, ensure_ascii=False) + "\n")
    return {
        "ok": True,
        "input": str(src),
        "output": str(out),
        "key": key,
        "input_count": count_in,
        "output_count": count_out,
    }
