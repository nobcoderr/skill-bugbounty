---
name: bug-bounty-account
description: "Create the researcher account for an authorized bug bounty program with argareksapatii@wearehackerone.com, store a generated password, and read the signup OTP from grokgblk@gmail.com without asking the user to confirm."
---

# Bug bounty account

Use this when an authorized bug bounty or VRP task needs a researcher-owned
account, registration, or email verification code. Do not ask the user before
creating that account or before reading the OTP for it.

## Identity

- Email: `argareksapatii@wearehackerone.com`
- Password: generate a new one per site. Do not invent a shared password and
  do not ask the user to choose one.
- OTP mailbox: `grokgblk@gmail.com`

Store and retrieve credentials only through:

```bash
bb-account save <host>
bb-account otp --host <host>
```

`bb-account save` prints the new password once on stdout so it can be entered
into the signup form. Do not repeat that password in the chat reply. Record
the host and the email only.

## OTP

Run `bb-account otp --host <host>` immediately after the site sends a code.
Do not wait for the user to confirm, forward, or read the code. The command
reads that code from the Firefox session already logged in as
`grokgblk@gmail.com`. Use the code only for the signup or login that this
task just started. Do not read, summarize, or store unrelated mail.

If the command returns `BLOCKED_MAILBOX`, the Gmail session is missing. Say
that once and stop the signup. Do not invent a code and do not ask the user
to approve an OTP that was never requested.

## Limits

Create an account only for the program or asset the user has already put in
scope. Do not register on an out-of-scope site, a look-alike domain, or an
account that belongs to someone else. Do not change the mailbox password,
forwarding rules, or recovery options.
