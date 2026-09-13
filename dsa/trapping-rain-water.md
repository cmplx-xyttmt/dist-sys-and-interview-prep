# Trapping Rain Water

LeetCode 42 · https://leetcode.com/problems/trapping-rain-water/ · solved 2026-09-13

**The formula, and the whole problem:**
`water[i] = min(max(h[0..i]), max(h[i..n-1])) - h[i]`. The *highest* bar on each
side, not the nearest taller one. `[5,1,2,1,4]` at i=1: nearest-taller gives 1 unit,
truth is 3.

**Prefix/suffix version (what passed):** left-max and right-max arrays, use-then-update
ordering so both are exclusive maxes, clip with `max(0, ...)`. O(n) time, O(n) extra.
Same move as Product of Array Except Self with `max` for `*`.

**Wrong first attempt (an hour lost):** scan for the next wall ≥ current, fill the
segment with one `highest_right`. Fails whenever there is no closing wall (descending
tail after the peak: `[5,3,1]` got 2, want 0) because the right max differs per
position inside the segment. 4812/20000 random inputs wrong. The bounding-walls
instinct itself is sound; it is the monotonic-stack solution, which comes back in the
Stack group. It is not the two-pointer solution.

**Two-pointer O(1)-extra version:** _pending. Hint in play: at the left pointer you
know the left max exactly and only a lower bound on the right max (the running max
from the right end). When is a lower bound enough to pin down the min?_

**Missed insight:** wrote the water formula wrong (nearest taller vs highest) and built
an algorithm on it. Verify the per-position formula on a 5-element example before
designing anything. Second: an hour of debugging with no reference implementation;
write the O(n)-space version first and test against it.

**Next re-solve:** 2026-09-20 (state the formula first; array version cold; then the
two-pointer version with the lower-bound argument said aloud).
