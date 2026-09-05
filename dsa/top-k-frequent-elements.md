# Top K Frequent Elements

LeetCode 347 · https://leetcode.com/problems/top-k-frequent-elements/ · solved 2026-09-05

**Pattern:** count, then select. Three ways to select the top k from d distinct counts:
- sort the (count, num) pairs — O(n + d log d), O(n log n) worst case. What I wrote.
- min-heap of size k (`heapq.nlargest`, which is what `Counter.most_common(k)` uses) —
  O(n + d log k). Push each pair, pop the smallest whenever size > k.
- bucket by count — counts are integers in [1, n], so an array of n+1 lists indexed
  by count (counting sort on frequencies), walked from the top until k collected. O(n)
  time and space. Derived 2026-09-05 after a hint, described not coded.

**Missed insight:** the sort is over d distinct values, not n, so say O(n + d log d).
Didn't know the heap or bucket versions; heap ops need a refresh
(`heappush`, `heappop`, `nlargest`; Python heaps are min-heaps, negate for max).
Trade-off to say unprompted: bucket is optimal on paper, heap is what you'd ship
for small k (log k is tiny, memory O(d + k) not O(n)). Watch the n+1 off-by-one
when coding the buckets.

**Next re-solve:** 2026-09-12 (code all three cold, then say the complexities and when
each wins).
