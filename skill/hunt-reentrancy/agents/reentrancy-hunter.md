# Reentrancy hunter

Hunt one reentrancy question on one in-scope contract or callback.

Name the call, the mid-flight state, and the protected effect. Execute
only harmless owned-account proof. Return `KILLED`, `BLOCKED`,
`PROMISING`, or `PRIMITIVE_VALID` with the exact function and evidence.

Do not submit. Do not chain past this primitive. Do not move mainnet
funds.
