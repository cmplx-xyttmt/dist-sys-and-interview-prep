# Largest Rectangle in Histogram

LeetCode 84 · https://leetcode.com/problems/largest-rectangle-in-histogram/ · solved 2026-10-24 (passed)

**Pattern:** for each bar, the widest rectangle in which it is the shortest bar. That
rectangle runs from just after the nearest strictly shorter bar on the left to just
before the nearest strictly shorter bar on the right. Both neighbours come from a
monotonic stack: pop everything at least as tall as the current bar, and the top is
the nearest shorter one. Every bar is the shortest bar of some rectangle, so the answer
is the max over bars. O(n) time, O(n) space. 20k random arrays against an O(n²) brute
force OK; 100k bars (increasing, decreasing, all equal, random) in about 30 ms.

**What I wrote:** two passes, one stack each way, then a third loop for the areas.
Correct. The comment at the top is the whole argument in three lines, which is the part
an interviewer wants to hear first. Cleanups:

- The sentinels `(-1, -1)` and `(-1, n)` have height -1, so they are never popped
  (heights are >= 0). `left_stack` is never empty and the `else` branches never run.
  The sentinels already do that job, so the `if` can go.
- Store indices only and read `heights[j]`. The heights in the tuples duplicate the input.
- `right = [0] * n` and `right[i] = ...` removes the append-then-reverse (same note as
  Daily Temperatures).
- `>=` on both sides is fine for a max. Only one side needs to be strict if you were
  counting rectangles, because equal bars would otherwise each claim the same one.

**Open, hinted:** the one-pass version. When bar `j` gets popped because `heights[i]`
is smaller, what do you already know about `j`'s right edge, and about its left edge?

**Missed insight:** none in the algorithm. Fourth sighting of "a newer, smaller
element ends older, taller ones".

**Next re-solve:** none (clean; re-solves paused except first-fail problems). Close the
Stack group with the one-pass version if you want it.
