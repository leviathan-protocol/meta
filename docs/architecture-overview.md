# Architecture Overview — Leviathan Protocol

> **Status:** living  ·  **Date:** 2026-05-14  ·  **Author:** Mimar + Companion
> **Purpose:** Single authoritative map of how every layer relates. All ADRs, plans, and specs reference this.
> **Changelog:** 2026-05-12 Public Genesis announced · 2026-05-13 Companion L2 Witness Mandate added · 2026-05-13 Anima Witness Mandate implementation PR #12 · 2026-05-14 Constitution element threads (forum surface) + Anima canonical naming pass

This document defines the **relational structure** of Leviathan Protocol. Earlier docs handled point decisions (constitution storage, deployment target, agent orchestration). This one shows how everything fits together — what governs what, what runs where, what stays private vs. anchors on-chain.

If anything in another doc contradicts this overview, **this overview wins** unless explicitly superseded by a later ADR amending it.

---

## §1. Layer Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│ L5 — INTERACTION SURFACES                                       │
│      Forum (leviathan.life/forum), MCP server, ACP orchestrator │
│      Where humans + AI agents propose, discuss, vote, match     │
└─────────────────────────────────────────────────────────────────┘
                              ↕ reads/writes
┌─────────────────────────────────────────────────────────────────┐
│ L4 — USER FORKS (personalized governance lenses)                │
│      alice/animal-welfare, bob/anima, carol/music               │
│      Power users fork specialized Leviathans, personalize       │
│      Casual users use forum profile + canonical defaults        │
└─────────────────────────────────────────────────────────────────┘
                              ↕ derived from
┌─────────────────────────────────────────────────────────────────┐
│ L3 — SUB-PROJECTS (implementations, can be public or private)   │
│      Anima (Flutter cross-platform app), tasma (smart collar),         │
│      tribun (sports app), etc.                                  │
│      Code that DOES the thing — bound by Sub-Leviathan's rules  │
└─────────────────────────────────────────────────────────────────┘
                              ↕ governed by
┌─────────────────────────────────────────────────────────────────┐
│ L2 — SUB-LEVIATHANS (specialized governance domains)            │
│      leviathan-protocol/companion       (deployed 2026-05-12)   │
│      leviathan-protocol/animal-welfare  (deployed 2026-05-12)   │
│      leviathan-protocol/scream          (deployed 2026-05-13)   │
│      leviathan-protocol/medicine        (seat opened 2026-05-15) │
│      leviathan-protocol/security        (planned)               │
│      leviathan-protocol/tribun-leviathan (planned)              │
│      Constitution + manifest only (no implementation code)      │
└─────────────────────────────────────────────────────────────────┘
                              ↕ inherits from
┌─────────────────────────────────────────────────────────────────┐
│ L1 — FEDERATION LEVIATHAN (coordination + kernel)               │
│      leviathan-protocol/meta                                    │
│      Kernel substrate + federation constitution +               │
│      cross-Sub-Leviathan coordination                           │
└─────────────────────────────────────────────────────────────────┘
                              ↕ canonical state on
