#!/usr/bin/env python3
"""
Companion MCP Server — Phase 1.B.1 federation_alert tool implementation.

This is the federation reference implementation (optional starting point for
new instances). Per-instance customization expected (Liveprob, Security have
their own existing patterns).

Federation principles applied:
  - P-1 sub-directory sovereignty (writes only to companion's own log)
  - P-7 reasoning trail (every call audited, append-only)
  - P-8 instance sovereignty (anti-impersonation check)
  - Q11 form authority boundary (federation form, instance content)
  - HARD constraint #8 (operator-only channel, no public-facing)

Pattern lineage:
  - Condor (hummingbot/condor mcp_servers/condor/server.py) → send_notification
  - Liveprob (src/liveprob/telegram/) → 3-tier UI + sovereign-phrase
  - Federation canonical (this file) → schema-conformant, channel-flexible

Schema: leviathan-meta/schemas/federation-alert-mcp.md v0.1

Required env vars:
  INSTANCE_ID            - this instance's id (e.g. "companion")
  INSTANCE_REPO          - absolute path to instance repo root
  TELEGRAM_BOT_TOKEN     - Telegram bot token (operator-only group)
  TELEGRAM_CHAT_ID       - operator-only group chat_id (negative for groups)

Usage (standalone test):
  TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... INSTANCE_ID=companion \\
    INSTANCE_REPO=. python3 server.py --test

Usage (MCP server mode for agent CLI):
  python3 server.py
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

try:
    import httpx
except ImportError:
    print("error: httpx required (pip install httpx)", file=sys.stderr)
    sys.exit(2)


# ── Config from env ──
INSTANCE_ID = os.environ.get("INSTANCE_ID", "")
INSTANCE_REPO = Path(os.environ.get("INSTANCE_REPO", "."))
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID_RAW = os.environ.get("TELEGRAM_CHAT_ID", "0")
try:
    TELEGRAM_CHAT_ID = int(TELEGRAM_CHAT_ID_RAW)
except ValueError:
    TELEGRAM_CHAT_ID = 0

ALERT_LOG = INSTANCE_REPO / ".federation-alert.log"


# ── Rate limit state (in-memory, daily reset) ──
_rate_state: dict[str, Any] = {
    "info_sent_today": 0,
    "warning_sent_today": 0,
    "day_key": "",
}


def _today_key() -> str:
    return time.strftime("%Y-%m-%d", time.gmtime())


def _maybe_reset_rate_state() -> None:
    today = _today_key()
    if _rate_state["day_key"] != today:
        _rate_state["info_sent_today"] = 0
        _rate_state["warning_sent_today"] = 0
        _rate_state["day_key"] = today


def _rate_limit_ok(level: str) -> bool:
    """Liveprob 3-tier filter discipline applied to alert levels."""
    _maybe_reset_rate_state()
    if level == "info":
        return _rate_state["info_sent_today"] < 5
    if level == "warning":
        return _rate_state["warning_sent_today"] < 10
    return True  # critical never throttled


def _record_sent(level: str) -> None:
    _maybe_reset_rate_state()
    if level == "info":
        _rate_state["info_sent_today"] += 1
    elif level == "warning":
        _rate_state["warning_sent_today"] += 1


def _format_alert(entry: dict[str, Any]) -> str:
    """Render alert as plain text + emoji-rich (no Markdown parse dependency).

    Markdown V1 was unreliable (em-dash, underscores, parens triggered fallback).
    Plain text with emoji indentation is robust across all special chars.
    """
    icon = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨"}.get(entry["level"], "📢")
    level_label = entry["level"].upper()

    text = f"{icon} {level_label} • {entry['instance_id']}\n\n"
    text += entry["reason"]

    if entry["action_required"]:
        text += "\n\n⚡ Operator action required"
    if entry["deferred_for_operator"]:
        text += "\n\n🛑 HARD constraint #8 — public action requires explicit Mimar command"
    if entry.get("context"):
        ctx_lines = [f"  • {k}: {v}" for k, v in entry["context"].items()]
        text += "\n\n📋 Context:\n" + "\n".join(ctx_lines)
    text += f"\n\n🕐 {entry['timestamp']}"
    return text


def _audit_log(entry: dict[str, Any]) -> None:
    """Append-only audit log (P-7 reasoning trail)."""
    ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ALERT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


async def _send_telegram(text: str) -> dict[str, Any]:
    """Condor send_notification pattern — direct httpx → Telegram API.

    No parse_mode (plain text + emoji-rich format). Avoids markdown parse failures
    on em-dashes, underscores, parens, and other special chars.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return {"error": "Telegram credentials not configured"}
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload: dict[str, Any] = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        # No parse_mode — plain text is robust across all chars
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload)
            data = resp.json()
            if data.get("ok"):
                msg_id = data["result"]["message_id"]
                return {"sent": True, "channel": "telegram", "message_id": str(msg_id)}
            return {"error": data.get("description", "Unknown Telegram API error")}
    except Exception as e:
        return {"error": f"send failed: {type(e).__name__}: {e}"}


