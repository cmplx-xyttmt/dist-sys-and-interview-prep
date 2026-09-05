# Top K Frequent Elements

LeetCode 347 · https://leetcode.com/problems/top-k-frequent-elements/ · solved 2026-09-05

**Pattern:** count, then select. Three ways to select the top k from d distinct counts:
- sort the (count, num) pairs — O(n + d log d), O(n log n) worst case. What I wrote.
- min-heap of size k (`heapq.nlargest`, which is what `Counter.most_common(k)` uses) —
  O(n + d log k). Push each pair, pop the smallest whenever size > k.
- bucket by count — counts are integers in [1, n], so index an array by count. O(n).

**Missed insight:** the sort is over d distinct values, not n, so say O(n + d log d).
Didn't know the heap or bucket versions; heap ops need a refresh
(`heappush`, `heappop`, `nlargest`; Python heaps are min-heaps, negate for max).
Bucket version still to derive.

**Next re-solve:** 2026-09-12 (do the bucket version cold, then say all three
complexities and when each wins).
