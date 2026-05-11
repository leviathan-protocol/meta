# 09-engage — How to Engage

> **Part version:** 0.1.0 · **Tier:** protected · **Status:** draft · **Last touched:** 2026-05-04
> **Scope:** practical entry points for the four audiences who will read this kernel — operators, users, researchers, critics. Out of scope: marketing, recruitment, vision statements (the kernel makes none).

---

## §1. Read in This Order

The parts of this kernel were ordered for first-pass comprehension, but each audience benefits from a different reading path. Below are the recommended paths. None of them require reading every part. None of them are exhaustive.

If you read only one part to decide whether this kernel is worth more attention, read **`08-shadow.md`** first. The kernel's failure modes are stated more candidly than its claims. A reader convinced by the shadows is a reader who has actually engaged with the protocol.

---

## §2. For Operators

You want to fork the kernel and run an instance.

### §2.1. Minimum read

- `00-meta.md` (how the kernel itself evolves — you will inherit this)
- `02-anatomy.md` (the four-layer structure your instance must conform to)
- `03-constellation.md` §6 (the forking protocol — conformant fork vs divergence fork)
- `08-shadow.md` (failure modes — most apply to your instance too)

### §2.2. Decisions you must make before forking

1. **Conformant or divergent.** Conformant forks preserve all 7 immutable invariants (`00-meta.md` §7) and may use the Leviathan name. Divergent forks must change the name (`03-constellation.md` §6). Decide which you are forking as.
2. **Your domain.** A POS instance differs from a trading-agent instance differs from a hardware-control instance. The four-layer anatomy is identical; the content of each layer is yours to define.
3. **Your Sovereign(s).** Who has override authority? `02-anatomy.md` §6.3 requires a named, addressable Sovereign — anonymity-via-pseudonym is acceptable, but absence is not.
4. **Your Magistrate plan.** A single-node panel is a known gap (`05-evidence.md` §4). At what scale do you intend to add a second node? The plan can be honest about "not yet" — see Decentralization Path criterion 2.

### §2.3. Minimum operational requirements

To claim "Leviathan-conformant" you must:

- Maintain a four-layer YAML constitution with versioned elements.
- Enforce the constitution at action time via a Sidecar (or document why your domain does not require runtime enforcement).
- Produce a reasoning artifact for each decision your Sovereign or Magistrate makes (`I-1`).
- Honor the immutable invariants. If you cannot, you are forking divergently — change the name.
- Publish your kernel version in your instance README (`forked-from: leviathan-kernel@v0.x.0`).

### §2.4. What sovereignty means for you

You are the Sovereign of your instance. The kernel maintainer (currently the founder) has no authority over your instance and cannot retract your fork rights (`I-4`). You may amend your local kernel — even the parts marked immutable, *if you are willing to fork divergently*. The only consequence the kernel imposes is the name.

You owe nothing to the constellation by default. Joining the Lesson Ledger or the Sovereign Console is opt-in.

---

## §3. For Users of an Instance

You are not running an instance — you are using one someone else operates. You want to know whether the operator's claims about constraints are real.

### §3.1. Minimum read

- `02-anatomy.md` §1–§5 (so you know what to look for)
- `03-constellation.md` §3 (the Sovereign Console — what it can and cannot show)
- `08-shadow.md` §6 (constitution as theater — the failure mode that affects you most)

### §3.2. Verification you can perform

The kernel obligates conforming instances to surface evidence to users. You can ask the operator for:

1. **The constitution.** A conformant instance's kernel-tier rules are public. If the operator refuses, the instance is not conformant on `I-1` (reasoning trail required).
2. **A reasoning sample.** For any past action you have access to, the operator must be able to produce the Sidecar/Magistrate verdict and reasoning artifact. If they cannot, either the artifact was not produced (violates `I-1`) or it is being withheld (violates conformance).
3. **The Magistrate panel composition.** For decisions that went to panel review, you may ask which models reviewed the decision. Heterogeneous panels are required (`I-2`); a panel of identical models is not Magistrate-pattern.
4. **The fork freedom statement.** A conformant instance must publicly affirm fork freedom (`I-4`). If the operator's terms of service contradict this, the instance is non-conformant.

