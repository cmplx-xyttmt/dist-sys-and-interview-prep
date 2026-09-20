# Progress Log

> Two logs, matching the two queues (ROADMAP §5): a one-line **DSA session log** per daily slot, and a **Sunday review** per half-day session headed by its queue position (S1, S2, …). Honest > pretty. After each *real* interview round, add a retro entry immediately.

## Scoreboard

| Metric | Target | Current |
|---|---|---|
| DSA problems solved (Python, timed) | 130+ | 2 (untimed so far) |
| DDIA chapters done (with note) | all | 0 |
| Written system designs | 10+ | 0 |
| Design mocks (verbal, timed) | 6+ | 0 |
| Glomers done — Python | 1–6 | – |
| Glomers done — Go | 1–3 + one of 4/5/6 | – |
| STAR stories drilled | 8 | 0 |
| Kaggle agents course (days done) | 5 | 0 |
| Explorations published | 3+ | 0 |
| Applications out | 15+ | 0 |
| Sunday queue position | S24 (proj. Feb 28, 2027) | next: S0 — Sun Sep 6, 2026 |

## Application pipeline

| Company | Role | Tier (warm-up/target/FAANG) | Stage | Last update | Notes |
|---|---|---|---|---|---|
| | | | | | |

## DSA session log

_One line per daily slot. Time is minutes to a passing solution (or "DNF"). Failed → re-solve date in `dsa/`._

| Date | Problems (pattern) | Time | Result | Re-solve due |
|---|---|---|---|---|
| 2026-09-05 | Group Anagrams (arrays/hashing: canonical key) · Top K Frequent Elements (arrays/hashing: count then select) | untimed | both solved; complexity narration wrong on both (per-word sort is m·n log n; sort is over d distinct, not n); heaps rusty — didn't know the heap or bucket versions | 2026-09-12 |
| 2026-09-06 | Encode and Decode Strings (arrays/hashing: length-prefix framing) | untimed | solved, correct incl. empty-string edge; shadowed builtin `str`; decoder indexing clunky (use `s.index(",", i)` + two named positions) | 2026-09-13 |
| 2026-09-06 | Product of Array Except Self (arrays/hashing: prefix/suffix) | untimed, "a few minutes" to find the idea | solved, O(n) extra; suffix array built reversed so combine indexing got confused; O(1)-extra version done after a hint, with off-by-one offsets (fix: use-then-update ordering) | 2026-09-13 |
| 2026-09-08 | Valid Sudoku (arrays/hashing: sets per constraint) | untimed | solved first try; box key written as corner coords instead of `// 3`; redundant `int()` | 2026-09-22 |
| 2026-09-08 | Longest Consecutive Sequence (arrays/hashing: set + start test) | untimed | solved via reinvented union-find w/ path compression (correct, O(n log n) amortized bound); then a memoized set-walk (O(n), TLE first w/o seen-set); didn't use the start test even after the hint | 2026-09-15 |
| 2026-09-09 | Valid Palindrome (two pointers) | untimed | solved; WA first (`isalpha` vs `isalnum`); loop stop `i == j` lets pointers cross on even lengths (2× comparisons); debug print left in; O(n) extra, in-place version pending | 2026-09-16 |
| 2026-09-10 | Two Sum II (two pointers, sorted) | untimed | solved, O(n) nested-loop variant; `i < j` guard on wrong loop (IndexError without guaranteed solution); first idea was both pointers from 0; wants practice stating invariants in plain English | 2026-09-17 |
| 2026-09-11 | 3Sum (two pointers: sort + fix one) | untimed | solved, O(n²) but i from 0 (every triplet found 3×, deduped via set of tuples + seen_targets); TLE on all zeros first; chased a linear solution first; break-at-first-match bug | 2026-09-18 |
| 2026-09-11 | Container With Most Water (two pointers) | untimed | solved via sort-by-height dominance walk, O(n log n); correct; linear two-pointer version done after a hint (couldn't find the move condition unaided); shadowed `height` param | 2026-09-18 |
| 2026-09-13 | Trapping Rain Water (two pointers / prefix-suffix) | ~1h+ | prefix/suffix version passed; an hour lost on a segment-scan attempt built on the wrong formula (nearest taller vs highest); two-pointer version done after a hint (wouldn't have found it unaided); account-then-move shape forced a `left == right` special case | 2026-09-20 |
| 2026-09-13 | Best Time to Buy and Sell Stock (sliding window: running min) | untimed | solved clean first try; asked what "sliding window" means | 2026-09-27 |
| 2026-09-15 | Longest Substring Without Repeating Characters (sliding window + set) | untimed | solved first try, left-driven window, O(n); used defaultdict(bool) for a set; right-driven shape and last-index jump to learn | 2026-09-22 |
| 2026-09-20 | Longest Repeating Character Replacement (sliding window + 26 counts) | untimed | hint needed to see the window and the 26-slot max; then solved first try, left-driven with add-check-undo; print left in | 2026-09-27 |

## Sunday reviews

_One per Sunday session, headed by queue position. Older weekly entries below kept as-is._

### S0 — Sun Sep 6, 2026 · A · Fly.io Sprites deep-dive
- **Done:**
- **What surprised me:**
- **Note / quiz questions added:**
- **What slipped & why:**
- **Next Sunday (S1, Sep 20): Maelstrom set up + Glomers 1 Echo — prep: DDIA ch. 5 in the weekday slots**

### Older weekly entries (pre-Sep 5 format)

### Week of Jul 6, 2026
- **DSA:**
- **DDIA:**
- **Go / Glomers:**
- **System design:**
- **Behavioral / logistics:**
- **What slipped & why:**
- **Adjustment for next week:**

### Week of Jul 20, 2026
- **DSA:**
- **DDIA:**
- **Go / Glomers:**
- **System design:** Wrote study note `system-design/designs/video-streaming-and-drm.md` (ABR/HLS/DASH, CDN economics, DRM/Widevine tiers, the piracy-adversary + trusted-client thesis) — a *domain note*, not a counted written-design rep. Spec'd the "Defender's Dilemma" security/design mini-game (§9 of that note).
- **Explorations:** Built `sprites-explainer.html` — interactive explainer on Fly.io Sprites (design, storage stack, what-to-learn map, projects, plan-fit). Added as bonus exploration #5 in ROADMAP §8. Researched Fly.io's Jul 24 2026 news: new CEO Scott Johnston (ex-Docker), $25M Series D, full pivot to "computers for agents."
- **Behavioral / logistics:**
- **What slipped & why:**
- **Adjustment for next week:**

## Interview retros

<!-- ### YYYY-MM-DD — Company, round type
What was asked · how it went · what to patch -->
