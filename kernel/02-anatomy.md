# 02-anatomy — Anatomy of a Leviathan

> **Part version:** 0.1.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-04
> **Scope:** structural definition of a Leviathan instance. Out of scope: cross-instance topology (`03-constellation.md`), evolution mechanics (`00-meta.md`, `04-living.md`), reference runtimes (`06-mind.md`).

---

## §1. The Four Layers

A Leviathan instance is a constitutional substrate organized into four layers. Each layer is constrained by the one above and is the type system for the one below.

```
┌──────────────────────────────────────────────────────┐
│ Layer 4: Meta-Rules                                   │
│   How Layers 1–3 themselves change. Versioning,       │
│   amendment procedure, immutable invariants.          │
├──────────────────────────────────────────────────────┤
│ Layer 3: Rules                                        │
│   Concrete behaviors enforced at action time.         │
│   Phrased in Principles, expressed in Terms.          │
├──────────────────────────────────────────────────────┤
│ Layer 2: Principles                                   │
│   Values that orient decisions. Compose Terms into    │
│   normative statements.                               │
├──────────────────────────────────────────────────────┤
│ Layer 1: Terms                                        │
│   Vocabulary. Atomic concepts the instance reasons    │
│   about. Definitions, not statements.                 │
└──────────────────────────────────────────────────────┘
```

A constitution that omits any layer is incomplete. A constitution with only Rules is brittle (no shared vocabulary, no principle to derive new rules from). A constitution with only Principles is unenforceable (no concrete behaviors). A constitution without Meta-Rules is dead the moment context shifts.

This four-layer pattern is observed in both reference instances:

| Layer | Companion (`openpos/my-pos/`) | Liveprob (`00_concept.md`) |
|-------|-------------------------------|----------------------------|
| Terms | `kavramlar/*.yaml` (8 concepts) | Primitive registry types |
| Principles | `prensipler/*.yaml` (6 principles) | Domain principles |
| Rules | `eylemler/*.yaml`, `protokoller/*.yaml` | Specialty agent rule sets |
| Meta-Rules | `pos.yaml` manifest, `changelog.yaml` | Tier system, governance procedure |

The structural identity between a personal operating system and an agent constitution is not metaphor. It is the central empirical claim of the protocol (see `01-why.md`).

---

## §2. Layer 1 — Terms

A **Term** is a definition. It does not assert anything; it gives a name to a concept the rest of the constitution will use.

```yaml
# Example (Companion):
id: kavram:caba-yasasi
name: "Çaba Yasası"
definition: "The Law of Reversed Effort. Forcing an outcome distances it."
version: 2.1
```

Terms have versions because the meaning of a term changes over time. The Companion's definition of `yalnızlık` (loneliness) has six recorded versions across four years; each version reflects a real change in the operator's understanding, with the trigger captured in the changelog.

**Why this matters at the kernel level:** if Layer 2 (Principles) is allowed to use undefined or implicitly-defined terms, the constitution becomes interpretive rather than enforceable. A Magistrate panel evaluating an action against `#dürüstlük` (honesty) needs the term layer to fix what `dürüstlük` means in this instance, at this version of the constitution.

Terms are typically **mutable** tier (per `00-meta.md` §2). They evolve naturally as the instance's understanding deepens. Terms used as the basis of Immutable invariants are themselves Immutable.

---

## §3. Layer 2 — Principles

A **Principle** is a normative statement composed of Terms. It orients decisions but does not enforce them at action time.

```yaml
# Example (Companion):
id: prensip:acik-avuclarla-tut
name: "Hold with Open Palms"
statement: "Apply Caba Yasası to relationships, projects, outcomes — but maintain limits."
depends: [kavram:su-ornegi, prensip:caba-yasasi]
version: 1.1
```

Principles have a `depends` field listing the Terms (and other Principles) they compose. This produces a directed acyclic graph: changing a Term forces a review of every Principle that depends on it. The Magistrate panel evaluating an amendment proposal is required to walk this graph (`00-meta.md` §4.2).

**Specialty principles** are scoped to a sub-domain. A trading agent under Liveprob has principles about leverage, position sizing, slippage tolerance — these compose with kernel-level principles (e.g., do not cause irreversible loss to other agents). Specialty principles cannot weaken kernel principles; they can only extend (§7 below).

