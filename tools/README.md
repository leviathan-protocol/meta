# tools/ — Federation Tooling

> Operational utilities for the federation. Pure Python, no external dependencies (except where noted).

---

## federation-search.py

The flagship tool. Solves the **knowledge loss / rediscovery** problem by surfacing existing work across all federation instances before new tasks begin.

### The Problem It Solves

Without this tool: founder remembered (or forgot) where things lived. Tonight (2026-05-05) we almost designed `ConstitutionRegistry` from scratch — until founder happened to remember 5 contract interfaces existed from March 28. Without that memory: hours of duplicate work.

With this tool: query before designing. The federation's accumulated knowledge becomes searchable across all instances.

### Usage

```bash
# Single keyword search across federation
python3 tools/federation-search.py "ConstitutionRegistry"

# Search a specific category only
python3 tools/federation-search.py "capability_class" --category=kernel

# Discovery mode — multi-keyword expansion of a topic
python3 tools/federation-search.py --discover "on-chain bridge"

# JSON output for programmatic use
python3 tools/federation-search.py "Açık Atölye" --json

# List categories + discovery topic expansions
python3 tools/federation-search.py --list-categories
```

### Categories (Authority-Weighted)

| Category | Weight | Purpose |
|----------|--------|---------|
| `kernel` | 10 | Abstract substrate (canonical) |
| `federation` | 9 | Federation's own constitution |
| `contracts` | 8 | Master governance contracts |
| `briefings` | 7 | Inter-agent briefings (append-only) |
| `companion`, `liveprob`, `security`, `tasma`, `atlas`, `anima` | 6 | Member instances |
| `templates` | 5 | Onboarding templates |

Higher weight = more authoritative source. Search results are sorted by category weight.

### Discovery Mode

Discovery mode expands a topic to related keywords automatically. Example:

```bash
python3 tools/federation-search.py --discover "on-chain bridge"
# Expands to: on-chain, onchain, chain_writer, ConstitutionRegistry,
#             snapshot_hash, Solidity, Avalanche, Fuji, smart contract
```

Built-in expansions for: `on-chain`, `contract`, `task layer`, `agent`, `constitutional company`, `sync`. Add more in `DISCOVERY_EXPANSIONS` dict in the script.

### How To Add Discovery Topics

Edit the `DISCOVERY_EXPANSIONS` dict in `federation-search.py`:

```python
DISCOVERY_EXPANSIONS = {
    "your-topic": ["keyword1", "keyword2", "keyword3"],
    # ...
}
```

Then test: `python3 tools/federation-search.py --discover "your-topic"`.

### Implementation Notes

- **Pure Python stdlib** — no external deps (no ripgrep needed)
- Searches `.md`, `.yaml`, `.yml`, `.json`, `.sol`, `.py`, `.toml`, `.txt`, `.sh`
- Skips `.git/` and other hidden directories
- Case-insensitive
- Performance: scans the whole federation (~50 files, < 1MB) in milliseconds

### Recommended Integration

**For founders / Companion at session start:**

Run discovery on every new eylem topic before designing:

```bash
python3 ~/caba_yasasi/leviathan-meta/tools/federation-search.py --discover "your-new-task"
```

This catches duplications before they happen.

**For Companion skill integration:**

See `.claude/skills/discover-existing-work/SKILL.md` in the Eternal Companion repo for a Companion-side skill that automates this query.

---

## Future Tools (TODO)

### federation-conformance.py (planned)

Validates each instance's manifest against `federation/rules.md` R-2 (mandatory fields), checks subdirectory ownership compliance, detects status staleness, reports missing acknowledgments.

### derive-public.py (planned)

Generates `leviathan-public` mirror from this private repo by applying public-safe filters per each instance's `manifest-public.yaml`.

### report-status.py (planned, instance-side)

Helper for instance machines to update their own `status.md` and push to meta-repo. Reads instance's `.federation` config.

### read-member.py (planned, instance-side)

Helper for instance machines to query other members' public manifests. Reads from local clone of meta-repo (assumes pull-rebase happened recently).

---

## Design Philosophy

Tools in this directory should:

- **Have zero or minimal external dependencies** — meta-repo should run on bare Python
- **Be readable as documentation** — code is the spec
- **Fail gracefully** — surface useful errors, don't crash silently
- **Be composable** — JSON output for piping, exit codes for CI
- **Respect privacy** — never write outside meta-repo without explicit flag
- **Work offline** — no network calls in core search/conformance

This matches the federation's own principles (P-2 Privacy, P-9 Frozen = Dead, P-10 Adaptation Rate).
