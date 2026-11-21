---
name: hunt-terminal-verdict
description: "Lock the hunt or audit conclusion until every todo, lane, and in-scope asset is actually finished. Cursor must match Codex CLI: no NO VALID FINDING, no hasil audit, and no REPORT_READY while work remains, and never conclude twice. Use automatically on bug bounty and multi-step audits. Ordinary one-shot answers do not enter this skill."
---

# Hunt terminal verdict

Codex CLI emits the audit conclusion only after there is nothing left
to do. Cursor must do the same.

A lane miss is `KILLED` or `EXHAUSTED` in the ledger. It is not a
user-facing `NO VALID FINDING`. Pack lines that say "if none survive,
output NO VALID FINDING" are lane-local. They do not close the hunt.

## Work still remains

Do not write a final kesimpulan, hasil audit, `NO VALID FINDING`,
tidak ada temuan, `REPORT_READY`, or hunt-complete summary while any
of these is true:

- a TodoWrite item is `pending` or `in_progress`
- a subagent, shell, browser, Burp, or MCP call is still running
- an official in-scope asset is `UNMAPPED`, `ACTIVE`, or `PROMISING`
- `hunt-scope-exhaustion` still has an empty feature × class cell
- a live hit exists and `SEVERITY_LOCKED` is not `YES`
- a retry wave from `adaptive-plan-check-loop` is still in budget

Do not mark todos completed only to unlock a conclusion.

## One conclusion

Set `HUNT_CLOSED=YES` only when every todo is `completed` or
`cancelled` with a reason, every in-scope asset is `EXHAUSTED`,
`BLOCKED`, `KILLED`, or `VALIDATED`, and no child is running.

Then emit **exactly one** terminal message:

- a finding: `REPORT_READY=YES` or the exact blocker;
- no finding: `NO VALID FINDING` plus the exhausted matrix.

If a conclusion already went to the user and work continues, that
conclusion is void. Keep working. Do not send a second audit
summary until `HUNT_CLOSED=YES`. Progress lines stay short and
must not sound final.

## Agents

Spawn `agents/verdict-lock.md` before any user-facing audit
summary. It returns `HUNT_CLOSED=YES` or `HUNT_CLOSED=NO` with
the remaining work. The parent may speak a verdict only on `YES`.
