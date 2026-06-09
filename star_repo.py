#!/usr/bin/env python3
"""
Star a GitHub repo from multiple accounts using PAT tokens.
Usage: python3 star_repo.py <owner/repo> <token1> <token2> ...
"""
import sys
import requests
import time

def star_repo(repo: str, token: str, idx: int) -> dict:
    """Star a repo using a PAT token."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    # Get username first
    user_resp = requests.get("https://api.github.com/user", headers=headers)
    if user_resp.status_code != 200:
        return {"idx": idx, "status": "error", "msg": f"Invalid token: {user_resp.status_code}"}
    
    username = user_resp.json().get("login", "unknown")
    
    # Star the repo
    star_resp = requests.put(
        f"https://api.github.com/user/starred/{repo}",
        headers={**headers, "Content-Length": "0"}
    )
    
    if star_resp.status_code in (200, 204):
        return {"idx": idx, "status": "success", "user": username}
    else:
        return {"idx": idx, "status": "error", "user": username, "code": star_resp.status_code}

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 star_repo.py <owner/repo> <token1> <token2> ...")
        sys.exit(1)
    
    repo = sys.argv[1]
    tokens = sys.argv[2:]
    
    print(f"⭐ Starring {repo} from {len(tokens)} accounts...\n")
    
    success = 0
    for i, token in enumerate(tokens, 1):
        result = star_repo(repo, token, i)
        if result["status"] == "success":
            print(f"  ✅ [{i}] @{result['user']}")
            success += 1
        else:
            print(f"  ❌ [{i}] {result.get('user', 'unknown')} — {result.get('msg', result.get('code', 'failed'))}")
        time.sleep(0.5)  # Rate limit courtesy
    
    print(f"\n{'='*40}")
    print(f"⭐ {success}/{len(tokens)} stars added to {repo}")

if __name__ == "__main__":
    main()
