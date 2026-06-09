#!/usr/bin/env python3
"""
Star a GitHub repository using multiple accounts.

Requires a JSON config file with account credentials:
[
  {"token": "ghp_xxxx", "username": "user1"},
  {"token": "ghp_yyyy", "username": "user2"}
]

Usage:
  python star_accounts.py --repo guajiimi/interceptiq --accounts accounts.json
"""

import argparse
import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def star_repo(token: str, repo: str) -> dict:
    """Star a repo using a GitHub personal access token."""
    url = f"https://api.github.com/user/starred/{repo}"
    req = Request(url, method="PUT")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Length", "0")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    try:
        with urlopen(req, timeout=15) as resp:
            return {"ok": True, "status": resp.status}
    except HTTPError as e:
        return {"ok": False, "status": e.code, "error": e.reason}


def main():
    parser = argparse.ArgumentParser(description="Star a GitHub repo from multiple accounts")
    parser.add_argument("--repo", required=True, help="owner/repo to star")
    parser.add_argument("--accounts", required=True, help="Path to JSON accounts file")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between requests (seconds)")
    args = parser.parse_args()

    with open(args.accounts) as f:
        accounts = json.load(f)

    results = []
    for i, acct in enumerate(accounts):
        token = acct["token"]
        username = acct.get("username", f"account-{i}")
        print(f"[{i+1}/{len(accounts)}] Starring {args.repo} as {username} ...")
        result = star_repo(token, args.repo)
        result["username"] = username
        results.append(result)
        print(f"  -> {result}")
        if i < len(accounts) - 1:
            time.sleep(args.delay)

    ok = sum(1 for r in results if r["ok"])
    print(f"\nDone: {ok}/{len(results)} accounts starred successfully.")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
