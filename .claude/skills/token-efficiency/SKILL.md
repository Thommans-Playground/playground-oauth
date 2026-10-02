---
name: token-efficiency
description: Concrete habits for cutting token/context usage in a coding-agent session — when to grep vs. read whole files, batching tool calls, right-sizing subagent use, trimming narration, and avoiding redundant re-reads or re-searches. Use when a session is getting long, before reading or searching a large file/repo, before spawning a subagent, or when asked how to reduce token usage or context bloat. Not a communication-style rewrite (see caveman-style tools) — this changes tool-use and search patterns, not how sentences are phrased.
---

# token-efficiency

Most of a coding agent's token spend is in tool *inputs and outputs* (file contents, search
results, diffs, subagent transcripts) — not in the model's own prose. These habits target
that spend directly, instead of shortening sentences at the cost of clarity.

## Reading & search

- Don't read a whole file to find one thing. Use `Grep`/`Glob` (or a fast search agent) to
  locate the symbol/pattern first, then read only the matching region.
- For a large file where you already know the region you need, read with `offset`/`limit`
  rather than the whole file.
- Don't re-read a file you just wrote or edited to "confirm" it — a successful `Write`/`Edit`
  already guarantees the change landed.
- Don't re-fetch or re-grep something already established earlier in the session unless the
  underlying file could plausibly have changed since (e.g. another process/tool touched it).
- One well-scoped search agent call beats several manual `Grep`→`Read`→`Grep` round-trips
  when exploring unfamiliar code — each round-trip re-pays a context "toll."

## Tool-call batching

- Independent tool calls (no data dependency between them) go in one turn, not sequential
  turns — sequential round-trips each carry fixed overhead on top of the work itself.
- Only serialize calls when a later call's arguments genuinely depend on an earlier call's
  result.

## Subagents

- Fork (when available) instead of spawning a fresh subagent for work that needs your
  existing context — a fresh agent re-derives everything from a cold start, which costs more
  than the work it's doing.
- Don't spawn a subagent at all for something answerable in one or two direct tool calls;
  subagent dispatch has fixed overhead that only pays off for genuinely multi-step or
  parallelizable work.
- Push large, disposable intermediate output (raw command dumps, exploratory search noise)
  into a fork or a scratch file instead of the main conversation, so it doesn't sit in context
  for the rest of the session.

## Output & narration

- Don't restate a plan that was just agreed, or re-summarize a diff/output the user can
  already see in the tool result.
- State conclusions and decisions directly; skip narrating the intermediate reasoning steps
  that got you there.
- When fetching a web page, give a specific extraction prompt ("find the config option for
  X") rather than "summarize this page" — a targeted prompt pulls back a paragraph instead of
  the whole page.

## Session hygiene

- Prefer the harness's own completion signals (background task notifications, fork
  completion) over manual polling loops — each poll is a wasted round-trip if nothing
  changed.
- When a task is truly done, stop — don't add speculative follow-up work "while you're at
  it" that reopens files already closed out.

## What this is not

This is not about compressing the model's *language* (dropping articles, clipping words) —
that saves negligible tokens and actively hurts correctness and readability. It's about not
paying for context you didn't need in the first place.
