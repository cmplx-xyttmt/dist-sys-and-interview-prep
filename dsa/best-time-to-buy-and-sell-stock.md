# Best Time to Buy and Sell Stock

LeetCode 121 · https://leetcode.com/problems/best-time-to-buy-and-sell-stock/ · solved 2026-09-13

**Pattern:** running minimum. Profit at day i uses the min of everything before i,
then the min absorbs day i (use-then-update). O(n), O(1). Solved clean, first try.

**Sliding window, defined:** contiguous `[l, r]`; `r` advances every step, `l`
advances only when the window becomes invalid, neither moves backward. Each element
enters once and leaves once, so O(n). Here it is degenerate: `l` = buy day, `r` = sell
day, and when `prices[r] < prices[l]` the left edge jumps to `r`, so `l` collapses to
"best buy so far" and no index is needed. Real windows with contents start at
Longest Substring Without Repeating Characters.

**Missed insight:** none in the code. Didn't know what sliding window meant; see above.

**Next re-solve:** 2026-09-27 (low priority).
