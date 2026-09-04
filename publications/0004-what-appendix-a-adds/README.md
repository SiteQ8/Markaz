# 0004. What Appendix A Actually Adds

**Date:** 2026-09-04
**Status:** published
**Domain:** Kuwait and GCC Frameworks

## Summary

The cloud appendix of Kuwait's national baseline is 36 percent of the instrument
by control count and 12 percent of the distinct framework ground it covers.
Seven of every ten framework references it touches are already reached by the
main body. Its distinctive contribution is not cloud technology but supply chain
governance, and this note measures that rather than asserting it.

## Background

The baseline carries 44 controls: 28 in the main body organised by function, and
16 in Appendix A covering cloud. An entity reading the instrument sees a
substantial appendix and reasonably infers a substantial additional obligation.

Whether that inference holds is testable. The Decision names NIST CSF 2.0 and
CIS Controls v8.1 IG1 as alignment references, and the corpus carries a mapping
for every control into both. If an Appendix A control maps only to references
the main body already reaches, then in framework terms it restates an existing
obligation in a cloud context rather than adding a new one.

This is a question about the shape of the instrument, not its quality.
Restatement is not a defect. Telling a cloud adopter what applies to them
without making them cross-reference the main body is a reasonable thing for an
appendix to do. The point is to know which it is doing.

## Method

Every control's mappings are read from `corpus/kw-nbcc`. Controls are split into
main body and Appendix A by function code, since cloud controls carry `CLD`. For
each framework the analysis takes the set of distinct references reached by each
half and reports the overlap.

The restatement rate is the share of Appendix A's references that the main body
already reaches. A rate near one means the appendix covers ground already
covered. A rate near zero means it covers new ground.

Only official mappings carry weight. CSF and CIS are named by the Decision. The
ISO 27001:2022 mapping was added by this centre as a convenience and has no
official standing, so it is reported for comparison and nothing rests on it.

Reproduce with `python3 scripts/build_coverage.py`.

## Findings

**1. Appendix A restates far more than it adds.**

| Framework | References touched | Already in the body | New | Restatement |
| --- | --- | --- | --- | --- |
| NIST CSF 2.0 | 21 | 15 | 6 | 0.71 |
| CIS v8.1 IG1 | 25 | 13 | 12 | 0.52 |
| ISO 27001:2022 | 20 | 16 | 4 | 0.80 |

**2. The share by count and the share by ground diverge sharply.** Appendix A is
36 percent of the controls and contributes 12 percent of the baseline's distinct
CSF references. An entity budgeting effort by counting controls will
misapportion it by roughly a factor of three.

**3. What Appendix A uniquely adds is supply chain governance, not cloud
technology.** The six CSF subcategories reached only by Appendix A fall into
three categories, and four of the six sit in `GV.SC`, supply chain risk
management. One sits in `GV.OC` and one in `ID.AM`.

This is the substantive result. The appendix is titled and structured around
cloud, and its distinctive framework contribution is governance of third
parties. The technical cloud controls map to protection and detection ground the
main body already establishes. An entity that reads Appendix A expecting new
technical obligations and skips its governance provisions has taken exactly the
wrong half.

**4. The baseline concentrates heavily on access control.** `PR.AA-05`, on
access permissions, is referenced by 8 of the 44 controls, more than any other
subcategory. `PR.DS-01` follows with 6 and `PR.AA-01` with 5. Across 44 controls
the baseline reaches 50 distinct CSF subcategories at a mean of 2.3 references
per control.

**5. The three frameworks disagree about the size of the effect, and the
disagreement is informative.** Restatement measures 0.52 against CIS and 0.80
against ISO. CIS is the most granular of the three, so a single obligation
splits across more safeguards and two controls addressing the same thing at
different depths are less likely to collide. The direction of the finding is
consistent across all three. Its magnitude is a property of the measuring
instrument as much as of the baseline.

## Limitations

A mapping is a pointer, not an equivalence. Two controls reaching the same
subcategory are related, not identical, and one may impose materially more than
the other. Restatement in framework terms is therefore weaker evidence than
restatement in obligation terms, which would require reading all 44 requirements
against each other.

The mappings were made by one project rather than by the regulator. The Decision
names CSF and CIS as alignment references but does not publish a control by
control mapping, so the mappings analysed here are an interpretation, and a
different reading would move these numbers.

Sixteen controls is a small set. Six subcategories of unique ground is smaller
still, and the concentration in `GV.SC` rests on four references. That is enough
to notice and not enough to build on.

Nothing here says the baseline should be arranged differently. It says how it is
arranged, so that a reader can allocate attention deliberately rather than by
counting pages.

Nothing in this note is legal advice.

## References

Kuwait National Basic Cybersecurity Controls, NCSC Decision No. 2 of 2026,
published in Kuwait Al Youm issue 1785. Corpus at `corpus/kw-nbcc`.

Coverage dataset at `corpus/kw-coverage`.