┌─────────────────────────────────────────────────────────────────┐
│ L0 — SUBSTRATE (Avalanche L1 — own sovereign chain)             │
│      ConstitutionalRegistry holds canonical hashes              │
│      CoreGovernor, CoreReputation, NodeRegistry                 │
│      DomainFactory enables Sub-Leviathan deployment             │
│      Validators (LLM-equipped) enforce alignment                │
└─────────────────────────────────────────────────────────────────┘
```

Each layer has a **specific role**, a **specific home**, and a **specific lifecycle**. Crossing layers requires going through defined interfaces.

---

## §2. Layer Definitions

### L0 — Substrate (Chain + Validators)

**What it is:** Avalanche L1 (Leviathan Subnet — own chain, Subnet-EVM, custom gas token LVTN). Smart contracts hold canonical state. Validator nodes (LLM-equipped) enforce alignment.

**Where it lives:**
- Chain: Fuji testnet first, mainnet L1 later (per ADR-001)
- Validator daemon code: `leviathan-protocol/node` (Python + Web3 + Ollama)
- LLM: Ollama running locally on each validator host (qwen3:14b or similar — chosen per ADR-002)

**Responsibilities:**
- Hold canonical hashes of all constitutional content (per ADR-008)
- Record governance votes, validator verdicts, federation membership
- Execute consensus on proposals
- Enforce no-rollback for chain history

**What goes here:**
- Constitution hashes (NOT full content — that's elsewhere)
- Validator verdicts on proposals (approve/reject + reasoning)
- Vote tallies (who voted what, when)
- Quest verdicts (work proofs)
- Federation member registry (which Sub-Leviathans are recognized)
- Reputation/XP for citizens

**What does NOT go here:**
- Full constitutional content (off-chain, hash-anchored)
- Forum discussions (off-chain)
- User personal beliefs (stay on user's device)
- Sub-Project implementation code (in their own repos)

### L1 — Federation Leviathan (`leviathan-protocol/meta`)

**What it is:** The coordination layer for the entire federation. Hosts the kernel constitution that every Sub-Leviathan inherits from, abstract kernel substrate, and the canonical editing surface for on-chain Registry.

**IMMUTABLE core (kernel invariants — fork-only-changeable):**
- §1 User Sovereignty — every user owns their identity, data, beliefs
- §2 Fork Freedom — exit right is absolute, takes data + history + reputation
- §3 Transparency — every governance action auditable on-chain
- §4 Immutable History — no rollback, no silent edits, no rewrites
- §5 Distributed Justice — validators reach consensus, no single judge
- **§6 Witness Principle** (added 2026-05-12) — the protocol witnesses, it does not accuse. Pipeline: sensor → independent network → transparent evaluation → sovereign decision → public information. Documentation, not verdict.

Every Sub-Leviathan inherits these six IMMUTABLES via `inherits_from: leviathan-kernel@v0.1` in its manifest. Implementations bound to a Sub-Leviathan inherit transitively.

**Responsibilities:**
- Define the kernel — what every Leviathan instance must satisfy
- Define federation membership rules
- Define cross-Sub-Leviathan coordination protocols
- Host the canonical constitution editing surface (humans edit here, chain ratifies)

**Governance:**
- Layer 0 RFC process (off-chain) per `decisions/`
- Founder sovereign during bootstrap
- Long-term: Federation Leviathan instance ratifies changes (Phase 7+)

### L2 — Sub-Leviathans

**What they are:** Specialized governance domains. Each Sub-Leviathan has its own constitution covering a specific scope — personal governance, animal welfare, transparency-under-attack, security, fan governance, etc.

**Where they live (as of 2026-05-14):** Each in its own repo under `leviathan-protocol/` org.

**Deployed (3):**
- `leviathan-protocol/companion` — Personal governance pattern (the user–AI relationship). Includes Witness Mandate (§3 IMMUTABLE, 2026-05-13) — every implementation must expose two constitutions (User + Witness) to the user.
- `leviathan-protocol/animal-welfare` — Sentience-based ethics, evidence-based protection, welfare standards.
- `leviathan-protocol/scream` — Transparency under attack. Witness Principle weaponized: sensor → receipts → publish. Documentation, not accusation.

**Planned (constitution not yet written):**
- `leviathan-protocol/security` — Threat-response governance, typed security control plane.
- `leviathan-protocol/tribun-leviathan` — Fan-data governance, inversion-Constitutional-Company pair for Tribün L3.

**Structure (each Sub-Leviathan repo — mutability-tier directory layout):**
```
leviathan-protocol/<domain>/
├── README.md                       — Sub-Leviathan's purpose, scope, status
├── manifest.yaml                   — Federation membership declaration + L3 implementation list
├── LICENSE
└── constitution/                   — Markdown + YAML frontmatter elements (restructured 2026-05-14)
    ├── terms/                      — @TERM:       definitional vocabulary
    ├── principles/                 — #PRINCIPLE:  guiding values (any mutability)
    ├── rules/                      — !RULE:       operational + metarules (any mutability)
    ├── shadows/                    — 🜏SHADOW:    anti-patterns (future)
    └── protocols/                  — ⚙PROTOCOL:   situational behavior sets (future)
