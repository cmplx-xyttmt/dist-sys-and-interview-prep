# Sliding Window Maximum

LeetCode 239 · https://leetcode.com/problems/sliding-window-maximum/ · solved 2026-09-26 (unaided, heap version; O(n) version pending)

**Pattern:** fixed-size window, max tracked by a max-heap with lazy deletion. Values
leaving the window aren't removed from the heap; a counter says whether the top is
still in the window, and stale tops are popped only when they surface. O(n log n)
time (stale entries can pile up, so the heap is bounded by n, not k), O(n) space.
20k random tests OK. Accepted, but an interviewer will ask for O(n).

**What I wrote:** the idea is sound, the housekeeping isn't. Two structures (heap
plus a counter keyed by the negated value) that have to be kept in step on every
add and every remove, a prefill loop before the main loop, and a trailing append
after it. The prefill and the trailing line are the same asymmetry as Permutation
in String: one loop over every index, record once `i >= k - 1`, remove the element
`k` back, and both go away. `window_set` is a `Counter`, and named like a set.

**Cleaner version of the same idea:** push `(-value, index)` pairs. Then "stale"
is `index <= i - k`, read straight off the heap top, and the counter disappears.
One structure, same complexity.

**Missed insight:** _pending the O(n) attempt._ The question to answer: when a
new number enters the window, what is true of every number already in the window
that is smaller than it? Can any of those ever be the maximum of a later window?
If not, why keep them?

**Next re-solve:** 2026-10-03 (code; the O(n) version cold, and say in one
sentence why the structure it uses stays sorted).
