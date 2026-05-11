# CHANGELOG — Kernel Modifications Log

> **Part version:** 0.1.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-05
> **Scope:** every modification to any kernel part. Format mirrors `openpos/my-pos/changelog.yaml`. Required by `00-meta.md` §6 (self-reference) and `04-living.md` §5 (versioning everywhere).

This file is the meta-rules in action. The kernel claims that frozen documents lie about their own evolution; this CHANGELOG is the test that the kernel does not lie about its own.

Format: each entry has **date · part · version bump · trigger · rationale · approver**. Entries are ordered most recent first.

---

## 2026-05-05 — `kernel/10-tasks.md` Created (Task Layer Part)

### `kernel/10-tasks.md` — created at v0.1.0

- Trigger: Cross-instance pattern observation in 2026-05-05 design session. Three live implementations (Liveprob `task_inbox` + `DecisionEntry`, Companion POS `eylemler/`, Security Leviathan `Action Profile` + `GateState` + canonical runner) were observed to share identical structural schema across radically different domains (personal identity, financial decisions, security operations). The founder's articulation: "this structure for the eylem is also the task structure in the autonomous system." This is the Task ↔ Constitutional Element structural identity claim, parallel to and reinforcing the POS↔Constitution claim in `01-why §3`.
- Rationale: Without a kernel part naming this identity, instances treat tasks as separate from constitutional content. The result is theater (constitution as audit reference, tasks as operational reality). With this part, tasks are explicitly the runtime expression of constitutional content — versioned, evidenced, lifecycle-governed, capability-classified. The eight-class capability taxonomy is borrowed from Security Leviathan (`LEVIATHAN_CAPABILITY_CLASS_TEMPLATES`) where it originated; this part generalizes it. The evidence requirement enforcement pattern is borrowed from Liveprob D.1.6 (`runner.py _audit_decision_evidence`, settled 2026-05-04). The outcome → lesson loop is the runtime engine that closes the substance↔governance circuit observed in Liveprob D.2 (settled 2026-05-05, first complete loop).
- Scope: this part asserts I-1 (reasoning trail required) at task-write time and I-7 (no retroactive amendment) for settled outcomes. Cross-references 02-anatomy (extends 4-layer with task as runtime expression), 04-living (loops into evolution mechanism), 06-mind (Mind primitives operate on task schema), 07-economy (slashing is a task at sensitive_active class), 08-shadow (evidence requirement is structural defense against Constitution as Theater).
- Compatibility: instances MUST declare a task layer using the universal schema; field removal is a divergent-fork act. Existing instances (Liveprob, Companion POS, Security Leviathan) require minimal adaptation — Liveprob already conforms via D.1.6, POS requires adding `capability` block to existing eylemler, Security requires kernel-anchoring (separate work).
- Manifest impact: `parts:` extended with `10-tasks` entry. `invariants: I-1.asserted_in` and `I-7.asserted_in` now include `10-tasks §6` and `10-tasks §3` respectively. `terms:` extended with four new entries: `task-layer`, `capability-class`, `outcome-lesson-loop`, `evidence-requirement`.
- Approver: founder.

---

## 2026-05-04 — `templates/` Created (Amendment Plan + Lesson Scaffolds)

### `templates/amendment-plan-template.md` — created at v0.1.0

- Trigger: `specs/research/spec-kit-inspiration.md` §5.1 identified spec-kit's Constitution Check Gate as the highest-leverage borrowable pattern. Today, kernel amendments and instance Lessons have no required template — `panels/0001-*` reasoning trail is freeform Markdown. Without a structural prompt, an amendment author can fail to confront `I-1`…`I-7` impact at all (Panel 0001 §3 documented exactly this failure mode for `I-2`).
- Rationale: Markdown template with mandatory `## §3. Invariant Impact Check` table — every row of `I-1`…`I-7` annotated `unchanged | strengthened | weakened`, rationale required for any non-`unchanged` row, `weakened` row treated as a divergent-fork declaration per `00-meta.md` §4.5. Sections also include propagation list (forces enumeration of dependent files), risks (both acceptance and status-quo perspectives), falsification (named observable that would refute the amendment), and panel signature placeholders. The template is a forcing function, not a verdict; only the panel approves.
- Scope: required for amendments touching `kernel/`, `specs/`, `tools/`, `templates/`, or `openpos/schema/` (kernel-owned scope per `specs/FORK_PROTOCOL.md` §2). Not required for instance-owned changes or `panels/*` reasoning trails.
- Compatibility: forks inherit the template; divergent forks use it to declare their weakening at the moment of amendment, which is the same divergence-declaration discipline `FORK_PROTOCOL.md` §3.2 requires.
- Approver: founder.

### `templates/lesson-template.md` — created at v0.1.0