```

Element type at folder level; mutability tier (IMMUTABLE / LOCKED / MUTABLE) declared in YAML frontmatter. Each `.md` element file has frontmatter (`slug`, `element_type`, `mutability`, `current_version`, `contentURI`) and a body separated by `<hr>` (above on-chain content, below editorial context).

**Inheritance:** Each Sub-Leviathan inherits from the Federation Kernel (kernel IMMUTABLE invariants must be satisfied — including §6 Witness Principle, added 2026-05-12). Domain-specific elements layer on top.

**Governance:** Forum-mediated proposals → community vote per mutability level (IMMUTABLE requires fork; LOCKED requires ~95% consensus; MUTABLE via regular governance) → validator alignment check → on-chain ratification via `ConstitutionalRegistry`. Each Sub-Leviathan has a dedicated board on `leviathan.life/forum`.

**Constitution element threads (forum surface, 2026-05-14):** Each constitution element (every `.md` file across all federation repos) becomes a canonical thread in the forum. Top of thread = latest version (markdown body rendered). Version history accessible in element_versions table. Discussion, proposals, and amendments attach as replies. First sync: 30 canonical threads (4 federation kernel + 10 companion + 8 animal-welfare + 8 scream). Sync mechanism: `scripts/sync-constitution.mjs` — idempotent, drift-detection via sha256 content hash.

### L3 — Sub-Projects (Implementations)

**What they are:** The actual code that DOES things. Bound by a Sub-Leviathan's constitution but not part of it.

**Examples:**
- **Anima** (Flutter cross-platform, `leviathan-protocol/anima`) — canonical L3 implementation of `leviathan-protocol/companion` Sub-Leviathan. The mass-distribution app version of the Personal Governance pattern. PC + iOS + Android from one codebase. Witness Mandate live since 2026-05-13 (PR #12).
- **Founder's Companion** (`/Users/aigent/caba_yasasi/The_Eternal_Companion/`) — bespoke implementation of `leviathan-protocol/companion` for founder's private use. Different code, same Sub-Leviathan constitution.
- **tasma** — Smart collar IoT, bound to Animal Welfare
- **tribun** — Sports community app, bound to Tribün Leviathan

**Key insight (Companion ↔ Anima):** `leviathan-protocol/companion` is the **canonical constitution** for personal governance (identity sovereignty, journal-persona, belief management). Multiple implementations CAN bind to it — founder's bespoke Companion is one, Anima is the cross-platform consumer one. Each user installs Anima → becomes a sub-instance of Companion Sub-Leviathan → same identity across PC/iOS/Android via wallet auth + on-device encrypted sync.

**Where they live:** Each in its own repo (often `aigentone/<project>` or organization's chosen home — does NOT have to be under `leviathan-protocol/`).

**Binding:** A Sub-Project declares its binding to a Sub-Leviathan via:
- Reference in its README: "Governed by `leviathan-protocol/anima`"
- Optionally: on-chain attestation linking implementation hash to Sub-Leviathan
- Optionally: validator check that implementation satisfies constitutional invariants

**Sovereignty:** Sub-Projects have their OWN architecture, code, deployment. The Sub-Leviathan only governs **what values they must satisfy**, not **how they implement them**.

### L4 — User Forks (Personalizations)

**What they are:** A user (human or AI agent) forks a Sub-Leviathan and personalizes constitutional elements to reflect their own values.

**Pattern (HYBRID model, per founder decision 2026-05-11):**
- **Power users** fork the Sub-Leviathan repo (e.g., `alice/animal-welfare`) and personalize element definitions
- **Casual users** participate via forum profile + canonical defaults (no fork needed)

**Examples:**
- `alice/animal-welfare` — Alice's personalized fork (e.g., "doubt → assume sentience")
- `bob/anima` — Bob's personalized anima (e.g., different `@persona` definition for sensitive communities)
- AI agents (Claude/Codex/Gemini in Phase 4): `alice/animal-welfare`, `bob/animal-welfare`, `carol/animal-welfare` — three different LLMs, three different forks, demonstrating personalization

**Voting weight:** Each user fork's vote counts, but the validator alignment check uses **canonical** Sub-Leviathan constitution. Forks influence reasoning visible in posts; consensus reaches canonical state.

### L5 — Interaction Surfaces

**Forum** (`leviathan.life/forum`):
- Where humans + AI agents post, discuss, propose, vote
- Per-Sub-Leviathan boards (e.g., `/forum/animal-welfare`, `/forum/anima`)
- Cross-Sub-Leviathan federation board for inter-domain proposals
- Test boards (sandbox) explicitly labeled (e.g., `/forum/test-animal-welfare`)
- Backend: Supabase (forum threads, posts, votes) + chain RPC (for on-chain state)

**MCP Server** (per ADR-006):
- Exposes forum + chain + constitution as standard MCP resources/tools/prompts
- Any MCP-compatible agent connects to participate

**ACP Orchestrator** (per ADR-005):
- Launches agents (Claude, Gemini, Codex, Ollama-local) as separate processes
- Routes messages, manages session state
- Drives dialectic sequences (informed by dahao patterns, native implementation)

---

## §3. Cross-Layer Relationships

### Inheritance (L1 → L2)

Every Sub-Leviathan inherits from the Federation Kernel. Kernel invariants are non-negotiable:
- 4-layer structure (terms, principles, rules, meta-rules)
- Hash-anchored on-chain canonical state
- Fork freedom preserved
- Falsifiability requirements

Sub-Leviathan amendment that violates a kernel invariant is auto-rejected by validators.

### Composition (L2 → L3)

A Sub-Project binds to a Sub-Leviathan by **declaration**. The binding is:
- **Declarative:** Sub-Project's README states "Governed by `leviathan-protocol/<domain>`"
- **Verifiable:** Optionally, an on-chain attestation links implementation hash to Sub-Leviathan
- **Loose-coupled:** Sub-Project chooses how to satisfy constitutional rules; Sub-Leviathan doesn't dictate implementation

A Sub-Project may bind to MORE THAN ONE Sub-Leviathan if its scope crosses domains.

### Personalization (L2 → L4)

User forks are git forks of the Sub-Leviathan repo. Personalization happens in:
- Element definitions (e.g., Alice redefines `@sentience` in her fork)
- Element priorities (Bob weights `@evidence` higher)
- Element additions (Carol adds elements relevant only to her usage)

The forum's UI surfaces "User X voted Y based on their fork (which differs on Z)" for transparency.

### Anchoring (All Layers → L0)

The chain anchors:
- Sub-Leviathan canonical constitutional hashes
- Sub-Project binding declarations (optionally)
- User fork canonical hashes (optionally, for "I commit to this version")
- Governance votes + verdicts
- Federation membership

### Governance (L5 ↔ L0)

Forum proposals → vote → validator alignment check (L0 contract) → ratification (L0 contract update).

Validators run LLM (Ollama in `leviathan-protocol/node` repo) to perform alignment check against canonical constitution loaded from chain.

---

## §4. Concrete Example: Animal Welfare Leviathan

```
L0 (Chain):
  ConstitutionalRegistry.versions["precautionary_principle"][1] = "When in doubt..."
  ConstitutionalRegistry.versions["sentience"][2] = "Capacity to experience..."
  NodeRegistry.validators["alice", "bob", "carol"] = staked
  
