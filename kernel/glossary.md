# glossary — Terms Layer of the Kernel

> **Part version:** 0.6.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-04
> **Scope:** every term that appears in the kernel with capitalized or specific meaning. This is the kernel's own Terms layer (in the four-layer sense of `02-anatomy.md` §2).

A reader who knows the terms can read any part out of order. A reader who does not will rediscover them part-by-part. This glossary makes the first reading possible.

Terms are listed alphabetically. Each entry: **definition · introduced in · version**. Where a term originates in Turkish-language work that predates the kernel, the Turkish form is preserved with English gloss.

---

## A

**Action time** — The moment at which an agent or operator commits to a primitive action with side effects. Constitutional evaluation occurs at action time, not at policy-write time. Distinct from regulatory frames that operate retrospectively. *Introduced: `02-anatomy.md` §6.1 · v0.1.0*

**Amendment Plan** — A filled-out copy of `templates/amendment-plan-template.md` that proposes a kernel-touching modification. Required input to a panel session for any change to kernel-owned files. Contains a mandatory `## §3. Invariant Impact Check` table marking each of `I-1`…`I-7` as `unchanged | strengthened | weakened`. A `weakened` row is a divergent-fork declaration per `00-meta.md` §4.5, not a normal kernel amendment. The plan is a forcing function (surfacing what the panel will need); only the panel approves. *Introduced: `templates/amendment-plan-template.md` · v0.6.0*

**Amendment Procedure** — The formal mechanism by which a kernel part is modified. Requires version bump, changelog entry, panel review for protected-tier changes, supermajority for immutable-constant additions. *Introduced: `00-meta.md` §4 · v0.1.0*

**Approved Model Registry** — Worked example of a tier-versioned mutable list. Catalogs LLM models eligible for Magistrate panel use. Maintained per-instance, optionally synchronized via Lesson Ledger. *Introduced: `04-living.md` §3 · v0.1.0*

---

## C

**Blind Evaluation** — Discipline by which panel members produce verdicts without seeing each other's work-in-progress. Implemented by file separation (`verdict-claude.md` and `verdict-codex.md` written before any merge file is opened). Defends `I-2` against single-source-of-influence collapse where heterogeneous panelists nonetheless converge on one panelist's framing. *Introduced: `specs/LLM_PANEL_PROTOCOL.md` §3 · v0.3.0*

**Build Phase** — The operational mode in which 0–4 of the 5 Decentralization Path criteria are met. Per-commit conformance cadence applies to kernel and specs (not instance content). Transitions to **Steady State** when all 5 criteria are met. *Introduced: `04-living.md` §6.1 · v0.2.0*

**Capture Window** — The 24-month period during which the form of agent constitutions is being decided. Closing window because once defaults solidify, alternatives become high-friction to introduce. *Introduced: `01-why.md` §1 · v0.1.0*

