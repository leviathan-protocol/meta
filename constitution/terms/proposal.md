---
slug: proposal
element_type: TERM
mutability: LOCKED
inline: false
current_version: 1
contentURI: null
inherited_by: [medicine, scream, animal-welfare, companion]
---

A formal request to modify a constitutional element (term, principle, rule, shadow, protocol) in any Leviathan instance. Every proposal carries five required fields:

- **target** — the slug of the element being changed, or a new slug if adding.
- **current_version** — integer version of the target at submission time. For new elements: `0`.
- **proposed_version** — integer version after ratification. Must increment per `rule_version_bump` (Phase 2).
- **justification** — the rationale: why this change serves the instance's purpose.
- **evidence** — at least one source per the `evidence` term and `rule_evidence_required`.

Proposal lifecycle (linear, no skipping, no return-to-earlier-state except WITHDRAWN):

```
DRAFT → DISCUSSION → VOTING → ACCEPTED | REJECTED | WITHDRAWN
```

- **DRAFT** — authored and visible in the forum; evidence attached; awaiting transition to DISCUSSION.
- **DISCUSSION** — open for `rule_dialectic_format` to apply; minimum 7 days; thesis/antithesis/synthesis recorded.
- **VOTING** — opens only after synthesis posted; thresholds and quorum per Phase 2 amendment.
- **ACCEPTED** — ratified to the on-chain `ConstitutionalRegistry`; element's `current_version` updated.
- **REJECTED** — vote failed; proposal closed with permanent record; new proposal may re-attempt.
- **WITHDRAWN** — proposer (or successor with `guardian` standing) closes the proposal at any pre-VOTING stage.

Proposer must hold at least **`sentinel`** standing (see `terms/standing`). Proposal title format: `[PROPOSAL] {action} @{target_slug} (v{current_version} → v{proposed_version})`.

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this term defines

The unit of constitutional change. A proposal is the smallest atomic legal act in the federation: it names what is changing, from which version to which version, why, and on what evidence. Outside of a proposal, no constitutional content moves.

## Lineage

Ported 2026-05-15 from the original DAHAO test-1 prototype (`@proposal` v1.0.0, 2024-12-13). The five required fields and the lifecycle states are preserved verbatim. Adaptations: standing requirement added (DAHAO test-1 had no standing concept); title format formalized; explicit "no skipping" lifecycle constraint added.

## Why "no skipping"

DRAFT → VOTING without DISCUSSION would bypass dialectic. DISCUSSION → ACCEPTED without VOTING would bypass democratic ratification. Both are constitutional violations. The lifecycle is a one-way pipeline because each phase produces an output that the next phase consumes: DRAFT produces a proposal record; DISCUSSION produces a synthesis; VOTING produces a tally; DECISION (ACCEPTED/REJECTED) produces an on-chain ratification or a closed record.

## Why standing matters at the proposal level

A proposal is a load-bearing constitutional act: it triggers community attention, dialectic effort, eventual vote-counting. Without a minimum standing requirement, the proposal channel becomes a DoS vector. `sentinel` standing is earned through enactment accumulation (see `terms/enactment`), which means a proposer has demonstrated participation before they can demand the community's attention. Higher-standing requirements may be set by Sub-Leviathans for proposals modifying their IMMUTABLE elements.

## Title format rationale

The title format is machine-parseable for the forum sync pipeline and for off-chain tooling (proposal trackers, validator dashboards). The format `[PROPOSAL] {action} @{target_slug} (v{current_version} → v{proposed_version})` lets any reader, human or agent, identify:

- That this is a proposal (not a discussion-only thread)
- The intended action (add, modify, remove, deprecate)
- The element slug being targeted
- The exact version transition

Example: `[PROPOSAL] modify @evidence (v1 → v2)`.

## Relation to other elements

- **`dialectic`** (TERM, LOCKED) — DISCUSSION phase obeys dialectic format.
- **`evidence`** (TERM, LOCKED) — every proposal carries evidence per this term.
- **`standing`** (TERM, MUTABLE) — proposer standing threshold.
- **`enactment`** (TERM, MUTABLE) — accepted proposals are enactment-bearing events for the proposer and synthesis author.
- **`rule_proposal_process`** (RULE, LOCKED) — operationalizes this term as a lifecycle enforcement check.
- **`rule_dialectic_format`** (RULE, LOCKED) — applies during DISCUSSION.
- **`rule_evidence_required`** (RULE, MUTABLE) — gates DRAFT → DISCUSSION transition.

## Edge cases and open questions for Phase 2

- **Concurrent proposals on same element** — when two proposers target the same element at the same version, the second proposal moves to DRAFT-BLOCKED until the first reaches a terminal state. Currently informal; Phase 2 candidate.
- **Cross-Sub-Leviathan proposals** — a proposal that touches an element inherited from meta requires concurrence from the meta governance; mechanism TBD in Phase 2.
- **Proposal hash-anchoring** — the proposal record is itself a constitutional event and should be hash-anchored to the registry, not just its accepted outcome. Open for Phase 2.
- **Voting thresholds** — deliberately omitted from this term and from `rule_proposal_process`. Each Sub-Leviathan defines thresholds for its own element types in Phase 2's `rule_consensus_threshold`.