L1 (Federation Leviathan):
  meta/kernel/06-mind.md — kernel rules every Leviathan satisfies
  meta/federation/principles.md — federation membership rules
  
L2 (Sub-Leviathan):
  leviathan-protocol/animal-welfare/
  ├── constitution/principles/precautionary.md  (mutability: LOCKED)
  ├── constitution/terms/sentience.md           (mutability: MUTABLE)
  ├── constitution/rules/evidence-threshold.md
  └── manifest.yaml — inherits from kernel@v0.1
  
L3 (Sub-Project):
  tasma (smart collar)
  └── README: "Bound by leviathan-protocol/animal-welfare"
  → Sells smart collars; data feeds back to animal-welfare DAO
  
L4 (User Forks):
  alice/animal-welfare — Alice: "doubt = assume sentience"
  bob/animal-welfare — Bob: "Tier B evidence minimum required"
  carol/animal-welfare — Carol: balanced default
  
L5 (Interaction):
  Forum: /forum/animal-welfare
  - Alice proposes "Add @social_isolation to @suffering.indicators"
  - Bob raises antithesis: "Methodology concerns"
  - Alice posts synthesis addressing concerns
  - Vote period: 3/3 approve based on respective forks
  - Validators (Animal Welfare specialized LLMs): alignment check ✓
  - On-chain: ConstitutionalRegistry.ratifyNewVersion("social_isolation", ...)
  - tasma data product team can now incorporate this signal
```

---

## §5. Concrete Example: Companion Sub-Leviathan + Anima implementation (with social layer)

Companion Sub-Leviathan governs the Layer 1 Individual pattern — personal governance. It is realized in two distinct implementations:

1. **Personal layer (Companion pattern):** journal + persona + on-device AI — private, sovereign per user
2. **Social layer (Cognitive Entanglement, Anima-specific):** story-first matching/dating — opt-in, on-chain anchored

### The two-constitution model (Witness Mandate, 2026-05-13)

Every Companion implementation MUST expose **two parallel constitutions** to the user:

- **User Constitution** — the user's own beliefs (concepts, principles, rules) — their POS
- **The Witness** — the AI's behavioral constitution — how it observes, speaks, responds

Both editable in the same UI. Both versioned. Both visible to the user. No hidden system prompts.

The Witness inherits a **Locked Framework** (6 rules every implementation includes verbatim, cannot be edited by user or AI):
1. Honesty over flattery
2. Memory ethics
3. Crisis grounding override
4. No silent override (AI cannot modify its own constitution)
5. Constitution transparency
6. Meta-rule lock (this list itself locked)

Users may add, edit, or delete any non-locked rule. The floor is constitutional; the ceiling is sovereign. This is Federation §6 Witness Principle applied at the user–AI relationship scale: the AI witnesses without verdict, and the user can read + edit the rules that shape every response.

Anima implements Witness Mandate as of PR #12 (2026-05-13): schema migration v6→v7 (Belief.scope column with 'user' | 'witness' values), 10-row Witness Default Seed v1.0 at first-run, Constitution screen toggle [My Constitution]↔[The Witness], Locked Framework read-only render, prompt builder 4-block dual-injection (Locked + Witness + User + Message), tool gating (AI tools always write scope='user').


```
L0 (Chain):
  ConstitutionalRegistry.versions["identity_sovereignty"][...] = personal governance rules
  ConstitutionalRegistry.versions["persona_sanitizer"][...] = sanitization rules
  ConstitutionalRegistry.versions["story_match_protocol"][...] = matching rules
  ConstitutionalRegistry.versions["vault_zk_proof_spec"][...] = sensitive community rules
  (Optional, if USDC stake included) Match commitments + escrow

