# Valid Sudoku

LeetCode 36 · https://leetcode.com/problems/valid-sudoku/ · solved 2026-09-08

**Pattern:** hash sets per constraint. One pass over the grid; for each filled cell,
check-then-add against its row set, column set, and box set. The only idea in the
problem is the box key: `(r // 3, c // 3)` says which third of the grid in each axis.

**Complexity:** 81 cells, constant work each: O(1) for the fixed board, O(n²) for n×n.
Space: 27 sets of ≤ 9.

**Missed insight:** wrote the box key as `(r - r % 3, c - c % 3)` (the box's corner),
which works but `r // 3` is the direct form and the one to have in your fingers for
any "which bucket does this coordinate fall in" grid problem. Also converted digits
with `int()` for no reason (strings are already hashable) and left an `else:` after a
`continue`.

Variant to know: one seen-set of tagged tuples `('r', r, ch)`, `('c', c, ch)`,
`('b', r//3, c//3, ch)`. Shorter, same cost, less readable than three named sets.

**Next re-solve:** 2026-09-22 (low priority; solved cleanly first try).
