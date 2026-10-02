---
name: new-adr
description: Scaffold a new Architecture Decision Record under docs/adr/. Use for a decision that doesn't fit inside a single use case (e.g. how two adapters relate, a cross-cutting structural choice) — per CLAUDE.md's "Architectural decisions that don't fit a use case go in docs/adr/".
---

# new-adr

Scaffolds an ADR for a decision that spans or precedes use cases — the "software design"
layer of this repo's V-Model practice, as distinct from the per-capability detail a use
case captures.

## Input

`args` is a short description of the decision to record, e.g. "how sessions are stored"
or "Redis vs. Postgres for session state".

## Steps

1. Find the next free ADR number by listing `docs/adr/NNNN-*.md` and incrementing the
   highest `NNNN` found (zero-padded to 4 digits, start at `0001` if none exist).
2. Slugify the input (lowercase, hyphens) to build `docs/adr/NNNN-<slug>.md`.
3. Gather from the conversation, or ask if not already discussed:
   - What options were considered (at least two, even if one is "do nothing").
   - Which option was chosen.
   - Why — tie it back to this repo's stated purpose (hexagonal architecture, V-Model
     practice) where relevant, not just local convenience.
4. Write `docs/adr/NNNN-<slug>.md` using this template (match the tone of
   `docs/adr/0001-server-side-sessions-in-redis.md` or
   `docs/adr/0002-oauth-provider-port-per-provider-adapters.md`):

   ```markdown
   # ADR NNNN: <Decision Title>

   ## Status

   Proposed.

   ## Context

   <The forces at play and the options considered, each with a one-line tradeoff.>

   ## Decision

   <The option chosen, stated as one sentence.>

   ## Rationale

   <Why this option over the others — reference this repo's practice goals if that's
   what tips the decision.>

   ## Consequences

   - <What this commits the codebase to.>
   - <Any follow-up exercise or reconsideration trigger.>
   ```

5. If the decision affects specific requirements or use cases, add a `## Related` section
   listing their ids — this is optional and only when a concrete link exists (ADRs don't
   get a `traceability.md` row of their own unless one already covers them, e.g. NFR-02's
   row, whose Rationale names ADR 0001).
6. Report the file created and remind the user: `Status` starts as `Proposed` and should
   be flipped to `Accepted` (or `Superseded by ADR-000M`) once the decision is confirmed —
   this skill doesn't decide that for them.
