# Longest Substring Without Repeating Characters

LeetCode 3 · https://leetcode.com/problems/longest-substring-without-repeating-characters/ · solved 2026-09-15

**Pattern:** sliding window with a set of window contents. Window is valid when no
char repeats. Each char enters once and leaves once, so O(n) despite the nested loop.
Correct on 30k random tests.

**What I wrote:** left-driven: for each `i`, extend `j` while `s[j]` is new, record
`j - i`, then remove `s[i]`. Valid. The canonical shape for this group is
right-driven: `for r: add s[r]; while window invalid: remove s[l]; l += 1; record`.
Learn the right-driven shape: Minimum Window Substring and Longest Repeating
Character Replacement don't fit the left-driven form as cleanly.

**Two ways to move `l` on a repeat, both O(n):**
- walk `l` forward removing chars until the duplicate is gone (what I wrote).
- jump: keep `last[c]` = last index of `c`; on repeat `l = max(l, last[c] + 1)`.
  The `max` matters: a stale `last[c]` left of `l` must not pull `l` backward.

**Missed insight:** `defaultdict(bool)` is a set with extra steps; use `set()` with
`add`, `remove`, `in`. `else:` after `break` is dead structure. Inner loop condenses
to `while j < n and s[j] not in seen: seen.add(s[j]); j += 1`.

**Next re-solve:** 2026-09-22 (right-driven shape cold with a set; then the
`last`-index jump version and say why the `max` is there).