### §3.3. What sovereignty does NOT mean for you

The Sovereign of an instance is the operator, not you. The operator's override applies to the agent's behavior; it does not extend to your data or your choices. Confusion on this point is the most common misreading of the protocol — the "sovereign" naming is operational (who can override the Sidecar), not personal (who controls the user).

If an operator claims authority over your data because they are "the Sovereign," they are misreading the kernel. `I-6` applies to instance data; user data within an instance is governed by the instance's own terms, which you should read separately.

### §3.4. Cross-Console verification

If multiple Sovereign Consoles exist (`03-constellation.md` §3.5), the same instance's public claims should be visible from any Console. Disagreements between Consoles signal one of: stale Console data, instance double-reporting, or evaluation method divergence. The disagreement is information; the absence of cross-Console comparison is information of a different kind.

---

## §4. For Researchers

You want to study, replicate, or measure claims made by the kernel.

### §4.1. Minimum read

- `01-why.md` §6 (falsification conditions — these are the testable claims)
- `05-evidence.md` (the n=4 evidence base, with limitations stated)
- `08-shadow.md` (the kernel's own assessment of where it is structurally weak)

### §4.2. Replication targets

The protocol's claims are falsifiable (`01-why.md` §6). The most accessible replications:

| Claim | Replication Setup | Cost |
|-------|-------------------|------|
| Four-layer anatomy is sufficient | Build any instance, attempt to express its rules in fewer or more layers without Procrustean fit. Report mismatch. | Weeks, single-operator. |
| POS↔Constitution structural identity | Build a POS for a person and a constitution for an agent in the same domain. Apply the same YAML schema to both. Report whether either required modification. | Weeks, single-operator (this has been done by the founder; independent replication is the value). |
| Heterogeneous panels reduce monoculture failure | Run a benchmark task set through (a) a panel of N copies of the same model and (b) a panel of N different models. Compare verdict variance and caught-failure rate. | Days, requires N model API access. |
| Dissent-protected panels improve outcomes | Compare majority-rule panels vs panels with explicit dissent protection on a benchmark task set. Measure caught failures, not just consensus rate. | Days. |
| Living constitutions outlive frozen ones | Run two parallel instances — one with active amendment, one frozen at v1.0 — over ≥3 years. Compare operational continuity. | Years. The expensive replication; the most informative one. |

### §4.3. Falsification points (replication that *refutes* the kernel)

The kernel earns its claim to falsifiability when researchers report failed replications. We do not promise a hospitable response to such reports — the kernel maintainers have a stake in the protocol — but we promise the kernel will record the result. Falsification reports submitted via the Lesson Ledger (`03-constellation.md` §4) and rejected without an articulable rebuttal are themselves evidence of the failure mode named in `08-shadow.md` §6 (constitution as theater).

### §4.4. What we want and do not want

**Want:** independent forks; benchmarked panel comparisons; long-horizon (>1 year) instance studies; cross-cultural POS instances built by operators outside the founder's cultural context.

**Do not want:** simulated instances built by researchers to "prove" the protocol works without actually running them under load; comparative studies that re-introduce single-evaluator panels because they are operationally easier (this re-introduces the failure mode `I-2` exists to address); citation without engagement (the kernel is not a citation farm).

---

## §5. For Critics

You believe the protocol is misguided, redundant, dangerous, naive, or self-serving.

### §5.1. Minimum read

- `08-shadow.md` (we already know — read this first to avoid arguing points the kernel concedes)
- `01-why.md` §5 (what the protocol is NOT — many critiques target claims the kernel does not make)
- `00-meta.md` §4.5 (fork divergence path — critics who want a different protocol can build one without us)

### §5.2. Critiques the kernel concedes

Several critiques are already named inside the kernel and require no rebuttal. If these are the substance of the critique, the kernel does not contest them:

- **The protocol is founder-dependent.** Acknowledged (`05-evidence.md` §6.3, `08-shadow.md` §2). The Founder Independence Criterion is named precisely because it is unmet.
- **The evidence base is tiny.** Acknowledged (`05-evidence.md` §7). n=4 instances, single operator, no control group.
- **The token mechanism could fail to produce meaningful Sybil resistance.** Acknowledged (`07-economy.md` §1.1) — economic Sybil resistance is the operationally available substrate, not a perfect one.
- **The protocol is psychologically driven by its founder's specific cognitive style.** Acknowledged (`08-shadow.md` §3) and named with the founder's own term.
- **The kernel could be captured by complexity.** Acknowledged (`08-shadow.md` §4).
- **Constitution-as-theater is the dominant failure mode of governance documents.** Acknowledged (`08-shadow.md` §6).

A critic whose argument terminates here is repeating the kernel back to itself. The kernel asks for a different argument.

### §5.3. Critiques the kernel contests

The following are critiques the kernel disagrees with, and the disagreement is substantive:

- **"Versioned constitutions are over-engineering for AI agents."** The kernel claims (`04-living.md` §7) that versioning is the only mechanism by which a constitution can be falsified — without it, every clause is ambiguously authoritative. The disagreement is empirical: produce an instance with a frozen constitution that operates over ≥3 years without ambiguity in clause authority. We have not seen one.
- **"Founder removability is not a real test, just a slogan."** The kernel claims (`01-why.md` §4) the test is operational and falsifiable — it has five named conditions, each of which can be observed as met or unmet. Bitcoin's Satoshi removal in 2010–2011 is the precedent we measure against. The disagreement is whether the precedent transfers; the kernel argues yes (governance form is portable across substrates), the critic may argue no.
- **"Multi-LLM Magistrate panels are operationally infeasible at scale."** The kernel claims (`07-economy.md` §1.1) that economic Sybil resistance plus heterogeneous-model registries make this feasible at the scale the protocol targets (specialty agents, not consumer chatbots). The disagreement is over the target scale. A critic arguing this is critiquing a use case the kernel does not target.

### §5.4. The fork-divergence path

A critic who finds the kernel structurally wrong in ways the kernel does not concede has the option to fork divergently (`00-meta.md` §4.5). The fork loses the Leviathan name and the constellation membership. It does not lose the right to exist or the right to compete. The kernel views well-executed competing forks as the highest possible signal of protocol health — they validate that the substrate (versioned, public, forkable governance) is operational, even if the specific kernel content is contested.

The most honest form of critique is to fork.

---

## §6. For Yourself, Reading This Cold

You are not yet an operator, user, researcher, or critic. You opened this document to find out what it is.

The protocol is a public, versioned, forkable, evolution-explicit governance substrate for AI agents (and, by structural identity, for personal operating systems of humans). It exists to occupy the next 24 months of the agent-governance window with an open alternative to the closed-source constitutions currently being written by six private organizations. It is operated by one founder; it claims success when the founder can be removed and it continues; it is currently in an explicitly pre-success state.

It is not an alignment proposal, not a regulatory framework, not a model, not a research project, not a brand.

If after reading the kernel you remain interested, pick the audience role above that fits — operator, user, researcher, critic — and follow that path. If after reading the kernel you are not interested, that is also a useful outcome: the kernel does not recruit, it filters.

---

## §7. Out of Scope for This Part

- Marketing or persuasion content.
- Roadmap or vision statements (kernel-tier content is timeless; vision lives in instance repos).
- Specific contact information or community channels (these change; they belong in the README, not the kernel).
- Any claim about how many operators, users, or researchers are currently engaged (those numbers belong in `05-evidence.md` and decay quickly).

---

## Citations

- `08-shadow.md` — referenced throughout as the prerequisite read.
- `01-why.md` §5 (what this protocol is not), §6 (falsification conditions).
- `03-constellation.md` §6 (forking protocol).
- `00-meta.md` §4.5 (fork divergence procedure).
- Bitcoin community engagement patterns (2009–) — operators/users/researchers/critics quadrant referenced in §1 has rough analog in early Bitcoin community structure.

---

*Part 09 of 09. Previous in outline order: `08-shadow.md`. Next: `glossary.md` (Terms layer of the kernel itself) and `CHANGELOG.md` (meta-rules in action).*
