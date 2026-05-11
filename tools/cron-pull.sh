#!/bin/bash
# cron-pull.sh — Federation reconciliation cron wrapper.
#
# Reads instance config env file, then runs pull-and-summarize.py. Same script
# on every federation machine; only the env file differs.
#
# Default config: ~/.federation-instance.env
# Multi-instance machines (e.g. Mac Mini hosting both Liveprob + Fast):
#   pass a different env file per cron entry via --env-file=<path>
#
# Required env vars (in the chosen file):
#   INSTANCE_ID     - companion | liveprob | security | fast | ...
#   INSTANCE_REPO   - absolute path to instance repo root
#   META_REPO       - absolute path to leviathan-meta clone
#
# Single-instance machine crontab entry:
#   */15 * * * * /path/to/leviathan-meta/tools/cron-pull.sh
#
# Multi-instance machine crontab entries (one per instance):
#   */15 * * * * /path/to/leviathan-meta/tools/cron-pull.sh --env-file=$HOME/.federation-instance-liveprob.env
#   */15 * * * * /path/to/leviathan-meta/tools/cron-pull.sh --env-file=$HOME/.federation-instance-fast.env
#
# Cron environment is minimal — PATH is set explicitly below.

set -e

# Parse --env-file argument if provided
ENV_FILE=""
for arg in "$@"; do
    case "$arg" in
        --env-file=*)
            ENV_FILE="${arg#--env-file=}"
            ;;
        --env-file)
            # support both --env-file=PATH and --env-file PATH
            shift
            ENV_FILE="$1"
            ;;
        --help|-h)
            grep '^#' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
    esac
done

# Default to ~/.federation-instance.env if no --env-file given
if [ -z "$ENV_FILE" ]; then
    ENV_FILE="$HOME/.federation-instance.env"
fi

if [ ! -f "$ENV_FILE" ]; then
    echo "[cron-pull $(date -u +%Y-%m-%dT%H:%M:%SZ)] error: env file missing: $ENV_FILE" >&2
    exit 1
fi

# shellcheck source=/dev/null
source "$ENV_FILE"

# Validate required vars
: "${INSTANCE_ID:?INSTANCE_ID not set in $ENV_FILE}"
: "${INSTANCE_REPO:?INSTANCE_REPO not set in $ENV_FILE}"
: "${META_REPO:?META_REPO not set in $ENV_FILE}"

# Cron PATH is minimal; ensure standard tools + Homebrew Python reachable
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

LOG_FILE="$INSTANCE_REPO/.federation-pull.log"

cd "$INSTANCE_REPO"
python3 "$META_REPO/tools/pull-and-summarize.py" \
    --meta-repo "$META_REPO" \
    --instance-id "$INSTANCE_ID" >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "[cron-pull $(date -u +%Y-%m-%dT%H:%M:%SZ)] script exited $EXIT_CODE on $INSTANCE_ID" >> "$LOG_FILE"
fi
exit $EXIT_CODE
