#!/bin/bash
# cron-act.sh — Phase 1.A federation auto-action wrapper.
#
# Composes Phase 0 + Phase 1.A:
#   1. Run cron-pull.sh (Phase 0 — refresh .federation-summary.json)
#   2. Run needs-action.py (Phase 1.A smart-skip — exit 0/1/2)
#   3. If needs-action exit 0 → invoke agent CLI with federation-act-prompt
#   4. Otherwise silent skip (no token spend)
#
# Single-instance machine crontab:
#   */15 * * * * /path/to/leviathan-meta/tools/cron-act.sh
#
# Multi-instance machine (Mac Mini Liveprob+Fast) — use --env-file:
#   */15 * * * * .../cron-act.sh --env-file=$HOME/.federation-instance-liveprob.env
#   */15 * * * * .../cron-act.sh --env-file=$HOME/.federation-instance-fast.env
#
# Env file required vars (in addition to Phase 0):
#   INSTANCE_ID, INSTANCE_REPO, META_REPO    (Phase 0)
#   AGENT_CLI                                 (Phase 1.A: claude | codex | ollama-claude | ...)
#   AGENT_CLI_FLAGS                           (Phase 1.A: e.g. -p)
#   AGENT_CLI_PROMPT_PATH                     (Phase 1.A: path to federation-act-prompt.md)
#
# Exit:
#   0 — success (skip OR action completed)
#   non-0 — script error or agent error (logged)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Step 0: Run Phase 0 (cron-pull) first to refresh summary ──
"$SCRIPT_DIR/cron-pull.sh" "$@"
PULL_EXIT=$?
if [ $PULL_EXIT -ne 0 ]; then
    # Phase 0 logged its own error; continue to act with whatever summary we have
    :
fi

# ── Step 1: Resolve env file ──
ENV_FILE=""
for arg in "$@"; do
    case "$arg" in
        --env-file=*)
            ENV_FILE="${arg#--env-file=}"
            ;;
    esac
done
if [ -z "$ENV_FILE" ]; then
    ENV_FILE="$HOME/.federation-instance.env"
fi
if [ ! -f "$ENV_FILE" ]; then
    echo "[cron-act $(date -u +%Y-%m-%dT%H:%M:%SZ)] error: env file missing: $ENV_FILE" >&2
    exit 1
fi
# shellcheck source=/dev/null
source "$ENV_FILE"

# Phase 0 vars validated by cron-pull.sh; validate Phase 1.A vars
: "${INSTANCE_ID:?INSTANCE_ID not set}"
: "${INSTANCE_REPO:?INSTANCE_REPO not set}"
: "${META_REPO:?META_REPO not set}"

# Phase 1.A specific (optional with sensible defaults)
AGENT_CLI="${AGENT_CLI:-claude}"
AGENT_CLI_FLAGS="${AGENT_CLI_FLAGS:--p}"
AGENT_CLI_PROMPT_PATH="${AGENT_CLI_PROMPT_PATH:-$META_REPO/tools/federation-act-prompt.md}"

# ── Step 2: PATH and log setup ──
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
ACT_LOG="$INSTANCE_REPO/.federation-act.log"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# ── Step 3: Smart-skip decision (needs-action.py) ──
SUMMARY_FILE="$INSTANCE_REPO/.federation-summary.json"
NEEDS_ACTION_OUTPUT=$(python3 "$SCRIPT_DIR/needs-action.py" \
    --instance-id "$INSTANCE_ID" \
    --summary-file "$SUMMARY_FILE" \
    --meta-repo "$META_REPO" 2>&1) || NEEDS_EXIT=$?
NEEDS_EXIT=${NEEDS_EXIT:-0}

case $NEEDS_EXIT in
    0)
        echo "[cron-act $TIMESTAMP] action needed: $NEEDS_ACTION_OUTPUT" >> "$ACT_LOG"
        ;;
    1)
        # Silent skip — only log if verbose mode (not implemented; keep log lean)
        exit 0
        ;;
    2)
        echo "[cron-act $TIMESTAMP] needs-action error: $NEEDS_ACTION_OUTPUT" >> "$ACT_LOG"
        exit 1
        ;;
    *)
        echo "[cron-act $TIMESTAMP] needs-action unexpected exit=$NEEDS_EXIT: $NEEDS_ACTION_OUTPUT" >> "$ACT_LOG"
        exit 1
        ;;
esac

# ── Step 4: Validate agent CLI available ──
if ! command -v "$AGENT_CLI" >/dev/null 2>&1; then
    echo "[cron-act $TIMESTAMP] error: AGENT_CLI=$AGENT_CLI not in PATH" >> "$ACT_LOG"
    exit 1
fi

if [ ! -f "$AGENT_CLI_PROMPT_PATH" ]; then
    echo "[cron-act $TIMESTAMP] error: prompt missing: $AGENT_CLI_PROMPT_PATH" >> "$ACT_LOG"
    exit 1
fi

# ── Step 5: Lock file (race avoidance) ──
LOCK_FILE="/tmp/federation-act-${INSTANCE_ID}.lock"
if [ -e "$LOCK_FILE" ]; then
    LOCK_AGE=$(($(date +%s) - $(stat -f %m "$LOCK_FILE" 2>/dev/null || stat -c %Y "$LOCK_FILE")))
    if [ "$LOCK_AGE" -lt 600 ]; then
        echo "[cron-act $TIMESTAMP] skip: lock held (${LOCK_AGE}s old)" >> "$ACT_LOG"
        exit 0
    fi
    # Stale lock (>10 min); break it
    rm -f "$LOCK_FILE"
fi
trap 'rm -f "$LOCK_FILE"' EXIT
echo "$$" > "$LOCK_FILE"

# ── Step 6: Invoke agent CLI ──
cd "$INSTANCE_REPO"

# Build prompt: federation-act-prompt.md content + instance context as preamble
PROMPT_PREAMBLE="You are running as federation instance: $INSTANCE_ID
Instance repo: $INSTANCE_REPO
Meta repo: $META_REPO
Cycle timestamp: $TIMESTAMP
Smart-skip output: $NEEDS_ACTION_OUTPUT

Read the federation-act protocol below and execute exactly as specified."

PROMPT_BODY=$(cat "$AGENT_CLI_PROMPT_PATH")
FULL_PROMPT="$PROMPT_PREAMBLE

---

$PROMPT_BODY"

# Export instance context for the agent's runtime to read (HARD constraint #1 in prompt)
export INSTANCE_ID INSTANCE_REPO META_REPO

echo "[cron-act $TIMESTAMP] invoking $AGENT_CLI" >> "$ACT_LOG"

AGENT_START=$(date +%s)
echo "$FULL_PROMPT" | "$AGENT_CLI" $AGENT_CLI_FLAGS >> "$ACT_LOG" 2>&1
AGENT_EXIT=$?
AGENT_DURATION=$(($(date +%s) - AGENT_START))

echo "[cron-act $TIMESTAMP] $AGENT_CLI exit=$AGENT_EXIT duration=${AGENT_DURATION}s" >> "$ACT_LOG"

# Lock cleanup happens via trap

exit $AGENT_EXIT
