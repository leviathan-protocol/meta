# 04-living — The Living Organism

> **Part version:** 0.2.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-04
> **Scope:** how an instance's constitution evolves over time. The kernel doc is one example; this part describes the general mechanism.

---

## §1. Why "Living"

A Leviathan instance is not a contract executed once. It is a constitution that must remain valid across years of operation in a world that changes. Three properties make it living:

1. **Every element has versions.** Terms, Principles, Rules, even Shadows.
2. **Every change has a trigger and a record.** Amendments are caused, not arbitrary.
3. **Untouched stable elements decay.** Silence becomes a signal that review is overdue.

This is not metaphor. It is the operating mode by which the protocol intends to outlive its founders, its first instances, and its first decade.

---

## §2. Versioning Everywhere

Every constitutional element carries a version. Every version carries a date and a trigger. Every trigger is an event the instance can point to: a breakthrough, a breakage, an external development, a periodic review.

```yaml
# Example: a Companion Term across versions
id: kavram:yalnizlik
versions:
  - v: 1.0
    date: "2022-Q3"
    statement: "Running your own server = strength."
    trigger: "isolation as productivity hypothesis"
  - v: 1.1
    date: "2026-01-15"
    statement: "Strength, but with a 30% energy cost."
    trigger: "session 014 — burnout pattern observed"
  - v: 2.0
    date: "2026-01-28"
    statement: "Isolation is preference, not strength — and the cost is high."
    trigger: "session 023 — confronted by Magistrate-equivalent dialogue"
  - v: 2.1
    date: "2026-03-12"
    statement: "Loneliness can be chosen, but the right-frequency people must be sought."
    trigger: "post-relocation isolation became actionable problem"
```

What this records is not a journal. It is a constitutional history: the term's authoritative meaning at each point in time, with the cause of each change.

The cost of versioning is real (~3–5 minutes per amendment to write the trigger and version-bump the dependents). The benefit is auditability: any future Magistrate panel evaluating an instance can answer the question *"what did this term mean when this rule was written?"* without speculation.

**Shadows are versioned.** A Shadow (a known unresolved pattern an instance is monitoring) has versions because the operator's relationship to it changes. Demoting a Shadow from `intensity: 70` to `intensity: 45` is a constitutional event, not a private feeling. It changes which actions the Sidecar treats as elevated-risk.

---

## §3. The Tier System (Applied to Instance Content)

The same three-tier classification used for the kernel itself (`00-meta.md` §2) applies recursively to every constitutional element in every instance.

| Tier | What Goes Here | Amendment Requirement |
|------|----------------|----------------------|
| **Immutable** | Identity-defining clauses. Removing them would make this a different instance, not an evolved one. | Cannot be amended; only forked. |
| **Protected** | Operationally important. Mature Terms, established Principles, load-bearing Rules. | Magistrate panel, Round 1 unanimity or Round 2 supermajority. |
| **Mutable** | Working content. Recent rules, evolving terms, ad-hoc protocols. | Operator commit + changelog entry. |

Tier assignment is itself a constitutional decision. Promoting a Mutable rule to Protected is an amendment — it requires panel review because it changes the rule's amendability going forward.

### Worked Example: Companion Tier Assignments

| Element | Tier | Rationale |
|---------|------|-----------|
| `kavram:caba-yasasi` (Çaba Yasası) | Immutable | Renaming this instance "Companion" would not survive removal of this Term. |
| `prensip:durustluk` v1.1 | Protected | Load-bearing principle; changes ripple through 12+ rules. |
| `protokol:transit-server` | Mutable | Situational, ad-hoc, may be deprecated once the relevant life phase passes. |
| `golge:ustunluk-yanilsamasi` | Protected | Demoting this Shadow's intensity affects multiple Sidecar evaluations. |

A new instance forking the Companion template is not bound to these tier assignments. The fork inherits the suggestions and re-classifies based on what is identity-defining for that operator.

---

## §4. Approved Model Registry — A Worked Example

A concrete instantiation of the tier system already exists in the protocol: the Approved Model Registry (NODE_SPEC.md §3).

```
APPROVED MODEL REGISTRY
│
├── IMMUTABLE: the registry's existence and approval threshold rules
│   └── A Magistrate panel cannot operate without an active registry.
│       Removing the registry produces a fork, not an amendment.
│
├── PROTECTED: the LVB benchmark thresholds
│   ├── reasoning coherence ≥ 85%
│   ├── instruction following ≥ 90%
│   ├── adversarial robustness ≥ 80%
│   ├── consistency ≥ 75%
│   └── latency < 120s
│       └── Lowering any threshold weakens panel quality. Requires panel review.
│
└── MUTABLE: the list of approved model hashes
    ├── Qwen3-30B-A3B, Qwen3-32B, Llama-3.3-70B, Mistral-Small-24B, DeepSeek-R1-Distill-32B
    └── New models added via CoreGovernor STANDARD proposal (NODE_SPEC.md §3).
        The list rotates as models improve; the criteria persist.
```

