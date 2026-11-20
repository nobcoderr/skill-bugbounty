# Scope snapshot schema

Keep the downloaded official policy body beside the JSON file. Hash that exact
file; do not hash a paraphrase.

```json
{
  "program": "Exact program name",
  "source_url": "https://official.example/program/policy",
  "source_kind": "official_program",
  "captured_at": "2026-11-15T00:00:00+07:00",
  "policy_file": "official-policy.html",
  "policy_sha256": "64 lowercase hexadecimal characters",
  "assets": [
    {
      "asset": "app.example.com",
      "status": "in_scope"
    }
  ]
}
```

`source_kind` is either `official_program` or `official_repository`.
`captured_at` must include a timezone and be no older than seven days. Every
asset must be copied from the current official policy and explicitly marked
`in_scope`; exclusions stay in the policy file and must still be obeyed.
