# Encode and Decode Strings

LeetCode 271 (premium) · https://neetcode.io/problems/string-encode-and-decode · solved 2026-09-06

**Pattern:** length-prefix framing. `<len>,<body>` per string; the header tells the
decoder how far to skip, so the body may contain anything, including the separator.
Same idea as netstrings, Redis bulk strings (`$5\r\nhello\r\n`), Protobuf
length-delimited fields (DDIA ch 4).

**Alternatives and the trade-off:**
- escaping a delimiter — no header, but worst case doubles the payload and decode
  must inspect every char; length-prefix skips the body in O(1) per string.
- fixed-width header (4 digits / 4 raw bytes) — no separator, O(1) parse, wastes
  bytes on short strings, caps the length. Variable width + terminator is the varint trade.

Time O(N) both ways, N = total chars. Overhead per string = digits(len) + 1.
Edge cases to say aloud: `[]` → `""` → `[]`; `""` → `0,` → `""`.
Over a socket, count encoded bytes, not code points (`len("héllo")` is 5, UTF-8 is 6).

**Missed insight:** `for str in strs` shadowed the builtin. Decoder did digit
accumulation by hand and index arithmetic on one cursor; cleaner to name two
positions: `j = s.index(',', i)`, `length = int(s[i:j])`, body is
`s[j+1 : j+1+length]`, then `i = j+1+length`. `index` over `find` so malformed
input raises instead of slicing garbage.

**Next re-solve:** 2026-09-13 (write the `index`-based decoder cold; state the
escaping vs fixed-width vs length-prefix trade-off unprompted).
