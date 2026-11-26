# Find Minimum in Rotated Sorted Array

LeetCode 153 · https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/ · solved 2026-11-26 (one hint)

**Pattern:** boundary template with a predicate you have to invent. A rotated array is two
sorted runs, and every value in the second run is smaller than every value in the first.
Compare each element with a fixed reference element so that the first run answers F and the
second answers T. The minimum is the first T. O(log n). 24k random rotations (n = 1..8,
including no rotation) against `min` OK.

**The hint:** "what can you compare `nums[mid]` against so that every index answers F or T,
F's first?" On the first attempt (late October) there was no way in; the hint was enough.

**What I wrote:** predicate `nums[i] < nums[0]`. `left = 0` is a real index that is always F
(nothing is smaller than itself), so it works as a sentinel without -1. `right = n`. When the
array isn't rotated, every index is F, `right` stays at n, and the special case returns
`nums[0]`. Correct, and the special case was found before coding, not after a failed test.

**Open, hinted:** is there a reference element that guarantees at least one T, so the
special case disappears? Tried the second element first (it can sit in either run), then
guessed the last element with `<=`, which is right: it is always in the minimum's run. Not
coded yet; left for the re-solve.

**Missed insight:** when there's no target value, build the predicate from an element you
already know the position of. The F/T table drawn on one example is how to find it.

**Next re-solve:** owed (code; find the predicate cold, then the version with no special case).
