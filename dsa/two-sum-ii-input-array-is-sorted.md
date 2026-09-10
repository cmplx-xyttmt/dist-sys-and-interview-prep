# Two Sum II (sorted input)

LeetCode 167 · https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/ · solved 2026-09-10

**Pattern:** two pointers converging on a sorted array. Invariant in one sentence:
if `a[i] + a[j] < target`, then `a[i]` paired with anything at or left of `j` is also
too small, so index `i` can never be in the answer and is eliminated; symmetric for
`> target` eliminating `j`. Every step permanently eliminates one index, so O(n).

**What I wrote:** outer loop on `i`, inner `while a[j] > target - a[i]: j -= 1`.
Framing: as `i` moves right, the needed complement `target - a[i]` is non-increasing,
so the search for it only moves left. Correct, O(n) because `j` is monotone (count
pointer moves, not loop iterations, same argument as Longest Consecutive Sequence).

**Missed insight:** the `i < j` guard is on the `if`, not the inner `while`, so
without the problem's guaranteed solution the inner loop runs `j` past 0, wraps via
negative indexing, and raises IndexError (`[5,6], target 3`). Guard the loop that
moves the pointer. The canonical single-loop form (compare sum, move one pointer per
iteration) has no such hole and is the one to write cold.

First wrong idea was both pointers starting at 0. Disproof in one sentence: that
scheme has a move that increases the sum but none that decreases it, so on overshoot
you must reset `j`, which is O(n²). Habit for disproving: build a 4-element
counterexample rather than argue abstractly.

**Explaining:** write the invariant as the first comment, before the loop: "what
does each pointer move do to the sum, and which index does it eliminate?"

**Next re-solve:** 2026-09-17 (single-loop form cold; say the elimination invariant
in plain English before typing).
