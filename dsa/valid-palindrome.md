# Valid Palindrome

LeetCode 125 · https://leetcode.com/problems/valid-palindrome/ · solved 2026-09-09

**Pattern:** two pointers converging. Skeleton is `i, j = 0, n-1; while i < j: ...; i += 1; j -= 1`.
Every problem in this group is that loop with a different body.

**What I wrote:** filter to alphanumerics (`lower()` then list comp), then compare
from both ends with a `for i` plus a `j` counter and `break` on `i == j`.
O(n) time, O(n) extra for the filtered list.

**Missed insight:** stop condition `i == j` never fires on even lengths, so the
pointers cross and every pair is compared twice (`abba`: 4 comparisons for 2).
Correct output, wrong loop shape; `while i < j` is the invariant. Left a debug
`print(i, j)` in the submission. Used `isalpha` first (WA), had to look up `isalnum`.

**Follow-up:** skip non-alphanumerics with the pointers themselves, no filtered list:
O(1) extra. Each pointer moves at most n steps, so O(n). Watch where `lower()` goes
once you stop preprocessing.

**Next re-solve:** 2026-09-16 (in-place skipping version cold, `while i < j`,
no debug output left; say the pointer-moves-once argument before coding).
