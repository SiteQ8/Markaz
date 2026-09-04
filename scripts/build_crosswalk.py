#!/usr/bin/env python3
"""Propose a crosswalk between the Kuwait national baseline and the CBK framework.

No such mapping exists publicly, and a Kuwaiti entity subject to both regimes
currently has no way to see where they overlap. This script does not assert one
either. It produces ranked candidates, states a confidence for each, and marks
every pair as unreviewed until a person records a decision.

The method is validated before it is applied. The national baseline already
carries human made mappings to NIST CSF 2.0 subcategories. If the similarity
metric has real signal, control pairs that share a CSF subcategory should score
higher than pairs that do not. That test runs first, and its result is reported
alongside the candidates so a reader can judge how much weight the ranking
deserves.

Usage:
    python3 scripts/build_crosswalk.py            validate and build
    python3 scripts/build_crosswalk.py --validate validation only
"""

import json
import math
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NBCC = ROOT / "corpus" / "kw-nbcc" / "controls.json"
CORF = ROOT / "corpus" / "kw-corf" / "controls.json"
OUT = ROOT / "corpus" / "kw-crosswalk"

# Words that appear in nearly every control and therefore carry no signal about
# which control this is. Removing them stops "shall", "entity" and "security"
# from dominating every comparison.
STOP = set("""
a an and are as at be been by for from has have if in into is it its may must not
of on or shall should such that the their there these this to under upon which
will with within would entity entities regulated relevant appropriate ensure
ensures required requirement requirements including include includes based
information security cyber cybersecurity control controls
""".split())

TOKEN = re.compile(r"[a-z][a-z0-9]{2,}")


def tokens(text):
    return [w for w in TOKEN.findall((text or "").lower()) if w not in STOP]


def build_idf(docs):
    df = Counter()
    for d in docs:
        df.update(set(d))
    n = len(docs)
    return {w: math.log((n + 1) / (c + 1)) + 1.0 for w, c in df.items()}


def vector(toks, idf):
    tf = Counter(toks)
    if not tf:
        return {}
    top = max(tf.values())
    v = {w: (0.5 + 0.5 * c / top) * idf.get(w, 1.0) for w, c in tf.items()}
    norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {w: x / norm for w, x in v.items()}


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0.0) for w, x in a.items())


def load():
    nbcc = json.loads(NBCC.read_text(encoding="utf-8"))
    corf = json.loads(CORF.read_text(encoding="utf-8"))
    return nbcc, corf


def nbcc_text(c):
    """Only official text is used. Editorial analysis would bias the mapping
    toward this centre's own wording rather than the regulator's."""
    return f"{c['official']['title']} {c['official']['requirement']}"


def validate(nbcc, idf_pool):
    """Do controls sharing a CSF subcategory score higher than those that do not?"""
    controls = nbcc["controls"]
    idf = build_idf([tokens(nbcc_text(c)) for c in controls])
    vecs = {c["id"]: vector(tokens(nbcc_text(c)), idf) for c in controls}

    shared, unshared = [], []
    for a, b in combinations(controls, 2):
        csf_a, csf_b = set(a["crosswalk"]["csf"]), set(b["crosswalk"]["csf"])
        score = cosine(vecs[a["id"]], vecs[b["id"]])
        (shared if csf_a & csf_b else unshared).append(score)

    def stats(xs):
        n = len(xs)
        m = sum(xs) / n
        sd = math.sqrt(sum((x - m) ** 2 for x in xs) / n)
        return n, m, sd

    ns, ms, ss = stats(shared)
    nu, mu, su = stats(unshared)
    pooled = math.sqrt(((ns - 1) * ss ** 2 + (nu - 1) * su ** 2) / (ns + nu - 2)) or 1e-9
    d = (ms - mu) / pooled

    return {
        "pairs_sharing_csf": ns,
        "pairs_not_sharing": nu,
        "mean_similarity_shared": round(ms, 4),
        "mean_similarity_unshared": round(mu, 4),
        "ratio": round(ms / mu, 2) if mu else None,
        "cohens_d": round(d, 3),
        "interpretation": (
            "large" if abs(d) >= 0.8 else
            "medium" if abs(d) >= 0.5 else
            "small" if abs(d) >= 0.2 else "negligible"
        ),
    }


