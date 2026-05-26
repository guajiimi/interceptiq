import argparse
import json
from pathlib import Path
from .payload_analyze import analyze_intercept as payload_analyze
from .dom_analyze import analyze_intercept as dom_analyze
from .replay_generate import generate as replay_generate
from .jsonl_pipeline import dedupe_jsonl


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(obj, path=None):
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text, encoding="utf-8")
    print(text)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="interceptiq")
    sub = parser.add_subparsers(dest="cmd", required=True)

    payload = sub.add_parser("payload-analyze")
    payload.add_argument("intercept_json")
    payload.add_argument("-o", "--output")

    dom = sub.add_parser("dom-analyze")
    dom.add_argument("intercept_json")
    dom.add_argument("-o", "--output")

    replay = sub.add_parser("replay-generate")
    replay.add_argument("intercept_json")
    replay.add_argument("--out-dir", default="replay")

    jsonl = sub.add_parser("jsonl-dedupe")
    jsonl.add_argument("jsonl")
    jsonl.add_argument("--key", default="id")
    jsonl.add_argument("--out", required=True)

    args = parser.parse_args(argv)
    if args.cmd == "payload-analyze":
        dump(payload_analyze(load_json(args.intercept_json)), args.output)
    elif args.cmd == "dom-analyze":
        dump(dom_analyze(load_json(args.intercept_json)), args.output)
    elif args.cmd == "replay-generate":
        dump(replay_generate(load_json(args.intercept_json), args.out_dir))
    elif args.cmd == "jsonl-dedupe":
        dump(dedupe_jsonl(args.jsonl, args.key, args.out))


if __name__ == "__main__":
    main()
