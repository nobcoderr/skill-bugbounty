---
name: bug-bounty-browser
description: "Control the user's own Chromium with Playwright during an authorized bug-bounty test, including moving and clicking the real mouse cursor. Use when a bug-bounty page, login, signup, browser challenge, or pointer click must run in the user's browser. Do not use it for ordinary coding, and do not launch a throwaway profile."
---

# Bug bounty browser

Drive the user's browser with Playwright. A skill does not authorize a
target. Open a page only after the program and the in-scope host are
already named.

Google Chrome and the BugBounty profile (Windows Profile 2) are not
installed on this Kali machine. Use the local fallback below. Do not
invent that Windows profile, do not create a new user-data directory,
and do not use Cursor's built-in browser.

## Browser

- Binary: `/usr/bin/chromium`
- Profile: `/home/kali/.config/chromium`
- DevTools: `http://127.0.0.1:9222`
- Playwright: `/home/kali/.local/lib/bb-browser`
- Command: `bb-browser`

This is the user's Chromium profile. Do not attach to the Firefox ESR
mailbox profile `~/.config/mozilla/firefox/65twzm6c.default-esr`. That
profile is only for `bug-bounty-account` OTP reads.

## When to use it

Use this during bug bounty when curl cannot complete the step: a login
wall, a browser challenge, a signup form, or a page whose script must
run. Do not ask first. Do not use it for ordinary coding.

If port `9222` is closed, run `bb-browser start`. When the hunt is also
using Burp, run `bb-browser start --proxy` so only this browser uses
`127.0.0.1:8080`. Do not set a system proxy.

## How to drive it

Connect Playwright to the running browser. Do not call `chromium.launch`
and do not pass a new `userDataDir`.

```bash
cd /home/kali/.local/lib/bb-browser
node --input-type=module << 'EOF'
import { chromium } from 'playwright';
const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const context = browser.contexts()[0];
const page = await context.newPage();
await page.goto('https://IN_SCOPE_HOST/', { waitUntil: 'domcontentloaded' });
console.log(JSON.stringify({ url: page.url(), title: await page.title() }));
await browser.close();
EOF
```

`browser.close()` after `connectOverCDP` disconnects Playwright. It must
leave the Chromium window open. If a test shows it closed the window,
stop calling `close()` and leave the Node process to exit.

`bb-browser open https://IN_SCOPE_HOST/path` does the same navigation
and prints only the final URL and title.

## Cursor

Move the visible pointer with `xdotool`. Playwright's mouse events do
not move it. Coordinates are CSS pixels inside the page, measured from
the top left of the viewport.

- `bb-browser move X Y` moves the pointer.
- `bb-browser click X Y` moves there and clicks.
- `bb-browser click-text TEXT` moves to the visible text and clicks.

Use these when a control must see a real pointer, including a challenge
checkbox. Keep the point inside the page. Do not click another window.

## Limits

Send the browser only to a host already in the named scope. Do not print
cookies, passwords, OTPs, tokens, or storage. Do not read the mailbox
profile. Leave intercept off unless one specific request must be held,
and keep that request inside Burp rather than inside this browser.
