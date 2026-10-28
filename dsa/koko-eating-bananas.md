# Koko Eating Bananas

LeetCode 875 · https://leetcode.com/problems/koko-eating-bananas/ · solved 2026-10-28

**Pattern:** binary search on the answer. The predicate "speed k finishes in h hours" is
F...FT...T over k, because eating faster never takes longer. Sentinels: `left = 0` (never
evaluated, so no division by zero) and `right = max(piles)` (a known T: one hour per pile,
and the problem promises `h >= len(piles)`). Return `right`, the first T. O(n log max).
20k random cases against a brute force that tries k = 1, 2, 3... OK; 10k piles of up to
1e9 in 10 ms.

**What I wrote:** correct and first try, with the invariant written first. Third time in a
row the boundary template came back on its own, and the first time on a search over
answers rather than positions (the Kth Smallest idea, unaided). Small things:

- The comment says `k < left` takes more than h hours. `left` itself is also an F (it only
  ever gets an F assigned), so it's `k <= left`. The off-by-one is in the comment, not the code.
- Why is `left = 0` safe to divide by? It never is divided by: inside the loop `mid > left
  >= 0`. Be ready to say that, because "what about k = 0?" is the obvious interviewer question.
- `math.ceil(p / k)` goes through a float. It's exact at these sizes (0 mismatches in 200k
  random pairs up to 1e9), but `(p + k - 1) // k` or `-(-p // k)` is integer-only and needs
  no argument.
- `time_to_eat` can stop as soon as `time > h`. Same complexity, less work on slow speeds.

**Missed insight:** none.

**Next re-solve:** none (clean).
