# CLAUDE.md — working notes for dist-sys-interview-prep

This repo is Isaac's FAANG-tier **senior interview prep + distributed systems learning** workspace (July 2026 → Jan 2027). `ROADMAP.md` is the source of truth for the plan; `PROGRESS.md` is the running log; `roadmap.html` is the **interactive living doc** (open locally in a browser — never publish as a hosted artifact unless asked).

## roadmap.html — living doc + testbed

- It mirrors ROADMAP.md (timeline tasks, tracks, scoreboard) — **when the plan changes, update both**. The data arrays: `MONTHS` (milestones), `DSA_GROUPS` (NeetCode 150 w/ LeetCode slugs), `DDIA_CH`, `GLOMERS`, `DESIGNS`, `MOCKS`, `COURSE`, `STORIES`, `EXPL`, `TRACKS_INFO`. The Schedule tab is **generated** from these (month field + `distribute()`), and the scoreboard is **derived** from checked items — don't hand-maintain either.
- It carries a `QUIZ` array (`{cat,q,opts,correct,why}` — same shape as 2brain-cc's explainer). When Isaac finishes a DDIA chapter or Glomers challenge, **add 1–3 medium-difficulty questions** covering it. No gotchas — questions must require understanding.
- Its **Lab tab prototypes interaction mechanics** for two downstream targets: 2brain-cc features and his blog's "interactive explorations" (see ROADMAP §8). Treat Lab widgets as experiments — small, self-contained, no external deps (the file must work offline from `file://`).
- Progress state lives in `localStorage` (`dsprep-v1`) with JSON export/import — never restructure the state shape without a migration path. Shape: `tasks` (manual timeline milestones), `items` (granular checkboxes), `notes` (per-week free text, keyed `wk-YYYY-MM-DD`), `metrics.apps`, `quiz`, `game`. The `AUTO` map derives most timeline milestones from `items` — when adding a milestone that corresponds to granular items, add an `AUTO` entry instead of a manual checkbox. **Week notes may contain Isaac's own learning notes — treat them as data to preserve, never regenerate.**

## Purpose & constraints

- Isaac is preparing for **senior (L5/E5) backend roles**. Interview language is **Python**; **Go is for learning distributed systems** (Gossip Glomers), never for interview practice.
- System design is his self-identified weakest area — bias help toward it.
- He is learning, not delegating: **explain reasoning and trade-offs, don't just produce answers.** For DSA problems especially: give hints and let him struggle before revealing solutions. Never just hand over a Glomers solution — that defeats the repo's purpose.

## Working style (mirrors his 2brain-cc conventions)

- Prefer the smallest coherent change; keep him in the loop on decisions.
- **Active recall:** after he completes a chapter, challenge, or design, offer to quiz him — he explains first, you assess and correct.
- When reviewing his designs (`system-design/designs/`), play the interviewer: probe bottlenecks, failure modes, and scale math rather than rewriting.

## Living-doc maintenance

- When a Glomers challenge, DDIA chapter, or design is completed, tick it in `ROADMAP.md` progress-relevant sections and prompt him to log it in `PROGRESS.md` (weekly entry format is defined there).
- If the schedule slips, adjust `ROADMAP.md` dates honestly rather than pretending — the checkpoints (Oct 2026 minimum readiness, Sept 2026 applications) are the anchors.
- Use absolute dates in all docs.

## Conventions

- Glomers layout: `glomers/python/challenge-N-name/` and `glomers/go/cmd/<name>/` with shared Go primitives in `glomers/go/pkg/`.
- DSA notes in `dsa/` are terse: problem, pattern, the missed insight, next re-solve date.
- Maelstrom binary + workloads: document setup in `glomers/README.md` once installed.
- Related project: `../acu-2brain-cc/` (his app build, separate time budget — see ROADMAP §7).
