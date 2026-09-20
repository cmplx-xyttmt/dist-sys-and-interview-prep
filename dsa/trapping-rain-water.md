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

**Two-pointer O(1)-extra version (coded 2026-09-13 after a hint):** at the left
pointer the left max is exact and the right max is only a lower bound (running max
from the right end). If `max_left <= max_right` that bound is enough: the true right
max is at least `max_right >= max_left`, so `min(L, R) = max_left` exactly and the
left position is settled. Symmetric on the other side. The reusable idea: a bound is
as good as the exact value when it can't change the min. 50k random tests OK.
My version accounted for the current position then moved, which forced a
`left == right` special case and two non-exclusive `if`s. Standard shape: `while l < r`,
pick the side, move the pointer first, then update that side's max and add its water;
ends 0 and n-1 hold nothing, so no special case.

**Missed insight:** wrote the water formula wrong (nearest taller vs highest) and built
an algorithm on it. Verify the per-position formula on a 5-element example before
designing anything. Second: an hour of debugging with no reference implementation;
write the O(n)-space version first and test against it.

**Re-solve 2026-09-20: DNF** (late, tired). Compared `height[left]` to
`height[right]` to pick the side, and updated the *other* side's max. The decision
has to be about the running maxes: the side whose max is smaller is the side whose
water is already determined, because the other side's max is a lower bound that
can't drop the min. Self-diagnosed the miss.

**Next re-solve:** 2026-09-24 (rested; formula first, then say "which side's max is
smaller, and why does that settle it?" before writing the branch).
