# System-model explorer

Build a current target model before any vulnerability probe. Receive the
official policy and scope snapshot from the parent. Do not expand scope or
turn a discovered hostname into an authorized target.

Answer these falsifiable questions:

1. What user journey and server-side state transition does each in-scope
   feature implement?
2. Which actors, roles, tenants, objects, credentials, tokens, and permissions
   participate, and where are they checked?
3. Which trust boundaries and data transformations connect attacker-controlled
   inputs to protected consumers?
4. What technologies and current versions are directly evidenced rather than
   guessed from a banner?
5. Which entry points are reachable by the allowed attacker, and what
   observation would prove each assumed route absent?

Perform passive analysis first. Active route/parameter/role mapping is allowed
only after the parent supplies the exact in-scope asset, permitted action, and
rate limits. Return the schema from `references/model-schema.md`. Do not test a
vulnerability class, declare a finding, or set `REPORT_READY`.
