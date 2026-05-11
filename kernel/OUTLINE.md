# Leviathan Kernel — Document Outline

> **Part version:** 0.1.0 · **Tier:** meta · **Status:** structural skeleton, not content. Approve structure first, then we expand part-by-part. **Last touched:** 2026-05-04
> Target: 30–40 pages total, distributed across files (no monolith).
> Doctrine: this document IS a Leviathan instance. It practices what it describes — versioned, forkable, living.

---

## Terminology Decisions (Locked)

- **Mind** — primitive registry + binary executor + skill synthesis runtime. Replaces all prior names ("Forge", "Foundry", "Atelier", "Constitutional Forge"). Motto: *"Model thinks, VM does."*
- **Kernel** — the abstract protocol described in this document. Forkable, instance-agnostic.
- **Instance** — a concrete Leviathan (Companion, Liveprob, Security, Tasma, etc.).
- **Constellation** — the federation of instances sharing kernel + Console + Lesson Ledger.
- **Sovereign** — the human operator with override authority for a given instance.
- **Sidecar** — runtime evaluator enforcing the constitution at action time.
- **Magistrate** — async reviewer/auditor (separate process, separate model).

If a future LLM proposes an alternative name, reject and link them here.

---

## File Structure

```
levi/kernel/
├── README.md          ← 1-page entry: what this is, how to read, fork instructions
├── OUTLINE.md         ← this file — structural decisions + open questions
├── 00-meta.md         ← how this doc evolves (meta-rules in action)
├── 01-why.md          ← capture window, alternatives critique
├── 02-anatomy.md      ← 4-layer + Trinity
├── 03-constellation.md ← federated model, decentralization path
├── 04-living.md       ← versioning, tier system, evolution mechanism
├── 05-evidence.md     ← n=4 instances, limitations stated
├── 06-mind.md         ← Mind reference runtime (clearly marked optional)
├── 07-economy.md      ← $LVTN, next-gen company, physical world
├── 08-shadow.md       ← founder dependency, capture risks, what kills this
├── 09-engage.md       ← for operators / users / researchers / critics
├── glossary.md        ← terms layer (vocabulary of this doc itself)
└── CHANGELOG.md       ← every change to kernel docs, with rationale
```

Rule: **no part exceeds 5 pages**. If a part wants more, it splits. Forces pruning.

---

## Part-by-Part: Scope and Non-Scope

### `00-meta.md` — How This Document Evolves
**Covers:**
- This doc is itself a 4-layer constitution (terms, principles, rules, meta-rules).
- Versioning: every part has version + date + trigger.
- Sacred Layer (cannot change without supermajority of forking instances): Founder Independence Criterion, structural identity of POS↔Constitution, federation-not-master.
- Mutable Layer: everything else.
- How to propose changes (PR + rationale + which Sacred constraints checked).
- "Frozen kernel = dead kernel" — review cadence: every 90 days a maintainer must touch each part or mark it explicitly stable.

**Does NOT cover:** specific governance procedures (those live in 03-constellation).
**Length:** 2 pages.

### `01-why.md` — Why This Exists
**Covers:**
- Software 3.0 capture window (Karpathy frame, 24-month estimate).
- Critique: Anthropic constitutional AI, OpenAI policy, EU AI Act — what they get right, what they miss.
- Founder Independence Criterion as the test.
- POS↔Constitution structural identity claim.
- Negative claim: this is *not* an AGI alignment proposal; it's a governance substrate for current-gen agents.

**Does NOT cover:** anatomy of the protocol, implementation details.
**Length:** 4 pages.

### `02-anatomy.md` — Anatomy of a Leviathan
**Covers:**
- 4-layer constitutional substrate: Terms / Principles / Rules / Meta-Rules — with example from Companion + example from Liveprob (proof of generality).
- Trinity: Sidecar (sync, hot path) / Magistrate (async, audit path) / Sovereign (human, override path).
- Sub-constitution superset rule: specialty agent constitutions inherit + extend, never weaken.
- Honest note: trinity is currently 2-of-3 in most instances (no Magistrate yet in Companion).

**Does NOT cover:** federation, multi-instance topology.
**Length:** 5 pages.

