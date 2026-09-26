# DSA notes

One file per problem, named by LeetCode slug (matches `DSA_GROUPS` in
`roadmap.html`). Each note is terse: problem, pattern, the missed insight,
next re-solve date. Update the date here and in the note every re-solve.

Before the Binary Search group, read
[Kth Smallest Element in a Sorted Matrix](./kth-smallest-element-in-a-sorted-matrix.md):
it holds the monotone-predicate template (F...FT...T, two known sentinels, pick which
end you return) rather than the find-the-element form.

| Problem | Pattern | Solved | Next re-solve |
|---|---|---|---|
| [Group Anagrams](./group-anagrams.md) | canonical key | 2026-09-05 | 2026-09-26 (code, today) |
| [Top K Frequent Elements](./top-k-frequent-elements.md) | count, then select | 2026-09-05 | with the Heap / Priority Queue group |
| [Encode and Decode Strings](./encode-and-decode-strings.md) | length-prefix framing | 2026-09-06 | 2026-09-27 (talk-through) |
| [Product of Array Except Self](./product-of-array-except-self.md) | prefix/suffix | 2026-09-06 | 2026-10-03 (code) |
| [Valid Sudoku](./valid-sudoku.md) | hash sets per constraint | 2026-09-08 | dropped |
| [Longest Consecutive Sequence](./longest-consecutive-sequence.md) | set + start-of-run test | 2026-09-08 | 2026-09-29 (code) |
| [Valid Palindrome](./valid-palindrome.md) | two pointers | 2026-09-09 | 2026-09-27 (talk-through) |
| [Two Sum II](./two-sum-ii-input-array-is-sorted.md) | two pointers, sorted | 2026-09-10 | 2026-09-27 (talk-through) |
| [3Sum](./3sum.md) | sort + fix one + two pointers | 2026-09-11 | 2026-09-30 (code) |
| [Container With Most Water](./container-with-most-water.md) | two pointers, elimination | 2026-09-11 | 2026-09-28 (code) |
| [Trapping Rain Water](./trapping-rain-water.md) | prefix/suffix max, two pointers | 2026-09-13, re-solved 2026-09-23 | 2026-10-07 (code) |
| [Best Time to Buy and Sell Stock](./best-time-to-buy-and-sell-stock.md) | running min | 2026-09-13 | dropped |
| [Longest Substring Without Repeating Characters](./longest-substring-without-repeating-characters.md) | sliding window + set | 2026-09-15 | 2026-09-27 (talk-through) |
| [Longest Repeating Character Replacement](./longest-repeating-character-replacement.md) | sliding window + 26 counts | 2026-09-20 | 2026-09-27 (code) |
| [Permutation in String](./permutation-in-string.md) | fixed-size sliding window + 26 counts | 2026-09-21 | 2026-09-27 (talk-through) |
| [Minimum Window Substring](./minimum-window-substring.md) | sliding window, shrink while valid | 2026-09-25 | 2026-10-02 (code) |
| [Sliding Window Maximum](./sliding-window-maximum.md) | fixed window max, lazy-deletion heap (O(n) pending) | 2026-09-26 | 2026-10-03 (code) |
| [Kth Smallest Element in a Sorted Matrix](./kth-smallest-element-in-a-sorted-matrix.md) (extra, from Repovive) | binary search on the answer + count predicate | 2026-09-24, with hints | 2026-10-01 (O(n) staircase count required) |

**Re-solve policy (set 2026-09-26, Isaac's call).** The full list was overdue and
would have blocked new problems for a week, so it is split three ways. **Code** a
re-solve again only when a hint was needed, it took more than one attempt, or the
missed insight was in the algorithm; one a day next to the new problem; spacing one
week, then three, then done unless it fails. **Talk-through** (no code, ~5 min: say
the pattern, the invariant, the complexity, tick it) when the miss was narration, an
API detail, or cleanliness; the five booked for 2026-09-27 clear in one sitting.
**Dropped** when the first solve was clean with nothing to learn. Top K Frequent
Elements waits for the Heap / Priority Queue group, since the gap was the heap and
bucket versions. Long-term home for this schedule: the spaced-repetition side of
acu-2brain-cc, which is why the notes keep their fields (date, result, focus).

**Re-read, 2026-09-26 (rested):** the "Missed insight" section of [Minimum Window Substring](./minimum-window-substring.md), the rule for which pointer leads a sliding window. Then say it back in one sentence before the Longest Substring talk-through on 2026-09-27.
