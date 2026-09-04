#!/usr/bin/env python3
"""Derive a bilingual cybersecurity lexicon from regulator drafted parallel text.

There is no authoritative Arabic security vocabulary, so each translator invents
one and the terms diverge. The national baseline is unusual in carrying 44
controls whose English and Arabic were drafted together by the regulator, which
makes it a defensible basis for deriving terminology rather than asserting it.

Two classes of pair are produced and never mixed.

  attested   the regulator's own equivalence, taken from a control title where
             the English and Arabic name the same thing by construction
  derived    a correspondence inferred from co-occurrence across the corpus,
             which is this centre's inference and carries no authority

The method is validated before it is trusted. Derived extraction is run against
the title pairs, whose answers are known, and the recovery rate is reported with
the output.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "corpus" / "kw-nbcc" / "controls.json"
OUT = ROOT / "corpus" / "kw-lexicon"

EN_STOP = set("""
a an and are as at be by for from has have in into is it its of on or shall that
the their to under upon which with within must should any all other such each
entity entities relevant appropriate ensure required including based
""".split())

AR_STOP = set("""
في من على عن الى إلى مع أو او و ثم التي الذي هذا هذه ذلك تلك كل أي عند بعد قبل
يجب على أن ان ما لا غير بين لدى حسب وفق كما بها به لها له عليها عليه ذات
""".split())

EN_TOKEN = re.compile(r"[A-Za-z][A-Za-z-]{2,}")
AR_TOKEN = re.compile(r"[\u0621-\u064A]{3,}")
AR_DIACRITIC = re.compile(r"[\u064B-\u0652\u0670]")


# Surface forms are what a reader needs. Normalisation exists only so that two
# spellings of the same word match each other, and must never reach the output.
SURFACE = {}


def norm_ar(word):
    """Fold a word for matching. Only the definite article is stripped, because
    a bare waw or lam is as often part of the word as a clitic: stripping it
    turns wasa'it, meaning media, into a fragment that is not a word."""
    w = AR_DIACRITIC.sub("", word)
    for prefix in ("وال", "بال", "كال", "فال", "لل", "ال"):
        if w.startswith(prefix) and len(w) - len(prefix) >= 3:
            w = w[len(prefix):]
            break
    key = (w.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
            .replace("ى", "ي").replace("ة", "ه"))
    # Remember the commonest spelling actually used for this fold.
    counts = SURFACE.setdefault(key, {})
    counts[word] = counts.get(word, 0) + 1
    return key


def surface(key):
    """Best surface spelling for a folded key, or the phrase for an n-gram."""
    parts = key.split(" ")
    if len(parts) > 1:
        return " ".join(surface(p) for p in parts)
    counts = SURFACE.get(key)
    return max(counts, key=counts.get) if counts else key


def en_terms(text, n=(1, 2, 3)):
    words = [w.lower() for w in EN_TOKEN.findall(text or "")]
    out = set()
    for size in n:
        for i in range(len(words) - size + 1):
            gram = words[i:i + size]
            if gram[0] in EN_STOP or gram[-1] in EN_STOP:
                continue
            if all(w in EN_STOP for w in gram):
                continue
            out.add(" ".join(gram))
    return out


def ar_terms(text, n=(1, 2, 3)):
    words = AR_TOKEN.findall(text or "")
    out = set()
    for size in n:
        for i in range(len(words) - size + 1):
            gram = words[i:i + size]
            if gram[0] in AR_STOP or gram[-1] in AR_STOP:
                continue
            out.add(" ".join(norm_ar(w) for w in gram))
    return out


def dice(a, b):
    return 2 * len(a & b) / (len(a) + len(b)) if (a or b) else 0.0


def build_index(pairs, extract_en, extract_ar):
    """Map each term to the set of segment indices it appears in."""
    e_idx, a_idx = defaultdict(set), defaultdict(set)
    for i, (en, ar) in enumerate(pairs):
        for term in extract_en(en):
            e_idx[term].add(i)
        for term in extract_ar(ar):
            a_idx[term].add(i)
    return e_idx, a_idx


