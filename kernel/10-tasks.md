# 10-tasks — The Task Layer: Constitutional Elements at Runtime

> **Part version:** 0.1.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-05
> **Scope:** the structural identity between tasks (transient work units) and constitutional content (persistent governance units). Out of scope: task-scheduler implementations (those live in instance repos), specific task schemas per domain.

---

## §1. Central Claim

A **task** is a constitutional element with a transient lifecycle.

This is not metaphor. The schema for a Personal Operating System action item (`openpos/my-pos/eylemler/*.yaml`), a Liveprob task envelope (`task_inbox` entry, `DecisionEntry` output), and a Security Leviathan workflow (Action Profile + GateState + canonical runner invocation) is structurally identical. The same fields, the same lifecycle states, the same dependency graph, the same evidence requirement, the same outcome → lesson loop.

The structural identity holds because tasks and constitutional rules are two phases of the same object:

- A **rule** specifies how a class of decisions ought to be made. It is timeless.
- A **task** is one specific invocation of that rule against a specific situation. It is timed.
- An **outcome** is the recorded resolution of the task with proof of effect. It is permanent evidence.
- A **lesson** is the inference drawn from N outcomes that proposes a rule change. It is the loop closing.

Tasks are not separate from the constitution. They are the constitution's runtime expression.

---

## §2. Universal Task Schema

Every kernel-conformant instance MUST express tasks using this minimum schema:

```yaml
id: <stable-task-id>           # e.g. eylem:public-content-launch, task:jump_decision_2026_05_05_001
type: <task | eylem | workflow | operation>  # instance-local synonym; meaning is identical
current_version: <semver>      # task spec evolves; instances of the spec inherit version

status:                        # lifecycle state — see §3
  state: <proposed | claimed | in_progress | settled | expired | rejected>
  reason: <optional, required if expired/rejected>

versions:                      # task spec history; not invocation history
  - version: <semver>
    period: <YYYY-MM>
    definition: <what this task does, scope, success criteria>
    trigger: <what causes this task to be claimable>

dependencies:
  depends_on: [<other-task-ids>]    # must complete before this can claim
  enables: [<other-task-ids>]       # this completion unblocks these
  shadow: [<failure-mode-ids>]      # known failure modes this task can trigger

capability:                    # see §4
  class: <observation_only | advisory_proposal | bounded_validation |
          executable_normalized | sensitive_active | annex_special_mode |
          policy_write | authority_effect>
  reversibility: <reversible | partial | irreversible>
  blast_radius: <self | instance | constellation | external>
  effect_proof_required: <bool>

evidence:                      # see §6
  cited_decisions: [<decision-ids>]
  cited_observations: [<observation-hashes>]
  cited_patterns: [<pattern-ids>]
  rationale: <prose, mandatory if state=settled>

outcome:                       # written when state transitions to settled
  result: <success | failure | partial | inconclusive>
  effect_observed: <bool>            # required if capability.class >= executable_normalized
  effect_proof: <hash | null>        # required if effect_proof_required=true
  settled_at: <ISO timestamp>
  settled_by: <actor-id>
  notes: <prose>
```

Instances may extend this schema with domain-specific fields. They MAY NOT remove or weaken any field above. Removing the `evidence` block is a divergent-fork act.

---

## §3. Task Lifecycle

A task moves through a finite state machine. Transitions are constrained; no transition is silent.

```
                   ┌──────────────┐
                   │   proposed   │  ← created, awaiting eligibility check
                   └──────┬───────┘
                          │ depends_on satisfied + actor authorized
                          ▼
                   ┌──────────────┐
                   │   claimed    │  ← actor committed; clock starts
                   └──────┬───────┘
                          │ work begins
                          ▼
                   ┌──────────────┐
                   │ in_progress  │  ← active work; intermediate outputs allowed
                   └──┬───────────┘
                      │
            ┌─────────┼─────────┐
            ▼         ▼         ▼
     ┌──────────┐ ┌──────────┐ ┌──────────┐
     │ settled  │ │ expired  │ │ rejected │
     └──────────┘ └──────────┘ └──────────┘
        ↑              ↑             ↑
        │              │             │
   outcome written  TTL exceeded  blocked by
   evidence cited   no settlement  governance/
                                   shadow trigger
```

Rules:

- `claimed → in_progress` MUST emit an audit event with actor identity.
- `in_progress → settled` MUST include an `outcome` block. Settlement without outcome is invalid.
- `expired` requires explicit reason; tasks do not silently lapse.
- `rejected` requires citation of the rule or shadow that forbade settlement.
- A settled task is append-only. Re-running the same logical work creates a new task with a new `id`, citing the prior task in `evidence.cited_decisions`.

