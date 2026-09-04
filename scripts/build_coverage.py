#!/usr/bin/env python3
"""Measure what each part of the national baseline contributes in framework terms.

The baseline has a main body of 28 controls and an Appendix A of 16 cloud
controls. Appendix A is 36 percent of the instrument by count, which invites the
assumption that it is 36 percent of the obligation. That assumption is testable,
because every control carries mappings into frameworks the Decision itself names
as alignment references, and those mappings say whether a control covers ground
the rest of the baseline already covers.

This produces a coverage dataset rather than an opinion. Nothing here judges
whether the baseline should be arranged differently. It reports what the
arrangement is.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "corpus" / "kw-nbcc" / "controls.json"
OUT = ROOT / "corpus" / "kw-coverage"

FRAMEWORKS = ("csf", "cis", "iso")


def refs(controls, fw):
    out = set()
    for c in controls:
        out |= set(c["crosswalk"][fw])
    return out


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    controls = data["controls"]
    body = [c for c in controls if c["function"] != "CLD"]
    cloud = [c for c in controls if c["function"] == "CLD"]

    split = {}
    for fw in FRAMEWORKS:
        b, cl = refs(body, fw), refs(cloud, fw)
        split[fw] = {
            "body_refs": len(b),
            "cloud_refs": len(cl),
            "shared": len(b & cl),
            "cloud_only": sorted(cl - b),
            "body_only": len(b - cl),
            "distinct_total": len(b | cl),
            "cloud_restatement_rate": round(len(b & cl) / len(cl), 3) if cl else None,
        }

    # Where the load concentrates. A subcategory carrying many controls is a
    # point the baseline returns to repeatedly.
    load = Counter()
    for c in controls:
        for m in c["crosswalk"]["csf"]:
            load[m] += 1

    by_function = defaultdict(lambda: {"controls": 0, "csf_refs": set()})
    for c in controls:
        by_function[c["function"]]["controls"] += 1
        by_function[c["function"]]["csf_refs"] |= set(c["crosswalk"]["csf"])

    # Group the ground unique to Appendix A by its CSF category, since a
    # scattered set and a concentrated set mean different things.
    cloud_only_csf = split["csf"]["cloud_only"]
    cloud_only_cat = Counter(m.split("-")[0] for m in cloud_only_csf)

    dataset = {
        "dataset": "kw-coverage",
        "title": "Coverage analysis of the Kuwait national baseline",
        "titleAr": "تحليل تغطية الأساس الوطني الكويتي",
        "licence": "MIT",
        "provenance": {
            "note": "Derived entirely from the mappings published in kw-nbcc. The CSF and CIS mappings are named by the Decision as alignment references. The ISO mapping is added by this centre and has no official standing, so figures resting on it are weaker.",
            "noteAr": "مشتق كليا من الربوط المنشورة في المدونة الوطنية، والربط بإطار المعهد الوطني وبالضوابط الحرجة مسمى في القرار مرجعا للمواءمة، أما الربط بالمعيار الدولي فأضافه المركز ولا يحمل صفة رسمية لذا فالأرقام القائمة عليه أضعف.",
        },
        "counts": {
            "controls": len(controls),
            "main_body": len(body),
            "appendix_a_cloud": len(cloud),
            "cloud_share_by_count": round(len(cloud) / len(controls), 3),
            "cloud_share_of_new_csf_ground": round(
                len(split["csf"]["cloud_only"]) / split["csf"]["distinct_total"], 3),
        },
        "by_framework": split,
        "cloud_only_csf_by_category": dict(cloud_only_cat),
        "csf_load": [{"subcategory": k, "controls": v} for k, v in load.most_common()],
        "by_function": {
            k: {"controls": v["controls"], "distinct_csf": len(v["csf_refs"])}
            for k, v in sorted(by_function.items())
        },
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "coverage.json").write_text(
        json.dumps(dataset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"controls {len(controls)}  main body {len(body)}  appendix A {len(cloud)}")
    for fw in FRAMEWORKS:
        s = split[fw]
        print(f"  {fw.upper():4} cloud touches {s['cloud_refs']:3}, "
              f"{s['shared']:3} already covered by the body, "
              f"{len(s['cloud_only']):3} new "
              f"(restatement {s['cloud_restatement_rate']})")
    print(f"\nAppendix A is {dataset['counts']['cloud_share_by_count']:.0%} of controls "
          f"and {dataset['counts']['cloud_share_of_new_csf_ground']:.0%} of distinct CSF ground")
    print(f"ground unique to Appendix A, by category: {dict(cloud_only_cat)}")


if __name__ == "__main__":
    main()