def main():
    nbcc, corf = load()
    n_controls, c_controls = nbcc["controls"], corf["controls"]

    report = validate(nbcc, None)
    print("Method validation, against the baseline's own CSF mappings")
    print(f"  pairs sharing a CSF subcategory   {report['pairs_sharing_csf']}")
    print(f"  pairs sharing none                {report['pairs_not_sharing']}")
    print(f"  mean similarity, shared           {report['mean_similarity_shared']}")
    print(f"  mean similarity, unshared         {report['mean_similarity_unshared']}")
    print(f"  ratio                             {report['ratio']}x")
    print(f"  Cohen's d                         {report['cohens_d']} ({report['interpretation']})")

    if "--validate" in sys.argv:
        return

    if report["cohens_d"] < 0.2:
        print("\nMetric shows no usable signal. Refusing to emit candidates.", file=sys.stderr)
        sys.exit(1)

    corpus = [tokens(nbcc_text(c)) for c in n_controls] + \
             [tokens(c["text"]) for c in c_controls]
    idf = build_idf(corpus)
    n_vecs = {c["id"]: vector(tokens(nbcc_text(c)), idf) for c in n_controls}
    c_vecs = {c["key"]: vector(tokens(c["text"]), idf) for c in c_controls}

    pairs = []
    for n in n_controls:
        scored = sorted(
            ((cosine(n_vecs[n["id"]], c_vecs[c["key"]]), c) for c in c_controls),
            key=lambda x: -x[0],
        )[:5]
        for rank, (score, c) in enumerate(scored, 1):
            if score < 0.10:
                continue
            pairs.append({
                "nbcc": n["id"],
                "nbcc_title": n["official"]["title"],
                "corf": c["key"],
                "corf_domain": c["domain"],
                "corf_text": c["text"][:240],
                "rank": rank,
                "score": round(score, 4),
                "confidence": "strong" if score >= 0.30 else "moderate" if score >= 0.18 else "weak",
                "status": "proposed",
                "reviewed_by": None,
                "decision": None,
            })

    covered = {p["nbcc"] for p in pairs}
    strong = [p for p in pairs if p["confidence"] == "strong"]

    dataset = {
        "dataset": "kw-crosswalk",
        "title": "Proposed crosswalk, Kuwait national baseline to CBK resilience framework",
        "titleAr": "ربط مقترح بين الأساس الوطني وإطار المرونة لبنك الكويت المركزي",
        "status": "unreviewed",
        "warning": "Every pair in this file is machine proposed and none has been reviewed by a person. It must not be used as a compliance mapping until reviewed.",
        "warningAr": "كل زوج في هذا الملف مقترح آليا ولم يراجعه إنسان بعد، لذا لا يجوز استعماله بوصفه ربطا للامتثال قبل المراجعة.",
        "method": {
            "description": "TF-IDF cosine similarity over official control text, top five candidates per national control, scores below 0.10 discarded.",
            "text_used": "Official title and requirement only. Editorial analysis excluded so the mapping reflects the regulator's wording.",
            "validation": report,
        },
        "counts": {
            "nbcc_controls": len(n_controls),
            "corf_controls": len(c_controls),
            "candidate_pairs": len(pairs),
            "nbcc_with_candidate": len(covered),
            "nbcc_without_candidate": len(n_controls) - len(covered),
            "strong": len(strong),
            "moderate": sum(1 for p in pairs if p["confidence"] == "moderate"),
            "weak": sum(1 for p in pairs if p["confidence"] == "weak"),
            "reviewed": 0,
        },
        "pairs": pairs,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "nbcc-corf.json").write_text(
        json.dumps(dataset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\ncorpus/kw-crosswalk/nbcc-corf.json")
    print(f"  candidate pairs        {len(pairs)}")
    print(f"  national controls hit  {len(covered)}/{len(n_controls)}")
    print(f"  strong / moderate / weak  {dataset['counts']['strong']}"
          f" / {dataset['counts']['moderate']} / {dataset['counts']['weak']}")


if __name__ == "__main__":
    main()