This is the pattern: the **structure** of governance is high-tier, the **content** governed by the structure can be low-tier. The constitution does not need to choose between stability and adaptability; it stratifies them.

---

## §5. Evolution Mechanism

Every amendment, regardless of tier, follows the same five-stage shape:

```
TRIGGER → PROPOSAL → REVIEW → VERSION BUMP → CHANGELOG
```

### §5.1. Trigger Categories

Amendments are caused. The protocol recognizes five trigger categories:

| Category | Source | Example |
|----------|--------|---------|
| Breakthrough | Internal — operator/instance reaches new understanding | Companion `kavram:yalnizlik` v2.0 (isolation reframed) |
| Breakage | Internal — existing rule produced wrong outcome | Liveprob primitive registry rejects a primitive that should have passed |
| External | Outside event the instance must respond to | New approved model published with better LVB scores |
| Periodic review | Time-based — `00-meta.md` §5 cadence | 90 days untouched, maintainer must reaffirm or amend |
| Escalation | A Sidecar evaluation produced ambiguity that recurred | Sub-constitution rule conflicts with parent in 3+ cases |

A proposal must declare its trigger category. Proposals without a stated trigger are rejected at Round 1 — the Magistrate panel cannot evaluate intent without it.

### §5.2. Proposal Format

A proposal is a structured document, not free text. Minimum fields (see `00-meta.md` §4 for the kernel-specific instantiation):

- Element(s) affected and their current versions.
- Proposed new content.
- Trigger category and the specific event(s) cited.
- Tier impact: does this proposal touch any Immutable clauses? Does it change any element's tier?
- Dependents: which other elements depend on this one (from the `depends` chain in `02-anatomy.md` §3).
- Magistrate panel composition for review.

### §5.3. Review

Tier-dependent (see `§3` above and `00-meta.md` §4.3). Mutable changes are committed by the operator with no panel. Protected changes go through Magistrate Round 1; dissent triggers Round 2. Immutable clauses are not subject to review because they cannot be amended — only forked.

### §5.4. Version Bump

```
MAJOR — backward-incompatible meaning change
MINOR — additive change (new clause, new evidence)
PATCH — clarifying edits, typos, link fixes
```

A Term whose definition changed in a way that would invalidate prior reasoning under the old definition gets a MAJOR bump. Adding a clarifying example is MINOR. Fixing a typo is PATCH.

### §5.5. Changelog Entry

The amendment is not complete until the entry is committed:

```yaml
- date: "2026-03-12"
  element: kavram:yalnizlik
  version: 2.0 → 2.1
  trigger:
    category: breakthrough
    event: "post-relocation isolation became actionable problem"
    session_ref: chunk-345
  panel: ["operator", "llm-claude-opus-4-7", "llm-gpt-5-pro"]
  reasoning_artifacts: ["_drafts/amendments/yalnizlik-v2.1/reasoning-*.md"]
  approved: true
```

The changelog is append-only (`00-meta.md` §7 I-7). Errors are corrected by new entries that supersede the old; old entries are never edited or deleted.

---

## §6. The Decay Mechanism

The decay cadence is operational-mode-dependent. The protocol distinguishes two modes:

### §6.1. Build phase (current)

A constellation in build phase has 0–4 of the 5 Decentralization Path criteria met (`03-constellation.md` §5). Time horizons are compressed: every commit to a kernel part or implementation spec triggers a conformance check (`tools/conformance.py`) against the 7 immutable invariants (`00-meta.md` §7). A commit that fails conformance does not merge. There is no 90-day grace period in build phase — drift detected at commit-time is drift fixed at commit-time.

The build-phase cadence is operationalized by the pre-commit hook in `tools/pre-commit.sh`. The cadence applies to:

- All kernel parts (`kernel/*.md`).
- All implementation specs (`specs/*.md`).
- The CHANGELOG (every commit touching kernel or specs requires a CHANGELOG entry).

Instance-level constitutional elements (a Companion's `kavramlar/`, a Liveprob's primitive registry) follow the steady-state cadence below — build-phase intensity applies to the kernel and its specs, not to the operator's day-to-day instance content.

### §6.2. Steady state

Once all 5 Decentralization Path criteria are met, the cadence relaxes. Stable elements that go untouched for 90 days are auto-flagged `stale`. A stale element has these properties:

