---
slug: rule_proposal_process
element_type: RULE
mutability: LOCKED
inline: false
current_version: 1
contentURI: null
inherited_by: [medicine, scream, animal-welfare, companion]
implements_principles: [user_sovereignty, witness_principle]
uses_terms: [proposal, dialectic, evidence, standing]
---

Every amendment to any constitutional element in any Leviathan instance MUST follow the lifecycle defined in the `proposal` term:

```
DRAFT → DISCUSSION → VOTING → ACCEPTED | REJECTED | WITHDRAWN
```

Each transition is gated:

| Transition | Gate | Failure mode |
|---|---|---|
| (new) → **DRAFT** | Proposer holds at least `sentinel` standing; required fields present (target, current_version, proposed_version, justification, evidence) | Submission rejected |
| **DRAFT → DISCUSSION** | `rule_evidence_required` satisfied (or exemption verified by `guardian`); proposer requests transition | DRAFT-BLOCKED until satisfied |
| **DISCUSSION → VOTING** | `rule_dialectic_format` satisfied (thesis + antithesis-or-no-objections-logged + synthesis present, in order, minimum 7 days elapsed) | Transition refused by forum tooling |
| **VOTING → ACCEPTED \| REJECTED** | Voting thresholds and quorum per Phase 2 amendment (`rule_consensus_threshold`, `rule_quorum_requirement`); recorded on-chain | Default to REJECTED on quorum failure |
| **DRAFT \| DISCUSSION → WITHDRAWN** | Proposer initiates, OR a `guardian` initiates with cause (e.g., proposer inactive 30+ days) | — |

A proposal cannot skip phases. A proposal cannot return to an earlier phase except via WITHDRAWN (which terminates the proposal; the proposer may submit a fresh proposal as a new DRAFT).

Proposal title format (required for sync pipeline parsing):
```
[PROPOSAL] {action} @{target_slug} (v{current_version} → v{proposed_version})
```
Where `action ∈ {add, modify, remove, deprecate, restore}`.

This rule is itself constitutional: amending it requires its own application (a proposal targeting `rule_proposal_process` follows the lifecycle defined by `rule_proposal_process`). This self-reference is intentional — it is the procedural counterpart to the kernel's self-referential consistency requirement (`kernel/00-meta.md §6`).

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this rule operationalizes

The `proposal` term defines the lifecycle states. This rule defines the **transition gates** between them. Without this rule, the lifecycle is a description of states; with it, the lifecycle becomes a sequence of enforceable checkpoints with explicit failure modes.

## Why self-application matters

A rule that defines the amendment procedure but is itself exempt from that procedure is unfalsifiable in the constitutional sense — it could be changed by edict, undermining every other amendment that obeys it. The self-reference clause closes this loop: changing how amendments work requires going through the amendment process itself. This is the procedural form of the witness principle (the protocol witnesses its own changes through its own procedure).

## Lineage

Ported 2026-05-15 from the original DAHAO test-1 prototype (`@rule_proposal_process` v1.0.0, 2024-12-13). The DISCUSSION → VOTING → DECISION lifecycle is preserved. Adaptations:

- DRAFT phase made explicit (prototype implicitly assumed DRAFT was just a pre-DISCUSSION state)
- WITHDRAWN added as an explicit terminal state from DRAFT or DISCUSSION (prototype had no withdrawal mechanism)
- Each transition gated with explicit failure mode (prototype had freeform "requirements" lists)
- Standing requirement added at submission (prototype had no standing concept)
- Self-application clause added (prototype was silent on self-amendment)
- Title format formalized with `action` enum (prototype had freeform action)

## Why thresholds and quorum are deferred to Phase 2

This rule defines the **shape** of the lifecycle. The **numbers** that determine VOTING outcomes — what fraction of votes constitutes acceptance, what fraction of standing-weighted participation constitutes quorum, what ratchet applies when a proposal removes protection — are the next layer down and deserve their own focused dialectic. Porting them in this same trio would conflate "how do we change things" with "by how much agreement do we change them," and those are separable questions.

The placeholder in the gate table (`per Phase 2 amendment`) is honest: a proposal in 2026-05 cannot reach VOTING in any Sub-Leviathan until Phase 2 settles thresholds. Until then, ACCEPTED requires an explicit `guardian` ratification entry — a stop-gap, not a final mechanism.

## Worked example — a complete Medicine proposal lifecycle

