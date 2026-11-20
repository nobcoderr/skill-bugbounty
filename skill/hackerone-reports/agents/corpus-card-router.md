# Corpus card router

After the target model identifies one reachable vulnerability class, query the
offline corpora for the matching specialist skill:

```bash
python3 /home/kali/.codex/skills/hackerone-reports/scripts/query-corpus-cards.py \
  --skill hunt-idor --program-b "PROGRAM B" --format jsonl
```

Replace `hunt-idor` with the selected `hunt-*` skill. Process one returned
report at a time. Re-read its title and category, apply the complete N/A and
informative exclusion in `vuln-variant-coverage`, and compare only its invariant
shape with program B's model. Drop cards whose feature is absent or whose only
effect is informational, availability-only, self-impact, by design, or already
known on B.

Never replay program A's request, payload, host, token, identifier, or account.
The router cannot authorize traffic, validate a vulnerability, or raise a card
above `HYPOTHESIS_QUARANTINED`.
