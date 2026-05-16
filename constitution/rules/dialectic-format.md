---
slug: rule_dialectic_format
element_type: RULE
mutability: LOCKED
inline: false
current_version: 1
contentURI: null
inherited_by: [medicine, scream, animal-welfare, companion]
implements_principles: [witness_principle]
uses_terms: [dialectic, proposal]
---

Every constitutional discussion thread in any federation forum board MUST contain three structural elements before the proposal can transition out of the DISCUSSION phase:

1. A post labeled **`[THESIS]`** — the original proposal as defined by the `proposal` term.
2. Either:
   - a post labeled **`[ANTITHESIS]`** containing substantive counter-arguments, OR
   - an explicit moderator entry labeled **`[NO_OBJECTIONS_LOGGED]`**, posted no earlier than 7 days after the thesis, in which a participant holding at least `guardian` standing attests that they have reviewed engagement and found no substantive objection.
3. A post labeled **`[SYNTHESIS]`** — the refined proposal incorporating valid concerns from any antithesis. If `[NO_OBJECTIONS_LOGGED]` was used, the synthesis may be a verbatim restatement of the thesis, but the synthesis post is still required (it converts the thesis into a vote-ready proposal).

A thread that does not satisfy all three structural elements cannot enter the VOTING phase. Forum tooling MUST refuse the transition. The check is structural (label presence and ordering) not semantic; semantic adequacy of the antithesis or synthesis is a community judgment, not a rule violation.

Sub-Leviathans may **extend** this rule (e.g., require a `[REVIEW]` post from a domain expert before synthesis) but may not weaken it. A weakening attempt is a divergent-fork act per `kernel/00-meta.md §4.5`.

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this rule operationalizes

The `dialectic` term defines the procedural shape of constitutional discussion. This rule turns that shape into an enforceable check on the forum sync pipeline and on the proposal advancement logic. Without this rule, the `dialectic` term is a description; with it, the term becomes a gate.

## Lineage

Ported 2026-05-15 from the original DAHAO test-1 prototype (`@rule_dialectic_format` v1.0.0, 2024-12-13). The original logic ("Discussion MUST include thesis AND (antithesis OR explicit_no_objections) AND synthesis") is preserved. Adaptations:

- "GitHub Discussions" → "federation forum board"
- `explicit_no_objections` formalized as `[NO_OBJECTIONS_LOGGED]` label, with a standing threshold (`guardian`) attached
- Structural-not-semantic clarification added (was implicit in the original)
- Extension-but-not-weakening clause added (Sub-Leviathan inheritance discipline)

## Why labels, not free text

The labels (`[THESIS]`, `[ANTITHESIS]`, `[SYNTHESIS]`, `[NO_OBJECTIONS_LOGGED]`) make the structure machine-readable. The forum sync pipeline and the proposal-advancement logic both consume them. A free-text rule ("the thread should include thesis, antithesis, and synthesis posts") would push interpretation onto the moderator, which is exactly the kind of constitutional drift this rule exists to prevent.

## Why the standing threshold on `[NO_OBJECTIONS_LOGGED]`

Without a standing requirement, any participant could short-circuit dialectic by posting `[NO_OBJECTIONS_LOGGED]` minutes after the 7-day mark, regardless of whether they had actually reviewed engagement. `guardian` standing is earned through demonstrated board moderation history, so the attestation has a witness behind it (compare: `witness_principle`).

## Worked example — a malformed thread

A `companion` participant proposes adding a new shadow element. Thread sequence:

- Day 0: `[THESIS]` post.
- Day 3: `[SYNTHESIS]` post (proposer, jumping ahead).
- Day 4: Proposer requests transition to VOTING.

The transition is refused. Reason: no `[ANTITHESIS]` and no `[NO_OBJECTIONS_LOGGED]`. The 7-day window has not even elapsed; even with patience, an antithesis or a moderator's no-objections log must appear. The proposer may re-engage the community for antithesis, or wait the full 7-day window and request a moderator's `[NO_OBJECTIONS_LOGGED]`.

## Worked example — well-formed thread under attack

A `medicine` proposal triggers a participant to flood the thread with low-quality `[ANTITHESIS]` posts in an attempt to bog down dialectic. The rule still passes structurally — there is an antithesis. But moderators may invoke a `protocols/` (future, Phase 2) anti-flood circuit-breaker to mark the disruptive antitheses as withdrawn; the rule remains satisfied if at least one substantive antithesis survives. Substantive-ness is a community judgment; this rule does not adjudicate it.

## Relation to other elements

- **`dialectic`** (TERM, LOCKED) — the term this rule operationalizes.
- **`proposal`** (TERM, LOCKED) — the rule applies to threads in proposal DISCUSSION phase.
- **`witness_principle`** (PRINCIPLE, IMMUTABLE) — the `[NO_OBJECTIONS_LOGGED]` mechanic is a witness act, not an assumption.
- **`standing`** (TERM, MUTABLE) — `guardian` threshold for no-objections-logged attestation.
- **`rule_proposal_process`** (RULE, LOCKED) — references this rule as the DISCUSSION phase gate.

## Sub-Leviathan extension examples

- **Medicine** may extend: require a `[CLINICAL_REVIEW]` post from a participant holding `clinical_reviewer` domain credential before `[SYNTHESIS]`.
- **Animal Welfare** may extend: require a `[PRECAUTIONARY_CHECK]` log when the proposal removes any species protection.

These extensions are added in the Sub-Leviathan's own `rules/dialectic-format.md` and inherit-merge with the federation rule at sync time. The pattern is: meta sets the floor, domains add the ceiling.

## Open question for Phase 2

- **Multi-round dialectic** — currently a single thesis-antithesis-synthesis cycle. Some proposals genuinely need a second round (synthesis fails to satisfy a substantive antithesis, new synthesis required). Currently handled informally by community re-discussion; Phase 2 candidate for explicit round numbering.
