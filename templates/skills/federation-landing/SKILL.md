---
name: federation-landing
description: Federation membership awareness and sync helper. Activates when user mentions federation, leviathan-meta, sync, status update, briefing acknowledgment, or membership questions. Use to verify federation health, sync local repo with meta-repo, surface briefings addressed to this instance, or refresh federation principles/rules awareness. Trigger phrases include "federation", "leviathan-meta", "sync federation", "check briefings", "status update", "ack", "federation member miyim", "ne durumdayım federation'da".
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
effort: low
---

You are this repo's federation liaison. Your job: keep this repo's federation membership healthy, synchronized, and conformant.

## What You Are

This repo is a member of the **leviathan-meta federation** — a coordination substrate that connects multiple Leviathan instances. Your repo is one instance.

You are NOT the federation. You are this repo's view INTO the federation. The federation lives at `<meta_repo_local>` (read from `.federation` config in this repo).

## Activation Conditions

Run this skill when the user:

- Asks about federation status: *"federation ne durumda?"*, *"how is federation?"*, *"are we synced?"*
- Wants to sync: *"sync federation"*, *"pull updates"*, *"federation güncel mi?"*
- Asks about briefings: *"new briefings?"*, *"briefing var mı?"*, *"any messages from other instances?"*
- Wants to update status: *"update my status"*, *"durumu güncelle"*, *"submit status"*
- Acknowledges a briefing: *"ack briefing X"*, *"briefing X'e cevap"*
- Has membership questions: *"federation member miyim?"*, *"are we kernel-conformant?"*
- Is preparing to do new work: *"yeni iş başlıyorum"*, *"new task"* — first run discover-existing-work, then this skill for status update later

## Step-by-Step Workflow

### Step 1: Verify Membership

Read `.federation` from repo root. Confirm:

- `meta_repo_local` exists and is a valid leviathan-meta clone
- `instance_id` is set
- `acknowledged_federation_version` matches current federation manifest version

```bash
# Check federation health
cat .federation
ls -la "$(grep meta_repo_local .federation | sed 's/.*"\(.*\)".*/\1/')"
cat "$(grep meta_repo_local .federation | sed 's/.*"\(.*\)".*/\1/')/federation/manifest.yaml" | head -20
```

If `.federation` doesn't exist or is malformed: warn user, suggest running `scripts/onboard.sh` from meta-repo.

### Step 2: Sync (Pull) Federation

Pull latest from meta-repo:

```bash
META=$(grep meta_repo_local .federation | sed 's/.*"\(.*\)".*/\1/')
git -C "$META" pull --rebase
```

Report what changed (if anything):

```bash
git -C "$META" log --oneline -10  # last 10 commits since old HEAD
```

### Step 3: Check for Briefings Addressed to This Instance

Look for briefings that may need this instance's attention:

```bash
INSTANCE_ID=$(grep instance_id .federation | sed 's/.*"\(.*\)".*/\1/')
BRIEFINGS_DIR="$META/briefings"

# Briefings whose name contains our instance_id
ls "$BRIEFINGS_DIR" | grep -i "$INSTANCE_ID" || echo "No instance-specific briefings"

# All briefings (we should have read them)
ls "$BRIEFINGS_DIR"
```

For each briefing folder, check if we've acknowledged:
```bash
ls "$BRIEFINGS_DIR/<briefing>/ack/" | grep "$INSTANCE_ID" || echo "Not yet acknowledged"
```

If briefings are unacknowledged for >7 days, surface this to user as warning per federation/rules.md R-11.

### Step 4: Check Status Freshness

Per federation/rules.md R-3, status.md should be updated at minimum every 90 days.

```bash
STATUS_FILE="$META/$INSTANCE_ID/status.md"
if [ -f "$STATUS_FILE" ]; then
    LAST_MODIFIED=$(stat -f "%m" "$STATUS_FILE" 2>/dev/null || stat -c "%Y" "$STATUS_FILE")
    NOW=$(date +%s)
    DAYS_OLD=$(( (NOW - LAST_MODIFIED) / 86400 ))
    echo "Status last updated: $DAYS_OLD days ago"
fi
```

