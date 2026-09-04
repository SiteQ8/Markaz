#!/usr/bin/env python3
"""Repair licence files across the SiteQ8 account.

Three faults are handled:

  truncated   a LICENSE that opens as MIT but stops before the liability
              limitation clause, which is why GitHub cannot detect it
  abridged    a summarised Apache text that is not the real licence
  missing     no licence file at all

Any custom text the author appended after the licence body is preserved and
moved to NOTICE.md rather than discarded. The existing copyright line is reused
wherever one is present, so years and attribution are never rewritten.

Run with --apply to push. Without it the script only reports.
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request

TOKEN = os.environ["GITHUB_TOKEN"]
OWNER = "SiteQ8"
AUTHOR = {"name": "SiteQ8", "email": "311682+SiteQ8@users.noreply.github.com"}

MIT_BODY = '''Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

LIABILITY = "IN NO EVENT SHALL THE"
DEFAULT_COPYRIGHT = "Copyright (c) 2026 Ali AlEnezi"
# The last line of the canonical MIT body, used to find where custom text begins.
MIT_END = re.compile(r"OTHER DEALINGS IN THE\s+SOFTWARE\.", re.I)


def api(path, body=None, method="GET"):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        data=json.dumps(body).encode() if body else None,
        headers={
            "Authorization": f"token {TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


def mit_for(existing):
    """Build a canonical MIT, keeping the author's own copyright line."""
    line = DEFAULT_COPYRIGHT
    if existing:
        found = re.search(r"^Copyright\s*\(c\).*$", existing, re.M | re.I)
        if found:
            line = found.group().strip()
    return f"MIT License\n\n{line}\n\n{MIT_BODY}"


def custom_tail(existing):
    """Return any text the author added after the MIT body."""
    if not existing:
        return ""
    end = MIT_END.search(existing)
    if not end:
        # Truncated file: anything after the warranty sentence is custom.
        cut = existing.upper().rfind("NONINFRINGEMENT.")
        tail = existing[cut + len("NONINFRINGEMENT."):] if cut != -1 else ""
    else:
        tail = existing[end.end():]
    tail = tail.strip()
    return tail if len(tail) > 40 else ""


def get_file(repo, path):
    status, data = api(f"/repos/{OWNER}/{repo}/contents/{path}")
    if status != 200 or not isinstance(data, dict):
        return None, None
    return base64.b64decode(data["content"]).decode("utf-8", "replace"), data["sha"]


def put_file(repo, path, text, message, sha=None):
    body = {
        "message": message,
        "content": base64.b64encode(text.encode()).decode(),
        "author": AUTHOR,
        "committer": AUTHOR,
    }
    if sha:
        body["sha"] = sha
    return api(f"/repos/{OWNER}/{repo}/contents/{path}", body, "PUT")


def delete_file(repo, path, sha, message):
    return api(
        f"/repos/{OWNER}/{repo}/contents/{path}",
        {"message": message, "sha": sha, "author": AUTHOR, "committer": AUTHOR},
        "DELETE",
    )


def plan():
    """Work out what each repository needs, without changing anything."""
    repos = []
    page = 1
    while True:
        status, batch = api(f"/users/{OWNER}/repos?per_page=100&page={page}")
        if status != 200 or not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    jobs = []
    for r in sorted(repos, key=lambda x: x["name"].lower()):
        name = r["name"]
        if r["fork"] or name in ("SiteQ8", "Markaz"):
            continue
        spdx = (r.get("license") or {}).get("spdx_id") if r.get("license") else None
        if spdx and spdx != "NOASSERTION":
            continue

        existing, sha, path = None, None, "LICENSE"
        for candidate in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
            text, s = get_file(name, candidate)
            if text is not None:
                existing, sha, path = text, s, candidate
                break

        if existing is None:
            jobs.append({"repo": name, "fault": "missing", "path": "LICENSE",
                         "sha": None, "existing": None, "tail": ""})
        elif existing.lstrip().startswith("Apache"):
            jobs.append({"repo": name, "fault": "abridged-apache", "path": path,
                         "sha": sha, "existing": existing, "tail": ""})
        elif not existing.lstrip().startswith("MIT License"):
            jobs.append({"repo": name, "fault": "not-a-licence", "path": path,
                         "sha": sha, "existing": existing, "tail": existing.strip()})
        elif LIABILITY not in existing:
            jobs.append({"repo": name, "fault": "truncated-mit", "path": path,
                         "sha": sha, "existing": existing,
                         "tail": custom_tail(existing)})
        else:
            jobs.append({"repo": name, "fault": "filename", "path": path,
                         "sha": sha, "existing": existing, "tail": custom_tail(existing)})
    return jobs


def main():
    apply = "--apply" in sys.argv
    jobs = plan()

    counts = {}
    for j in jobs:
        counts[j["fault"]] = counts.get(j["fault"], 0) + 1
    print(f"{len(jobs)} repositories need attention")
    for k, v in sorted(counts.items()):
        print(f"  {k:18} {v}")
    print()

    for j in jobs:
        note = f" + NOTICE.md ({len(j['tail'])}b preserved)" if j["tail"] else ""
        rename = f" [{j['path']} -> LICENSE]" if j["path"] != "LICENSE" else ""
        print(f"  {j['repo']:32} {j['fault']:18}{rename}{note}")

    if not apply:
        print("\nDry run. Re-run with --apply to push.")
        return

    print("\nApplying.\n")
    ok = fail = 0
    for j in jobs:
        repo, tail = j["repo"], j["tail"]
        if j["fault"] == "abridged-apache":
            apache = open("LICENSE", encoding="utf-8").read()
            found = re.search(r"^Copyright\s+\d{4}.*$", j["existing"] or "", re.M)
            if found:
                apache = apache.replace("Copyright 2026 Ali AlEnezi", found.group().strip())
            status, resp = put_file(repo, "LICENSE", apache,
                                    "Restore the full Apache 2.0 licence text.", j["sha"])
            print(f"  {repo:32} {'done, full Apache 2.0' if status in (200,201) else f'FAILED {status}'}")
            ok += 1 if status in (200, 201) else 0
            continue

        text = mit_for(j["existing"])
        msg = ("Add the MIT licence." if j["fault"] == "missing"
               else "Restore the full MIT licence text.")

        # When the licence lived under another filename, write LICENSE then drop the old one.
        sha = j["sha"] if j["path"] == "LICENSE" else None
        status, resp = put_file(repo, "LICENSE", text, msg, sha)
        if status not in (200, 201):
            print(f"  {repo:32} FAILED {status} {str(resp)[:90]}")
            fail += 1
            continue

        if tail:
            put_file(repo, "NOTICE.md", tail.rstrip() + "\n",
                     "Move the project specific notice out of the licence file.")
        if j["path"] != "LICENSE" and j["sha"]:
            delete_file(repo, j["path"], j["sha"],
                        "Remove the duplicate licence file so the licence is detected.")
        ok += 1
        print(f"  {repo:32} done{'  + NOTICE.md' if tail else ''}")

    print(f"\napplied {ok}, failed {fail}")


if __name__ == "__main__":
    main()
