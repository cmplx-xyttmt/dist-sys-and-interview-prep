# Daily Temperatures

LeetCode 739 · https://leetcode.com/problems/daily-temperatures/ · solved 2026-10-14 (unaided, first try)

**Pattern:** monotonic stack, scanned right to left. The stack holds days still
waiting to be someone's "next warmer day", strictly increasing in temperature from
top to bottom. For each day, pop everything at or below its temperature: those days
can never be the answer for any earlier day, because this day is closer and at least
as warm. The top after popping is the answer. Push, move on. Each day enters and
leaves the stack once, so O(n). 30k random tests against brute force OK; 100k days
in 16 ms.

**What I wrote:** correct and first try. The `<=` is the right comparison (an equal
temperature is not "warmer", so it must be popped). Two small shapes to know. Storing
`(day, temp)` pairs is fine; storing just the index and reading `temperatures[i]`
is the common form and halves the tuple traffic. Preallocating `answer = [0] * n`
and writing `answer[day] = ...` removes the append-then-reverse.

**The forward version, to have ready:** scan left to right, stack of unresolved
days. When a warmer day arrives, pop every stack day colder than it and write their
answers (`today - that_day`). Same O(n), same invariant, resolved on arrival instead
of looked up on departure. Right-to-left answers each day at the moment it is
visited; left-to-right answers each day when its warmer day shows up. Pick by which
is easier to state for the problem at hand.

**Missed insight:** none. Third sighting of "a newer, larger element makes older,
smaller ones dead" (Trapping Rain Water walls, Sliding Window Maximum deque), applied
without a hint.

**Next re-solve:** none (clean first-try solve; re-solves paused except first-fail
problems).
