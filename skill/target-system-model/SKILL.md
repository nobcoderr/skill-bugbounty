---
name: target-system-model
description: "Before vulnerability testing on an authorized bug bounty target, learn how the system works, then do passive and active recon, fingerprinting, threat modeling, and attack-surface mapping. Use at the start of a web, API, mobile, or source-code bounty. Do not hunt bugs before this model exists."
---

# Target system model

Build this model before `vuln-variant-coverage` or any exploit hypothesis.
The target must already be an official in-scope asset. Read the program
policy first.

## Order

1. **How the system works.** Read official docs, the in-scope source tree,
   and one real user journey. Record actors, data objects, trust boundaries,
   authentication, authorization, and the feature that changes state.
2. **Passive recon.** Use public DNS, certificate names, archives, JavaScript,
   and `gtm-recon` when Tag Manager is present. Do not send exploit probes
   in this pass.
3. **Fingerprinting.** Name the framework, language, auth, API style, and
   version from responses and source. A version is a fact only when the
   current response or file shows it.
4. **Active recon.** Map live routes, parameters, roles, and hosts that the
   program lists. Stay inside scope and rate limits. Use Burp when HTTP
   history is needed.
5. **Threat model.** For each boundary, write the attacker position, the
   protected object, and the effect that would matter to this program.
6. **Attack surface.** List entry points that an allowed attacker can
   actually reach. Drop hosts and features the program excludes.

Write the model down and keep it with the hunt. Vulnerability lanes start
only after the surface list exists. A new asset discovered later goes
through the same six steps before it is tested.

Use `agents/system-model-explorer.md` for the delegated mapping role and
`references/model-schema.md` for the handoff. Set `MODEL_READY=YES` only when
the current official scope, system flow, actor/object/permission map, trust
boundaries, evidenced fingerprints, reachable entry points, and exclusions are
all recorded. Unknowns remain explicit; they are not filled by inference.
