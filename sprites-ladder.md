# The Sprites ladder

_The ladder now lives as an interactive guide: `sprites-guide/index.html` (open it; the sidebar
tracks which rungs are passed, every reading and mission step has a checkbox, and the map page
says which rung each section of the explainer needs). This file is the short, plain-text version
for planning: what the ladder is, how it maps onto the calendar, and what the standup has to decide.
Rewritten Fri Sep 18, 2026, 06:30, after the first draft used labels Isaac had never seen._

## The words, spelled out first

- **The explainer** is `dist-sys-interview-prep/sprites-guide/explainer.html` (the old path
  `sprites-explainer.html` redirects there), the page written Sep 6 about how Fly.io built Sprites. It has ten numbered sections; "section 04" means that page's
  section 04, "The storage stack".
- **The three design bets** are the three items in the explainer's section 03: (1) kill the
  container image, (2) object storage is the source of truth, (3) inside-out orchestration.
- **The Sunday session queue** is section 5 of `dist-sys-interview-prep/ROADMAP.md`, "The two
  queues": the ordered list of system-design sessions S0, S1, S2 and so on, alternating a design
  note (type A) with a Gossip Glomers challenge (type B). An earlier draft of this file called it
  "the S-queue's A/B alternation"; it means that list and that alternation.
- **Gossip Glomers** are Fly.io's distributed-systems challenges (fly.io/dist-sys); **Maelstrom**
  is the test harness they run on.
- **A mission** is a task with a check at the end you can't pass without the material, as defined in
  `curriculum-edtech/learning-through-code-and-maths.md`. That document sizes them at 20 to 40 minutes
  for reading checkpoints; the ladder's missions are 1 to 2 hours each.
- **The showcase project** is `curriculum-edtech/course-from-a-link-on-sprites.md`.

## Why the explainer didn't land

Its section 04 uses fifteen ideas in six paragraphs (block device, filesystem, NVMe, read-through
cache, dm-cache, immutability, content addressing, object storage, S3, SQLite, write-ahead log, log
shipping, metadata versus data, JuiceFS, GFS) without building any of them up. They stack, and the
explainer starts at the top. The fix is to climb the stack, one rung a week, with a mission at each,
then read the explainer again.

## The nine rungs

| Rung | Title | Mission's check |
|---|---|---|
| L0 | A computer from the inside (process, filesystem vs block device, container vs virtual machine, container image) | Two docker timings, prediction within 3x, five lines on what a container shares with the host |
| L1 | Bytes, files, and why the log comes first (SQLite, write-ahead log) | A 60-line key-value store killed three ways: buffered loses acknowledged keys, flushed loses nothing, fsync changes nothing under `kill -9` but you can say which crash it is for |
| L2 | Hashing, immutability, content addressing (git's object model, the JuiceFS data/metadata split) | A chunk store: byte-identical rebuild, one new chunk for a near-duplicate, a checkpoint of about 11 KB against 10 MB |
| L3 | Object storage, caches, and easy invalidation (S3 model, read-through cache) | The chunk store behind MinIO with a local cache: nothing lost when the cache is deleted, warm read 10x faster |
| L4 | Replication by shipping a log (Litestream) | SQLite replicated to MinIO, killed, deleted, restored, row count within one interval |
| L5 | Snapshots, copy-on-write, forking (overlay filesystems, Firecracker snapshots) | Three overlays over one unchanged lower directory; fork added to the chunk store |
| L6 | Gossip, membership, service discovery (Gossip Glomers broadcast, Corrosion) | Maelstrom passes echo, broadcast 3a and 3b; 3c under partitions is the second-week stretch |
| L7 | Capabilities, not credentials (token broker, Sprites Connectors) | A proxy that injects the key; the agent behind it cannot read the key |
| L8 | Read it again, then the sources | Quiz score recorded; the storage stack explained from memory in one paragraph |

Each rung's readings, steps, hints and explainer links are on its page in `sprites-guide/`.

## Calendar

One rung a week: the reading in the Thursday 19:30 slot (the season's reading half), the mission the
following Tuesday 19:30 (the build half). Season 2: L0 (read Thu Sep 24, mission Tue Sep 29), L1 (read
Oct 1, mission Oct 6), L2 (read Oct 8; its mission is season 3's first Tuesday, Oct 13). Tue Sep 22 has
no Thursday before it, so it takes the roadmap's S1 (Maelstrom install plus Echo, about an hour), which
rung L6 needs later. L3 to L8 are season 3, L6 taking two weeks. Proposed "shipped" for the
system-design bet this season: L0 and L1 passed with missions logged, L2 read, two posts published, the
explainer re-read at the Oct 11 wrap with the quiz score recorded as the baseline for L8.

## The explainer's projects, reviewed

Four of its five projects kept and placed on rungs (drive a Sprite by hand goes into the showcase's
first phase; the chunk store is L2; Litestream is L4; Glomers broadcast plus Corrosion is L6). The
fifth, a design document for the lead-identification harness at Tunga, is replaced by the showcase
project because a work design can't be published. Four missions added: L0, L3, L5, L7.

## Publishing

Series "What I had to learn to understand Sprites" on `~/Projects/cmplx-xyttmt.github.io` (Hugo;
posts in `content/posts/`), one post per rung, written the same week in at most 60 minutes, per
section 8 of the dist-sys roadmap. The showcase project gets one post per phase.

## For the Fri Sep 18 standup

1. Pause the Sunday session queue for the ladder, L0's reading on Thu Sep 24 and its mission on Tue Sep 29?
2. Give Tue Sep 22 to S1 (Maelstrom install plus Echo), so rung L6 has no set-up cost later?
3. Adopt the "shipped" sentence above for the system-design bet?
