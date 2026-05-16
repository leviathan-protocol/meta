---
slug: evidence
element_type: TERM
mutability: LOCKED
inline: false
current_version: 1
contentURI: null
inherited_by: [medicine, scream, animal-welfare, companion]
---

Documentation supporting any factual claim in a proposal, antithesis, or synthesis. Evidence is classified into five quality tiers, each with an associated weight used by Sub-Leviathans when aggregating evidence in stratified reviews:

| Tier | Name          | Description                                                         | Weight |
|------|---------------|---------------------------------------------------------------------|--------|
| S    | Systematic    | Peer-reviewed meta-analysis or systematic review                    | 1.0    |
| A    | Academic      | Peer-reviewed primary research                                      | 0.8    |
| B    | Institutional | Reports from recognized institutions (WHO, FAO, IEEE, NIST, etc.)   | 0.6    |
| C    | Expert        | Expert opinion, grey literature, preprints                          | 0.4    |
| D    | Anecdotal     | Personal observation, unverified claim                              | 0.1    |

**Federation-wide minimum** for any proposal that modifies a factual claim: **at least one source at Tier C or higher**. Sub-Leviathans may declare a stricter minimum in their domain rules (Medicine, for example, may require Tier A for sentience claims). Sub-Leviathans may not lower this minimum below Tier C.

**Citation format** (required): `[Author (Year)] Title. Source. URL/DOI`. The URL or DOI must resolve at the time of submission; broken links discovered later trigger an evidence-staleness flag (handled per Phase 2 amendment).

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this term defines

The federation's standard for what counts as supporting evidence in any constitutional discussion. It is deliberately broad (Tier D is admissible, just weighted near zero) and deliberately ranked (the weight column is intended to be used, not merely contemplated). The point is not to exclude weak evidence but to make its weakness visible and accountable.

## Lineage

Ported 2026-05-15 from the original DAHAO test-1 prototype (`@evidence` v1.0.0, 2024-12-13). The five-tier scaffold and the weight values are preserved verbatim from that prototype; the only adaptations are vocabulary (DAHAO → Leviathan) and the explicit floor clause ("Sub-Leviathans may not lower this minimum below Tier C").

## Why five tiers and not three

The temptation to collapse to "good / okay / bad" loses signal. Tier B (institutional) and Tier C (expert opinion) behave differently in adversarial review: an institutional report can be cited as if it were peer-reviewed primary research, which it is not. Keeping them separate prevents this category drift. Tier S (systematic review) is separated from Tier A because meta-analyses can aggregate underpowered studies into apparent significance; treating them as equivalent to a single peer-reviewed study would understate the difference.

## Why weights, and where they are used

The weight column is not for blocking proposals — that is what the minimum-tier check does. Weights are for **stratified review**, primarily in Sub-Leviathans whose domain involves quantitative aggregation (Medicine, Animal Welfare). Example: an Animal Welfare claim that a practice causes suffering, supported by two Tier-D personal accounts and one Tier-B institutional report, has aggregate weight `0.1 + 0.1 + 0.6 = 0.8` — equivalent in weight to one Tier-A peer-reviewed paper, not three independent sources of equivalent strength. The weight column lets Sub-Leviathan rules make this distinction explicit.

## Sub-Leviathan override pattern

Each Sub-Leviathan may define a `rules/evidence-required.md` that **raises** the minimum tier for its domain. Examples:

- **Medicine** — minimum Tier B for any clinical-outcome claim; minimum Tier A for safety claims that affect routine practice.
- **Scream** — minimum Tier B for institutional-failure claims (because anecdotal failure-reporting is the standard signal in this domain, but moving to amendment requires harder evidence).
- **Animal Welfare** — minimum Tier B for sentience claims (because the precautionary principle already covers Tier C in the absence of contradicting evidence).

A Sub-Leviathan cannot **lower** the federation floor below Tier C.

## Relation to other elements

- **`proposal`** (TERM, LOCKED) — every proposal must carry evidence per this tier system.
- **`dialectic`** (TERM, LOCKED) — antithesis posts often consist of counter-evidence; the same tier system applies.
- **`rule_evidence_required`** (RULE, MUTABLE) — operationalizes this term as a submission-gate check.
- **`witness_principle`** (PRINCIPLE, IMMUTABLE) — evidence is the substrate of witnessing; without it the protocol cannot record, only assert.

## Edge cases and open questions for Phase 2

- **Evidence freshness** — when does a Tier-A study become obsolete? Currently no time-based decay. Phase 2 candidate.
- **Conflicting evidence at same tier** — handled by dialectic (antithesis is the proper venue), not by tier arithmetic.
- **Industry-funded peer review** — currently classified Tier A. Sub-Leviathans whose domain has a known conflict-of-interest problem (Medicine pharmaceuticals, Animal Welfare agribusiness) may add a Tier-A-modifier in their domain rules. Phase 2 candidate for kernel-level promotion.
