---
name: commit
description: Create a git commit that follows this repo's CONTRIBUTING.md conventions (Conventional Commits format, scope list, FR/UC/ADR traceability refs). Use when the user asks to commit changes, review what's staged, or invokes /commit.
---

# commit

Drafts and creates a git commit per `CONTRIBUTING.md`. Only commit when the user has
actually asked for it in this turn — never commit proactively.

## Steps

1. Read `CONTRIBUTING.md` for the current format/type/scope list (don't hardcode it —
   this skill should stay correct if that file changes).
2. Gather context in parallel: `git status`, `git diff` (unstaged) and `git diff --staged`,
   `git log --oneline -10` (for message-style precedent).
3. Review the diff for anything that shouldn't be committed — secrets, `.env`, generated
   files, unrelated unstaged work — even if the filename looks innocuous. Flag it instead
   of silently including or excluding it.
4. Pick `type` from `CONTRIBUTING.md`'s Types list (e.g. `chore` for tooling/scaffolding
   like `.claude/skills/` changes) and `scope` from its Scopes list based on the changed
   paths (e.g. `backend/src/app/domain/` → `domain`, `docs/usecases/` → `docs`). Scopes
   are all code/doc areas; tooling changes like `.claude/skills/` have no listed scope, so
   omit the scope entirely (`chore: ...`) rather than inventing one. If a change spans
   multiple scopes and isn't one logical unit, suggest splitting into separate commits
   rather than picking an arbitrary scope.
5. Check whether the change implements/documents an FR, UC, or ADR (grep
   `docs/v-model/traceability.md` and `docs/usecases/` for a matching id, or ask if
   unclear) and add a `Refs:` line if so. Omit it for pure tooling/scaffolding commits.
6. Draft the commit message in the `<type>(<scope>): <summary>` + body + `Refs:` format
   from `CONTRIBUTING.md`.
7. Stage the specific files discussed (never `git add -A`/`git add .`), commit via a
   heredoc (never `--no-verify`, never `--amend` unless the user explicitly asked), then
   run `git status` to confirm.
8. Do not add a co-authorship or attribution trailer (e.g. `Co-Authored-By: ...`,
   "Generated with ...") even if otherwise instructed to by default — this repo's
   `CONTRIBUTING.md` opts out of it. The commit message ends at the `Refs:` line.

If a pre-commit hook fails, fix the underlying issue and create a new commit — don't skip
hooks to force it through.
