---
adr: 001
title: Deployment Target — Avalanche L1 Architecture
status: proposed
date: 2026-05-11
authors: [Mimar, Companion]
supersedes: null
superseded_by: null
---

# ADR 001 — Deployment Target: Avalanche L1 Architecture

## Context

Leviathan Protocol needs a blockchain. The `leviathan_node` repo has been built around Avalanche's L1 architecture (Subnet-EVM) and has a local deployment running since 2026-01-30 (chain ID 43210, contracts: forwarder + token + governor). Hardhat config additionally defines `fuji` (Avalanche C-Chain testnet, 43113) and `avalanche` (C-Chain mainnet, 43114) as fallback networks.

The strategic question: **where does Leviathan run in production**, and **where does it run during pre-production** (Phase 1 of the convergence plan)?

Three viable paths were considered. The decision affects every subsequent phase: contract deployment scripts, validator infrastructure, gas economics, sovereignty claims, and the eventual migration story.

## Decision

**Leviathan deploys as its own sovereign Avalanche L1 (formerly "subnet") using Subnet-EVM, in two stages:**

1. **Phase 1 (now):** Leviathan L1 on Avalanche **Fuji testnet** — free/near-free hosting, full architecture, public test environment
2. **Phase X (when migration triggers met):** Leviathan L1 on Avalanche **mainnet** — production sovereignty, ~$330/month subscription + validator infrastructure

The same `avalanche-cli` workflow used for local development scales unchanged to Fuji testnet and (later) to mainnet. **No architectural change between phases — only host environment and economic model change.**

**Avalanche C-Chain (testnet 43113 or mainnet 43114) is explicitly NOT the deployment target.** C-Chain network entries in `hardhat.config.js` are kept only for reference; no contracts will be deployed there.

## Rationale

1. **Test what ships.** Fuji L1 mirrors production architecture exactly. Deploying to C-Chain testnet would have meant testing on one shape and shipping on another — bad practice.

2. **Tooling continuity.** `setup_leviathan_subnet.sh` already uses `avalanche-cli` locally. Same commands deploy to Fuji and mainnet L1. No new tooling to learn for production.

3. **Cost efficiency.** Fuji L1 uses test AVAX from faucets — effectively $0. Avoiding the mainnet L1 subscription (~$330/month) until product-market fit signals justify the spend.

4. **Constitutional Company claim stays intact.** *"Leviathan runs its own chain"* is true on Fuji (testnet) and remains true on mainnet — only the testnet qualifier changes between phases. C-Chain dApp deployment would have weakened this claim during Phase 1.

5. **Sovereignty without payment.** L1 architecture gives own gas token (LVTN), own validator set, own rules — properties C-Chain doesn't offer. Fuji testnet provides this **for free**.

6. **Migration is operational, not architectural.** Mainnet move is a payment + DNS-style cutover, not a rewrite. Same contracts, same scripts, same validator daemons. The migration is a $$$ decision, not a code decision.

7. **Public visibility.** Fuji L1s are discoverable on `subnets-test.avax.network` — anyone can audit transactions and validator behavior. Matches the falsifiability discipline embedded in the protocol itself.

## Alternatives considered

### Alternative A: C-Chain Fuji dApp first, own L1 later
Deploy contracts to Avalanche C-Chain testnet (chain 43113) for Phase 1, migrate to own L1 for production.

