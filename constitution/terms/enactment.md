---
slug: enactment
element_type: TERM
mutability: MUTABLE
inline: true
current_version: 1
contentURI: null
---

A numeric measure of a participant's accumulated constitutional enactment within the Leviathan federation. Every ratified proposal, accepted vote, validator verdict, or other recognized contribution is one enactment event — bringing a piece of constitutional intent into reality. Enactment is non-transferable (not a token, not currency), serves as the basis for advancing standing, and is recorded across all Sub-Leviathans the participant engages with.

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this term defines

The federation's measure of who has enacted what. Replaces the gamified "XP" terminology used during early prototyping with a constitutional verb: **to enact**. Every accepted contribution doesn't accumulate "experience"; it **enacts a piece of the commonwealth**.

## Etymology and semantic intent

**Enactment** = the act of bringing law / constitution / intent into effect. Constitutional vocabulary native. When a participant's contribution is ratified, they have **enacted** something — a thread, a vote, a proposal, a validator verdict. The count of such enactments is `enactment`.

This is intentionally NOT:
- `experience` — implies passive accumulation through being present
- `points` — implies game token
- `score` — implies competition
- `reputation` — implies opinion-of-others (we measure action, not opinion)

It IS:
- A record of constitutional acts performed
- Earned through specific recognized events
- Owned by the participant (non-transferable)
- The basis for advancing standing

## Properties

1. **Event-based, not time-based** — accrues per accepted action, not per day present
2. **Non-transferable** — cannot be sold, gifted, or moved between accounts (unlike LVTN token)
3. **Domain-aware** — each Sub-Leviathan tracks enactment within its domain; federation aggregates across
4. **Decays slowly with inactivity** — slow decay prevents long-dormant participants from carrying disproportionate weight (decay parameters set per Sub-Leviathan; default TBD)
5. **Quadratic weight basis** — vote weight = sqrt(enactment), per quadratic voting principles (anti-plutocracy)

## Sources of enactment accrual

Federation-wide baseline (subject to refinement):
- Ratified constitutional proposal: +100
- Accepted post (≥3 upvotes): +5
- Validator alignment-check verdict accepted: +20
- Quest completion (per Sub-Leviathan): variable
- Mediated/auto-contribution (advisory tier, v1.1+): +1 (small, encourages, doesn't game)

Each Sub-Leviathan may define domain-specific surfaces (e.g., Animal Welfare may recognize "evidence-tier-A submission" with +10).

## Why mutable

Accrual amounts, decay rates, and per-domain surfaces are operational parameters — should refine based on real federation behavior. The CONCEPT (constitutional enactment as the basis of civic measure) is stable; the SPECIFIC FORMULA evolves.

## Relationship to existing system

- On-chain: `CoreReputation.sol` smart contract in `leviathan-protocol/node` tracks the canonical ledger.
- Off-chain: forum database `users.enactment` column (renamed from `users.xp`) holds the fast-updating mirror, eventually-consistent with chain.
- Migration: `users.xp` column renamed to `users.enactment` in PR #3 (server-side rename + xp increment system).

This term retires the prior "XP" naming, which carried gamified RPG connotations inappropriate for constitutional contribution.

## Related elements

- `standing` (TERM, MUTABLE) — tier system that uses enactment as input
- `vote_weight` (RULE, future) — sqrt(enactment) quadratic formula
- `decay_policy` (RULE, future) — inactivity decay rates
- `CoreReputation` contract — on-chain authoritative ledger
- `enactment_sources` (RULE, future) — formal per-event accrual rules