**Clarify Marker** — Inline marker `[CLARIFY: <question>]` written into kernel-owned files at the point where a question is open and a decision is deferred, rather than papering over the gap with a placeholder or silently leaving it undefined. The English form is canonical; only kernel-owned files (`kernel/`, `specs/`, `tools/`, `templates/`, and the kernel-owned subset of `openpos/`) are scanned by `tools/conformance.py --clarify-debt`. Instance-owned content (operator's POS, bible, memory, sessions) is operator-sovereign and may use any equivalent in the operator's language; the kernel does not enforce a marker convention there. The marker count is informational, not failing — a non-zero count is normal and tracked in `kernel/STATUS.md`. *Introduced: `specs/research/spec-kit-inspiration.md` §5.4, §8 Q4 · v0.5.0; templates/ scope added v0.6.0*

**Conformance Harness** — `tools/conformance.py`. Programmatic check that takes a kernel part, spec, or directory and verifies the 7 immutable invariants (`I-1`…`I-7`) are observable. Tier-aware: kernel must affirm and not violate; specs must not violate and must affirm a smaller required subset. Also supports `--fork` (fork conformance, three-state PASS/DIVERGENT/FAIL) and `--clarify-debt` (count of `[CLARIFY: ...]` markers in kernel-owned files). *Introduced: `tools/conformance.py` · v0.1.0*

**Companion** — Reference instance: a personal operating system (POS) instance for one human, operating since 2026-01 with prior context dating to 2024. Used as proof of POS↔Constitution structural identity. *Introduced: `02-anatomy.md` §2 · v0.1.0*

**Conformant Fork** — A fork that preserves all 7 immutable invariants (`I-1` through `I-7`). Retains the Leviathan name and constellation membership. Contrast with **Divergent Fork**. *Introduced: `03-constellation.md` §6 · v0.1.0*

**Constellation** — The federation of Leviathan instances that share the kernel, optionally subscribe to Sovereign Consoles, and optionally participate in the Lesson Ledger. Membership is voluntary. *Introduced: `03-constellation.md` §1 · v0.1.0*

---

## D

**Decay Mechanism** — The 90-day reaffirmation cadence by which kernel parts and instance constitutional elements lose authoritative status if untouched. Stale clauses cannot be cited as authoritative until reaffirmed. *Introduced: `04-living.md` §6 · v0.1.0*

**Decentralization Path** — The 5 named conditions under which the protocol claims operational decentralization: first non-founder fork, ≥3 independent validators, ≥7 subnet validators with no >25% stake, accepted non-founder kernel amendment, sustained Lesson Ledger traffic. Currently 0/5 met. *Introduced: `03-constellation.md` §5 · v0.1.0*

**Dictionary VM** — Component of the Mind reference runtime: catalog of constitution-approved primitive actions executed by deterministic binary executors. *Introduced: `06-mind.md` §3 · v0.1.0*

**Divergent Fork** — A fork that modifies an immutable invariant. Loses the right to use the Leviathan name; must rename. Permitted by `00-meta.md` §4.5; the fork-divergence path is the protocol's escape valve, not its violation. *Introduced: `00-meta.md` §4.5 · v0.1.0*

---

## F

**Falsification Condition** — A specific observation that, if made, refutes a claim of the kernel. Falsification conditions are stated in `01-why.md` §6 and `05-evidence.md` §8. *Introduced: `01-why.md` §6 · v0.1.0*

**Fork Manifest** — The `.fork-manifest.yaml` file at the root of every Leviathan-conformant fork. Records upstream provenance, fork type, instance metadata, and content hashes for kernel-owned files. Used by `tools/conformance.py --fork` to detect drift. *Introduced: `specs/FORK_PROTOCOL.md` §4 · v0.4.0*

**Founder Independence Criterion** — The operational test that the protocol claims success when its founder can be removed and the system continues. Five named conditions; precedent: Satoshi Nakamoto's removal from Bitcoin in 2010–2011. Currently unmet. *Introduced: `01-why.md` §4, `05-evidence.md` §8 · v0.1.0*

---

## I

**Immutable Invariant** — A clause in the kernel that cannot be changed by amendment without a divergent fork. Currently 7 such invariants (`I-1` through `I-7`). May be added but not removed. *Introduced: `00-meta.md` §7 · v0.1.0*

**Invariant Impact Check** — The mandatory `## §3` section of every Amendment Plan. Enumerates `I-1` through `I-7` in a table, each row marked `unchanged | strengthened | weakened` with rationale required for any non-`unchanged` row. A `weakened` row is, per `00-meta.md` §4.5, not a kernel amendment but a divergent-fork declaration; the check forces the proposer to identify which case they are in before the panel convenes. The structural prompt is borrowed from spec-kit's Constitution Check Gate; the operational shape (per-invariant row, weakening = divergence) is Leviathan-specific. *Introduced: `templates/amendment-plan-template.md` §3, `specs/research/spec-kit-inspiration.md` §5.1 · v0.6.0*

**Instance** — A concrete Leviathan in operation. Distinct from the kernel: instances inherit the kernel and add domain-specific constitutional content. Examples: Companion, Liveprob, Security Leviathan, Levi Template. *Introduced: `02-anatomy.md` §1, `03-constellation.md` §2 · v0.1.0*

**Instance Data Sovereignty** — `I-6`: an operator's instance data (conversations, POS contents, session logs) is not extractable by the kernel, the constellation, or any tokenomics mechanism. *Introduced: `00-meta.md` §7, `07-economy.md` §2.2 · v0.1.0*

---

## K

**Kernel** — The abstract protocol described in this document. Forkable, instance-agnostic. Distinct from any single instance. *Introduced: `00-meta.md` §1, `OUTLINE.md` Terminology · v0.1.0*

---

## L

**Lazy Node** — A Magistrate node detected as rubber-stamping rather than evaluating. Detected via pattern analysis (NODE_SPEC.md §8.2). Penalized via slashing. *Introduced: `07-economy.md` §3 · v0.1.0*

**Lesson** — A structural observation that has stabilized over time at one or more instances, recorded as a filled-out copy of `templates/lesson-template.md`. Distinguished from a one-off observation by reproducibility: another operator running the same instance under the same conditions would observe the same pattern. The lesson's `## §5. Kernel-relevance check` determines whether the lesson stays instance-local (typical) or promotes through the chain to an Amendment Plan. The Lesson is the upstream artifact of the lesson → propagate workflow chain; an unaccepted Lesson is not a kernel statement, only an instance record. *Introduced: `templates/lesson-template.md`, `specs/research/spec-kit-inspiration.md` §5.2 · v0.6.0*

**Lesson Ledger** — The optional cross-instance pattern transfer mechanism. Anonymized lessons proposed by one instance, reviewed by Magistrate panel, propagated to subscribing instances. Submission cost denominated in token (anti-spam). *Introduced: `03-constellation.md` §4 · v0.1.0*

**Leviathan** — The protocol's name. Hobbesian reference (a constructed sovereign). Use of the name requires conformance to the 7 immutable invariants. *Introduced: `00-meta.md` §1, `OUTLINE.md` Terminology · v0.1.0*

**LLM Panel Protocol** — The build-phase operationalization of the Magistrate Pattern using LLM CLIs (Claude Code, Codex CLI, optionally Gemini or local models) as heterogeneous reviewers. Tier-sized panels, blind evaluation, file-separated verdicts. Satisfies `I-2` for the build phase; does not satisfy Decentralization Path criterion 2 (which requires governance-stake separation, not just inference separation). *Introduced: `specs/LLM_PANEL_PROTOCOL.md` · v0.3.0*

**Liveprob** — Reference instance: a specialty trading agent constitution with primitive registry, irreversibility tagging, and Magistrate-pattern review for novel instruments. *Introduced: `02-anatomy.md` §2, `05-evidence.md` §3 · v0.1.0*

---

## M

**Magistrate** — Async reviewer/auditor in the Trinity. Multi-node, multi-model panel that evaluates non-routine actions. Heterogeneity required (`I-2`); dissent protected (`I-3`). *Introduced: `02-anatomy.md` §6.2 · v0.1.0*

**Magistrate Pattern** — The architectural pattern of N≥3 heterogeneous nodes, blind evaluation, dissent protection, slashing for lazy evaluation but never for honest dissent. Specified in NODE_SPEC.md. *Introduced: `02-anatomy.md` §6.2, `07-economy.md` §3 · v0.1.0*

**Meta-Rule** — The fourth layer of the constitutional substrate: rules about how rules change. The kernel's `00-meta.md` is the meta-rule layer for the kernel itself. *Introduced: `02-anatomy.md` §2.4 · v0.1.0*

**Mimar** — Turkish: "architect." Founder's POS-internal designation; appears in citations to the founder's personal operating system. Not a kernel-tier term; included here for cross-reference clarity. *Cross-reference: `08-shadow.md` §3 · v0.1.0*

**Mind** — Reference runtime implementation. LLM Orchestrator + Dictionary VM + Binary Executor + Voyager-style skill synthesis. Motto: *"Model thinks, VM does."* Marked as appendix-tier reference, not protocol-tier requirement. *Introduced: `06-mind.md` · v0.1.0*

**Mutable Tier** — Constitutional content that may be amended by routine instance procedure. Most clauses live here. *Introduced: `00-meta.md` §2, `04-living.md` §3 · v0.1.0*

---

## P

**Panel Tier Sizing** — The mapping from constitutional tier of a proposed change to required panel size: mutable changes require N=1 LLM (single CLI suffices); protected changes require N=2 LLM (Claude + Codex by default in build phase); immutable-invariant changes require N≥3 LLM with at least one model from a distinct provider family. Stated in `specs/LLM_PANEL_PROTOCOL.md` §2; defends `I-2` proportional to amendment risk. *Introduced: `specs/LLM_PANEL_PROTOCOL.md` §2 · v0.3.0*

**POS (Personal Operating System)** — A versioned constitutional substrate governing one human's choices. Structurally identical to an agent constitution under the kernel's claim (`01-why.md` §3). *Introduced: `01-why.md` §3 · v0.1.0*

**Pre-conformance Fork** — A fork that has been initialized (kernel-owned files copied, fork-manifest written) but whose instance-owned directories are not yet populated. Transient state expected to last only until the operator's first session. *Introduced: `specs/FORK_PROTOCOL.md` §3.3 · v0.4.0*

**Primitive** — A binary-executable action exposed by the Mind runtime to the LLM orchestrator. Each primitive is constitutionally tier-tagged (immutable / protected / mutable) and irreversibility-tagged. *Introduced: `06-mind.md` §3 · v0.1.0*

**Principle** — The second layer of the constitutional substrate. Directional commitments from which rules are derived. *Introduced: `02-anatomy.md` §2.2 · v0.1.0*

**Protected Tier** — Constitutional content that may be amended only via supermajority Magistrate panel. Includes most architectural commitments. *Introduced: `00-meta.md` §2 · v0.1.0*

---

## R

**Reasoning Artifact** — The document produced by every Sidecar verdict, Magistrate review, or Sovereign override. Required by `I-1`. Must be addressable, retrievable, and human-readable. *Introduced: `00-meta.md` §7 (`I-1`), `02-anatomy.md` §6 · v0.1.0*

**Rule** — The third layer of the constitutional substrate. Specific behavioral constraints derived from principles. *Introduced: `02-anatomy.md` §2.3 · v0.1.0*

---

## S

**Satoshi Mode** — The founder's POS principle (`#satoshi-mode v1.1`): "framework public, person private." Applied to the kernel: the protocol is public, the founder's specific identity is structurally minimized. *Introduced: `08-shadow.md` §7 (cited from POS) · v0.1.0*

**Security Leviathan** — Reference instance: local-LLM-based code-commit auditor for the founder's repositories. Currently single-node Magistrate (n=1) — flagged as gap against `I-2`. *Introduced: `05-evidence.md` §4 · v0.1.0*

**Sidecar** — Synchronous evaluator in the Trinity. Operates in the hot path: every primitive action is evaluated against the active rule set before execution. *Introduced: `02-anatomy.md` §6.1 · v0.1.0*

**Slashing** — Reduction of a validator's stake as penalty for constitutional violation at the Magistrate layer. Schedule specified in NODE_SPEC.md §10. Honest dissent never penalized. *Introduced: `07-economy.md` §3 · v0.1.0*

**Sovereign** — The named, addressable human(s) holding override authority for an instance. One per instance is the default; multi-Sovereign instances are permitted with documented decision procedure. *Introduced: `02-anatomy.md` §6.3 · v0.1.0*

**Sovereign Console** — Visibility primitive for cross-instance comparison. Code pattern, not deployment. Anyone may run a Console; no Console may claim canonical status. Currently planned, not built. *Introduced: `03-constellation.md` §3, §3.5 · v0.2.0*

**Steady State** — The operational mode reached when all 5 Decentralization Path criteria are met. Per-commit conformance cadence relaxes to 90-day reaffirmation. Default cadence for instance-level elements regardless of constellation phase. *Introduced: `04-living.md` §6.2 · v0.2.0*

**Sub-Constitution Superset Rule** — The Liskov-substitution analog for constitutions. Specialty agent constitutions inherit and extend their parent constitution; they may add constraints but never weaken inherited ones. Runtime-enforced. *Introduced: `02-anatomy.md` §3 · v0.1.0*

---

## T

**Tasma** — Reference instance / venture: a smart-collar IoT product with ethical animal welfare focus. Existing legal-entity company; not yet a Leviathan-native organization (cited in `07-economy.md` §4 as migration target). *Introduced: `07-economy.md` §4, §5.1 · v0.1.0*

**Term** — The first layer of the constitutional substrate. Vocabulary the rest of the constitution is written in. This document's `glossary.md` is the kernel's own Terms layer. *Introduced: `02-anatomy.md` §2.1 · v0.1.0*

**Tier System** — The classification (immutable / protected / mutable) applied to every constitutional clause. Determines amendment procedure. *Introduced: `00-meta.md` §2, `04-living.md` §3 · v0.1.0*

**Trinity** — The three runtime roles: Sidecar (synchronous), Magistrate (asynchronous), Sovereign (override). Together they form the protocol's enforcement architecture. *Introduced: `02-anatomy.md` §6 · v0.1.0*

---

## V

**Validator** — A party operating one or more Magistrate nodes, with stake denominated in token. Eligible for governance voting. Subject to slashing. *Introduced: `07-economy.md` §1.1, §3 · v0.1.0*

**Vendored Fork** — A fork that holds a complete local copy of every kernel-owned file, rather than referring to upstream via git submodule. Selected as the build-phase strategy for forkability under network partition, operator autonomy, and privacy of fork existence. Drift detected mechanically via fork-manifest hash check. *Introduced: `specs/FORK_PROTOCOL.md` §1 · v0.4.0*

**Voyager Synthesis** — Reference to Voyager (Wang et al., 2023): an agent system that synthesizes new skills from primitives through self-directed exploration. The Mind runtime adapts this pattern under the constraint that all synthesized skills pass constitutional approval (`06-mind.md` §4). *Introduced: `06-mind.md` §3 · v0.1.0*

---

## Notes on This Layer

This glossary is itself a kernel part. Its tier is **protected** — terms can be added without panel review (mutable extension), but a term's definition cannot be retroactively narrowed without amendment (`I-7` analog at the documentation layer).

When a kernel part introduces a new capitalized term, the term must be added here in the same patch. The reverse review applies: a term in this glossary that is no longer cited in any kernel part is a candidate for removal at the next 90-day review (`04-living.md` §6).

---

*Glossary follows the parts. Companion file: `CHANGELOG.md`.*
