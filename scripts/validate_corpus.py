#!/usr/bin/env python3
"""Validate the published corpus against its schema and its provenance rules.

A schema alone would only prove the shape is right. The checks below assert the
things that make the dataset trustworthy: that official and editorial material
stay separated, that no control claims official text it does not have, and that
both languages are complete. The script exits non zero on any failure so it can
gate a release.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus" / "kw-nbcc" / "controls.json"

FUNCTIONS = {"GOV", "ID", "PR", "DE", "RS", "RC", "CLD"}


def main():
    data = json.loads(CORPUS.read_text(encoding="utf-8"))
    controls = data["controls"]
    faults = []

    seen = set()
    for c in controls:
        cid = c.get("id", "(no id)")

        if cid in seen:
            faults.append(f"{cid}: duplicate identifier")
        seen.add(cid)

        if c.get("function") not in FUNCTIONS:
            faults.append(f"{cid}: unknown function {c.get('function')!r}")

        off, ed = c["official"], c["editorial"]

        # Official text must be present and complete in both languages.
        for field in ("title", "titleAr", "requirement", "requirementAr"):
            if not off.get(field):
                faults.append(f"{cid}: official.{field} is empty")

        # A purpose is either official or editorial. Never both, never neither
        # silently: a control with no purpose at all must show that on both sides.
        if off.get("purpose") and ed.get("purpose"):
            faults.append(f"{cid}: purpose claimed as both official and editorial")

        # Arabic must accompany every English string, or the record is half usable.
        if off.get("purpose") and not off.get("purposeAr"):
            faults.append(f"{cid}: official purpose has no Arabic")
        if ed.get("purpose") and not ed.get("purposeAr"):
            faults.append(f"{cid}: editorial purpose has no Arabic")
        if len(ed.get("checks", [])) != len(ed.get("checksAr", [])):
            faults.append(f"{cid}: checks and checksAr differ in length")
        if len(ed.get("evidence", [])) != len(ed.get("evidenceAr", [])):
            faults.append(f"{cid}: evidence and evidenceAr differ in length")

        # Every control must reach both frameworks the Decision names.
        if not c["crosswalk"]["csf"]:
            faults.append(f"{cid}: no CSF mapping")
        if not c["crosswalk"]["cis"]:
            faults.append(f"{cid}: no CIS mapping")

    # The Annex prints a purpose for the main body and not for the Appendix A
    # cloud tables. If that ever stops holding, the corpus has drifted from the
    # source and the separation can no longer be trusted.
    cloud = [c for c in controls if c["function"] == "CLD"]
    main_body = [c for c in controls if c["function"] != "CLD"]
    if any(c["official"]["purpose"] for c in cloud):
        faults.append("a cloud control claims an official purpose, which Appendix A does not print")
    without = [c["id"] for c in main_body if not c["official"]["purpose"]]
    if without:
        faults.append(f"main body controls missing an official purpose: {without}")

    total = len(controls)
    print(f"corpus: {total} controls, {len(cloud)} cloud, {len(main_body)} main body")
    print(f"  official purpose   {sum(1 for c in controls if c['official']['purpose'])}")
    print(f"  editorial purpose  {sum(1 for c in controls if c['editorial']['purpose'])}")
    print(f"  csf / cis mapped   {sum(1 for c in controls if c['crosswalk']['csf'])}"
          f" / {sum(1 for c in controls if c['crosswalk']['cis'])}")

    if faults:
        print(f"\n{len(faults)} fault(s):", file=sys.stderr)
        for f in faults:
            print(f"  {f}", file=sys.stderr)
        sys.exit(1)
    print("\nAll provenance and completeness checks passed.")


if __name__ == "__main__":
    main()
