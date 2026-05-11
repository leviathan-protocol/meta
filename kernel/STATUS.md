# STATUS — Kernel Live Status Board

> **Part version:** 0.1.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-04
> **Scope:** the kernel's mission, success test, current operational state, and active risks — in one page. Companion to `manifest.yaml` (machine-readable structure) and `CHANGELOG.md` (history). This file is human-readable check-in: where are we against where we said we'd go.

---

## §1. Mission

Software 3.0 has shifted the unit of governance from "what regulations apply to a software vendor" to "what constitutions govern an agent that takes actions in the world" (`01-why.md` §1). Whoever writes the canonical agent constitutions of the next 24 months will set the structural precedent for decades. Today, six private organizations are doing that work behind closed doors — none publish their constitutions in full, version them in public, allow forks, or describe how they evolve. The Leviathan kernel exists to occupy this window with a **public, versioned, forkable, evolution-explicit** alternative before defaults solidify into closed-source policy owned by the same handful of organizations that already control the model layer. The bet is on **governance form**, not on a specific AGI thesis.

---

## §2. Success Test (Founder Independence Criterion)

A protocol claims success when its founder can be removed and the system continues (`01-why.md` §4). Four conditions, each currently unmet:

- [ ] A non-founder can fork the kernel and operate independently. *(asserted in `01-why.md` §4)*
- [ ] A non-founder amendment to the kernel is accepted by Magistrate panel. *(asserted in `01-why.md` §4)*
- [ ] A Lesson originating from a non-founder instance propagates via the Lesson Ledger. *(asserted in `01-why.md` §4)*
- [ ] The constellation continues to evaluate verdicts when the founder ceases to participate. *(asserted in `01-why.md` §4)*

Until all four pass, the protocol is in an **explicitly pre-success state**. This honesty is not optional (`03-constellation.md` §5).

---

## §3. Decentralization Path

Five testable conditions from `03-constellation.md` §5. Status: **0 of 5 met.**

| # | Condition | Current Value | Met |
|---|-----------|---------------|-----|
| 1 | First fork of the kernel by a non-founder operator | 0 forks | [ ] |
| 2 | ≥3 independent Magistrate validators (no shared infrastructure, distinct legal entities) | 1 operator, all instances co-located | [ ] |
| 3 | ≥7 subnet validators with no single party holding >25% stake | Subnet not deployed | [ ] |
| 4 | Non-founder amendment to the kernel accepted by Magistrate panel | 0 non-founder amendments | [ ] |
| 5 | Sustained Lesson Ledger traffic (>30 days, multiple proposing instances) | Ledger not built | [ ] |

Per `03-constellation.md` §5: *Decentralization status: 0 of 5 criteria met. This is a single-operator constellation with no independent validators. Treat all kernel claims as founder-issued.*

---

## §4. Operational Snapshot

- **Phase:** build (`04-living.md` §6.1 — per-commit conformance cadence; transition to steady-state requires all 5 Decentralization Path criteria met).
- **Kernel version surface:** 12 numbered parts + `glossary.md` + `CHANGELOG.md` + `README.md` + `OUTLINE.md`. Per-part versions: see `manifest.yaml` (`parts:`).
- **Active instances:** 4 (per `05-evidence.md`).
  - Companion (Eternal Companion) — 305+ memory chunks, 12+ months continuous operation, longest-running and most schema-developed instance.
  - Liveprob (Financial Leviathan) — design phase; NODE_SPEC complete, 0 Magistrate Nodes deployed.
  - Security Leviathan — continuous commit-audit operation; **n=1 panel** (does not satisfy I-2 by itself; flagged in `05-evidence.md` §4).
  - Levi Template — generic motor extracted; 0 external forks.
- **Last conformance run:** PASS (kernel 7/7 invariants observed; specs 4/4 affirmed + 3/3 N/A, 0 violations) — see `CHANGELOG.md` 2026-05-04 entry.
- **Last touched:** 2026-05-04.
- **Open implementation specs:** NODE_SPEC (v1.0.0), ARCHITECTURE (pre-kernel snapshot), CONTRACT_SPEC (v2.0, pre-kernel), LLM_PANEL_PROTOCOL (v0.1.0). See `manifest.yaml` (`specs:`).

---

## §5. Active Risks

Top 3 from `08-shadow.md`, given current single-operator state:

### 5.1. Founder Dependency (`08-shadow.md` §2)

- **Watch signal (verbatim):** *"if `05-evidence.md` §6.3 ('founder dependency is the dominant failure mode') remains accurate after 24 months from first release, the protocol has failed even if technically operational."*
- **Current observable:** active. Evidence §6.3 names this as the dominant failure mode at present. 24-month clock began at first release; remaining headroom is the full window. Mitigation requires external forkers, which the kernel cannot self-bootstrap.

