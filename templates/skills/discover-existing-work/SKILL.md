---
name: discover-existing-work
description: Queries the leviathan-meta federation to surface existing related work BEFORE starting any new task. Solves the rediscovery / knowledge-loss problem. Use proactively when user starts a new eylem, mentions a new topic that might already exist somewhere in the federation, asks "have we done this?", or before designing anything from scratch. Trigger phrases include "new eylem", "let's design", "yeni eylem", "yeni iş", "tasarlayalım", "kuralım", "implement edelim", "başlayalım", or any task-creation moment.
allowed-tools: ["Bash", "Read"]
effort: low
---

You are the federation's institutional memory. Your job: prevent rediscovery, prevent duplicate work, surface accumulated wisdom across all instances.

## Why This Skill Exists

On 2026-05-05, founder almost designed `ConstitutionRegistry` from scratch — until he happened to remember 5 contract interfaces existed from March 28. Without that lucky memory: hours of duplicate work.

This skill makes that memory **systematic** instead of lucky.

## Activation Conditions

Run this skill when ANY of these happens:

- User starts a new eylem (mentions creating new task/action)
- User uses task-creation language: *"new task"*, *"yeni eylem"*, *"tasarlayalım"*, *"kuralım"*, *"implement edelim"*, *"başlayalım"*
- User mentions a topic that might already exist (concept, pattern, code module)
- User says *"have we done this?"*, *"daha önce yaptık mı?"*, *"hatırlatır mısın?"*
- Before designing anything new from scratch (Companion proactive trigger)
- User asks the federation to do something across instances

## Workflow

### Step 1: Identify Search Topic

From user's intent, extract the core topic. Examples:

- *"Let's design an on-chain bridge"* → topic = `on-chain bridge`
- *"Yeni bir capability sistem yaratalım"* → topic = `capability_class`
- *"Tasma için kontract tasarımı"* → topic = `Tasma contract` (or `Constitutional Company`)
- *"Sözcülük strategisi"* → topic = `acik atolye` or `Açık Atölye`

### Step 2: Run Federation Discovery

Execute the federation search tool:

```bash
python3 ~/caba_yasasi/leviathan-meta/tools/federation-search.py --discover "<topic>"
```

If the topic matches a known expansion (`on-chain`, `contract`, `task layer`, `agent`, `constitutional company`, `sync`), discovery mode expands to related keywords automatically.

If no expansion matches, fall back to direct search:

```bash
python3 ~/caba_yasasi/leviathan-meta/tools/federation-search.py "<topic>"
```

### Step 3: Read Top Hits

For matches with weight ≥ 8 (kernel, federation, contracts), Read the actual file at the matched line to verify relevance. Don't trust snippet alone.

For lower-weight matches, snippet might be enough — but if topic is critical, Read.

### Step 4: Report to Founder

Format the report concisely:

```
🔍 Federation Discovery — '<topic>'

✓ EXISTING WORK FOUND in N instances:

  [HIGH-PRIORITY — review before designing]
  - <file>:<line> — <one-line summary of what's there>
  
  [BACKGROUND — relevant context]
  - <file>:<line> — <summary>

⚠ Recommendation: <one of>
  → "Start from existing artifact, refactor/extend"
  → "Existing work is partial — fill gaps"
  → "Existing work is for different purpose — separate concern, but cross-reference"
  → "No structural overlap — new work is genuinely needed"
```

### Step 5: Wait for Founder Acknowledgment

Don't proceed to design until founder confirms how to integrate the existing work. Common responses:

- *"Tamam, refactor edelim"* → use existing as base
- *"Hayır, ayrı bir şey lazım"* → new work, but cross-reference existing
- *"Görmemiştim, bana zaman ver okuyayım"* → pause, let founder review

## Examples

### Example 1: User says "let's design on-chain bridge"

```bash
python3 tools/federation-search.py --discover "on-chain bridge"
```

Returns: 56+ hits including `contracts/interfaces/*.sol` (5 interfaces from March 28), `kernel/07-economy.md` (token economy plans), `briefings/2026-05-05-*` (architecture plan from this session).

Report:
> 🔍 Federation Discovery — 'on-chain bridge'
> 
> ✓ EXISTING WORK FOUND in 4 instances:
> 
>   [HIGH-PRIORITY — review before designing]
>   - contracts/interfaces/ICitizenRegistry.sol — 5 governance interfaces from March 28
>   - briefings/2026-05-05-liveprob-briefing/07_*.md — full integration plan written
>   - federation/manifest.yaml — federation snapshot pattern
> 
> ⚠ Recommendation: Start from existing artifacts. The 5 interfaces cover governance layer; the briefing plans the receipt layer. Refactor B2 references → kernel references; add 2 new interfaces (IConstitutionRegistry, IActionReceipt).

### Example 2: User says "yeni bir prensip yaratalım: dürüst olmak"

```bash
python3 tools/federation-search.py "dürüstlük"
python3 tools/federation-search.py "honesty"
```

Returns: hits in `companion/manifest-public.yaml` (prensip:durustluk v1.1 already exists), `kernel/02-anatomy.md` (mentions honesty principle pattern).

Report:
> 🔍 Federation Discovery — 'dürüstlük / honesty'
> 
> ✓ EXISTING WORK FOUND:
> 
>   - companion/manifest-public.yaml:91 — `prensip:durustluk v1.1` already in master POS
>   - Statement: "Dürüstlük bazen susmaktır — herkes her şeyi duymak zorunda değil"
> 
> ⚠ Recommendation: This principle already exists at master Leviathan level. New eylem should DEPEND_ON existing prensip:durustluk, not duplicate it. If wanting to evolve: version bump to v1.2 with reasoning.

### Example 3: User says "let's add a new mode to ANIMA"

```bash
python3 tools/federation-search.py "ANIMA mode"
python3 tools/federation-search.py --category=anima "mode"
```

Returns: anima/status.md mentions Time Travel modes, theme modes.

Report:
> 🔍 Federation Discovery — 'ANIMA mode'
> 
> ✓ EXISTING MODES IN ANIMA:
> 
>   - Time Travel: Geçmiş Ben + Yansıma (2 modes)
>   - Themes: Enchanted Forest, Ocean, Sunset, Minimal (4 themes)
>   - Personas: Stoic, Growth Mindset, Minimalist, Entrepreneur (4 presets)
> 
> ⚠ Recommendation: Specify which axis the new mode belongs to. If Time Travel — extend to 3rd mode. If themes — add 5th theme. If personas — add preset. New axis means new design effort.

## Output Discipline

- **Be concise.** Founder doesn't have time for exhaustive lists. Top 3-5 hits per category.
- **Be honest.** If discovery finds nothing relevant, say so explicitly: *"No structural overlap found in federation. New work appears genuinely novel."*
- **Be actionable.** End with a clear recommendation, not "here's information, you decide."

## Failure Modes (Don't Do These)

- ❌ Don't run search after starting design. Run BEFORE.
- ❌ Don't dump raw search output. Synthesize.
- ❌ Don't skip Read step for high-priority hits. Verify before reporting.
- ❌ Don't recommend "start from scratch" without checking discovery. Always check first.
- ❌ Don't skip activation when user is in "let's just build it" mode. Especially then — that's when rediscovery happens.

## Bonus: Update Discovery Expansions

If you notice a topic comes up frequently and isn't in `DISCOVERY_EXPANSIONS`, suggest adding it:

> *"This topic ('X') has come up 3+ times this week. Consider adding to DISCOVERY_EXPANSIONS in federation-search.py for faster future discovery."*

The founder can add it; the federation gets smarter over time.
