# Leviathan Kernel

> **Part version:** 0.1.0 · **Tier:** protected · **Status:** initial draft, founder-only signed-off · **Last touched:** 2026-05-04 · **License:** MIT (see `00-meta.md` §7 `I-4`).
>
> ⚠ **Honest header (required by `03-constellation.md` §5):** This kernel is operated by one founder. The Founder Independence Criterion (`01-why.md` §4) is currently unmet. 0 of 5 Decentralization Path criteria satisfied. Treat this as a pre-success protocol that says so.

A public, versioned, forkable, evolution-explicit governance substrate for AI agents — and, by structural identity, for personal operating systems of humans.

This repo is the **kernel**: the abstract protocol. Concrete **instances** live in their own repos, fork this kernel, and add domain-specific content.

---

## What This Is

- A constitution architecture for autonomous agents that take actions in the real world.
- Four-layer (Term / Principle / Rule / Meta-Rule), three-tier (immutable / protected / mutable), three-role (Sidecar / Magistrate / Sovereign).
- Versioned everywhere, fork-friendly, decay-honest (90-day reaffirmation cadence).
- Explicit about what would refute it (`01-why.md` §6, `05-evidence.md` §8).
- Operated as if the founder will be removed — because the protocol claims success when that becomes possible (`01-why.md` §4).

## What This Is Not

- Not an AGI alignment proposal.
- Not a regulatory framework.
- Not an LLM (governs LLMs; is not one).
- Not an academic research project (collects evidence; aims at operation).
- Not a brand (`01-why.md` §5).

---

## How to Read

If you read only one part, read **`08-shadow.md`** first. The kernel's failure modes are stated more candidly than its claims.

By audience role (`09-engage.md`):