- Trigger: `specs/research/spec-kit-inspiration.md` §5.2 identified that the implicit chain `lesson-observed → amendment-propose → panel-convene → conformance-verify → propagate` is documented in three different files and enforced nowhere. The upstream artifact (Lesson) has no defined shape, so an instance operator has no canonical way to surface a kernel-relevant pattern.
- Rationale: Markdown template for instance-recorded structural observations. Frontmatter carries `recurrence` (single observations are not lessons), `kernel_relevant` (explicit boolean), and `proposes` (link to draft amendment if promoted). Mandatory `## §5. Kernel-relevance check` enumerates seven categories the lesson could change (invariant scope, Amendment Procedure, glossary term, immutable constant, tier definition, fork-protocol clause, conformance check); if all seven are unchecked the lesson stays instance-local. Falsification section forced — a non-falsifiable observation is a preference, not a lesson.
- Scope: instance-owned in normal use (`<instance-root>/lessons/`); kernel-side use is rare (panel retrospectives that observe their own structural issue).
- Compatibility: forks inherit the template; instance-owned `lessons/` directories are not part of the kernel-owned scope and the kernel does not mandate their existence, only the format if used.
- Approver: founder.

### `kernel/manifest.yaml` — extended (templates: block added)

- Trigger: new `templates/` directory needs to be discoverable in the structural skeleton; otherwise manifest drift cannot detect a template change.
- Rationale: new top-level `templates:` key with two entries (`amendment-plan`, `lesson`), each carrying version, tier (protected), role description, `depends_on_kernel`, and `referenced_by`. Mirrors the `parts:`/`specs:`/`tools:` shape so the manifest stays one consistent graph. Glossary entry version bumped 0.5.0 → 0.6.0 in the same edit (3 new terms below).
- Approver: founder.

### `kernel/glossary.md` — amended to v0.6.0

- Trigger: three new structurally-loaded terms introduced by the templates and the chain they participate in.
- Rationale: added **Amendment Plan** (the filled-out copy of the amendment template, required input to a panel session), **Invariant Impact Check** (the mandatory `## §3` section enumerating I-1..I-7 with weakening = divergence-declaration semantics), **Lesson** (structural observation stabilized over time, distinguished from one-off observations by reproducibility, upstream artifact of the lesson → propagate chain). Existing **Clarify Marker** entry's scope updated to include `templates/` directory (kernel-owned scaffolds inherit the same `--clarify-debt` scope as `kernel/`).
- Approver: founder.

### `tools/conformance.py` — `_CLARIFY_SCAN_DIRS` extended

- Trigger: `templates/` is kernel-owned and may contain `[CLARIFY: ...]` markers; without scope inclusion, debt in templates would be invisible.
- Rationale: added `"templates"` to the scan-dirs tuple. No new flag; behavior is additive within the existing `--clarify-debt` mode. Conformance tool version is not bumped (pure scope addition, no logic change).
- Approver: founder.

---

## 2026-05-04 — `specs/FORK_PROTOCOL.md` Created + Fork Tooling + Conformance `--fork` Mode

### `specs/FORK_PROTOCOL.md` — created at v0.1.0

- Trigger: `kernel/03-constellation.md` §6 specifies abstract forking requirements but no operational mechanism. The kernel's first claim ("forking is encouraged") was theoretically open and operationally unspecified — Founder Independence Criterion #1 (`STATUS.md` §2) cannot be tested when forking is undefined. Discussion: user noted that the framework is not yet ready for public push, AND that the founder cannot fork the kernel for their own private POS instance with the spec as it stood. The missing layer was named: a concrete fork procedure.
- Rationale: vendored-fork model selected over submodule on five grounds (forkability under network partition, operator autonomy, privacy of fork existence, privacy of fork content, mechanical drift detection). Three file boundary categories defined: kernel-owned (immutable in fork), instance-owned (private to operator), hybrid (template + instance customization). Schema for `.fork-manifest.yaml` specified including upstream provenance, fork type (pre-conformance / conformant / divergent), kernel-owned content hashes, and divergence enumeration. Init/pull/conformance procedures specified at the level of explicit steps with named failure modes.
- Test plan named (§9): three test forks before promotion to v0.2.0 — (1) The Eternal Companion retrofit, (2) fresh synthetic fork, (3) deliberately divergent fork. Each test produces an outcome record in `panels/0002-fork-protocol/`.
- Status: build-phase carve-out per Panel 0001 precedent. Founder-only authorship of v0.1.0 recorded explicitly. Panel review required before v0.2.0.
- Approver: founder.

### `tools/fork-init.sh` — created at v0.1.0

