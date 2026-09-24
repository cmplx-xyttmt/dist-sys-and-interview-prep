# Kth Smallest Element in a Sorted Matrix

LeetCode 378 · https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/ · solved 2026-09-24

Not in the NeetCode 150 queue. It came from Repovive's Logarithms section
(maths leg (b)), and it is the cleanest statement of the binary-search-on-the-answer
pattern I have hit, so it lives here for the Binary Search group.

**The pattern:** binary search over the *value*, not over an index. The matrix has
no index arithmetic that gives a rank, so rank comes from counting:
`count(x)` = how many entries are ≤ x. Then the answer is the smallest `x` with
`count(x) >= k`.

**Wrong first attempt (a whole session):** assumed `matrix[i][j]` has rank
`i * cols + j + 1`, i.e. that reading the matrix row by row gives sorted order.
Rows sorted and columns sorted is weaker than that. `[[1,5],[2,9]]` flattens to
1, 5, 2, 9; the 2nd smallest is 2, at row-major index 3. Every off-by-one after
that was unfixable because the invariant did not exist. Same failure as Trapping
Rain Water: built an algorithm on an unchecked formula. Check the formula on a
2x2 before writing the loop.

**The binary search template that came out of it.** I only knew the form that
returns `low`, so I kept trying to bend problems into it. The general shape:

- A predicate `P(x)` that is monotone: F F F T T T along the number line. Here
  `P(x) = count(x) >= k`, monotone because `count` never decreases.
- Two sentinels you *know* the value of. `low = matrix[0][0] - 1` has count 0, so
  it is an F. `high = matrix[n-1][n-1]` has count n², so it is a T.
- Invariant: `low` is always an F, `high` is always a T. The loop only ever moves a
  pointer onto a value whose side it just tested, so the invariant holds.
- `while low < high - 1`, then return `high` for the first T or `low` for the last F.

Which end you return is the whole question, and getting it wrong is not an
off-by-one, it is the wrong predicate. On `[[1,5,9],[10,11,13],[12,13,15]]` with
k=8 both 13 and 14 have count 8, so `count(x) == k` does not pin a value.
`count(x) <= k` converges on the last F, 14, which is not in the matrix.
`count(x) >= k` converges on the first T, 13, which is the answer.

**Why the answer is always a matrix entry:** if `x` is not in the matrix then
`count(x) == count(x - 1)`, so `x - 1` satisfies the predicate too and `x` was not
the smallest. The first T therefore has to be a value that is present.

**What passed (2026-09-24):** `bisect_right` per row for the count, O(n log n) per
count, O(n log n log V) overall where V is the value range.

```python
low, high = matrix[0][0] - 1, matrix[n-1][n-1]
while low < high - 1:
    mid = (low + high) // 2
    if count(mid) >= k: high = mid
    else:               low = mid
return high
```

**Open: the O(n) count.** The passing version uses rows sorted and ignores columns
sorted. There is a staircase walk from the bottom-left corner that counts in O(n)
and brings the whole thing to O(n log V). Hint I was given and have not yet cashed:
standing at the bottom-left, if the entry is ≤ x you learn something about the whole
column above it, and if it is > x you learn something about the rest of that row.
Each step deletes a column or a row. Do not read the answer before trying it.

**Missed insight:** binary search is boundary-finding on a monotone predicate.
"Find the element" is one instance. Before coding, write the F/T row for a small
example and say out loud which end you want.

**Re-solve 2026-10-01:** from scratch, and the count must be the O(n) staircase.
