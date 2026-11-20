# State-Machine Security Method

## Build the machine

Identify authoritative states, transition functions, guards, side effects,
persisted markers, queue messages, retries, cancellation, rollback, restore,
and terminal states. Derive legal transitions from code and tests instead of
assuming the documented happy path is complete.

For every transition record:

| From | Event | Principal | Guard | Written state | Delayed effect | To |
|---|---|---|---|---|---|---|
| | | | | | | |

Include error, timeout, duplicate, recovery, compatibility, and shutdown paths.

## Mine state invariants

Ask whether:

- authority is still valid when a delayed operation executes;
- a revoked or replaced object can be consumed through stale identity;
- retry repeats a non-idempotent protected effect;
- partial success makes mutually exclusive states coexist;
- cancellation or rollback removes all derived authority and artifacts;
- cached state outlives the policy, identity, or generation it represents;
- recovery bypasses a guard required on the normal path;
- two legal transitions compose into an illegal state.

Write each invariant as a precondition and protected postcondition.

## Explore sequences

Generate bounded sequences from attacker-reachable events. Prioritize:

- create -> approve -> revoke -> use;
- enqueue -> authority changes -> execute;
- validate -> replace -> consume;
- authenticate -> cache -> revoke -> reuse;
- start -> timeout -> retry -> commit;
- upgrade -> rollback -> restore.

These are abstract sequence shapes, not payloads. Bind names and events to the
target's actual state machine.

Use partial-order reasoning for concurrent events. Change one ordering edge at
a time and retain a baseline schedule that must remain safe.

## Proof requirements

Before `state_proven=true`, show:

- the complete attacker-reachable sequence;
- state before and after every event;
- the authoritative store, not only UI or logs;
- the guard and consumer identity at execution time;
- a negative schedule differing by one event/order;
- repeatability and cleanup.

KILL impossible sequences, intended equal-authority transitions, idempotent
effects, or paths blocked on the current release.
