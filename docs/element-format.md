# Constitutional Element File Format

> **Status:** draft  ·  **Date:** 2026-05-11  ·  **Related ADRs:** [008](../decisions/008-constitution-storage.md)
> **Audience:** anyone editing `leviathan-protocol/meta/constitution/` content

This spec defines the file format for constitutional elements (principles, rules, terms, shadows, references) in `leviathan-protocol/meta/`. Format choice: **Markdown + YAML frontmatter** (Option B per format decision 2026-05-11).

---

## Why this format

- **GitHub-native rendering** — anyone viewing a file in browser sees formatted content
- **Long content friendly** — markdown handles paragraphs, lists, code blocks naturally
- **Diff-friendly** — PRs show exactly what constitutional text changed
- **Editorial separation built-in** — `<hr>` divides on-chain content from editorial context
- **Compile-friendly** — `python-frontmatter` library parses metadata + body in 2 lines

---

## File structure

```
leviathan-protocol/meta/constitution/
  ├── 00-immutable-core/         # mutability: IMMUTABLE
  │   ├── 1-user-sovereignty.md
  │   ├── 2-fork-freedom.md
  │   └── ...
  ├── 10-protocol-mutable/        # mutability: LOCKED
  │   ├── citizenship.md
  │   └── ...
  ├── 20-domains/                 # per-domain
  │   └── animal-welfare/
  │       ├── principles/
  │       ├── terms/
  │       └── rules/
  ├── 30-shared-terms/            # mutability: MUTABLE
  └── README.md
```

One file per element. Filename = element slug (kebab-case) with leading number for sort order in immutable_core.

---

## Frontmatter schema

```yaml
---
slug: user_sovereignty           # snake_case, unique across all elements
element_type: PRINCIPLE          # PRINCIPLE | RULE | TERM | SHADOW | REFERENCE
mutability: IMMUTABLE            # IMMUTABLE | LOCKED | MUTABLE
inline: true                     # true = on-chain inline; false = contentURI used
current_version: 1               # incremented on each ratification
contentURI: null                 # IPFS or HTTPS URI if inline: false
---
```

### Field semantics

| Field | Type | Notes |
|-------|------|-------|
| `slug` | string (snake_case) | Unique identifier; used as on-chain key. Never change after ratification. |
| `element_type` | enum | Maps to `ConstitutionalRegistry.ElementType` |
| `mutability` | enum | `IMMUTABLE` = soulbound forever; `LOCKED` = high-bar governance vote required; `MUTABLE` = regular vote |
| `inline` | bool | `true` if content ≤ 500 chars (goes on-chain directly); `false` if longer (URI used) |
| `current_version` | int | Latest ratified version. Repo file = this version. History on chain. |
| `contentURI` | string \| null | When `inline: false`, IPFS CID or HTTPS URL where full content lives. Hash computed from URI-fetched content. |

---

## Body structure

Two zones separated by horizontal rule:

```markdown
[CONSTITUTIONAL CONTENT — goes on chain]

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

[EDITORIAL CONTENT — for human readers, contributors, future maintainers]
```

### Constitutional content (above the `<hr>`)

- This is what gets ratified, hashed, stored on-chain
- Should be terse, precise, normative
- Avoid examples, reasoning, history — those go below
- Markdown allowed but kept minimal (paragraphs, light emphasis)
- Total length ≤ 500 chars if `inline: true`, otherwise no limit (but URI used)

### Editorial content (below the `<hr>`)

- For humans only; never goes on-chain
- Reasoning, examples, enforcement details, historical context
- Cross-references to other elements
- Update freely without governance vote (just a PR)
- Compile script strips this section before hashing

---

## Seed example: `00-immutable-core/1-user-sovereignty.md`

