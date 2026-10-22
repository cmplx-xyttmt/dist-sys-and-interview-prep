# Arithmetic Slices

LeetCode 413 · https://leetcode.com/problems/arithmetic-slices/ · solved 2026-10-22

Not in the NeetCode 150 queue. It came from Repovive, like
[Kth Smallest Element in a Sorted Matrix](./kth-smallest-element-in-a-sorted-matrix.md).
Kept for the complexity argument, which is the first charging argument on this track.

**What he wrote, unaided, correct:** for each start index i, the maximal run of equal
differences beginning at i ends at `end_idx`, and it contains `end_idx - i - 1` slices
(run length minus two). The saving is that the run from i + 1 inside a known run ends at
the same `end_idx`, so the inner scan only re-runs once the cached run is used up.
Checked against a brute force on 20,000 random arrays, no mismatches.

**The complexity, which was his question.** Measured first: the inner loop does 1000
comparisons on `range(1000)`, 1150 on 1000 random values, 4597 at n = 4000. Linear. The
argument:

> Let p₁ < p₂ < ... < p_m be the iterations where the inner `while` runs, and let e_t be
> the `end_idx` it computes at p_t. That scan costs `e_t - p_t + 1` comparisons. An
> iteration i takes the cheap branch exactly when `end_idx > i + 1`, so the next scan is
> at `p_{t+1} = max(p_t + 1, e_t - 1)`, hence `e_t <= p_{t+1} + 1` and
> `cost_t <= (p_{t+1} - p_t) + 2`. Summing, the first part telescopes to at most n and
> the second is at most 2n.

His own sentence for it was "if the branch with the while loop goes on for too long, those
intermediate values won't enter that branch until the end", which is right and is exactly
the inequality `e_t <= p_{t+1} + 1`. What he could not do was put it in a frame.

**The frame, worth keeping:** when work is spread unevenly across iterations, don't bound
each iteration. Give the expensive ones an index, bound the *gap* between consecutive ones,
and let the sum telescope. Nearly every amortized argument has this shape.

**Indexing cleanups (his own words: "I think I can make the indexing cleaner").**

- `ad` was declared beside `end_idx` as if it were carried across iterations. It is written
  and read inside the same `else` body, so it is a local. The only state is `end_idx`.
- `end_idx = 0` works by accident: at i = 0 the test `0 > 1` is false, so it rescans. But 0
  is a real index, so the sentinel is lying. `-1` means "no run known".
- `seqs += (end_idx - i - 1)` appeared in both branches. The branch is only about whether
  the cached run is still usable, so the addition hoists out.
- `if i + 1 < len(nums)` is a loop bound in disguise. No slice starts at the last two
  indices.

```python
n = len(nums)
end = -1          # last index of the known run; -1 = none yet
total = 0
for i in range(n - 2):
    if end < i + 2:                        # the cached run doesn't reach i+2
        diff = nums[i + 1] - nums[i]
        end = i + 1
        while end + 1 < n and nums[end + 1] - nums[end] == diff:
            end += 1
    total += end - i - 1                   # run length (end - i + 1), minus 2
return total
```

**Two shapes that need no amortized argument.** Both tested against brute force on 30,000
random arrays.

Count by where a slice *ends* rather than where it starts. If `cur` slices end at i - 1,
then `cur + 1` end at i when the difference holds, and 0 when it breaks:

```python
total = cur = 0
for i in range(2, len(nums)):
    if nums[i] - nums[i-1] == nums[i-1] - nums[i-2]:
        cur += 1
        total += cur
    else:
        cur = 0
return total
```

Or walk the maximal runs and use the closed form. A run of length L holds
`k(k + 1) / 2` slices with `k = L - 2`, because it has k slices of length 3, k - 1 of
length 4, and so on. This is the version in the Repovive solution, which Isaac read before
finding it himself. One subtlety: consecutive maximal runs *share* their boundary element,
so the outer loop restarts at j rather than j + 1.

**Missed insight:** needing an amortized argument to explain the running time is a signal
that the shape is more complicated than the problem needs. Both simpler versions touch each
index once, so there is nothing to prove. Ask "what if I count by the other end" before
settling on a shape.

**Re-solve:** none for now (re-solves paused 2026-10-09, and this one passed unaided on the
first attempt). If they resume: write the per-run closed-form version from scratch, since
that one was read rather than found.
