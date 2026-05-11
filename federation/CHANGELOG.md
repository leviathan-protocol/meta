# Federation Constitution — Modification Log

> Every amendment to federation/terms.md, federation/principles.md, federation/rules.md, federation/meta-rules.md, or federation/manifest.yaml is logged here.  
> Format mirrors `kernel/CHANGELOG.md`.  
> Entries ordered most recent first.  
> Append-only per MR-7.

---

## 2026-05-05 — Federation Constitution Genesis (v0.1.0)

### Trigger

During the 2026-05-05 design session for `leviathan-meta` skeleton building, the founder articulated:

> *"aslinda bu leviathan-meta da iletisim leviathan i degil mi? oraya katilmak icin de kurallar rules prensip term falan olmali. girdiler yapisal olmali. biraz boyle dusunelim."*

This recursive insight — `leviathan-meta` is itself a Leviathan instance, requiring its own constitution to govern federation membership and coordination — was correct. The kernel's principle "this document is itself a Leviathan instance" (kernel/00-meta.md §1) applies recursively at federation scope.

### Rationale

Without a federation constitution:

- `leviathan-meta` would be just a coordination tool, not a kernel-conformant Leviathan
- Membership rules would be implicit (READMEs and informal convention), causing drift
- Federation evolution would be unprincipled — anyone could change rules silently
- The recursive model "every coordinating entity needs its own constitution" would be violated at the very layer that coordinates other entities

Adding `federation/` with terms / principles / rules / meta-rules brings federation governance into the same kernel-conformant pattern as instance governance.

### Created in This Genesis

- `federation/terms.md` v0.1.0 — 13 terms (instance, subdirectory ownership, snapshot_hash, forked_from, inherits_from, status manifest, public-safe manifest, briefing, acknowledgment, sync workflow, discrepancy, provisional top, re-anchor seam, kernel-conformant fork, divergent fork, Sovereign Console, federation member)
- `federation/principles.md` v0.1.0 — 10 principles (P-1 through P-10):
  - P-1 Subdirectory Ownership Discipline (immutable)
  - P-2 Privacy Sovereignty (immutable)
  - P-3 Kernel Anchor Required (immutable)
  - P-4 No Silent Override (protected)
  - P-5 Append-Only Briefings (protected)
  - P-6 Sovereign Console Discipline (protected)
  - P-7 Reasoning Trail at Federation Layer (protected)
  - P-8 Instance Sovereignty Outranks Federation Convenience (immutable)
  - P-9 Frozen Federation Is Dead Federation (mutable)
  - P-10 Adaptation Rate Over Prediction Completeness (mutable)
- `federation/rules.md` v0.1.0 — 17 rules (R-1 through R-17) covering membership, sync workflow, briefing structure, privacy, public mirror plan, conformance check
- `federation/meta-rules.md` v0.1.0 — 13 meta-rules (MR-1 through MR-13) covering amendment procedure, decay & reaffirmation, reasoning artifacts, conflict resolution, version bump triggers
- `federation/manifest.yaml` v0.1.0 — federation snapshot (forked_from kernel, inherits_from null because federation sits beside master), member registry, falsification commitments, decentralization status (0/5)

### Compatibility

- New constitution: backward-compatible because there was no prior federation constitution to break
- Existing instance subdirectories (companion, liveprob, security, tasma, atlas) become members under R-1; first-status briefings can be retroactively filed if needed (recommended within 30 days)
- Kernel relationship: federation forks from `leviathan-kernel@v0.1.0`, does not inherit from any other Leviathan (sits beside master)

### Falsification Commitments (per P-7)

Three falsification commitments declared in `federation/manifest.yaml`:

1. Federation rules are honored by member instances → refuted if silent override at scale
2. Federation evolves via reasoned amendment, not stealth → refuted if protected rule amended without briefing
3. Federation visibility does not become control → refuted if founder enforces instance behavior via meta-repo

### Approver

Founder (master Mac, on behalf of all federation members). MR-10 (founder as last-resort arbiter) governs current single-founder phase.

### Open Questions Carried Forward

- `federation/manifest.yaml.federation_constitution.snapshot_hash` is currently `TBD`. Compute via tool (TODO: `tools/federation-conformance.py`) when available.
- Some manifest fields for member instances reference `manifest.yaml` files not yet written (liveprob, security, tasma — placeholders only). Members will create these as they take subdirectory ownership.

---

*This is the foundation entry. All future amendments will append above this line.*
