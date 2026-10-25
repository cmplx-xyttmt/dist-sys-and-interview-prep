# Generate Parentheses

LeetCode 22 · https://leetcode.com/problems/generate-parentheses/ · solved 2026-10-13 (third attempt, unaided; enumerate-and-filter, backtracking version pending)

**Pattern:** backtracking with two counts. _Pending: write it, then fill this in._

**Attempt 1 (wrong):** build size n from size n-1 by three rules: wrap `(p)`,
prepend `()p`, append `p()`. Correct through n=3 (all 5), misses one at n=4:
`(())(())`, which is two non-trivial valid strings side by side, and none of the
three rules concatenates two of those. 34 of 42 at n=5. The build-from-smaller idea
can be completed, though. Every valid string starts with `(`; the `)` that matches it
splits the string into an inside part and an after part, both valid and smaller.
That decomposition is exhaustive, and it is the Catalan recurrence. Found it the
same day from the hint: for k in 0..n-1, `"(" + a + ")" + b` with `a` of size k and
`b` of size n-1-k, base case `gen(0) = [""]`. The match position is unique, so each
string appears for exactly one k and no set is needed. The three rules were k=n-1,
k=0, and one string of the general case.

**Attempt 2 and 3 (passed):** enumerate all 2^(2n) bit masks, keep the valid ones.
Validity is a counter: `+1` on `(`, `-1` on `)`, fail if it ever goes negative, pass
if it ends at zero. Attempt 3 checks the mask before building the string: 143 ms to
29 ms on LeetCode, beats 5%. O(4^n · n).

**Why it is slow:** almost every mask is rejected. At n=8, 65536 masks and 1430
valid (2.2%); the share shrinks as n grows, since the count of valid strings is
Catalan(n), about 4^n / n^1.5. The validity counter is also the whole answer
already: it rejects a mask the moment the count goes negative, then moves to the
next mask and re-walks the same prefix. _Pending: apply the counter while building,
not after, so a prefix is extended only when the next character keeps it valid._

**Missed insight:** _pending the backtracking attempt._

**Next re-solve:** owed, no date (backtracking version cold; say the two counts and the
two conditions before coding).