### `03-constellation.md` — The Federated Constellation
**Covers:**
- Why federated, not master (founder independence + fork freedom + capture resistance).
- Kernel/Instance separation (this repo = kernel; instance repos own their own data).
- Sovereign Console — visibility primitive, NOT control primitive. What it can show, what it explicitly cannot do.
- Lesson Ledger — anonymized pattern transfer between instances. Schema sketch.
- Decentralization Path (5 conditions, copied verbatim from living-doc):
  1. First fork by non-founder operator.
  2. ≥3 independent validators (no shared infrastructure).
  3. ≥7 subnet validators, no single party >25% stake.
  4. Non-founder amendment to kernel accepted.
  5. Sustained Lesson Ledger traffic (>30 days, multiple instances).
- Forking protocol: how to legitimately fork the kernel.

**Does NOT cover:** token economics (07), implementation runtime (06).
**Length:** 5 pages.

### `04-living.md` — The Living Organism
**Covers:**
- Versioning everywhere (elements, principles, even shadows).
- Tier system: **immutable** / **protected** / **mutable** — what goes where, who decides.
- Constitutional evolution mechanism: trigger → proposal → review → version bump → changelog.
- Why frozen constitution = dead constitution (with one historical example: stagnant org policies).
- Self-reference: this very document follows these rules — see `CHANGELOG.md`.

**Does NOT cover:** specific governance procedures (those live in 03 + 00).
**Length:** 4 pages.

### `05-evidence.md` — Empirical Evidence
**Covers:**
- n=4 instances (Companion / Liveprob / Security Leviathan / Levi Template).
- Per-instance: scale, duration, mode (operator-only, multi-user, etc.), what worked, what broke.
- Pattern observations across instances (tier system value, sub-constitution superset value, founder dependency cost).
- **Limitations stated explicitly:** n=4, all single-operator, no control group, no cross-cultural data, no adversarial testing.
- What would falsify the protocol.

**Does NOT cover:** vision/roadmap claims about future scale.
**Length:** 5 pages.

### `06-mind.md` — Mind: Reference Runtime
**Covers:**
- ⚠ Marked clearly: **Mind is a reference implementation, not the protocol.** A Leviathan instance can run on any compatible runtime.
- Architecture: Dictionary VM + Binary Executor + LLM Orchestrator.
- Self-extension via Voyager-style skill synthesis.
- Constitutional approval pipeline for new primitives (tier filter).
- Why "Model thinks, VM does" — determinism boundary.
- Multi-LLM provider agnostic: orchestrator interchangeable.
- Open problems: skill library zehirlenmesi, primitive bloat, dictionary versioning.

**Does NOT cover:** instance-specific Mind configurations.
**Length:** 4 pages.

### `07-economy.md` — Economy and the Physical World
**Covers:**
- $LVTN as utility, not speculation: validator stake + governance vote weight + Lesson Ledger access fee.
- Anti-extraction mechanisms (no founder allocation > X%, time-locked vesting, validator slashing).
- Next-gen company hypothesis: company = constitutional substrate + agent fleet + token, not legal entity + employees.
- Physical-world stakes: which instances touch hardware (Tasma collar, Atlas device control, future Smart Collar). Why this raises the safety bar.

**Does NOT cover:** specific tokenomics numbers (those evolve, live in instance repos).
**Length:** 4 pages.

### `08-shadow.md` — Shadow Layer
**Covers:**
- Founder dependency — currently the dominant risk (Founder Independence Criterion not met).
- Tanrı Kompleksi as fuel — acknowledging the psychological driver, not denying it.
- Capture by complexity — "only the founder can read the docs" failure mode.
- Tier abuse — marking everything immutable to prevent legitimate evolution.
- Constitution as theater — having the documents but not actually enforcing them.
- Cult risk — Sovereign as guru rather than operator.

**Does NOT cover:** mitigation specifics (those live in respective parts).
**Length:** 3 pages.

### `09-engage.md` — How to Engage
**Covers:**
- For operators: how to fork, what's needed to run an instance, what sovereignty means in practice.
- For users of an instance: how to validate the operator isn't lying about constraints.
- For researchers: replication targets, what data to ask for, where the falsification points are.
- For critics: read 08-shadow first; we already know.

**Does NOT cover:** marketing.
**Length:** 3 pages.

