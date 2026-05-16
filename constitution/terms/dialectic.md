---
slug: dialectic
element_type: TERM
mutability: LOCKED
inline: false
current_version: 1
contentURI: null
inherited_by: [medicine, scream, animal-welfare, companion]
---

A structured discussion process to refine proposals through collaborative reasoning. A dialectic proceeds through three phases:

1. **Thesis** — the original proposal, with evidence and justification. Authored by the proposer.
2. **Antithesis** — counter-arguments, concerns, questions, and alternative views. Authored by the community. If, after the minimum 7-day discussion window, no substantive antithesis is raised, a moderator may log an explicit `no_objections_logged` entry in place of an antithesis post; silence alone is never a substitute.
3. **Synthesis** — a refined proposal that incorporates valid concerns from the antithesis. Authored by the original proposer or any other participant. The synthesis must address every substantive antithesis before the proposal can advance to VOTING.

Minimum total dialectic duration: **7 days**. Dialectic happens in the federation forum board for the relevant Sub-Leviathan. No off-platform conversation, private channel, or external decision counts as constitutional dialectic. The thread is the record.

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this term defines

The federation's epistemic procedure for changing constitutional content. Borrowed from Hegelian dialectic but stripped of metaphysical baggage — here it is a **procedural standard**: a discussion is only constitutional if it has been shaped by the friction of competing positions and a recorded attempt at reconciliation.

## Lineage

Ported 2026-05-15 from the original DAHAO test-1 prototype (`@dialectic` v1.0.0, 2024-12-13). Adapted to Leviathan vocabulary: "GitHub Discussions" replaced with "federation forum board"; "contributor" replaced with "participant"; explicit no-objections-logged mechanic clarified as moderator action, not implicit.

## Why "explicit no_objections_logged" exists

Silence is not consent. If a thesis sits for 7 days with no antithesis, the question is not "was the proposal good?" but "did the community see it?" The `no_objections_logged` entry is a positive witness act by a moderator: I read this, I checked engagement, I confirm no substantive objection was raised. This converts absence-of-objection from an assumption into a recorded fact. Compare: the Witness Principle.

## Relation to other elements

- **`witness_principle`** (PRINCIPLE, IMMUTABLE) — antithesis is the witness role: it documents counter-evidence, it does not accuse.
- **`proposal`** (TERM, LOCKED) — dialectic is the DISCUSSION phase of the proposal lifecycle.
- **`evidence`** (TERM, LOCKED) — thesis requires evidence; antithesis often takes the form of counter-evidence.
- **`rule_dialectic_format`** (RULE, LOCKED) — operationalizes this term as a forum-thread enforcement check.

## Worked example — Sub-Leviathan amendment

A `medicine` participant proposes raising the minimum evidence tier for sentience claims from B to A.

- **[THESIS]** post in `/forum/medicine` thread: "Raise sentience-claim minimum from B to A. Justification: aggregating institutional reports (B) often launders methodologically weak claims. Evidence: [cites two meta-analyses showing tier-B aggregation drift]."
- **[ANTITHESIS]** post: "Tier-A studies for marginal-sentience species are rare. This rule would freeze the species directory at current entries. Counter-evidence: [survey of available literature for cephalopods, decapods]."
- **[SYNTHESIS]** post: "Adopt A as default minimum, with named exception for species whose tier-A literature does not yet exist; those entries flagged for revision when published. Adds `evidence_tier_exception` field to species profile."

Without the synthesis, no vote.

## Edge cases the rule does not yet cover (open for Phase 2)

- **Hostile antithesis** (off-topic, vexatious): handled by moderator standing, not constitutional rule.
- **Emergency amendments** under attack: see `protocols/` (future) for circuit-breaker pattern.
- **Sub-Leviathan that wants a longer minimum** (e.g., Medicine = 14 days): permissible via override rule in their domain `rules/dialectic-format.md`. Federation minimum is a floor.
