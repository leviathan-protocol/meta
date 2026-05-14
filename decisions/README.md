# Architectural Decision Records (ADRs)

Each ADR captures one significant decision: the context, what was chosen, why, and the consequences.

## Why ADRs

Decisions get forgotten. Six months from now, no one will remember why the test board is a sub-forum instead of a separate domain. The ADR is the durable answer to "wait, why did we do it this way?"

## Numbering

`NNN-short-name.md` — three-digit zero-padded number, kebab-case slug.

`000-template.md` is the template. Number from `001` for actual decisions.

## When to write one

- Architectural choice between 2+ viable options
- Decision that affects multiple repos
- Decision the founder wants to commit to (not just experiment)
- Reversal of a previous ADR (write a new ADR explaining the reversal)

## When NOT to write one

- Implementation detail with one obvious answer
- Code style or formatting choice
- Temporary scaffolding decisions

## Status field

| Status | Meaning |
|--------|---------|
| `proposed` | Drafted, not yet committed |
| `accepted` | Committed; implementation can proceed |
| `superseded` | Replaced by a later ADR (link to it) |
| `deprecated` | No longer relevant (no replacement) |

## Process

1. Copy `000-template.md` to next number
2. Fill in `proposed` state
3. Discuss (asynchronously or in conversation)
4. Update to `accepted` when committed
5. Reference from relevant plan files / specs

## Existing ADRs

(none accepted yet — see `../status.md` for open decisions awaiting input)
