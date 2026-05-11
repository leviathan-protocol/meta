# 03-constellation — The Federated Constellation

> **Part version:** 0.2.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-04
> **Scope:** how multiple Leviathan instances relate to each other and to the kernel. Out of scope: the structural anatomy of any single instance (`02-anatomy.md`), evolution mechanics (`04-living.md`), economic substrate (`07-economy.md`).

---

## §1. Why Federated, Not Master

The protocol explicitly rejects a master-instance topology.

A "master Leviathan" — one privileged instance that all others register with, route through, or report to — would re-introduce every property the protocol exists to avoid:

- **Single point of failure.** Master instance goes down → constellation goes silent.
- **Single point of capture.** Master instance subverted → entire constellation governed by the captor.
- **Founder dependency by architecture.** The master is operated by someone; that someone becomes structurally indispensable.
- **Asymmetric authority.** Master has read-write on instance data it should never see (`00-meta.md` §7 I-6).

A federated constellation has **no privileged instance**. Every Leviathan is structurally equal: same kernel, own data, own Sovereign. Coordination is opt-in and channel-specific (Lesson Ledger, Magistrate panel composition). No instance can compel another.

This is not a preference. It is the only topology that can satisfy:

- I-4 (fork freedom — a master could revoke fork rights for downstream instances).
- I-5 (founder removability — a master architecture preserves founder dependency by definition).
- I-6 (instance data sovereignty — a master needs to read-write across instances to act as master).

A master-Leviathan is therefore not an alternative architecture — it is a different protocol that happens to use the name. Under §4.5 of `00-meta.md` (fork divergence), it would have to call itself something else.

---

## §2. Kernel / Instance Separation

The constellation has exactly one kernel and many instances.