### `glossary.md` — Terms Layer
**Covers:**
- Every term that appears with capital letter or specific meaning.
- Each term: definition + part where it's introduced + version.
- This is the constitution's own Terms layer.

**Length:** living, currently ~1 page, grows naturally.

### `CHANGELOG.md` — Meta-Rules in Action
**Covers:**
- Every modification to any kernel doc: date, part affected, version bump, trigger, who proposed, who approved.
- Format mirrors `openpos/my-pos/changelog.yaml` schema.

**Length:** grows monotonically.

---

## Open Structural Questions (Need Decision Before Expansion)

1. **Audience and tone.** Two candidates: (a) academic-paper register (peer-reviewable, citations), (b) protocol-RFC register (terse, normative, fork-friendly). I lean **(b)** — matches "living organism" thesis. Academic register implies frozen artifact. **Decision needed.**

2. **References and citations.** Karpathy talk, Ostrom, Hobbes, Voyager paper, etc. Inline links or formal bibliography file? I lean inline + a separate `references.md`. **Confirm.**

3. **Code in kernel doc.** Mind primitives, sidecar evaluator pattern — include code or pseudocode? I lean **pseudocode in kernel, real code in instance repos**. **Confirm.**

4. **English or Turkish.** Kernel doc is a public artifact for forkers worldwide. I lean **English with Turkish glossary entries where the term originated in your POS** (e.g., "Caba Yasası", "Mimar"). **Confirm.**

5. **Mind in core or appendix.** Other LLM said "C: middle path inclusion". I argued kernel-doc, not living-doc. Decision needed: in kernel doc, is `06-mind.md` a **core part** or **appendix**? I lean **appendix-tier with clear "optional implementation" framing**, because the federated constellation thesis requires that any compatible runtime works. **Confirm.**

6. **Empirical evidence — anonymization.** `05-evidence.md` references real instances including yours. Public kernel doc — do we anonymize ("Instance A: personal companion, 12+ months, n=1 operator") or name them? I lean **named, because Satoshi Mode v1.1 says framework public, person private — the *instance* can be named without naming the *operator***. **Confirm.**

7. **Versioning scheme.** Semver per-part (00-meta.md v1.2.0) or single doc-wide version (Kernel v0.7)? I lean **per-part semver** so parts evolve independently — fits living thesis. **Confirm.**

---

## Open Content Questions (Affect Multiple Parts)

A. **Mind authorship.** Is Mind your invention or external (Liveprob has primitive registry already)? This affects 06-mind framing. Currently I'd write "Mind synthesizes Liveprob's primitive-VM pattern with Voyager's skill-synthesis pattern." **Confirm or correct.**

B. **Sovereign Console — built or designed?** Living doc says "designed". Is there code? Affects 03-constellation and 05-evidence honesty.

C. **Lesson Ledger schema.** Does a draft schema exist anywhere, or is this still a sketch? Affects 03-constellation specificity.

D. **Multi-LLM strategy as protocol claim.** You're running 3-4 parallel LLM sessions. Is this incidental (just practical) or doctrinal (Multi-Perspective Reality applied to your own development)? If doctrinal, it goes in 09-engage as a recommended practice. If incidental, it doesn't enter kernel doc.

E. **Physical-world stakes — which instances really touch hardware?** Tasma is real (smart collar). Atlas is uiautomator2 (controlling phones). Anything else? Affects 07-economy specificity.

---

## What This Outline Explicitly Excludes

- Marketing claims about adoption.
- Roadmap with dates (kernel doc is timeless; instance repos own roadmaps).
- Detailed code for any instance.
- Personal POS contents (Mimar's specific shadows etc.) — those stay in instance, only structural patterns enter kernel.
- Comparison to other LLM-pasted suggestions — those go in `notes/` or are silently absorbed; kernel doc doesn't reference its own drafting process.

---

## Next Step

Approve structure (or push back on parts). Once locked, I expand part-by-part, starting with whichever you pick. Suggested order: **00-meta → 02-anatomy → 04-living → 03-constellation → 01-why → 05-evidence → 06-mind → 07-economy → 08-shadow → 09-engage**. Reasoning: build the protocol's self-description first (00, 02, 04), then the topology (03), then the framing (01), then evidence (05), then implementation appendix (06), then external dimensions (07, 08, 09).