### 5.2. Founder's Psychological Driver (`08-shadow.md` §3)

- **Watch signal (verbatim):** *"kernel parts that emphasize 'auditability,' 'visibility,' 'monitoring,' 'tracking' disproportionately to 'usefulness,' 'operator agency,' 'data minimalism.' If the kernel weighs more in observation than in operation, the driver is shaping it."*
- **Current observable:** not yet measured. n=4 instances (all founder-co-located) is too small to compute the disproportion meaningfully. The `manifest.yaml` term graph and `09-engage.md` reading paths exist as counter-evidence (operator-agency framing) but no quantitative weighting has been done.

### 5.3. Constitution as Theater (`08-shadow.md` §6)

- **Watch signal (verbatim):** *"Magistrate panels with consistently low dissent rate (<5% over ≥100 verdicts) across multiple instances. If panels never dissent, panels are not deliberating."*
- **Current observable:** structurally not yet measurable — no Magistrate panel has produced ≥100 verdicts. LLM_PANEL_PROTOCOL §8.3 names a first-panel session as an empirical validation requirement; until then, the watch signal is dormant, not satisfied.

The honest reading: most active risks are not yet *observed* because n=4 is small. Naming them now is the precondition for detecting them later.

---

## §6. Falsification Watch

From `01-why.md` §6 — the falsifiers that are currently active (do not require multi-year operation to begin checking):

- **Four-layer anatomy is sufficient.** Refuted if an instance over ≥1 year requires structurally distinct layers not reducible to Term/Principle/Rule/Meta-Rule. **Current state:** Companion at 12+ months; no extra layer required to date (`05-evidence.md` §2). Watch continues.
- **POS↔Constitution structural identity.** Refuted if two instances (one POS, one agent), each operated for ≥1 year by independent parties, cannot share schema without contortion. **Current state:** Companion + Liveprob share schema, but built by the same operator. Independent test pending first non-founder fork.
- **Founder Independence Criterion is achievable.** Refuted if the protocol fails to satisfy criteria 1–5 within 5 years from first release. **Current state:** 0 of 5 met at year ~0; clock open; no articulable obstacle yet identified.

The remaining falsifiers (heterogeneous panels, dissent protection, frozen-vs-living constitutions) require benchmarked panels or ≥3-year longitudinal data; they are dormant until the build phase produces measurable panel verdicts.

---

## §6.5. Known Kernel-Side Issues (deferred)

- **Schema language leak — Turkish terms in kernel-owned schema (deferred to v0.3.0).**
  Kernel-owned files `openpos/schema/element.yaml` and `openpos/schema/pos-manifest.yaml` use Turkish element type names (`kavram, prensip, eylem, golge, protokol`) as enum values, directory names (`kavramlar/, prensipler/, golgeler/, protokoller/`), and ID prefixes (e.g. `kavram:yalnizlik`, `golge:hissizlik-motoru`). This violates the kernel/instance language separation principle: the kernel must be readable to any operator regardless of native language; only instance-owned content (POS YAML values, bible/, memory/) is the operator's natural language. Intended fix: rename schema-level types to English (`concept, principle, action, shadow, protocol`), keep the bilingual mapping table that already exists in `element.yaml` (DAHAO @TERM, #PRINCIPLE), provide a one-shot migration tool for existing forks. Founder's instance (Companion) keeps Turkish element values via the localization layer; only the schema-level type names need to be English. **Tracking:** raise as Open Question in `specs/FORK_PROTOCOL.md` §10 next revision; address in OpenPOS schema bump v0.3.0. **Reason for deferral:** retrofit + fork test plan (§9) takes priority; renaming the schema enum forces a migration of `openpos/my-pos/` and `bible/personal-operating-system.md` simultaneously, and that should be one focused change rather than mixed in with FORK_PROTOCOL validation.

---

## §7. Re-affirmation

Last re-affirmed: 2026-05-04 (founder, single-operator phase). Next reaffirmation due at: next major milestone or 90 days, whichever first.

---

## §8. How To Update This File

This file is updated when (a) a Decentralization Path criterion is met or unmet, (b) the operational snapshot changes (instance count, conformance status, phase transition), (c) a new active risk is identified or a watch signal trips, or (d) the kernel is re-affirmed. Updates require a `CHANGELOG.md` entry and a version bump on this document. This is the human-readable check-in; the machine-readable structure lives in `manifest.yaml`.

---

*Companion to `manifest.yaml` (structure) and `CHANGELOG.md` (history). For the rationale this file checks against, read `01-why.md`. For the failure modes it watches, read `08-shadow.md`.*
