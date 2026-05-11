# 00-meta — How This Document Evolves

> **Part version:** 0.1.0 · **Status:** draft · **Last touched:** 2026-05-04
> **Doctrine:** This document is itself a Leviathan instance. It applies the protocol it describes to its own evolution. A frozen kernel is a dead kernel.

---

## §1. What This Document Is

The Leviathan Kernel is a constitutional substrate, not a fixed artifact. It defines:

- A four-layer structure (terms, principles, rules, meta-rules) that any compatible instance inherits.
- The minimum invariants every fork must preserve to remain a Leviathan.
- The mechanism by which the kernel itself changes.

It is **not** an implementation specification. Reference implementations (Companion, Liveprob, Mind, Magistrate Node) live alongside and may evolve faster than the kernel. The kernel describes what they must satisfy, not how they must be built.

This document is published under the same constitutional discipline it requires of the instances that fork it. Changes to the kernel follow the same amendment procedure (§4) that a Liveprob node would follow when revising its trading constitution. The kernel is recursive in this respect: it governs itself.

---

## §2. Layered Structure of the Kernel Itself

Every kernel part is classified into one of three tiers, drawn from the Liveprob primitive registry pattern (`/Users/aigent/caba_yasasi/00_concept.md`) and the Approved Model Registry tier system (NODE_SPEC.md §3).

| Tier | Meaning | Amendment Threshold |
|------|---------|---------------------|
| **Immutable** | Removing or weakening this clause makes the document no longer a Leviathan kernel. Forking is permitted; weakening is not. | None. A fork that weakens an immutable clause is a different protocol. |
| **Protected** | Substantive content. May change with deliberation. | Magistrate panel of ≥3 independent operators (different kernel forks count as different operators) returns supermajority APPROVE on the amendment proposal. |
| **Mutable** | Working content, framing, evidence, examples. | Single maintainer commit + entry in `CHANGELOG.md`. |

Each part declares its tier in its front matter. This `00-meta.md` is itself **Protected** except for §7 (immutable list) which is **Immutable**.

---

## §3. Versioning

Per-part semantic versioning. Document-wide version is computed, not declared.

```
PART VERSION: MAJOR.MINOR.PATCH
  MAJOR — backward-incompatible meaning change (e.g., redefining Magistrate)
  MINOR — additive change (new evidence, new clause)
  PATCH — clarifying edits, typos, link fixes
```

**Front matter requirements** (every part):

```
Part version: X.Y.Z
Tier: immutable | protected | mutable
Status: draft | stable | deprecated
Last touched: YYYY-MM-DD
```

A part with `status: stable` and no `last touched` change in 90 days triggers the mandatory review (§5).

---

## §4. Amendment Procedure

```
PROPOSE → MAGISTRATE EVALUATION → SETTLE → APPLY
```

### Step 1 — Propose

Open a pull request to the kernel repository. The PR description must contain:

1. The exact part(s) and lines affected.
2. The proposed new wording.
3. **Rationale** — what triggered this amendment. Cite empirical evidence where applicable (instance behavior, breakage, external development).
4. **Tier check** — confirmation that no clauses in `§7` (Immutable Constants) are weakened. If an immutable clause is the target, the PR must be marked as a fork-divergence proposal (§4.5), not an amendment.
5. **Magistrate panel** — list of at least three independent operators (or LLMs, see §4.3) who will review. Self-evaluation does not count.

### Step 2 — Magistrate Evaluation (Round 1)

Each panel member produces a **reasoning document** (NODE_SPEC.md §6 format, abbreviated) addressing:

- Does the proposal preserve all immutable constants?
- Is the rationale evidence-supported?
- Does the change introduce inconsistency with other kernel parts?
- Verdict: APPROVE / REJECT / ESCALATE.

Reasoning documents are stored under `levi/kernel/_drafts/amendments/{pr-id}/` and committed alongside the merge. They are not deleted after settlement — they constitute the kernel's audit trail.

### Step 3 — Settlement

| Tier | Round 1 Threshold | On Failure |
|------|-------------------|------------|
| Mutable | Maintainer accepts, no panel required | — |
| Protected | Unanimous APPROVE among ≥3 panel members | Escalate to Round 2 (5 new reviewers, 6/7 supermajority — NODE_SPEC.md §4.4) |
| Immutable | Cannot be amended; can only be diverged from via fork (§4.5) | — |

### Step 4 — Apply

