# Product of Array Except Self

LeetCode 238 · https://leetcode.com/problems/product-of-array-except-self/ · solved 2026-09-06

**Pattern:** prefix/suffix decomposition. "f(everything except i)" with f associative
(product, sum, max, min) = f(left of i) · f(right of i), each a prefix scan. Same move
as Trapping Rain Water (max) and range-sum queries (sum). "No division" is the hint
pointing here; division breaks on zeros anyway.

**Solution as written:** two arrays of running products, O(n) time, O(n) extra.
Follow-up (O(1) extra, output not counted): write prefixes into the output array,
then sweep right-to-left multiplying by a running suffix scalar. Coded 2026-09-06 after
a hint, correct, but with offsets (`range(1, n)`, `nums[idx-1]`, `range(n-2, -1, -1)`).

**Missed insight:** built the suffix array in reverse orientation (entry k = product
of last k) and then indexed it from the end, so the combine step mixed "position i"
with "k-th from the end". Keep both arrays position-aligned: `prefix[i]` =
product of `nums[:i]`, `suffix[i]` = product of `nums[i+1:]`, fill suffix with
`range(n-1, -1, -1)`, answer is `prefix[i] * suffix[i]`. Rule: when two arrays get
combined, index them by the same thing. Took a few minutes to find the pattern;
trigger phrase to learn is "except self / excluding i".

Off-by-one habit: the offsets came from update-then-use. Use the running value at
`i` first, then fold `nums[i]` in; both loops run over the full range with no `±1`.
Invariant: at the top of iteration i, `pref == prod(nums[:i])`. `reversed(range(n))`
over the three-arg range. Trigger to check: any `range(1, n)` / `range(n-2, -1, -1)` /
`idx ± 1` inside a loop.

Say aloud: Python ints don't overflow, Go/Java would; problem guarantees 32-bit fit.

**Next re-solve:** 2026-09-13 (O(1)-extra two-pass version cold with use-then-update ordering
and no offsets; name the pattern before writing code).
