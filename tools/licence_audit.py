#!/usr/bin/env python3
"""Detect licence files that exist but are not recognised.

A repository can carry a licence file and still be treated as unlicensed by
GitHub, by package registries and by dependency scanners. The file is present,
a reader sees it, and every automated consumer disagrees. This tool finds that
class of fault across an account.

Usage:
    python3 licence_audit.py OWNER
    GITHUB_TOKEN=... python3 licence_audit.py OWNER --json

Nothing is written. The tool only reads.
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request

CANDIDATES = ("LICENSE", "LICENCE", "LICENSE.md", "LICENSE.txt",
              "LICENCE.md", "LICENCE.txt", "COPYING")

# Clauses whose absence stops a licence being recognised.
MIT_LIABILITY = "IN NO EVENT SHALL THE"
MIT_OPENING = "Permission is hereby granted, free of charge"
APACHE_FULL = "APPENDIX: How to apply the Apache License"

FAULTS = {
    "truncated": "licence text is cut short and omits a required clause",
    "appended": "licence is complete but extra text in the same file blocks detection",
    "summarised": "file summarises a licence rather than reproducing it",
    "filename": "licence is complete but the filename is not recognised",
    "not-a-licence": "file is a notice or disclaimer rather than a licence",
    "missing": "no licence file of any kind",
}


def api(path, token):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Accept": "application/vnd.github+json",
                 **({"Authorization": f"token {token}"} if token else {})},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None


def classify(text, filename):
    """Work out why a licence file would fail detection."""
    body = text.lstrip()

    if body.startswith("MIT License") or MIT_OPENING in body[:600]:
        if MIT_LIABILITY not in text:
            return "truncated"
        tail = re.split(r"OTHER DEALINGS IN THE\s+SOFTWARE\.", text, flags=re.I)
        if len(tail) > 1 and len(tail[-1].strip()) > 40:
            return "appended"
        if filename != "LICENSE":
            return "filename"
        return None

    if body.startswith("Apache License"):
        if APACHE_FULL not in text:
            return "summarised"
        if filename != "LICENSE":
            return "filename"
        return None

    return "not-a-licence"


def audit(owner, token):
    repos, page = [], 1
    while True:
        status, batch = api(f"/users/{owner}/repos?per_page=100&page={page}", token)
        if status != 200 or not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    results = []
    for r in sorted(repos, key=lambda x: x["name"].lower()):
        if r["fork"]:
            continue
        spdx = (r.get("license") or {}).get("spdx_id") if r.get("license") else None
        detected = bool(spdx and spdx != "NOASSERTION")

        found_name, found_text = None, None
        if not detected:
            for candidate in CANDIDATES:
                status, data = api(
                    f"/repos/{owner}/{r['name']}/contents/{candidate}", token)
                if status == 200 and isinstance(data, dict):
                    found_name = candidate
                    found_text = base64.b64decode(
                        data["content"]).decode("utf-8", "replace")
                    break

        if detected:
            fault = None
        elif found_text is None:
            fault = "missing"
        else:
            fault = classify(found_text, found_name) or "filename"

        results.append({
            "repo": r["name"],
            "detected_as": spdx if detected else None,
            "licence_file": found_name,
            "fault": fault,
        })
    return results


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    owner = args[0]
    results = audit(owner, os.environ.get("GITHUB_TOKEN", ""))

    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
        return

    faulty = [r for r in results if r["fault"]]
    silent = [r for r in faulty if r["fault"] != "missing"]

    print(f"{owner}: {len(results)} original repositories")
    print(f"  recognised            {len(results) - len(faulty)}")
    print(f"  no licence at all     {len(faulty) - len(silent)}")
    print(f"  present but unread    {len(silent)}")

    if silent:
        print("\nThese carry a licence file that no automated consumer will read:\n")
        for r in silent:
            print(f"  {r['repo']:34} {r['licence_file']:12} {FAULTS[r['fault']]}")


if __name__ == "__main__":
    main()
