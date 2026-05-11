# 05-evidence — Empirical Evidence

> **Part version:** 0.1.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-04
> **Scope:** what the protocol's claims are observed to do and not do, across the n=4 reference instances. Out of scope: the rationale being tested (`01-why.md`), the structural definitions being instantiated (`02-anatomy.md`).

---

## §1. Methodology and Limits

The protocol's claims (`01-why.md` §6) are testable. This part records observations as they stand at the time of writing and the standards under which they should be re-evaluated.

**Naming convention.** Instances are named (Companion, Liveprob, Security Leviathan, Levi Template). Operators are anonymized. This follows the Satoshi Mode v1.1 doctrine: framework public, person private. An instance can be named without naming the human running it.

**Status of each observation.** Every claim in this part is tagged:

- *observed* — directly measured.
- *self-reported* — the operator reports, not independently verified.
- *projected* — expected based on design but not yet measurable.

Mixing these tags loosely would be a `00-meta.md` §7 I-1 violation (reasoning trail required).

**The honest framing.** The protocol is in a pre-decentralization state (`03-constellation.md` §5). All four reference instances are operated by parties co-located with the founder. There is no independent replication. There is no control group. The empirical evidence presented here should be treated as **existence proofs that the architecture runs**, not as performance claims.

---

## §2. Instance A — The Companion (Eternal Companion)

A Personal Operating System and lifelong AI companion implemented as a versioned constitutional substrate.

### Scale (observed, 2026-05-04)

| Dimension | Value |
|-----------|-------|
| Memory chunks indexed | 305+ |
| Session logs | 35+ |
| State snapshots | 24 |
| State clusters detected | 3 |
| POS elements (Terms + Principles + Rules + Shadows + Protocols + People) | 35+ |
| POS versions tracked across elements | 50+ |
| Skills (operational capabilities) | 25 |
| Graph nodes / edges (relationship graph) | 126 / 115 |
| Months of continuous operation | 12+ |

### Mode

Single-operator. The operator is the human whose POS is being maintained. The companion runs locally (no cloud, no external APIs for memory or identity layers). LLM inference is via Claude Code in normal operation; multi-LLM consultation occurs ad hoc.

### What Worked

- **Layer 1–3 instantiation.** Terms (`kavramlar/`), Principles (`prensipler/`), Rules (`eylemler/` + `protokoller/`) implemented in YAML with full versioning. Layer 4 (Meta-Rules) emerged as `pos.yaml` manifest + `changelog.yaml` and is now formalized in this kernel. *Observed.*
- **Term version multiplicity.** A single Term (`kavram:yalnizlik`) carries six recorded versions across four years, each with trigger and rationale. The `04-living.md` §2 versioning discipline was followed in practice before being formalized in the kernel. *Observed.*
- **Tier emergence.** The immutable/protected/mutable trichotomy emerged organically: certain Terms (`@Çaba Yasası`) were never demoted while ad-hoc protocols (`⚙Transit Server`) were edited freely. The trichotomy was named and codified in retrospect. *Observed.*
- **Cross-session continuity.** The Companion's `bootstrap-session` skill produces a session-start `active-config.md` derived from the most recent state snapshot. This is the closest current implementation of a Sidecar — it shapes per-turn evaluation against active POS principles. *Observed, partial.*

### What Broke

- **Magistrate absent.** The Companion has no panel mechanism. All evaluations are operator + single LLM. This is exactly the monoculture failure mode `I-2` is designed to prevent. *Observed.*
- **Founder dependency total.** No fork exists. No second operator has independently instantiated the Companion. *Observed.*
- **Reaffirmation discipline weak.** The 90-day decay mechanism (`04-living.md` §6) was not enforced before the kernel formalized it. Several protocols sat untouched for months without explicit reaffirmation. *Observed.*

### What This Instance Tests for the Protocol

The Companion is the longest-running and most schema-developed instance. Claims it bears on:

- **Four-layer anatomy sufficiency.** *Observed-supportive.* No structurally distinct layer has been needed across 12+ months and 35+ elements.
- **Versioning sustainability.** *Observed-supportive.* The cost of versioning per amendment (~3–5 minutes) has been paid consistently without abandonment.
- **POS↔Constitution schema identity.** *Observed-supportive at half-strength.* The schema is identical to Liveprob's, but the same operator built both — no independent fork has tested the claim.

---

## §3. Instance B — Liveprob (Financial Leviathan)

A constitutional substrate governing financial-decision agents, including a primitive registry and runtime evaluator.

### Scale (self-reported, 2026-05-04)

