# OpenPOS Governance Contracts

Avalanche C-Chain smart contracts for decentralized POS governance.

## Architecture

```
contracts/
├── interfaces/
│   ├── ICitizenRegistry.sol         — Wallet → POS hash mapping
│   ├── IGovernanceVoting.sol        — Quadratic voting (sqrt-weighted)
│   ├── IProposalSystem.sol          — Thesis/antithesis/synthesis discourse
│   ├── IRepresentationRegistry.sol  — AI proxy voting for offline nodes
│   └── IBranchManager.sol          — Governance topic branch management
└── README.md                        ← this file
```

## Status: Interfaces Only

These are **interface definitions** — the contract API surface. Implementations come in Faz 4 (Network). This design-first approach ensures:

1. Skills (`/export-governance`, `/represent`) can be built against stable interfaces
2. Contract logic can be reviewed before writing Solidity implementations
3. The governance identity schema and contracts stay aligned

## Key Design Decisions

### From B2 (Anayasa)
- **No node can be removed** — `withdraw()` is soft delete, citizen record persists
- **Delegation always revocable** — hardcoded, no governance override possible
- **Privacy sovereign** — `pos_hash` proves POS exists without revealing content
- **Fork Freedom** — any node can exit any Leviathan at any time

### Quadratic Voting
- Vote weight = `sqrt(base_value + earned_xp + delegated_tokens)`
- Prevents plutocracy — 100 tokens = 10 weight, not 100

### Discourse Protocol
- Proposals follow thesis → antithesis → synthesis flow
- Mandatory discussion period before voting opens
- Discussion time scales with threshold level (24h routine → 90 days mission)

### AI Representation
- Every AI vote tagged `[REPRESENTED]` on-chain
- 24h override window for user correction
- Constitutional+ proposals: NEVER auto-voted
- Full reasoning published for transparency

## Threshold Levels (from B2 §Master Esik Tablosu)

| Level | Core Leviathan | Discussion | Quorum |
|-------|---------------|------------|--------|
| Routine | 60% | 24h | — |
| Important | 66% | 48h | — |
| Constitutional | 75% | 72h | — |
| Mission | 90% | 90 days | 50% |
| Immutable | 95% | — | 75% (or Fork) |

## Next Steps

- [ ] Solidity implementations (Faz 4)
- [ ] Hardhat/Foundry project setup
- [ ] Avalanche Fuji testnet deployment
- [ ] Integration tests with governance identity export
