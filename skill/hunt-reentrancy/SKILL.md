---
name: hunt-reentrancy
description: "Offensive reentrancy hunter. Find a callback or hook window, re-enter, and move an owned-account asset or authority. Use automatically on contracts, vaults, tokens, and external calls."
---

# Hunt reentrancy

Authorized offensive-first. Look for an external call or token hook
while state is mid-flight, re-enter, and change a balance, share, or
authority on a researcher-owned or local/testnet account.

Read `web3-audit` / `web3-bug-classes` for the catalog. This skill fires
the live attack.

## Attack

Name the function, the call or hook, the stale read/write, and the asset
that moves. Prefer cross-function, read-only-to-decision, ERC-777/hooks,
and transient-storage windows over a textbook CEI miss.

Prove with an owned-account canary, then reverse it. A hit is
`PRIMITIVE_VALID` and goes to `finding-validator` then
`hunt-severity-climb` (share-price, vault drain path, governance).

## Limits

Stay on the in-scope contract. Do not drain, brick, grief, or move
mainnet funds that are not yours.
