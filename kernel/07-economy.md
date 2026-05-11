# 07-economy — Economy and the Physical World

> **Part version:** 0.1.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-04
> **Scope:** the economic substrate the protocol depends on, and the physical-world stakes that distinguish a Leviathan instance from a chatbot. Out of scope: specific tokenomics numbers (those live in instance repos and evolve), legal/regulatory analysis (jurisdiction-specific, not kernel content).

---

## §1. Why a Token at All

The protocol introduces an economic substrate (denoted `$LVTN` in the founder's reference instance; the name is implementation-tier, not kernel-tier) for three reasons. None of them is "speculation" or "fundraise."

### §1.1. Sybil resistance for Magistrate panels

A panel of N≥3 heterogeneous nodes (`I-2`) is structurally meaningless if a single party can run all N nodes. NODE_SPEC.md §8.5 establishes economic Sybil resistance: each Magistrate node requires a non-trivial stake. If the same operator runs five nodes, they put up 5× the stake — and slashing applies per-node, so correlated misbehavior multiplies losses. The token is the substrate stake is denominated in.

Without economic Sybil resistance, the Magistrate panel mechanism collapses to operator-of-many-nodes-pretending-to-be-many-operators. No alternative substrate (proof-of-work, proof-of-personhood, biometric uniqueness) is operationally available with the maturity Sybil resistance requires today.

### §1.2. Governance vote weight

When a kernel amendment is proposed (`00-meta.md` §4), the panel that reviews it is itself drawn from validators. Validator status requires stake. Vote weight in kernel-amendment Magistrate panels is bounded by stake-with-cap to prevent capture by single accumulators (`I-4` indirectly, via fork freedom: a captured kernel can be forked).

### §1.3. Lesson Ledger access cost

Submitting a Lesson to the Ledger (`03-constellation.md` §4) carries a small cost denominated in the token. This is anti-spam: the Ledger must not become a firehose of low-quality proposals diluting Magistrate panel attention. The cost is refunded if the Lesson is accepted by panel review, and forfeited if rejected as low-quality. This produces a quality signal: a proposer who frequently has Lessons rejected pays repeatedly; a proposer whose Lessons are accepted pays nothing in net.

---

## §2. What the Token Must Not Do

Token mechanisms readily distort the protocol they exist to support. The kernel constrains what an instance's tokenomics may do.

### §2.1. No founder lock-in

A token whose founder allocation is large enough to dominate governance for years preserves the founder dependency the protocol exists to remove (`I-5`). The kernel requires:

- Founder allocation does not exceed the supermajority threshold needed to block kernel amendments. The specific percentage is implementation-tier, but the principle is immutable: **no single party — including the founder — may have unilateral veto over kernel amendments via stake-weighted voting.**
- Time-locked vesting is applied to founder and early-contributor allocations. The specific schedule is implementation-tier, but the principle is that early allocations cannot be deployed in governance during the period when the constellation is youngest and most vulnerable to capture.
- Validator stake is independent of founder allocation. The set of parties who can run Magistrate nodes overlaps with but is not contained within the set of early allocation recipients.

### §2.2. No data-extraction primitive

The token does not gate access to instance data. An instance's Companion conversations, POS contents, session logs are not "purchasable" via token. `I-6` (instance data sovereignty) cannot be circumvented by a tokenomics design that creates a market in operator data. This is an immutable architectural constraint, not a tokenomics parameter.

### §2.3. No license-tightening leverage

The kernel's license cannot be retroactively tightened (`I-4`). A tokenomics design that effectively tightens the license — e.g., requiring token holdings for access to "official" forks while operating Sybil-prohibitive cost barriers on independent forks — violates the spirit of `I-4` even when the letter of the license is preserved. The Sovereign Console requirement (`03-constellation.md` §3.5) that no Console may claim authoritative status applies analogously to tokenomics: no token-gated artifact may claim canonical status over publicly-available kernel content.

### §2.4. No kernel-fee extraction

A founder cannot impose a perpetual fee on kernel use. Forks pay no royalty to the kernel maintainers. Instances pay no recurring fee to the kernel. Validator rewards flow from the operations validators perform (verdicts settled, Lessons reviewed), not from a tax on existence. This is implicit in the MIT-tier license requirement (`I-4`) and is stated here so token designers cannot route around it via "service fees."

---

## §3. Validator Slashing as Constitutional Enforcement

Slashing — the reduction of a validator's stake as a penalty — is the operational mechanism by which constitutional violations at the Magistrate layer are punished. NODE_SPEC.md §10 specifies the slashing conditions for the reference Magistrate Node:

| Offense | Penalty | Triggered by |
|---------|---------|--------------|
| Missed deadline | reliability decrement | automatic, on-chain |
| Lazy evaluation | progressive (warning → suspension → 10% slash) | pattern detection |
| Unapproved model | 10% slash + suspension | model attestation mismatch |
| Proven collusion | 50% slash + permanent ban | governance proposal |
| Honest dissent | **no penalty** | n/a — protected by `I-3` |

The honest-dissent exemption is structurally important. A slashing schedule that punished dissent would produce panels that converge on majority opinion to avoid penalty — exactly the monoculture failure `I-2` is designed to prevent. The economic substrate must reinforce the constitutional invariants, not erode them.

---

## §4. The Next-Gen Company Hypothesis

This section articulates a hypothesis the protocol enables but does not require. Treat as forward-looking, not load-bearing on `01-05`.

A traditional company is a legal entity that owns assets, employs humans, and produces outputs through human labor. Its governance is corporate-board structured; its accountability is to shareholders.

The protocol enables a different organizational form:

```
TRADITIONAL COMPANY:        legal entity + employees + assets
                            governance: board of directors
                            accountability: shareholders

LEVIATHAN-NATIVE ORGANIZATION:   constitutional substrate + agent fleet + token
                                 governance: Magistrate panel + Sovereign(s)
                                 accountability: validators + token holders + auditable history
```

**Why this is hypothesis, not claim:** no Leviathan-native organization currently exists. Reference instances (Companion, Liveprob, Security Leviathan) are infrastructure, not organizations producing market outputs. Tasma (a smart-collar IoT venture) is an existing legal-entity company that may eventually instantiate parts of itself as Leviathan instances; the migration has not occurred.

**What the hypothesis predicts:** a Leviathan-native organization should be cheaper to coordinate (governance is in the substrate), more auditable (every action has a Sidecar verdict and reasoning artifact), more forkable (anyone disagreeing with direction can fork the constitution rather than dissent within a corporate hierarchy), and more founder-removable (the protocol's Founder Independence Criterion applies at organization scale too).

**What the hypothesis does not claim:** Leviathan-native organizations are universally superior to traditional companies. The hypothesis is testable only by existence proofs — a Leviathan-native organization that operates for ≥1 year and produces measurable output would constitute supportive evidence; an attempt that fails would constitute disconfirmation of the form, not the protocol.

This hypothesis lives in the kernel because tokenomics design choices made today shape whether the form is feasible later. A token that gates kernel access defeats the form. A token that funds heterogeneous Magistrate panels enables it.

---

## §5. Physical-World Stakes

A Leviathan instance whose actions stay inside text — generating responses, updating documents, evaluating proposals — has bounded blast radius. Constitutional violations produce wrong text, which can be retracted.

A Leviathan instance whose actions reach into the physical world has unbounded blast radius. Constitutional violations can produce harm that cannot be retracted. This raises the operational bar for the Sidecar, the Magistrate panel, and the Sovereign override.

### §5.1. Reference instances with physical-world reach

| Instance | Physical-world surface | Bounded by |
|----------|------------------------|------------|
| Tasma (smart collar) | IoT hardware on living animals; pattern detection of harmful pet-food signatures | Sidecar gates collar state changes; Sovereign (operator) approves elevated actions |
| Atlas (digital twin) | uiautomator2-controlled phone; can interact with apps, send messages, make purchases | Sidecar gates "irreversible" tier actions; Sovereign approval required for outside-of-routine actions |
| Liveprob (financial) | Trade execution against real markets via approved exchanges | Sidecar enforces leverage/position-size rules; Magistrate panel reviews novel instruments |
| Security Leviathan | Code commits to repositories that may control physical systems downstream | n=1 single-node panel currently — flagged as gap (`05-evidence.md` §4) |

### §5.2. The elevated bar

For instances that touch the physical world, three protocol provisions tighten:

- **Action irreversibility tagging.** Every primitive in the dictionary (`06-mind.md` §2.2) declares whether its effect is reversible. Irreversible actions require Sovereign approval at action time, not just constitutional pre-approval. This is implementation-tier specification but the principle is kernel: irreversibility must be visible to the Sidecar.
- **Multi-node Magistrate for novel actions.** A Sidecar evaluating a routine action consults the active rule set in milliseconds. A Sidecar evaluating an action with no precedent in the rule set escalates to a Magistrate panel before execution. Physical-world instances cannot reduce this to a single-node decision (per `I-2`).
- **Hardware-sandboxed primitives.** Primitives that touch physical hardware (motor commands, IoT state changes, financial transactions over a threshold) must run in TEE-attested or hardware-isolated executors when operationally available. The kernel does not require specific hardware; it requires that the executor's trust boundary match the action's blast radius.

### §5.3. Why the kernel cares

If the protocol's text-only instances succeed and its physical-world instances fail, the protocol is not generally useful. The kernel must hold to the same constitutional discipline at both scales. Physical-world stakes are not an "advanced topic" for a separate document — they are the test that the protocol either passes or fails as a real-world governance substrate.

---

## §6. Out of Scope for This Part

- Specific tokenomics numbers (allocations, vesting periods, slashing percentages) — these live in instance repos and evolve.
- Jurisdiction-specific legal and regulatory analysis — kernel-neutral.
- Specific physical-world hardware integrations — instance-level.
- Comparison to specific cryptoeconomic systems (Ethereum, Avalanche substrate-specific) beyond the precedents already cited.

---

## Citations

- NODE_SPEC.md (`../specs/NODE_SPEC.md`) §8.5 (Sybil resistance), §10 (Slashing schedule).
- Liveprob `00_concept.md` — primitive irreversibility tagging origin.
- Bitcoin (2008–) — operational example of token-as-Sybil-resistance over a decadal horizon.
- Avalanche subnet architecture — implementation-tier substrate the reference instance targets.
- Ostrom, E. (1990). *Governing the Commons*. Polycentric governance with explicit cost-of-defection — applies to slashing as constitutional enforcement.

---

*Part 07 of 09. Previous in outline order: `06-mind.md`. Next: `08-shadow.md`.*
