# Group Anagrams

LeetCode 49 · https://leetcode.com/problems/group-anagrams/ · solved 2026-09-05

**Pattern:** canonical key for equivalence classes. Map each item to a key that
all members of its class share, then bucket with `defaultdict(list)`.

**Keys:**
- `"".join(sorted(s))` — O(n log n) per word, works for any alphabet.
- 26-count tuple, index `ord(c) - ord('a')` — O(n) per word, but hashing costs
  26 regardless of word length, so it only wins on long words. Depends on the
  lowercase-only constraint; with Unicode fall back to sorting or a sorted
  tuple of `(char, count)` pairs.

**Missed insight:** stated the total as O(m + n log n). Sorting happens per
word, so it is O(m · n log n). Also called string hashing O(1); it is O(n),
dominated by the sort. Code was fine, the narration was not. Say the
complexity out loud as you build it: "m words, each costs X, so m · X."

**Next re-solve:** 2026-09-12 (focus: narrate complexity while coding, then
give both keys and the trade-off unprompted).