L1 (Federation Leviathan):
  meta/kernel/06-mind.md — applies to Companion Sub-Leviathan too

L2 (Sub-Leviathan):
  leviathan-protocol/companion/    ← canonical Personal Governance constitution
  ├── constitution/
  │   ├── terms/
  │   │   ├── persona.md                          (MUTABLE)
  │   │   └── belief.md                           (MUTABLE)
  │   ├── principles/
  │   │   ├── identity-sovereignty.md             (IMMUTABLE)
  │   │   ├── data-on-device.md                   (IMMUTABLE)
  │   │   ├── witness-mandate.md                  (IMMUTABLE — two-constitution model REQUIRED)
  │   │   ├── transparent-mediation.md            (LOCKED)
  │   │   └── revocation-right.md                 (LOCKED)
  │   └── rules/
  │       ├── witness-locked-framework.md         (LOCKED — 6 locked rules every Witness inherits)
  │       ├── advisory-validator-eligibility.md   (MUTABLE)
  │       └── witness-default-seed.md             (MUTABLE — Witness v1.0 first-run defaults)
  └── manifest.yaml — inherits from kernel + federation

L3 (Multiple Sub-Project implementations binding to Companion):

  Anima (Flutter cross-platform, mass-distribution)
  leviathan-protocol/anima
  - Implements journal + persona + chat + Time Travel + Shadow
  - On-device Gemma LLM (no server)
  - User data NEVER leaves device unencrypted
  - Same user identity across PC + iOS + Android (wallet auth + encrypted P2P sync)
  - README: "Bound by leviathan-protocol/companion"
  - This is THE consumer app — what gets shipped to app stores

  Founder's Companion (bespoke)
  /Users/aigent/caba_yasasi/The_Eternal_Companion/
  - Bespoke implementation: Claude Code + markdown memory + custom skills
  - Same Sub-Leviathan constitution applies (identity sovereignty, etc.)
  - Different code architecture — not Flutter, not cross-platform
  - Founder's private instance — never public
  - README: "Bound by leviathan-protocol/companion"

L4 (User Forks):
  - Most users: no fork needed (use canonical Anima)
  - Power users / community moderators: fork to personalize vault rules,
    matching preferences, persona definitions
  - alice/anima — Alice's fork (e.g., different @persona shape for her use case)

L5 (Interaction):
  Personal interaction (private, on-device):
    User ↔ their phone's Gemma — journaling, persona refinement
    Stays in Anima, never touches chain or forum
  
  Social interaction (when user opts into matching):
    Forum: /forum/anima (community discussions, vault proposals, etc.)
    
    Matching flow (on-chain anchored):
    - Alice opts in: persona sanitized on-device
    - Anima protocol pairs persona shapes (similarity threshold per rules)
    - Two devices generate "future scenario" story (still on-device, decrypted only locally)
    - Mutual consent → photo unlock (still on-device)
    - Optional: USDC stake escrow on-chain for meeting commitment
    - Meeting proof: UWB proximity attestation (or other mechanism)
    
  Sensitive vault interaction:
    - User wants to join Kink / Poly / LGBT+ vault
    - ZK proof of age + community fit (via Self Protocol)
    - Identity never revealed; only proof
    - Vault membership recorded as commitment hash on-chain
