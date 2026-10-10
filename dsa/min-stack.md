# Min Stack

LeetCode 155 · https://leetcode.com/problems/min-stack/ · solved 2026-10-10 (unaided, first try)

**Pattern:** a second stack holding the running minimum. The question to settle
before coding: when the current minimum is popped, what is the new minimum? It is
whatever was the minimum before that value was pushed, which is exactly the history
a stack keeps. Push to the min stack only when the new value is `<=` the current min;
pop from it only when the popped value equals its top. All four operations O(1).
5k random sessions with duplicate-heavy values OK.

**What I wrote:** the sparse form (min stack shorter than the main stack), which is
the better of the two. The `>=` on push is the part that makes duplicates safe: a
second copy of the minimum gets its own entry, so popping one copy leaves the other
on the min stack. With a strict `>` and an `==` on pop, pushing 1, 1 then popping
once would empty the min stack while a 1 is still inside. Worth saying out loud in
an interview, since it is the only thing that can go wrong here.

**Missed insight:** none. The one-line alternative to have ready: push `(value,
current_min)` pairs onto a single stack, no second structure and no equality test,
at the cost of one extra int per element.

**Next re-solve:** none (clean first-try solve; re-solves paused except first-fail
problems).
