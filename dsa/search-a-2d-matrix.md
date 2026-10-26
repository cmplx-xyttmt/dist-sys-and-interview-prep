# Search a 2D Matrix

LeetCode 74 · https://leetcode.com/problems/search-a-2d-matrix/ · solved 2026-10-26 (second version; the first was a linear scan)

**Pattern:** treat the matrix as one sorted array of length `rows * cols`. Position `i`
is `divmod(i, cols)`, which is row-major order. Then it's the Binary Search template:
sentinels -1 and `size`, predicate `value <= target`, `left` ends on the last T, check it.
O(log(mn)). 20k random matrices against `target in values` OK, at most 6 steps on 6x6.

**Why row-major works here and didn't in Kth Smallest:** this problem promises each row's
first value is bigger than the previous row's last, so row-major order *is* sorted order.
In [Kth Smallest](./kth-smallest-element-in-a-sorted-matrix.md) rows and columns were
sorted separately (`[[1,5],[2,9]]`), and `i * cols + j` was not a rank. Check the
promise before flattening.

**What I wrote:** the first version had `mid = (left + right)` with no `// 2`. It still
returned correct answers. While `left = -1`, `mid` is `right - 1`, so `right` walked down
one position at a time until it reached the target's boundary: a linear scan from the end,
up to `rows * cols` steps (36 on a 6x6, 10,000 on 100x100) where binary search needs 14.
It passes LeetCode because 10,000 is small. Correct output did not mean the right
algorithm; counting loop steps showed it. Found the missing `// 2` from a hint.

**Same hidden step as Binary Search:** when every value is above the target, `left` ends
at -1 and `divmod(-1, cols)` is `(-1, cols - 1)`, the bottom-right corner via negative
indexing. That corner is above the target, so the answer is still False, but say it or
write `left >= 0 and`. (Asked; not answered yet.)

**Missed insight:** a binary search that is accidentally linear still passes. If the
complexity matters, count iterations on a test, don't trust the green tick.

**Next re-solve:** none (a typo, not an algorithm gap).
