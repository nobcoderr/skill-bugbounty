# Chrome Public Report Routing and Study Ladder

## Authority order

Use sources in this order:

1. [Chrome VRP rules](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules)
2. [Chrome VRP FAQ](https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md)
3. [Chrome Releases](https://chromereleases.googleblog.com/)
4. [Chromium Issue Tracker](https://issues.chromium.org/)
5. Chromium/V8 Gerrit CL, Gitiles commit, regression test, and current source
6. Original reporter write-up, then independent analyses and public PoCs

Chrome Releases establishes that a security fix shipped and supplies the CVE,
issue ID, component, reporter, and sometimes reward. The public issue and landed
CL establish the root and remediation. Secondary write-ups teach analysis and
exploit reasoning but do not override current program rules or source.

The Chromium security lifecycle documents that public issue disclosure normally
occurs after the fix and release process. Public availability therefore makes a
root useful prior art, not a new bounty candidate.

## Eligibility checkpoints

Before retaining a variant, verify from current official material:

- the affected code ships in Chrome Stable, Beta, or Dev;
- the reproducer targets a released build, not only Canary, trunk, or a local
  modified build;
- V8 experimental features and unsafe/debug-only configurations are excluded;
- the Chrome or d8 command line and build flags are exact;
- the PoC is minimized and locally reproducible without a custom harness;
- static reasoning is paired with a demonstrable security consequence;
- ASAN evidence is symbolized when memory safety is claimed;
- current prior art and duplicate status are checked again before submission.

## Patch-led workflow

```text
Chrome Releases
  -> CVE and Chromium issue ID
  -> public issue and fixed CL
  -> vulnerable/fixed revisions and regression
  -> exact invariant restored by the fix
  -> sibling equality/hash/cache/copy/state sites
  -> harmless runtime oracle
  -> current released Chrome reproduction
  -> prior-art and impact gates
```

Do not ask an AI to audit all Chromium randomly. Give it one frozen source
snapshot, one public semantic seed, one component map, one invariant, and one
falsification target at a time. Human review selects the seed and adjudicates
the root; AI is best used for local tracing, inventory, comparison, and bounded
test iteration.

## Study ladder

1. [Journey to Root, Episode I](https://calif.io/research/journey-to-root) —
   human-directed AI-assisted Chrome research and end-to-end chain context.
2. [CVE-2026-15776: From Regex to RCE](https://github.com/Serotav/Writeups/blob/main/v8/CVE-2026-15776-From-Regex-To-Rce.md) —
   original researcher root-to-primitive analysis.
3. [CVE-2026-0899 analysis](https://starlabs.sg/blog/2026/04-check-removed-context-confused-checkmate-achieved/) and
   [official CL 7203465](https://chromium-review.googlesource.com/c/v8/v8/+/7203465) —
   patch-diff and lazy-reparse ordering analysis. Treat exploitation requiring
   removed checks as historical learning, not production proof.
4. [CVE-2026-6307 Part 1](https://tashita.net/turbofan-js-to-wasm-deopt-type-confusion/),
   [Part 2](https://tashita.net/turbofan-js-to-wasm-deopt-type-confusion-part-2/),
   [official fix](https://chromium.googlesource.com/v8/v8/+/1b0cbb19f825), and
   [official CL 7735261](https://chromium-review.googlesource.com/c/v8/v8/+/7735261) —
   the canonical derived-metadata equality seed. Public PoC repositories such as
   `0xsha/CVE-2026-6307` are optional prior art and must never be auto-run.
5. [GitHub Security Lab on CVE-2021-30632](https://github.blog/security/vulnerability-research/chrome-in-the-wild-bug-analysis-cve-2021-30632/) —
   consistency across property access, metadata, and JIT assumptions.
6. [Project Zero: In-the-Wild Series, Chrome Exploits](https://projectzero.google/2021/01/in-wild-series-chrome-exploits.html) —
   real-world exploit reliability and chain context.

If a preferred research site is unavailable, continue from the official issue,
CL, commit, regression, and archived or alternate analyses. Do not make an
unavailable NebuSec article a required dependency.

## Historical seed status

These examples are public and fixed. They are learning material and novelty
burn entries:

- CVE-2026-6307: missing JS-to-Wasm signature comparison in frame-state
  equality; official fix commit `1b0cbb19f825863bbcaccd865ea260859008268b`.
- CVE-2026-0899: class initializer lazy-reparse ordering/ID mismatch; official
  CL 7203465.
- CVE-2021-30632: JIT/global-property metadata inconsistency.

Only a different exact root that still reaches an eligible current Chrome build
may enter the candidate pipeline.
