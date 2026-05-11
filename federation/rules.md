# Federation — Rules (Layer 3)

> **Part version:** 0.1.0 · **Tier:** mutable (most rules) / protected (membership rules) · **Last touched:** 2026-05-05  
> **Scope:** concrete coordination protocols. Phrased in principles (federation/principles.md), expressed in terms (federation/terms.md). Rules implement principles.

---

## §1. Why Rules Layer

Principles tell you how to think. Rules tell you what to do. Without rules, every coordination action becomes a fresh interpretation of principles. Rules compress recurring decisions into reproducible protocol.

---

## §2. Membership Rules

### R-1. Becoming a Federation Member (protected)

To register as a federation member, an instance owner must:

1. Create a subdirectory at `leviathan-meta/<instance-name>/`
2. Copy `templates/instance-status-template.md` to `<instance-name>/status.md` and fill in
3. Copy `templates/instance-manifest-template.yaml` to `<instance-name>/manifest.yaml` and fill in (or `manifest-public.yaml` for instances with private subset disclosure)
4. Add an entry to `README.md` Subdirectory Ownership table indicating which machine owns the new subdirectory
5. Submit a first-status briefing in `briefings/YYYY-MM-DD-<instance>-genesis/` describing what the instance is and why it joined
6. Push commit to main branch

The instance is now a member. No central approval required (P-2 sovereignty + P-8 fork freedom). The founder may issue cautionary briefings if the genesis declaration looks problematic, but cannot prevent membership.

### R-2. Mandatory Manifest Fields (protected)

Each instance manifest (`manifest.yaml` or `manifest-public.yaml`) must contain:

- `instance.name` (string)
- `instance.domain` (string)
- `instance.owner_machine` (string)
- `inheritance.forked_from` (must be a valid `leviathan-kernel@vX.Y.Z`)
- `inheritance.inherits_from` (`null` or valid `master-leviathan@vX.Y.Z`)
- `constitution.snapshot_hash` (sha256 hex string)
- `constitution.active_version` (semver)
- `tiers_present` (list, must include at least one of immutable/protected/mutable)
- `capability_classes` (list of classes from kernel/10-tasks.md §4)
- `falsification` (list of claim/refuted_if pairs — at least one)

Missing required fields → conformance check fails → instance is non-member until corrected.

### R-3. Status Update Cadence (mutable)

Instance owners are encouraged (not required) to update `status.md` every:

- **At minimum:** every 90 days (kernel/04-living.md §6 decay cadence)
- **Triggered:** any version bump, snapshot_hash change, milestone, blocker
- **Recommended:** weekly for active instances

If status.md hasn't been touched in 90+ days, federation considers the instance dormant. Dormant ≠ inactive (maintenance mode is fine), but dormancy should be acknowledged in status if intentional.

---

## §3. Sync Workflow Rules

### R-4. Pull-Rebase Before Edit (mutable)

Every machine, before editing files in `leviathan-meta/`:

```bash
cd leviathan-meta/
git pull --rebase
```

Skipping this leads to merge conflicts. Rebase (not merge) keeps history linear and easy to follow.

### R-5. Subdirectory Edits Only (protected — implements P-1)

Each machine edits only files in its owned subdirectory. Cross-cutting needs:

- **Kernel evolution:** founder edits `kernel/`, files briefing to all instances
- **Contract changes:** founder edits `contracts/`, files briefing to affected instances
- **README updates:** founder edits `README.md` for ownership matrix changes; instance owners may PR for typo fixes

Direct edits to other instances' subdirectories: forbidden. Use briefings.

### R-6. Commit Message Format (mutable)

```
[machine-name] [YYYY-MM-DD]: [brief description]
```

Examples:
- `[master-mac] 2026-05-05: kernel/10-tasks.md created`
- `[liveprob-mac] 2026-05-06: status.md updated post-briefing-ack`
- `[mac-mini] 2026-05-07: security/status.md migration v4 progress`

Why: makes git log greppable across machines. `git log --grep="liveprob-mac"` shows everything that machine did.

### R-7. Push After Session, Not During (mutable)

Push at the end of a coherent change, not after every micro-edit. Reduces noise, makes diffs easier to review. If a long session, intermediate pushes are fine; just batch them logically.

### R-8. Never Force-Push to Main (immutable)

Force-pushing rewrites history, invalidating other machines' rebase bases. This is forbidden in `leviathan-meta`. If you've made a mistake, fix it with a new commit.