async def federation_alert_impl(
    level: str,
    reason: str,
    instance_id: str,
    action_required: bool = False,
    deferred_for_operator: bool = False,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Federation-canonical federation_alert tool implementation.

    Federation form: tool signature matches schema v0.1.
    Federation content: this implementation (Telegram + Liveprob 3-tier filter).
    """
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # Validate level
    if level not in ("info", "warning", "critical"):
        result = {"error": f"invalid level: {level} (must be info|warning|critical)"}
        _audit_log({
            "timestamp": timestamp, "level": level, "instance_id": instance_id,
            "reason": reason, "result": result,
        })
        return result

    # Anti-impersonation (HARD constraint)
    if instance_id != INSTANCE_ID:
        result = {"error": f"instance_id mismatch: caller={instance_id} env={INSTANCE_ID}"}
        _audit_log({
            "timestamp": timestamp, "level": level, "instance_id": instance_id,
            "reason": reason, "result": result,
        })
        return result

    # Build entry
    entry = {
        "timestamp": timestamp,
        "level": level,
        "reason": reason,
        "instance_id": instance_id,
        "action_required": action_required,
        "deferred_for_operator": deferred_for_operator,
        "context": context or {},
    }

    # Filter discipline (level + rate limit)
    should_send = (
        level == "critical"
        or action_required
        or deferred_for_operator
        or _rate_limit_ok(level)
    )

    if not should_send:
        result = {"throttled": True, "reason": "rate_limit", "retry_after": 86400}
        _audit_log({**entry, "result": result})
        return result

    # Format + send
    msg = _format_alert(entry)
    result = await _send_telegram(msg)

    # Record + audit
    if result.get("sent"):
        _record_sent(level)
    _audit_log({**entry, "result": result})

    return result


# ── MCP server entry (for agent CLI integration) ──

def serve_mcp() -> None:
    """Run as MCP server (FastMCP) for agent CLI consumption."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        print(
            "error: mcp package not installed (pip install mcp)",
            file=sys.stderr,
        )
        sys.exit(2)

    mcp_server = FastMCP("companion-federation")

    @mcp_server.tool()
    async def federation_alert(
        level: str,
        reason: str,
        instance_id: str,
        action_required: bool = False,
        deferred_for_operator: bool = False,
        context: dict | None = None,
    ) -> dict:
        """Push federation alert to operator-only Telegram channel.

        Federation form-defined schema (leviathan-meta/schemas/federation-alert-mcp.md v0.1).
        Per-instance content: Telegram + Liveprob 3-tier filter + audit log.

        HARD: NEVER for public-facing communication. NEVER fabricate alerts.
        Use only for real federation events that need operator visibility.
        """
        return await federation_alert_impl(
            level=level,
            reason=reason,
            instance_id=instance_id,
            action_required=action_required,
            deferred_for_operator=deferred_for_operator,
            context=context,
        )

    mcp_server.run()


# ── CLI entry (for testing + direct invocation) ──

async def cli_test() -> int:
    """Standalone test mode — send a test alert."""
    test_entry = {
        "level": "info",
        "reason": "Phase 1.B.1 deploy complete — Companion MCP server federation_alert tool operational",
        "instance_id": INSTANCE_ID,
        "action_required": False,
        "deferred_for_operator": False,
        "context": {"phase": "1.B.1", "commit": "TBD"},
    }
    result = await federation_alert_impl(**test_entry)
    print(json.dumps(result, indent=2))
    return 0 if result.get("sent") or result.get("throttled") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Companion MCP server (federation_alert tool)")
    parser.add_argument("--test", action="store_true", help="Run standalone test (send sample alert)")
    parser.add_argument("--mcp", action="store_true", help="Run as MCP server (default if no flag)")
    args = parser.parse_args()

    # Validate env
    if not INSTANCE_ID:
        print("error: INSTANCE_ID env var required", file=sys.stderr)
        return 2
    if not INSTANCE_REPO.is_dir():
        print(f"error: INSTANCE_REPO not a directory: {INSTANCE_REPO}", file=sys.stderr)
        return 2

    if args.test:
        return asyncio.run(cli_test())

    serve_mcp()
    return 0


if __name__ == "__main__":
    sys.exit(main())
