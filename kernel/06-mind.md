# 06-mind — Mind: Reference Runtime

> **Part version:** 0.1.0 · **Tier:** protected (appendix) · **Status:** draft · **Last touched:** 2026-05-04
>
> ⚠ **This part describes a reference implementation, not the protocol.** A Leviathan instance can run on any runtime that satisfies the kernel's interfaces. Mind is the runtime the founder builds; it is not what makes a Leviathan a Leviathan.
>
> **Scope:** the architecture, motivation, and limitations of the Mind runtime. Out of scope: anything in `01–05` (those are kernel; this is implementation).

---

## §1. Status: Reference Implementation, Not Protocol

The kernel deliberately does not require a specific runtime. An instance that satisfies:

- Layer 3 Rule enforcement at action time (Sidecar interface),
- Magistrate panel participation when invited,
- Reasoning artifact production per `00-meta.md` §7 I-1,
- Sub-constitution superset enforcement (`02-anatomy.md` §7),

is a kernel-conformant instance regardless of the runtime that meets these obligations.

Mind is one such runtime. It is the founder's reference implementation and is the runtime the Companion and Liveprob will eventually use. Other runtimes are not only allowed; they are encouraged (`I-4`, fork freedom). A constellation in which all instances run the same runtime would be a monoculture in the implementation layer — analogous to the monoculture `I-2` exists to prevent at the evaluation layer.

This part is **appendix-tier**: substantively important to anyone implementing Mind, irrelevant to anyone implementing a different runtime that meets the kernel interfaces.

---

## §2. Architecture

Mind is a synthesis of two existing patterns plus one constitutional addition:

- **Primitive registry + Binary executor** (Liveprob origin, `00_concept.md`). A versioned dictionary of executable primitives runs in a sandboxed binary executor.
- **Voyager-style skill synthesis** (Wang et al., 2023). When the LLM orchestrator needs a primitive that does not exist, it synthesizes one, tests it, and proposes addition to the registry.
- **Constitutional approval pipeline** (this kernel, `00-meta.md` + `02-anatomy.md`). New primitives do not enter the registry until a Magistrate panel approves them against the active tier rules.

```
                                  ┌─────────────────────┐
   USER / OPERATOR / AGENT  ───▶  │   LLM ORCHESTRATOR  │
                                  │  (planner, slow,     │
                                  │   non-deterministic) │
                                  └──────────┬──────────┘
                                             │ composes plan from primitives
                                             ▼
                                  ┌─────────────────────┐
                                  │   DICTIONARY VM      │
                                  │  - Lookup primitives │
                                  │  - Versioned         │
                                  │  - Tier-classified   │
                                  └──────────┬──────────┘
                                  primitive  │  missing primitive
                                  exists     │  ┌────────────────────────┐
                                  │          ▼  │   SYNTHESIS LOOP        │
                                  ▼          ┌──┤   - LLM proposes        │
                          ┌──────────────┐  │  │   - Local test           │
                          │   BINARY     │  │  │   - Magistrate review    │
                          │   EXECUTOR   │  │  └─────┬──────────────────┘
                          │  - Sandboxed │  │        │ APPROVE
                          │  - Determin. │  │        ▼
                          │  - Fast      │  └──▶ ADD TO DICTIONARY
                          └──────────────┘
                                  │
                                  ▼
                          OBSERVABLE ACTION
                          (return to orchestrator)
```

### §2.1. The LLM Orchestrator

The orchestrator does not execute. It plans. Given a goal, it composes a plan as a sequence of primitive calls drawn from the dictionary. If the plan requires a primitive that does not exist, the orchestrator enters the synthesis loop (§6).

The orchestrator is non-deterministic, slow, and capable of error. It is the **mind** in the runtime's name — the deliberative component.

### §2.2. The Dictionary VM

The dictionary is a tiered, versioned registry of named primitives. Every primitive has:

- A name and a stable identifier.
- A version (`MAJOR.MINOR.PATCH` per `04-living.md` §5.4).
- A tier (`immutable` / `protected` / `mutable`, per `04-living.md` §3).
- A typed signature (input types, output type, side effects declared).
- A sandboxed binary implementation.
- A reasoning artifact from the Magistrate panel that approved its addition.

