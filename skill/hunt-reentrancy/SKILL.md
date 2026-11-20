---
name: hunt-reentrancy
description: "Hunt reentrancy on authorized Web3 or callback surfaces: classic, cross-function, read-only, ERC-777/hooks, and transient-storage windows. Use when a hunt has contracts, tokens, vaults, or external calls. Do not wait to be named. Skip ordinary coding and non-contract web apps."
---

# Hunt reentrancy

One class, one question. Prove a protected-effect window or kill it.

Read `web3-audit` and `web3-bug-classes` only when the current target is a
contract. This skill does not replace those catalogs.

## Question

State the function, the external call or hook, the state read or write
that still sits mid-flight, and the asset or authority that would move.

Kill the lane when:

- Checks-Effects-Interactions plus a real guard close the window
- the hook cannot run on the current in-scope token
- the read-only path cannot change a protected decision
- the next proof needs mainnet funds, persistence, or another person's
  account

## Proof

Use a researcher-owned or local/testnet fixture. Stop at a harmless
canary: a balance or share change on an account you own, then reverse it.
Do not drain, brick, or grief.

Return `KILLED`, `BLOCKED`, `PROMISING`, or `PRIMITIVE_VALID`. Never set
`REPORT_READY`. A valid primitive goes to `finding-validator`, then
`hunt-severity-climb`.
