# Corpus

Regulatory corpora published as data. Each dataset exists because the material
was previously readable only by running a tool, which meant nobody could build
on it, cite it, or check it.

## Datasets

| Dataset | Instrument | Records | Formats |
| --- | --- | --- | --- |
| [`kw-nbcc`](kw-nbcc/) | Kuwait National Basic Cybersecurity Controls, NCSC Decision No. 2 of 2026 | 44 controls | JSON, CSV |
| [`kw-corf`](kw-corf/) | CBK Cyber and Operational Resilience Framework v1.0 | 874 controls | JSON, CSV |

## The provenance rule

A regulatory corpus is only useful if a reader can tell what the regulator wrote
from what the publisher added. Every `kw-nbcc` record splits into two objects:

- `official` holds text quoted from the Annex
- `editorial` holds analysis produced by this centre and carries no official standing

Nothing appears in both. `scripts/validate_corpus.py` fails the release if a
control ever claims a purpose as official and editorial at once, if official
text is missing in either language, or if the parallel Arabic and English arrays
fall out of step.

One invariant is asserted rather than assumed: the Annex prints a purpose for the
main body and not for the Appendix A cloud tables. The corpus therefore expects
exactly 28 official purposes and 16 editorial ones. If that ratio moves, the
corpus has drifted from its source and the build stops.

## Reproducing

```
node scripts/build_corpus.mjs /path/to/Kuwait-NBCC
python3 scripts/validate_corpus.py
```

## Known limitations

The CORF source catalogue reports 876 official controls and yields 874 on
extraction. Two controls are unaccounted for. The gap is recorded here rather
than rounded away, and the dataset should not be treated as complete until it is
resolved.

The `kw-corf` records are English only, because the framework was issued in
English. The `kw-nbcc` records are complete in both languages.

Crosswalk mappings to NIST CSF 2.0 and CIS v8.1 are named as alignment
references by the Decision itself. The ISO/IEC 27001:2022 mapping is added by
this centre as a convenience and has no official standing. A mapping is a
pointer, not an equivalence: holding a certificate against one framework does
not discharge a requirement under another.

## Licence and citation

MIT, consistent with the rest of the centre. Control text remains the work of
its issuing authority and is reproduced for reference. Cite the dataset by its
release tag so a reader can retrieve the exact version you used.