- Trigger: spec §6 specifies fork initialization procedure; without a script, the procedure is documentation only.
- Rationale: bash script. Inputs: target directory (must be empty or non-existent), environment overrides for instance metadata. Procedure: validates target, copies kernel-owned (kernel/, specs/, tools/, .gitignore) and hybrid (.claude/, README.md), creates instance-owned skeleton (openpos/my-pos/{kavramlar,prensipler,eylemler,golgeler,protokoller,people}/, memory/raw, memory/indexed, sessions/, notes/, bible/), copies openpos/{compile.py,export.py,schema/} as kernel-owned (POS schemas remain compatible across forks), computes SHA-256 of every kernel-owned file, writes `.fork-manifest.yaml`, runs `git init` if needed.
- Approver: founder.

### `tools/fork-pull.sh` — created at v0.1.0

- Trigger: spec §7 specifies pull procedure for upstream kernel updates flowing into a vendored fork; without a script, drift is the operator's manual problem.
- Rationale: bash script. Inputs: run from inside fork (cwd). Reads `.fork-manifest.yaml`. For each kernel-owned file: if local SHA matches recorded hash, safe to overwrite from upstream; if differs, flagged as local divergence (not overwritten). For each hybrid file: 3-way merge with `git merge-file` against upstream's last_pull commit as base. Conflicts written with standard markers; pull aborts at conflict, requires manual resolution and re-run. After successful pull, kernel-owned hashes recomputed, `last_pull` block updated, `forked_from.kernel_version` refreshed.
- Approver: founder.

### `tools/conformance.py` — extended to v0.2.0 (`--fork` mode added)

- Trigger: spec §8 requires fork-specific conformance check. Existing harness checks invariants and manifest drift but has no awareness of fork-manifest or fork-type semantics.
- Rationale: added `check_fork()` function. Validates `.fork-manifest.yaml` parses and has required fields; verifies `forked_from.kernel_version` matches the fork's local `kernel/manifest.yaml`; checks instance-owned dirs exist; computes SHA-256 of every kernel-owned file and compares to recorded hashes. Three-state result: PASS (no drift, fork_type matches reality), DIVERGENT (drift declared in `divergences:` block, fork_type=divergent), FAIL (drift not declared, or fork_type/reality mismatch, or required field missing). When `--fork` is passed, the harness runs the standard kernel/specs invariant checks against the fork's own copies, then the fork-specific checks. Exit codes: 0 PASS, 1 FAIL, 2 invocation error, 3 DIVERGENT (new).
- Caveat added to docstring per Panel 0001-build-skeleton merge.md §4.5: PASS is necessary but not sufficient; regex evidence + hash check is smoke testing, not proof of invariant preservation. This addresses action item #4 from `panels/0001-build-skeleton/merge.md` §8.
- Approver: founder.

### `kernel/manifest.yaml` — bumped to v0.2.0

- Trigger: new spec (FORK_PROTOCOL) and new tools (fork-init, fork-pull) added to the kernel; manifest-drift coherence requires manifest to enumerate them.
- Rationale: `specs:` block gained FORK_PROTOCOL entry with `implements: [I-1, I-4, I-7]`, `depends_on_kernel: [00-meta, 03-constellation, 04-living]`, build-phase carve-out note. `tools:` block gained fork-init and fork-pull entries, both `enforces_via: [FORK_PROTOCOL]`. The conformance tool's recorded version bumped to 0.2.0 (added `--fork` mode). The LLM_PANEL_PROTOCOL entry's `notes:` field updated to reference the v0.2.0 amendment flag from Panel 0001.
- Why MINOR bump on manifest_version: structural additions (new specs and tools entries) without breaking changes to existing entries. Per `00-meta.md` §3.
- Approver: founder.

### `kernel/glossary.md` — amended to v0.4.0

- Trigger: FORK_PROTOCOL spec introduces three terms used elsewhere in the kernel surface: Vendored Fork, Fork Manifest, Pre-conformance Fork. Per glossary's append-only discipline, all referenced terms must be defined here.
- Rationale: three new entries inserted alphabetically. Conformant Fork and Divergent Fork already present from glossary v0.1.0; FORK_PROTOCOL operationalizes them but does not redefine them.
- Approver: founder.

---

## 2026-05-04 — Panel 0001-build-skeleton Concluded (First Empirical Panel Session)

### `panels/0001-build-skeleton/` — created (4 files: proposal, two verdicts, merge)

