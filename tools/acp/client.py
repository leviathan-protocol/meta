"""Federation Minimal ACP Client

Spawns an agent CLI subprocess and speaks Agent Communication Protocol v1
over JSON-RPC 2.0 stdio. Federation-fit minimal implementation — supports
multi-vendor agent backends (claude-code, codex, gemini, copilot) with one-line
config switch. Federation Q10 (tool-level interchangeability) operasyonel kanıt.

Pattern reference: hummingbot/condor/condor/acp/client.py (MIT, 350 lines)
Federation adaptation:
  - federation-canonical naming (clientInfo: "leviathan-federation")
  - permission_callback wired for HARD constraints enforce (no public-facing,
    no constitutional amendments, sovereignty boundary)
  - stdlib only (no pydantic_ai dependency)
  - simplified event types — no pydantic models, raw dataclasses

Usage:
    async def my_permission_check(tool_call, options):
        # Federation HARD constraint enforcement
        if "tweet" in tool_call.get("title", "").lower():
            return {"outcome": {"outcome": "selected", "optionId": "reject"}}
        return {"outcome": {"outcome": "selected", "optionId": options[0]["optionId"]}}

    client = ACPClient(
        command="claude-agent-acp",  # or "npx @zed-industries/codex-acp"
        working_dir="/path/to/instance",
        permission_callback=my_permission_check,
    )
    await client.start()
    async for event in client.prompt_stream("federation-act-prompt content..."):
        if isinstance(event, TextChunk):
            print(event.text)
    await client.stop()
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
from dataclasses import dataclass
from typing import Any, AsyncIterator, Awaitable, Callable

from .jsonrpc import JSONRPCPeer

log = logging.getLogger(__name__)


# Federation-supported agent commands. Each instance picks via env var
# (P-1 sovereignty + Q10 tool interchangeability). Add new providers here.
#
# Default paths assume LOCAL node_modules pattern (no global install) — see
# tools/acp/package.json. Use working_dir=<path-to-tools/acp> when invoking
# ACPClient so relative paths resolve correctly. Alternatively, override these
# via env var or pass an absolute path directly to ACPClient(command=...).
#
# Pattern reference: Mimar 2026-05-08 — federation tooling sovereignty preserved
# via local node_modules (Python uv venv analog), no system-level npm install.
ACP_COMMANDS: dict[str, str] = {
    "claude-code": "./node_modules/.bin/claude-agent-acp",
    "codex":       "./node_modules/.bin/codex-acp",
    # Gemini and Copilot are aspirational — ACP-mode binaries not yet
    # confirmed installable as local npm deps. Test before production use.
    "gemini":      "gemini --experimental-acp",
    "copilot":     "copilot --acp",
}


# --- Event types yielded by prompt_stream ---


@dataclass
class TextChunk:
    text: str


@dataclass
class ThoughtChunk:
    text: str


@dataclass
class ToolCallEvent:
    tool_call_id: str
    title: str
    status: str  # pending | in_progress | completed | failed
    kind: str = "other"
    input: dict | None = None


@dataclass
class ToolCallUpdate:
    tool_call_id: str
    status: str | None = None
    title: str | None = None
    output: str | None = None


@dataclass
class PromptDone:
    stop_reason: str  # end_turn | error | timeout | disconnected | cancelled


@dataclass
class Heartbeat:
    elapsed_seconds: float


ACPEvent = TextChunk | ThoughtChunk | ToolCallEvent | ToolCallUpdate | PromptDone | Heartbeat

# Permission callback type: receives tool_call dict + options list, returns outcome dict
PermissionCallback = Callable[[dict, list[dict]], Awaitable[dict]]


class ACPClient:
    """Manages ACP subprocess lifecycle: spawn → handshake → prompt → stop."""

    def __init__(
        self,
        command: str,
        working_dir: str | None = None,
        mcp_servers: list[dict[str, Any]] | None = None,
        permission_callback: PermissionCallback | None = None,
        extra_env: dict[str, str] | None = None,
        prompt_timeout_seconds: int = 1800,  # 30 min default; long ack writes
    ):
        self.command = command
        self.working_dir = working_dir or os.getcwd()
        self.mcp_servers = mcp_servers or []
        self.permission_callback = permission_callback
        self.extra_env = extra_env
        self.prompt_timeout = prompt_timeout_seconds

        self._process: asyncio.subprocess.Process | None = None
        self._peer = JSONRPCPeer()
        self._session_id: str | None = None
        self._read_task: asyncio.Task | None = None
        self._stderr_task: asyncio.Task | None = None
        self._event_queue: asyncio.Queue[ACPEvent] = asyncio.Queue()

        self._peer.register_handler("session/update", self._on_session_update)
        self._peer.register_handler("session/request_permission", self._on_request_permission)

    # --- Lifecycle ---

    async def start(self) -> None:
        """Spawn subprocess, run ACP handshake (initialize + session/new)."""
        env = dict(os.environ)
        if self.extra_env:
            env.update(self.extra_env)

        self._process = await asyncio.create_subprocess_shell(
            self.command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.working_dir,
            env=env,
            limit=10 * 1024 * 1024,  # 10 MB stdout buffer
            start_new_session=True,  # Own process group for clean kill
        )
        self._read_task = asyncio.create_task(self._read_loop())
        self._stderr_task = asyncio.create_task(self._drain_stderr())

        try:
            await self._peer.send_request(
                "initialize",
                {
                    "protocolVersion": 1,
                    "clientCapabilities": {},
                    "clientInfo": {"name": "leviathan-federation", "version": "0.1.0"},
                },
                self._process.stdin,
            )
            result = await self._peer.send_request(
                "session/new",
                {"cwd": self.working_dir, "mcpServers": self.mcp_servers},
                self._process.stdin,
            )
        except Exception:
            await self.stop()
            raise

        self._session_id = result["sessionId"]
        log.info("ACP session started: %s (cmd=%s)", self._session_id, self.command)

    async def stop(self) -> None:
        """Terminate subprocess + all child processes (MCP servers etc.) cleanly."""
        self._peer.cancel_all()
        for task in (self._read_task, self._stderr_task):
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        if self._process and self._process.returncode is None:
            pid = self._process.pid
            try:
                # Kill entire process group (subprocess + MCP server children)
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                pass
            try:
                await asyncio.wait_for(self._process.wait(), timeout=5)
            except asyncio.TimeoutError:
                try:
                    os.killpg(os.getpgid(pid), signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    self._process.kill()
                try:
                    await asyncio.wait_for(self._process.wait(), timeout=3)
                except asyncio.TimeoutError:
                    log.warning("ACP process %d could not be reaped", pid)
        self._process = None

    @property
    def alive(self) -> bool:
        return self._process is not None and self._process.returncode is None

    # --- Read loops ---

    async def _read_loop(self) -> None:
        assert self._process and self._process.stdout
        try:
            while True:
                line = await self._process.stdout.readline()
                if not line:
                    break
                await self._peer.handle_line(line.decode(), self._process.stdin)
        except asyncio.CancelledError:
            return
        except Exception:
            log.exception("ACP read loop error")
        # Stream ended → unblock consumers
        self._peer.cancel_all()
        self._event_queue.put_nowait(PromptDone(stop_reason="disconnected"))

    async def _drain_stderr(self) -> None:
        """Drain stderr to prevent pipe buffer fill blocking the subprocess."""
        assert self._process and self._process.stderr
        try:
            while True:
                line = await self._process.stderr.readline()
                if not line:
                    break
                text = line.decode(errors="replace").rstrip()
                if text:
                    log.debug("ACP stderr: %s", text)
        except asyncio.CancelledError:
            return
        except Exception:
            log.exception("ACP stderr drain error")

    # --- Prompt ---

    async def prompt(self, text: str) -> str:
        """One-shot prompt: collect all TextChunks, return joined string."""
        chunks: list[str] = []
        async for event in self.prompt_stream(text):
            if isinstance(event, TextChunk):
                chunks.append(event.text)
        return "".join(chunks)

    async def prompt_stream(self, text: str) -> AsyncIterator[ACPEvent]:
        """Send prompt, yield ACPEvents as they arrive (TextChunk, ToolCall, Heartbeat, Done)."""
        assert self._process and self._session_id

        # Drain queue (in case previous prompt left events)
        while not self._event_queue.empty():
            self._event_queue.get_nowait()

        # Send session/prompt without awaiting (read loop handles incoming notifications)
        req_id = self._peer._next_id
        self._peer._next_id += 1
        msg = {
            "jsonrpc": "2.0",
            "method": "session/prompt",
            "params": {
                "sessionId": self._session_id,
                "prompt": [{"type": "text", "text": text}],
            },
            "id": req_id,
        }
        self._process.stdin.write((json.dumps(msg) + "\n").encode())
        await self._process.stdin.drain()

        future: asyncio.Future[Any] = asyncio.get_event_loop().create_future()
        self._peer._pending[req_id] = future

        def _on_response(fut: asyncio.Future) -> None:
            if fut.cancelled():
                self._event_queue.put_nowait(PromptDone(stop_reason="cancelled"))
            elif fut.exception():
                self._event_queue.put_nowait(PromptDone(stop_reason="error"))
            else:
                result = fut.result()
                reason = (
                    result.get("stopReason", "end_turn")
                    if isinstance(result, dict)
                    else "end_turn"
                )
                self._event_queue.put_nowait(PromptDone(stop_reason=reason))

        future.add_done_callback(_on_response)

        loop = asyncio.get_event_loop()
        start = loop.time()

        while True:
            try:
                event = await asyncio.wait_for(self._event_queue.get(), timeout=30)
            except asyncio.TimeoutError:
                elapsed = loop.time() - start
                if not self.alive:
                    yield PromptDone(stop_reason="disconnected")
                    break
                if elapsed > self.prompt_timeout:
                    log.warning("Prompt hard timeout after %.0fs", elapsed)
                    yield PromptDone(stop_reason="timeout")
                    break
                yield Heartbeat(elapsed_seconds=elapsed)
                continue
            yield event
            if isinstance(event, PromptDone):
                break

    # --- Reverse-RPC handlers ---

    def _on_session_update(
        self, sessionId: str, update: dict[str, Any], _meta: dict | None = None, **kw: Any
    ) -> None:
        kind = update.get("sessionUpdate")
        if kind == "agent_message_chunk":
            text = update.get("content", {}).get("text", "")
            if text:
                self._event_queue.put_nowait(TextChunk(text=text))
        elif kind == "agent_thought_chunk":
            text = update.get("content", {}).get("text", "")
            if text:
                self._event_queue.put_nowait(ThoughtChunk(text=text))
        elif kind == "tool_call":
            self._event_queue.put_nowait(
                ToolCallEvent(
                    tool_call_id=update.get("toolCallId", ""),
                    title=update.get("title", ""),
                    status=update.get("status", "pending"),
                    kind=update.get("kind", "other"),
                    input=update.get("input"),
                )
            )
        elif kind == "tool_call_update":
            self._event_queue.put_nowait(
                ToolCallUpdate(
                    tool_call_id=update.get("toolCallId", ""),
                    status=update.get("status"),
                    title=update.get("title"),
                    output=update.get("output"),
                )
            )

    async def _on_request_permission(
        self,
        sessionId: str = "",
        options: list[dict[str, Any]] | None = None,
        toolCall: dict[str, Any] | None = None,
        _meta: dict | None = None,
        **kw: Any,
    ) -> dict[str, Any]:
        """Federation HARD constraint enforcement point.

        If permission_callback set, delegate (federation-act-prompt HARD constraints
        check). Otherwise default: select first allow-option (auto-approve).
        """
        options = options or []

        if self.permission_callback:
            return await self.permission_callback(toolCall or {}, options)

        # Default auto-approve (when no callback set, federation HARD constraints
        # must be enforced inside the prompt itself, not at permission layer)
        for opt in options:
            if opt.get("kind") in ("allow_once", "allow_always"):
                return {"outcome": {"outcome": "selected", "optionId": opt["optionId"]}}
        if options:
            return {"outcome": {"outcome": "selected", "optionId": options[0]["optionId"]}}
        return {"outcome": {"outcome": "cancelled"}}