1. It still applies — the Sidecar continues to enforce stale Rules.
2. It cannot be cited as authoritative justification for a new amendment.
3. It must be **reaffirmed** or **amended** before the citation block is unlocked.

```yaml
# Reaffirmation example (no content change, just review):
status: stable
last_touched: "2026-05-04"
reaffirmed: "2026-08-02"
reaffirmed_by: "operator"
note: "Reviewed in light of post-NYC stabilization; no change required."
```

The 90-day window is a steady-state default. Instances may set tighter cadences in their own meta-rules; they may not set looser ones — the cadence is a floor, not a ceiling.

### §6.3. Why two cadences

A protocol that uses the same cadence in build phase and steady state is calibrated for one of them and wrong for the other. Build phase requires per-commit detection because everything is moving — the kernel itself is in flux, specs are being adapted to it, instances are testing the substrate. Steady state requires periodic review because the system is settled and constant per-commit overhead would be theatrical.

The transition trigger is operational, not arbitrary: the 5 Decentralization Path criteria. Until they are met, build phase. Once met, the kernel maintainers record the transition in `CHANGELOG.md` and the pre-commit hook is replaced by a 90-day review job.

### §6.4. Why decay at all

This mechanism prevents the failure mode where a constitution silently diverges from the operator's actual practice. If `prensip:durustluk` (honesty) has not been touched in a year, but the operator has been making honesty-related decisions weekly, something is wrong: either the principle is so internalized it does not need amendment, or it has quietly drifted from how the operator actually behaves. Reaffirmation forces the question.

A constitution where most elements are stale is a dead constitution — even if the Sidecar is still firing.

---

## §7. Frozen Constitution = Dead Constitution

A constitution that cannot or does not change is structurally unable to govern anything but its founding moment.

**Empirical observations the protocol draws from:**

- **GDPR (2016).** Drafted before the LLM era. Its core articles have not been amended despite the obvious mismatch between its consent-and-data-minimization frame and how generative systems actually train. Application to AI is now done through interpretive guidance (which is not the constitution amending itself; it is the courts approximating an amendment the legislators did not perform). The result: regulatory friction without regulatory clarity.

- **Internet RFCs.** Opposite design. RFCs are explicitly superseded — RFC 822 became 2822 became 5322. The mechanism for amendment is the protocol itself. The result: the email standard has remained operationally relevant across five decades of context shift.

- **Cargo-cult organizational policies.** Policies whose original justification is forgotten but whose enforcement persists. The Sidecar still fires; no one can defend the rule under panel review. Without a decay mechanism, this is the equilibrium.

The protocol's bet: a constitution that costs ~3–5 minutes per amendment to maintain, and forces a 90-day review on every stable element, is cheaper than the cost of cargo-cult enforcement and regulatory drift over years.

---

## §8. Self-Reference

This document — the Leviathan Kernel — applies §1–§7 to itself.

- Every part has a version, tier, status, and `last touched` date in its front matter.
- Amendments to any part follow `00-meta.md` §4.
- The kernel maintains its own `CHANGELOG.md`.
- Stale parts are flagged and unable to be cited until reaffirmed.

The kernel is not exempt from the rules it requires of instances. If a kernel maintainer cannot perform the discipline this part describes, the kernel itself becomes unfit to govern.

This recursive property — the constitution governing its own evolution by the same rules it imposes on what it governs — is what distinguishes a Leviathan from a static specification document.

---

## §9. Out of Scope for This Part

- Cross-instance Lesson transfer (`03-constellation.md`).
- The structural anatomy that is being versioned (`02-anatomy.md`).
- The kernel's own meta-rules (`00-meta.md`).
- Empirical observations of evolution over n=4 instances (`05-evidence.md`).

---

## Citations

- NODE_SPEC.md §3 — Approved Model Registry as worked tier example.
- Liveprob `00_concept.md` — origin of immutable/protected/mutable trichotomy.
- Companion `openpos/my-pos/changelog.yaml` + `kavramlar/yalnizlik.yaml` — empirical evidence of multi-version Term evolution.
- Postel, J. (1982). RFC 822, superseded by RFC 2822 (2001), superseded by RFC 5322 (2008). Operational example of a long-lived protocol that amends itself.
- EU GDPR (2016). Operational example of a constitution that cannot amend itself across a context shift.
- North, D. (1990). *Institutions, Institutional Change and Economic Performance*. Long-term institutional viability requires explicit, low-cost amendment mechanisms.

---

*Part 04 of 09. Previous in outline order: `02-anatomy.md`. Next: `03-constellation.md`.*