- Trigger: `specs/LLM_PANEL_PROTOCOL.md` §8.3 requires the spec be exercised on a real corpus before being treated as load-bearing. The build-skeleton batch (entries 2–4 below in this CHANGELOG) was the first body of work substantial enough to test the panel mechanism. Retrospective scope chosen explicitly so the session could not block already-shipped work — only detect what the conformance harness missed.
- Mechanism: two LLM CLIs as panelists (Claude Code, Codex CLI v0.125.0). Blind evaluation enforced by file separation: each panelist wrote a verdict file without reading the other's. Codex invoked via `codex exec --sandbox read-only --skip-git-repo-check`, ~90.5k tokens, ~4 minutes wall.
- Outcome: `RECORDED — REQUIRES AMENDMENT`. Verdicts diverged on Decision (Claude approve_with_concerns / Codex reject) and on `I-2` (Claude affirmed / Codex violated). Per the tie-breaking rule proposed in `merge.md` §6, the more conservative verdict controlled because it was grounded in a named invariant violation (`I-2`) and a named procedural contradiction (`00-meta.md §4` ≥3 vs spec's N=2 for Protected tier).
- Findings the conformance harness did not catch: (i) `LLM_PANEL_PROTOCOL.md` claims same-operator multi-LLM panels satisfy `I-2` while `00-meta.md §7` reads "no single LLM or single operator" — definition laundering; (ii) spec sets Protected = N=2 in direct contradiction to `00-meta.md §4` requiring ≥3 for protected amendments; (iii) `manifest.yaml` does not list itself in its own `parts:` block, so drift in the manifest file cannot be detected by the drift check; (iv) all batch entries record `Approver: founder` but `00-meta.md §4` propose→panel→settle→apply was not followed for any of them — the panel session itself is the first time the procedure has run.
- What this CHANGELOG entry deliberately does NOT do: it does not retroactively edit prior entries to recharacterize their approver lines. `I-7` forbids that. The carve-out (`00-meta.md §4.6` to be drafted in follow-up) names the build-phase reality going forward; the historical record remains as written.
- Self-validation note: Claude (this orchestrator and co-author of the batch under review) failed to escalate `I-2` to a violation despite naming the single-operator concern parenthetically. Codex (independent panelist) caught it as a clean violation. This is exactly the bias the panel was designed to detect — recorded here as evidence that the mechanism produced signal beyond what the author could produce alone.
- Action items carried forward (full list in `panels/0001-build-skeleton/merge.md §8`): (1) `LLM_PANEL_PROTOCOL.md` v0.2.0 amendment session; (2) `00-meta.md §4.6` build-phase carve-out; (3) `manifest.yaml` self-entry + `panels:` block; (4) `tools/conformance.py` docstring caveat (PASS necessary not sufficient); (5) `STATUS.md` update for manifest-threshold-gap and measurement-deferral.
- Approver: founder. Panel composition recorded: Claude Code (CLI) + Codex CLI v0.125.0. Per the `merge.md §6` tie-breaking rule (itself a v0.2.0 amendment proposed in this session), Codex's reject controlled.

---

## 2026-05-04 — `kernel/STATUS.md` Created + Header Standardization + Drift Check

### `tools/conformance.py` — extended (manifest drift check added)

- Trigger: manifest.yaml exists but conformance.py only checked the 7 invariants. A part header could drift from manifest version field with no detection. Build-phase per-commit cadence requires this caught at commit time, not at next manual check.
- Rationale: added `check_manifest_drift()` function. Loads `kernel/manifest.yaml`, iterates `parts:`, opens each part file, extracts `**Part version:**` via regex, compares to manifest entry. Mismatches reported as `[DRIFT]` with both versions named. Wired into `--all` invocation only; single-target invocations unaffected. Existing invariant logic untouched (purely additive). Falls back to a 30-line hand-parser when PyYAML unavailable.
- Initial run after wiring: detected 3 real drift cases (CHANGELOG, README, OUTLINE used non-standard header field names) — fix in next entry.
- Approver: founder.

### `kernel/CHANGELOG.md`, `kernel/README.md`, `kernel/OUTLINE.md` — header standardization

- Trigger: drift check exposed that these three parts used `**Document version:**`, `**Kernel doc release:**`, and an unversioned title respectively, while every other part uses `**Part version:**`. Heterogeneity here was historical drafting noise, not intentional schema variance.
- Rationale: standardized all three to `**Part version:** 0.1.0 · **Tier:** ... · **Status:** ... · **Last touched:** 2026-05-04`. No semantic change to any part — only header field renaming. Drift check now PASS for all 15 parts.
- Why this is not a version bump: the part contents are unchanged. A header field rename is a meta-change to the conformance harness's interface, not a substantive amendment. By analogy: renaming a `description:` field to `desc:` in YAML schema does not change the document's claims.
- Approver: founder.

### `kernel/STATUS.md` — created at v0.1.0

- Trigger: discussion identified that mission, success test, current operational state, and active risks were stated across `01-why.md`, `03-constellation.md`, `05-evidence.md`, and `08-shadow.md` — but no single page answered "where are we against where we said we'd go." Companion's `bible/active-config.md` is the structural analogue at the personal-OS level; the kernel needed its own.
- Rationale: 105-line single-page status board. Sections: Mission (distilled from `01-why §1`), Success Test (4 conditions from `01-why §4`, all `[ ]` not met), Decentralization Path (5 criteria from `03-constellation §5`, 0/5), Operational Snapshot (phase, version surface, 4 active instances, last conformance run, open specs), Active Risks (top 3 from `08-shadow` with watch signals verbatim and current observable state), Falsification Watch (currently-active falsifiers from `01-why §6`), Re-affirmation, Update procedure.
- Honesty discipline: every status indicator currently shows `[ ]` (not met) or "not yet measurable." The status board names this explicitly — pre-success state is the current state, and the board is the public confession.
- Manifest update: STATUS added to `parts:` with depends_on [`01-why`, `03-constellation`, `05-evidence`, `08-shadow`, `manifest`]. Drift check now sees 15/15 parts agreeing.
- Approver: founder.

---

## 2026-05-04 — `kernel/manifest.yaml` Created (Structural Skeleton)

### `kernel/manifest.yaml` — created at v0.1.0

- Trigger: discussion on whether kernel should mirror POS's machine-readable graph (YAML `depends:` `enables:` chains). User: "ilerisi için ekleyelim." Decision: minimal manifest now, STATUS.md deferred.
- Rationale: glossary.md holds term DEFINITIONS; CHANGELOG.md holds per-part history; cross-references in markdown carry semantic meaning. What was missing: machine-readable structural graph. The manifest stores the part list, invariant assertion/enforcement map, and load-bearing term dependency graph. One source of truth per fact: definitions stay in glossary, history stays in CHANGELOG, structure goes here.
- Scope kept minimal: parts (14), specs (5), tools (2), invariants (7), structurally load-bearing terms (~30 of glossary's ~37). Terms with single-part appearances and no outgoing dependencies were omitted; they live only in glossary.
- Why not in glossary itself: definition-and-graph-in-one would either bloat glossary entries with non-readable graph data or force prose to carry both jobs. Separation keeps glossary readable as a glossary.
- Forward integration noted in file: conformance.py will be extended to drift-check between manifest version fields and part-file headers. Not yet wired in v0.1.0 of conformance.py.
- Approver: founder.

---

## 2026-05-04 — `specs/LLM_PANEL_PROTOCOL.md` Created (Multi-LLM Panel Operationalization)

### `specs/LLM_PANEL_PROTOCOL.md` — created at v0.1.0

- Trigger: `00-meta.md` §4.3 acknowledges LLM-only Magistrate panels as legitimate at small N but specifies no operational mechanism. `06-mind.md` §4.4 requires multi-LLM heterogeneity with orchestrator/reviewer separation by `I-2`. Build phase needs a runnable specification, not just an in-principle gesture. User: "codex cli da ayni claude code gibi destek olarak kullanilabilir. o multi llm kisminda... bir md dosyasi yaratalim."
- Rationale: tier-based panel sizing (Mutable=1 LLM, Protected=2 LLM, Immutable=3+ LLM); blind evaluation discipline via file separation (`proposal.md` / `verdict-claude.md` / `verdict-codex.md` / `merge.md`); B→C→A trigger progression (Manual → Skill-mediated → pre-commit hook auto-trigger) with each level's pre-conditions stated; explicit heterogeneity vs Sybil resistance distinction (this spec satisfies `I-2` for build phase; it does NOT satisfy Decentralization Path criterion 2 — that requires governance-stake separation, not just inference separation); POS-specific tier mapping in §8 for the Companion as first instance; first panel session named as empirical validation requirement (§8.3).
- Why this is a spec, not a kernel part: the kernel asserts heterogeneous evaluation (`I-2`) and names the panel pattern (`02-anatomy.md`, `06-mind.md`); the spec implements it for a specific LLM-only build-phase regime. Other implementations (multi-operator panels, hybrid LLM+human, fully decentralized) remain valid and can sit alongside this spec.
- Open questions logged in spec §9: Codex CLI headless mode availability (gates Level C trigger), per-panel cost ceiling, schema enforcement (lint vs trust), tie-breaking when N=2 disagree, Approved Model Registry update procedure (referenced from `04-living.md` §3.2 but not yet drafted at spec level), evidence trail granularity vs storage cost.
- Approver: founder.

### `kernel/glossary.md` — amended to v0.3.0

- Trigger: spec introduces three terms used nowhere else in the kernel: "LLM Panel Protocol", "Blind Evaluation", "Panel Tier Sizing".
- Rationale: glossary must include any term that appears in protocol- or spec-level documents and is not self-defining. MINOR bump: terms added, none removed or redefined.
- Approver: founder.

---

## 2026-05-04 — Repo Restructure: B+C Adoption (kernel + specs siblings, conformance harness)

### Structural decision: B+C path (federation + conformance)

- Trigger: discussion of how kernel, specs, and instances stay aligned without drift. User specified: "B-C gidelim" — federation (kernel public, instances private with `forked-from`) plus conformance harness as code (not just documentation).
- Rationale: B alone is theater (`08-shadow.md` §6 risk). C alone without B confuses Satoshi Mode v1.1 (framework public, instance private). Together: kernel + specs are public siblings; conformance is mechanical, not aspirational.
- Approver: founder.

### `kernel/references/` → `specs/` (top-level sibling)

- Trigger: semantic clarity. Specs are not "references inside the kernel" — they are concrete implementation specifications, peers to the abstract kernel.
- Rationale: kernel/ holds abstract protocol; specs/ holds implementation; they evolve on independent cadences but are conformance-checked together. New layout: `levi/kernel/`, `levi/specs/`, `levi/tools/`.
- Path migration: NODE_SPEC.md, ARCHITECTURE.md, CONTRACT_SPEC.md, README.md moved from `kernel/references/` to `specs/`.
- Citation updates: all kernel parts citing `references/X.md` updated to `../specs/X.md` (02-anatomy, 03-constellation, 05-evidence, 06-mind, 07-economy). Historical CHANGELOG entries citing `references/` left as-is (append-only history).
- Approver: founder.

### `tools/conformance.py` — created

- Trigger: kernel must be testable, not just describable. `08-shadow.md` §6 (constitution as theater) names this risk; the harness operationalizes the defense.
- Rationale: minimal scope — checks the 7 immutable invariants (`I-1` through `I-7`) via regex evidence/violation patterns. Tier-aware: kernel/ must affirm AND not violate every invariant; specs/ must not violate any and must affirm `I-1`/`I-2`/`I-3` (specs implement, kernel asserts). Negation-aware to avoid false positives on description-of-prohibition.
- Initial run: kernel/ PASS (7/7), specs/ PASS (4 affirmed + 3 N/A, 0 violations).
- Approver: founder.

### `tools/pre-commit.sh` — created

- Trigger: build-phase cadence requires per-commit enforcement, not periodic review.
- Rationale: shell hook that runs `conformance.py --all` whenever kernel/ or specs/ files are staged. Skips when no relevant files staged. Install via symlink to `.git/hooks/pre-commit`.
- Approver: founder.

### `04-living.md` — amended to v0.2.0

- Trigger: original §6 (Decay Mechanism) specified 90-day cadence as the only cadence. User noted: "90 gun falan cok uzun biz su an zamanlari dakikalara indirecegiz. builddeyiz cunku."
- Rationale: §6 split into §6.1 (Build phase — per-commit conformance), §6.2 (Steady state — 90-day decay, the original mechanism), §6.3 (Why two cadences — calibration for current operational mode), §6.4 (Why decay at all — preserved from original §6). Transition trigger from build to steady state is operational: all 5 Decentralization Path criteria met. Until then, per-commit cadence applies to kernel/ and specs/; instance-level elements continue under steady-state cadence.
- Why v0.2.0 not v0.1.1: a new operational mode is introduced (build phase as a first-class concept, not just an aside), and the cadence specification is fundamentally restructured. MINOR bump per `00-meta.md` §3.
- Approver: founder.

### `specs/README.md` — substantive update (Cadence: Build Phase vs Steady State section added)

- Trigger: spec-side documentation must reflect kernel's two-cadence model.
- Rationale: explicit "Build phase / Steady state" section pointing back to `kernel/04-living.md` §6.1; conformance check command added at the bottom.
- Approver: founder.

### `kernel/README.md` — minor amendment

- Trigger: structural change requires updating the "How to Read" topology and citations paragraph.
- Rationale: `references/` → `../specs/` in pointers; sibling-structure rationale added to citations paragraph.
- Approver: founder.

---

## 2026-05-04 — References Completed: ARCHITECTURE.md + CONTRACT_SPEC.md Imported

### `references/ARCHITECTURE.md` and `references/CONTRACT_SPEC.md` — added as snapshots

- Trigger: NODE_SPEC.md cross-references both files; previous `references/README.md` flagged them as "aspirational pointers to future companion specs," but they existed in `The_Eternal_Companion/` as pre-kernel artifacts. The flag was inaccurate.
- Rationale: importing the snapshots makes NODE_SPEC.md's cross-references resolve locally; the kernel reference set is now self-contained.
- Source: `The_Eternal_Companion/ARCHITECTURE 2.md` (1176 lines), `The_Eternal_Companion/CONTRACT_SPEC.md` (2123 lines).
- Approver: founder.

### `references/README.md` — substantive update (Pre-Kernel Status section added)

- Trigger: with all three implementation specs now imported, the relationship between kernel and references needs explicit framing.
- Rationale: documents the causal-direction reversal — these specs predate the kernel and influenced it; going forward the kernel is authoritative and the references are revised to conform. Drift detection policy specified: source updating *toward* the kernel triggers re-snapshot; source drifting *away* triggers review-cadence flag, not silent re-import.
- Removed: the previous "Broken Internal Links" section (the links are no longer broken).
- Approver: founder.

### `README.md` — minor amendment

- Trigger: kernel-level README's reference paragraph cited `NODE_SPEC.md` only; with three references now present, the paragraph needed updating.
- Rationale: name all three references; state the pre-kernel artifact status and the causal-direction reversal in one sentence; pointer to `references/README.md` for full policy.
- Approver: founder.

---

## 2026-05-04 — Initial Release of Kernel Parts (v0.1.0)

The first release. Most parts created in a single drafting session. Listed for completeness; future releases will not bundle.

### `OUTLINE.md` — created

- Date: 2026-05-04
- Version: 0.1.0
- Trigger: structural design decision before content drafting.
- Rationale: lock terminology (Mind, Kernel, Instance, Constellation, Sovereign, Sidecar, Magistrate); establish part-by-part scope; surface open questions for explicit decision before drafting.
- Approver: founder (single-operator phase).

### `00-meta.md` — created at v0.1.0

- Trigger: kernel needs a self-description before any other part can be authoritative.
- Rationale: defines the four-layer structure applied to the kernel itself, the tier system, the amendment procedure, the 90-day review cadence, the 7 immutable invariants (`I-1` through `I-7`).
- Notable provisions: §4.3 acknowledges LLM-only Magistrate panels as legitimate at small N, deprecated as constellation grows. §4.5 establishes the fork-divergence path.
- Approver: founder.

### `02-anatomy.md` — created at v0.1.0

- Trigger: anatomy must be specified before federation (`03`) makes sense.
- Rationale: defines the four-layer constitutional substrate (Term/Principle/Rule/Meta-Rule); establishes the Trinity (Sidecar/Magistrate/Sovereign); states the Sub-Constitution Superset Rule; honest-implementation status table showing all four reference instances are incomplete.
- Approver: founder.

### `04-living.md` — created at v0.1.0

- Trigger: the protocol's "living organism" thesis must be specified before evidence (`05`) can claim it operates.
- Rationale: defines versioning everywhere, the tier system applied (with Approved Model Registry as worked example), the evolution mechanism (5 trigger categories), the decay mechanism (90-day reaffirmation), and the frozen-vs-living constitution argument with GDPR / RFC examples.
- Approver: founder.

### `03-constellation.md` — created at v0.1.0

- Trigger: federation topology must be specified before forking protocol (`§6`) and forking documents (`09-engage`) make sense.
- Rationale: kernel/instance separation, Sovereign Console as visibility primitive, Lesson Ledger v0 schema sketch, Decentralization Path 5 criteria, forking protocol (conformant vs divergent).
- Approver: founder.

### `03-constellation.md` — amended to v0.2.0

- Date: 2026-05-04 (same session as v0.1.0).
- Trigger: design clarification on Sovereign Console operatorship.
- Rationale: §3.5 added — anyone may run a Console; Console is a code pattern, not a deployment; no Console may claim canonical status; cross-Console dissent serves as detection mechanism for instance double-reporting.
- Why amendment vs initial draft: the v0.1.0 draft had Console operatorship implicit; the amendment makes the open-Console requirement explicit, which is structurally important enough to record as its own version bump.
- Approver: founder.

### `01-why.md` — created at v0.1.0

- Trigger: rationale must be statable in its own right, not derivable from architecture alone.
- Rationale: Software 1.0/2.0/3.0 framing (Karpathy 2025); Capture Window argument; critique of Anthropic CAI / OpenAI Model Spec / EU AI Act; POS↔Constitution structural identity claim; Founder Independence Criterion (Bitcoin precedent); five negative claims (what this is NOT); falsification conditions table.
- Approver: founder.

### `05-evidence.md` — created at v0.1.0

- Trigger: kernel claims about empirical operation must be backed by stated evidence with stated limitations, or marked as projected.
- Rationale: methodology with observed/self-reported/projected tags; per-instance evidence for Companion (305+ chunks, 12+ months), Liveprob (NODE_SPEC.md complete, 0 nodes deployed), Security Leviathan (n=1 panel — flagged), Levi Template (0 forks); cross-instance pattern observations; explicit limitations (n=4, single-operator, no control group); falsification thresholds with specific N-counts.
- Notable: §6.3 names founder dependency as the dominant failure mode in plain language.
- Approver: founder.

### `06-mind.md` — created at v0.1.0

- Trigger: reference runtime must be specified to make protocol claims concrete, but must be marked clearly as appendix-tier so federation thesis is preserved.
- Rationale: Architecture (LLM Orchestrator + Dictionary VM + Binary Executor); constitutional approval pipeline for new primitives; "Model Thinks, VM Does" determinism boundary; multi-LLM provider agnostic with orchestrator/reviewer separation required by `I-2`; five open problems explicitly stated.
- Notable framing: header paragraph emphasizes that any compatible runtime preserves protocol conformance.
- Approver: founder.

### `07-economy.md` — created at v0.1.0

- Trigger: token mechanisms shape what governance is operationally possible; must be specified at kernel tier.
- Rationale: three reasons for a token (Sybil resistance, governance vote weight, anti-spam); four constraints on what the token must NOT do (no founder lock-in, no data extraction, no license tightening, no kernel-fee extraction); slashing as constitutional enforcement (honest dissent never penalized); Next-Gen Company Hypothesis (forward-looking, marked non-load-bearing); physical-world stakes table.
- Approver: founder.

### `08-shadow.md` — created at v0.1.0

- Trigger: a protocol that documents only its successes lies; failure modes must be named at kernel tier so they can be detected by review cadence.
- Rationale: 7 named failure modes (Founder Dependency, Founder's Psychological Driver, Capture by Complexity, Tier Abuse, Constitution as Theater, Cult Risk, Shadow-of-Shadows: Performative Shadow Naming); each with Watch Signal as testable threshold; each paired with the kernel provision pushing against it.
- Notable: §3 references the founder's POS Shadow `🜏 Üstünlük Yanılsaması` (Superiority Illusion) by name; §8 makes the part self-referential by naming "performative shadow naming" as its own shadow.
- Approver: founder.

### `09-engage.md` — created at v0.1.0

- Trigger: a forkable kernel must include explicit reading paths for each audience; without them, the protocol filters by social access rather than by published guidance.
- Rationale: four audience paths (operators, users, researchers, critics); explicit list of conceded vs contested critiques; fork-divergence path framed as the most honest critique; reading-cold guidance for the as-yet-unaffiliated reader.
- Approver: founder.

### `glossary.md` — created at v0.1.0

- Trigger: the kernel cannot be read out-of-order without a Terms layer of its own.
- Rationale: every capitalized or specifically-meaning term in the kernel is defined here with introduction-point and version. Mirrors the Term layer of the constitutional substrate the kernel describes (`02-anatomy.md` §2.1).
- Notable: terms originating in Turkish-language POS work (Mimar, Caba Yasası reference, Satoshi Mode) are preserved with English gloss.
- Approver: founder.

### `references/NODE_SPEC.md` — added as snapshot

- Trigger: kernel part `02-anatomy.md` §6.2 and `07-economy.md` §3 reference NODE_SPEC.md non-trivially.
- Rationale: snapshot copied from `/Users/aigent/caba_yasasi/NODE_SPEC.md` rather than symlinked, so kernel fork is self-contained. Update policy stated in `references/README.md`.
- Approver: founder.

### `references/README.md` — created

- Trigger: contributors need to know whether referenced files are live or snapshotted.
- Rationale: states that NODE_SPEC.md is a snapshot at a specific date; flags broken-link warning for CONTRACT_SPEC.md and ARCHITECTURE.md (cited in NODE_SPEC.md but not present in the source repo at snapshot time — aspirational links).
- Approver: founder.

---

## Format for Future Entries

Each future modification should follow this template:

```
### `<path/to/part>.md` — <created | amended to vX.Y.Z>

- Date: YYYY-MM-DD
- Trigger: <what caused this change — breakthrough, breakage, external, periodic review, escalation; per `04-living.md` §4>
- Rationale: <one paragraph on what changed and why>
- Approver: <founder | Magistrate panel | listed approvers>
```

For protected-tier amendments, the approver line must list the panel composition that reviewed the change. For immutable-constant additions or removals, the approver line must show the supermajority recorded.

A modification without a CHANGELOG entry is, per `04-living.md` §5, *not a real modification* — it is a drift event that the next maintainer is obligated to either retroactively log or revert.

---

## Out of Scope for This File

- Modifications to instance-level constitutions (those have their own changelogs, e.g., `openpos/my-pos/changelog.yaml`).
- Modifications to the founder's POS (cited in `08-shadow.md` §3 by reference; lives outside the kernel).
- Drafting-process notes ("I considered X but rejected Y") — those belong in `notes/` if anywhere; the CHANGELOG records what changed, not what was considered.
- Marketing announcements or release blog posts — not kernel-tier content.

---

*This is the kernel's living memory of itself. If it stops growing, the kernel has stopped evolving — which `08-shadow.md` §6 names as a dominant failure mode.*
