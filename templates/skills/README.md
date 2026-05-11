# templates/skills/ — Federation-Wide Skills

> Canonical skill library distributed by the federation. When a new repo onboards via `scripts/onboard.sh`, these skills are copied to that repo's `.claude/skills/` directory.

---

## What's Here

| Skill | Purpose | Trigger |
|---|---|---|
| `federation-landing/` | Federation membership maintenance — sync, briefings, status updates, conformance check | "federation status", "sync federation", "check briefings", "update status" |
| `discover-existing-work/` | Auto-query federation before starting new tasks. Solves rediscovery / knowledge-loss problem. | "new eylem", "yeni iş", "tasarlayalım", "let's design", "have we done this?" |

## Why These Are Canonical Here

Each instance has its own runtime constitution (its own `.claude/skills/` with instance-specific skills like therapy, indexing, etc.). But these two skills are **federation-wide** — every instance benefits from having them.

By centralizing them in `leviathan-meta/templates/skills/`, we get:

1. **Single source of truth.** When the skill is improved, all instances pull the update.
2. **Onboarding automation.** New repos get them automatically via `onboard.sh`.
3. **Versioning.** Skill changes are tracked in meta-repo's git history.
4. **Discovery.** Federation members can find the canonical version when looking.

## Updating a Skill

When you (founder) want to improve `federation-landing` or `discover-existing-work`:

1. Edit the version here in `leviathan-meta/templates/skills/<skill>/SKILL.md`
2. Commit + push to meta-repo
3. Other instances will get the update on their next `git pull` of meta-repo
4. They can re-run `onboard.sh` to refresh their local copy, OR symlink to meta-repo's version

If a member instance has customized their copy, they're sovereign — federation update suggests, doesn't override (P-6 + P-8).

## Adding a New Federation-Wide Skill

If a skill genuinely benefits ALL instances (not just one), it belongs here:

1. Create `templates/skills/<new-skill>/SKILL.md` following standard skill format
2. Update `scripts/onboard.sh` to copy it
3. Update this README's table
4. Add `briefings/YYYY-MM-DD-new-federation-skill/` announcing the addition
5. Other instances pull, ack, install

If a skill is only useful for ONE instance, keep it in that instance's repo, not here.

## Customization Discipline

When a member instance copies a skill from here:

- **Allowed:** add instance-specific examples to the skill file (within the skill's own copy)
- **Allowed:** disable a skill if it doesn't apply (don't install it, or remove the file)
- **Discouraged:** silently modify behavior — surface via briefing instead
- **Forbidden (P-5):** push your modified version back to meta-repo and call it canonical

If you want to propose canonical change to a skill: file a briefing, federation-amend per `meta-rules.md` MR-2.

---

*Federation-wide skill library. Updates flow through git. Customization is sovereign.*
