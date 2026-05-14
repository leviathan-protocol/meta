# Leviathan Protocol — Meta Repository

> **The Federation Leviathan.**
> Coordination layer for the Leviathan Protocol: kernel substrate, federation constitution, member instance registry, and governance contracts.

---

## What this repository is

Leviathan is a **constitutional governance protocol** for AI agents and organizations. It is not a single project — it is a **federation of instances**, each running its own constitution that inherits from a shared kernel.

This repository (`leviathan-protocol/meta`) is itself a Leviathan instance — the **Federation Leviathan**. It has its own constitution (`federation/`), its own membership rules, its own amendment procedure. It coordinates other instances without controlling them.

**What lives here:**

- The **canonical kernel** (abstract substrate) → `kernel/`
- The **federation's own constitution** → `federation/` (terms, principles, rules, meta-rules)
- The **canonical constitution editing surface** for the on-chain ConstitutionalRegistry → `constitution/`
- **Master governance contracts** → `contracts/`
- **Federation tooling** → `tools/`
- **Templates** for new instances joining → `templates/`
- **Schemas** for federation messaging → `schemas/`

**What does NOT live here:**

- Implementation code — instance code lives in instance-specific repositories
- Founder personal data or POS information — strictly private, never in any public repo
- Operational manifests with sensitive details (trading strategies, internal machine paths, investor relationships) — these belong to private federation tracking
- A public website — that's `leviathan.life`

---

## Three-tier federation architecture

```
TIER 1: Federation manifest    ← here, in meta/<instance>/
  • Public-appropriate "this instance exists, is part of federation"
  • Pointer to TIER 2 (constitution repo)

TIER 2: Instance constitution  ← separate repo, leviathan-protocol/<instance>
  • Specialized Leviathan's constitution (principles, rules, terms)
  • Federation membership manifest
  • Pointer to TIER 3 (implementation)

TIER 3: Implementation code    ← separate repo, can be private
  • Actual app/service/contract code
  • Constitution-bound but not constitutional itself
```

A Leviathan instance can be partial — TIER 2 without TIER 3 yet (constitution drafted, not yet implemented), or TIER 1 without TIER 2 yet (federation member, constitution not crystallized).

---

## Featured public instances

The federation currently has these public-facing member instances:

| Instance | Role | Repository | Status |
|----------|------|-----------|--------|
| **Companion** | Layer 1 — personal POS governance pattern | (private — personal instance) | Operational |
| **Anima** | Layer 3 — mobile POS, on-device sovereignty | TBD | Active development (Flutter native migration) |
| **Animal Welfare** | First specialized Leviathan | `leviathan-protocol/animal-welfare` | Genesis (constitution being authored) |
| **Tribün** | Sports/fandom community governance | TBD | Planned |
| **Security** | Validator federation auditor | TBD | Planned |

Additional internal/operational instances are tracked privately in the founder's federation backup; they may join public federation when their public manifests are ready.

---

## Constitution storage

Per [`constitution/README.md`](./constitution/README.md), constitutional elements (principles, rules, terms, shadows, references) are:

1. **Authored here** in `constitution/` as Markdown + YAML frontmatter files
2. **Compiled** to ratification calldata via `tools/`
3. **Ratified on-chain** via `ConstitutionalRegistry.sol` (deployed on Leviathan L1)
4. **Canonical state lives on-chain**, not in this repo

The repo is the **editing surface**; the chain is the **canonical record**. This separation allows large editorial content and version history to live in chain while the repo stays a readable editing experience.

See [`docs/element-format.md`](./docs/element-format.md) for the file format spec, and [`docs/architecture-overview.md`](./docs/architecture-overview.md) for how every layer of the federation relates.

---

## Governance layers

Leviathan operates on two distinct governance layers:

### Layer 0 — Implementation (off-chain, RFC-style)
Changes to the reference implementation repos (this one, `node`, `ui`, sub-leviathans, etc.) follow an **RFC-style process** documented in this repo's [`decisions/`](./decisions/) folder via Architectural Decision Records (ADRs). Founder is the sovereign authority during bootstrap; this may evolve toward a community-elected developer council as the project matures.

### Layer 1 — Protocol (on-chain)
The Leviathan Protocol itself — once fully deployed — is governed **on-chain** via the `ConstitutionalRegistry` contract, validator network, and forum-based proposals.

These are deliberately separate to avoid infinite recursion (you cannot govern your own bootstrap with the thing you're bootstrapping). Mirrors Bitcoin Core (BIP process) + Bitcoin protocol, or Ethereum (EIPs) + Ethereum protocol patterns.

---

## How to contribute

1. **Read the kernel** — `kernel/` describes the abstract substrate every Leviathan instance must satisfy
2. **Read the federation constitution** — `federation/` describes how this Federation Leviathan governs itself
3. **Read [`leviathan-protocol/meta`](https://github.com/leviathan-protocol/meta)** — the coordination repo with current ADRs, phase plans, and active decisions
4. **Propose changes** via PRs to relevant files, following the editorial separator pattern (constitutional content above `<hr>`, editorial below)
5. **For specialized Leviathans** — propose a new TIER 2 repo via PR to `templates/`

---

## License

CC BY-SA 4.0 (or compatible). Fork freedom is built into the protocol itself — see `federation/principles.md`.

---

## Related repositories

- [`leviathan-protocol/meta`](https://github.com/leviathan-protocol/meta) — Cross-repo coordination, ADRs, phase plans, status dashboard
- [`leviathan-protocol/animal-welfare`](https://github.com/leviathan-protocol/animal-welfare) — First specialized Leviathan instance
- [`leviathan-protocol/node`](https://github.com/leviathan-protocol/node) — Smart contracts + validator daemon *(coming)*
- [`leviathan-protocol/ui`](https://github.com/leviathan-protocol/ui) — Site + forum *(coming)*

Website: [leviathan.life](https://leviathan.life)