A `medicine` participant (Dr. X, holds `sentinel` standing) wants to add `@informed_consent_architecture` as a new RULE.

1. **Submission.** Dr. X drafts the rule file; opens a thread in `/forum/medicine` with the required title format. Cites three sources (Tier A meta-analysis, Tier B WHO report, Tier C expert commentary). The DRAFT post is visible.
2. **DRAFT → DISCUSSION.** `rule_evidence_required` check passes (Tier A source exceeds Medicine override). Dr. X requests transition; forum tooling permits.
3. **DISCUSSION.** Day 0: `[THESIS]`. Day 2: `[ANTITHESIS]` from another participant questioning the time-bound clause. Day 4: `[ANTITHESIS]` from a third participant questioning the no-bundling clause. Day 6: Dr. X posts `[SYNTHESIS]` clarifying time-bound mechanics and adding a worked example for no-bundling. Day 7: `rule_dialectic_format` check passes; minimum elapsed.
4. **DISCUSSION → VOTING.** Dr. X requests transition; permitted.
5. **VOTING.** Per Phase 2 (when settled), votes counted. Until Phase 2, a `guardian` ratification entry is required; one `guardian` for Medicine attests acceptance.
6. **ACCEPTED.** On-chain ratification call writes `@informed_consent_architecture` v1 to the registry; `current_version` updates from 0 to 1 in the Medicine repo.

Total elapsed time: ~7-10 days.

## Worked example — a WITHDRAWN proposal

Same participant, different proposal. After `[THESIS]` posted, Dr. X realizes the proposal targets the wrong element slug. Dr. X posts `[WITHDRAWN]` with a brief explanation. Forum tooling closes the thread; the proposal is recorded as WITHDRAWN with the explanation as terminal comment. Dr. X immediately opens a new DRAFT with the corrected slug. The withdrawn record is permanent (witness principle: the federation remembers).

## Relation to other elements

- **`proposal`** (TERM, LOCKED) — defines the lifecycle states this rule gates.
- **`dialectic`** (TERM, LOCKED) — referenced via `rule_dialectic_format`.
- **`evidence`** (TERM, LOCKED) — referenced via `rule_evidence_required`.
- **`standing`** (TERM, MUTABLE) — `sentinel` for proposers; `guardian` for exemption verification and stop-gap ratification.
- **`user_sovereignty`** (PRINCIPLE, IMMUTABLE) — the lifecycle ensures users (participants) author and ratify their own constitutional changes; no edict.
- **`witness_principle`** (PRINCIPLE, IMMUTABLE) — every transition is recorded; failed transitions are not hidden, they are visible DRAFT-BLOCKED or REJECTED records.
- **`enactment`** (TERM, MUTABLE) — ACCEPTED proposals are enactment-bearing events for proposer and synthesis author.
- **`rule_dialectic_format`** (RULE, LOCKED) — companion rule; this rule references it.
- **`rule_evidence_required`** (RULE, MUTABLE) — companion rule; this rule references it.

## Sub-Leviathan override pattern

A Sub-Leviathan cannot bypass this rule (the lifecycle is mandatory federation-wide) but may **tighten** it in its own `constitution/rules/proposal-process.md`:

- Require higher standing for proposers (Medicine may require `guardian` for clinical rule changes).
- Add an extra phase before VOTING (Animal Welfare may insert a `PRECAUTIONARY_REVIEW` phase for proposals removing species protection).
- Require longer DISCUSSION minimums for IMMUTABLE-tier amendments.

Any tightening is permitted; loosening is a divergent-fork act.

## Open questions for Phase 2

- **Thresholds and quorum** — the largest unfinished piece. Without numbers, VOTING is stuck behind a `guardian` stop-gap that is not the long-term mechanism.
- **Cross-Sub-Leviathan proposals** — when a proposal in `medicine` modifies an element inherited from meta, how is concurrence from meta governance recorded? Currently TBD.
- **Emergency amendments** — bypass mechanism for proposals during active attack on the federation (e.g., a vulnerability in `witness_principle` interpretation that is being exploited). Currently no such mechanism; Phase 2 candidate for circuit-breaker protocol.
- **Hash-anchoring of intermediate states** — every transition (DRAFT → DISCUSSION → VOTING) is currently a forum thread state, not an on-chain anchor. The accepted proposal anchors on-chain; the intermediate states do not. Open for Phase 2 whether to anchor the synthesis hash.