- **Operator** (you want to fork and run an instance): `00-meta.md` → `02-anatomy.md` → `03-constellation.md` §6 → `08-shadow.md`.
- **User** (you use someone else's instance): `02-anatomy.md` §1–§5 → `03-constellation.md` §3 → `08-shadow.md` §6.
- **Researcher** (you want to replicate or refute): `01-why.md` §6 → `05-evidence.md` → `08-shadow.md`.
- **Critic** (you think this is wrong): `08-shadow.md` → `01-why.md` §5 → `00-meta.md` §4.5.

By topic (sequential):

- `00-meta.md` — how this kernel itself evolves
- `01-why.md` — the capture window, what existing frames miss
- `02-anatomy.md` — the four-layer + Trinity
- `03-constellation.md` — federated topology, decentralization path
- `04-living.md` — versioning, decay, frozen-vs-living argument
- `05-evidence.md` — n=4 instances, limitations stated
- `06-mind.md` — *appendix* — Mind reference runtime
- `07-economy.md` — token, slashing, physical-world stakes
- `08-shadow.md` — failure modes
- `09-engage.md` — paths for each audience
- `glossary.md` — Terms layer of the kernel itself
- `CHANGELOG.md` — meta-rules in action; every modification logged
- `../specs/` — implementation specs cited by parts (`NODE_SPEC.md`, `ARCHITECTURE.md`, `CONTRACT_SPEC.md`); sibling to kernel

---

## Key Claims (and Where They Live)

| Claim | Where | Falsifiable? |
|-------|-------|--------------|
| Four-layer anatomy is sufficient | `02-anatomy.md` §2 | Yes (`01-why.md` §6) |
| POS↔Constitution structural identity | `01-why.md` §3 | Yes (`01-why.md` §6) |
| Heterogeneous Magistrate panels reduce monoculture failure | `02-anatomy.md` §6.2, `I-2` | Yes (`01-why.md` §6) |
| Living constitutions outlive frozen ones | `04-living.md` §7 | Yes (`01-why.md` §6) |
| Founder independence is achievable | `01-why.md` §4, `05-evidence.md` §8 | Yes (5-year window) |

If a researcher refutes any of these via published replication, the kernel records it. The protocol's standing or fall depends on these tests, not on the founder's continued attention.

---

## How to Fork

1. Read at least `00-meta.md`, `02-anatomy.md`, `03-constellation.md` §6, `08-shadow.md`.
2. Decide whether you are forking **conformantly** (preserves all 7 immutable invariants — keeps the Leviathan name) or **divergently** (modifies an invariant — must rename).
3. Clone this repo. In your fork's README, declare the parent: `forked-from: leviathan-kernel@v0.1`.
4. Add an instance constitution following `02-anatomy.md` (four layers, with content for your domain).
5. Honor the immutable invariants (`I-1` through `I-7`, `00-meta.md` §7) or rename per step 2.
6. If you participate in the constellation: register with a Sovereign Console of your choice (`03-constellation.md` §3.5 — anyone may run a Console); optionally subscribe to the Lesson Ledger (`03-constellation.md` §4).

The kernel maintainer collects no fees, retains no veto, and cannot retract your fork rights once granted (`I-4`).

---

## Project Status (Honest)

- **Kernel doc:** v0.1, 11 parts + glossary + CHANGELOG, written.
- **Reference instances:** 4 named (`05-evidence.md`). All single-operator. Companion is the longest-running (12+ months); Liveprob's Magistrate Node specification is complete but no nodes deployed; Security Leviathan is a single-node panel (gap flagged); Levi Template has 0 forks.
- **Sovereign Console:** designed in `03-constellation.md` §3, code pattern not deployed.
- **Lesson Ledger:** v0 schema sketched (`03-constellation.md` §4), no traffic.
- **Token (`$LVTN`):** designed in `07-economy.md`, no live tokenomics.
- **Decentralization Path:** 0 of 5 criteria met.

The kernel exists in a pre-operational state and says so. Reading it as if it claimed otherwise is a misreading.

---

## License

MIT (specified by immutable invariant `I-4`). Forks may not retroactively tighten the license. If you depend on this kernel and a future maintainer attempts retroactive tightening, the prior license remains valid for your version — that is what `I-4` enforces.

The Leviathan name is preserved through the immutable invariants (`I-1` through `I-7`). Forks that diverge from any invariant must rename. This is information preservation, not territorialism (`01-why.md` §5.5).

---

## Citations and References

Karpathy (2025) *Software 3.0*; Anthropic (2022, 2023) *Constitutional AI*; OpenAI (2024) *Model Spec*; European Union (2024) *AI Act*; Nakamoto (2008) *Bitcoin*; Hobbes (1651) *Leviathan*; Liskov (1987) *Substitution principle*; Ostrom (1990) *Governing the Commons*; Wang et al. (2023) *Voyager*; Popper (1959) *Logic of Scientific Discovery*; Bostrom (2014) *Superintelligence*; Roko (2010) *Roko's Basilisk* (referenced in `04-living.md` §7); RFC process (1969–) and the Linux kernel mailing list (1991–) — operational precedents for living, versioned, forkable specifications.

Implementation specs snapshotted in `../specs/` (`NODE_SPEC.md`, `ARCHITECTURE.md`, `CONTRACT_SPEC.md`). These are pre-kernel artifacts; they will be revised against this kernel going forward (causal direction reverses — see `../specs/README.md`). The kernel and specs are kept in sibling directories so the kernel doc remains self-contained and the specs can evolve independently while still being conformance-checked against the kernel by `../tools/conformance.py`.

---

## Filing Issues, Proposing Amendments, Forking

- **Issue or correction:** open a PR against the affected part. Include the version bump and CHANGELOG entry per `00-meta.md` §4.
- **Amendment to a protected-tier part:** PR + Magistrate panel review per `00-meta.md` §4.2. While the panel is single-node (founder-only), this is acknowledged as a known pre-success state per the honest header above.
- **Amendment touching an immutable invariant:** the kernel does not accept these as in-place edits. Fork divergently per `00-meta.md` §4.5; the kernel records the divergence and the rationale.
- **Fork:** see "How to Fork" above. No permission required; conformance is observable from your fork's content.

---

*This README is itself a kernel part. It follows the same rules: versioned, decay-tracked, amendable. Last touched 2026-05-04.*