Principles are typically **protected** tier. Changes require a Magistrate panel.

---

## §4. Layer 3 — Rules

A **Rule** is a concrete behavior enforced at action time. Rules are the layer that the runtime evaluator (the **Sidecar**, §6.1) actually checks against.

```yaml
# Example (Companion):
id: eylem:duzeltme-durtusunu-fark-et
name: "Notice the Urge to Fix"
trigger: "When attempting to correct another person's behavior"
action: "Pause. This is Saviour Narcissism."
depends: [kavram:kurtarici-narsizmi]
status: active
```

```yaml
# Example (Liveprob):
id: rule:no-leverage-above-2x
trigger: "trader_agent.action == OPEN_POSITION"
condition: "leverage <= 2.0"
on_violation: REJECT
depends: [prensip:limited-downside]
status: active
```

A Rule has a trigger (when does this apply), a condition or action specification, a violation behavior, and a `depends` chain back to the Principles that justify it. Rules without justification chains do not pass kernel review; they are arbitrary enforcement and cannot be defended in a Magistrate evaluation.

Rules are typically **mutable** tier — they are the working surface where the constitution meets reality, and they need to evolve quickly. Rules promoted to operational stability may be reclassified as protected.

---

## §5. Layer 4 — Meta-Rules

Meta-Rules govern how Layers 1–3 themselves change. They are defined for this kernel in `00-meta.md`. Each instance forks the kernel's meta-rules and may extend them; instances cannot weaken the immutable invariants in `00-meta.md` §7.

The minimum Meta-Rule set every Leviathan instance must have:

1. A versioning scheme for Terms, Principles, and Rules.
2. A changelog recording every amendment with trigger and rationale.
3. An amendment procedure (who proposes, who reviews, threshold for acceptance).
4. A declaration of which clauses are Immutable for this instance.
5. A review cadence preventing silent ossification.

A constitution lacking any of these five is not a Leviathan instance. It may still be useful, but it is not in the constellation.

---

## §6. The Trinity

A Leviathan instance enforces its constitution through three loci. Each handles a different time scale and a different decision class.

### §6.1. Sidecar — Synchronous, In-Line

The **Sidecar** evaluates every action proposed by the instance against Layer 3 (Rules). It runs synchronously: the action does not execute until the Sidecar returns APPROVE.

```
Agent → proposes ACTION → Sidecar.evaluate(ACTION, constitution)
                              │
                              ├── APPROVE → execute
                              ├── REJECT  → block, return reason
                              └── ESCALATE → defer to Magistrate
```

Sidecar latency budget is on the order of action latency itself — milliseconds for a Liveprob primitive, seconds for a Companion conversation turn. The Sidecar does not deliberate; it pattern-matches against the active rule set.

The Sidecar's authority is bounded: it can only evaluate against Rules that are loaded and active. It cannot rewrite rules, accept ambiguous outcomes, or run a panel. If the action is outside the Sidecar's confident envelope, it must escalate.

**Reference implementation:** Liveprob `ConstitutionalEvaluator.evaluate(action) → EvaluationResult` pattern (`00_concept.md`). Companion's Sidecar is currently implicit (the operator + LLM jointly evaluate every response against `bible/active-config.md` and POS principles); explicit per-turn evaluation is on the roadmap.

### §6.2. Magistrate — Asynchronous, Multi-Model Panel

The **Magistrate** is the constitutional verdict mechanism for decisions the Sidecar cannot resolve alone:

- Constitutional amendments (kernel or instance).
- Promotion of a primitive into the dictionary (`06-mind.md`).
- Acceptance of a Lesson Ledger entry from another instance (`03-constellation.md`).
- Audits of Sidecar decisions (was the rejection justified, was the approval too lenient).
- Resolution of ambiguous cases the Sidecar escalated.

Defined in detail in `../specs/NODE_SPEC.md`. Summary properties:

- **Multi-node, multi-model.** A Magistrate panel is composed of N≥3 nodes running heterogeneous LLMs. Heterogeneity is an Immutable invariant (`00-meta.md` §7 I-2).
- **Blind evaluation.** No node sees another's verdict before settlement (NODE_SPEC.md §8.1).
- **Mandatory reasoning documents.** Every verdict produces a written, retrievable artifact (NODE_SPEC.md §6).
- **Two-round dispute resolution.** Round 1 unanimity → settle. Any dissent → Round 2 with fresh panel + 80% supermajority (NODE_SPEC.md §4.3–§4.5).
- **Dissent protected.** A dissenting node is not penalized for disagreement; dissent is the trigger for deeper review (`00-meta.md` §7 I-3).