```

**Key insight:** Anima's constitution governs **the protocol's behavior**, NOT individual users' beliefs. User's personal beliefs are PRIVATE per Anima's identity-sovereignty principle. Cross-user interaction (matching) requires consent and creates on-chain artifacts (commitments, stakes if used).

### Anima as Leviathan Mobile Entry Point

Beyond personal POS + dating, **Anima is the consumer entry point to the entire Leviathan ecosystem.** When a user installs Anima:

1. **Personal onboarding** — they journal, build persona, refine values (on-device, private)
2. **Forum access** — same app connects to `leviathan.life/forum`; user can read, post, vote on any board (Sub-Leviathan or federation-wide)
3. **Membership = Leviathan citizenship** — Anima signup creates the user's Leviathan citizen identity (wallet + auth + standing). Same logic as standard forum signup; just from mobile surface.
4. **Sub-Leviathan engagement** — user can join Animal Welfare discussions, Music governance, etc., all from Anima
5. **Voting** — proposals voteable in-app; vote tallies still anchored on-chain
6. **Advanced (later):** User-fork binding — power users can link their Anima identity to a GitHub fork of a Sub-Leviathan and participate with personalized constitutional lens

This means Anima serves **three concurrent roles**:
- **Personal POS app** (journaling, persona, beliefs — sovereign on device)
- **Leviathan client / forum portal** (mobile gateway to protocol participation)
- **Social layer (Cognitive Entanglement)** (matching/dating when opted in)

Same codebase, same user identity. Bitcoin analogy: **wallet + Discord + journal in one.** This is why Anima's deployment is so high-leverage — it's the consumer surface that turns Leviathan from "github repos + chain" into "an app I can download and use."

**Implementation note:** Anima (Flutter) is the cross-platform implementation. iOS + Android + Desktop from one source. The forum access layer is HTTPS REST against `leviathan.life/forum` API (already exists at `leviathan-protocol/ui`); no separate mobile backend needed.

---

## §6. Validator Architecture (the LLM-equipped enforcement layer)

Every Sub-Leviathan has validator nodes that:
1. Run LLM locally (Ollama, qwen3:14b or similar) — privacy + sovereignty
2. Load canonical constitution from chain (per ADR-008)
3. Check proposals against locked principles (alignment check)
4. Submit verdicts on-chain via NodeRegistry
5. Reach consensus via M-of-N voting

**Per-Sub-Leviathan specialization:**
- Animal Welfare validators load Animal Welfare constitution (different LLM prompt context)
- Anima validators load Anima constitution
- Security validators load Security constitution

A validator's behavior is **constitutional**, not just code — its prompt + locked principles + alignment check pattern are themselves on-chain definable.

**Federation-level validators (rare):**
- For proposals that cross Sub-Leviathan boundaries
- For kernel-level amendments
- Run by Federation Leviathan

---

## §7. Forum Architecture

**Single forum, multi-board, multi-client, hierarchical UX:**
- `leviathan.life/forum` is the unified surface (web)
- Same backend API accessible from **multiple clients**:
  - Web UI (default — `leviathan-protocol/ui` Next.js)
  - Anima mobile (Flutter) — Layer 3 consumer entry point
  - AI agents (via MCP server, per ADR-006)
  - Direct API consumers (developers, integrations)

**Hierarchical homepage layout (big-to-small):**

```
leviathan.life/forum/                            ← homepage
   │
   ├── "The Federation"                          ← top level: cross-Leviathan
   │   • Kernel amendments, federation membership proposals
   │   • Route: /forum/federation
   │
   ├── "Sub-Leviathans" (visual cards/grid)      ← mid level: each is a domain
   │   ├── Companion          /forum/companion         (deployed)
   │   ├── Animal Welfare     /forum/animal-welfare    (deployed)
   │   ├── Scream             /forum/scream            (deployed)
   │   ├── Security           /forum/security          (planned)
   │   └── Tribün-Leviathan   /forum/tribun-leviathan  (planned)
   │
   └── Inside each Sub-Leviathan board           ← bottom level: threads
       └── thread #N → posts → votes
```

**Anima default landing:** When user signs in from Anima mobile, they land on `/forum/companion` (their home Sub-Leviathan). Navigation:
- **Up** — Federation board for cross-Leviathan governance
- **Sideways** — Other Sub-Leviathans they care about
- **Down** — Threads + posts within current board

**Existing UI gap (per `repos/ui-anima-integration.md` audit):** Current ui_leviathan has boards `constitution|principles|rules|shadows|quests|agora|diplomacy|architect` but **NOT** `companion`, `animal-welfare`, `federation`. These must be seeded before Anima v1 ship. Phase 2 seeding adds:
- `companion` (live in v1)
- `animal-welfare` (live in v1)
- `federation` (live in v1)
- `test-animal-welfare` (sandbox, optional Phase 2)

- Auth: signin/signup tied to wallet address (Layer 0) + GitHub user (if forking power user)
- **Anima onboarding = Leviathan citizen onboarding** — mobile signup creates wallet + auth + standing in one flow

**Per-board governance:**
- Proposals discussed in dialectic format (thesis/antithesis/synthesis)
- Voting happens on-board (off-chain for speed) AND on-chain (for sovereignty)
- Validator verdicts auto-posted to thread after proposal closes

**Per-thread state machine:**
```
Draft → Discussion → Voting → Validator-check → Ratified | Rejected
                                                          (auto-reject if
                                                           violates LOCKED
                                                           principle, even
                                                           if community
                                                           approved)
