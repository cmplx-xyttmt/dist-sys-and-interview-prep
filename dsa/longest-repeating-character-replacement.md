# Longest Repeating Character Replacement

LeetCode 424 · https://leetcode.com/problems/longest-repeating-character-replacement/ · solved 2026-09-20 (hint needed)

**Pattern:** sliding window with a 26-count summary. Window `[l, r]` is valid when
`(r - l + 1) - max(count) <= k`: change everything to the most common letter, which
needs the fewest replacements. Rescanning 26 counts for the max is O(26) per step, so
O(26n) = O(n). Accepted as is.

**What I wrote:** left-driven again (for `i`, extend `j`), which forced an
add-check-undo dance: add `s[j]`, test, and if invalid subtract it back and break.
Right-driven has no undo: add `s[r]`, `while invalid: remove s[l]; l += 1`, record.
Debug `print` left in a third time. Right-driven rewrite done the same day, and it
came out as the *sliding* form: on invalid, drop one from the left and move on, no
inner while. The window is then allowed to stay invalid while it slides
(`AABBBAA`, k=1: at j=6 the window `BBAA` slides and is still invalid). That is fine
because sizes only grow through valid states, so `best` is never inflated, and a
window of that size was already recorded. Same total work as the shrink-until-valid
form (n adds, at most n removals), simpler control flow, and one step from the O(n)
version: replace `max(occ)` with a running max that never decreases.

**Missed insight:** couldn't see what the window was or how to escape O(n²). The
window's contents are summarized by a fixed-size count array, and the "max" is over
26 slots, not n. Hint needed to get started. When a problem says "characters", ask
what the alphabet size is before deciding anything is O(n) per step.

**Refinement (the famous part):** `max_count` never needs to decrease. Answer is the
largest window size ever valid, and a window is at the frontier of size
`max_count + k`; a later window whose true max is lower cannot be longer than one
already recorded. So keep a running max, never rescan, and the window slides instead
of shrinking. _Pending: state that argument in your own words._

**Next re-solve:** 2026-09-27 (right-driven, no undo, no print; then the
never-decrease version and the sentence that justifies it).
