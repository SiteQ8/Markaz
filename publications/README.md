# Publications

Research notes from the centre. Each note is numbered, dated and self contained.

## Format

```
publications/
  0001-short-slug/
    README.md        English text
    README.ar.md     Arabic text
    CITATION.cff     citation metadata
    data/            any supporting data
```

## Rules

Numbering is sequential and never reused. A published number is permanent even if the
note is later superseded, in which case the original stays and gains a pointer to its
replacement at the top.

Each note exists fully in both languages. A note is not published until both versions
are complete, because a half translated research centre is worse than a monolingual one.

Every factual claim about a Kuwaiti or Gulf regulation cites the issuing decision by
number and date. Claims about tooling cite the specific commit or release.

## Citation and DOI

Tag a release when a note is final. Zenodo is wired to this repository, so each release
receives a persistent DOI automatically. Cite the DOI, not the branch.