```
┌─────────────────────────────────────────────────┐
│         KERNEL (this repository: levi/)          │
│   - protocol definition (Parts 00–09)            │
│   - reference implementations (companion/, mind) │
│   - schemas, glossary, changelog                 │
│   - NO instance data                             │
└─────────────────────────────────────────────────┘
                      ▲
                      │ forks from
                      │
        ┌─────────────┼─────────────┬─────────────┐
        │             │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ Instance │   │ Instance │   │ Instance │   │ Instance │
   │    A    │   │    B    │   │    C    │   │    D    │
   │ (own POS,│   │ (own POS,│   │ (own POS,│   │ (own POS,│
   │ memory,  │   │ memory,  │   │ memory,  │   │ memory,  │
   │ logs)    │   │ logs)    │   │ logs)    │   │ logs)    │
   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

### What lives in the kernel

- The four-layer anatomy specification (`02-anatomy.md`).
- The amendment procedure and immutable invariants (`00-meta.md`).
- The Magistrate Node specification (`../specs/NODE_SPEC.md`).
- The Lesson Ledger schema and validation procedure (`§4` below).
- Reference implementations of runtimes (`06-mind.md`).
- Forking instructions (`§6` below).

### What lives in an instance

- The instance's specific Terms, Principles, Rules (its content, not its structure).
- Memory: conversation logs, indexed chunks, raw archives.
- State snapshots, session logs, emotional/operational fingerprints.
- The instance's `bible/` — curated truth specific to the instance's operator.
- The instance's local audit trail (which Sidecar evaluations fired, which were escalated).

The **structural identity** between two instances is enforced by the kernel they fork from. The **operational divergence** between two instances is preserved by the kernel never reading their data.

A consequence: an instance can be run entirely offline. It must only re-touch the kernel for amendment review (and even then, only if the operator chooses to participate in cross-instance Magistrate panels).

---

## §3. The Sovereign Console

The Sovereign Console is a **visibility primitive**, never a control primitive.

> **Status: planned, not built.** The Console does not yet exist as code. This part of the kernel describes what it must be when it exists. Marking this honestly is itself a `00-meta.md` §7 I-1 obligation.

### What the Console is for

When a constellation has multiple instances, the Sovereign of any one instance benefits from a partial view across the constellation:

- Are other instances applying similar amendments? (early warning of context shift)
- Are Lesson Ledger entries from peers being accepted by Magistrate panels? (signal of constellation health)
- Are decentralization criteria progressing? (`§5` below)
- Is any instance exhibiting failure-mode patterns described in `08-shadow.md`?

### What the Console can show

| Visible at constellation level | Origin |
|--------------------------------|--------|
| Number of registered instances | Self-reported, opt-in |
| Aggregate amendment rate per kernel part | Anonymized changelog metadata |
| Magistrate panel availability and average response time | Node Registry public data |
| Lesson Ledger entry counts and acceptance rates | Public ledger metadata |
| Decentralization Path criteria status | Computed from public data |

### What the Console cannot show

| Never visible at constellation level | Reason |
|--------------------------------------|--------|
| Any instance's specific Terms, Principles, or Rules | Instance content is private (I-6) |
| Any instance's memory, conversation logs, or session data | Operator data sovereignty (I-6) |
| Any instance operator's identity beyond what they self-declare | Satoshi Mode — framework public, person private |
| Any instance's Sidecar evaluation logs | Instance-internal audit, not constellation business |

The Console is not a dashboard built on top of instance data exfiltration. It is a register of self-reported, public-by-design metadata. An instance that does not self-register is not visible to the Console — and is no less a Leviathan for it.

### Architectural prohibition

The Console cannot:

- Issue commands to instances.
- Demand data from instances.
- Sanction or de-list instances based on content (only on protocol-violation evidence reviewed by Magistrate panel).
- Aggregate identifying metadata in ways that defeat operator anonymity (e.g., correlating self-report timestamps with public chain activity).

A Console implementation that violates these prohibitions is a fork (`00-meta.md` §4.5), not a kernel-conformant Console.

### §3.5. Who Operates a Console

The Console is **a code pattern, not a deployment**. Anyone may run an instance.

This follows directly from three properties already established:

- The data a Console aggregates (Magistrate Node Registry, Lesson Ledger entries, on-chain governance state, self-reported instance metadata) is **public by construction**. There is no privileged data Console operators access that other operators cannot.
- Founder removability (I-5) requires that Console availability not depend on any single party. A founder-operated Console is a structural founder-dependency.
- Heterogeneous evaluation (I-2) is a kernel doctrine; restricting it to verdict panels and excluding observation infrastructure would be inconsistent.

Multiple competing Consoles are the expected steady state, not an exception. Differences in filtering, presentation, alerting, and historical depth are legitimate product variation. The web-search-engine analogy is exact: the public web is not Google's; the Magistrate Registry and Lesson Ledger are not any single Console's.

**Cross-Console dissent as detection.** When Consoles compute conflicting summaries from the same public data, the conflict is itself a public signal. A Console that consistently reports figures other Consoles cannot reproduce is detectable by the same pattern-analysis used for lazy Magistrate nodes (NODE_SPEC.md §8.2 — pattern analysis, statistical detection). Console honesty is enforced by the existence of competing Consoles, not by central audit.

**No "official" Console.** No Console may claim authoritative status. A Console operator may claim "comprehensive" or "real-time" or "best UI" — those are product claims. "Official" or "canonical" claims are I-5 violations and disqualify the Console from kernel-conformant status.

**Operator transparency requirement.** A kernel-conformant Console must publish: who operates it, what subset of public data it aggregates, what filtering or weighting it applies, and how often its data refreshes. Consoles that obscure these are not kernel-conformant — they are visibility products that happen to display Leviathan data.

---

## §4. The Lesson Ledger

Instances learn things. The Lesson Ledger is the mechanism by which one instance can offer a learning to others, without exposing the data the learning came from.

> **Status: schema sketch only.** No implementation exists. Schema below is a v0 proposal subject to amendment.

### What a Lesson is

A Lesson is a structured proposal of the form *"behavior X under condition Y leads to outcome Z; consider amending Rule R or Principle P."* It is not the underlying data; it is the conclusion.

### Schema (v0 sketch)

```yaml
lesson_id: <ipfs-hash>
proposed_by: <instance-id>     # not operator-id
proposed_at: <iso-date>

condition:                      # under what circumstances was this observed
  domain: <kernel-domain-tag>
  context: <freeform-anonymized-summary>
  observation_count: <int>      # how many times observed in proposing instance

claim:                          # what the lesson asserts
  type: rule_amendment | principle_extension | shadow_promotion | term_clarification
  target_element_pattern: <kernel-element-pattern>  # e.g. "any prensip:durustluk-equivalent"
  proposed_change: <freeform>

evidence:                       # what justifies the claim
  reasoning: <freeform>
  redacted_examples: <freeform-fully-anonymized>
  counter_evidence_considered: <freeform>

constraints:                    # what kernel parts must NOT change
  immutables_checked: [I-1, I-2, ...]   # from 00-meta §7
  precondition_terms: [<term-id>...]