On settlement, the maintainer commits the change, bumps the part version, and records the entry in `CHANGELOG.md` with the panel composition and reasoning hashes (filenames or content addresses if IPFS-pinned).

### §4.3. On Panel Composition

A panel member is one of:

- An independent human operator running a Leviathan instance.
- An LLM operated by a non-author of the proposal.

This formalizes a practice that has been informal: testing kernel proposals across multiple LLMs is **the Magistrate pattern operating manually**. The kernel acknowledges this as a legitimate panel mode at small N. As the constellation grows (Decentralization Path criteria 1–5, defined in `03-constellation.md`), human-operator panels become the norm and LLM-only panels are deprecated.

### §4.5. Fork Divergence

A fork that wishes to weaken or remove an immutable clause does not amend the kernel — it forks. The forked document must:

1. Remove the Leviathan name from any clause that previously declared it.
2. Cite the kernel commit hash from which it diverged.
3. Document the diverged clause(s) and rationale.

Forking is encouraged when justified. Misrepresentation is not.

---

## §5. Review Cadence

Every part with `status: stable` must be touched by a maintainer within 90 days of its `last touched` date. Touching means one of:

- A minor or patch amendment.
- An explicit `Reaffirmed: YYYY-MM-DD` line added to the part front matter, indicating review without change.

Untouched stable parts are auto-flagged `status: stale` after 90 days. Stale parts cannot be cited as authoritative in new amendment proposals until reaffirmed.

This cadence prevents the failure mode that this document was written to avoid: a kernel that ossifies, then quietly diverges from the instances it claims to govern.

---

## §6. Self-Reference

This part — `00-meta.md` — evolves under its own rules.

A change to §3 (Versioning) requires a Round 1 Magistrate panel because the part is Protected. A change to §7 (Immutable Constants below) is structurally impossible: it can only be forked.

The recursive question — *can the amendment procedure itself be amended?* — is answered: yes, via §4 procedure on §4 itself, except for the immutable invariant that **all amendments must produce a written, panel-reviewed reasoning trail**. That invariant is in §7.

---

## §7. Immutable Constants

The following are the kernel's hard constraints. Removing or weakening any of these produces a fork, not an amendment (§4.5). The list itself is immutable; new immutable constants may be added by Protected procedure but existing ones cannot be removed.

I-1. **Reasoning trail required.** Every amendment to any kernel part must produce a written reasoning document, panel-reviewed, retained for audit.

I-2. **Heterogeneous evaluation.** No constitutional verdict (kernel amendment, instance Lesson acceptance, sub-constitution change, primitive promotion) may be settled by a single LLM or single operator. Panels are heterogeneous by construction.

I-3. **Dissent is protected.** A panel member who disagrees with a settled outcome receives no penalty for the disagreement, provided their reasoning was substantive. Dissent triggers deeper review; deeper review is the system working correctly.

I-4. **Fork freedom.** Any party may fork the kernel at any commit. The original maintainers cannot revoke fork rights. License (MIT or successor) cannot be tightened retroactively.

I-5. **Founder removability.** The kernel is not declared decentralized until the Founder Independence Criterion is met (defined in `03-constellation.md`). Until then, every release acknowledges this gap. The criterion itself can be tightened but not loosened.

I-6. **Instance data sovereignty.** A Leviathan instance's local data (memory, POS, conversation logs) belongs to the instance operator. The kernel never specifies a mechanism that would extract this data without explicit operator action.

I-7. **No retroactive amendment.** A panel decision, once settled and recorded in `CHANGELOG.md`, cannot be erased. It can be superseded by a new amendment, but the historical record persists.

---

## Citations

- NODE_SPEC.md §3 (Approved Model Registry), §4.4 (Round 2 procedure), §6 (Reasoning Document Format), §10 (Dissent protected).
- Liveprob `00_concept.md` (tier system: immutable / protected / mutable; primitive registry).
- Karpathy, A. (2025). *Software 3.0*. Frame for why kernel must remain editable: code-as-English implies governance-as-text.
- Ostrom, E. (1990). *Governing the Commons*. Polycentric governance with explicit amendment procedures outperforms top-down rule-setting in long-lived institutions.
- Hobbes, T. (1651). *Leviathan*. Source name. Note: Hobbes's sovereign was indivisible; this kernel's Sovereign is per-instance, divisible by fork — explicit doctrinal departure.

---

*Part 00 of 09. Next part: `01-why.md`.*
