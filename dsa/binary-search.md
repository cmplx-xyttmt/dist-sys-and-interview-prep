# Binary Search

LeetCode 704 · https://leetcode.com/problems/binary-search/ · solved 2026-10-25

**Pattern:** the boundary template from the
[Kth Smallest note](./kth-smallest-element-in-a-sorted-matrix.md). The predicate
`nums[i] <= target` is T...TF...F over a sorted array. Sentinels `left = -1` (always T)
and `right = n` (always F) are positions you never read. Loop `while left + 1 < right`,
and `left` ends on the last T. Then check whether that position holds the target.
O(log n). 50k random sorted arrays against `list.index` OK.

**What I wrote:** correct, with the invariant written as the first line. That's the
habit that makes binary search safe, and it came back from the Kth Smallest session
without a prompt (second time, after Sum of Square Numbers). Two cleanups:

- `if mid < 0: break` never runs. Inside the loop `left + 1 < right`, so `mid` is
  strictly between them and at least 0. Being able to say why a guard is dead is part
  of the invariant argument.
- `nums[left]` with `left = -1` reads the last element through Python's negative
  indexing. It still returns the right answer, because `left = -1` means every element
  is above the target, the last one included. That reasoning is correct but hidden.
  Write `left >= 0 and nums[left] == target` so the reader doesn't need it (and so the
  code ports to a language where -1 is out of bounds).

**Missed insight:** none. With duplicates this returns the last occurrence; flip the
predicate to `nums[i] < target` and return `right` for the first.

**Next re-solve:** none (clean).
