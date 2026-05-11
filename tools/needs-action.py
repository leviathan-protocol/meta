#!/usr/bin/env python3
"""
needs-action.py — Phase 1.A smart-skip decision engine.

Reads federation summary + meta-repo briefings to decide whether this instance
has actionable work pending. Stateless: no file writes, no state — just an
exit code plus an optional one-line stdout description.

Exit codes:
  0 — action needed (cron-act.sh should invoke claude/codex CLI)
  1 — skip (no work pending, silent exit, no token spend)
  2 — error (config issue; cron-act.sh should log and skip)

Action conditions (any of):
  - `briefings.ack_pending` contains a briefing addressed to this instance
    (cover letter `to:` field matches instance_id or "all") AND the instance
    has not already filed an ack.
  - `warnings` contains an entry starting with `<instance-id>-` (e.g.
    "companion-manifest-malformed").
  - `errors` array is non-empty.

Skip conditions (overrides above):
  - Summary `last_sync_age_seconds` exceeds STALE_TOLERANCE_SECONDS (1h).
    Stale state = skip; don't act on outdated information.
  - Meta-repo `pull_status` is "fail" in the most recent run.

Usage:
  needs-action.py --instance-id <id> \\
    --summary-file <path/to/.federation-summary.json> \\
    --meta-repo <path/to/leviathan-meta> \\
    [--verbose]

Schema version: matches federation-summary v0.1 (Phase 0 schema).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


STALE_TOLERANCE_SECONDS = 3600  # 1 hour — Phase 1.A pre-mortem decision #5
SCHEMA_VERSION_EXPECTED = "0.1"
RESERVED_BROADCAST_KEYWORD = "all"  # briefing `to: [all]` addresses every instance


def parse_briefing_cover(briefing_dir: Path) -> dict | None:
    """
    Find a cover letter (00_*.md, first match) and parse YAML front-matter.
    Returns dict on success, None on missing/malformed.
    Conservative: malformed YAML = None = treat as not-addressed-to-me.
    """
    candidates = sorted(briefing_dir.glob("00_*.md"))
    if not candidates:
        return None
    cover = candidates[0]
    try:
        content = cover.read_text(encoding="utf-8")
    except OSError:
        return None
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        front_matter = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    if not isinstance(front_matter, dict):
        return None
    return front_matter


def briefing_addressed_to(cover: dict | None, instance_id: str) -> bool:
    """
    Does this briefing's cover letter address my instance?
    Conservative on missing cover: returns False (skip rather than over-trigger).
    """
    if cover is None:
        return False
    to_list = cover.get("to") or []
    if not isinstance(to_list, list):
        return False
    if RESERVED_BROADCAST_KEYWORD in to_list:
        return True
    if instance_id in to_list:
        return True
    return False


def ack_already_filed(briefing_dir: Path, instance_id: str) -> bool:
    """Check if my instance has an ack file in this briefing's ack/ directory."""
    ack_dir = briefing_dir / "ack"
    if not ack_dir.is_dir():
        return False
    # Match {instance_id}-ack.md or {instance_id}-ack-anything.md
    matches = list(ack_dir.glob(f"{instance_id}-ack*.md"))
    return bool(matches)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smart-skip decision for Phase 1.A federation auto-action.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--instance-id", required=True,
                        help="Instance identifier (companion, liveprob, fast, security, ...)")
    parser.add_argument("--summary-file", required=True, type=Path,
                        help="Path to .federation-summary.json")
    parser.add_argument("--meta-repo", required=True, type=Path,
                        help="Path to leviathan-meta clone")
    parser.add_argument("--verbose", action="store_true",
                        help="Log decision rationale to stderr")
    args = parser.parse_args()

    def log(msg: str) -> None:
        if args.verbose:
            print(f"[needs-action] {msg}", file=sys.stderr)

    # ── Read summary ──
    if not args.summary_file.exists():
        print(f"error: summary file missing: {args.summary_file}", file=sys.stderr)
        return 2
    try:
        summary = json.loads(args.summary_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"error: summary parse failed: {e}", file=sys.stderr)
        return 2

    # ── Schema version soft check (decision #3) ──
    schema_version = summary.get("schema_version", "unknown")
    if schema_version != SCHEMA_VERSION_EXPECTED:
        log(f"warning: schema_version={schema_version} != expected={SCHEMA_VERSION_EXPECTED}")

    # ── Stale tolerance (decision #5) ──
    sync_age = summary.get("last_sync_age_seconds")
    if sync_age is not None and sync_age > STALE_TOLERANCE_SECONDS:
        log(f"skip: sync stale ({sync_age}s > {STALE_TOLERANCE_SECONDS}s)")
        return 1

    # ── Meta-repo pull health ──
    meta_pull_status = summary.get("meta_repo", {}).get("pull_status")
    if meta_pull_status == "fail":
        log("skip: meta-repo pull failed in last cycle")
        return 1

    # ── Validate meta-repo path ──
    if not args.meta_repo.is_dir():
        print(f"error: meta-repo path not a directory: {args.meta_repo}", file=sys.stderr)
        return 2

    # ── Filter ack_pending briefings for this instance ──
    actionable_briefings: list[str] = []
    skipped_due_to_other_instance: list[str] = []
    skipped_due_to_already_acked: list[str] = []

    for briefing_id in summary.get("briefings", {}).get("ack_pending", []):
        briefing_dir = args.meta_repo / "briefings" / briefing_id
        if not briefing_dir.is_dir():
            log(f"warning: briefing dir missing: {briefing_id}")
            continue
        cover = parse_briefing_cover(briefing_dir)
        if not briefing_addressed_to(cover, args.instance_id):
            skipped_due_to_other_instance.append(briefing_id)
            continue
        if ack_already_filed(briefing_dir, args.instance_id):
            skipped_due_to_already_acked.append(briefing_id)
            continue
        actionable_briefings.append(briefing_id)

    # ── Filter warnings for this instance ──
    all_warnings = summary.get("warnings", [])
    instance_warnings = [w for w in all_warnings if w.startswith(f"{args.instance_id}-")]

    # ── Errors are always actionable (federation-wide problem) ──
    errors = summary.get("errors", [])

    log(f"ack_pending total: {len(summary.get('briefings', {}).get('ack_pending', []))}")
    log(f"  → addressed to me + not yet acked: {len(actionable_briefings)}")
    log(f"  → for other instances: {len(skipped_due_to_other_instance)}")
    log(f"  → already acked by me: {len(skipped_due_to_already_acked)}")
    log(f"warnings total: {len(all_warnings)}")
    log(f"  → instance-specific (mine): {len(instance_warnings)}")
    log(f"errors: {len(errors)}")

    # ── Decision ──
    has_action = bool(actionable_briefings or instance_warnings or errors)
    if has_action:
        parts = []
        if actionable_briefings:
            parts.append(f"{len(actionable_briefings)} briefing(s) need ack: {','.join(actionable_briefings)}")
        if instance_warnings:
            parts.append(f"{len(instance_warnings)} self-warning(s)")
        if errors:
            parts.append(f"{len(errors)} error(s)")
        print("; ".join(parts))
        return 0

    log("skip: no action pending for this instance")
    return 1


if __name__ == "__main__":
    sys.exit(main())
