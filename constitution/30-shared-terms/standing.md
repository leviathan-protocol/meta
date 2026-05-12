---
slug: standing
element_type: TERM
mutability: MUTABLE
inline: true
current_version: 1
contentURI: null
---

A participant's civic position in the Leviathan federation, expressed as a tier. Standing carries different rights and responsibilities (vote, propose, validate, moderate). Standing is earned through enactment accumulation, never granted by edict. Current tiers (ascending): novice (signup default, reply-only) → sentinel (vote + propose) → guardian (board moderation) → arbiter (cross-domain authority).

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this term defines

The civic position of each federation participant. Replaces the gamified "rank" terminology with **standing** — a civic word meaning one's recognized position in a body. Standing is civic; rank is military/competitive. Leviathan uses civic.

## Etymology and semantic intent

**Standing** = one's recognized position within a civic body. From law: "standing to sue" means having recognized position to bring a case. In Leviathan: one's standing is what they may do constitutionally.

This is intentionally NOT:
- `rank` — military/hierarchy
- `level` — gaming
- `tier` — neutral but flat
- `class` — class-based connotations
- `caste` — rigid stratification

It IS:
- A recognized civic position
- Earned through enactment, not granted
- Tied to specific constitutional rights
- Transparent (visible to all)

## Tier definitions (v1, refinable)

### Novice (default at signup)
- Can read all public boards
- Can reply to threads
- **Cannot** create threads
- **Cannot** vote
- Threshold to advance: 10 accepted contributions (replies with ≥1 upvote, or constitutional draft accepted into review)

### Sentinel (entry-level full participant)
- All novice rights
- Can create threads (constitutional proposals)
- Can vote (vote weight = sqrt(enactment))
- Can flag content for moderation
- Threshold: accumulated enactment ≥ 100 + active for ≥30 days

### Guardian (board moderator)
- All sentinel rights
- Can moderate Sub-Leviathan boards (lock threads, mark spam, escalate disputes)
- Can validate quest completions for the Sub-Leviathan they guard
- Threshold: enactment ≥ 1000 + elected by Sub-Leviathan participants (governance vote)

### Arbiter (cross-domain authority)
- All guardian rights
- Can mediate cross-Sub-Leviathan disputes
- Can propose federation-level amendments
- Can participate in ratification-tier validation
- Threshold: enactment ≥ 10000 + federation-wide vote (high bar)

## Properties

1. **Earned, never granted** — no founder/admin grant of high standing; advancement comes from enactment + community recognition
2. **Domain-specific recognition possible** — a participant may be Guardian standing in Animal Welfare but Sentinel standing in Music; cross-Sub-Leviathan recognition is separate
3. **Recall possible** — sustained inactivity, abuse findings, or community recall vote can lower standing
4. **Transparency** — participant's current standing + how it was earned is publicly visible (per kernel's transparency principle)

## Why mutable

Tier thresholds and rights are operational parameters. As the federation matures, thresholds will tune to actual behavior (early-day "100 enactment" may be too low or too high). The CONCEPT (earned civic tier system) is stable; the SPECIFIC BOUNDARIES evolve.

## Tier names — why these specific words

The four tier names (novice, sentinel, guardian, arbiter) are deliberately Leviathan-native:

- **Novice** — one new to the constitutional practice; learning to enact
- **Sentinel** — one who watches over the constitution; the first level of active defense
- **Guardian** — one who actively maintains a Sub-Leviathan's domain
- **Arbiter** — one who judges cross-domain matters

These are civic guardianship roles, not RPG combat classes. They carry duty and trust, not just power.

## Relationship to existing system

- Database: `users.rank` column retained for migration compatibility; semantic name is `standing`. Future migration may rename column to `users.standing`.
- On-chain: standing is derived from enactment via `CoreReputation` smart contract; no separate "standing contract" needed.
- Migration: PR #3 server-side adds advancement logic; PR #3.1 may rename column.

This term retires the prior "rank" naming, which carried gamified/militaristic connotations inappropriate for civic standing.

## Related elements

- `enactment` (TERM, MUTABLE) — input to standing advancement
- `vote_weight` (RULE, future) — sentinel+ only, sqrt(enactment) weighted
- `moderation_authority` (RULE, future) — guardian+ powers
- `federation_amendment` (RULE, future) — arbiter+ proposal rights
- Federation Kernel principle of democratic-evolution — earned-not-granted is foundational
- `enactment_sources` (RULE, future) — what events accrue enactment toward standing
