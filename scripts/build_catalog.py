#!/usr/bin/env python3
"""Rebuild data/catalog.json from the live GitHub API.

Usage:
    GITHUB_TOKEN=... python3 scripts/build_catalog.py

The script fails loudly when a repository is missing from the taxonomy, so the
catalogue can never silently drift out of date as new work is published.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from taxonomy import ASSIGN, DOMAINS, EXCLUDE, maturity  # noqa: E402

ACCOUNT = "SiteQ8"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "catalog.json"


def fetch_repos(token):
    repos, page = [], 1
    while True:
        url = (
            f"https://api.github.com/users/{ACCOUNT}/repos"
            f"?per_page=100&page={page}&sort=updated"
        )
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        if token:
            req.add_header("Authorization", f"token {token}")
        with urllib.request.urlopen(req) as resp:
            batch = json.load(resp)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


DASHES = {0x2012: "-", 0x2013: "-", 0x2014: "-", 0x2015: "-"}


def clean(text):
    """Strip Unicode dashes that arrive with upstream GitHub descriptions."""
    return (text or "").translate(DASHES).strip()


def build(repos):
    originals, mirrors, missing = [], [], []

    for r in sorted(repos, key=lambda x: x["name"].lower()):
        name = r["name"]
        if name in EXCLUDE:
            continue
        if r["fork"]:
            mirrors.append({
                "name": name,
                "url": r["html_url"],
                "description": clean(r["description"]),
            })
            continue
        domain = ASSIGN.get(name)
        if domain is None:
            missing.append(name)
            continue
        originals.append({
            "name": name,
            "domain": domain,
            "description": clean(r["description"]),
            "language": r["language"] or "",
            "stars": r["stargazers_count"],
            "size_kb": r["size"],
            "url": r["html_url"],
            "pages": f"https://{ACCOUNT.lower()}.github.io/{name}/" if r["has_pages"] else "",
            "license": (r["license"] or {}).get("spdx_id", "") if r.get("license") else "",
            "topics": r.get("topics") or [],
            "updated": r["pushed_at"][:10],
            "maturity": maturity(r),
        })

    if missing:
        print("Repositories missing from the taxonomy:", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)
        sys.exit(1)

    return {
        "account": ACCOUNT,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "domains": [
            {"id": d[0], "en": d[1], "ar": d[2], "en_desc": d[3], "ar_desc": d[4]}
            for d in DOMAINS
        ],
        "projects": originals,
        "mirrors": sorted(mirrors, key=lambda x: x["name"].lower()),
        "stats": {
            "projects": len(originals),
            "mirrors": len(mirrors),
            "stars": sum(p["stars"] for p in originals),
            "licensed": sum(1 for p in originals if p["license"] and p["license"] != "NOASSERTION"),
            "with_site": sum(1 for p in originals if p["pages"]),
            "flagship": sum(1 for p in originals if p["maturity"] == "flagship"),
        },
    }


def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    catalog = build(fetch_repos(token))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    s = catalog["stats"]
    print(f"Catalogue written to {OUT.relative_to(ROOT)}")
    print(f"  projects   {s['projects']}")
    print(f"  mirrors    {s['mirrors']}")
    print(f"  licensed   {s['licensed']}/{s['projects']}")
    print(f"  with site  {s['with_site']}/{s['projects']}")


if __name__ == "__main__":
    main()
