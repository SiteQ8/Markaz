#!/usr/bin/env python3
"""Render index.html from data/catalog.json and data/descriptions.ar.json.

Data is embedded directly in the page so the centre works offline and from the
local filesystem, with no fetch and no external dependency of any kind.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src" / "index.template.html"
OUT = ROOT / "index.html"


def main():
    catalog = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
    arabic = json.loads((ROOT / "data" / "descriptions.ar.json").read_text(encoding="utf-8"))
    english = json.loads((ROOT / "data" / "descriptions.en.json").read_text(encoding="utf-8"))

    arabic_script = re.compile(r"[\u0600-\u06FF]")
    latin_word = re.compile(r"[A-Za-z]{3,}")
    faults = []

    for project in catalog["projects"]:
        name = project["name"]
        project["description"] = english.get(name, project["description"])
        project["ar"] = arabic.get(name, "")

        if arabic_script.search(project["description"]):
            faults.append(f"{name}: Arabic script in the English description")
        if latin_word.search(project["ar"]):
            faults.append(f"{name}: Latin words in the Arabic description")
        if not project["ar"]:
            faults.append(f"{name}: no Arabic description")

    if faults:
        print("Language purity check failed:", file=sys.stderr)
        for f in faults:
            print(f"  {f}", file=sys.stderr)
        sys.exit(1)

    payload = json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
    corpus = (ROOT / "data" / "corpus-lite.json").read_text(encoding="utf-8").strip()
    html = (TEMPLATE.read_text(encoding="utf-8")
            .replace("/*__CATALOG__*/null", payload)
            .replace("/*__CORPUS__*/null", corpus))
    if "__CATALOG__" in html or "__CORPUS__" in html:
        print("A payload placeholder was not replaced.", file=sys.stderr)
        sys.exit(1)
    OUT.write_text(html, encoding="utf-8")

    size = OUT.stat().st_size
    print(f"index.html written: {size // 1024} KB, {len(catalog['projects'])} projects embedded")


if __name__ == "__main__":
    main()
