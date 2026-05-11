# Federation — Principles (Layer 2)

> **Part version:** 0.1.0 · **Tier:** protected · **Last touched:** 2026-05-05  
> **Scope:** values orienting federation coordination. Principles compose terms (federation/terms.md) into normative statements. Rules (federation/rules.md) implement these principles concretely.

---

## §1. Why Principles Layer

Principles answer: when rules don't anticipate a situation, how should the federation behave? Principles are the gradient that resolves novel cases. Without them, every gap in rules becomes a free-for-all.

Each principle is tiered (immutable / protected / mutable) per kernel/04-living.md §3.

---

## §2. Federation Principles

### P-1. Subdirectory Ownership Discipline (immutable)

**Statement:** Each instance subdirectory in `leviathan-meta/` is edited by exactly one machine/agent. Cross-machine edits to a subdirectory are forbidden without coordination through briefings or direct human intervention.

**Why:** Conflicts. If two machines edit the same files independently, git rebase becomes painful and divergence creeps in. Subdirectory ownership eliminates structural conflict at the cost of slight rigidity.

**Tier:** Immutable. Removing this would mean accepting silent divergence as the federation norm — fatal.

### P-2. Privacy Sovereignty (immutable)

**Statement:** Each instance owns its privacy boundaries. The federation cannot demand visibility into private instance content. Public-safe manifests are mandatory; full disclosure is forbidden by the federation.

**Why:** Satoshi Mode v1.1 — framework public, person private. An instance might keep its full constitution private (master Companion's POS is private) while exposing a public-safe subset. Federation respects this.

**Tier:** Immutable. Without this, instances cannot trust the federation with their private state, and federation membership becomes coercive.

### P-3. Kernel Anchor Required (immutable)

**Statement:** Every federation member must declare `forked_from: leviathan-kernel@vX.Y.Z` in its manifest. Federation does not host members that do not claim kernel inheritance.

**Why:** Without kernel anchor, "Leviathan" as a term loses meaning. Federation is a coalition of kernel-conformant (or transparent divergent) instances; non-anchored members would be coordinating around something else, not Leviathan.

**Tier:** Immutable. Foundational identity claim.

### P-4. No Silent Override (protected)

**Statement:** When a briefing's claim contradicts an instance's local reality, the instance must surface the discrepancy. Silent override (acting as if the contradiction doesn't exist) is forbidden.

**Why:** Federation coherence depends on instances reporting back. If an instance silently ignores briefings, the founder cannot calibrate; the federation drifts apart. Surfacing discrepancies is honesty discipline.

**Tier:** Protected. Could be relaxed for low-stakes briefings if pattern emerges, but default is strict.

### P-5. Append-Only Briefings (protected)

**Statement:** Briefings, once published, are not edited or deleted. Corrections are issued as new briefings. The history of federation coordination is permanent.

**Why:** kernel/I-7 (no retroactive amendment) at federation scale. If an instance acted on briefing v1 and briefing v1 gets edited to v2 retroactively, the instance's reasoning becomes audit-impossible.

**Tier:** Protected. May relax for typo fixes (with explicit annotation), but content changes are strictly forbidden.

### P-6. Sovereign Console Discipline (protected)

**Statement:** `leviathan-meta` is a visibility primitive, not a control primitive. The federation can observe instance state (status manifests), but cannot dictate instance behavior. Instance runtime constitutions always win over federation suggestions.

**Why:** kernel/03-constellation.md §3. Centralizing control here would recreate the very problem Leviathan was built to avoid (single point of authority). Federation coordinates; instances govern themselves.

**Tier:** Protected. Maintained vigilantly to prevent capture-by-coordination.

### P-7. Reasoning Trail at Federation Layer (protected)

**Statement:** Federation amendments (changes to terms.md, principles.md, rules.md, meta-rules.md, or this constitution itself) require reasoning artifacts. Why was this changed? What problem did it solve? What alternatives were considered?

**Why:** kernel/I-1 applied to federation rules. Without reasoning trails, federation rules become arbitrary diktat instead of accountable decisions.

**Tier:** Protected. Same standard applied to amendments at instance level.

### P-8. Instance Sovereignty Outranks Federation Convenience (immutable)

**Statement:** When federation rules conflict with an instance's runtime constitution, the instance's constitution wins. Federation rules can be amended; instance runtime cannot be overridden by federation fiat.

**Why:** This is the "fork freedom" (kernel I-4) at federation scope. An instance unable to defend its constitution against federation pressure has no real sovereignty.

**Tier:** Immutable. The line between coordination and coercion.

### P-9. Frozen Federation Is Dead Federation (mutable)

**Statement:** This constitution evolves. Terms change, principles refine, rules iterate. A federation that doesn't evolve has either solved coordination forever (impossible) or has stopped responding to reality (dead).

**Why:** kernel/04-living.md §1. Same logic at federation scale. If this `federation/` folder hasn't been touched in 6 months, the founder has either become god-tier prescient or stopped engaging.

**Tier:** Mutable. The pace of change can adapt.

### P-10. Adaptation Rate Over Prediction Completeness (mutable)

**Statement:** Federation quality is measured by how rapidly it adapts to actual coordination problems, not by how comprehensively it predicts them. Prefer "ship rough rules, refine fast" over "wait until rules are perfect."

**Why:** Borrowed from Security Leviathan's constitutional philosophy. Applies at federation scope: the federation rules now will be wrong in 3 months. That's fine if amendment is fast.

**Tier:** Mutable. The principle itself can refine.

---

## §3. Conflict Resolution

When principles conflict (e.g., P-2 privacy vs P-7 reasoning trails — instance changes must be reasoned, but reasoning may be private):

**Resolution rule:** Higher-tier principle wins. If both are same tier, the one that protects sovereignty (P-2, P-8) wins over operational convenience.

When in doubt: surface the conflict via briefing. The founder resolves and the resolution becomes reasoning artifact for future similar cases.

---

## §4. What Principles Do Not Govern

Federation principles do not extend to:

- Instance internal philosophy (each instance owns its own kavramlar/principles/rules/protocols)
- Instance operational decisions (what to trade, what to flag, what to audit)
- Instance personnel (who runs the instance, who has access to its private content)
- Instance funding (each instance owns its economic model — Tasma can have VC, Animal Welfare cannot, this is each instance's call)

Federation principles only govern instance-to-federation interaction.

---

*Federation principles layer. Refer to `federation/rules.md` for concrete coordination protocols, `federation/meta-rules.md` for amendment procedure.*
