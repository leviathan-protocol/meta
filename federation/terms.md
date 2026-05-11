# Federation — Terms (Layer 1)

> **Part version:** 0.1.0 · **Tier:** protected · **Last touched:** 2026-05-05  
> **Scope:** vocabulary used in federation coordination. Not an instance's terms (those live in instance constitutions); these are the words the federation itself uses to describe its members and protocols.

---

## §1. Why Terms Layer

The federation cannot enforce coordination if members disagree on what words mean. This terms layer defines the vocabulary every member instance must use when interacting with the federation: status manifests, briefings, sync workflow, ownership claims.

Terms here are normative for federation-level interaction. Instance-internal vocabularies are sovereign — instances may use any words they like in their own constitutions; only when speaking TO the federation must they conform to terms here.

---

## §2. Federation Vocabulary

### `instance`

A Leviathan substrate (constitution + runtime + memory) that has registered with the federation by maintaining a subdirectory in `leviathan-meta/`. Instances are sovereign — they have their own constitutions, their own runtime, their own machines. Federation membership requires conformance to schema (terms, principles, rules) but does not require identical constitutions.

Examples: `companion`, `liveprob`, `security`, `tasma`, `atlas`.

### `subdirectory ownership`

The federation rule that each instance directory in `leviathan-meta/` is **edited by exactly one machine/agent**. Other machines may read but must not push changes to subdirectories they don't own. Ownership is declared in `README.md` Subdirectory Ownership table.

Cross-cutting changes (kernel evolution, contracts) require coordination via `briefings/`.

### `snapshot_hash`

The deterministic hash of an instance's full constitution at a specific version. Provides cryptographic anchor for "this constitution was X at this time." Computed by instance's own tooling (e.g., `compute_snapshot.py`). Recorded in instance's manifest.yaml. Optionally anchored on-chain via `IConstitutionRegistry`.

### `forked_from`

A claim, recorded in instance manifest, of which kernel version the instance derived from. Format: `leviathan-kernel@vX.Y.Z`. Required for federation membership.

### `inherits_from`

A claim, recorded in instance manifest, of which parent constitution the instance inherits from. May be `null` (provisional top), or `master-leviathan@vX.Y.Z` (when master is formalized). When non-null, the instance's elements must be a **superset** of parent's (no weakening).

### `status manifest`

The `status.md` file in each instance subdirectory. Public-facing description of instance state. Updated whenever the instance has changes other instances should know about. Required for federation membership.

### `public-safe manifest`

The `manifest-public.yaml` (or equivalent) in instance subdirectory. Machine-readable subset of instance's full constitution manifest, redacted to remove private content. This is what gets exported to public mirror.

### `briefing`

A structured communication addressed to one or more instances about a system-wide or cross-cutting change. Lives in `briefings/YYYY-MM-DD-<topic>/`. Includes a cover letter, content, and (after acknowledgment) ack files.

### `acknowledgment`

An instance's confirmation that it has read a briefing addressed to it. Submitted as builder-report on instance's machine OR as ack file in `briefings/<briefing>/ack/`. Closes the coordination loop.

### `sync workflow`

The git protocol for coordinating across machines: pull-rebase before edits, push after edits. Defined in `federation/rules.md`.

### `discrepancy`

A contradiction surfaced by an instance between a briefing's claim and the instance's local reality. Required to be reported, not silently ignored. Process defined in `federation/rules.md`.

### `provisional top`

An instance with `inherits_from: null` because the master Leviathan it would inherit from doesn't exist yet. Operationally a specialty domain, constitutionally top-level fork. Maintains "re-anchor seam" — when master crystallizes, sets `inherits_from` to master and runs validator.

### `re-anchor seam`

The discipline of preserving the path to attach to a future parent constitution. Manifest keeps `inherits_from: null` visible; SubConstitutionValidator skeleton exists; explicit acknowledgment of provisional state. Per kernel/03-constellation.md §6.

### `kernel-conformant fork`

A federation member that has not weakened any kernel invariant (`I-1` through `I-7`). Verifiable via `tools/conformance.py` (kernel) plus federation conformance check (TBD).

### `divergent fork`

A federation member that has weakened one or more kernel invariants. Permitted (per kernel I-4 fork freedom) but is no longer a kernel-conformant Leviathan; technically a different protocol. Federation may still host divergent forks for transparency, but they are flagged as such.

### `Sovereign Console`

The kernel/03-constellation.md §3 visibility primitive. `leviathan-meta` is the operational implementation of Sovereign Console for the founder. Critical: Console is a **visibility** primitive, NOT a **control** primitive. It shows state across instances; it does NOT enforce instance behavior.

### `federation member`

An instance that has:
1. A subdirectory in `leviathan-meta/`
2. A `status.md` conforming to template
3. A manifest declaring `forked_from` (and optionally `inherits_from`)
4. Acknowledged the federation principles (federation/principles.md)

Once these conditions are met, the instance is a member. Membership grants subdirectory ownership; revocation requires founder action (rare).

---

## §3. Reserved Vocabulary

These words have specific meaning in the federation context and should not be used loosely:

- `instance` — never just "project" or "service" in federation docs
- `briefing` — not "memo" or "doc" or "update"
- `acknowledgment` — not "reply" or "response"
- `subdirectory ownership` — not just "ownership" (which is ambiguous)
- `master-leviathan` — only when referring to formal `master-leviathan@vX.Y.Z`, not casual "the master"

---

*Federation terms layer. Refer to `federation/principles.md` for federation principles, `federation/rules.md` for concrete protocols.*
