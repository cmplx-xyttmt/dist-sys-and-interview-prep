# Valid Parentheses

LeetCode 20 · https://leetcode.com/problems/valid-parentheses/ · solved 2026-10-09 (unaided, first try)

**Pattern:** stack of unmatched openers. Push every opener; on a closer, the stack
top must be its partner, else fail. Valid at the end only if nothing is left open.
A map from closer to opener makes the partner test one lookup. O(n) time and space.
50k random tests against a cancel-pairs reference OK.

**What I wrote:** clean. One cosmetic: `return not bool(stack)` is `return not stack`;
an empty list is already falsy, and `not` on it returns a bool.

**Missed insight:** none. The two failure modes (closer with empty stack, closer with
the wrong top) and the end check (stack not empty) were all there first time.

**Next re-solve:** none (clean first-try solve; re-solves paused 2026-10-09 except for
problems that needed a hint or more than one attempt).
