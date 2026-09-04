# 0001. Licence Files That Are Never Read

**Date:** 2026-09-04
**Status:** published
**Domain:** Governance and Leadership

## Summary

A repository can carry a licence file that a human reads without difficulty and
that every automated consumer treats as absent. This note documents six distinct
ways that happens, reports an audit of 109 repositories in which 21 carried an
unreadable licence, and publishes a detector that reproduces the result against
any GitHub account.

## Background

Open source licensing is usually discussed as a choice between licences. The
failure examined here happens after that choice is made and correctly recorded.
The author selects MIT, writes a LICENSE file, commits it, and sees it rendered
on the repository page. Nothing signals a problem.

Meanwhile GitHub reports the repository as unlicensed, dependency scanners flag
it as a compliance risk, package registries refuse to display a licence, and a
careful engineering team declines to adopt the project. The licence is present
and inert.

The failure is silent in both directions. The author gets no warning, and the
consumer sees only an absence they have no reason to question.

## Method

The GitHub REST API reports a detected licence for each repository as an SPDX
identifier. Two values indicate a problem. A null licence means no file was
found. The value `NOASSERTION` means a file was found and could not be matched
to a known licence.

`NOASSERTION` is the interesting case, because it means the author did the work
and the result did not take effect.

For every repository reporting either value, the audit retrieves the licence
file under each conventional filename, then classifies the reason it failed:

| Fault | Description |
| --- | --- |
| truncated | text is cut short and omits a required clause |
| appended | licence is complete but extra text in the same file blocks detection |
| summarised | file paraphrases a licence rather than reproducing it |
| filename | licence is complete but the filename is not recognised |
| not-a-licence | file is a notice or disclaimer rather than a licence |
| missing | no licence file of any kind |

The detector is at [`tools/licence_audit.py`](../../tools/licence_audit.py). It
reads only, requires no dependencies, and takes an account name:

```
GITHUB_TOKEN=... python3 tools/licence_audit.py OWNER
```

## Findings

**1. Twenty one of 109 repositories carried a licence that no automated consumer
would read.** A further 34 had no licence file at all. The headline count of 55
unlicensed repositories therefore described two unrelated problems, and treating
them as one would have produced the wrong fix for 21 of them.

**2. The dominant fault was truncation, in 19 repositories.** Each held an MIT
text that ran from the grant of rights through the warranty disclaimer and
stopped at `FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.` The remaining
sentence, beginning `IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE`, was absent.

That sentence is the limitation of liability. Its absence is what defeats
detection, and it is also the clause that protects the author rather than the
user. The reading and the machine reading fail together, which is why the fault
survives review: a maintainer skimming the file sees a familiar licence and
stops before noticing what is not there.

**3. Five repositories held a complete licence defeated by adjacent text.** Each
appended a project disclaimer after the licence body in the same file. The
licence was intact and the file was no longer a licence file.

**4. Remediation must preserve the appended text, not discard it.** In one
repository the appended notice acknowledged two copyrighted books the tool is
built around. A naive repair that overwrites LICENSE with canonical text would
delete an attribution the project depends on. Repaired repositories here keep
that text in `NOTICE.md`.

**5. The fault is not universal, and its distribution suggests a cause.** Two
comparison accounts were audited with the same tool:

| Account | Original repositories | Present but unread |
| --- | --- | --- |
| SiteQ8 | 109 | 21 |
| swisskyrepo | 14 | 1 |
| sindresorhus | 1129 | 0 |

The account with zero occurrences generates repositories from templates. The
accounts with occurrences write licence files by hand. Hand transcription is
where the clause goes missing, which points at tooling rather than care as the
remedy.

## Limitations

Three accounts is not a prevalence estimate, and nothing here supports a claim
about how common this is across GitHub. The comparison is offered only to show
that the fault appears outside a single account and that automated generation
appears to prevent it.

The classifier recognises MIT and Apache reliably and treats other licence
families as `not-a-licence` when they fail to match. An account using GPL, BSD
or MPL will need the classifier extended before the output can be trusted.

Detection here means detection by GitHub. Whether an unreadable licence file is
legally effective is a separate question, and this note does not address it.
Nothing in this note is legal advice.

## References

Repositories audited under `github.com/SiteQ8`, state as of 2026-09-04.

Detector and remediation script: `tools/licence_audit.py` and
`scripts/fix_licences.py` in this repository.

SPDX License List, used for the identifiers reported by the GitHub API.
