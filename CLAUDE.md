# CLAUDE.md — working notes for dist-sys-interview-prep

This repo is Isaac's FAANG-tier **senior interview prep + distributed systems learning** workspace (started July 2026; restarted Sep 4, 2026 — checkpoints are scoreboard triggers, not dates). `ROADMAP.md` is the source of truth for the plan; `PROGRESS.md` is the running log; `roadmap.html` is the **interactive living doc** (open locally in a browser — never publish as a hosted artifact unless asked).

## roadmap.html — living doc + testbed

- It mirrors ROADMAP.md (queues, timeline tasks, tracks, scoreboard) — **when the plan changes, update both**. The data arrays: `SUNDAYS` (the Sunday queue — ROADMAP §5, one entry per half-day session, in order, with projected dates), `MONTHS` (stage containers + milestones for the Timeline tab), `DSA_GROUPS` (NeetCode 150 w/ LeetCode slugs — the DSA queue is this list in order), `DDIA_CH`, `GLOMERS`, `DESIGNS`, `MOCKS`, `COURSE`, `STORIES`, `EXPL`, `TRACKS_INFO`. The Schedule tab renders the two queues from `SUNDAYS` + `DSA_GROUPS`, and the scoreboard is **derived** from checked items — don't hand-maintain either. **Weeks are gone (Sep 5, 2026):** a slipped Sunday shifts the dates of everything after it; re-project at season boundaries, never re-order to hide a slip.
- It carries a `QUIZ` array (`{cat,q,opts,correct,why}` — same shape as 2brain-cc's explainer). When Isaac finishes a DDIA chapter or Glomers challenge, **add 1–3 medium-difficulty questions** covering it. No gotchas — questions must require understanding.
- Its **Lab tab prototypes interaction mechanics** for two downstream targets: 2brain-cc features and his blog's "interactive explorations" (see ROADMAP §8). Treat Lab widgets as experiments — small, self-contained, no external deps (the file must work offline from `file://`).
- Progress state lives in `localStorage` (`dsprep-v1`) with JSON export/import — never restructure the state shape without a migration path. Shape: `tasks` (manual timeline milestones), `items` (granular checkboxes), `notes` (per-session free text, keyed `wk-YYYY-MM-DD` = the Monday of that Sunday's week, so pre-Sep-5 week notes stay attached), `metrics.apps`, `quiz`, `game`. The `AUTO` map derives most timeline milestones from `items` — when adding a milestone that corresponds to granular items, add an `AUTO` entry instead of a manual checkbox. **Week notes may contain Isaac's own learning notes — treat them as data to preserve, never regenerate.**

## Purpose & constraints

- Isaac is preparing for **senior (L5/E5) backend roles**. Interview language is **Python**; **Go is for learning distributed systems** (Gossip Glomers), never for interview practice.
- System design is his self-identified weakest area — bias help toward it.
- He is learning, not delegating: **explain reasoning and trade-offs, don't just produce answers.** For DSA problems especially: give hints and let him struggle before revealing solutions. Never just hand over a Glomers solution — that defeats the repo's purpose.

## Working style (mirrors his 2brain-cc conventions)

- Prefer the smallest coherent change; keep him in the loop on decisions.
- **Active recall:** after he completes a chapter, challenge, or design, offer to quiz him — he explains first, you assess and correct.
- When reviewing his designs (`system-design/designs/`), play the interviewer: probe bottlenecks, failure modes, and scale math rather than rewriting.

## Living-doc maintenance

- When a Glomers challenge, DDIA chapter, or design is completed, tick it in `ROADMAP.md` progress-relevant sections and prompt him to log it in `PROGRESS.md` (DSA sessions go in the session log; Sundays get a review entry headed by their queue position).
- If the schedule slips, shift the Sunday-queue projections in `ROADMAP.md` §5 and `SUNDAYS` honestly rather than pretending; the anchors are the scoreboard triggers (§3E, §5), not dates.
- Use absolute dates in all docs.

## Conventions

- Glomers layout: `glomers/python/challenge-N-name/` and `glomers/go/cmd/<name>/` with shared Go primitives in `glomers/go/pkg/`.
- DSA notes in `dsa/` are terse: problem, pattern, the missed insight, next re-solve date.
- Maelstrom binary + workloads: document setup in `glomers/README.md` once installed.
- Related project: `../acu-2brain-cc/` (his app build, separate time budget — see ROADMAP §7).

## sprites-guide/ — the Sprites ladder (added Sep 18, 2026; owns system design from Sep 23)

- **From Sep 23, 2026 the guide is the system-design track for season 2** (WEEK.md bet 3): Tue + Thu 19:30, one rung a week in two halves, every session interleaving reading and doing (Isaac cannot sustain reading-only sessions; two evenings proved it). Before each Thursday, re-cut the rung's page into the two-half script in `build.py` and pre-stage `rungs/<lN>/` (commands, check script). ROADMAP §5 Queue 2 is the backlog after L8; Glomers/Maelstrom = rung L6, Python, guided. Calendar and decisions live on `index.html`; `sprites-ladder.md` was folded in and deleted Sep 23.

- An interactive prerequisite guide in the shape of `../optimization-competitions/learning/guide/`: nine rung pages (L0–L8), generated by `sprites-guide/build.py`, `index.html` (start page + glossary), `explainer-map.html`, `showcase.html`, and `explainer.html` (the former `sprites-explainer.html`, restyled light and given a sidebar; the old path redirects). **Since Sep 24 the pages are reference only: no text boxes, checkboxes or checkpoint widget.** Each rung has a tutor session: `cd sprites-guide/rungs/<id> && claude`, then `start`. The tutor's instructions are `rungs/<id>/CLAUDE.md` (generated by build.py); it discusses the guesses, gives feedback, and writes progress to `rungs/<id>/progress.json` (build.py never overwrites it), including the pass. That file is the record for the ladder. The old `localStorage` key `sprites-ladder-v1` no longer changes, so the sidebar dots don't show passes. Every term a rung's say-list names needs a source or an inline explanation before the step that uses it; the known gaps for L1–L8 are in `sprites-guide/rungs/SOURCE-GAPS.md`.
- `build.py` generates the rung pages, the map, `showcase.html` (from `../curriculum-edtech/course-from-a-link-on-sprites.md`, which stays the source text) and refreshes the "Rungs that make this section readable" line under each `explainer.html` heading. Edit `RUNGS` in `build.py`, then run it. `assets/progress.js` holds the sidebar's copy of the curriculum; keep slugs and checkpoint sentences in step.
- **Spell every label out.** Isaac flagged (Sep 18) that first drafts leaned on coined shorthand ("S-queue", "§03 bets 1 and 3"). Name the file and section, or link the anchor.