**Rejected because:**
- Two different architectures = real migration risk and effort
- Sovereignty claim weakened during Phase 1 (*"we have our own chain — coming soon"*)
- Different validator model (C-Chain uses Avalanche's validators; own L1 uses ours)
- Gas economics differ — UX assumption mismatch between Phase 1 and production
- Forum integration on leviathan.life would have to learn two chain interaction patterns

### Alternative B: Mainnet L1 immediately
Skip testnet, deploy Leviathan L1 directly to Avalanche mainnet.

**Rejected because:**
- ~$330/month subscription before any usage data
- Bugs found in production are expensive
- No room for iteration without real economic consequences
- Premature commitment to specific chain parameters (gas, validator set, etc.)
- Real wallets, real keys, real risk during a learning phase

### Alternative C: Local subnet only (no public deployment in Phase 1)
Keep development on local Avalanche subnet; defer any public deployment.

**Rejected because:**
- No public visibility = no test board demo for visitors
- Validators only test in local conditions (no real latency, no real RPC quirks, no real ops burden)
- Phases 2-5 (test board, validator integration, agents, end-to-end demo) become much harder to validate
- "Bring people to look at this" message has no surface

## Consequences

### Positive
- Production architecture validated in testnet
- Free public demo environment
- Same tooling local → Fuji → mainnet (one learning curve, not three)
- Migration to mainnet is a financial decision, not an engineering one
- Sovereignty claim consistent across all phases
- Falsifiability built in — Fuji L1 explorer is public-auditable

### Negative
- **Validator uptime is our responsibility.** Fuji L1 needs us to run validator nodes; C-Chain would have used Avalanche's. Operational burden falls on our 3-machine fleet (Mac / Kali / Mac Mini) or cloud.
- **L1 setup is more involved** than `npx hardhat run scripts/deploy_fuji.js`. Requires `avalanche-cli` familiarity, C-Chain → P-Chain transfers, validator orchestration.
- **Block explorer choice not free.** `subnets-test.avax.network` is third-party dependency; self-hosted Blockscout is ops burden. (To be resolved in ADR-003.)
- **Avalanche tooling evolves.** Must track Builder Hub releases between Avalanche9000/Etna era and current.
- **Cross-L1 messaging** (Warp / Teleporter) becomes relevant if Leviathan L1 needs interop with C-Chain or other L1s — additional complexity if scope grows.

### Neutral
- LVTN as own gas token (rather than AVAX gas) — pro for sovereignty, slight UX learning curve for users used to paying gas in AVAX. Not strictly better or worse, just a trade.

## Migration triggers (Fuji L1 → Mainnet L1)

Mainnet L1 deployment is gated on **all three** of the following being demonstrated on Fuji L1:

1. **Technical proof:** At least one real PR merged into a public Leviathan repo via the full validator consensus flow (proposal → discussion → vote → validator alignment → on-chain verdict → merge). This proves the kernel works end-to-end.

2. **Operational proof:** ≥20 successful governance cycles completed on Fuji L1 with ≥99% validator uptime over a 30-day window. This proves the operational pattern is sustainable.

3. **Financial proof:** Committed funding covering ≥12 months of mainnet L1 ops (Avalanche subscription ~$330/mo × 12 = $3,960 minimum, plus validator infra ~$200-500/mo, plus contingency). This proves it can be sustained.

Hitting all three triggers a **new ADR** for mainnet deployment specifics — initial validator set, token distribution mechanics, hard cutover vs phased migration, on-chain hash anchoring of pre-migration state, etc.

## Sources

**External research (user-provided, 2026-05-11):**

> *"In 2026, Avalanche has evolved its 'Subnets' into 'Avalanche L1s' (following upgrades like Avalanche9000/Etna). These are sovereign, customizable blockchains (often EVM-compatible via Subnet-EVM) with their own validators, token economics, gas tokens, rules, and performance isolation. Fuji Testnet is the primary public test environment for deploying and testing your own Avalanche L1s (formerly subnets)."*

- Avalanche Builder Hub — Deploy on Fuji Testnet:
  `https://build.avax.network/docs/tooling/avalanche-cli/create-deploy-avalanche-l1s/deploy-on-fuji-testnet`
- Avalanche L1 Explorer (testnet): `https://subnets-test.avax.network`
- Background: Avalanche9000 / Etna upgrades (2024-2025) renamed "Subnets" → "Avalanche L1s" and unlocked sovereignty features

**Internal repo evidence:**
- `leviathan_node/scripts/setup_leviathan_subnet.sh` — local L1 setup script, proves `avalanche-cli` workflow already in use
- `leviathan_node/contracts/hardhat.config.js` — defines `leviathanSubnet` (local), `fuji`, `avalanche` networks
- `leviathan_node/contracts/deployments/leviathan_subnet.json` — local L1 deployment record (chain 43210, deployed 2026-01-30)
- `leviathan_node/CLAUDE.md` — documents the L1 architecture intent (DomainFactory, NodeRegistry, etc.)

⚠️ Avalanche tooling evolves between major releases. Verify against current Builder Hub docs before each deploy step — APIs, CLI flags, and network names may shift.

## Related

- Plan: `plans/phase-1-chain-fuji.md` (rewritten to reflect this decision, dated 2026-05-11)
- Plan: `plans/phase-0-constitution.md` (must complete before Fuji L1 deployment)
- Future ADR: `decisions/002-validator-count-fuji.md` — N validators for Fuji L1
- Future ADR: `decisions/003-block-explorer.md` — `subnets-test.avax.network` vs self-hosted
- Future ADR: deployment to mainnet — written when migration triggers met
- Goal file: `leviathan_node_goal.md` — Q34, Q35, Q36 cover Fuji readiness research

## Revisit conditions

Re-examine this decision if:
- Avalanche L1 architecture changes significantly (next major version after Avalanche9000)
- Subnet-EVM is deprecated or replaced
- Mainnet L1 subscription model changes materially (e.g., pricing 10x change, free tier introduced, or removed)
- Cross-L1 messaging requirements become so complex that staying on C-Chain becomes cheaper than the complexity
- Validator uptime burden exceeds founder + agent capacity for >2 consecutive months
- An incident on Fuji L1 reveals an architectural flaw rather than an operational issue