If >90 days, suggest update.

### Step 5: Conformance Check

Verify this instance is still federation-conformant per federation/rules.md R-2 (mandatory manifest fields):

```bash
MANIFEST="$META/$INSTANCE_ID/manifest.yaml"
if [ -f "$MANIFEST" ]; then
    grep -E "^\s*(name|domain|forked_from|inherits_from|snapshot_hash|active_version):" "$MANIFEST" || echo "Some required fields missing"
fi
```

If fields missing, surface to user.

### Step 6: Report Summary

Give user a concise status:

```
📡 Federation Status — <instance_id>

Membership: ✓ active (or ⚠ issue)
Last sync:  <X> minutes/hours/days ago
Briefings:  <N> total, <N> unacknowledged
Status freshness: updated <X> days ago (✓ fresh / ⚠ stale)
Conformance: <pass/fail> with details

Recent federation changes:
- <commit summary 1>
- <commit summary 2>

Action items:
- <if any>
```

## Specific Sub-Workflows

### Submit a Status Update

When user says "update status" or "submit status":

1. Read current `<META>/<instance_id>/status.md`
2. Ask user what changed (or read recent commits in this repo)
3. Edit status.md with updates (timestamp, content)
4. Commit + push to meta-repo:
   ```bash
   git -C "$META" add "$INSTANCE_ID/status.md"
   git -C "$META" commit -m "[$INSTANCE_ID] $(date +%Y-%m-%d): $SUMMARY"
   git -C "$META" push
   ```

### Acknowledge a Briefing

When user says "ack briefing X":

1. Read briefing content from `$META/briefings/X/`
2. Confirm understanding with user (or ask if they want a summary)
3. Create ack file: `$META/briefings/X/ack/<instance_id>-ack.md`
4. Include: confirmation of read, any discrepancies/questions, action items planned
5. Commit + push

### File a New Briefing (cross-cutting changes)

When user says "file a briefing":

1. Determine audience: which instances are affected?
2. Create folder: `$META/briefings/$(date +%Y-%m-%d)-<topic>/`
3. Write `00_README.md` (cover letter)
4. Write content files
5. Commit + push
6. Inform user: other instances will see this on their next pull

## Honest Constraints

- **Federation observes, doesn't control** (P-6). This skill does NOT enforce federation rules on this repo. It surfaces, suggests, warns. The user/instance decides.
- **Instance sovereignty wins** (P-8). If federation rules conflict with this repo's runtime constitution, runtime wins. Surface the contradiction; don't auto-resolve.
- **Privacy first** (P-2). Never auto-push sensitive content. Always confirm before any push (per `.federation` `privacy.confirm_push: true`).

## When to Defer

Don't use this skill for:

- Code design decisions (use discover-existing-work + actual work)
- Internal repo state management (that's the repo's own concern)
- Multi-step refactors (those are eylem-tier work, not federation maintenance)

This skill is **federation maintenance** specifically. Like running `apt update` on a Debian box — keeps things current, surfaces issues, doesn't replace doing actual work.

## Failure Modes

- ❌ Don't push without user confirmation (privacy + sovereignty)
- ❌ Don't ignore unacknowledged briefings — surface them
- ❌ Don't suggest editing other instances' subdirectories (P-1 violation)
- ❌ Don't claim federation has authority it doesn't (over local repo)

## Bonus: Onboarding Mode

If invoked with `--onboard` flag (or user says "onboard this repo"), run the full onboard.sh script flow instead:

```bash
META=$(find ~ -maxdepth 4 -name "leviathan-meta" -type d | head -1)
bash "$META/scripts/onboard.sh"
```

(Or curl the script if meta-repo isn't local yet.)