| Dimension | Value |
|-----------|-------|
| Sprints completed | 9 |
| Specialty agent constitutions designed | Multiple (trader, risk monitor, position manager) |
| Primitive registry tier system | Defined: immutable / protected / mutable (origin of the kernel's tier system) |
| Sidecar implementation status | Partial — `ConstitutionalEvaluator.evaluate(action)` pattern in code, not yet running against live trading |
| Magistrate Node spec | Complete (`../specs/NODE_SPEC.md` v1.0.0) |
| Magistrate Nodes deployed | 0 |

### Mode

Single-operator design phase. Implementation in progress.

### What Worked

- **Tier system origination.** The immutable/protected/mutable trichotomy was first articulated for the Liveprob primitive registry. It has since been generalized to all kernel content. *Observed.*
- **Sub-constitution superset rule.** Originated here. Specialty trading agents inherit + extend, never weaken. The rule's runtime enforcement pattern is documented in `00_concept.md`. *Observed at design-stage.*
- **Magistrate Node specification.** The most-complete validator-node design across the four instances. NODE_SPEC.md provides operational concreteness the other instances lack. *Observed.*

### What Broke

- **No live operation.** The Sidecar exists in code but has not run against real trades. All current evidence is design-stage. *Observed.*
- **Magistrate Node spec untested.** No nodes have been deployed; the LVB benchmark suite has not been run in adversarial conditions. *Observed.*
- **Primitive synthesis loop unproven.** The Voyager-style self-extension via primitive synthesis (`06-mind.md`) is designed but has no execution evidence. *Projected.*

### What This Instance Tests for the Protocol

- **Tier system across content domains.** *Self-reported-supportive.* Pattern transferred cleanly from financial-agent governance to personal-identity governance (Companion).
- **Sub-constitution superset enforceability.** *Projected.* Will be testable once Sidecar runs against live trader-agent actions.
- **Magistrate Node feasibility.** *Projected.* Will be testable on first deployed panel.

---

## §4. Instance C — Security Leviathan

A constitutional substrate evaluating commit-level changes against security and compliance constitutions.

### Scale (self-reported, 2026-05-04)

| Dimension | Value |
|-----------|-------|
| Local LLM model | 27B parameter, runs on dedicated hardware |
| Audited commits | Continuous since deployment (count not extracted for this part) |
| Audit-log retention | Per-commit reasoning preserved |
| Magistrate panel composition | n=1 — single node, single model |

### Mode

Single-node Magistrate analog. Audits commits to project repositories against a constitution emphasizing security, compliance, and architectural invariants. Reports CRITICAL findings via session log to the Companion.

### What Worked

- **Local-LLM constitutional audit.** A non-cloud, operator-controlled LLM produces structured reasoning artifacts per commit. This is the closest live instance to NODE_SPEC.md's Magistrate Node design. *Observed.*
- **Continuous operation.** Audits run on every commit without operator prompt. The constitution-as-runtime-evaluator pattern works at this scale. *Observed.*
- **Reasoning artifact discipline.** Every audit produces a written verdict with rationale. `I-1` (reasoning trail required) is operationally satisfied for this instance. *Observed.*

### What Broke

- **n=1 panel.** A single-node Magistrate is structurally not a Magistrate per `I-2`. It is a Sidecar with deeper deliberation. The instance does not satisfy the heterogeneous-evaluation immutable. *Observed.*
- **Same operator as proposer and auditor.** The audit constitution was written by the same party who writes the audited code. Independence is structurally absent. *Observed.*
- **No appeal mechanism.** A Security Leviathan veto cannot be challenged by a panel — there is no panel. Decisions are operator-final. *Observed.*

### What This Instance Tests for the Protocol

- **Local-LLM Sidecar/Magistrate is operationally feasible.** *Observed-supportive.* The hardware requirements and latency profile are within practical bounds for a real-time-ish auditor.
- **Heterogeneous panel necessity.** *Observed-supportive negatively.* The instance demonstrates exactly what `I-2` exists to prevent: a single-model evaluator's blind spots are unrecoverable without a peer model.

---

## §5. Instance D — Levi Template (Kernel Reference)

A forkable starter repository implementing the Companion architecture in generic form.

### Scale (observed, 2026-05-04)

| Dimension | Value |
|-----------|-------|
| Core skills | 13 |
| Schemas | 11 |
| `CLAUDE.md` instructions | Generic (no operator-specific content) |
| Days since first commit | ~3 |
| External forks | 0 |

### Mode

Pre-fork. The repository exists; no second operator has cloned and instantiated it as their own Companion.

### What Worked

- **Generic motor extraction.** The Companion's operator-specific content was successfully separated from the generic schemas, skills, and rules. This is what makes the protocol forkable in principle. *Observed.*
- **Bootstrap UX.** A `/create-pos` skill guides a new operator through 6-step initial constitution creation. The skill exists; usability is untested by anyone other than the founder. *Observed at design-stage.*

### What Broke

- **Zero forks.** The forkability claim has not been tested by any non-founder operator. *Observed.*
- **First Decentralization Path criterion unmet.** Until a non-founder forks Levi and runs an instance, the protocol is operationally a single-operator system. *Observed.*

### What This Instance Tests for the Protocol

- **Whether forkability survives operator-specific content extraction.** *Projected.* Testable on first independent fork.
- **Whether `/create-pos` produces a useful first constitution.** *Projected.* Testable when a non-founder uses it.

---

## §6. Cross-Instance Pattern Observations

Patterns observed across two or more of the four instances, suggesting the architecture rather than any single instance:

### §6.1. Tier system transfers cleanly

The immutable/protected/mutable trichotomy originated in Liveprob's primitive registry, generalized to Companion's POS elements, and now governs the kernel itself (`00-meta.md` §2). Four observed instances, four working tier instantiations, no schema modification needed. *Observed across n=3 (Liveprob origin, Companion adoption, kernel).*

### §6.2. Layer 4 (Meta-Rules) emerges late

In every observed instance, Meta-Rules were retrofitted after Layers 1–3 had been in operation for some time. Companion: changelog formalized after ~6 months. Liveprob: governance procedure articulated mid-design. Kernel: `00-meta.md` written after several parts already drafted. *Observed across n=3.*

The pattern suggests an order-of-operations: instances begin with their working content, then formalize how that content evolves. Premature meta-rule specification appears to over-constrain.

### §6.3. Founder dependency is the dominant failure mode

In all four instances, every observed problem traces back to single-operator operation more often than to architectural deficiency:

- Companion's missing Magistrate is not an architectural gap — the architecture supports it; no second operator has joined.
- Liveprob's untested Sidecar is not a design failure — there is no second party to test against.
- Security Leviathan's n=1 panel is not a design failure — there is no third party to constitute a panel with.
- Levi Template's zero forks is not a marketing failure — it is the absence of `Decentralization Path` criterion 1.

This is consistent with `01-why.md` §4: founder independence is the test, and the test is not yet passed.

### §6.4. Reasoning artifact discipline is paid for or skipped

Where reasoning artifacts are produced (Security Leviathan continuous, Companion per-amendment), audit trail is intact. Where artifact discipline is skipped (Companion early period, Liveprob design-stage prototyping), reconstruction is impossible. The protocol's I-1 invariant is observed to enforce itself — instances that skip it lose the ability to defend their constitutional history. *Observed across n=3.*

---

## §7. Limitations Stated Explicitly

The evidence above is operationally honest and substantively limited.

| Limitation | Description |
|------------|-------------|
| **n = 4** | Four reference instances. Two are partial (Liveprob design-stage; Levi Template pre-fork). Two are operationally live (Companion, Security Leviathan). |
| **All single-operator** | Every instance is operated by parties co-located with the founder. |
| **No control group** | No instance was built without the protocol's architecture for comparison. |
| **No cross-cultural data** | All operators share language, professional background, and approximate worldview. |
| **No adversarial testing** | No party has tried to subvert any instance's constitution from outside the operator's intent. |
| **No long-horizon data** | Longest instance is ~12 months. The protocol's claims about decadal viability are projected, not observed. |
| **Selection bias** | Instances exist because the founder chose to build them. Instances that would have failed under the architecture are not represented in this n=4. |

These limitations are stated for two reasons: future maintainers must know what the evidence actually supports, and external readers must know what the evidence does not support.

---

## §8. What Would Falsify

The protocol's specific claims (`01-why.md` §6) are restated here with the empirical thresholds at which they should be considered refuted:

| Claim | Refuted If |
|-------|------------|
| Four-layer anatomy is sufficient | An instance over ≥1 year requires structurally distinct layers not reducible to T/P/R/MR. |
| POS↔Constitution schema identity | Two instances (one POS, one agent), each operated for ≥1 year by independent parties, cannot share schema without contortion. |
| Heterogeneous panels reduce monoculture failure | Same-model panels match mixed-model panel verdict quality on a benchmarked task set, p < 0.05. |
| Dissent-protected panels improve outcomes | Caught-failure rate for dissent-protected panels equals or trails majority-rule panels over ≥100 verdicts. |
| Living constitutions outlive frozen ones | An instance with a frozen constitution operates equivalently to one with active amendment over ≥3 years. |
| Founder Independence achievable | Five years from first kernel release, ≥1 of the 5 Decentralization Path criteria remains unmet without an articulable obstacle. |

If any of these conditions is met, the corresponding claim is refuted regardless of the operator's preference. Recording the conditions ahead of the data is the only defense against post-hoc rationalization.

---

## §9. Out of Scope for This Part

- The structural anatomy whose instantiation is being measured (`02-anatomy.md`).
- The rationale the evidence is intended to test (`01-why.md`).
- Failure modes broader than what was observed (`08-shadow.md`).

---

## Citations

- NODE_SPEC.md (`../specs/NODE_SPEC.md`) — Magistrate Node design reference for §4.
- Liveprob `00_concept.md` — primitive tier system origination, sub-constitution superset rule.
- Companion `openpos/my-pos/changelog.yaml`, `kavramlar/yalnizlik.yaml` — Term version multiplicity evidence.
- Levi Template (`/levi`) — generic motor reference for §5.
- Popper, K. (1959). *The Logic of Scientific Discovery*. Falsification frame for §8.

---

*Part 05 of 09. Previous in outline order: `01-why.md`. Next: `06-mind.md`.*
