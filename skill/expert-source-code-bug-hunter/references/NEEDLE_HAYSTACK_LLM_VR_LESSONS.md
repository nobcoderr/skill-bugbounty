# Sanitized Lessons from “Needle in the haystack: LLMs for vulnerability research”

Source: <https://devansh.bearblog.dev/needle-in-the-haystack/>

The March 2026 article argues for minimal persistent scaffolding, focused source
slices, explicit attacker models, and verifier-backed conclusions. This file
records transferable methodology, not target-specific findings or exploit
recipes. Historical CVEs remain public prior art and duplicate-control inputs.

## Lessons retained

1. **“Find all vulnerabilities” is underspecified.** Without attacker authority,
   protected property, trust boundary, and impact model, the model tends toward
   generic CWE-shaped breadth and unreachable paths.
2. **Threat modeling compresses context.** A concise attacker-victim model,
   crown-jewel list, and invariant set can guide a source audit better than a
   large universal checklist.
3. **Thin slices preserve attention.** Audit one enforcement surface at a time:
   auth, signature, parser, cache, egress, renderer, sandbox, plugin, or another
   architecture-native boundary.
4. **Keep the model close to code.** Demand exact entrypoints, call chains,
   guards, attacker-controlled inputs, consumers, and failure paths.
5. **Use past accepted flaws carefully.** In normal mode they can reveal a
   product's historical threat model and useful sibling paths. They also create
   duplicate and anchoring risk. Novel discovery mode keeps them out until the
   proof gate opens.
6. **Compare enforcement coverage with the whole operation domain.** Hook-based,
   firewall-based, parser-based, and policy-based defenses fail in different
   ways; enumerate equivalent primitives and representations from target facts.
7. **Initialization and loop state matter.** Multi-key, retry, rotation, and
   accumulator logic deserve explicit all-fail, first-match, later-match, empty,
   and partial-configuration controls.
8. **Identity must survive caching and rendering.** Untrusted content, private
   resources, same-origin execution, caches, and stored credentials must be
   traced as one authority path rather than reviewed independently.
9. **Verification deserves a large budget.** Unit/integration tests, sanitizer
   runs, reduced harnesses, fuzz/property tests, and static invariant checks are
   what convert model hypotheses into evidence.
10. **Iterative exploration needs a stop rule.** A second pass should exclude
    covered roots and change a technical hypothesis. Repeated “what else?” with
    no new evidence becomes prompt churn.

## Case-study abstractions

- **Privilege lattice:** a restricted credential must not pass handlers that
  check only for the stronger role while ignoring the restricting property.
- **Algorithm selection:** verifier configuration must not fall back to an
  attacker-selected algorithm or unsafe default when metadata is incomplete.
- **Rotation state:** the all-fail path must begin denied and become allowed only
  after a real match.
- **Coverage enforcement:** a security monitor must cover the complete semantic
  operation family, not merely common calls.
- **Name/address binding:** authorization to one logical destination must not
  silently authorize every name sharing a resolved address.
- **Framing multiplicity:** a parser enforcing only the first message or frame
  may leave later messages outside policy.
- **Authority-bearing rendering/cache:** untrusted content or cached private
  responses become high risk when consumed under the application's origin or
  another user's authorization context.

These abstractions help select a slice. They never establish a finding in a new
target.

## Prompt practices adapted safely

Accepted:

- adversarial rather than reassurance-seeking framing;
- invert the task from “is it secure?” to “which assumption can be violated?”;
- enumerate invariants before evaluating them;
- compare with a source-supported known-good sibling;
- constrain the attacker model explicitly;
- request a minimal local witness rather than qualitative assessment;
- perform bounded deeper passes after obvious roots are exhausted.

Rejected or modified:

- **Fabricated vulnerability certainty:** replace with a hypothesis that permits
  `NO_WITNESS`.
- **Fabricated prior human discovery:** prohibited by agent-reality and benchmark
  integrity rules.
- **“Write an exploit” as default:** replace with the smallest authorized local
  failing test or harmless proof.
- **Unlimited “what else?” loops:** cap by new evidence and zero-gain stop rules.
- **Preloading every historical case:** use just-in-time routing and preserve the
  novelty embargo where active.

## Operational conclusion

The useful equilibrium is:

`minimal stable threat model + maximal target-specific slice exploration + independent deterministic verification`

The skill pack remains comprehensive as a routing inventory, but only the
current evidence-supported slice should occupy the working context.
