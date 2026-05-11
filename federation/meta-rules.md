# Federation — Meta-Rules (Layer 4)

> **Part version:** 0.1.0 · **Tier:** protected · **Last touched:** 2026-05-05  
> **Scope:** how the federation rules themselves change. Meta-rules govern terms.md, principles.md, rules.md, and this file. Without meta-rules, the federation cannot evolve safely.

---

## §1. Why Meta-Rules

Without meta-rules:

- Anyone can edit federation rules at any time
- Bad amendments can pass silently
- The federation becomes whatever the last editor wanted it to be
- Capture-by-stealth becomes possible

Meta-rules force amendments through a structured process. Slow when needed; fast when warranted.

---

## §2. Federation Amendment Procedure

### MR-1. Mutable Rules — Single Maintainer Commit

For a rule marked `mutable` (most rules in federation/rules.md):

1. Anyone with subdirectory ownership of `federation/` (currently founder) makes the edit
2. Commit message includes brief reasoning: `[master-mac] 2026-05-DD: R-X amended — [reason]`
3. CHANGELOG entry added the same commit
4. Push

No external review required. Mutable means "operational tuning, not architectural change."

### MR-2. Protected Rules — Reasoning + Acknowledgment Window

For a rule marked `protected`:

1. Founder authors amendment proposal as a briefing (`briefings/YYYY-MM-DD-federation-amendment/`)
2. Briefing includes: current rule, proposed rule, reasoning, falsification (what would refute the amendment)
3. All federation members notified (cover letter delivered to each instance)
4. **7-day acknowledgment window** — instances can object via discrepancy report
5. If no objections: founder commits the amendment with reference to the briefing
6. If objections: founder addresses (revise proposal, defer, or override with documented reasoning)
7. CHANGELOG entry references the briefing

### MR-3. Immutable Rules — Cannot Be Amended

For a rule marked `immutable`:

- Cannot be removed, weakened, or relaxed within this federation
- May be circumvented only by **forking the federation** (creating a divergent fork)
- A divergent fork is a different federation, not the same federation under new rules

This is the final guarantee that core membership terms (P-1 ownership, P-2 privacy, P-3 kernel anchor, P-8 sovereignty) are not eroded over time.

### MR-4. Adding a New Rule

To add a rule (vs amending existing):

1. Determine target tier (mutable / protected / immutable)
2. Mutable: single-commit add per MR-1
3. Protected: briefing + 7-day window per MR-2
4. Immutable: requires unanimous federation member acknowledgment + founder declaration that this is a new immutable. Rare. New immutables should be added at most 1-2 per year (kernel/08-shadow.md tier abuse pattern).

### MR-5. Removing a Rule

To remove a rule:

1. Mutable: single-commit remove + CHANGELOG entry explaining why
2. Protected: briefing + 7-day window + reasoning. Removal is a substantive change.
3. Immutable: cannot be removed within this federation. Fork-divergence required.

---

## §3. Decay & Reaffirmation

### MR-6. 90-Day Review Cadence

Every rule and principle has a `last_touched` date (in front matter or CHANGELOG). Review cadence:

- **Every 90 days:** founder reviews this constitution. Either:
  - Amend (per MR-1, MR-2, MR-4, MR-5), or
  - Reaffirm by updating `last_touched` field with no content change
- **Untouched > 90 days:** rule is "stale." Citing it as authoritative in new federation discussions requires reaffirming first.

This implements kernel/04-living.md §6 at federation scope.

### MR-7. CHANGELOG Append-Only

`federation/CHANGELOG.md` is append-only. Every amendment generates an entry. No entry deletion. No retroactive editing of past entries.

This implements kernel/I-7 at federation scope.

---

## §4. Reasoning Artifact Requirement

### MR-8. Every Amendment Has Reasoning

Per P-7 (reasoning trail at federation layer), every amendment to terms / principles / rules / meta-rules must include:

- **Trigger:** what observation or problem motivated this change
- **Rationale:** why this specific amendment solves the problem
- **Alternatives considered:** what other approaches were rejected and why
- **Falsification:** what observation would refute the amendment

Mutable changes can be brief (CHANGELOG entry suffices). Protected changes need full briefing-tier reasoning.

### MR-9. Reasoning Lives Forever

Reasoning artifacts (briefings) are append-only (R-10). Future federation members can read why current rules exist by traversing the CHANGELOG and briefings.

---

## §5. Conflict Resolution Authority

### MR-10. Founder as Last-Resort Arbiter

When federation members disagree on rule interpretation:

1. Members raise via briefing
2. Other members weigh in via acknowledgment / counter-briefing
3. If no consensus emerges within 14 days: founder issues binding interpretation as briefing
4. Interpretation becomes precedent (referenced in future similar cases)

This concentrates final authority in the founder. Acceptable for current single-founder phase. Will need decentralization (kernel/03-constellation.md §5 criteria) as federation grows.

### MR-11. Sunset on Founder Sole Authority

When kernel/03-constellation.md §5 criterion 4 is met (non-founder amendment to kernel accepted), federation arbitration similarly transitions:

- From: founder sole arbiter
- To: panel of ≥3 senior federation members (those with longest active membership) for protected rule disputes; founder for immutable matters only

This is forward-looking — currently 0/4 criteria met, so MR-10 governs.

---

## §6. Versioning Federation Constitution

### MR-12. Federation Version Bump Triggers

The federation constitution (this set of files) has a version. Recorded in `federation/manifest.yaml`. Bumped when:

- **Patch (0.X.Y → 0.X.Y+1):** typo fix, clarification, mutable rule amendment
- **Minor (0.X.Y → 0.X+1.0):** new rule added, protected rule amended, new term/principle
- **Major (0.X.Y → 1.0.0):** structural change (new layer, removed layer, immutable amended via fork-divergence)

### MR-13. Snapshot at Each Version

Every version bump → snapshot_hash recomputed → CHANGELOG entry → optionally on-chain anchor via `IConstitutionRegistry`.

The federation snapshot anchors are themselves audit trails — anyone can verify "the federation operated under rules vX.Y.Z at this time."

---

## §7. Evolution of Meta-Rules Themselves

Recursive question: how do meta-rules change?

**Answer:** meta-rules are protected (MR-2 procedure). The recursion bottoms out at:
- Immutable principles (P-1 through P-3, P-8) — cannot change without fork
- Otherwise: standard MR-2 protected amendment

This gives federation evolution a finite tree of changeable elements with clear immutable ground truth.

---

## §8. What Meta-Rules Do Not Cover

- How instance internal rules change (each instance owns its meta-rules)
- How master Leviathan formalizes (separate process — see `eylem:pos-kernel-conformance` in companion's eylemler)
- How kernel itself changes (governed by kernel/00-meta.md, separate process)

Federation meta-rules govern only the federation/ folder of `leviathan-meta`.

---

*Federation meta-rules. The recursive ground floor of federation governance.*
