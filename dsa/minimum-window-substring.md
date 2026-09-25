# Minimum Window Substring

LeetCode 76 · https://leetcode.com/problems/minimum-window-substring/ · solved 2026-09-25 (third attempt, unaided)

**Pattern:** variable-size sliding window, right-driven, shrink while valid. Add
`s[right]` unconditionally; while the window covers `t`, record it and drop `s[left]`.
Validity is monotone: a superset of a valid window is valid, so once `[left, right]`
is valid every larger `right` is too, and the smallest window ending at `right` is
found by shrinking from the left. O(52 · 2n) with a 52-slot compare.

**Attempt 1 (wrong):** both pointers at the ends, shrink whichever end has more
surplus. Greedy from the outside throws away windows it can never get back.
`ABXXBA`, `t=AB`: equal surplus at both ends, shrink both, then both again, returns
`X`. A one-minute paper trace on six characters would have killed it before coding.

**Attempt 2 (wrong):** left-driven: for each `left` that is in `t`, extend `right`
until valid. The `right` updates were the mess: `right = left if right == 0 or
right < left else right + 1` is recomputing what `right` *means* every iteration
(inclusive? exclusive? reset?), and `if right >= len(s): right = len(s) - 1` clamps
where it should `break` (once `right` runs off the end no later `left` can be valid).
Debug `print` left in, fourth time. Left-driven is not wrong, it just needs two
decisions right-driven never asks for. The clean version:

```python
right = 0                      # window is [left, right), exclusive
for left in range(n):
    while right < n and not valid():
        add(s[right]); right += 1
    if not valid(): break      # exhausted: nothing later can be valid
    record(right - left)
    remove(s[left])
```

**Attempt 3 (passed):** right-driven. Same shape as Longest Substring Without
Repeating and Character Replacement, with the inner condition flipped (shrink
*while valid* because we want the minimum, not while invalid).

**Bug, in all three:** `ord(c) - ord('a')` with 52 slots. `ord('A') - ord('a')` is
-32, and Python wraps negative indexes, so `A`..`F` land on the slots for `u`..`z`
and `G`..`Z` on 26..45. `s="u", t="A"` returns `"u"`. LeetCode's tests happen not
to mix those letters. Use `[0] * 128` indexed by `ord(c)`, or a dict. Fifty-two was
the right size and the wrong map; check the index formula on one uppercase letter.

**Missed insight (the question I asked):** how to know which pointer leads before
coding. Answer: write the invariant first, one sentence, then pick the pointer whose
unconditional step *cannot break it*. Here the invariant is "every character up to
`right` has entered the window once, and every valid window ending at `right` has
been recorded". Adding `s[right]` only moves the window toward valid, so the outer
loop never repairs anything; the inner `while` does, and it has one exit. Leading
with `left`, the unconditional step (drop `s[left]`) moves *away* from valid, so
every iteration starts by repairing, and repair has two exits (became valid, ran
out), which is exactly where the clamp bug came from. Rule: the `for` loop goes over
the pointer that adds; the `while` loop belongs to the pointer that repairs. Same
rule in all three window problems so far. Second: trace attempt 1 on paper before
coding it.

**Refinement (the standard follow-up):** replace the 52-way `is_valid` with a
`have`/`need` pair: `need` is the number of distinct letters in `t`, `have` counts
how many of those currently have `occ_s >= occ_t`. Update `have` only when a letter's
count crosses its target (on add, `occ_s == occ_t` after; on remove, `occ_s ==
occ_t - 1` after). Valid when `have == need`. Same trick as the `matches` counter in
Permutation in String. True O(n).

**Next re-solve:** 2026-10-02 (128-slot or dict; say the invariant sentence before
writing the loop; then the `have`/`need` version).
