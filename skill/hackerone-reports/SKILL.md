---
name: hackerone-reports
description: "Use the pinned reddelexc/hackerone-reports corpus as prior-art context for authorized bug bounty work. Read the local reports when a bug class or program history matters. Do not scrape HackerOne unless the user explicitly asks to refresh the corpus."
---

# HackerOne report corpus

Local clone: `/home/kali/security-research/hackerone-reports`
Pinned commit: `4c279ab` (2026-11-07).
Source: `https://github.com/reddelexc/hackerone-reports`

Use the checked-in files only:

- `data.csv` for raw rows
- `docs/tops_100/` for upvote and bounty rankings
- `docs/tops_by_bug_type/` for a bug class
- `docs/tops_by_program/` for a program name

For automatic class routing, run `scripts/query-corpus-cards.py` through the
`agents/corpus-card-router.md` role after `target-system-model` identifies a
reachable class. The script merges both local corpora, deduplicates report IDs,
excludes explicit N/A/informative/by-design/duplicate/spam titles and strong
impact-free title shapes, and returns quarantined cards for the selected
`hunt-*` skill. It never fetches a report or contacts a target.

The second local corpus is
`/home/kali/security-research/hackerone-bug-bounty-reports` at `cb5d63c`
(`results/based_on_vulnerability_type/` and `results/based_on_program/`).
Read it the same way. Do not run `main.py` there unless the user explicitly
asks to refresh that corpus.

When hunting program B, read another program's file as program A and follow
`vuln-variant-coverage` to test that bug shape on B. A's report is prior
art, not proof that B is vulnerable and not proof that B is a duplicate.
Confirm against B's current program, release, and primary source.

Do not run `fetcher.py`, `filler.py`, or `rater.py` unless the user
explicitly asks to refresh this corpus. Those scripts browse the live
HackerOne site.

The repositories do not contain a reliable triage-resolution field for every
report. Therefore script output is never directly testable: the corpus analyst
must apply the N/A/informative gate in `vuln-variant-coverage` before a card
enters program B's queue. Unknown eligibility stays quarantined rather than
being assumed valid.
