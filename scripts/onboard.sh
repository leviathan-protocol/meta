#!/bin/bash
#
# onboard.sh — Federation onboarding for a new Leviathan instance repo.
#
# What this does:
#   1. Verifies you're in a git repo
#   2. Clones leviathan-meta locally (if not already)
#   3. Asks for instance_id (must match meta-repo subdirectory)
#   4. Creates .federation config in current repo
#   5. Copies federation-landing + discover-existing-work skills to .claude/skills/
#   6. Appends federation section to CLAUDE.md
#   7. Reports next steps
#
# Run from inside the new instance repo's root:
#   curl -L https://raw.githubusercontent.com/aigentone/leviathan-meta/main/scripts/onboard.sh | bash
#
# Or after cloning leviathan-meta locally:
#   bash <leviathan-meta>/scripts/onboard.sh
#
# Idempotent: safe to re-run for refresh.

set -e

# ============================================================================
# Configuration
# ============================================================================

META_REPO_URL="${META_REPO_URL:-https://github.com/aigentone/leviathan-meta}"
META_PATH="${LEVIATHAN_META_PATH:-$HOME/caba_yasasi/leviathan-meta}"
TODAY=$(date +%Y-%m-%d)

# Colors (graceful fallback for terminals without color support)
if [ -t 1 ]; then
    GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
else
    GREEN=''; YELLOW=''; RED=''; BLUE=''; NC=''
fi

# ============================================================================
# Helper functions
# ============================================================================

info()    { echo -e "${BLUE}[i]${NC} $1"; }
success() { echo -e "${GREEN}[✓]${NC} $1"; }
warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
error()   { echo -e "${RED}[✗]${NC} $1" >&2; }

# ============================================================================
# Step 1: Verify environment
# ============================================================================

info "Verifying environment..."

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
    error "Not in a git repository. Run from your instance repo's root."
    exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")
success "Git repo: $REPO_ROOT (name: $REPO_NAME)"

# ============================================================================
# Step 2: Clone or update meta-repo
# ============================================================================

if [ ! -d "$META_PATH" ]; then
    info "leviathan-meta not found at $META_PATH"
    info "Cloning from $META_REPO_URL..."
    mkdir -p "$(dirname "$META_PATH")"
    git clone "$META_REPO_URL" "$META_PATH"
    success "Cloned to $META_PATH"
else
    info "leviathan-meta exists at $META_PATH"
    info "Pulling latest..."
    git -C "$META_PATH" pull --rebase 2>/dev/null || warn "Pull failed (offline?). Continuing with local copy."
    success "Updated"
fi

# Verify it's actually a meta-repo
if [ ! -f "$META_PATH/federation/manifest.yaml" ]; then
    error "$META_PATH does not look like a leviathan-meta repo (federation/manifest.yaml missing)"
    exit 1
fi

# ============================================================================
# Step 3: Determine instance_id
# ============================================================================

if [ -f "$REPO_ROOT/.federation" ]; then
    EXISTING_ID=$(grep -E "^\s*instance_id:" "$REPO_ROOT/.federation" 2>/dev/null | head -1 | sed -E 's/.*"([^"]+)".*/\1/' || echo "")
    if [ -n "$EXISTING_ID" ]; then
        info "Existing .federation found, instance_id=$EXISTING_ID"
        read -r -p "Use existing instance_id '$EXISTING_ID'? [Y/n] " response
        if [[ "$response" =~ ^[Nn] ]]; then
            EXISTING_ID=""
        fi
    fi
fi

