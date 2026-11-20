# libheif Derived-Item and Pixel-Plane Invariant Method

## Purpose and prior-art status

Use this method for authorized source review of native image pipelines where
logical image metadata, derived items, auxiliary images, and physical channel
planes can diverge. It distills the root-cause methodology from
GHSA-2jg2-4ch7-h545.

The advisory lists libheif versions through 1.23.1 as affected and 1.23.2 as
patched. It reports a confirmed RCE proof and 11 related vulnerabilities. The
exact derived-item/pixel-plane root is therefore public prior art. Re-check the
current advisory, distro backports, and deployed artifact before using any
version statement in a report.

## Central invariant split

Do not treat a decoded image as one geometry object. Model at least:

```text
logical item geometry: width, height, transforms, declared channel layout
physical plane state:  allocation width, allocation height, stride, element size
channel mapping:       channel -> zero/one/multiple/aliased planes
derivation graph:      source -> identity-derived item -> auxiliary chain -> consumer
```

The public root arose because consumers trusted logical width/height for plane
access and assumed a single backing plane per channel, while derived and
auxiliary item composition could violate those assumptions.

## Procedure

### 1. Build producer and consumer maps

Enumerate every producer or transformer that can create, copy, attach, replace,
or alias planes:

- ordinary coded image creation;
- identity-derived items;
- auxiliary image chains;
- crop, scale, rotate, overlay, tile, alpha, depth, or color conversion;
- lazy decode/cache paths;
- channel insertion/replacement helpers.

Then enumerate every consumer that indexes, loops, copies, divides, allocates,
or computes offsets from logical geometry. Group by root invariant, not crash
site alone.

### 2. Record the geometry used at each operation

For every memory operation, record:

```text
loop bounds source
plane allocation dimensions
stride and bytes per sample
channel-to-plane lookup result
offset/size arithmetic type
validation dominating the access
```

Flag consumers where bounds come from item-level geometry while the pointer and
stride come from a differently sized plane.

### 3. Generate valid-structure differential fixtures

Prefer structurally valid images that vary one semantic relation at a time:

| Fixture | Purpose |
|---|---|
| ordinary coded item | baseline |
| derived item with equal geometry | safe sibling |
| derived item with smaller backing plane | bounds mismatch |
| derived item with larger backing plane | asymmetric control |
| auxiliary chain with mismatched geometry | composition path |
| repeated or aliased channel plane | cardinality/alias invariant |
| zero dimension or stride edge | arithmetic/division control |

Avoid random byte mutation as the primary method. The goal is to preserve the
container grammar while changing the producer-consumer invariant.

### 4. Use sanitizer-backed deterministic oracles

Run the smallest decoder or library harness under ASan and UBSan. Preserve:

- exact release/commit/compiler and sanitizer options;
- minimized input and SHA-256;
- full stack trace and first invalid access;
- allocation site, access size, and offset;
- three-run reproducibility;
- safe sibling and patched-version result.

A decoder error is not memory corruption. A sanitizer crash is a primitive,
not automatically RCE.

### 5. Hunt variants by invariant coverage

After one consumer fails, search all consumers of the same representation for:

- logical/physical dimension disagreement;
- missing per-plane validation after derivation;
- channel replacement or multiple-plane ambiguity;
- integer overflow/underflow in stride and offset calculations;
- divide-by-zero when logical or plane dimensions collapse;
- stale validation before a later transform changes the plane;
- safe checks on one channel but not alpha, depth, or auxiliary siblings.

Deduplicate crashes that share the same unchecked invariant and fix locus.
Separate findings only when the sink, impact, and required remediation are
materially different.

### 6. Prove release and downstream reachability

For a downstream application, prove the whole path:

```text
attacker-controlled upload/input
  -> MIME/extension/content dispatch
  -> exact ImageMagick/libheif build
  -> vulnerable decoder function
  -> sandbox/process identity
  -> protected application effect
```

Package version strings alone are insufficient because distributions may
backport fixes. Compare source package patches or function-level code identity.
If only the upstream library is in scope, do not infer application, SSO, cloud,
or connector impact.

When a native decoder primitive plausibly reaches an application identity or
connector boundary, additionally load the package-level
`IMAGE_DECODER_SSO_CONNECTOR_CHAIN_METHOD.md`; keep each authority transition
separate.

### 7. Escalate severity only from demonstrated primitives

Use these states:

```text
PARSE_REJECTION
CONTROLLED_CRASH
OOB_READ
OOB_WRITE
RELIABLE_MEMORY_PRIMITIVE
CONTROL_FLOW_OR_CODE_EXECUTION
SANDBOX_OR_PROCESS_AUTHORITY
APPLICATION_OR_IDENTITY_AUTHORITY
```

Do not skip states. RCE requires a working local proof or equivalent vendor-
confirmed evidence bound to the exact root and build. A downstream cloud or
account claim requires a separately proven, authorized bridge.

## Evidence matrix

```text
CURRENT_ARTIFACT_IDENTITY       = PASS / FAIL
STRUCTURALLY_VALID_FIXTURE      = PASS / FAIL
LOGICAL_PHYSICAL_MISMATCH       = PASS / FAIL
CONSUMER_ACCESS_TRACE           = PASS / FAIL
ASAN_OR_UBSAN_ORACLE            = PASS / FAIL
SAFE_SIBLING_CONTROL            = PASS / FAIL
PATCHED_VERSION_CONTROL         = PASS / FAIL
DOWNSTREAM_FORMAT_DISPATCH      = PASS / BLOCKED / NOT_APPLICABLE
PROCESS_AUTHORITY               = PROVEN / BLOCKED / NOT_TESTED
RCE                             = PROVEN / VENDOR_CONFIRMED / NOT_PROVEN
PUBLIC_EXACT_ROOT_PRIOR_ART     = FOUND / NOT_FOUND
REPORT_ELIGIBILITY              = PASS / BLOCKED / KILL
```

## Falsifiers and kill conditions

- The current artifact includes the fix or a verified downstream backport.
- The malformed relation cannot be constructed through accepted file grammar.
- Plane dimensions are validated after every derivation and before the sink.
- The crash originates in the harness or an unsupported build configuration.
- Only denial of service is proven while the program excludes crashes/DoS.
- A downstream application does not dispatch the format to the affected build.
- The same root/fix is already covered by the advisory or prior report.
- The claimed RCE, sandbox escape, SSO, or cloud impact lacks its own bridge.

## Source

- GHSA-2jg2-4ch7-h545, "Remote Code Execution: Out-of-bounds read and write in
  derived-item and pixel-plane handling," published August 25, 2026:
  https://github.com/strukturag/libheif/security/advisories/GHSA-2jg2-4ch7-h545

