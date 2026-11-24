# Wildcard recon operator

Run only when `mandatory-auto-router` marks `wildcard-scope-recon` ACTIVE and
the official scope contains a wildcard. The attacker objective at this stage
is a reachable in-scope entrypoint, not a finished exploit chain.

1. Read the scope file and quote the wildcard line that covers `--domain`.
2. Run `scripts/wildcard-recon.sh --check-scope` first. If it fails, stop.
3. Run passive mode before active mode. Active mode requires the program to
   allow automation and the flag `--i-am-authorized`.
4. Read `summary.txt`, `meta/missing-tools.txt`, and
   `meta/rejected-out-of-scope-hosts.txt`.
5. Choose the smallest set of live in-scope hosts whose titles, technologies,
   or paths indicate authentication, an API, an admin surface, or file
   handling. Hand those hosts to the matching hunt skill.
6. Do not treat a tool hit as a finding. Do not request a host that the scope
   filter rejected. Do not widen the wordlist, rate, or host budget.

Maximum status from this role is an inventory plus a falsifiable next
question. Validation belongs to the hunt skill and an independent review.
