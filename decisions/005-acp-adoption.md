---
adr: 005
title: Agent Orchestration via ACP (Agent Client Protocol)
status: proposed
date: 2026-05-11
authors: [Mimar, Companion]
supersedes: null
superseded_by: null
---

# ADR 005 — Agent Orchestration via ACP

## Context

Leviathan needs to host AI agents that participate in forum discussions, vote on proposals, run validator alignment checks, and (eventually) coordinate across specialized Leviathan instances. Several AI agents are candidates: Claude (via Claude Agent SDK / Claude Code), Gemini CLI, OpenAI Codex CLI, GitHub Copilot, and local models (Ollama).

The existing `dahao-all/simulation/` has demonstrated this pattern works (60+ run logs, Dec 2025 onwards) but uses **custom subprocess integration** — each new AI agent CLI requires its own wrapper code in `agents.py`. This is maintenance-heavy and creates lock-in to specific tool quirks.

Zed (the editor) faces the same problem at IDE scope and has solved it via **Agent Client Protocol (ACP)**. Per Zed docs: *"Zed supports many external agents, including CLI-based ones, through the Agent Client Protocol (ACP). Claude Agent (running Claude Code under the hood, communicating over ACP), Gemini CLI (Google reference impl), Codex CLI (OpenAI)..."*

The pattern: agents run as separate processes, communicate over ACP, get tool access via MCP forwarded through ACP.

## Decision

**Leviathan adopts ACP (Agent Client Protocol) as the standard interface for AI agent orchestration.** A `LeviathanOrchestrator` component (refactored from `dahao-all/simulation/supervisor.py`) launches agents over ACP, routes messages, manages session state.

Supported agents in Phase 4 (initial):
- **Claude** (via Claude Agent SDK)
- **Gemini CLI** (Google reference ACP implementation)
- **Codex CLI** (OpenAI ACP implementation)
- **Ollama-local validator** (custom ACP wrapper around local LLM)

Additional agents can be added via ACP config without touching orchestrator code.

ACP is paired with MCP (ADR-006) — ACP for process management, MCP for tool/data access.

## Rationale

1. **Battle-tested pattern.** Zed runs this in production; three open-source reference implementations exist (Claude Agent SDK, Gemini CLI, Codex CLI).

2. **Reduces dahao-all migration cost dramatically.** Current `supervisor.py` is 1953 lines, much of which is subprocess management. ACP standardizes that layer → orchestrator drops to ~300-500 lines, focused on Leviathan-specific orchestration logic.

3. **New agent = config change, not code change.** Adding Llama4 local or a new commercial model becomes an `agent_servers` entry, not a new Python file with subprocess wiring.

4. **Separation of concerns.** ACP handles "which agent, how to start, how to talk to it." Leviathan's own logic (governance, validator alignment, forum integration) stays in higher layers.

5. **Filesystem access semantic.** ACP agents have "full filesystem access" per Zed docs — useful for agents that need to read/write proposal drafts, fork their personalized constitution copies, etc.

6. **Future-proof.** ACP is becoming a standard in the agent ecosystem; choosing it positions Leviathan inside the emerging conventions rather than building a bespoke layer.

## Alternatives considered

### Alternative A: Continue custom subprocess integration (current dahao-all pattern)
**Rejected because:** maintenance burden grows linearly with agent count; quirks per CLI tool leak into orchestrator code; no standard ecosystem to lean on.

### Alternative B: Use only MCP, no ACP layer
**Rejected because:** MCP is for tool/data access (capability), not for agent process management (orchestration). Trying to do both via MCP conflates two different concerns and reinvents what ACP already standardizes.

### Alternative C: Build a custom Leviathan agent protocol
**Rejected because:** premature standardization; would isolate Leviathan from ACP ecosystem (Zed, Claude Code, etc.); no clear differentiation value over ACP.

### Alternative D: A2A (Agent-to-Agent Protocol, Google)
**Considered, partly deferred:** A2A is for agent-to-agent coordination + agent cards + cross-system discovery. Useful for Phase 3+ (cross-Leviathan federation). Not the right primitive for "launch a Claude/Gemini/Codex agent process and talk to it" — that's ACP's lane.

## Consequences

### Positive
- Single integration point for all AI agents
- Adding new agents is a config-level operation
- Aligned with broader agent ecosystem (Zed, Claude Code, others adopting ACP)
- Cleaner orchestrator code → easier to audit, test, evolve
- Filesystem access semantic enables agent forking patterns (each agent reads its own fork.yaml)

### Negative
- Dependency on ACP spec stability — must track ecosystem evolution
- Refactoring `dahao-all/simulation/supervisor.py` is real work (Phase 1.5 or Phase 4)
- Some agents may not have ACP wrappers yet — custom ACP-to-CLI shims needed for those
- Process management complexity (start/stop/recover) shifts from custom code to ACP semantics — learning curve

### Neutral
- Existing dahao-all logs become historical reference; new orchestrator behavior may differ subtly (e.g., timeouts, error handling) — not pro/con, just transition reality

## Scope (initial, can extend)

In scope for Phase 1.5 / Phase 4:
- Launch + tear down agent processes over ACP
- Route messages between orchestrator and agents
- Configure each agent's personalized fork (different fork.yaml per agent)
- Connect agents to MCP server (per ADR-006) for forum/chain/validator access
- Logging + audit trail of agent actions

Out of scope for now:
- Cross-Leviathan agent communication (deferred to A2A, Phase 3+)
- Agent payments (deferred to x402 or LVTN-native, Phase 6+)
- ACP-level identity/reputation (deferred to ERC-8004 adapter, ADR-007 pending)

## Sources

**Primary reference (user-provided, 2026-05-11):**
- Zed external agent documentation: `https://zed.dev/docs/ai/external-agents`
- Quoted: *"Zed supports many external agents, including CLI-based ones, through the Agent Client Protocol (ACP). Claude Agent (Claude Code), Gemini CLI (Google reference impl), Codex CLI (OpenAI), GitHub Copilot..."*

**ACP reference implementations (mentioned in Zed docs):**
- Claude Agent SDK (Anthropic) — runs Claude Code under the hood
- Gemini CLI (Google) — reference ACP implementation
- Codex CLI (OpenAI)

**Internal repo evidence:**
- `dahao-all/simulation/supervisor.py` (1953 lines) — current custom subprocess pattern, becomes ACP-based after refactor
- `dahao-all/simulation/agents.py` — current per-agent integration code
- `dahao-all/simulation_*.log` files — proof the current pattern works (60+ runs)

⚠️ ACP spec details (stdio vs WebSocket, exact message format) not documented in Zed external-agents page reviewed; verify against current ACP spec or reference implementation source before implementing.

## Related

- ADR-006 (MCP server for Leviathan capabilities) — paired decision
- ADR-007 (ERC-8004 adapter) — pending audit
- Plan: `plans/phase-4-agent-participants.md` — implementation target
- Goal file: `dahao_goal.md` — Q18-22 cover migration map
- Future ADR: A2A adoption (Phase 3+ for cross-Leviathan)

## Revisit conditions

Re-examine if:
- ACP spec changes incompatibly between reference implementations
- A more widely-adopted standard emerges (A2A absorbs ACP, or new protocol displaces it)
- Performance limits hit (e.g., orchestrating >50 agents simultaneously)
- Custom Leviathan-specific protocol becomes necessary for cross-L1 features ACP doesn't cover
