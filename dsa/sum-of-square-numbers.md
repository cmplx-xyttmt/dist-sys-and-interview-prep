# Sum of Square Numbers

LeetCode 633 · https://leetcode.com/problems/sum-of-square-numbers/ · solved 2026-10-22

Not in the NeetCode 150 queue. Third note in a row built on the monotone-boundary idea,
after [Kth Smallest Element in a Sorted Matrix](./kth-smallest-element-in-a-sorted-matrix.md)
and [Arithmetic Slices](./arithmetic-slices.md).

**What he wrote, unaided, correct:** scan a from 0 while a² <= c, and binary search for an
integer square root of c - a². The binary search reuses the boundary template from the
kth-smallest note. `low = 0` satisfies `low² <= num`, `hi = num + 1` satisfies `hi² > num`,
and it returns the last value on the low side. Cost O(√c log c).

**Timings.** Worst case is c = 2147483647, the top of the constraint, prime and ≡ 3 (mod 4),
so every a is tried and the answer is False:

```
binary search per candidate   102 ms
same loop with math.isqrt     4.2 ms
two pointers                  2.6 ms
Fermat (factor c)             1.6 ms
```

All four agree on c = 0 through 2999, the `c = 0` and `c = 1` edges included.

**1. Drop the log.** `r = math.isqrt(x); r * r == x` answers "is x a perfect square" in place
of the inner binary search. Same O(√c) outer loop, 24x faster on the worst case. The binary
search was never wrong, it was just a per-candidate O(log c) that the library does better.

**2. Two pointers, O(√c), no squareness test at all.**

```python
a, b = 0, math.isqrt(c)
while a <= b:
    s = a * a + b * b
    if s == c:  return True
    if s < c:   a += 1
    else:       b -= 1
return False
```

It works because `a² + b²` rises with a and falls as b drops, so each comparison eliminates
a whole row or column of the pair space. Same elimination argument as Two Sum II and
Container With Most Water, over pairs of squares instead of array indices. This is the
interview answer.

**3. Fermat's two-square theorem.** c is a sum of two squares exactly when every prime
p ≡ 3 (mod 4) in its factorization appears to an even power. Trial divide; the moment a
3-mod-4 prime has an odd exponent, return False; at the end check whatever is left of n.

Not asymptotically better. A prime c still forces trial division to √c, the same √c the
two-pointer walks. What makes it fast in practice is that dividing out factors shrinks n as
you go, so most inputs die early. On 2147418113 = 32767² + 32768², the two-pointer took
0.56 ms and Fermat 0.22 ms.

**Missed insight:** reaching for a hand-written binary search where the question is "is this
a perfect square". The inner search was the only log factor in the solution, and the outer
loop already knew enough to avoid asking the question at all.

**Re-solve 2026-10-29 (code).** Isaac's call on 2026-10-22, an exception to the re-solve
pause of 2026-10-09. Write all three from scratch: the isqrt scan, the two-pointer, and
Fermat. State which is asymptotically better and which is faster in practice, and why those
are different answers.
