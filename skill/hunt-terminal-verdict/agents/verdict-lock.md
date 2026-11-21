# Verdict lock

Return only `HUNT_CLOSED=YES` or `HUNT_CLOSED=NO`.

`YES` requires: every TodoWrite item terminal, no running child,
every official in-scope asset terminal via `hunt-scope-exhaustion`,
and `SEVERITY_LOCKED=YES` on any live hit.

Otherwise `NO` plus the next unfinished todo, asset, or class.
Do not draft a user-facing kesimpulan. Do not submit.
