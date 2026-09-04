# Corpus

Regulatory corpora published as data. Each dataset exists because the material
was previously readable only by running a tool, which meant nobody could build
on it, cite it, or check it.

## Datasets

| Dataset | Instrument | Records | Formats |
| --- | --- | --- | --- |
| [`kw-nbcc`](kw-nbcc/) | Kuwait National Basic Cybersecurity Controls, NCSC Decision No. 2 of 2026 | 44 controls | JSON, CSV |
| [`kw-corf`](kw-corf/) | CBK Cyber and Operational Resilience Framework v1.0 | 874 controls | JSON, CSV |
| [`kw-crosswalk`](kw-crosswalk/) | Proposed national baseline to CBK mapping, **unreviewed** | 215 candidate pairs | JSON |
| [`kw-lexicon`](kw-lexicon/) | Bilingual security vocabulary from the baseline's parallel text | 44 attested, 228 derived | JSON, CSV |
| [`kw-coverage`](kw-coverage/) | What each half of the baseline contributes in framework terms | 50 CSF references analysed | JSON |

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

## The review rule

`kw-crosswalk` is a proposal, not a mapping. Every pair carries `status:
proposed` with a null reviewer, and the validator fails the build if a pair
claims a reviewed status without a named reviewer, if a decision is recorded on
a still proposed pair, or if the headline reviewed count disagrees with the
file. The method behind it is validated in
[note 0002](../publications/0002-validated-regulatory-crosswalk/).

## Reproducing

```
node scripts/build_corpus.mjs /path/to/Kuwait-NBCC
python3 scripts/build_crosswalk.py
python3 scripts/build_lexicon.py
python3 scripts/build_coverage.py
python3 scripts/validate_corpus.py
```

## Known limitations

The CORF source catalogue reports 876 official controls and yields 874 on
extraction. That gap was investigated rather than left as a round number, and
what is now known narrows it considerably without closing it.

An exhaustive walk of the source, following every path rather than the expected
one, finds the same 874, so nothing is lost in flattening. Control identifiers
run contiguously within every area, so no control is missing from the middle of
a sequence. The domain and subdomain counts match the 25 and 93 the source
declares, so no structural node is absent.

What remains is that the figure of 876 is a claim in the source's own count
object which the structure does not corroborate. Either two controls failed to
extract at a position that leaves no trace, most likely at the end of an area,
or the figure itself is wrong. Settling it requires the framework as issued by
the Central Bank, which this centre does not hold. Until then the dataset should
not be treated as complete.

The derived half of `kw-lexicon` is unreviewed and its validation recovery is
0.808, so roughly one derived entry in five is expected to be wrong. Attested
entries are the regulator's own equivalences and are traceable to a control
identifier.

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
