# Container With Most Water

LeetCode 11 · https://leetcode.com/problems/container-with-most-water/ · solved 2026-09-11

**What I wrote:** sort bars by height, walk from tallest down, track the leftmost and
rightmost index seen so far; for the current (shorter) bar the best partner among
taller bars is the furthest one. Correct on 20k random tests incl. ties and zeros.
O(n log n) from the sort, O(n) extra. Not two pointers, but the same dominance idea
("the shorter bar sets the height, so pair it with the widest taller partner").

**Intended O(n) pattern:** two pointers from the ends (max width). Each step the
width shrinks by one, so the only way a later pair beats the current one is a taller
minimum. _Pending: which of the two bars can be discarded without losing any better
candidate, and why?_

**Missed insight:** reached for sorting to organize by height when position-based
elimination does it in one pass. Also: comment said width `j - i + 1` (code used
`j - i`, correct); shadowed the `height` parameter with the loop variable (works only
because `n` was read first; a bug waiting for a refactor).

**Next re-solve:** 2026-09-18 (two-pointer version cold; state the elimination
sentence first).
