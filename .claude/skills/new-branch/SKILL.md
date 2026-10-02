---
name: new-branch
description: Create a branch that follows this repo's docs/engineering/branching-strategy.md naming and merge conventions (feat/hotfix/experiment, named after the UC or ADR it implements). Use when the user is about to start work on a use case, ADR, fix, or spike and asks to branch, or invokes /new-branch.
---

# new-branch

Creates a branch per `docs/engineering/branching-strategy.md`. Only branch when the user
has actually asked for it in this turn — never branch proactively.

## Input

`args` is whatever the user gave: a UC or ADR id (`UC-01`, `ADR-0001`), a short
description, or both (e.g. "UC-01 register with password backend"). The use case (or ADR, for
architecture-only work) is the unit of work a branch holds — an FR/NFR id alone isn't
enough to name a branch, since it's the requirement satisfied, not the slice being
implemented; if the user gives an FR instead, find its use case (or say one needs to be
written first via `new-use-case`) rather than branching on the FR id. If no id is given
and the work isn't tooling/scaffolding, ask which UC/ADR this branch implements before
proceeding.

## Steps

1. Read `docs/engineering/branching-strategy.md` for the current branch types, naming
   convention, and merge rules (don't hardcode them — stay correct if that file changes).
2. Pick the branch type:
   - `hotfix/*` — a fix for something already merged to `main`, described as urgent/
     production-critical.
   - `experiment/*` — a PoC or spike not guaranteed to merge.
   - `feat/*` — everything else, including scaffolding/tooling with no UC/ADR id
     (`.claude/skills/`, docs setup) — those use `feat/<desc>` without an id.
   If the type isn't obvious from what the user said, ask.
3. Validate the id (if given) actually exists — grep `docs/usecases/` for a UC doc or
   `docs/adr/` for an ADR file. If it doesn't exist yet, tell the user and confirm whether
   to branch anyway or scaffold the doc first (`new-use-case`/`new-adr`). If the user gave
   an FR/NFR id instead of a UC, check whether a use case already covers it (grep the
   "Related Requirements" section of `docs/usecases/*.md`); if one exists, use its UC id;
   if not, say so and offer to run `new-use-case` first rather than branching on the FR id.
4. Build the branch name from the convention: `<type>/<ID>-<slug>` (id uppercase as written
   in the docs, e.g. `UC-01`, `ADR-0001`) or `<type>/<slug>` when there's no id. Slugify the
   description (lowercase, hyphens, no stop words beyond what's needed for clarity).
5. Before branching, check git state: `git status` (working tree must be clean or changes
   stashed — don't silently carry uncommitted work onto a new branch without saying so) and
   confirm the current branch is `main` (branches always fork from `main` per the
   strategy doc). If not on `main`, ask whether to switch to `main` first (pulling latest if
   a remote tracking branch exists) or branch off the current branch instead.
6. Show the computed branch name and ask for confirmation if it required any judgment call
   (type inference, slug wording) rather than being a direct restatement of the user's
   input.
7. Create and switch to it: `git checkout -b <name>`. Run `git status` after to confirm.

## Non-goals

- Doesn't create the PR, commit anything, or touch `staging`/release tags — those are
  separate, mostly-planned parts of the strategy doc.
- Doesn't invent an id — if the user's work has no FR/UC/ADR yet, point them at
  `new-requirement`, `new-use-case`, or `new-adr` first, or confirm this is genuinely
  id-less tooling work.