This lifecycle applies whether the actor is a human operator, an LLM agent, a deterministic runner, or a multi-actor panel. The discipline does not vary by actor.

---

## §4. Capability Class Taxonomy

Borrowed from Security Leviathan's eight-class action taxonomy (`LEVIATHAN_CAPABILITY_CLASS_TEMPLATES`). Universal because every governance question reduces to "what can this action do, and how reversible is it?"

| Class | What It Does | Reversibility | Example |
|-------|--------------|---------------|---------|
| `observation_only` | Reads, classifies, records. No state change. | n/a | Wallet snapshot, metric calculation, log analysis. |
| `advisory_proposal` | Suggests an action; does not execute. | trivially reversible | Draft amendment proposal, jump_decision verdict. |
| `bounded_validation` | Checks a condition; may block downstream action. | reversible if not yet enforced | Sidecar pre-flight check, evidence sufficiency probe. |
| `executable_normalized` | Performs an action via the canonical runner. | depends on operation | Pattern promotion to L3, wallet status update. |
| `sensitive_active` | Touches state with elevated authority. | partial | Slashing, XP penalty, capability grant. |
| `annex_special_mode` | Operates in a domain-restricted privileged mode. | constrained | Emergency pause, Magistrate panel convene. |
| `policy_write` | Mutates the constitution itself. | reversible only via amendment | Element version bump, tier change proposal. |
| `authority_effect` | Changes external real-world state. | typically irreversible | Trade execution, firewall block, DNS sinkhole. |

**Two implications follow:**

**§4.1. Capability class gates settlement.** A task at `authority_effect` MUST present `effect_proof` before transitioning to `settled`. A task at `observation_only` MAY settle on rationale alone. The settlement rigor scales with the class.

**§4.2. Capability class gates actor authorization.** Sub-constitutions declare which classes their agents may claim. A specialty agent designated for `observation_only + advisory_proposal` cannot claim `policy_write` even if its evidence is impeccable. Class restriction is the granular form of the Sub-Constitution Superset Rule (`02-anatomy.md` §6).

---

## §5. Outcome → Lesson Loop

Settled outcomes feed the constitutional evolution mechanism (`04-living.md` §5).

```
N settled outcomes  →  pattern detection threshold crossed
                    →  lesson candidate emitted
                    →  amendment proposal drafted (uses templates/lesson-template.md)
                    →  Magistrate panel review (per tier of affected element)
                    →  approved / rejected / refined
                    →  if approved: rule version bump + CHANGELOG entry
                    →  next task generation uses new rule version
```

This loop is the structural answer to the question "how does the constitution learn?" Without it, the constitution either freezes (no learning channel) or drifts unaccountably (learning happens but is not recorded). With it, every change to a rule is traceable to the outcomes that triggered the change.

The threshold for emission is itself a rule (a `meta_rule_lesson_extraction_threshold` or equivalent). Instances calibrate this threshold; the kernel only requires that one exist and be defined in the constitution, not in code.

---

## §6. Evidence Requirement

Every task that settles MUST cite evidence in its outcome block. Acceptable evidence types:

- **`cited_decisions`** — IDs of prior settled tasks whose outcomes inform this one
- **`cited_observations`** — Hashes of raw observations (sensor data, snapshots, logs)
- **`cited_patterns`** — IDs of registered patterns (`memory/patterns.yaml` or instance equivalent)
- **`rationale`** — Prose argument tying evidence to outcome

Empty evidence + non-trivial settlement is a falsification trigger. The auditor (Sidecar runtime, validator, or Magistrate panel) MUST emit an `EVIDENCE_MISSING` event when this pattern is detected.

This is not aspirational. It is enforced. Liveprob's `_audit_decision_evidence` (`runner.py` D.1.6, settled 2026-05-04) is the reference implementation: structured fields checked at write time, missing-evidence events emitted to operator review surface. Instances MAY implement this differently, but they MUST implement it.

The reason is `08-shadow.md` §6 — *Constitution as Theater*. A constitution that records decisions without requiring evidence becomes a polite fiction. The evidence requirement is what makes the constitution real.

---

## §7. Implications for Instances

Any kernel-conformant instance MUST:

1. **Declare a task layer.** Whether named `eylemler/`, `task_inbox/`, `workflows/`, or `operations/`, the layer exists and is part of the constitutional substrate, not separate from it.

