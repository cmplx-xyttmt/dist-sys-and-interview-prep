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
| [Group Anagrams](./group-anagrams.md) | canonical key | 2026-09-05 | 2026-09-12 |
| [Top K Frequent Elements](./top-k-frequent-elements.md) | count, then select | 2026-09-05 | 2026-09-12 |
| [Encode and Decode Strings](./encode-and-decode-strings.md) | length-prefix framing | 2026-09-06 | 2026-09-13 |
| [Product of Array Except Self](./product-of-array-except-self.md) | prefix/suffix | 2026-09-06 | 2026-09-13 |
| [Valid Sudoku](./valid-sudoku.md) | hash sets per constraint | 2026-09-08 | 2026-09-22 |
| [Longest Consecutive Sequence](./longest-consecutive-sequence.md) | set + start-of-run test | 2026-09-08 | 2026-09-15 |
| [Valid Palindrome](./valid-palindrome.md) | two pointers | 2026-09-09 | 2026-09-16 |
| [Two Sum II](./two-sum-ii-input-array-is-sorted.md) | two pointers, sorted | 2026-09-10 | 2026-09-17 |
| [3Sum](./3sum.md) | sort + fix one + two pointers | 2026-09-11 | 2026-09-18 |
| [Container With Most Water](./container-with-most-water.md) | two pointers, elimination | 2026-09-11 | 2026-09-18 |
| [Trapping Rain Water](./trapping-rain-water.md) | prefix/suffix max, two pointers | 2026-09-13, re-solved 2026-09-23 | 2026-10-07 |
| [Best Time to Buy and Sell Stock](./best-time-to-buy-and-sell-stock.md) | running min | 2026-09-13 | 2026-09-27 |
| [Longest Substring Without Repeating Characters](./longest-substring-without-repeating-characters.md) | sliding window + set | 2026-09-15 | 2026-09-22 |
| [Longest Repeating Character Replacement](./longest-repeating-character-replacement.md) | sliding window + 26 counts | 2026-09-20 | 2026-09-27 |
| [Permutation in String](./permutation-in-string.md) | fixed-size sliding window + 26 counts | 2026-09-21 | 2026-09-28 |
| [Minimum Window Substring](./minimum-window-substring.md) | sliding window, shrink while valid | 2026-09-25 | 2026-10-02 |
| [Kth Smallest Element in a Sorted Matrix](./kth-smallest-element-in-a-sorted-matrix.md) (extra, from Repovive) | binary search on the answer + count predicate | 2026-09-24, with hints | 2026-10-01 (O(n) staircase count required) |
