# Longest Consecutive Sequence

LeetCode 128 · https://leetcode.com/problems/longest-consecutive-sequence/ · solved 2026-09-08

**What I wrote:** union-find, reinvented. `start` = parent map, `find_start` = find
with path compression, "n-1 and n+1 both present" = union (right root under left
root). Correct on 20k random tests incl. duplicates and negatives. Amortization
instinct was right but the result is O(log n) amortized per op for path compression
alone (Tarjan); union by rank gets near-constant. Descending inserts (5,4,3,2,1) build
a chain with no find called, so it is not obviously constant. Comes back by name in
Graphs: Number of Connected Components, Redundant Connection.

**Intended O(n) pattern:** set + start-of-run test. _Pending: derive from the hint
"how do you know n starts a run in O(1)?" then "how many times is each number
visited across all upward scans?"_

**Missed insight:** reached for a linking structure when a membership test was
enough. Check first whether the set alone answers "is this a start?" before building
anything with pointers.

**Next re-solve:** 2026-09-15 (set version cold, state the each-number-visited-once
argument; then explain union-find's amortized bound in two sentences).
