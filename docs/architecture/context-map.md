# Context Map

`context-map.puml` is this repo's DDD strategic context map (Evans/Vernon): bounded
contexts, their subdomain type, and the integration pattern between them, as opposed to
the tactical, per-use-case sequence diagrams in `docs/usecases/`.

## Reading it

- **Stereotypes** (`«Core»`, `«Supporting»`, `«Generic»`) classify a bounded context's
  strategic importance, per Evans' subdomain classification.
- **Relationship labels** (`«C/S»` customer/supplier, `«OHS»` open host service, `«ACL»`
  anti-corruption layer, `«shared kernel»`) name the integration pattern between two
  contexts, per Vernon's *Implementing Domain-Driven Design*.
- A commented-out `package`/relationship is a **planned, not-yet-built** context — kept
  visible so the strategic shape isn't lost, but it isn't a decision and isn't reflected
  in code until it's actually pursued (and gets its own FRs/use cases/ADR first, per the
  doc-first workflow in `CLAUDE.md`).

## Current state

playground-oauth has one bounded context: **Identity & Access** (`«Core»`) — everything in
`docs/requirements/functional.md`'s "Account Registration & Authentication" and "Session
Management" features lives here, not as separate contexts.

Google, Microsoft, and GitHub are drawn as three **external** systems (`«Generic»`
subdomain — undifferentiated identity-provider plumbing, not something this project builds
or competes on). The relationship is an **anti-corruption layer (ACL)**: this context never
adopts a provider's own token/userinfo model directly — each `OAuthIdentityProvider`
adapter (ADR-0002) translates a provider's response into this context's own
(`provider_user_id`, `verified_email`) shape before it crosses into `application/`.

This map does **not** show the hexagonal architecture (REST adapter, Postgres, Redis) —
that's ADR-0001/ADR-0002 and the per-use-case `.puml` diagrams. A context map is about
domain boundaries, not technical layering.

For the ubiquitous language and tactical model (Entity/Value Object/Aggregate) *within*
the Identity & Access context, see `glossary.md` — this file only maps the contexts and
their relationships, not what's inside them.
