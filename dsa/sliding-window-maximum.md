# Sliding Window Maximum

LeetCode 239 · https://leetcode.com/problems/sliding-window-maximum/ · solved 2026-09-26 (heap version unaided; O(n) deque version the same day after one leading question)

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

**O(n) version (same day, after one leading question):** a monotonic deque. When
`num` arrives, every number already in the window that is smaller than `num` can never
be the max of a later window, because `num` outlives all of them. So pop them from the
back before appending. What survives is non-increasing front to back, so the front is
the max, and the departing element `nums[i - k]`, if it is still present, can only be
at the front. Each element is pushed once and popped at most once: O(n), deque
bounded by k. 50k random tests with heavy duplicates OK; a million elements in 0.12s.

**Why the value comparison at the front is safe:** the eviction is strict (`num >
window[-1]`), so an element leaves the deque early only when something strictly larger
and newer arrives, and that larger element (or something larger still) is still
ahead of it when it would have departed. So `window[0] == nums[i - k]` can only be
true when the front *is* the departing index, never a later equal value. Subtle; the
standard shape stores indices in the deque and pops the front when `window[0] <=
i - k`, which needs no argument. Have that form ready too.

**Missed insight:** couldn't see past "keep the max in a heap". The question that
unlocked it: what is true of the numbers smaller than the one entering, given that
it outlives them? A newer, larger element makes older, smaller ones dead. That is the
monotonic-stack idea, and it comes back in the Stack group (Daily Temperatures, Largest
Rectangle). The deque is a monotonic stack that also drops from the front when an
element ages out.

**Next re-solve:** 2026-10-03 (code; deque version cold, index-based, and say in one
sentence why the deque stays sorted).
