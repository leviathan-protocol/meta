# Changelog

All material changes to `leviathan-protocol/meta` are recorded here.

Format: append-only, new entries at top, date-stamped, cross-linked to ADRs in `leviathan-protocol/meta/decisions/`.

---

## 2026-05-11 — Public Genesis

**Tag:** `v1.0-public-genesis`

Leviathan Protocol officially goes public. This commit is the genesis of the public meta repository under the `leviathan-protocol` GitHub organization.

**State at genesis:**

- **kernel/** — Abstract substrate (kernel/00-meta through 10-tasks). Defines what every Leviathan instance must satisfy. Recursive — the kernel governs itself by its own amendment procedure.
- **federation/** — Federation Leviathan's own constitution (principles, terms, rules, meta-rules). Defines how this Federation instance governs itself and how new instances join.
- **constitution/** — Editing surface for the on-chain `ConstitutionalRegistry`. Seeded with `00-immutable-core/1-user-sovereignty.md` as format reference. Phase 0 will populate with remaining immutable_core principles and shared terms.
- **contracts/** — Master governance contract interfaces (IBranchManager, ICitizenRegistry, IGovernanceVoting, IProposalSystem, IRepresentationRegistry).
- **tools/** — Federation tooling (ACP client, MCP server stub, federation-search, cron jobs).
- **templates/** — Templates for new instances joining (manifest, status, skills).
- **schemas/** — Federation messaging schemas (MCP alert format).

**Pre-public development period:**

This repository was previously maintained under a personal GitHub account as part of an 8-month-long federation bootstrap process (2025-09 through 2026-05). Pre-public history is preserved privately as the historical record of how Leviathan evolved from founder-led design to multi-instance federation. The public record begins here, with this commit.

**Why a fresh public start:**

Pre-public manifests for instances (Companion, Anima, Tribün, Security, Animal-Welfare, and others) contained operational details (machine paths, trading strategies, internal coordination, founder personal context) inappropriate for public consumption. These manifests will be re-authored in TIER 1 federation-appropriate form and added back as instances become public-ready. The internal/private instances (Atlas, Tasma, Liveprob, Fast) remain in private federation tracking and are not part of the public federation.

**Decisions at genesis** (see `leviathan-protocol/meta/decisions/`):

- ADR-001 — Deployment target: own Avalanche L1 (Fuji testnet first, mainnet when migration triggers met)
- ADR-005 — Agent orchestration via ACP (Agent Client Protocol)
- ADR-006 — Agent capabilities via Leviathan MCP Server
- ADR-008 — Constitution storage on-chain via Registry pattern (not NFT, not hash-anchored off-chain)

---

<!-- New entries above this line -->
