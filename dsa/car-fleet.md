# Car Fleet

LeetCode 853 · https://leetcode.com/problems/car-fleet/ · solved 2026-10-17 (unaided, first try)

**Pattern:** sort by position, sweep from the car nearest the target, track the
arrival time of the current fleet's leader. A car that would arrive strictly later
than that leader cannot catch it, so it starts a new fleet and becomes the leader.
A car that would arrive at the same time or earlier catches up and merges, and the
fleet keeps the leader's time. O(n log n) for the sort, O(n) after.
30k random tests against an exact-fraction reference OK.

**What I wrote:** correct, first try, and one detail better than the usual
solution: the comparison `(target - p1) * s2 > (target - p2) * s1` is the time
comparison cross-multiplied, so there is no float. Both sides are positive (every
car is before the target, every speed is positive), so the inequality keeps its
direction. Strict `>` is right: equal arrival time is the same fleet.

**On the stack:** the textbook version pushes each new leader's time on a stack and
answers with the stack's size. The stack never pops, because the sweep is in
position order and a merging car just doesn't push. An append-only stack that is
only read at the top is one variable plus a counter, which is what I wrote. The
"monotonic stack" framing is for seeing the problem; it isn't needed in the code.

**On O(n):** the sort is the only step above linear, and it is over positions,
which are distinct integers below `target` (at most 10^6). A bucket by position
makes it O(n + target). Comparison sorting is Θ(n log n); sorting bounded integer
keys is not. In an interview O(n log n) is the expected answer, and the bucket is
the follow-up to offer, not to lead with.

**Missed insight:** none in the solution. The one to carry: "sort, then sweep from
one end comparing only to the current group's representative" is the same shape as
merging intervals, which comes later in the list.

**Next re-solve:** none (clean first-try solve; re-solves paused except first-fail
problems).