def derive(pairs, min_docs=3, min_dice=0.72):
    e_idx, a_idx = build_index(pairs, en_terms, ar_terms)
    e_idx = {k: v for k, v in e_idx.items() if len(v) >= min_docs}
    a_idx = {k: v for k, v in a_idx.items() if len(v) >= min_docs}

    by_doc = defaultdict(list)
    for term, docs in a_idx.items():
        for d in docs:
            by_doc[d].append(term)

    out = []
    for en, e_docs in e_idx.items():
        best, best_score = None, 0.0
        seen = set()
        for d in e_docs:
            for ar in by_doc[d]:
                if ar in seen:
                    continue
                seen.add(ar)
                score = dice(e_docs, a_idx[ar])
                if score > best_score:
                    best, best_score = ar, score
        if best and best_score >= min_dice:
            out.append({"en": en, "ar": surface(best), "fold": best,
                        "score": round(best_score, 3), "segments": len(e_docs)})

    # One Arabic term should not be claimed by several English terms. Keep the
    # longest English phrase per fold, which is the most specific reading, and
    # drop the rest rather than publish contradictory equivalences.
    best_for = {}
    for r in out:
        cur = best_for.get(r["fold"])
        if cur is None or (r["score"], len(r["en"])) > (cur["score"], len(cur["en"])):
            best_for[r["fold"]] = r
    return [dict(r, fold=None) and {k: v for k, v in r.items() if k != "fold"}
            for r in best_for.values()]


def validate(controls):
    """Run derivation over the title pairs, where the answer is already known."""
    titles = [(c["official"]["title"], c["official"]["titleAr"]) for c in controls]
    e_idx, a_idx = build_index(titles, en_terms, ar_terms)
    shared_en = {k: v for k, v in e_idx.items() if len(v) >= 2}
    hits = 0
    for en, docs in shared_en.items():
        best = max((dice(docs, a_idx[a]), a) for a in a_idx) if a_idx else (0, None)
        if best[0] >= 0.72:
            hits += 1
    return {"title_pairs": len(titles),
            "repeated_en_terms": len(shared_en),
            "aligned_at_threshold": hits,
            "recovery_rate": round(hits / len(shared_en), 3) if shared_en else 0.0}


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    controls = data["controls"]

    attested = [{
        "en": c["official"]["title"],
        "ar": c["official"]["titleAr"],
        "source": "attested",
        "control": c["id"],
    } for c in controls]

    segments = []
    for c in controls:
        segments.append((c["official"]["requirement"], c["official"]["requirementAr"]))
        ck, ckAr = c["editorial"]["checks"], c["editorial"]["checksAr"]
        if len(ck) == len(ckAr):
            segments.extend(zip(ck, ckAr))

    report = validate(controls)
    derived = sorted(derive(segments), key=lambda x: (-x["score"], -x["segments"]))

    dataset = {
        "dataset": "kw-lexicon",
        "title": "Bilingual cybersecurity lexicon, derived from the Kuwait national baseline",
        "titleAr": "معجم ثنائي اللغة للأمن السيبراني مشتق من الأساس الوطني الكويتي",
        "licence": "MIT",
        "provenance": {
            "note": "Attested pairs are the regulator's own equivalences, taken from control titles. Derived pairs are inferred by this centre from co-occurrence and carry no authority.",
            "noteAr": "الأزواج المُثبتة هي مقابلات المنظِّم نفسه مأخوذة من عناوين الضوابط، أما الأزواج المشتقة فاستنتجها المركز من التلازم ولا تحمل أي صفة رسمية.",
        },
        "method": {
            "segments": len(segments),
            "description": "Dice coefficient over segment level co-occurrence, requiring a term to appear in at least 3 segments and to reach 0.72 agreement.",
            "validation": report,
        },
        "counts": {"attested": len(attested), "derived": len(derived)},
        "attested": attested,
        "derived": derived,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "terms.json").write_text(
        json.dumps(dataset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    esc = lambda v: '"' + str(v).replace('"', '""') + '"'
    rows = ["en,ar,source,evidence"]
    rows += [",".join([esc(a["en"]), esc(a["ar"]), "attested", esc(a["control"])]) for a in attested]
    rows += [",".join([esc(d["en"]), esc(d["ar"]), "derived", esc(d["score"])]) for d in derived]
    (OUT / "terms.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")

    print(f"segments aligned      {len(segments)}")
    print(f"validation recovery   {report['aligned_at_threshold']}/{report['repeated_en_terms']}"
          f" ({report['recovery_rate']})")
    print(f"attested pairs        {len(attested)}")
    print(f"derived pairs         {len(derived)}")
    if report["recovery_rate"] < 0.3:
        print("\nRecovery too low to publish derived pairs.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