```markdown
---
slug: user_sovereignty
element_type: PRINCIPLE
mutability: IMMUTABLE
inline: true
current_version: 1
contentURI: null
---

Users grant initial consent by bonding with an agent and defining its operating boundaries. After that, the agent acts independently within those bounds. The validator network ensures the agent stays within bounds — not the user checking every action. Users retain absolute revocation rights through unbonding.

<!-- BELOW THIS LINE: editorial context. Not stored on-chain. -->

---

## What this principle establishes

The bonding contract between user and agent is the foundational consent mechanism. Once a user bonds with an agent and accepts its values, the agent operates autonomously within defined boundaries until explicitly revoked.

## Enforcement mechanisms

1. **Bonding ceremony** — User explicitly accepts agent's values before any autonomous action
2. **Boundary definition** — User declares what the agent may and may not do
3. **Autonomous operation** — No per-action consent required within boundaries
4. **Revocation right** — User can unbond at any time, ending the agent's authority

## Why immutable

This principle is `IMMUTABLE` because it is constitutive of the agent-user relationship. Changing it would not be amending the constitution — it would be replacing the protocol entirely. Forks may choose different bonding semantics; this Leviathan instance does not.

## Reasoning trail

- Initial framing draws on Hobbes' social contract: citizens grant authority to sovereign, retain natural rights
- Adapted to AI agent context: user grants authority to agent, retains revocation right
- The Magistrate (validator) network exists precisely so users don't have to check every agent action

## Related elements

- `validator_consensus` (mutable) — defines how the network enforces boundaries
- `revocation_mechanism` (locked) — technical implementation of unbond
- `bonding_ceremony` (locked) — protocol for initial consent
```

In this example:
- **On-chain content** = the first paragraph after frontmatter (≤ 500 chars, fits inline)
- **Editorial content** = everything below the `<hr>`
- Compile script extracts only the on-chain portion, computes its hash, generates `ratifyNewVersion()` calldata

---

## Compile pipeline expectations

`leviathan-protocol/meta/scripts/compile-to-registry-calldata.py`:

1. Walk `constitution/` recursively
2. For each `.md` file:
   - Parse frontmatter → element metadata
   - Split body at the editorial separator (`<!-- BELOW THIS LINE: -->`)
   - Take only the pre-separator content
   - Compute `keccak256(content)` → `contentHash`
   - If `inline: true` and `len(content) > 500`: ERROR (fix file)
   - If `inline: false` and `contentURI` is null: ERROR (upload to IPFS first or fix)
3. Sort elements: IMMUTABLE first, then LOCKED, then MUTABLE
4. Emit `compiled/ratification-calls.json` — array of `ratifyNewVersion(...)` calldata
5. Emit `compiled/ui-snapshot.json` — JSON snapshot for UI fallback rendering

`leviathan-protocol/meta/scripts/verify-against-chain.py`:

1. Read each `.md` file in `constitution/`
2. Compute its hash (same algorithm as compile)
3. Query `ConstitutionalRegistry.getCurrentContent(slug)` for the same slug
4. Compare hashes — must match
5. Report mismatches (= chain drifted from repo, or repo edited without ratification)

---

## Editing workflow

```
1. Contributor edits a .md file in their fork
2. Open PR against leviathan-protocol/meta
3. Review (technical correctness, governance fit)
4. If approved + would be ratified on-chain:
   - Compile script runs in CI
   - Generates ratification calldata
   - Calldata submitted to ConstitutionalRegistry via governance vote
   - On successful ratification: PR merged + current_version frontmatter bumped
5. If editorial-only changes (below `<hr>`):
   - PR merged directly (no on-chain action needed)
   - No version bump
```

The `<hr>` separator is the key — it determines whether a change is constitutional (requires governance) or editorial (PR + merge).

---

## Validation rules (CI-enforced)

- Filename must match `slug` field (`user_sovereignty` ↔ `user-sovereignty.md` or `N-user-sovereignty.md`)
- `slug` must be unique across entire `constitution/` tree
- `inline: true` content must be ≤ 500 chars (after editorial strip)
- `inline: false` must have non-null `contentURI`
- `current_version` must be monotonically increasing (no rewinds)
- `element_type` and `mutability` must be valid enum values
- Editorial separator (`<!-- BELOW THIS LINE: -->`) must appear exactly once OR not at all (if entire file is constitutional)

---

## Open questions

- Should compile script also enforce a max constitutional text length even when `inline: false` (e.g., 5000 chars hard cap)?
- Should we allow multi-language variants per element (English + Turkish)? If so, format extension needed.
- How are deprecated/retired elements represented in repo? (One option: move to `99-retired/` subfolder; another: `retired: true` frontmatter flag)
- Should the compile script also produce a printable PDF of the full constitution as a release artifact?

These are deferred to the implementation team and will become ADRs as decided.
