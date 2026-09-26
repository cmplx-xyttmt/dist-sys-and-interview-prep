# Permutation in String

LeetCode 567 · https://leetcode.com/problems/permutation-in-string/ · solved 2026-09-21 (unaided)

**Pattern:** fixed-size sliding window compared by a 26-count summary. Two count
arrays: one for `s1`, one for the current window of `s2`. A window is a permutation
when the arrays are equal. Comparing costs O(26) per step, so O(26n) = O(n).
Right-driven, no undo (the shape from Character Replacement, applied unprompted).
Passes 20k random tests against brute force.

**What I wrote:** tracked `i` by hand and shrank with `elif j - i + 2 > len(s1)`.
The `+2` is a disguised `>=`: `j - i + 2 > n` is `j - i + 1 >= n`, and since the
window never grows past `n`, that is just "the window is full". The first draft had
`+1` and shrank one step late, because the check runs before `j` advances. Correct,
but a reader has to do that algebra to trust it.

**Missed insight:** the window size is fixed, so `i` is not a variable, it is
`j - n + 1`. Once `j >= n`, drop `s2[j - n]` and there is nothing to track. The
26-way check is also just list equality:

```python
for j, ch in enumerate(s2):
    occ[ord(ch) - orda] += 1
    if j >= n:
        occ[ord(s2[j - n]) - orda] -= 1
    if occ == occ_s1:
        return True
```

Note `occ == occ_s1` can only be true when the window holds `n` letters, so the
size check disappears too. In general: fixed-size window means "remove the element
`n` back", never a left pointer. A left pointer is for windows whose size varies.

**Refinement (optional):** replace the O(26) compare with a `matches` counter, the
number of the 26 slots where `occ[k] == occ_s1[k]`. Each add or remove touches one
slot, so update `matches` in O(1) by checking that slot before and after. Answer
when `matches == 26`. True O(n) instead of O(26n). Worth knowing the shape, not
worth reaching for in an interview unless asked.

**Next re-solve:** 2026-09-27, talk-through only (no left pointer, list equality; then say why the
size check is redundant).