The Magistrate's authority is to settle constitutional questions and produce an auditable record. It cannot execute actions in the world — that is the Sidecar's domain, gated by the Magistrate's verdict.

### §6.3. Sovereign — Human Override

The **Sovereign** is the human operator with override authority for an instance. The Sovereign can:

- Halt the instance.
- Override a Sidecar approval (decline to execute).
- Refuse to apply a Magistrate-settled amendment.
- Initiate a fork (`00-meta.md` §4.5).

The Sovereign cannot:

- Forge a Magistrate verdict.
- Erase the audit trail (`00-meta.md` §7 I-7).
- Tighten the license retroactively (`00-meta.md` §7 I-4).
- Extract another instance's data without that instance's operator action (`00-meta.md` §7 I-6).

The Sovereign is per-instance, divisible by fork. This is an explicit doctrinal departure from Hobbes's indivisible sovereign (cited in `00-meta.md`). A constellation has many Sovereigns, none of which has authority over another's instance.

---

## §7. Sub-Constitution Superset Rule

A specialty agent operating under a Leviathan instance has its own constitution (its specialty rules, principles, possibly extended terms). This sub-constitution must be a **superset** of the parent constitution: it inherits everything and may extend, but cannot weaken.

```
ParentConstitution ⊆ SubConstitution
```

Concretely:

- Every Term in the parent is defined identically (or more strictly) in the sub.
- Every Principle in the parent appears in the sub, possibly with additional clauses, never with weakened ones.
- Every Rule in the parent is enforced by the sub's Sidecar.

This is **runtime enforced**, not honor-system. The Sidecar of the specialty agent loads both the parent and the sub-constitution and refuses to execute if a sub-rule contradicts a parent rule. The Magistrate refuses to approve a sub-constitution amendment that weakens parent invariants.

Without this rule, sub-constitutions would silently nullify the parent. With this rule, the parent's guarantees compose through the agent hierarchy.

This pattern is the constitutional analog of the Liskov substitution principle: a sub-constitution must be substitutable for the parent in every context the parent governs.

---

## §8. Current Implementation Status (Honest)

The Trinity is fully present in **zero** of the n=4 reference instances at the time of writing. This section records the gap.

| Instance | Sidecar | Magistrate | Sovereign |
|----------|---------|------------|-----------|
| Companion (Eternal Companion) | implicit (operator + LLM joint evaluation per turn) | not implemented | yes (operator) |
| Liveprob (Financial) | designed, partial impl in `ConstitutionalEvaluator` | designed (NODE_SPEC.md), not deployed | yes (operator + Telegram approval) |
| Security Leviathan | n/a (audit role only) | partial (1 node, 1 model — not yet a panel) | yes (operator) |
| Levi Template | not applicable (template, not running instance) | not applicable | yes (whoever forks) |

The honest framing: the Trinity is the protocol's claim about what a complete Leviathan looks like. None of the current instances are complete. The claim is testable: as instances move toward Trinity completeness, do constitutional violations decrease, do amendment cycles improve, do cross-instance Lessons transfer cleanly? Empirical answers live in `05-evidence.md`.

---

## §9. Out of Scope for This Part

- How instances communicate (`03-constellation.md`).
- How layers evolve over time (`04-living.md`, `00-meta.md`).
- What runtime executes Layer 3 Rules in detail (`06-mind.md`).
- Why this anatomy is the right anatomy (`01-why.md`).

---

## Citations

- NODE_SPEC.md — Magistrate definition, blind evaluation, reasoning documents, two-round procedure.
- Liveprob `00_concept.md` — `ConstitutionalEvaluator` pattern, primitive tier system, sub-constitution superset rule (originated here).
- Liskov, B. (1987). *Data abstraction and hierarchy*. Substitutability principle, applied here to constitutional composition.
- Companion `openpos/my-pos/` schema — empirical four-layer instantiation across 35+ versioned elements.

---

*Part 02 of 09. Previous: `00-meta.md`. Next per outline order: `04-living.md`.*