(Hotfix exception: if a secret is committed accidentally, force-push to remove from history is allowed BUT requires immediate broadcast to all federation members so they can re-clone.)

---

## §4. Briefing Rules

### R-9. Briefing Structure (protected)

A briefing is a folder under `briefings/` named `YYYY-MM-DD-<topic>/`. It must contain:

- A cover letter (named `00_README.md` or `00_READ_FIRST_*.md`)
- The briefing content itself (markdown files)
- An `ack/` subdirectory (created when first acknowledgment lands)

Optional content: diagrams, supporting docs, draft amendments.

### R-10. Append-Only (immutable — implements P-5)

Once published, a briefing's content files are not edited. Corrections are issued as new briefings (`YYYY-MM-DD-<topic>-correction/`) that reference the original.

Exception: typo fixes that don't change meaning. Annotated in commit message: `[typo-fix in 2026-05-05-liveprob-briefing]`.

### R-11. Acknowledgment Window (mutable)

Instances are encouraged to acknowledge briefings within 7 days of receipt. Late acknowledgments are accepted; silent non-acknowledgment for 30+ days triggers a follow-up from founder.

### R-12. Discrepancy Reporting (protected — implements P-4)

If an instance reading a briefing finds discrepancy with local reality, the instance must:

1. NOT act on the briefing's contradicted claim
2. Surface the discrepancy in its acknowledgment OR via dedicated `briefings/YYYY-MM-DD-<instance>-discrepancy/`
3. Continue with existing constitution per kernel I-2 (instance constitution wins)
4. Wait for founder reply / clarification

If urgency is high, mark `[BLOCKING]` in subject.

---

## §5. Privacy Rules

### R-13. Strict .gitignore (immutable — implements P-2)

The repo's `.gitignore` blocks:

- All cryptographic material (keys, certs)
- All wallet files
- All `.env` files
- Raw decision logs from any instance
- Personal POS sensitive content (shadows, people, raw kavramlar)
- Therapy session content
- Threat intel raw findings

If you find yourself wanting to commit one of these — STOP. Use a separate channel or process.

### R-14. Pre-Commit Secret Scan (mutable, recommended)

Each machine should run a secret-scanner pre-commit hook (gitleaks, trufflesecrets, or equivalent). If a secret slips into history:

1. Force-push to remove (R-8 hotfix exception)
2. Rotate the leaked secret
3. Broadcast to all members
4. File post-mortem briefing

### R-15. Manual Review Before Push (mutable, recommended)

`git diff --staged` before `git push`. Eyes on the actual content. Especially for:

- Status manifests (might inadvertently contain PII)
- Briefing acknowledgments (might quote private context)
- Manifest YAML changes (snapshot_hash should match local computation)

---

## §6. Public Mirror Rules

### R-16. Public Mirror Derivation (mutable, future)

When `leviathan-public` repo exists (currently TBD), it will be derived from this repo by:

1. Apply public-safe filters per each instance's `manifest-public.yaml` (or equivalent)
2. Remove all `*-private.md` files
3. Strip private content from compiled views
4. Include kernel/, contracts/, federation/, public templates, public briefings

The derivation script lives in this repo at `scripts/derive-public.py` (TBD).

### R-17. Pre-Mirror Review (mutable, future)

Before each mirror push, founder reviews the diff. No automated push of public content without human review (currently — may relax once trust in derivation is established).

---

## §7. Conformance Check

The federation should provide a tool (TBD: `tools/federation-conformance.py`) that:

- Validates each instance manifest against R-2 mandatory fields
- Verifies snapshot_hash matches what the instance's compute_snapshot reports
- Checks status.md non-staleness (R-3)
- Detects subdirectory edit violations (R-5)
- Reports missing acknowledgments (R-11)

Until the tool exists, conformance is checked manually via founder review.

---

## §8. Rule Versioning

Each rule is mutable unless marked otherwise. Mutability tier per kernel/04-living.md §3:

- **Immutable** (R-8, R-10, R-13): cannot weaken; forking is permitted, weakening is not
- **Protected** (R-1, R-2, R-5, R-9, R-12): change with reasoning + founder approval
- **Mutable** (R-3, R-4, R-6, R-7, R-11, R-14, R-15, R-16, R-17): refine with single commit + CHANGELOG entry

---

*Federation rules layer. Refer to `federation/meta-rules.md` for amendment procedure (how rules themselves change).*
