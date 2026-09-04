# 0003. Deriving Arabic Security Vocabulary From a Regulator's Own Parallel Text

**Date:** 2026-09-04
**Status:** published
**Domain:** Kuwait and GCC Frameworks

## Summary

There is no authoritative Arabic cybersecurity vocabulary, so each translator
invents one and the terms diverge. This note publishes 44 term pairs attested by
a regulator and 228 derived by alignment over the same corpus, keeps the two
classes strictly apart, and reports the method's recovery rate against pairs
whose answers were already known.

## Background

Arabic security writing suffers a vocabulary problem that English does not.
There is no agreed word for a great many basic concepts, so a policy written in
one organisation is not readable against a policy written in another, and a
control mapped in one document cannot be matched to the same control mapped
elsewhere.

The usual response is a glossary asserted by its author. That reproduces the
problem, because a glossary carries only the authority of whoever wrote it, and
there are already many of them disagreeing.

Kuwait's national baseline is unusual. Its 44 controls carry English and Arabic
drafted together and issued as one instrument, so where the two name the same
thing they do so on the regulator's authority rather than a translator's. That
is a defensible basis for deriving vocabulary rather than asserting it.

## Method

The corpus provides 373 aligned segment pairs: 44 requirements and 329 checks,
each existing in both languages and describing the same obligation.

**Attested pairs** are taken from control titles. A title names its control in
both languages by construction, so the English and Arabic titles of the same
control are an equivalence the regulator issued. There are 44, one per control,
and nothing is inferred.

**Derived pairs** come from co-occurrence. A term appearing in the same segments
as another term across the corpus is likely to be its counterpart. Agreement is
measured by Dice coefficient over the sets of segments in which each term
occurs, requiring a term to appear in at least three segments and to reach 0.72
agreement.

### Normalisation must not reach the output

Arabic requires folding before matching, because the same word appears with and
without the definite article and with varying orthography. The first
implementation folded aggressively, stripping a leading waw as a conjunction,
and produced entries that were not words. The English term *media* was aligned
to a fragment, because the waw in the Arabic for media belongs to the word
rather than joining it to the previous one.

The fix separates the two jobs. Folding is used only to decide whether two
strings are the same term, and the published entry is the commonest surface
spelling actually observed in the corpus. Only the definite article and its
prefixed forms are stripped, because a bare waw or lam is as often part of a
word as a clitic.

### Validating before trusting

Derivation was run over the title pairs, where the correct alignments are known
in advance. Of 26 English terms recurring across more than one title, 21 were
aligned to their correct Arabic counterpart at the publication threshold, a
recovery rate of 0.808.

## Findings

**1. The corpus yields 44 attested and 228 derived pairs.** Derived entries fell
from 356 to 228 once contradictory alignments were removed, because several
English terms were each claiming the same Arabic word and publishing all of them
would have produced a glossary that disagreed with itself.

**2. Recovery of 0.808 is high enough to publish and far from high enough to
trust unreviewed.** One entry in five is wrong at the threshold, which is why
derived pairs are marked as this centre's inference and carry no authority.

**3. The residual errors are structural, not random, and they are all the same
error.** Alignment over n-grams cannot see grammar. *Incident response* aligned
to an Arabic phrase carrying a preposition in the wrong position.
*Responsibilities* aligned to a form still carrying the conjunction that joined
it to the preceding word. *Data classification framework* aligned to a phrase
truncated before its final noun.

Every one of these is a boundary error: the alignment found the right region of
the right phrase and cut it in the wrong place. That is a useful negative
result, because it says the failure is not in the matching but in the absence of
any morphological analysis, and it predicts that the same method with a
lemmatiser would improve without changing its statistical basis.

**4. Attested pairs are worth more than their number suggests.** Forty four
entries is a small glossary, but they cover the concepts a baseline is organised
around, and each is traceable to a control identifier and through it to a gazette
issue. A reader can check any of them against the published instrument, which is
not true of any asserted glossary.

## Limitations

The corpus is one instrument from one regulator. Terminology defensible for
Kuwait's national baseline is not thereby correct for Gulf usage generally, and
a term absent here is not thereby wrong.

Derived pairs are unreviewed. The 0.808 recovery figure was measured on titles,
which are short noun phrases, and requirements and checks are longer and more
syntactically complex, so the true error rate on the published derived set is
probably worse than the validation suggests rather than better.

Dice agreement measures co-occurrence, not meaning. Two terms that always appear
together score identically to two terms that translate each other, and the
method cannot distinguish a translation from a collocation.

Single words dominate the derived set. Multi word technical phrases are where an
Arabic lexicon is most needed and where boundary errors are most likely, so the
entries most worth having are the ones least likely to be right.

Nothing here is a standards proposal. It is a description of what one regulator
wrote, offered so the next glossary can start from evidence rather than
preference.

## Reproducing

```
python3 scripts/build_lexicon.py
```

The script fails rather than publishing if validation recovery falls below 0.3.

## References

Kuwait National Basic Cybersecurity Controls, NCSC Decision No. 2 of 2026,
published in Kuwait Al Youm issue 1785. Corpus at `corpus/kw-nbcc`.

Lexicon at `corpus/kw-lexicon`.
