---
adr: 000
title: <Short title — what was decided>
status: template
date: YYYY-MM-DD
authors: [name]
supersedes: null
superseded_by: null
---

# ADR 000 — <Title>

## Context

What's the situation? What forces are at play? What problem are we solving? Keep this section factual and brief — describe the world before the decision was made.

## Decision

What did we decide? Be specific. Include enough detail that someone reading this years later can re-derive the decision.

## Rationale

Why this option over the alternatives? List the specific reasons. Tie back to forces from the Context section.

## Alternatives considered

For each viable alternative:

### Alternative A: <name>
- What it would have looked like
- Why we didn't choose it

### Alternative B: <name>
- What it would have looked like
- Why we didn't choose it

## Consequences

### Positive
- What's now possible / easier / safer

### Negative
- What's now harder / more costly / more constrained
- Tech debt taken on

### Neutral
- Trade-offs that aren't strictly better or worse

## Related

- Links to relevant plan files, specs, code
- Links to upstream decisions this depends on
- Links to downstream decisions this enables

## Revisit conditions

When should we re-examine this decision? Examples:
- "If validator latency exceeds X seconds"
- "When we hit N concurrent agents"
- "After the first public incident"

If conditions never get met, the decision stands.
