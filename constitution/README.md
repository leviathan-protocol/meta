# Constitution — Editing Surface for the On-Chain Registry

> **Status:** draft  ·  **Phase:** 0 (in progress as of 2026-05-11)
> **Format spec:** [leviathan-protocol/meta/specs/element-format.md](https://github.com/leviathan-protocol/meta/blob/main/docs/element-format.md)
> **On-chain target:** `ConstitutionalRegistry.sol` deployed on Leviathan L1 (per [ADR-008](https://github.com/leviathan-protocol/meta/blob/main/decisions/008-constitution-storage.md))

This folder is the **human-editable surface** for Leviathan's on-chain constitution. The canonical state lives on-chain in the `ConstitutionalRegistry` contract; this folder is where amendments are drafted, reviewed, and prepared for ratification.

---

## Structure

Element type at folder level. Mutability tier (IMMUTABLE / LOCKED / MUTABLE) in YAML frontmatter of each file. Restructured 2026-05-14 to align with the founder's POS pattern; all 4 federation repos use this layout.

```
constitution/
  ├── terms/         ← @TERM       definitional vocabulary
  ├── principles/    ← #PRINCIPLE  guiding values
  ├── rules/         ← !RULE       operational + metarules
  ├── shadows/       ← 🜏SHADOW    anti-patterns (future)
  ├── protocols/     ← ⚙PROTOCOL   situational behavior sets (future)
  └── README.md
```

Each constitutional element is a single `.md` file with:
- **YAML frontmatter** for metadata (slug, element_type, mutability, current_version, ...)
- **Body** for content, split into:
  - **Constitutional content** (above the `<hr>`) — goes on-chain
  - **Editorial content** (below the `<hr>`) — for human readers, not stored on-chain

See [`../docs/element-format.md`](../docs/element-format.md) for full spec, including the seed example.

---

## Workflow

```
Edit .md file → PR → Review → Compile (CI) → Governance vote → On-chain ratify
```

The on-chain ratification (via `ConstitutionalRegistry.ratifyNewVersion(...)`) is the moment a change becomes canonical. Until then, repo edits are drafts.

## Migration status

- **Seed:** `00-immutable-core/1-user-sovereignty.md` (2026-05-11, written as format reference)
- **Restructure 2026-05-14:** flat element folders (`terms/`, `principles/`, `rules/`, ...) with mutability declared in YAML frontmatter
- **2026-05-15 — dialectic/evidence/proposal trio ported** from DAHAO test-1 prototype:
  - `terms/dialectic.md` (LOCKED), `terms/evidence.md` (LOCKED), `terms/proposal.md` (LOCKED)
  - `rules/dialectic-format.md` (LOCKED), `rules/evidence-required.md` (MUTABLE), `rules/proposal-process.md` (LOCKED)
- **TODO Phase 0 Step 4:**
  - Migrate `federation/principles.md`, `federation/terms.md`, `federation/rules.md` content into individual element files here
  - Migrate `leviathan_node/leviathan-core.yaml` immutable_core entries into `00-immutable-core/`
  - Migrate `dahao-all/aigentone/dahao-animal-welfare-test-1/data/*.json` into `leviathan-protocol/animal-welfare` repo (separate repo, not this one)
- **TODO Phase 2 — process layer numbers and ratchet:**
  - Port `rule_consensus_threshold`, `rule_protection_ratchet`, `rule_quorum_requirement`, `rule_alignment_check`, `rule_reference_validity`, `rule_version_bump` from DAHAO test-1 with Leviathan-vocabulary adaptation (standing-weighted quorum, magistrate panel for alignment check, etc.)

## Compile pipeline

(To be implemented in Phase 0 Step 6 — scripts will live in `../scripts/`)

- `compile-to-registry-calldata.py` — produces ratification calldata for on-chain registry population
- `compile-to-ui-snapshot.py` — produces JSON snapshot for UI fallback rendering
- `verify-against-chain.py` — verifies repo content matches on-chain hashes

## What does NOT live here

- Implementation code (lives in `leviathan-protocol/node`, `leviathan-protocol/ui`, etc.)
- Federation Leviathan's own membership/coordination governance (lives in `../federation/`)
- Instance status manifests (lives in `../anima/`, `../atlas/`, etc.)
- Founder POS or other private content (never enters this repo)
