# Longest Consecutive Sequence

LeetCode 128 · https://leetcode.com/problems/longest-consecutive-sequence/ · solved 2026-09-08

**What I wrote:** union-find, reinvented. `start` = parent map, `find_start` = find
with path compression, "n-1 and n+1 both present" = union (right root under left
root). Correct on 20k random tests incl. duplicates and negatives. Amortization
instinct was right but the result is O(log n) amortized per op for path compression
alone (Tarjan); union by rank gets near-constant. Descending inserts (5,4,3,2,1) build
a chain with no find called, so it is not obviously constant. Comes back by name in
Graphs: Number of Connected Components, Redundant Connection.

**Second version (after hint):** set + walk upward, but memoized (`lengths` dict,
`seen` set) instead of using the start test. Correct, O(n) (each value marked seen
once, then only an O(1) break point). 200k values in any order: ~0.04s. Got TLE first
without the seen-set: walking from every n is O(n²) on one long run.

**Intended version:** n is a start iff `n - 1 not in s`. Walk up only from starts;
each number is visited by exactly one walk (its own run's), so O(n) with no memo,
no seen-set, no empty guard. Iterate over the set, so duplicates are free.

**Missed insight:** twice reached for structure (parent pointers, then a memo)
before asking what a bare membership test answers. The neighbour's absence *is* the
boundary. Habit: before adding pointers or a memo, ask what the simplest structure
already tells you. The analysis itself (count touches per element, not loop
iterations) was fine; the gap is in the design step. Same touched-once argument
recurs in Two Pointers, Sliding Window, and monotonic Stack.

**Next re-solve:** 2026-09-15 (set version cold, state the each-number-visited-once
argument; then explain union-find's amortized bound in two sentences).