Lookup by name returns the version compatible with the calling context's constitution. If no compatible version exists, lookup fails and the orchestrator must either replan or trigger synthesis.

### §2.3. The Binary Executor

The executor runs primitive implementations. It is deterministic, fast, and has no LLM call in the hot path. Its job is to run sandboxed binaries with declared resource limits (time, memory, syscalls) and return the typed output to the orchestrator.

The executor refuses to run a primitive whose signature does not match the call site, whose tier does not satisfy the active constitution, or whose binary hash does not match the registry's stored hash.

---

## §3. Constitutional Approval Pipeline

A primitive synthesized by the orchestrator does not enter the dictionary directly. The pipeline:

```
SYNTHESIZE  →  LOCAL TEST  →  MAGISTRATE PANEL  →  ADD TO DICTIONARY
                                                  (or REJECT)
```

### §3.1. Synthesize

The orchestrator generates a primitive proposal: name, signature, implementation, declared tier, justification (why this primitive is needed, why it cannot be expressed as a composition of existing ones).

### §3.2. Local Test

The proposal runs against a battery of synthetic inputs to verify type-signature conformance and basic correctness. Failures here loop back to the orchestrator without invoking a panel.

### §3.3. Magistrate Panel

Per `02-anatomy.md` §6.2 and `../specs/NODE_SPEC.md`. Panel evaluates:

- Does the primitive's signature match its declared tier? (e.g., a primitive with side effects on protected resources cannot be `mutable` tier.)
- Does the implementation respect sandbox limits?
- Does adding this primitive expand the dictionary's capability in a way that introduces unmonitored failure modes?
- Are there existing primitives whose composition expresses the proposed primitive? (Bloat prevention.)

Round 1 unanimity → addition. Any dissent → Round 2 with fresh panel.

### §3.4. Why This Pipeline Exists

A self-extending system that cannot self-govern its extensions becomes capability-unbounded over time. Voyager's original skill library has no constitutional gate; a Voyager that runs long enough accumulates skills its operator did not anticipate and may not want. The constitutional approval pipeline is the boundary that converts "self-extending" into "bounded self-extension."

The cost is real (panel review per primitive proposal adds latency). The protection is real (no primitive is in the dictionary that no panel ever read).

---

## §4. "Model Thinks, VM Does" — The Determinism Boundary

Mind separates the non-deterministic component (the LLM orchestrator) from the deterministic component (the executor running primitive binaries). This separation is intentional:

- **Reproducibility.** Given the same plan, the executor produces the same output across runs. Debugging, audit, and Magistrate review all depend on this.
- **Sandboxability.** A binary executor with declared resource limits can be locked down in ways an LLM call cannot.
- **Performance.** Hot-path execution does not pay LLM latency. Only planning does.
- **Cost.** Most operations are primitive-call sequences, not new reasoning. Only novel goals invoke the orchestrator's full deliberation.

This is the "model thinks, VM does" formulation. Operationally:

```
Action latency budget for a Mind primitive = executor latency
Action latency budget for orchestrator deliberation = planning latency
Total latency = planning + sum(executor calls)
```

Against a single-LLM-call architecture (where every action is "ask the model"), Mind concentrates the LLM cost at planning time and amortizes it across many executions of the resulting plan.

---

## §5. Multi-LLM Provider Agnostic

The orchestrator slot is not bound to any specific LLM provider. Mind can swap the orchestrating model without changing the dictionary, the executor, or the constitutional pipeline. This is required by `I-2` (heterogeneous evaluation): an instance whose primitive synthesis is gated by a single-model orchestrator is exposed to the same monoculture failure as a single-model Magistrate panel.

In the synthesis pipeline (§3), the **proposer** of a primitive (the orchestrator) and the **reviewers** (the Magistrate panel) should not be the same model. A primitive synthesized by Claude reviewed by a panel of {Claude, Claude, Claude} is structurally a Claude consensus — not a heterogeneous review.

The recommended baseline configuration:

- Orchestrator: any single approved model (NODE_SPEC.md §3 registry).
- Magistrate panel for primitive review: ≥3 models, none equal to the orchestrator's model.

This is operationally achievable today via the Approved Model Registry. As more models are added, the diversity space grows.