if [ -z "$EXISTING_ID" ]; then
    echo ""
    info "Available instance_ids in meta-repo:"
    for d in "$META_PATH"/*/; do
        bn=$(basename "$d")
        if [ -f "$d/status.md" ]; then
            echo "    - $bn"
        fi
    done
    echo ""
    read -r -p "Instance ID for this repo: " INSTANCE_ID

    if [ -z "$INSTANCE_ID" ]; then
        error "Instance ID is required."
        exit 1
    fi
else
    INSTANCE_ID="$EXISTING_ID"
fi

# Verify subdirectory exists
if [ ! -d "$META_PATH/$INSTANCE_ID" ]; then
    warn "$META_PATH/$INSTANCE_ID does not exist."
    warn "After onboarding, you'll need to create it via R-1 onboarding flow:"
    warn "  1. mkdir $META_PATH/$INSTANCE_ID"
    warn "  2. Copy templates/instance-status-template.md → status.md"
    warn "  3. Copy templates/instance-manifest-template.yaml → manifest.yaml"
    warn "  4. Add entry to README.md Subdirectory Ownership table"
    warn "  5. File first-status briefing"
    echo ""
    read -r -p "Continue with onboarding anyway? [y/N] " response
    if [[ ! "$response" =~ ^[Yy] ]]; then
        info "Aborted. Run again after creating the subdirectory."
        exit 0
    fi
fi

# ============================================================================
# Step 4: Create/update .federation config
# ============================================================================

info "Writing .federation config..."

if [ -f "$REPO_ROOT/.federation" ]; then
    cp "$REPO_ROOT/.federation" "$REPO_ROOT/.federation.bak.$TODAY"
    info "Backup: .federation.bak.$TODAY"
fi

cat > "$REPO_ROOT/.federation" <<EOF
# Federation Membership Config
# Generated by onboard.sh on $TODAY
# Edit freely. See $META_PATH/templates/federation-config-template.yaml for full schema.

federation:
  meta_repo_url: "$META_REPO_URL"
  meta_repo_local: "$META_PATH"
  instance_id: "$INSTANCE_ID"
  acknowledged_federation_version: "0.1.0"

sync:
  mode: "manual"   # manual | hook | cron — start with manual, advance later
  last_pull: null
  last_push: null

publish:
  status_file: "status.md"
  manifest_file: "manifest.yaml"

discovery:
  pre_task_search: true   # auto-query federation before starting major new work

privacy:
  use_public_filter: true
  confirm_push: true

# Onboarding info
onboarding:
  date: "$TODAY"
  by: "scripts/onboard.sh"
  source_repo: "$REPO_NAME"
EOF

success "Wrote $REPO_ROOT/.federation"

# ============================================================================
# Step 5: Copy skills to .claude/skills/
# ============================================================================

info "Installing federation skills..."

mkdir -p "$REPO_ROOT/.claude/skills/federation-landing"
mkdir -p "$REPO_ROOT/.claude/skills/discover-existing-work"

if [ -f "$META_PATH/templates/skills/federation-landing/SKILL.md" ]; then
    cp "$META_PATH/templates/skills/federation-landing/SKILL.md" \
       "$REPO_ROOT/.claude/skills/federation-landing/SKILL.md"
    success "Installed federation-landing skill"
else
    warn "federation-landing template not found in meta-repo"
fi

if [ -f "$META_PATH/templates/skills/discover-existing-work/SKILL.md" ]; then
    cp "$META_PATH/templates/skills/discover-existing-work/SKILL.md" \
       "$REPO_ROOT/.claude/skills/discover-existing-work/SKILL.md"
    success "Installed discover-existing-work skill"
else
    warn "discover-existing-work template not found in meta-repo"
fi

# ============================================================================
# Step 6: Append federation section to CLAUDE.md
# ============================================================================

CLAUDE_MD="$REPO_ROOT/CLAUDE.md"
FEDERATION_MARKER="<!-- FEDERATION_MEMBERSHIP_BEGIN -->"

if [ -f "$CLAUDE_MD" ]; then
    if grep -q "$FEDERATION_MARKER" "$CLAUDE_MD"; then
        info "CLAUDE.md already has federation section, skipping append"
    else
        info "Appending federation section to CLAUDE.md..."
        cp "$CLAUDE_MD" "$CLAUDE_MD.bak.$TODAY"

        cat >> "$CLAUDE_MD" <<EOF

---

$FEDERATION_MARKER
## Federation Membership (added $TODAY by onboard.sh)

This repo is a member of the **leviathan-meta federation** — a coordination
substrate connecting Leviathan instances.

**Identity:**
- Instance ID: \`$INSTANCE_ID\`
- Federation URL: $META_REPO_URL
- Local meta-repo: \`$META_PATH\`
- Config: \`.federation\` (this repo's root)

**Quick references:**
- Federation principles: \`$META_PATH/federation/principles.md\` (10 principles, P-1..P-10)
- Federation rules: \`$META_PATH/federation/rules.md\` (17 rules, R-1..R-17)
- Cross-instance search: \`python3 $META_PATH/tools/federation-search.py "<query>"\`
- Discovery (multi-keyword): \`python3 $META_PATH/tools/federation-search.py --discover "<topic>"\`

**Skills installed:**
- \`.claude/skills/federation-landing/\` — federation awareness + sync helpers
- \`.claude/skills/discover-existing-work/\` — auto-query federation before new tasks

**Federation discipline (what you implicitly accept by being a member):**
- P-1: Subdirectory ownership — only edit \`$META_PATH/$INSTANCE_ID/\`, not other instances
- P-2: Privacy sovereignty — never push secrets, sensitive POS, or raw decisions
- P-3: Kernel anchor required — your manifest must declare \`forked_from: leviathan-kernel@vX.Y.Z\`
- P-4: No silent override — surface discrepancies via builder-report or briefing reply
- P-5: Append-only briefings — never edit/delete existing briefings
- P-6: Sovereign Console discipline — federation observes, doesn't control
- P-7: Reasoning trail at federation layer
- P-8: **Instance sovereignty outranks federation convenience** — your runtime constitution always wins

**Workflow:**
- Before any major new task: invoke \`discover-existing-work\` skill or run federation-search
- After major changes: update \`$META_PATH/$INSTANCE_ID/status.md\` and push
- For cross-cutting changes: file a briefing in \`$META_PATH/briefings/YYYY-MM-DD-<topic>/\`
- Read \`$META_PATH/briefings/\` for briefings addressed to this instance

If anything in federation files contradicts THIS REPO's runtime constitution,
**this repo's runtime constitution wins**. The federation is informational/
coordinative; it does not override local sovereignty.

For full landing skill behavior, see \`.claude/skills/federation-landing/SKILL.md\`.
<!-- FEDERATION_MEMBERSHIP_END -->
EOF
        success "Appended to CLAUDE.md (backup: CLAUDE.md.bak.$TODAY)"
    fi
else
    warn "CLAUDE.md not found in repo root. You may want to create one and reference federation."
fi

# ============================================================================
# Step 7: Final report
# ============================================================================

echo ""
echo "============================================================"
success "Federation Onboarding Complete"
echo "============================================================"
echo ""
echo "  Instance ID:    $INSTANCE_ID"
echo "  Meta-repo:      $META_PATH"
echo "  Config:         $REPO_ROOT/.federation"
echo "  Skills:         $REPO_ROOT/.claude/skills/{federation-landing,discover-existing-work}/"
echo "  CLAUDE.md:      federation section ${CLAUDE_MD:+appended}"
echo ""
echo "Next steps:"
echo "  1. Read federation principles + rules:"
echo "       cat $META_PATH/federation/principles.md"
echo "       cat $META_PATH/federation/rules.md"
echo ""
echo "  2. Verify your manifest declares kernel anchor (forked_from):"
echo "       cat $META_PATH/$INSTANCE_ID/manifest.yaml 2>/dev/null || echo '(create from template)'"
echo ""
echo "  3. Test federation search:"
echo "       python3 $META_PATH/tools/federation-search.py \"your-topic-here\""
echo ""
echo "  4. Commit your changes:"
echo "       git add .federation .claude/skills/ CLAUDE.md"
echo "       git commit -m \"Onboard to leviathan-meta federation as $INSTANCE_ID\""
echo ""
echo "  5. (If new instance) Create your subdirectory in meta-repo and submit"
echo "     first-status briefing per federation/rules.md R-1."
echo ""
echo "Welcome to the federation."
