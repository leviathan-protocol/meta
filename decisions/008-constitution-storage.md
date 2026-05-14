---
adr: 008
title: On-Chain Constitution Storage — Registry Pattern
status: proposed
date: 2026-05-11
authors: [Mimar, Companion]
supersedes: null
superseded_by: null
---

# ADR 008 — On-Chain Constitution Storage (Registry Pattern)

## Context

Leviathan needs to store its constitutional content (principles, rules, terms, shadows, references) in a way that:

1. **Preserves sovereignty** — constitution is the protocol's law; should be on-chain
2. **Supports versioning** — history preserved across amendments
3. **Differentiates mutability** — immutable_core (never changes), locked (high-bar vote), mutable (regular vote)
4. **Enables auditing** — anyone can verify "what is the current constitution"
5. **Connects to governance** — each version traceable to the vote that ratified it
6. **Scales gas economics** — Leviathan L1 controls own gas; on-chain storage is affordable
7. **Allows cross-Leviathan reference** — other Leviathans can inherit from or reference Core

Initial framing (in earlier drafts of the convergence plan) was "hash anchoring": content lives off-chain (markdown in `leviathan-meta/`), hash anchored on-chain. This was a gas-optimization compromise that weakens sovereignty — *"constitution lives outside, chain just points to it."*

User pushback (2026-05-11): *"Bu term/principle/rule'lar zaten anayasa — on-chain olması mantıklı değil mi?"* + *"NFT içinde tutsak? Veya daha iyi bir logic varsa?"*

Three on-chain storage patterns considered: ERC-721 NFT, plain struct mapping, and Registry pattern.

## Decision

**Deploy a purpose-built `ConstitutionalRegistry` contract on the Leviathan L1.** Constitutional elements (principles, rules, terms, shadows, references) are first-class on-chain entities. Each element has versioned content (inline if ≤ 500 chars, URI + hash if larger). Updates flow through governance, ratified versions emit events.

This is NOT an NFT pattern — Registry pattern was selected after evaluation because NFT semantics (transferability, ownership, marketplace) don't match constitutional governance needs.

The full `leviathan-meta/constitution/` markdown source remains as the **working draft surface** where humans edit and propose. On approval, a compile step generates the calldata to ratify a new version on-chain. The Registry on Leviathan L1 is **canonical**; `leviathan-meta/` is the editable mirror.

## Rationale

### Why on-chain at all (not hash-anchored)

