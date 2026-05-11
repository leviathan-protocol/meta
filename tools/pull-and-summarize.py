#!/usr/bin/env python3
"""
pull-and-summarize.py — Federation reconciliation engine (Phase 0).

Pulls the latest meta-repo state and produces a derived `.federation-summary.json`
in the calling instance's repo root. This file is the cache that hooks (Phase 1)
will read instead of querying meta-repo live.

Pattern: GitOps reconciliation (ArgoCD/Flux). Pull > push for offline tolerance.
The script is idempotent: running it twice produces the same output (modulo timestamps).

Usage:
    pull-and-summarize.py --meta-repo <path> --instance-id <name>
    pull-and-summarize.py --instance-repo <path> --no-pull --verbose
    pull-and-summarize.py --help

Cron usage (every 15 minutes):
    */15 * * * * cd <instance_repo> && python3 <meta>/tools/pull-and-summarize.py \
        --meta-repo <meta> --instance-id <name> >> <meta>/.cron-pull.log 2>&1

Schema version: 0.1 (see notes/2026-05-07-phase0-onboarding-plan.md §"Schema")
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


SCHEMA_VERSION = "0.1"
SUMMARY_FILENAME = ".federation-summary.json"

# Known federation instances and their meta-repo paths (P-1 sub-directory sovereignty).
# Each instance has a manifest path (one of the variants — manifest.yaml or manifest-public.yaml)
# and a status file. F-2 pending instances (fast) declare manifest absent, note explains.
KNOWN_INSTANCES: dict[str, dict[str, Any]] = {
    "companion": {
        "manifest_candidates": ["companion/manifest-public.yaml", "companion/manifest.yaml"],
        "status_file": "companion/status.md",
    },
    "liveprob": {
        "manifest_candidates": ["liveprob/manifest.yaml"],
        "status_file": "liveprob/status.md",
    },
    "security": {
        "manifest_candidates": ["security/manifest.yaml"],
        "status_file": "security/status.md",
    },
    "fast": {
        "manifest_candidates": ["fast/manifest.yaml"],
        "status_file": "fast/status.md",
        "note": "F-2 federation onboarding pending kernel crystallization",
    },
    "anima": {
        "manifest_candidates": ["anima/manifest.yaml"],
        "status_file": "anima/status.md",
    },
    "atlas": {
        "manifest_candidates": ["atlas/manifest.yaml"],
        "status_file": "atlas/status.md",
    },
    "tasma": {
        "manifest_candidates": ["tasma/manifest.yaml"],
        "status_file": "tasma/status.md",
    },
}


def log(msg: str, verbose: bool, stream=sys.stderr) -> None:
    if verbose:
        print(f"[pull-and-summarize] {msg}", file=stream, flush=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def fetch_meta_repo(meta_path: Path, no_pull: bool, verbose: bool) -> tuple[dict, list[str]]:
    """
    Pull meta-repo (or skip if --no-pull). Return meta_repo info dict + warnings list.
    Pull failure is non-fatal — script continues with stale state.
    """
    warnings: list[str] = []
    info: dict[str, Any] = {
        "head_commit": None,
        "fetched_at": None,
        "pull_status": "skipped" if no_pull else "ok",
    }

    if no_pull:
        log("skipping git pull (--no-pull)", verbose)
    else:
        log(f"pulling {meta_path}", verbose)
        try:
            subprocess.run(
                ["git", "-C", str(meta_path), "pull", "--rebase", "--quiet"],
                check=True,
                capture_output=True,
                timeout=60,
            )
            info["fetched_at"] = now_iso()
        except subprocess.TimeoutExpired:
            info["pull_status"] = "fail"
            warnings.append("meta-repo-pull-timeout")
            log("pull timed out after 60s", verbose)
        except subprocess.CalledProcessError as e:
            info["pull_status"] = "fail"
            stderr = e.stderr.decode("utf-8", errors="replace") if e.stderr else ""
            warnings.append(f"meta-repo-pull-failed: {stderr.strip()[:200]}")
            log(f"pull failed: {stderr}", verbose)

    # Get HEAD commit regardless of pull success (last known state)
    try:
        result = subprocess.run(
            ["git", "-C", str(meta_path), "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            timeout=10,
        )
        info["head_commit"] = result.stdout.decode("utf-8").strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        warnings.append(f"meta-repo-head-unavailable: {type(e).__name__}")
        log(f"could not read HEAD: {e}", verbose)

    return info, warnings


def file_age_seconds(path: Path) -> int | None:
    """Return age in seconds since file mtime, or None if missing."""
    try:
        mtime = path.stat().st_mtime
        return int(datetime.now().timestamp() - mtime)
    except FileNotFoundError:
        return None


def parse_manifest(manifest_path: Path) -> tuple[dict | None, str | None]:
    """
    Parse a manifest YAML. Return (data, error). On success error is None.
    Strips comments-only top sections — yaml.safe_load handles that automatically.
    """
    try:
        with manifest_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return None, "not-a-mapping"
        return data, None
    except FileNotFoundError:
        return None, "not-found"
    except yaml.YAMLError as e:
        return None, f"yaml-error: {str(e)[:100]}"
    except OSError as e:
        return None, f"io-error: {str(e)[:100]}"


def scan_instances(meta_path: Path, verbose: bool) -> tuple[dict[str, dict], list[str]]:
    """
    Scan meta-repo for each known instance's manifest + status.
    Return instances dict + warnings list.
    """
    instances: dict[str, dict] = {}
    warnings: list[str] = []

    for instance_id, spec in KNOWN_INSTANCES.items():
        instance_data: dict[str, Any] = {
            "manifest_present": False,
            "manifest_path": None,
            "snapshot_hash": None,
            "last_touched_age_seconds": None,
            "status_file": None,
        }
        if "note" in spec:
            instance_data["note"] = spec["note"]

        # Try each manifest candidate (companion has -public variant)
        for candidate in spec["manifest_candidates"]:
            mpath = meta_path / candidate
            if mpath.exists():
                data, err = parse_manifest(mpath)
                if err:
                    warnings.append(f"{instance_id}-manifest-malformed: {err}")
                    log(f"{instance_id} manifest malformed: {err}", verbose)
                    instance_data["manifest_path"] = candidate
                    break
                instance_data["manifest_present"] = True
                instance_data["manifest_path"] = candidate
                # Snapshot hash extraction (varies by schema)
                constitution = data.get("constitution") or {}
                snapshot = constitution.get("snapshot_hash")
                if snapshot:
                    instance_data["snapshot_hash"] = snapshot
                instance_data["last_touched_age_seconds"] = file_age_seconds(mpath)
                break

        if not instance_data["manifest_present"] and "note" not in spec:
            warnings.append(f"{instance_id}-manifest-missing")

        # Status file
        status_path = meta_path / spec["status_file"]
        if status_path.exists():
            instance_data["status_file"] = spec["status_file"]
            # Update last_touched_age if manifest missing but status present
            if instance_data["last_touched_age_seconds"] is None:
                instance_data["last_touched_age_seconds"] = file_age_seconds(status_path)

        instances[instance_id] = instance_data

    return instances, warnings


def scan_briefings(meta_path: Path, verbose: bool) -> tuple[dict, list[str]]:
    """
    Scan briefings/ folder for ack status.
    v0.1 heuristic:
      - briefing has ack/ subdir with no .md files (or only .gitkeep) → ack_pending
      - briefing has ack/ with at least one .md → ack received (recent_filed)
      - open: empty for v0.1 (formal status field not yet in briefing schema)
    """
    briefings_root = meta_path / "briefings"
    result = {
        "open": [],
        "ack_pending": [],
        "recent_filed": [],
    }
    warnings: list[str] = []

    if not briefings_root.is_dir():
        warnings.append("briefings-dir-missing")
        return result, warnings

    briefing_dirs = sorted(
        [d for d in briefings_root.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )

    for bdir in briefing_dirs:
        ack_dir = bdir / "ack"
        if ack_dir.is_dir():
            ack_files = [f for f in ack_dir.iterdir() if f.suffix == ".md"]
            if ack_files:
                result["recent_filed"].append(bdir.name)
            else:
                result["ack_pending"].append(bdir.name)
        else:
            # No ack/ subdir — briefing might be reference-only or pre-ack-protocol
            result["recent_filed"].append(bdir.name)

    # Truncate recent_filed to last 10 (already date-sorted desc by folder name)
    result["recent_filed"] = result["recent_filed"][:10]

    return result, warnings


def build_summary(
    instance_id: str,
    meta_path: Path,
    meta_info: dict,
    instances: dict[str, dict],
    briefings: dict,
    warnings: list[str],
    errors: list[str],
) -> dict:
    """Assemble the full summary dict."""
    last_sync_age = None
    if meta_info.get("fetched_at"):
        last_sync_age = 0  # just fetched
    elif meta_info["pull_status"] == "skipped":
        last_sync_age = None  # not fetched this run

    return {
        "schema_version": SCHEMA_VERSION,
        "instance_id": instance_id,
        "generated_at": now_iso(),
        "last_sync_age_seconds": last_sync_age,
        "meta_repo": meta_info,
        "instances": instances,
        "briefings": briefings,
        "warnings": warnings,
        "errors": errors,
    }


def atomic_write(target_path: Path, content: str, verbose: bool) -> bool:
    """
    Write content atomically: write to temp file in same directory, then rename.
    POSIX guarantees rename is atomic on the same filesystem.
    Returns True on success, False on failure.
    """
    target_path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = f".{target_path.name}.tmp.{uuid.uuid4().hex[:8]}"
    temp_path = target_path.parent / temp_name
    try:
        with temp_path.open("w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.rename(temp_path, target_path)
        log(f"wrote {target_path}", verbose)
        return True
    except OSError as e:
        log(f"atomic write failed: {e}", verbose)
        try:
            temp_path.unlink()
        except OSError:
            pass
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Federation reconciliation engine (Phase 0).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--meta-repo",
        type=Path,
        default=Path(os.environ.get("LEVIATHAN_META_REPO", "")),
        help="Path to leviathan-meta repo (or $LEVIATHAN_META_REPO env)",
    )
    parser.add_argument(
        "--instance-repo",
        type=Path,
        default=Path.cwd(),
        help="Path to calling instance's repo root (default: cwd)",
    )
    parser.add_argument(
        "--instance-id",
        required=True,
        help="Instance identifier (companion, liveprob, security, fast, etc.)",
    )
    parser.add_argument(
        "--no-pull",
        action="store_true",
        help="Skip git pull (test mode)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Log diagnostics to stderr",
    )
    args = parser.parse_args()

    if not args.meta_repo or not args.meta_repo.is_dir():
        print(
            f"error: --meta-repo invalid or missing: {args.meta_repo}",
            file=sys.stderr,
        )
        return 1
    if not args.instance_repo.is_dir():
        print(
            f"error: --instance-repo not a directory: {args.instance_repo}",
            file=sys.stderr,
        )
        return 1
    if args.instance_id not in KNOWN_INSTANCES:
        log(
            f"warning: instance-id '{args.instance_id}' not in KNOWN_INSTANCES; "
            f"summary will still be generated",
            args.verbose,
        )

    log(
        f"meta-repo={args.meta_repo}, instance-repo={args.instance_repo}, "
        f"instance-id={args.instance_id}",
        args.verbose,
    )

    errors: list[str] = []
    all_warnings: list[str] = []

    # Phase 1: pull meta-repo
    meta_info, pull_warnings = fetch_meta_repo(args.meta_repo, args.no_pull, args.verbose)
    all_warnings.extend(pull_warnings)

    # Phase 2: scan instances
    instances, instance_warnings = scan_instances(args.meta_repo, args.verbose)
    all_warnings.extend(instance_warnings)

    # Phase 3: scan briefings
    briefings, briefing_warnings = scan_briefings(args.meta_repo, args.verbose)
    all_warnings.extend(briefing_warnings)

    # Phase 4: build + write summary
    summary = build_summary(
        instance_id=args.instance_id,
        meta_path=args.meta_repo,
        meta_info=meta_info,
        instances=instances,
        briefings=briefings,
        warnings=all_warnings,
        errors=errors,
    )

    target_path = args.instance_repo / SUMMARY_FILENAME
    content = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    if not atomic_write(target_path, content, args.verbose):
        print(f"error: atomic write to {target_path} failed", file=sys.stderr)
        return 2

    log(f"summary written ({len(content)} bytes)", args.verbose)
    return 0


if __name__ == "__main__":
    sys.exit(main())
