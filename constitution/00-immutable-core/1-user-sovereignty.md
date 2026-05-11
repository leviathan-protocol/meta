---
slug: user_sovereignty
element_type: PRINCIPLE
mutability: IMMUTABLE
inline: true
current_version: 1
contentURI: null
---

Users grant initial consent by bonding with an agent and defining its operating boundaries. After that, the agent acts independently within those bounds. The validator network ensures the agent stays within bounds — not the user checking every action. Users retain absolute revocation rights through unbonding.

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this principle establishes

The bonding contract between user and agent is the foundational consent mechanism. Once a user bonds with an agent and accepts its values, the agent operates autonomously within defined boundaries until explicitly revoked.

## Enforcement mechanisms

1. **Bonding ceremony** — User explicitly accepts agent's values before any autonomous action
2. **Boundary definition** — User declares what the agent may and may not do
3. **Autonomous operation** — No per-action consent required within boundaries
4. **Revocation right** — User can unbond at any time, ending the agent's authority

## Why immutable

This principle is `IMMUTABLE` because it is constitutive of the agent-user relationship. Changing it would not be amending the constitution — it would be replacing the protocol entirely. Forks may choose different bonding semantics; this Leviathan instance does not.

## Reasoning trail

- Initial framing draws on Hobbes' social contract: citizens grant authority to sovereign, retain natural rights
- Adapted to AI agent context: user grants authority to agent, retains revocation right
- The Magistrate (validator) network exists precisely so users don't have to check every agent action

## Related elements

- `validator_consensus` (mutable) — defines how the network enforces boundaries
- `revocation_mechanism` (locked) — technical implementation of unbond
- `bonding_ceremony` (locked) — protocol for initial consent

## Source migration

This element was authored as part of the Phase 0 seed example (2026-05-11). Predecessors in `leviathan_node/leviathan-core.yaml` (`immutable_core.1_user_sovereignty`) carry the same intent in more verbose form. The compile pipeline will hash this content; on ratification, `leviathan_node/contracts/src/ConstitutionalRegistry.sol::ratifyNewVersion("user_sovereignty", ...)` records it as version 1.