- Constitution IS law; law is sovereign; sovereignty in this architecture = on-chain
- Leviathan L1 has own gas economics — affordable on our chain, expensive only on C-Chain mainnet (which we're not deploying to per ADR-001)
- Hash anchoring is a hedge ("law lives outside") that contradicts the Constitutional Company framing
- Auditors / validators / other Leviathans can verify current state with a single chain query — no off-chain fetch chain

### Why Registry pattern, not NFT

1. **No false transferability semantics** — constitutional elements don't transfer between owners; the protocol owns them all
2. **Purpose-built events** — `ElementRatified` is more meaningful than `Transfer` for constitutional changes
3. **Cleaner queries** — `getCurrentContent("user_sovereignty")` direct, no tokenId enumeration mystery
4. **Cheaper gas** — no ERC-721 overhead (balance tracking, approval mechanics, operator hooks)
5. **Type-safe slug access** — slug-based addressing matches mental model from `leviathan-meta/`
6. **Direct link to governance** — `proposalId` field on each version traces it to the vote that ratified it
7. **NFT semantics aren't needed** — we don't sell/transfer/approve constitutional elements

NFT pattern's main appeal — auto-discovery in standard explorers (Snowtrace) — is a UX issue, not an architecture one. We're building a constitution-aware browser anyway (LeviathanCore graph).

### Why content split (inline ≤ 500 chars + URI for longer)

- Short core principles (immutable, oft-quoted) fully on-chain → maximum sovereignty
- Long reasoning / examples / history → URI pointer + hash → still verifiable, no chain bloat
- Content size determines storage strategy automatically at compile time

## Contract sketch

```solidity
contract ConstitutionalRegistry {
    enum ElementType { PRINCIPLE, RULE, TERM, SHADOW, REFERENCE }
    enum Mutability { IMMUTABLE, LOCKED, MUTABLE }
    
    struct Element {
        ElementType elementType;
        string slug;
        uint256 currentVersion;
        Mutability mutability;
        bool active;
        uint256 firstRatifiedAt;
    }
    
    struct Version {
        bytes32 contentHash;
        string inlineContent;
        string contentURI;
        uint256 ratifiedAt;
        address proposer;
        bytes32 proposalId;
    }
    
    mapping(bytes32 => Element) public elements;
    mapping(bytes32 => mapping(uint256 => Version)) public versions;
    
    address public governor;
    
    modifier onlyGovernance() {
        require(msg.sender == governor, "only governance");
        _;
    }
    
    event ElementRatified(bytes32 indexed slugHash, uint256 version, bytes32 contentHash);
    event ElementRetired(bytes32 indexed slugHash, uint256 atVersion);
    
    function ratifyNewVersion(
        string memory slug,
        string memory inlineContent,
        string memory contentURI,
        bytes32 contentHash,
        bytes32 proposalId
    ) external onlyGovernance returns (uint256 newVersion) { ... }
    
    function retireElement(string memory slug, bytes32 proposalId) external onlyGovernance { ... }
    
    function getCurrentContent(string memory slug) external view returns (Version memory) { ... }
    function getVersionAt(string memory slug, uint256 v) external view returns (Version memory) { ... }
    function getVersionHistory(string memory slug) external view returns (uint256[] memory) { ... }
}
```

Per-domain extensions: `DomainConstitutionalRegistry` deployed via `DomainFactory` for each domain (Animal Welfare, Music, Security, etc.). Each domain registry references the core registry for shared immutable principles.

## Alternatives considered

### Alternative A: ERC-721 NFT pattern
Each constitutional element is an NFT, versions = new tokens, immutable elements soulbound, governance contract holds them.

**Rejected because:**
- Transfer semantics misleading — constitution isn't tradeable
- ERC-721 overhead (balance tracking, approval) costs gas with no benefit
- Standard explorers auto-show NFTs, but we need custom UI anyway
- `Transfer` event doesn't carry constitutional meaning; `Ratified` does

### Alternative B: Hash anchoring + off-chain content (initial framing)
Constitution lives in `leviathan-meta/` markdown; only hash stored on-chain. Validator fetches content from canonical off-chain source, verifies hash.

**Rejected because:**
- Sovereignty weakened — "law lives outside, chain just points"
- Off-chain content storage = single point of failure (or trust assumption)
- Hash-mismatch detection is reactive; on-chain content is direct truth
- Leviathan L1 own gas economics removes the cost objection

### Alternative C: Plain mapping with struct (no contract wrapping)
Just a public mapping with structured data, no events, no governance hooks.

**Rejected because:**
- No event log = harder to index changes off-chain
- No access control encoded — any caller could rewrite
- No version history retention pattern
- Loses the audit trail value

### Alternative D: ERC-1155 (multi-token, balance = active version)
tokenId encodes (elementType, slug, version); balance signals active status.

**Rejected because:**
- Encoding complexity (packing element type + slug + version into uint256)
- Same ERC overhead problem as ERC-721
- Less type-safe than slug-string addressing

## Consequences

### Positive
- Constitution is on-chain in the strongest sense: queryable, immutable per version, sovereign
- Single source of truth: chain state, no "which copy is right" question
- Each version traces to its ratifying proposal — full governance audit trail
- Other Leviathans can directly read this registry — federation pattern enabled
- LeviathanCore UI can show "live constitution" by querying chain
- Validator alignment check becomes: read chain → use content for LLM prompt

### Negative
- New contract to maintain (`ConstitutionalRegistry.sol`) — must be tested, audited
- Compile pipeline (Phase 0) gets a new step: generate calldata to ratify versions
- Initial constitution deployment is many transactions (one per element)
- Updates are gas-costing on-chain ops (cheap on our L1, but not free)
- Migration burden if Registry contract itself needs upgrading (use OpenZeppelin upgradeable pattern or accept that v2 of the registry would itself be ratified by v1)

### Neutral
- `leviathan-meta/` becomes editing surface, not source of truth — slight mental model shift but matches "law is on-chain, drafts are off-chain" framing
- Validators run on Leviathan L1 anyway (per ADR-001) — querying chain for content is local-fast

## Migration approach

1. **Phase 0** (constitution unification): Compile `leviathan-meta/constitution/*.md` to ratification calldata. Each element becomes one ratification call.
2. **Phase 1** (chain deployment): Deploy `ConstitutionalRegistry.sol` to Fuji L1 as part of v2 suite. Execute ratification calls to populate.
3. **Validator daemon**: Update to read from chain registry, not from local YAML file. Cache for performance.
4. **Updates** (Phase 3+): Forum proposal → vote → if approved + aligned → governance contract calls `ratifyNewVersion()`.

## Sources

**Architectural reasoning:**
- User pushback (2026-05-11): *"Term/principle/rule on-chain olmalı, anayasa o çünkü"*
- Constitutional Company framing (ADR pending) — protocol's law must be sovereign
- ADR-001 (deployment target — own L1) makes on-chain storage gas-affordable

**Internal repo evidence:**
- `leviathan_node/contracts/src/DomainFactory.sol` — already supports clone pattern (extendable to ConstitutionalRegistry)
- `leviathan_node/contracts/src/CoreGovernor.sol` — already has governance entry point for `onlyGovernance` calls
- `leviathan_node/leviathan-core.yaml` — `constitution_hash` field exists as hedge; this ADR supersedes that approach

**External standards consulted:**
- ERC-721 — considered, rejected (transferability semantics wrong)
- ERC-1155 — considered, rejected (encoding complexity)
- ERC-5192 (Soulbound) — considered as NFT-with-no-transfer; rejected (still has unwanted NFT overhead)

## Related

- ADR-001 — Deployment target (own L1, makes on-chain storage feasible)
- ADR-009 (TBD) — Compile pipeline: leviathan-meta → ratification calldata
- ADR-010 (TBD) — Per-domain Registry deployment via DomainFactory
- Plan: `plans/phase-0-constitution.md` (must reflect Registry deployment as output)
- Plan: `plans/phase-1-chain-fuji.md` (must add ConstitutionalRegistry.sol to deployment)

## Revisit conditions

Re-examine if:
- Gas costs on Leviathan L1 become unexpectedly expensive (mainnet pricing changes)
- Cross-L1 references become a frequent operation and Registry pattern lacks needed primitives
- A new EVM standard emerges that combines registry semantics with explorer-native UI
- Constitutional element count exceeds chain practical limits (~1000s of elements)
- Versioning patterns expose a flaw (e.g., need branching constitutions rather than linear versions)