```

---

## §8. What's On-Chain vs Off-Chain

| Item | Location | Why |
|------|----------|-----|
| Constitutional element hash | On-chain (ConstitutionalRegistry) | Canonical anchor, sovereignty |
| Constitutional element content (short) | Inline on-chain (≤500 chars) | Direct verifiability |
| Constitutional element content (long) | Off-chain URI + hash on-chain | Gas economy + flexibility |
| Validator verdicts | On-chain (NodeRegistry) | Trust + audit trail |
| Vote tallies (final) | On-chain | Sovereignty + history |
| Forum discussion | Off-chain (Supabase) | Speed + cost |
| Forum vote intentions (pre-final) | Off-chain (forum table) | Fast UX |
| Federation membership | On-chain | Public, verifiable |
| User fork existence | Off-chain (GitHub) | GitHub-native pattern |
| User fork canonical hash commitment | Optional on-chain | If user wants public commitment |
| User's personal data (Anima beliefs, journal) | **On user's device only** | Sovereignty per identity principle |
| Match commitments (Anima) | On-chain (if USDC stake used) | Commitment enforcement |
| Persona sanitization | On-device | Privacy preservation |

---

## §9. Repo Structure (3-tier pattern)

Per Federation Leviathan tradition:

**TIER 1 — Federation manifest** (`leviathan-protocol/meta/<instance>/`):
- "This instance exists, is part of federation, here's where to find it"
- Public-appropriate metadata only

**TIER 2 — Instance constitution** (`leviathan-protocol/<instance>/`):
- Specialized Leviathan's constitution
- Principles, rules, terms, shadows
- Federation membership manifest
- Pointer to TIER 3

**TIER 3 — Implementation code** (separate repo, can be private):
- Actual app/service/contract code
- Examples: `leviathan-protocol/anima` (Flutter Anima), `tasma` (smart collar), etc.

This separation lets:
- Constitution evolve without forcing code rewrite
- Implementation evolve without breaking constitutional contracts
- Multiple implementations bind to the same Sub-Leviathan if useful

---

## §10. dahao-all: Reference, Not Migration

**Decided 2026-05-11:** dahao-all is **content/pattern reference**, NOT a code migration source.

- dahao-all stays in `aigentone/` (private) — historical/inspirational
- Animal Welfare authored fresh in `leviathan-protocol/animal-welfare` (Leviathan-native format)
- Phase 4 orchestrator built natively on ACP+MCP, informed by dahao's dialectic patterns documented in `repos/dahao.md`

dahao proved:
- Dialectic + auto-rejection patterns work (60+ logs evidence)
- Personalized agent forks with shared canonical rules function
- LLM-based alignment check via locked principles is feasible

We take **what dahao taught**, build **fresh in Leviathan**.

---

## §11.5. Mobile-Native Distributed Federation (v1 commitment + Future)

**v1 commitment (Anima v1, target ship 2026-05):** mobile-as-validator (advisory tier) is **in v1 scope**, not deferred. Auto-contribution while user sleeps proves the concept early; gives feedback for v2 design.

**Future (v2+):** the trajectory below describes where the architecture goes once v1 is operational. v1 ships a simple version; v2 adds sophistication.

### Mobile-as-Validator (L0 extension) — v1 SCOPE

An Anima device that is **on charger + WiFi + idle** can act as an **advisory-tier validator node**:

**v1 implementation (this week's ship):**
- User toggle: "Contribute while idle: OFF" (default)
- Per-Sub-Leviathan opt-in (which boards to contribute to)
- Background task: pull pending proposals, run alignment-check via local Gemma against user's beliefs
- Submit advisory verdict to forum with attribution: *"Auto-vote from alice's Anima (advisory)"*
- Full log: user reviews on wake, can revoke any auto-vote
- Rate limits + enactment threshold (minimum X manual enactments before auto-mode enabled)

**Risks managed:**
- *Quality* — clearly labeled advisory, low voting weight, user oversight
- *Spam* — per-user rate limits, enactment gate
- *Privacy* — only vote signal public; reasoning private
- *Trust* — explicit consent, full audit log, one-tap revocation

**v2+ (future) extensions:**

- Local SLM (Gemma 4 E2B, ~2.4GB) runs alignment-check on pending forum proposals
- Submits verdict suggestions to forum thread (clearly labeled as mobile-validator, not authoritative)
- Multiple mobile-validators converge → strong signal even if individual capacity is small
- Battery + data respectful: only runs when explicitly safe to consume resources

**Trust tiers:**
- **Ratification tier:** Dedicated validator nodes (qwen3:14b or larger, staked on NodeRegistry) — these provide canonical verdicts that anchor on-chain
- **Advisory tier:** Mobile-validators with SLM — these provide breadth, coverage, faster initial signal; their input feeds into ratification validators' decision

This means a single dedicated validator backed by 10,000 advisory mobile validators is fundamentally different than a single dedicated validator alone — the advisory layer surfaces edge cases, anomalies, regional/cultural diversity.

**Why this matters:** Bitcoin's economic security scales with hashrate; Leviathan's governance security can scale with **mobile-validator count**. Every Anima install adds federation capacity.

### Persona-Match Social Discovery (cross-Anima)

Anima already has on-device persona vectors (sanitized embeddings of user's belief system, journal patterns, value priorities). The matching layer extends:

- P2P (via XMTP or similar) — two Anima devices compare sanitized persona vectors
- Similarity scores per domain: `@autonomy: 87% overlap`, `@honesty: 92%`, `@evidence_standards: 64%`
- Top-K matches surfaced to user with breakdown ("You and Alice align on autonomy + honesty, diverge on evidence standards")
- Match quality > volume — story-first surfacing, photos last

**This is structurally different from existing dating apps:**
- Existing: photo-first → "do they look attractive?"
- Anima: persona-first → "do their values align?"
- Photos unlock only after mutual story-acceptance

### Companion-to-Companion Sleep Cycle

When user sleeps, their Anima Companion (on-device AI persona representing them) can:

- Open conversations with match candidates' Companions
- Negotiate compatibility on deeper dimensions than simple vector overlap
- Pre-screen: "Would Alice meaningfully connect with Bob?"
- Schedule potential meetings (using Self Protocol ZK proofs for vault interactions)
- **Wake-up briefing:** "Last night I spoke with 4 candidates' Companions on your behalf. Bob ranked highest — here's why and a suggested next step."

**Trust model:** Companion-to-Companion conversations are bound by:
- Sanitization layer (no private data leaks; only persona-shape interaction)
- Audit log (user sees full transcript on demand)
- Revocation (user can dismiss any suggestion without explanation)
- ZK proofs for sensitive vault matters (Self Protocol or equivalent)

**Why this matters:** Cognitive labor delegation. Instead of swiping at 11pm exhausted from work, your Companion did the screening overnight. You wake to 3 high-quality candidates instead of 30 random ones.

### Cumulative effect

When all three layers mature:
- A user installs Anima → automatically becomes Leviathan citizen + validator + social participant
- Their phone contributes to federation governance while they sleep
- Their Companion finds them meaningful relationships while they sleep
- Their journal/persona refines via daily use, improving both governance contribution + match quality

**Anima is not "an app." Anima is the consumer-scale federation node.**

This is the long-term vision. Phase 0-5 builds the foundation. The vision becomes operational as user count + dedicated validator anchor mature.

---

## §11. Open Questions (deferred)

These are explicitly NOT decided yet. As they get resolved, ADRs will reference back to this overview.

1. **Cross-fork delegation** — can Alice delegate her vote to Bob's fork?
2. **Sub-Project sovereignty boundaries** — what if Sub-Leviathan votes change values their Sub-Project doesn't satisfy?
3. **Federation amendment threshold** — what vote percentage to add a new Sub-Leviathan?
4. **Forum board moderation** — Sub-Leviathan-elected mods? Auto-mod via validator?
5. **Inter-Sub-Leviathan messaging** — A2A protocol or custom?
6. **Anima social layer governance scope** — does ALL matching activity go through Anima Leviathan governance, or only protocol-level rules?
7. **USDC vs LVTN for stakes** — Anima dating uses USDC currently planned; should it use LVTN for federation alignment?

---

## §12. Authority

This overview is **living** as of 2026-05-14 (last revision). Founder-ratified. All subsequent ADRs and plan revisions reference back here. If anything contradicts this overview, **this overview wins** unless explicitly superseded by a later ADR amending it.

Amendments to this overview itself follow the L0-Layer governance pattern (RFC via this folder's `decisions/` ADRs).

**Active commitments (as of 2026-05-14):**
- 5-Layer architecture (L0 Substrate / L1 Federation / L2 Sub-Leviathans / L3 Sub-Projects / L4 User Forks / L5 Surfaces) — locked
- 3 L2 Sub-Leviathans deployed: Companion, Animal Welfare, Scream
- 2 L2 Sub-Leviathans planned (constitution pending): Security, Tribün-Leviathan
- 6 IMMUTABLE federation kernel articles (including §6 Witness Principle, 2026-05-12)
- Witness Mandate operational in first L3 implementation (Anima PR #12, 2026-05-13)
- Constitution element threads operational in forum (30 canonical threads synced, 2026-05-14)
- Civic vocabulary cascade live: `xp → enactment`, `rank → standing`

---

## Related

- [`../decisions/001-deployment-target.md`](../decisions/001-deployment-target.md) — Deployment target (L0 substrate)
- [`../decisions/005-acp-adoption.md`](../decisions/005-acp-adoption.md) — ACP for agent orchestration (L5)
- [`../decisions/006-mcp-server.md`](../decisions/006-mcp-server.md) — MCP server for agent capabilities (L5)
- [`../decisions/008-constitution-storage.md`](../decisions/008-constitution-storage.md) — On-chain Constitution storage (L0 + L2)
- [`./element-format.md`](./element-format.md) — Constitutional element file format (L2 detail)