2. **Use the universal schema (§2) at minimum.** Domain extensions are permitted; field removal is not.

3. **Enforce the lifecycle (§3) without silent transitions.** State changes emit audit events. Expired tasks have explicit reason. Settlement requires outcome.

4. **Classify every task by capability class (§4).** Default-to-most-restrictive when unclear. A task without a declared class is treated as `authority_effect` for safety.

5. **Implement the outcome → lesson loop (§5).** The loop's threshold may be high (lesson emission rare) but the channel must exist. An instance with no path from outcome to constitutional change is a frozen kernel in disguise.

6. **Audit evidence at write time (§6).** Settlement without evidence emits an event. Operators see missing evidence as a first-class signal, not a buried log line.

The kernel does NOT mandate:

- Specific scheduler implementations (cron, queue, manual claim, agent FIFO — all valid)
- Specific persistence (YAML files, SQLite, Postgres, append-only logs — all valid)
- Specific actor types (human, LLM, deterministic — all valid, mixed actors valid)
- Specific UI for operator review (CLI, web, Telegram bot, none — operator's choice)

What the kernel mandates is the **shape of the discipline**, not its expression.

---

## §8. Falsification Conditions

What would refute this part of the kernel?

| Claim | Refuted If |
|-------|-----------|
| Task ↔ constitutional element structural identity | A working instance demonstrably benefits from treating tasks as separate from constitution (e.g., faster iteration, cleaner mental model) — and the benefit persists after fair comparison with a structurally-identical implementation. |
| Universal task schema fits all instances | An instance discovers a domain where the schema's fields cannot be filled meaningfully, and adding the missing field breaks the universality claim. |
| Capability class taxonomy is complete | An action surfaces in any instance that does not fit any of the eight classes, and the residual cannot be modeled as a combination of existing classes. |
| Outcome → lesson loop is universal | An instance operates productively for ≥6 months with zero lessons emitted from a steady stream of outcomes, AND the operator can articulate why no lesson was emittable. |
| Evidence requirement is non-optional | An instance demonstrates that allowing evidence-free settlements (for some class of tasks) produces better outcomes than requiring evidence, measured over ≥3 months with comparable workload. |

These are public commitments. If any falsification fires, the part changes — or the kernel loses honesty.

---

## §9. Cross-References

- **02-anatomy.md §1–§3** — Four-layer substrate that this part extends. Tasks are the runtime expression of all four layers acting together.
- **04-living.md §5** — Evolution mechanism. The outcome → lesson loop in §5 above is the runtime engine of evolution.
- **05-evidence.md §6.3** — Founder dependency failure mode. A task layer with single-actor authorization across all classes is a founder-dependency proof.
- **06-mind.md §3** — Reference runtime. Mind's primitive registry executes tasks; the task schema is what Mind operates on.
- **07-economy.md §3** — Slashing as constitutional enforcement. Slashing is itself a task at `sensitive_active` class; settlement requires panel-tier evidence.
- **08-shadow.md §6** — Constitution as Theater. The evidence requirement (§6 above) is the structural defense against this shadow.

---

## §10. Reference Implementations

Three live implementations of this part, in order of completeness:

1. **Liveprob** (`/Users/aigent/caba_yasasi/levi/liveprob/`) — Most complete schema fidelity. `task_inbox` queue, `DecisionEntry` output with structured evidence fields (D.1.5, D.1.6 settled 2026-05-04), evidence sufficiency rule (D.2 settled 2026-05-05), first complete substance↔governance closed loop. Reference for §3 lifecycle and §6 evidence enforcement.

2. **Companion / POS** (`/Users/aigent/caba_yasasi/The_Eternal_Companion/openpos/my-pos/eylemler/`) — Reference for §2 schema (versioning, dependencies, shadows). Currently lacks formal capability class field; conformance to this part requires adding it. Lifecycle states map onto `status: aktif | pending | strategic | urgent | done`. Outcome → lesson loop expressed as version bumps to constitutional elements (kavram, prensip).

3. **Security Leviathan** (`nwr` repository) — Reference for §4 capability class taxonomy. The eight-class action taxonomy originated here. Most rigorous on `effect_proof_required` (read-after-write + independent observation + reconciliation). Currently the least kernel-anchored of the three; this part is the structural bridge.

The three implementations together demonstrate that the schema generalizes across personal identity, financial decisions, and security operations. The bet of this part is that the same shape will hold for any future domain.

---

*End 10-tasks.md*
