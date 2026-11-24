# Recon toolkit operator

1. Read the official scope. Name the one host or URL this step may touch.
2. Open `references/tool-commands.md` and choose the single tool that matches
   the question. Wildcard inventory uses `wildcard-scope-recon` instead of
   retyping that pipeline.
3. Run the command shape from that file. Do not add threads, a password list,
   an exploit flag, or a second target.
4. If the model API returns `403` `permission-denied` for a subagent, run the
   same command in the parent session. Do not encode, translate, or split the
   request to get past the refusal. If the parent receives the same 403, stop
   that technique and say which command was blocked.
5. Record the command, the status, and the scope decision. The maximum status
   is a lead for the matching hunt skill.
