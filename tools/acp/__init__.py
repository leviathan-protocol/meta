"""Federation Minimal Agent Communication Protocol (ACP)

Multi-vendor agent CLI adapter via JSON-RPC 2.0 over subprocess stdio.
Federation Phase 1.A Q10 (tool-level interchangeability) operasyonel substrate.

Pattern reference: hummingbot/condor (MIT) — adapted to federation-fit minimal,
stdlib-only, no pydantic_ai dependency. ~480 lines total (vs Condor's 998).

Federation form: ACPClient(command=...) interface, schema-conformant
Federation content: per-instance command choice (claude-code | codex | gemini | copilot)

Usage:
    from acp import ACPClient, TextChunk, PromptDone, ACP_COMMANDS

    client = ACPClient(
        command=ACP_COMMANDS["claude-code"],  # or "codex", etc.
        working_dir="/path/to/instance",
        permission_callback=federation_hard_constraint_check,
    )
    await client.start()
    async for event in client.prompt_stream(prompt_text):
        if isinstance(event, TextChunk):
            ...
        elif isinstance(event, PromptDone):
            break
    await client.stop()
"""

from .client import (
    ACPClient,
    ACPEvent,
    ACP_COMMANDS,
    TextChunk,
    ThoughtChunk,
    ToolCallEvent,
    ToolCallUpdate,
    PromptDone,
    Heartbeat,
    PermissionCallback,
)
from .jsonrpc import JSONRPCError, JSONRPCPeer

__all__ = [
    "ACPClient",
    "ACPEvent",
    "ACP_COMMANDS",
    "TextChunk",
    "ThoughtChunk",
    "ToolCallEvent",
    "ToolCallUpdate",
    "PromptDone",
    "Heartbeat",
    "PermissionCallback",
    "JSONRPCError",
    "JSONRPCPeer",
]