---

## §6. Self-Extension and Skill Synthesis

The synthesis loop (already shown in §3) is the mechanism by which Mind's capability grows over time. Three observations on its dynamics:

### §6.1. Tier defaults to mutable

Synthesized primitives enter at `mutable` tier by default. Promotion to `protected` requires sustained use without observed failure plus a Magistrate panel decision. This mirrors `04-living.md` §3 — operational primitives become protected; experimental ones stay mutable until proven.

### §6.2. Synthesis does not bypass constitutional limits

If an orchestrator's plan would violate the active constitution, the constraint is felt at the **Sidecar** (action time), not at the synthesis layer. A primitive may be in the dictionary and still be refused execution by the Sidecar in a context whose sub-constitution forbids it. This is the sub-constitution superset rule (`02-anatomy.md` §7) operating across runtime layers.

### §6.3. Synthesis can be observed by panel

The Magistrate panel reviewing a primitive proposal can request the orchestrator's reasoning trace — what plan triggered the synthesis, what primitives were considered first, why none sufficed. This trace is itself an artifact under `I-1` and must be retained for audit.

---

## §7. Open Problems

These are unresolved and should be flagged in any deployment of Mind. The protocol does not require them to be solved before Mind is used; it requires them to be acknowledged.

### §7.1. Skill Library Poisoning

A primitive that passes panel review but contains subtle latent failure can poison subsequent compositions. Voyager's original architecture has no recovery mechanism for this. Mind's tier system + Magistrate review reduces but does not eliminate the risk. Mitigation candidates: periodic re-review of `protected` tier primitives, automatic deprecation of primitives that produce verdict-revisable outcomes, primitive-level reputation tracking.

### §7.2. Primitive Bloat

Each accepted primitive adds dictionary lookup cost, increases panel review burden, and competes with composability. Without an active deprecation procedure, the dictionary grows monotonically. Mitigation candidates: usage telemetry (primitives unused for 90 days are flagged for deprecation review), composability-first review (a primitive that could be expressed as composition of existing primitives is rejected unless it provides distinct guarantees).

### §7.3. Dictionary Versioning Across Constellation

Two instances running Mind do not necessarily run the same dictionary. A primitive `tx-execute` v1.3 in instance A may not be `tx-execute` v1.3 in instance B if independent Magistrate panels approved different versions. The Lesson Ledger (`03-constellation.md` §4) is the candidate mechanism for cross-instance primitive coordination, but the schema and procedure for primitive-level Lessons are not yet specified.

### §7.4. Synthesized Primitive Provenance

A primitive synthesized by orchestrator-LLM-X reviewed by panel-of-{Y,Z,W} carries provenance metadata (who synthesized, who reviewed). Whether this provenance is visible to downstream callers, and whether it should affect tier or trust, is unresolved.

### §7.5. Determinism Boundary Erosion

If the orchestrator can call non-deterministic primitives (e.g., a primitive that itself invokes an LLM), the determinism boundary is leaky. Whether such primitives should be tier-restricted to `protected` or `immutable`, refused entry to the dictionary entirely, or marked with a non-determinism flag visible to the Sidecar — unresolved.

---

## §8. Out of Scope for This Part

- Why heterogeneous evaluation is required (`01-why.md` §2, `02-anatomy.md` §6.2).
- The structural anatomy Mind implements (`02-anatomy.md`).
- The constellation-level coordination Mind participates in (`03-constellation.md`).
- The economic mechanism funding Magistrate panel operation when reviewing primitives (`07-economy.md`).

---

## Citations

- Liveprob `00_concept.md` — primitive registry, tier system, binary executor pattern (Mind's executor side).
- Wang, G. et al. (2023). *Voyager: An Open-Ended Embodied Agent with Large Language Models*. Self-extending skill library (Mind's synthesis side).
- NODE_SPEC.md (`../specs/NODE_SPEC.md`) — Magistrate Node spec referenced for primitive review panel composition.
- `02-anatomy.md` §6 (Sidecar / Magistrate / Sovereign).
- `04-living.md` §3 (tier system applied to instance content; primitives are instance content).

---

*Part 06 of 09. Previous in outline order: `05-evidence.md`. Next: `07-economy.md`.*
