# 3Sum

LeetCode 15 · https://leetcode.com/problems/3sum/ · solved 2026-09-11

**Pattern:** sort, fix the smallest element `k`, run Two Sum II on `nums[k+1:]`.
O(n²) time, O(1) extra beyond output. Don't look for linear: 3SUM is conjectured to
have no O(n^(2-ε)) algorithm (the "3SUM conjecture"); saying that is the right answer
to "can you do better?"

**Duplicate handling, the whole difficulty:**
- skip `k` when `nums[k] == nums[k-1]` (k > 0).
- after recording a match, advance `i` while `nums[i] == nums[i-1]` (compare to the
  value just used, not the next one).
- wrong point to skip: before the first comparison. On `[-2, 1, 1]`, skipping equal
  `i` values up front jumps past the first 1 and misses the only triplet.

**What I wrote:** correct, O(n²), but i started at 0 and skipped `k` with `i == k` /
`j == k` checks, so every triplet is found three times and deduped through a set of
sorted tuples, plus a `seen_targets` set to dedupe `k` by value (added after TLE on
all zeros). 2.5× slower than canonical on 3000 random ints (0.67s vs 0.26s), mostly
tuple sorting and hashing. Also had a bug of breaking the inner loop at the first
match: one `k` can have many pairs.

**Missed insight:** start `i` at `k + 1`. Sorting means you can fix the smallest
element, which makes each triplet reachable exactly once and turns dedupe into
adjacent-value skips instead of a set. Both extra sets disappear. Chased a linear
solution first; recognize the problem class instead.

**Next re-solve:** 2026-09-30 (canonical form cold; place the two duplicate skips
without testing; say why linear isn't on the table).
