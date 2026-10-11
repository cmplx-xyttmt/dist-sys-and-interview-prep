# Evaluate Reverse Polish Notation

LeetCode 150 · https://leetcode.com/problems/evaluate-reverse-polish-notation/ · solved 2026-10-11 (unaided, first try)

**Pattern:** stack of operands. A number is pushed; an operator pops two, applies,
pushes the result. Pop order is the only trap: the second pop is the left operand.
O(n) time and space. 20k random expression trees against a reference OK, including
every sign combination on division.

**What I wrote:** correct, including truncation toward zero on division (the
problem's rule; Python's `//` floors instead, so `-7 // 2` is `-4` where the
answer wants `-3`). The ceil-or-floor branch on the float quotient is five lines
for what `int(val1 / val2)` does in one: `int()` on a float truncates toward zero.
It goes through a float, which is exact here (operands stay within 32-bit range,
and a float holds any quotient of those to well past the integer part). The
integer-only form, if an interviewer objects to floats:
`q = abs(a) // abs(b); q if (a < 0) == (b < 0) else -q`.

The `if/elif` chain over four operators can be a dict of two-argument functions
(`operator.add`, `operator.sub`, `operator.mul`, and the `int(a / b)` lambda), so the
loop body becomes "pop two, look up, push". Same work, less to read.

**Missed insight:** none in the algorithm. Know what `int()` on a negative float
does before reaching for `math.ceil`.

**Next re-solve:** none (clean first-try solve; re-solves paused except first-fail
problems).
