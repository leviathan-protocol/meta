# federation_alert MCP Tool — Federation Canonical Schema v0.1

**Status:** Federation form-defined (REQUIRED — every instance MUST conform)
**Date:** 2026-05-07
**Lineage:** Condor `send_notification` → Liveprob 3-tier UI → Federation canonical
**Federation principles:** P-1 sub-directory sovereignty + P-7 reasoning trail + P-8 instance sovereignty + Q11 form authority

---

## Tool Signature (Mandatory)

Every federation instance MUST expose an MCP tool matching this signature:

```python
@mcp.tool()
async def federation_alert(
    level: str,                            # REQUIRED: "info" | "warning" | "critical"
    reason: str,                           # REQUIRED: human-readable summary (~1-3 sentences)
    instance_id: str,                      # REQUIRED: caller's $INSTANCE_ID env var
    action_required: bool = False,         # operator decision pending?
    deferred_for_operator: bool = False,   # HARD constraint #8 trigger? (public action requested)
    context: dict | None = None,           # optional structured context (briefing_id, hash, etc.)
) -> dict:
    """Push federation alert to operator-only channel.
    
    Federation requires the SCHEMA (form). Each instance chooses
    backing channel (Telegram / Signal / Matrix / custom) per P-1.
    """
```

## Level Enum (Federation-Defined)

| Level | Use Case | Throttling |
|---|---|---|
| `info` | Stratejik visibility (sprint unlock, manifest publish, milestone) | Rate limit max 5/day |
| `warning` | Operator decision pending (discrepancy, federation health, token cost) | Rate limit max 10/day |
| `critical` | Sistem-level alarm (Phase rollback, security VETO, MR-2 amendment) | NEVER throttle |

## Return Schema

```json
// Success
{"sent": true, "channel": "telegram", "message_id": "1234"}

// Throttled
{"throttled": true, "reason": "rate_limit", "retry_after": 3600}

// Error  
{"error": "<reason>", "deferred": false}

// Anti-impersonation rejection
{"error": "instance_id mismatch: caller=X env=Y"}
```

## HARD Constraints (Federation Discipline)

1. **NEVER public-facing.** Tool MUST send to operator-only channel. Public Telegram channels, social media, public web — all FORBIDDEN. (federation-act-prompt HARD constraint #8)

2. **instance_id anti-impersonation.** Tool MUST verify `instance_id` parameter matches caller's `$INSTANCE_ID` env var. Mismatch → return error, do NOT send.

3. **Audit log mandatory.** Every call (sent OR throttled OR error) MUST append entry to `<instance_repo>/.federation-alert.log` (append-only, JSON lines). P-7 reasoning trail.

4. **Critical level NEVER throttled.** Rate limits apply to info/warning. Critical bypasses all filters.

5. **NEVER fabricate alerts to test the channel.** Each call must reference real federation event. Fabricated/test alerts → audit log review surface, operator review.

6. **Token security.** Channel credentials (Telegram bot token, etc.) MUST be:
   - Stored in env file (gitignored)
   - File mode 600
   - Never logged (httpx default OK)
   - Rotated 90 days

## Implementation Choice (Per-Instance)

Federation does NOT specify:
- Backing channel (Telegram / Signal / Matrix / custom webhook)
- Filter discipline implementation (rate limit algorithm, throttle window)
- Alert formatting (Markdown/HTML/plain)
- 3-tier UI presentation (Liveprob pattern recommended, instance can adapt)
- Audit log format (JSON / YAML / SQLite)

These are per-instance content (P-1 sovereignty + Q10 tool sovereignty + Q11 content authority).

## Reference Implementation

`leviathan-meta/tools/federation-alert-reference/` — Companion's MCP server (federation reference impl, optional starting point).

New instances may:
- Copy and adapt (starting point)
- Roll own (P-1 sovereignty)
- Reuse existing Telegram bot (Liveprob, Security current pattern)

## Example — Three Implementations Same Schema

| Instance | Implementation | Channel | Format |
|---|---|---|---|
| Companion | `tools/companion-mcp/server.py` (reference) | Telegram | Markdown 3-tier |
| Liveprob | `src/liveprob/telegram/` (extend) | Telegram | Markdown + sovereign-phrase |
| Security | Mimar's existing bot (extend) | Telegram | (per Mimar's design) |
| Fast | `tools/codex_fast/mcp/` (Codex tarafı) | Telegram or other | Codex SDK pattern |

All four → same `federation_alert(level, reason, instance_id, ...)` schema. Different backing implementations. Q10 + Q11 operasyonel kanıt.

## Anti-Patterns (Federation Discipline Violations)

❌ **Tool name mismatch.** Tool MUST be named `federation_alert`. Federation parsers detect by name.

❌ **Custom level enum.** Levels MUST be `info`, `warning`, `critical`. Custom levels (urgent, emergency, etc.) NOT federation-canonical.

❌ **Skipping audit log.** Every call MUST append to `.federation-alert.log`. Silent calls = hidden state (P-2 violation).

❌ **Public channel backing.** Even if technically Telegram, sending to public channel = HARD constraint #8 violation.

❌ **Bypassing instance_id check.** Skipping anti-impersonation = federation-wide trust break.

❌ **Cron-driven fabricated alerts.** Federation auto-action MUST NOT call federation_alert just to "ping" the channel. Real events only.

## Versioning

Schema version 0.1 (initial). Future versions will be additive (new optional fields). Breaking changes require MR-2 protected amendment.

## Audit Log Schema

Each entry (JSON line):

```json
{
  "timestamp": "2026-05-08T16:30:00Z",
  "level": "warning",
  "instance_id": "companion",
  "reason": "Discrepancy in briefing 2026-05-08-X",
  "action_required": true,
  "deferred_for_operator": false,
  "context": {"briefing_id": "2026-05-08-X"},
  "result": {"sent": true, "message_id": "1234"}
}
```

Operator weekly review surfaces:
- Alert frequency per instance (notification fatigue check)
- False alerts (audit vs reality)
- Pattern emergence (recurring discrepancies → systemic issue)

## Federation Maturation Path

| Phase | Channel substrate | Vendor concern |
|---|---|---|
| Phase 1.B.1 (now) | Telegram (vendor: Telegram BV) | Accepted transitional |
| Phase 2 | Multi-channel (Telegram + Signal parallel) | Vendor failure tolerance |
| Phase 3 | Self-hosted ntfy / gotify / custom webhook | Federation-sovereign substrate |
| Phase 4+ | Custom federation alert protocol (gRPC/MQTT?) | Full sovereignty |

Schema v0.1 is **channel-agnostic by design** — only the implementation behind `_send_telegram` (or equivalent) changes per phase. Instance code remains stable.
