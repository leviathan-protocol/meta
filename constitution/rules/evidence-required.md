---
slug: rule_evidence_required
element_type: RULE
mutability: MUTABLE
inline: false
current_version: 1
contentURI: null
inherited_by: [medicine, scream, animal-welfare, companion]
implements_principles: []
uses_terms: [evidence, proposal]
---

A proposal that modifies any factual claim MUST include at least one evidence source meeting the federation-wide minimum tier: **Tier C or higher**, as defined in the `evidence` term.

Each evidence source MUST be cited in the canonical format:
```
[Author (Year)] Title. Source. URL/DOI
```
The URL or DOI MUST resolve at the time of submission. The forum sync pipeline checks resolvability; an unresolvable citation marks the proposal as DRAFT-BLOCKED until corrected.

**Exemptions** — the following proposal types are exempt from the evidence requirement:
- Typographical corrections
- Formatting changes
- Clarifications that introduce no new factual claim
- Slug-renaming proposals where the slug is unambiguously broken (e.g., contains forbidden characters)

A proposer claims an exemption by including the line `evidence_exempt: <reason>` in the proposal frontmatter; a moderator with `guardian` standing verifies the exemption claim during the DRAFT phase. A disputed exemption claim is treated as ungranted, and the proposal requires evidence.

Sub-Leviathans may **raise** the minimum tier in their own `rules/evidence-required.md` for some or all element types. Sub-Leviathans may not **lower** the federation floor below Tier C.

A proposal that fails this check cannot transition from DRAFT to DISCUSSION.

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this rule operationalizes

The `evidence` term defines what counts as evidence and how it is tiered. This rule turns that taxonomy into a submission-gate check: no proposal advances to discussion without it.

## Why this rule is MUTABLE (not LOCKED)

The minimum-tier floor (Tier C) and the citation format are operationally important but are likely to evolve as the federation matures. As Sub-Leviathans accumulate experience with their domain's evidence ecosystem, the federation may want to raise the floor to Tier B (institutional minimum), or adopt a different citation format (e.g., structured JSON-LD evidence records readable by agents). Keeping this rule at MUTABLE allows that evolution under regular vote rather than the higher bar required for LOCKED amendments.

By contrast, `rule_dialectic_format` is LOCKED because the structural shape of dialectic is constitutive of the federation's epistemology — changing it changes what kind of polity Leviathan is. The evidence-required rule is enforcement of an underlying principle (evidence-based reasoning, expressed in the `evidence` term), and enforcement mechanisms are expected to tighten or loosen with experience.

## Lineage

Ported 2026-05-15 from the original DAHAO test-1 prototype (`@rule_evidence_required` v1.0.0, 2024-12-13). Original logic preserved. Adaptations:

- DRAFT-BLOCKED state added (was implicit; sync pipeline needs an explicit state)
- Resolvability check added (URLs that 404 at submission time were accepted by the prototype)
- `evidence_exempt: <reason>` claim mechanic formalized (was undocumented in prototype)
- Sub-Leviathan override-but-not-weaken clause added

## Why exemptions exist (and why they are tightly scoped)

If every typo fix required citing a dictionary, the proposal channel would clog with ceremonial evidence. Exemptions exist because the rule's purpose is to anchor factual claims, and typo fixes make no factual claim. The exemption list is deliberately short and the verification is moderator-gated, so the exemption channel cannot become a back-door for skipping evidence on actual factual changes.

## URL resolvability — why a runtime check matters

Citation rot is the largest silent failure mode of evidence-based discussion. A 2024 DAHAO test-1 thread cited a paper at a now-dead URL; the rule passed at submission, the evidence has since become un-checkable, and the synthesis stands on unverifiable ground. The resolvability check at submission time prevents new instances of this failure, though it does nothing about pre-existing decay (the evidence-staleness flag in Phase 2 will address that).

## Worked example — Medicine proposal under stricter override

The Medicine Sub-Leviathan's `rules/evidence-required.md` overrides the federation floor as follows:
- Clinical outcome claims: minimum Tier B.
- Safety claims affecting routine practice: minimum Tier A.
- All other claims: federation default (Tier C).

A `medicine` proposal modifies the `@algorithmic_fairness` rule to require pre-deployment audit reports. The justification cites:
- One IEEE institutional report on algorithmic audit methodology (Tier B) ✓
- One personal blog post by an audit consultant (Tier D) ✗ (below floor)

Federation floor is met (the IEEE report is Tier B, above Tier C). Medicine override does not apply (this is a procedural rule change, not a clinical outcome or safety claim). Proposal advances to DISCUSSION.

If the same proposal were to claim "audit-deployment reduces patient harm by 40%" — that is a safety claim, Medicine override requires Tier A, and the IEEE report (Tier B) is insufficient. The proposal would be DRAFT-BLOCKED until a Tier-A source is added.

## Relation to other elements

- **`evidence`** (TERM, LOCKED) — defines the tier system this rule enforces.
- **`proposal`** (TERM, LOCKED) — the rule applies to every proposal carrying a factual claim.
- **`standing`** (TERM, MUTABLE) — `guardian` standing required for exemption verification.
- **`rule_proposal_process`** (RULE, LOCKED) — references this rule as the DRAFT → DISCUSSION gate.
- **`rule_dialectic_format`** (RULE, LOCKED) — sibling rule; both gate the DRAFT → DISCUSSION transition (dialectic-format gates DISCUSSION → VOTING).

## Sub-Leviathan override pattern

A Sub-Leviathan that wants to tighten the rule writes its own `constitution/rules/evidence-required.md` with the same slug. At sync time, the federation rule and the Sub-Leviathan rule are merged: the Sub-Leviathan's stricter clauses apply within its board; the federation floor still applies everywhere.

A Sub-Leviathan that does NOT write its own `rules/evidence-required.md` inherits the federation rule unchanged.

## Open questions for Phase 2

- **Evidence staleness** — accepted proposals whose evidence URLs later die. Should the proposal be flagged? Re-validated periodically?
- **Conflict-of-interest tagging** — industry-funded peer review currently classified Tier A; some Sub-Leviathans may want a structured COI flag rather than tier adjustment. Phase 2 candidate.
- **AI-generated evidence** — what tier is a synthesis report produced by an LLM that summarizes 200 papers? Currently treated as Tier D (no human peer review of the synthesis); open for review.