```

A Lesson is a **proposal**, not a directive. Receiving instances are free to ignore, accept, or accept-with-modification.

### Validation procedure

A Lesson cannot enter the constellation until a Magistrate panel approves it.

1. The proposing instance pins the Lesson to IPFS and submits the hash to the Ledger.
2. A Magistrate panel of N≥3 nodes (heterogeneous models, per I-2) is randomly assigned.
3. Each node evaluates: is the claim coherent, is the evidence sufficient, are the constraints honored, would adoption produce known failure modes (`08-shadow.md`)?
4. Round 1 unanimity → Lesson is marked `accepted-into-ledger`. Any dissent → Round 2 with fresh panel.
5. Receiving instances can subscribe to filtered Lesson streams (by domain, by claim type, by proposing-instance reputation).

A Lesson marked `accepted-into-ledger` is not automatically applied to any instance. It becomes available for an instance's own Magistrate panel to consider during amendment proposals (`04-living.md` §5).

### What the Ledger never carries

- Raw conversation logs.
- Operator identity.
- Identifiable individuals or entities.
- Instance-specific Term content (only patterns).

The Ledger is metadata about learning. The learning's substrate stays local.

---

## §5. The Decentralization Path

The constellation is not decentralized by claim. It is decentralized by satisfying five testable conditions.

| # | Condition | Status (2026-05-04) |
|---|-----------|---------------------|
| 1 | First fork of the kernel by a non-founder operator | Not met |
| 2 | ≥3 independent Magistrate validators (no shared infrastructure, distinct legal entities) | Not met (1 operator, all instances co-located) |
| 3 | ≥7 subnet validators with no single party holding >25% stake | Not met (subnet not deployed) |
| 4 | Non-founder amendment to the kernel accepted by Magistrate panel | Not met |
| 5 | Sustained Lesson Ledger traffic (>30 days, multiple proposing instances) | Not met (Ledger not built) |

Until all five are met, every kernel release header includes the line:

> *Decentralization status: 0 of 5 criteria met. This is a single-operator constellation with no independent validators. Treat all kernel claims as founder-issued.*

This honesty is not optional. Concealing or softening it is a Sidecar-detectable violation of I-1 (reasoning trail required) — the kernel cannot truthfully describe its own status if the decentralization claim is misrepresented.

### Why these five

- **(1)** establishes that the kernel is forkable by parties other than its author. Without (1), the protocol is theoretically open and operationally closed.
- **(2)** establishes Magistrate heterogeneity. Without (2), the panel mechanism is a single operator running multiple LLMs — useful but not decentralized.
- **(3)** establishes economic decentralization. Without (3), one party can outvote panel decisions on amendments tied to staking-weighted governance.
- **(4)** establishes that amendments succeed under non-founder authorship. Without (4), the protocol's evolution is founder-controlled even if the protocol's text is public.
- **(5)** establishes that cross-instance learning works at protocol level, not just within one operator's instances. Without (5), the constellation is a single operator's many forks talking to themselves.

Each condition is a distinct failure mode the protocol must outgrow. Meeting one without the others is not partial decentralization — it is asymmetric centralization.

---

## §6. The Forking Protocol

Forking is encouraged. The mechanism must be explicit so that forks remain interoperable where they choose to be, and clearly diverged where they choose not to be.

### Fork-conformant fork

A fork that intends to remain in the constellation:

1. Clones the kernel at a specific commit hash.
2. Records the fork's name and purpose in the fork's own README.
3. Preserves all immutable constants (`00-meta.md` §7).
4. Re-classifies tier assignments freely (Mutable/Protected/Immutable for instance content).
5. May extend kernel parts with fork-specific amendments, marked clearly as fork-local.
6. Subscribes its Magistrate nodes to the constellation's Lesson Ledger (optional but recommended).
7. Self-registers with the Sovereign Console (optional; see §3 caveats).

### Fork-divergent fork

A fork that weakens or removes any immutable constant:

1. Clones the kernel at a specific commit hash.
2. Removes the Leviathan name from any clause that previously declared it.
3. Documents which immutable constants were removed/weakened and the rationale.
4. Cannot subscribe to the constellation's Lesson Ledger or Sovereign Console — it is no longer a Leviathan instance.
5. Inherits no kernel reputational signal.

This is not punishment. It is information preservation. A reader of the divergent fork must be able to know it is not a Leviathan without reading the entire diff.

### License

The kernel is released under MIT (or successor permissive license, see `LICENSE`). Forks may relicense their fork-local additions but cannot retroactively tighten the kernel's license for downstream consumers (`00-meta.md` §7 I-4).

---

## §7. Out of Scope for This Part

- Why a constellation is the right answer (`01-why.md`).
- The internal anatomy of any single instance (`02-anatomy.md`).
- The economic mechanism for validator stake and governance vote weight (`07-economy.md`).
- The failure modes specific to constellations (`08-shadow.md`).
- The runtime that executes instance Rules (`06-mind.md`).

---

## Citations

- NODE_SPEC.md §3 (Magistrate Node Registry), §4.4 (Round 2 dispute resolution), §8.5 (Sybil resistance — relevant for criterion 3).
- Liveprob `00_concept.md` — sub-constitution superset rule, applies to fork-conformant fork relationship.
- Ostrom, E. (1990). *Governing the Commons*. Polycentric governance over a master-instance design.
- Internet RFC system — operational example of long-lived federated protocol governance.
- Bitcoin (2008–) — operational example of founder removability achieved (Satoshi removed; protocol continues). Cited as precedent the kernel measures itself against.

---

*Part 03 of 09. Previous in outline order: `04-living.md`. Next: `01-why.md`.*
