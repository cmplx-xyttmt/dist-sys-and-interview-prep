#!/usr/bin/env python3
"""Generates the rung pages (l0-*.html ... l8-*.html), explainer-map.html and showcase.html (from
../../curriculum-edtech/course-from-a-link-on-sprites.md), and refreshes the rung links under each
section heading of explainer.html (which is otherwise hand-edited).

It also writes rungs/<id>/CLAUDE.md for every rung: the tutor a Claude session reads when Isaac runs
`claude` in that folder (and an empty rungs/<id>/progress.json if none exists; never overwritten).

index.html is hand-written. assets/progress.js holds the sidebar's copy of the curriculum
(id, slug, title, blurb, the passing sentence); keep the two in step when a slug or a check changes.
Run:  python3 build.py

Sep 24, 2026: guess boxes, tick boxes and the self-graded checkpoint widget removed from the rung
pages. Guesses and recall go to the tutor; progress.json is the only record of a rung.

Revised Sep 18, 2026 (09:30) after an independent read-through: L1's crash model, L5's overlay
mount, L2's checkpoint size, the schedule, and every term used before it was defined.
"""
import html, pathlib, re

EXPLAINER = "explainer.html"
# Section anchors in explainer.html, by the number shown on the page.
SECTIONS = {
    "01": ("what", "01 · What is a Sprite?"),
    "02": ("why", "02 · Why now: the agent framing"),
    "03": ("design", "03 · The three design bets"),
    "04": ("storage", "04 · The storage stack: how a disk becomes a URL"),
    "05": ("checkpoint", "05 · Checkpoint and restore"),
    "06": ("vs", "06 · Sprites vs Fly Machines"),
    "07": ("learn", "07 · What you'd need to learn"),
    "08": ("build", "08 · Small projects"),
    "09": ("plan", "09 · How this fits your plan"),
    "10": ("quiz", "10 · Check yourself (the quiz)"),
}

def sec(num, note=""):
    anchor, title = SECTIONS[num]
    return (f'<li><a href="{EXPLAINER}#{anchor}">{title}</a>' + (f" — {note}" if note else "") + "</li>")

# Each rung: say (what you can explain after), read (url, title, core|optional, why), mission steps,
# check, hint, unlocks (explainer sections), showcase (how it appears in the showcase project),
# hours (honest budget for reading + mission).
RUNGS = [
 dict(id="L0", slug="l0-a-computer-from-the-inside.html", tag="operating systems", hours="about 2 h 50 min over two sessions (87 min Thursday, 80 min Tuesday)",
  title="A computer from the inside",
  showcase="Phase P1 of the showcase creates one Sprite by hand with the CLI. Knowing what a virtual machine and a container image are is what makes <code>sprite create</code> finishing in one second surprising rather than magic.",
  say=[
   "what a <b>process</b> is, and what the <b>kernel</b> does that a process can't (talk to hardware, hand out memory, decide who runs). Step 1, below, explains both and gives the reading",
   "what a <b>filesystem</b> is (names, directories, an index of which blocks hold which file) versus the <b>block device</b> under it (a disk seen as a numbered array of fixed-size blocks, typically 4 KB). Step 2 explains both, with its reading",
   "why a <b>container</b> is a normal process with a restricted view of the machine (the kernel features are called namespaces and cgroups; step 7's reading defines them) and a <b>virtual machine</b> is a whole second kernel with its own emulated hardware (step 8)",
   "what a <b>container image</b> is: a stack of tar archives plus a JSON manifest, in the format the Open Container Initiative (OCI) standardised; and why pulling and unpacking one is the slow part of starting a container. Step 6 measures it, step 12 looks inside one",
   "what a <b>microVM</b> is: a virtual machine with almost no emulated hardware, so it boots in milliseconds. Firecracker is the one Fly uses under every Sprite. Step 10's reading",
  ],
  read=[
   ("https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf", "<i>Operating Systems: Three Easy Pieces</i>, chapter 4 \"The Abstraction: The Process\", sections 4.1 and 4.2", "core", "8 min. What a process is made of."),
   ("https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-mechanisms.pdf", "OSTEP chapter 6 \"Mechanism: Limited Direct Execution\", section 6.2 up to the trap table", "core", "8 min. User mode, kernel mode, the system call."),
   ("https://pages.cs.wisc.edu/~remzi/OSTEP/file-implementation.pdf", "<i>Operating Systems: Three Easy Pieces</i>, chapter \"File System Implementation\", the first four pages (up to and including the inode section)", "core", "15 min. Blocks, the inode table, how a name becomes a list of blocks. This is the filesystem-versus-block-device distinction."),
   ("https://jvns.ca/blog/2016/10/10/what-even-is-a-container/", "Julia Evans, <i>What even is a container: namespaces and cgroups</i>", "core", "15 min. The clearest statement that a container is a process with a restricted view."),
   ("https://pages.cs.wisc.edu/~remzi/OSTEP/vmm-intro.pdf", "OSTEP appendix B \"Virtual Machine Monitors\", sections B.1 and B.2", "core", "10 min. What a virtual machine is."),
   ("https://www.usenix.org/conference/nsdi20/presentation/agache", "<i>Firecracker: lightweight virtualization for serverless applications</i> (NSDI 2020), sections 1 and 2 only (about three pages)", "core", "25 min. Why Amazon wanted something between a container and a virtual machine."),
   ("https://github.com/opencontainers/image-spec/blob/main/spec.md", "OCI image specification, the overview page", "core", "10 min skim: layers, manifest, config. Just enough to know what <code>docker pull</code> downloads."),
  ],
  mission_type="estimate, then check",
  mission=[
   "Before running anything, write two predictions in a text file: how long <code>docker pull python:3.12</code> will take on your connection (run <code>docker rmi python:3.12</code> first if you already have it, so the pull is real), and how long <code>docker run --rm python:3.12 python -c 'print(1)'</code> will take once the image is local. Write the ratio you expect.",
   "Time both with <code>time</code>. Run the second one three times and take the median.",
   "Compare the inside of a container with the Linux machine it runs on. Inside: <code>docker run --rm -it python:3.12 sh</code>, then <code>hostname</code>, <code>ls /proc | head</code> (<code>/proc</code> is the kernel's live view of processes, one directory per process id), <code>mount | wc -l</code>, <code>ps aux | wc -l</code>. Outside, on a Mac, means Docker Desktop's Linux virtual machine, not macOS; get a shell in it with <code>docker run --rm -it --privileged --pid=host alpine nsenter -t 1 -m -u -n -i sh</code> and run the same four commands.",
   "Write five lines: what the container shares with the kernel it runs on (the process list you could see from outside, the kernel version), and what it has its own copy of (hostname, mounts, the process tree it can see).",
  ],
  check="The two timings, your predicted ratio within 3x of the measured one, and the five lines. If the ratio surprised you by more than 3x, write one sentence on what you had wrong; that sentence is the point of the mission.",
  hint=("If the pull is fast anyway", "You are on a fast connection and the image is small. Pull something bigger, such as <code>pytorch/pytorch</code> (several GB), or read the pull's output: it lists the layers, and each is one of the tar archives from the say-list. The 60-second tax the explainer's first design bet removes is real on Fly's side because their images are bigger and their network path longer."),
  unlocks=[sec("01", "what \"a full Linux VM that creates in 1 to 2 seconds\" is claiming"), sec("03", "bet 1, <i>Kill the container image</i>, and bet 3, <i>Inside-out orchestration</i>"), sec("06", "the creation-time row of the comparison table")],
 ),
 dict(id="L1", slug="l1-bytes-files-and-the-log.html", tag="storage", hours="about 3 h (reading 1.5 h, mission 1.5 h)",
  title="Bytes, files, and why the log comes first",
  showcase="The course agent's <code>progress.json</code> and review queue in the showcase are exactly the kind of small state a SQLite file with a write-ahead log is for.",
  say=[
   "the three places a written byte can be before it is safe: your program's own buffer (Python's file object), the kernel's page cache, and the disk. Which crash loses which: a killed process loses only its own buffer; a power cut or kernel crash loses the page cache too; only <b>fsync</b> (the system call that forces the page cache to disk) protects against the last one",
   "what <b>SQLite</b> is: one file, organised as fixed-size pages arranged in a <b>B-tree</b> (a sorted, shallow tree of pages), read and written by a library inside your process rather than a separate server",
   "what a <b>write-ahead log</b> (WAL) is: every change is appended to a log and made durable <i>before</i> the main structure is updated, so a crash mid-update loses nothing that was acknowledged",
   "why \"append to a log, then apply\" is the move underneath every durable system in the explainer: SQLite's WAL, Litestream, and the storage stack's metadata layer",
  ],
  read=[
   ("https://fly.io/blog/sqlite-internals-btree/", "Ben Johnson, <i>SQLite internals: pages and B-trees</i>", "core", "15 min. What a page is, how the B-tree sits on pages."),
   ("https://fly.io/blog/sqlite-internals-wal/", "Ben Johnson, <i>SQLite internals: WAL</i>", "core", "15 min. The write-ahead log, frame by frame. Makes rung L4's stretch step legible."),
   ("https://sqlite.org/wal.html", "SQLite, <i>Write-ahead logging</i>, the first half", "core", "20 min. Why the WAL exists, what a WAL \"checkpoint\" means there (folding the log back into the main file; a different meaning from a Sprite checkpoint)."),
   ("https://dataintensive.net/", "<i>Designing Data-Intensive Applications</i> (DDIA), chapter 3, first half: hash indexes, SSTables, LSM-trees", "core", "60 min. Append-only logs and compaction (merging old log segments), the same idea at database scale. An SSTable is a sorted log segment; an LSM-tree is a stack of them. You own the book."),
   ("https://litestream.io/how-it-works/", "Ben Johnson, <i>Litestream: how it works</i>", "optional", "10 min now, again at L4. Read it once so the word WAL has a picture attached."),
  ],
  mission_type="model it",
  mission=[
   "Write <code>kv.py</code>, about 60 lines, with two modes. <code>set(key, value)</code> appends one JSON line to <code>kv.log</code>. <code>--write</code>: a loop that sets keys 1, 2, 3 ... with a few kilobytes of value each and prints each key the moment <code>set</code> returns (that print is the acknowledgement). <code>--verify</code>: replay the log line by line, print how many records were read, how many were torn (a line that fails to parse) and dropped, and the last good key.",
   "<b>Trial A, buffered.</b> In <code>set</code>, call <code>f.write(line)</code> and nothing else. Terminal 1: <code>python kv.py --write</code>. Terminal 2, a few seconds later: <code>pkill -9 -f 'kv.py --write'</code>. Then <code>python kv.py --verify</code>. Compare the last key terminal 1 printed with the last good key <code>--verify</code> found. Expect a gap of hundreds of keys, and possibly a torn last line: Python's file object buffers in your process, and the kill destroys that buffer.",
   "<b>Trial B, flushed.</b> Add <code>f.flush()</code> after the write (the bytes now belong to the kernel's page cache, which outlives your process). Repeat the kill three times. Expect no gap: the kernel keeps what your process handed it.",
   "<b>Trial C, the one you cannot run.</b> Add <code>os.fsync(f.fileno())</code> after the flush. Nothing changes under <code>kill -9</code>, and that is the lesson: fsync protects against a crash of the machine, not of the process, and this mission cannot pull the plug. Measure instead what it costs: time 1,000 sets with and without fsync.",
  ],
  check="Trial A: the number of acknowledged keys that were lost (must be more than zero, or your values were too small to fill the buffer; make them bigger). Trial B: zero lost, three trials out of three. Trial C: the two timings, and one sentence naming the crash fsync is for.",
  hint=("If trial A loses nothing", "Python flushes a file buffer when it fills (about 8 KB by default). If each value is small and the loop is fast, the kill may land just after a flush. Use 4 KB values so most kills land mid-buffer, or set <code>open(..., buffering=1 &lt;&lt; 20)</code> to make the buffer 1 MB and the loss obvious."),
  unlocks=[sec("04", "the <i>Metadata: SQLite + Litestream</i> layer, and the sentence \"streaming its writes to object storage\""), sec("07", "the <i>Litestream / WAL log-shipping</i> card")],
 ),
 dict(id="L2", slug="l2-hashing-and-immutability.html", tag="storage", hours="about 2.5 h (reading 45 min, mission 1.5 h)",
  title="Hashing, immutability, content addressing",
  showcase="A Sprite checkpoint is this rung's manifest at machine scale; phase P2 of the showcase uses checkpoints as undo between generation stages.",
  say=[
   "what a <b>cryptographic hash</b> (such as SHA-256) gives you here: a fixed-size name that is a function of the content, so two identical blobs get one name and a changed blob gets a new one",
   "what <b>content addressing</b> means: store each blob under its hash. A blob under a given name can never change, so a copy of it can never be out of date",
   "how <b>git</b> stores a repository as a graph of immutable objects (blobs, trees, commits) and why a commit is cheap: it is a few pointers over objects that already exist",
   "why <b>deduplication</b> falls out for free, and why a <b>snapshot</b> of content-addressed data is a small manifest (a list of names) rather than a copy of the data",
   "what <b>JuiceFS</b> is, since the explainer's storage section is built on its model: a filesystem that stores file data as chunks in object storage and the metadata (which chunks make up which file) in a separate database. The same split as Google's 2003 <b>GFS</b> paper, which had one metadata server and many chunk servers",
  ],
  read=[
   ("https://git-scm.com/book/en/v2/Git-Internals-Git-Objects", "<i>Pro Git</i>, 10.2 Git internals: Git objects", "core", "30 min, with a terminal open. Do the <code>hash-object</code> and <code>cat-file</code> examples; the aha is watching a tree object point at blob hashes."),
   ("https://git-scm.com/book/en/v2/Git-Internals-Git-References", "<i>Pro Git</i>, 10.3 Git references", "optional", "10 min. A branch is a 41-byte file holding a hash. That is what a checkpoint pointer is."),
   ("https://juicefs.com/docs/community/architecture/", "JuiceFS, <i>Architecture</i>", "core", "10 min. The data / metadata split in one diagram. This is the page the explainer's section 07 means by \"the JuiceFS design doc\"."),
  ],
  mission_type="model it (this is the explainer's Level 2 chunk-store project)",
  mission=[
   "Write <code>chunks.py</code>: <code>put(path)</code> splits the file into 64 KB chunks, computes <code>sha256</code> of each, writes each chunk to <code>store/&lt;hash&gt;</code> if not already there, and writes <code>manifests/&lt;name&gt;.json</code> holding the ordered list of hashes and the total length.",
   "<code>get(name, out)</code> rebuilds the file from the manifest. Check with <code>cmp</code>.",
   "Make a 10 MB test file (<code>head -c 10000000 /dev/urandom &gt; big.bin</code>), put it, count the files in <code>store/</code>. Copy it, append one line, put the copy; count again. The difference is the number of new chunks.",
   "Add <code>checkpoint(name, label)</code>, which copies the manifest to <code>checkpoints/&lt;label&gt;.json</code>, and <code>restore(label)</code>, which copies it back over <code>manifests/&lt;name&gt;.json</code>. Neither touches file data; <code>get</code> is what rebuilds a file. Print the byte size of the checkpoint file.",
   "Afterwards, re-read the explainer's <a href=\"explainer.html#checkpoint\">section 05</a> \"Predict first\" box. It should now read as obvious.",
  ],
  check="The rebuilt file is byte-identical (cmp prints nothing). The near-duplicate added one new chunk (the last one; two at most), not 160. The checkpoint is about 11 KB, which is 160 hashes of 64 hex characters plus JSON, against 10 MB of data. Record the three numbers.",
  hint=("If the near-duplicate adds many chunks", "You changed the start of the file, or the chunk boundary shifted. Fixed-size chunking only deduplicates when the change is at the end; that is exactly why real systems (JuiceFS included) split on content rather than at fixed offsets. Note it and move on; content-defined chunking is a rabbit hole for another day."),
  unlocks=[sec("03", "bet 2, <i>Object storage is the source of truth</i>: why the durable state can be \"simply a URL\""), sec("04", "the <i>Data chunks: object storage</i> layer and the phrase \"immutable chunks\""), sec("05", "why a checkpoint \"merely shuffles metadata around\" and can be used \"like a git restore\""), sec("07", "the <i>Object storage as source of truth</i> card"), sec("08", "the Level 2 chunk-store project, which this rung is")],
 ),
 dict(id="L3", slug="l3-object-storage-and-caches.html", tag="storage", hours="about 3 h (reading 1.5 h, mission 1.5 h)",
  title="Object storage, caches, and easy invalidation",
  showcase="The Sprite's disk is object storage behind a local cache; phase P4's cost table in the showcase comes from the hot and cold storage prices this rung explains.",
  say=[
   "the <b>object storage</b> model, as Amazon S3 defines it: a flat namespace of keys inside a bucket, whole-object PUT and GET, no partial in-place writes, strong read-after-write consistency since December 2020, tens of milliseconds a call, very cheap per byte",
   "the latency gap: a read from the server's local <b>NVMe</b> drive (the fast solid-state disk attached directly to the machine) takes around a hundred microseconds; an object-storage read takes tens of milliseconds, so a few hundred times slower",
   "what a <b>read-through cache</b> is (on a miss, fetch from the slow store and keep a copy; on a hit, serve the copy) and what <b>cache invalidation</b> is (knowing when a copy has gone stale)",
   "why immutable, content-addressed chunks make invalidation disappear: a chunk under a given hash never changes, so a cached chunk is never stale, so the cache can be thrown away and refilled at will",
   "what <b>dm-cache</b> is in one paragraph: a Linux block-layer cache that puts a fast disk in front of a slow one, which is what the explainer compares the NVMe layer to",
  ],
  read=[
   ("https://calpaterson.com/s3.html", "Cal Paterson, <i>S3 is files, but not a filesystem</i>", "core", "10 min. The clearest statement of what the S3 model is and isn't."),
   ("https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel", "AWS, <i>Amazon S3 data consistency model</i>", "core", "5 min. The paragraph that matters is read-after-write."),
   ("https://colin-scott.github.io/personal_website/research/interactive_latency.html", "<i>Latency numbers every programmer should know</i>, interactive version", "core", "10 min. Drag the year slider; note SSD read, disk seek and datacentre round trip."),
   ("https://docs.kernel.org/admin-guide/device-mapper/cache.html", "Linux kernel documentation, <i>Cache</i> (dm-cache), the introduction only", "core", "5 min. Origin device, cache device, policy."),
   ("https://dataintensive.net/", "DDIA chapter 3, second half (B-trees versus LSM-trees; skim the column-storage part)", "core", "45 min. Then re-read the explainer's section 04 top to bottom."),
  ],
  mission_type="model it",
  mission=[
   "Run MinIO, an S3-compatible object store, locally: <code>docker run -d --name minio -p 9000:9000 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=minio12345 minio/minio server /data</code>.",
   "<code>pip install minio</code>. In <code>chunks.py</code>, add <code>--backend s3</code>: the client is <code>Minio('127.0.0.1:9000', access_key='minio', secret_key='minio12345', secure=False)</code>; create the bucket in code with <code>client.make_bucket('ladder')</code> if it doesn't exist; chunks are <code>put_object</code> to and <code>get_object</code> from it, keyed by hash, instead of written to <code>store/</code>.",
   "Add a local <code>cache/</code> directory holding at most N chunks, evicting the least recently used. Every GET checks the cache first. Count hits and misses and print them at the end.",
   "Time a cold read of the 10 MB file (empty cache) and a warm read (same file again). Then <code>rm -rf cache</code>, read again, compare bytes with the original. Finally set N to half the chunk count and confirm <code>cache/</code> never holds more than N files.",
  ],
  check="Nothing is lost after deleting the cache (cmp is silent), and the warm read is at least 10x faster than the cold one. Record the two timings and the hit/miss counts. Then count the lines of cache-invalidation code you wrote; the answer is zero, and you should be able to say why in one sentence.",
  hint=("If MinIO on Docker Desktop feels slow", "It will be slower than real S3 in some ways and faster in others (no network). The ratio is what you are after, not absolute numbers. For a realistic cold read, add <code>time.sleep(0.02)</code> per GET to simulate a 20 ms round trip."),
  unlocks=[sec("03", "bet 2, <i>Object storage is the source of truth</i>, and the phrase \"the durable state of a Sprite is simply a URL\""), sec("04", "the <i>NVMe cache</i> layer and the closing paragraph \"the two never fight\""), sec("06", "the honest limit \"object storage is too slow to be a hot Postgres node\"")],
 ),
 dict(id="L4", slug="l4-replication-by-shipping-a-log.html", tag="replication", hours="about 3 h (reading 1.5 h, mission 1.5 h)",
  title="Replication by shipping a log",
  showcase="Not used directly by the showcase; it is how the Sprite's own metadata stays durable under your course.",
  say=[
   "what <b>leader-based replication</b> is: one node accepts writes, the others apply a copy of its log",
   "the three things you can ship: SQL statements, the write-ahead log (the physical bytes of changed pages), or a logical change log (row-level changes), and what each is good and bad at",
   "what <b>point-in-time restore</b> means (rebuild the database as it was at a chosen moment) and why a log makes it possible",
   "what <b>Litestream</b> does: watches SQLite's write-ahead log and ships each transaction to object storage continuously (as raw WAL frames before version 0.5, as its own LTX transaction files since September 2025); and what it can't do: more than one writer, or zero lag",
  ],
  read=[
   ("https://dataintensive.net/", "DDIA chapter 5, the leader-based replication half (up to the multi-leader section)", "core", "60 min. Replication logs, replication lag, and \"read-your-writes\" (a reader always sees its own writes even on a lagging replica)."),
   ("https://litestream.io/how-it-works/", "<i>Litestream: how it works</i>, second pass", "core", "15 min. It now speaks of LTX files and TXIDs (transaction ids): the same WAL frames from rung L1, batched per transaction and compacted into levels."),
   ("https://litestream.io/guides/s3-compatible/", "Litestream guide, <i>S3-compatible storage</i>", "core", "10 min, for the mission's exact configuration."),
  ],
  mission_type="model it (this is the explainer's Level 2 replication project)",
  mission=[
   "Install Litestream: <code>brew install benbjohnson/litestream/litestream</code> (check the <a href=\"https://litestream.io/install/\">install page</a> if the tap has moved). Write <code>litestream.yml</code> with one database entry for <code>app.db</code> and one replica: <code>type: s3</code>, <code>bucket: ladder</code>, <code>path: app.db</code>, <code>endpoint: http://127.0.0.1:9000</code>, <code>force-path-style: true</code>, and the MinIO access and secret keys from L3.",
   "Write <code>writer.py</code>: opens <code>app.db</code>, runs <code>PRAGMA journal_mode=WAL</code>, creates <code>rows(id integer primary key, t text)</code>, then inserts one row a second and prints <code>select count(*)</code> after each commit. Terminal 1: <code>litestream replicate -config litestream.yml</code>. Terminal 2: <code>python writer.py</code>.",
   "After a minute, kill both. Delete <code>app.db</code>, <code>app.db-wal</code> and <code>app.db-shm</code> (the WAL file and its shared-memory index). Then <code>litestream restore -config litestream.yml -o restored.db app.db</code> and <code>sqlite3 restored.db 'select count(*) from rows'</code>.",
   "Point-in-time: <code>litestream restore -config litestream.yml -timestamp 2026-...T..:..:..Z -o then.db app.db</code> with a timestamp 30 seconds before the kill; count rows again. The difference is the log replayed to a chosen moment.",
   "Stretch: open <code>app.db-wal</code> with Python's <code>struct</code>, read the 32-byte header and the 24-byte frame headers, and print the page numbers. Compare with what rung L1's second reading described.",
  ],
  check="The restored row count equals the last acknowledged count minus at most one replication interval of writes (Litestream's default sync interval is one second, so at most one row). The point-in-time restore has fewer rows, and the difference matches the 30 seconds. Record both counts.",
  hint=("If restore gives fewer rows than expected", "That gap is replication lag, and it is the honest cost of asynchronous replication (the writer does not wait for the replica). Shorten the sync interval and measure again; then ask what it would take to make the gap zero. The answer is synchronous replication, and its price is in DDIA chapter 5."),
  unlocks=[sec("04", "\"Litestream continuously ships SQLite's write-ahead log to object storage\" and \"log-shipping replication\""), sec("07", "the <i>Litestream / WAL log-shipping</i> card, now done rather than read"), sec("08", "the Level 2 replication project, which this rung is")],
 ),
 dict(id="L5", slug="l5-snapshots-and-copy-on-write.html", tag="storage", hours="about 3 h (reading 1.5 h, mission 1.5 h)",
  title="Snapshots, copy-on-write, forking",
  showcase="Phase P2's \"regenerate this section\" in the showcase is restore-then-rerun, and the missing native fork is why creating a learner's Sprite is a bootstrap script rather than a copy of a template.",
  say=[
   "what <b>copy-on-write</b> means: readers share one copy; a writer gets a private copy of only the part it changes",
   "how an <b>overlay filesystem</b> works: a read-only lower directory, a writable upper directory holding only the changes, a work directory the kernel uses internally, and a merged view that shows both",
   "why a virtual-machine <b>snapshot</b> can be taken in milliseconds (memory and disk are marked copy-on-write rather than copied) and what Firecracker's snapshot and restore do",
   "why <b>forking</b> a disk from a snapshot is cheap, and why Sprites cannot yet do it natively: restore is in-place, and fork-from-checkpoint is a requested feature as of mid-2026. The explainer's section 05 describes forking as if it shipped; treat that paragraph as the plan, not the product",
  ],
  read=[
   ("https://jvns.ca/blog/2019/11/18/how-containers-work--overlayfs/", "Julia Evans, <i>How containers work: overlayfs</i>", "core", "10 min. Lower, upper, merged, with the exact mount command the mission uses."),
   ("https://docs.kernel.org/filesystems/overlayfs.html", "Linux kernel documentation, <i>Overlay filesystem</i>, the first two sections", "optional", "15 min, if you want the rules for whiteouts and directory merging."),
   ("https://github.com/firecracker-microvm/firecracker/blob/main/docs/snapshotting/snapshot-support.md", "Firecracker, <i>Snapshot support</i> documentation", "core", "30 min. What a snapshot contains, why restore is fast, the copy-on-write memory mapping. (The 2020 paper predates snapshots, so it is not assigned here.)"),
   ("https://fly.io/blog/design-and-implementation/", "Fly.io, <i>The design and implementation of Sprites</i>, the section headed \"Decision #2: Object Storage For Disks\"", "core", "20 min. Where checkpoints and the block device live in the real design. The other sections are rung L8."),
   ("https://community.fly.io/t/feature-request-native-fork-sprite-from-checkpoint/28191", "Fly community, <i>Feature request: native fork Sprite from checkpoint</i>", "core", "5 min. The honest state of forking, needed for the last condition below."),
  ],
  mission_type="model it",
  mission=[
   "Overlay mounts are a Linux kernel feature, so do this inside Linux: <code>docker run --rm -it --privileged ubuntu bash</code> gives a root shell in a container that is allowed to mount. One trap: the container's own root filesystem is itself an overlay, and the kernel refuses an upper directory that sits on an overlay. So first <code>mkdir /ov &amp;&amp; mount -t tmpfs tmpfs /ov &amp;&amp; cd /ov</code> and work there.",
   "Make <code>lower/</code> with three small files <code>a.txt b.txt c.txt</code>, copy it to <code>lower.orig/</code>, and make empty <code>upper1 work1 merged1</code> (and the same with 2 and 3). Mount: <code>mount -t overlay overlay -o lowerdir=lower,upperdir=upper1,workdir=work1 merged1</code>, and likewise for 2 and 3.",
   "<code>echo changed &gt; merged1/a.txt</code>, <code>echo changed &gt; merged2/b.txt</code>, <code>echo changed &gt; merged3/c.txt</code>. Then <code>diff -r lower lower.orig</code> (must print nothing) and <code>ls upper1 upper2 upper3</code> (one file each).",
   "Back on the Mac, in <code>chunks.py</code>: add <code>fork(label, new_name)</code>, which copies a checkpoint's manifest under a new name, and <code>shared(a, b)</code>, which prints how many hashes two manifests have in common out of the total. Fork <code>big.bin</code>'s checkpoint as <code>big-fork</code>, change the middle of the forked file and put it again under that name, then run <code>shared</code>.",
  ],
  check="<code>lower/</code> is byte-unchanged after all three edits (diff prints nothing); each upper holds only the one file changed through its own merged view; in <code>chunks.py</code>, the fork shares all but the one or two changed chunks with the original. Record the shared-out-of-total count. Then write two sentences on why Sprites can't fork from a checkpoint yet, from the community thread.",
  hint=("If mount says wrong fs type or invalid argument", "Your upper or work directory is on the container's overlay root. Check <code>df .</code> shows tmpfs. If it says operation not permitted instead, you forgot <code>--privileged</code>. Either way the friction is the point: filesystems are a kernel matter, which is what rung L0 said."),
  unlocks=[sec("05", "\"drive forking\", the copy-on-write Sprite Block Device (SBD), and \"spin up 100 agents from one warmed template\", read with the caveat above"), sec("07", "the <i>Copy-on-write / drive forking</i> and <i>Checkpoint / restore</i> cards")],
 ),
 dict(id="L6", slug="l6-gossip-and-service-discovery.html", tag="distributed systems", hours="about 4 h over two weeks (reading 1.5 h, install 1 h, mission 1.5 h; challenge 3c is the stretch)",
  title="Gossip, membership, service discovery",
  showcase="Every learner's course URL in the showcase finds its Sprite through Corrosion; nothing to build, but it is why the URL survives the Sprite moving to another host.",
  say=[
   "how a <b>gossip protocol</b> spreads a fact: each node tells a few random peers each round, so the whole fleet knows in a number of rounds proportional to the logarithm of its size",
   "what <b>SWIM</b> (Scalable Weakly-consistent Infection-style process group Membership, the 2002 protocol behind Serf and Consul) does: nodes ping each other and gossip about who is alive",
   "what a <b>CRDT</b> (conflict-free replicated data type) is: a data structure whose replicas can be updated independently and always merge to the same result, without a coordinator",
   "what <b>service discovery</b> means (finding which machine currently serves a name), and how a Sprite's public URL finds the physical host it lives on right now: Fly's <b>Corrosion</b> gossips that mapping across the fleet",
  ],
  read=[
   ("https://en.wikipedia.org/wiki/Gossip_protocol", "<i>Gossip protocol</i> on Wikipedia", "core", "10 min. Just the mechanism and the logarithmic rounds."),
   ("https://www.serf.io/docs/internals/gossip.html", "HashiCorp Serf, <i>Gossip protocol</i> internals", "core", "20 min. A production SWIM with the parameters explained. (The developer.hashicorp.com copy of this page is gone; this is the live one.)"),
   ("https://crdt.tech/", "<i>crdt.tech</i>, the introduction", "core", "15 min."),
   ("https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md", "Maelstrom, <i>Protocol</i> documentation", "core", "15 min. The JSON message shapes your node reads and writes."),
   ("https://github.com/superfly/corrosion", "Fly.io, the <i>Corrosion</i> README", "core", "15 min, after the mission."),
   ("https://dataintensive.net/", "DDIA chapter 5, the leaderless replication half", "optional", "40 min, if the season allows."),
  ],
  mission_type="model it (already on the dist-sys roadmap as a Gossip Glomers challenge)",
  mission=[
   "Install Maelstrom, the test harness Fly's <a href=\"https://fly.io/dist-sys/\">Gossip Glomers</a> challenges run on. It starts your program as several nodes, sends them requests (a <i>workload</i>), can cut the network between nodes (a <i>partition</i>, injected by what it calls a <i>nemesis</i>), and checks the results. <code>brew install openjdk graphviz gnuplot</code>, download the latest release tarball from <a href=\"https://github.com/jepsen-io/maelstrom/releases\">github.com/jepsen-io/maelstrom/releases</a>, unpack it.",
   "Fly's pages show Go; you are writing Python. Your node is a script with a <code>#!/usr/bin/env python3</code> first line and <code>chmod +x</code>, reading one JSON message per line from stdin and writing one per line to stdout (about 40 lines of scaffolding from the protocol reading). Pass challenge 1, Echo: <code>./maelstrom test -w echo --bin ./echo.py --node-count 1 --time-limit 10</code>. \"Everything looks good!\" means valid.",
   "Challenge 3a, single-node broadcast: <code>--node-count 1</code>. Challenge 3b, five nodes, every node must end up with every message: forward each new message to your neighbours. <code>./maelstrom test -w broadcast --bin ./broadcast.py --node-count 5 --time-limit 20 --rate 10</code>.",
   "Stretch, the second week: 3c, the same under partitions, <code>--nemesis partition</code>. Messages sent during a partition must be retried until acknowledged, and a node must be able to receive a message twice without double-counting (that property is called idempotence). Then read the Corrosion README and write ten lines mapping your broadcast onto it: what is gossiped, how conflicts resolve (Corrosion uses CRDTs over SQLite), what happens during a partition.",
  ],
  check="Maelstrom prints \"Everything looks good!\" for echo, 3a and 3b. For 3c (stretch) the same, and from its results block record <code>:msgs-per-op</code> under <code>:net :servers</code>, the number Glomers 3d later asks you to lower. The ten-line mapping exists.",
  hint=("If 3c fails under partition", "Two bugs cover most failures: you send once and never retry, or you retry and count duplicates. Keep a set of seen message ids, and keep a per-neighbour queue of unacknowledged messages that you resend on a timer."),
  unlocks=[sec("05", "the networking aside: \"public URLs propagate via Corrosion, Fly's gossip-based service-discovery layer\""), sec("07", "the <i>Corrosion (gossip service discovery)</i> card"), sec("08", "the Level 3 project, which this rung is")],
 ),
 dict(id="L7", slug="l7-capabilities-not-credentials.html", tag="security", hours="about 2.5 h (reading 1 h, mission 1.5 h)",
  title="Capabilities, not credentials",
  showcase="Phase P3 of the showcase in miniature: the learner's code calls the language model through a Connector and never sees the key.",
  say=[
   "the difference between holding a <b>credential</b> (the API key itself) and holding a <b>capability</b> (an unforgeable right to perform one action, which can be handed out and revoked)",
   "what a <b>token broker</b> is: a process that holds the real secret and performs calls on behalf of a less-trusted process, adding the secret itself. The secret usually travels as an HTTP header, <code>Authorization: Bearer &lt;key&gt;</code>",
   "why an agent's machine should never contain the raw key: anything with root on that machine (including the agent's own mistakes) can read it",
   "how Sprites <b>Connectors</b> implement this: the Sprite reaches OpenRouter (a service that fronts many language-model APIs behind one key), Slack, GitHub or any HTTP API, and the credential never enters the VM. <b>OAuth</b> is the web's standard way for one service to grant another limited access on a user's behalf; Connectors hide its dance too",
  ],
  read=[
   ("https://fly.io/sprites/", "The Sprites product page, the Connectors section", "core", "10 min. What a Connector is from the platform's side. (The docs site's Connectors concept page moves around; start from the product page and follow the Connectors link.)"),
   ("https://fly.io/sprites-blog/slack-bots-on-sprites/", "Fly.io Sprites blog, <i>Slack bots on Sprites: OAuth is easy now</i>", "core", "10 min. A Connector doing the OAuth dance so the code inside never holds a token."),
   ("https://fly.io/sprites-blog/running-untrusted-code/", "Fly.io Sprites blog, <i>Run any code fearlessly</i>", "core", "10 min. The other half: what the VM boundary buys."),
   ("https://en.wikipedia.org/wiki/Capability-based_security", "<i>Capability-based security</i> on Wikipedia, the definition and the first example", "core", "15 min."),
  ],
  mission_type="model it (new; not in the explainer)",
  mission=[
   "Write <code>upstream.py</code>, about 20 lines: an HTTP server on port 9000 that returns 200 and a JSON body only if the request carries <code>Authorization: Bearer &lt;REAL_KEY&gt;</code>, else 401. This stands in for the real API, so no real key is at risk.",
   "Write <code>broker.py</code>, about 100 lines: an HTTP server on port 8787 that accepts requests on <code>/proxy/&lt;path&gt;</code>, allows exactly one upstream host (<code>127.0.0.1:9000</code>), adds <code>Authorization: Bearer $REAL_KEY</code> from its own environment, forwards the request, and logs method, path and status.",
   "Write <code>agent.py</code>: calls <code>$API_BASE/proxy/hello</code> and prints the status and body. With <code>--try-to-leak</code> it instead prints its own environment, searches the filesystem for the key's first eight characters, and tries to read <code>/proc/&lt;broker pid&gt;/environ</code>.",
   "Separation is the point, so run the three as two users inside one Linux container: <code>docker run --rm -it ubuntu bash</code>, then <code>apt update &amp;&amp; apt install -y python3 &amp;&amp; useradd -m agent</code>. As root: <code>REAL_KEY=sk-ladder-test python3 upstream.py &amp;</code> and <code>REAL_KEY=sk-ladder-test python3 broker.py &amp;</code>. As the agent: <code>su agent -c 'env -i PATH=$PATH API_BASE=http://127.0.0.1:8787 python3 agent.py'</code>, then the same with <code>--try-to-leak</code>.",
  ],
  check="The agent gets 200 through the broker. Every leak attempt fails: the key is not in the agent's environment, not in any file it can read, and <code>/proc/&lt;broker pid&gt;/environ</code> is permission denied (it belongs to root). Record the status code, the number of attempts, and the number that succeeded, which must be zero.",
  hint=("If the agent can read the key", "Both processes run as the same user, so <code>/proc/&lt;pid&gt;/environ</code> is readable. Check <code>ps -o user,pid,cmd</code>. Running the agent as a different user is the whole mechanism; the VM boundary in Sprites is a stronger version of the same line."),
  unlocks=[sec("02", "\"credentialed access to external systems without handing the agent your secrets\""), sec("05", "\"Connectors give a Sprite authenticated access to external systems without exposing the credentials\""), sec("07", "the <i>Capability vs credential (Connectors)</i> card")],
 ),
 dict(id="L8", slug="l8-read-it-again.html", tag="synthesis", hours="about 4 h, reading-heavy (sources 3 h, mission 1 h); split over two slots",
  title="Read it again, then the sources",
  showcase="Read the four Sprites blog posts with the showcase's five phases open beside them; each post is one phase seen from Fly's side.",
  say=[
   "every sentence in the explainer's sections 03 to 07, in your own words",
   "the storage stack from memory: immutable chunks in object storage, a SQLite index whose write-ahead log is shipped to object storage, a throwaway NVMe cache in front, and why the three don't fight",
   "where Sprites stop working (the explainer's section 06) and why; what \"running, warm, cold\" mean in the docs (billed and awake; asleep with its memory kept; asleep with only the disk kept); and what the S3 block device in early access is (the disk itself served from object storage, the next step of design bet 2)",
  ],
  read=[
   (EXPLAINER, "The explainer, end to end, then the quiz in section 10", "core", "60 min. Tell the tutor the quiz score; it has five questions."),
   ("https://fly.io/blog/code-and-let-live/", "Kurt Mackey, <i>Code and let live</i>", "core", "15 min. The why: \"ephemeral sandboxes are obsolete\" (a sandbox that forgets everything when the task ends)."),
   ("https://fly.io/blog/design-and-implementation/", "Thomas Ptacek, <i>The design and implementation of Sprites</i>", "core", "40 min. The how, and the explainer's main source."),
   ("https://fly.io/sprites/", "The Sprites product page and docs", "core", "30 min: checkpoints, the HTTPS URL per Sprite, Connectors, the running / warm / cold states, the S3 block device in early access."),
   ("https://fly.io/sprites-blog/", "The Sprites blog: <i>Run any code fearlessly</i>, <i>Make computers make computers</i>, <i>Agent swarms on Sprites</i>, <i>Slack bots on Sprites</i>", "core", "40 min. The four that map onto the showcase project."),
   ("https://simonwillison.net/2026/Jan/9/sprites-dev/", "Simon Willison, note on sprites.dev (Jan 9, 2026)", "optional", "5 min. An outside view."),
  ],
  mission_type="teach it back",
  mission=[
   "Take the explainer's quiz cold. Write the score down before reading the explanations. Four of five is the pass line; below that, the wrong answers name the rung to revisit.",
   "Close everything and write one paragraph explaining the storage stack to someone who has done L0 to L2 but nothing after. Then check it against section 04.",
   "Test the paragraph on a stranger: paste it to Claude with the explainer closed and ask what is unclear. Two or fewer sentences questioned is the pass line.",
   "Write the list of things you still can't explain. That list is season 3's reading.",
  ],
  check="Quiz at least 4 of 5, taken cold. The paragraph exists and drew at most two clarifying questions. The remaining gaps are listed by name.",
  hint=None,
  unlocks=[sec("10", "the quiz"), sec("07", "every card, now as a checklist of things you can explain"), sec("09", "the plan section, which the showcase project replaces")],
 ),
]

TAGS = {"core": "core", "optional": "opt"}

def page(r, i):
    n = len(RUNGS)
    folder = r["id"].lower()
    say = "".join(f"<li>{x}</li>" for x in r["say"])
    acts = ACTIVE.get(r["id"], [])
    def active_block(k):
        a = acts[k] if k < len(acts) else None
        if not a: return ""
        trace = f'<p class="trace"><b>Alongside:</b> {a["trace"]}</p>' if a.get("trace") else ""
        return f'<div class="active">{guess_html(a["predict"])}{trace}</div>'
    read = "".join(
        f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a> <span class="tag {TAGS[tag]}">{tag}</span>'
        f'<span class="why"> — {why}</span>{active_block(k)}</li>'
        for k, (u, t, tag, why) in enumerate(r["read"]))
    write = "".join(f"<li>{w}</li>" for w in WRITE.get(r["id"], []))
    steps = "".join(f"<li>{x}</li>" for x in r["mission"])
    hint = ""
    if r["hint"]:
        hint = f'<details class="hint"><summary>Hint · {r["hint"][0]}</summary><p>{r["hint"][1]}</p></details>'
    unlocks = "".join(r["unlocks"])
    if r["id"] in SESSIONS:
        body = ('<h2 id="work">2 · Work through it, in order</h2>\n'
                '<p class="srcnote">Read a little, then do a little. Step 0 starts the tutor; it keeps your place in '
                f'<code>rungs/{folder}/progress.json</code>.</p>\n' + sessions_html(r) + "\n" + hint)
        passing = ("The tutor checks the evidence and records it in <code>rungs/l0/progress.json</code>: it runs "
                   "<code>check.py</code> itself (all five lines must say PASS) and goes over your five lines from step 11 "
                   "against <code>compare.json</code>. You don't mark the rung passed yourself.")
    else:
        body = f"""<h2 id="read">2 · Read, in this order</h2>
<p class="srcnote">Under most readings is a "before you read" list: tell the tutor your guesses before you open the
reading, run the command alongside if there is one, and afterwards the tutor asks you a question or two about it.</p>
<ul class="plain">{read}</ul>

<h2 id="mission">3 · Mission <span class="tag deep">{html.escape(r["mission_type"])}</span></h2>
<div class="spec">
<strong>Do this</strong>
<ol>{steps}</ol>
<p><b>The check:</b> {r["check"]}</p>
</div>
{hint}
"""
        passing = (f"The tutor checks the evidence and records it in <code>rungs/{folder}/progress.json</code>: the "
                   "numbers and sentences the check above asks for, discussed with you. You don't mark the rung passed yourself.")
    nb = (3, 4, 5) if r["id"] in SESSIONS else (4, 5, 6)
    docker = " &amp;&amp; open -a Docker" if r["id"] == "L0" else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sprites ladder · {r["id"]} · {html.escape(r["title"])}</title>
<link rel="stylesheet" href="assets/style.css">
<style>
  li .why {{ color: var(--muted); font-size: .92em; }}
  ul.plain {{ list-style: none; padding-left: 0; }}
  ul.plain > li {{ margin: .6rem 0; }}
  .spec ol {{ padding-left: 1.2rem; }}
  .spec ol li {{ margin: .55rem 0; }}
  div.active {{ margin: .35rem 0 .6rem 1.2rem; font-size: .86rem; padding: .4rem .7rem; background: #f7f9fc; border: 1px solid #d3ddea; border-radius: 6px; }}
  div.active .trace {{ margin: .3rem 0; color: var(--muted); }}
  p.guess {{ margin: .6rem 0 .1rem; }}
  ul.guess {{ margin: .1rem 0 .4rem; padding-left: 1.2rem; }}
  h3.half {{ margin: 2rem 0 .4rem; }}
  ol.steps {{ padding-left: 1.4rem; }}
  ol.steps > li.step {{ margin: 1.4rem 0; }}
  div.steph {{ display: flex; gap: .55rem; align-items: baseline; flex-wrap: wrap; }}
  div.steph .min {{ margin-left: auto; font-size: .8rem; color: var(--muted); }}
  .kind {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; padding: .1rem .45rem; border-radius: 4px; font-weight: 600; }}
  .kind.read {{ background: var(--callout-bg); color: var(--accent); }}
  .kind.do {{ background: var(--warn-bg); color: var(--accent-warm); }}
  .see {{ color: var(--muted); font-size: .92em; }}
  .stop {{ margin: 1.2rem 0 2rem; padding: .9rem 1.1rem; border: 2px dashed var(--accent-warm); border-radius: 8px; font-size: .92rem; }}
  .stop strong {{ display: block; margin-bottom: .3rem; }}
</style>
</head>
<body>
<nav id="sidebar"></nav>
<main>
<p class="kicker">Rung {i} of {n-1} · {html.escape(r["tag"])} · {html.escape(r["hours"])}</p>
<h1>{r["title"]}</h1>

<p class="srcnote">One rung per week, in two sessions: the first half on Thursday at 19:30, the second half the following Tuesday at 19:30.
Work through it with the tutor, a Claude session that knows this rung:
<code>cd ~/Projects/dist-sys-interview-prep/sprites-guide/rungs/{folder}{docker} &amp;&amp; claude</code>, then type <b>start</b>.
It asks the questions on this page, tells you what you got right and wrong, and keeps your place in <code>progress.json</code>.</p>

<h2 id="say">1 · After this rung you can say</h2>
<ul>{say}</ul>

{body}

<div class="callout" id="passing"><strong>Passing this rung</strong>{passing}</div>

<h2 id="showcase">{nb[0]} · In the showcase project</h2>
<p>{r.get("showcase","")} See <a href="showcase.html">Course from a link, on Sprites</a>.</p>

<h2 id="unlocks">{nb[1]} · Where this shows up in the explainer</h2>
<p>Links go to the numbered sections of <a href="{EXPLAINER}">the explainer</a>, the page this ladder exists to make readable.</p>
<ul>{unlocks}</ul>

<h2 id="write">{nb[2]} · Write about it</h2>
<p>For the series on your site (plan and titles on the <a href="publishing.html">publishing page</a>). Sixty minutes of polish at most, the same week.</p>
<ul>{write}</ul>

</main>
<footer class="pager" data-auto></footer>
<script src="assets/progress.js"></script>
</body>
</html>
"""

def explainer_map():
    rows = []
    for num in ["01","02","03","04","05","06","07","08","09","10"]:
        anchor, title = SECTIONS[num]
        who = [r for r in RUNGS if any(f'#{anchor}"' in u for u in r["unlocks"])]
        links = ", ".join(f'<a href="{r["slug"]}">{r["id"]} {r["title"]}</a>' for r in who) or "no rung needed; read it any time"
        rows.append(f'<tr><td><a href="{EXPLAINER}#{anchor}">{title}</a></td><td>{links}</td></tr>')
    bets = """
<h2>The "three design bets" in section 03</h2>
<p>Section 03 of the explainer is titled <i>The three design bets</i>. Each bet is one thing Fly chose to do differently from their older product, Fly Machines, and each has a click-to-open box on that page. When a rung says "bet 1" it means this list:</p>
<ol>
<li><b>Kill the container image.</b> Sprites don't start from a downloaded container image; every host already has one standard base image and a pool of pre-warmed empty Sprites, so creating one is claiming one. Needs <a href="l0-a-computer-from-the-inside.html">L0</a>.</li>
<li><b>Object storage is the source of truth.</b> A Sprite's disk lives in S3-compatible object storage, not on one physical server's NVMe; "the durable state of a Sprite is simply a URL". Needs <a href="l2-hashing-and-immutability.html">L2</a> and <a href="l3-object-storage-and-caches.html">L3</a>.</li>
<li><b>Inside-out orchestration.</b> The platform's services (storage, restarts, logging, networking) run inside the VM rather than on the host. Needs <a href="l0-a-computer-from-the-inside.html">L0</a>.</li>
</ol>
<p class="srcnote">The table above is generated from each rung's own "where this shows up in the explainer" list, so the two never disagree; this bets paragraph is hand-written in <code>build.py</code>.</p>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sprites ladder · Map of the explainer</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<nav id="sidebar"></nav>
<main>
<p class="kicker">Reference</p>
<h1>Map of the explainer</h1>
<p><a href="{EXPLAINER}">The explainer</a> has ten numbered sections. This table says which rungs each section needs. If a section reads as noise, do its rungs and come back.</p>
<table>
<tr><th>Explainer section</th><th>Rungs that make it readable</th></tr>
{"".join(rows)}
</table>
{bets}
</main>
<script src="assets/progress.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- markdown → html body
def md_body(src):
    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
        t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
        t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'(?<![\w*])_([^_]+)_(?![\w*])', r'<em>\1</em>', t)
        return t
    lines = src.split('\n'); out = []; i = 0; buf = []
    def flush():
        nonlocal buf
        if buf: out.append('<p>' + inline(' '.join(buf)) + '</p>'); buf = []
    while i < len(lines):
        l = lines[i]
        if l.startswith('#'):
            flush(); n = len(l) - len(l.lstrip('#')); txt = l[n:].strip()
            if n == 1: i += 1; continue   # the page supplies its own h1
            out.append(f'<h{n} id="{re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")}">{inline(txt)}</h{n}>')
        elif l.startswith('|'):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith('|'): rows.append(lines[i]); i += 1
            cells = lambda r: [c.strip() for c in r.strip().strip('|').split('|')]
            h = cells(rows[0]); body = [cells(r) for r in rows[2:]]
            t = '<table><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in h) + '</tr>'
            for r in body: t += '<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
            out.append(t + '</table>'); continue
        elif re.match(r'^(\d+\.|-) ', l):
            flush(); ordered = l[0].isdigit(); items = []
            while i < len(lines) and (re.match(r'^(\d+\.|-) ', lines[i]) or (lines[i].startswith('  ') and lines[i].strip())):
                if re.match(r'^(\d+\.|-) ', lines[i]): items.append(re.sub(r'^(\d+\.|-) ', '', lines[i]))
                else: items[-1] += ' ' + lines[i].strip()
                i += 1
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>'); continue
        elif l.strip() == '': flush()
        else: buf.append(l.strip())
        i += 1
    flush()
    return '\n'.join(out)

SHOWCASE_MD = "../../curriculum-edtech/course-from-a-link-on-sprites.md"

def showcase():
    src = pathlib.Path(__file__).parent.joinpath(SHOWCASE_MD).read_text()
    src = src.replace("`dist-sys-interview-prep/sprites-guide/l7-capabilities-not-credentials.html`", "[rung L7](l7-capabilities-not-credentials.html)")
    src = src.replace("(`dist-sys-interview-prep/sprites-guide/index.html`, in the Thursday", "([this guide](index.html), in the Thursday")
    body = md_body(src)
    body = body.replace('href="/Users/isaacowomugisha/Projects/curriculum-edtech/learning-through-code-and-maths.md"', 'href="../../curriculum-edtech/learning-through-code-and-maths.html"')
    rungs = "".join(f'<a href="{r["slug"]}">{r["id"]}</a> ' for r in RUNGS if r["id"] != "L8")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sprites ladder · Showcase: course from a link</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<nav id="sidebar"></nav>
<main>
<p class="kicker">Showcase project · what the ladder is for</p>
<h1>Course from a link, on Sprites</h1>
<div class="callout"><strong>Rungs this project leans on</strong> {rungs}(L4 and L6 as background only). Each rung page has an "In the showcase project" section pointing back here.
The source text is <code>curriculum-edtech/course-from-a-link-on-sprites.md</code>; edit that and run <code>build.py</code>.</div>
{body}
</main>
<script src="assets/progress.js"></script>
</body>
</html>
"""

def refresh_explainer_chips():
    """Under each <h2> of explainer.html, one line naming the rungs that make that section readable."""
    p = pathlib.Path(__file__).parent / "explainer.html"
    s = p.read_text()
    s = re.sub(r'\n  <p class="rungs">.*?</p>', '', s, flags=re.S)
    for num, (anchor, title) in SECTIONS.items():
        who = [r for r in RUNGS if any(f'#{anchor}"' in u for u in r["unlocks"])]
        if not who: continue
        chips = "".join(f'<a href="{r["slug"]}">{r["id"]} {r["title"]}</a>' for r in who)
        line = f'\n  <p class="rungs">Rungs that make this section readable: {chips}</p>'
        s = re.sub(rf'(<section id="{anchor}">\n  <h2>.*?</h2>)', lambda m: m.group(1) + line, s, count=1, flags=re.S)
    p.write_text(s)

# ---------------------------------------------------------------- read actively + write about it
# ACTIVE[rung id] is a list parallel to that rung's `read` list: for each reading, the questions the tutor
# asks before he reads it, and (where one exists) a command or action to run alongside. L0's live in SESSIONS.
ACTIVE = {
 "L1": [
  dict(predict=["What is SQLite's page size? How many tree levels does a table of a million rows need?"], trace="<code>sqlite3 t.db 'create table x(a); insert into x select value from generate_series(1,1000000); pragma page_size; pragma page_count;'</code>. Compare the page count with the post's arithmetic."),
  dict(predict=["Where does a write go first in WAL mode? When does the main database file change?"], trace="Open a second terminal and <code>watch ls -la t.db*</code> while you insert rows in WAL mode; watch <code>-wal</code> grow and the main file stand still."),
  dict(predict=["What does the word checkpoint mean on this page? What is the cost of never running one?"], trace="<code>pragma wal_checkpoint;</code> and look at the <code>-wal</code> size before and after."),
  dict(predict=["The chapter opens with the simplest possible database, two shell functions. Before reading: write them yourself, and say what is slow about them.", "What is an index, in one sentence, and what does it cost on writes?"], trace="Type the chapter's <code>db_set</code> / <code>db_get</code> into bash, insert 100,000 keys, time one <code>db_get</code>. That number is why the rest of the chapter exists."),
  dict(predict=["How can a separate program replicate a SQLite database without SQLite cooperating?"], trace=None),
 ],
 "L2": [
  dict(predict=["What is a commit made of? If you change one file in a repository of 1,000 files and commit, how many new objects are created?"], trace="<code>git init t &amp;&amp; cd t &amp;&amp; echo hi &gt; a &amp;&amp; git add a &amp;&amp; git commit -qm x &amp;&amp; find .git/objects -type f | wc -l</code>; change <code>a</code>, commit again, count again."),
  dict(predict=["What is in the file <code>.git/refs/heads/main</code>? How big is it?"], trace="<code>cat .git/refs/heads/main</code> and <code>wc -c</code> on it."),
  dict(predict=["Where do file names live and where do file bytes live? What happens to your files if the metadata engine dies?"], trace="Draw the architecture from memory first, then compare with the page's diagram."),
 ],
 "L3": [
  dict(predict=["Can you append to an S3 object? Rename one? List a directory?"], trace="Write your three answers, then check each against the article. Later, try each against MinIO with the client from the mission."),
  dict(predict=["Right after a PUT, can a GET from another machine still return the old version?"], trace=None),
  dict(predict=["SSD read versus a round trip inside a datacentre: what ratio do you expect?"], trace="Time a 4 KB file read in Python against one HTTP request to a local server; compare with the page's numbers."),
  dict(predict=["On a write that misses the cache, what does dm-cache do? Who decides what to evict?"], trace=None),
  dict(predict=["Why do B-trees overwrite pages in place while LSM-trees never overwrite? Which handles a write-heavy load better, and why?"], trace="Write a five-row comparison table (write path, read path, space, crash recovery, where used) before reading, then correct it."),
 ],
 "L4": [
  dict(predict=["If the leader dies, how does a follower know whether it has everything? What exactly is replication lag?", "Name a bug a user would see with a lagging replica."], trace="Draw the leader, two followers and one write as a sequence diagram before reading; correct it after."),
  dict(predict=["What is an LTX file compared with a WAL frame from rung L1? Why compact them?"], trace="With <code>litestream replicate</code> running, list the bucket with the MinIO client every few seconds and watch files appear."),
  dict(predict=["Why does path-style addressing matter for MinIO and not for real S3?"], trace=None),
 ],
 "L5": [
  dict(predict=["Where do writes through the merged view go? What happens when you delete a lower-layer file through merged?"], trace="In the mission's container: <code>rm merged1/b.txt; ls -la upper1</code>. The odd entry you see is a whiteout, a marker that hides the lower file."),
  dict(predict=["What is a whiteout, and why does an overlay need one?"], trace=None),
  dict(predict=["What is in a snapshot: disk, memory, both? Which is bigger? How can restore be fast if memory is gigabytes?"], trace=None),
  dict(predict=["If the truth is in object storage, what does Fly use the local NVMe for? What happens when a physical host dies?"], trace=None),
  dict(predict=["Why is fork harder than restore in Fly's design?"], trace=None),
 ],
 "L6": [
  dict(predict=["1,000 nodes, each telling 3 random peers per round: how many rounds until everyone knows?"], trace="Write a 30-line simulation: N nodes, fanout F, count rounds until all informed; run it for N = 100, 1,000, 10,000. Keep it; it is a blog interactive."),
  dict(predict=["How does a node decide another is dead without a central monitor? What does a false positive cost?"], trace=None),
  dict(predict=["Two replicas increment a counter at the same time; how do you merge without losing one? Now do it for a set with removals."], trace=None),
  dict(predict=["What fields must every reply message carry? What identifies a node?"], trace="Run the echo challenge and read one request and one reply from Maelstrom's log."),
  dict(predict=["Does Fly gossip whole rows or changes? What is the conflict rule?"], trace=None),
  dict(predict=["How can a read be correct when writes go to any node?"], trace=None),
 ],
 "L7": [
  dict(predict=["Where does the credential live? What does the code inside the Sprite see when it calls the external service?"], trace=None),
  dict(predict=["Which part of OAuth is painful for a bot developer, and what does the Connector remove?"], trace=None),
  dict(predict=["What can code inside a Sprite damage? What can it not reach?"], trace=None),
  dict(predict=["What is the difference between an access-control check and a capability? Why can a capability be handed on safely?"], trace="After the mission: write which part of your broker is the capability and which is the credential."),
 ],
 "L8": [
  dict(predict=["Take the quiz first, cold. Write the score down before reading anything."], trace=None),
  dict(predict=["What is wrong with ephemeral sandboxes for agents, in the author's view?"], trace=None),
  dict(predict=["Name the three design decisions from memory before reading. Then find what the post says the hardest part was."], trace=None),
  dict(predict=["What is the difference between warm and cold? Which states are billed?"], trace=None),
  dict(predict=["Which showcase phase does each of the four posts map to?"], trace=None),
  dict(predict=["What did an outsider notice that Fly did not say?"], trace=None),
 ],
}

# WRITE[rung id]: what to write about after this rung, for the series on cmplx-xyttmt.github.io.
WRITE = {
 "L0": ["<b>Post 1 · \"A container is a process: measured on my laptop.\"</b> Standalone. The two timings and your prediction, the inside/outside comparison, and the surprise most Mac users never see: Docker Desktop is a hidden Linux VM. Figure: the timing table. Under 800 words."],
 "L1": ["<b>Post 2 · \"Three places a byte can hide.\"</b> Standalone, and the strongest early post. The three trials as a story: what kill -9 destroyed, what it didn't, and what fsync is for. One diagram: program buffer, page cache, disk. The 1,000-set timing with and without fsync as the closing figure."],
 "L2": ["<b>Post 3 · \"A disk that is just a URL.\"</b> Combine L2 and L3. Build the chunk store on the page: hashing, the manifest, deduplication for free, then the checkpoint that is 11 KB against 10 MB, then MinIO behind a cache that needed zero invalidation code. Interactive: a manifest view that highlights shared chunks between two files. Write it after L3 passes."],
 "L3": ["Folded into post 3 with L2 (above). If it grows too long, split at the cache: L3 alone as <b>\"The cache that never goes stale\"</b> with the cold/warm timings and the hit-ratio-versus-cache-size figure from step 4."],
 "L4": ["<b>Post 4 · \"Replication is shipping a log.\"</b> Standalone, or a sequel to post 2 (\"the same database, killed again\"). Litestream against MinIO, the row-count gap as replication lag, the point-in-time restore. Figure: acknowledged rows versus restored rows across sync intervals."],
 "L5": ["<b>Post 5 · \"Copy-on-write, from overlayfs to forking a machine.\"</b> Standalone. The three overlays and the whiteout, then fork() in the chunk store, then how Firecracker snapshots memory. End honestly with why Sprites cannot fork yet. Figure: lower / upper1 / upper2 / upper3 as a tree."],
 "L6": ["<b>Post 6 · \"Gossip, simulated then built.\"</b> Standalone. The 30-line gossip simulation as an interactive (fanout and fleet-size sliders, rounds as output), then Glomers broadcast under partitions, then the ten-line mapping to Corrosion. This is the most shareable post in the series."],
 "L7": ["<b>Post 7 · \"Give the agent a capability, not the key.\"</b> Standalone, short. The broker, the failed leak attempts with their error messages, and what a Sprites Connector adds. Ties to the showcase's phase P3; can double as that phase's post."],
 "L8": ["<b>Post 8, the capstone · \"Re-reading the Sprites post after eight rungs.\"</b> The annotated re-read: which sentences became obvious, which still don't land, the storage-stack paragraph from memory, and the quiz score then versus now. Link every earlier post from the sentence it explains.", "<b>Post 0, the introduction</b>, is written before post 1; the draft and the title options are on the <a href=\"publishing.html\">publishing page</a>."],
}

# ---------------------------------------------------------------- sessions (reading and doing, interleaved)
# SESSIONS[rung id] replaces that rung's separate "Read" and "Mission" sections with one ordered list of
# steps, split into the Thursday half and the Tuesday half (the Sep 23 re-plan). Each step is a dict:
#   kind ("read" or "do"), title, mins, body (HTML), guess (questions for the tutor to ask before the
#   reading or the prediction, optional), check (the check.py step name, optional).
# Since Sep 24, 2026 there are no boxes or ticks: guesses and recall happen in a tutor session
# (rungs/<id>/CLAUDE.md, generated below), and rungs/<id>/progress.json is the only record.
# The starter code and check.py for each rung live in rungs/<id>/; step numbers match check.py's names.
OSTEP = "https://pages.cs.wisc.edu/~remzi/OSTEP/"
SESSIONS = {
 "L0": [
  dict(name="First half", when="Thursday", steps=[
   dict(kind="do", title="Set up, and start the tutor", mins=5,
    tutor="If he is talking to you, he has done the first half of this step. Run `python3 check.py`, walk him through the five lines it prints (what each step name means, and that TODO is expected), and mark step 0 done. If Docker is not running yet, say that is fine until step 6.", body=
    '<p>Everything in this rung happens in one folder. Docker Desktop takes a minute or two to start and you won\'t need it '
    'until step 6, so start it first. Then open the tutor: a Claude session in the rung\'s folder that knows these steps. '
    'Copy and paste this into a terminal:</p>'
    '<pre class="term">cd ~/Projects/dist-sys-interview-prep/sprites-guide/rungs/l0 &amp;&amp; open -a Docker &amp;&amp; claude</pre>'
    '<p>Then type <b>start</b>. The tutor reads <code>progress.json</code> in that folder, tells you which step you are on, and '
    'runs it with you: it asks the "before you read" questions on this page, tells you what you got right and wrong, and asks a '
    'question or two after each reading. It gives hints on the do-steps, not answers. Ask it about any word you don\'t know.</p>'
    '<p>To run a command, use a second terminal tab in the same folder, or type it into the tutor with a <code>!</code> in front '
    '(for example <code>! python3 check.py</code>).</p>'
    '<p class="see">What you should see: the tutor runs <code>python3 check.py</code> and shows five lines. <code>setup</code> says '
    'PASS once Docker is up ("not running yet" is fine for now; it will pass in a minute), and <code>step3</code>, '
    '<code>step5</code>, <code>step6</code> and <code>step9</code> say TODO. Each do-step has a starter file in that folder with '
    '<code>TODO</code> lines where your code goes. Nothing to install.</p>'),
   dict(kind="read", title="What a process is, and what the kernel does", mins=18, body=
    '<p>Two words come first, because everything else in this rung is built on them.</p>'
    '<p>A <b>process</b> is a program that is running. The program is a file on disk. The process is that file loaded into '
    'memory, with its own memory, its own list of open files, and a note of which instruction runs next. Open two terminal '
    'tabs and run <code>python3</code> in each: that is one program and two processes.</p>'
    '<p>The <b>kernel</b> is the part of the operating system that is always running and is in charge of every process. It is '
    'the only code allowed to talk to the hardware (the disk, the network card). It hands out memory, and it decides which '
    'process gets the CPU next. A process that wants to read a file can\'t touch the disk itself. It asks the kernel, and that '
    'request is called a <b>system call</b>.</p>'
    '<p>Try it. Each line <code>ps</code> prints is one process, and the PID column is its process id. <code>echo $$</code> '
    'prints the id of your own shell, and <code>uname -r</code> prints the version of the kernel you are talking to (on a Mac, '
    'the kernel is called Darwin).</p>'
    '<pre class="term">ps aux | head -5\necho $$\nuname -r</pre>'
    f'<p>Then read two short pieces of <i>Operating Systems: Three Easy Pieces</i> (OSTEP), a free textbook:</p>'
    f'<ul><li><a href="{OSTEP}cpu-intro.pdf" target="_blank" rel="noopener">Chapter 4, "The Abstraction: The Process"</a>, '
    'from the start through section 4.2 "Process API" (about three pages, 8 minutes). What a process is made of.</li>'
    f'<li><a href="{OSTEP}cpu-mechanisms.pdf" target="_blank" rel="noopener">Chapter 6, "Mechanism: Limited Direct Execution"</a>, '
    'section 6.2 "Problem #1: Restricted Operations", from its start to where it begins on the trap table (about two pages, '
    '8 minutes). This is where user mode, kernel mode and the system call come from.</li></ul>',
    guess=["When you run <code>python3</code> in two terminal tabs, how many programs are there, and how many processes?",
           "Why can't your Python script write to the disk directly? What would go wrong if it could?"]),
   dict(kind="read", title="What a filesystem sits on", mins=10, body=
    '<p>A <b>block device</b> is a disk seen the plain way: a long row of fixed-size blocks, numbered 0, 1, 2 and so on, '
    'usually 4 KB each. It knows nothing about names or folders. You can only say "read block 7" or "write block 7". A '
    '<b>filesystem</b> is what the kernel keeps on top of it: file names, directories, and an index of which blocks belong to '
    'which file. On your Mac, <code>diskutil list</code> shows the block devices (<code>/dev/disk0</code> and so on) and '
    '<code>df -h /</code> shows the filesystem that sits on one of them.</p>'
    f'<p>Now open <a href="{OSTEP}file-implementation.pdf" target="_blank" rel="noopener">OSTEP chapter 40, '
    '"File System Implementation"</a>. Read from the start through section 40.2 "Overall Organization", and stop when section '
    '40.3 (about the inode) begins. That\'s about two pages. Look hard at the picture of the 64-block disk; you\'ll use its '
    'numbers in step 5.</p>',
    guess=["How does the filesystem get from the name <code>notes.txt</code> to the disk blocks holding its bytes?",
           "What is stored about a file besides its bytes?"]),
   dict(kind="do", title="A file's size versus the disk it takes", mins=12, check="step3", body=
    '<p>The chapter says the disk is split into 4 KB blocks. Is your Mac\'s disk like that? Ask it:</p>'
    '<pre class="term">diskutil info / | grep "Block Size"</pre>'
    '<p>Now open <code>step3_blocks.py</code> and write the two functions marked TODO: <code>blocks_needed</code> (how many 4 KB '
    'blocks a file of some size needs) and <code>allocated_bytes</code> (how much disk the filesystem says a file takes, from '
    '<code>os.stat</code>). The docstring for <code>allocated_bytes</code> has a warning about units. Read it. Then:</p>'
    '<pre class="term">python3 step3_blocks.py\npython3 check.py step3</pre>'
    '<p class="see">What you should see: <code>step3: PASS</code> and a small table. A 1-byte file takes 4096 bytes on disk, and a '
    '4097-byte file takes 8192. If the check says you are off by a factor of 8, that is the units warning.</p>'),
   dict(kind="read", title="The inode", mins=8, body=
    f'<p>Back to <a href="{OSTEP}file-implementation.pdf" target="_blank" rel="noopener">the OSTEP chapter</a>. Read section 40.3 '
    '"File Organization: The Inode", up to where it starts on multi-level indexes. The part to slow down on is the worked example '
    'that finds inode number 32. Say each step of that arithmetic out loud once.</p>'
    '<p>Alongside, try it on a real file. The first number <code>ls -i</code> prints is the inode number:</p>'
    '<pre class="term">ls -i step3_blocks.py\nstat step3_blocks.py</pre>',
    guess=["An inode is the filesystem's record of one file. What do you think it has to hold, and roughly how big is it?"]),
   dict(kind="do", title="Find an inode on the disk", mins=12, check="step5", body=
    '<p>Open <code>step5_inode.py</code>. The constants at the top are the chapter\'s example filesystem: 4 KB blocks, 256-byte '
    'inodes, an inode table starting at 12 KB. Check them against the picture first. Then write the three functions: the byte '
    'address where an inode starts, the block that holds it, and the sector that holds its first byte. The chapter\'s own example '
    '(inode 32 starts at 20 KB) is your first test.</p>'
    '<pre class="term">python3 step5_inode.py\npython3 check.py step5</pre>'
    '<p class="see">What you should see: <code>step5: PASS</code>. The check\'s last line says something about inodes 0 to 15. '
    'The disk only reads whole blocks, so what does looking up one file\'s inode fetch for free?</p>'),
   dict(kind="do", title="Predict, then time a container pull", mins=10, check="step6",
    tutor="The pull takes minutes. Once `run_timing.py` is running, move on to step 7 and come back to finish step 6 (median() and the check) when it prints \"Saved timings.json\". Step 6 is done only when its check passes. If his ratio is off by more than 3x, talk through what he had wrong before he writes SURPRISE.", body=
    '<p>Two words first. A <b>container</b> is a process that the kernel starts with a restricted view of the machine (step 7\'s '
    'reading shows how). A <b>container image</b> is the files that process starts from: a stack of archives, one per layer, '
    'plus a small JSON file that lists them. Docker has to download and unpack all of it before a container can start '
    '(step 12 looks inside one). Starting a container from an image you already have is a different cost. How different?</p>'
    '<p>Guess before you measure. Open <code>step6_timing.py</code> and fill in the two predictions in seconds: the pull of '
    '<code>python:3.12</code> from nothing, and one <code>docker run</code> once it\'s local. Then start the measurement (it '
    'removes any local copy first, so the pull is from nothing):</p>'
    '<pre class="term">python3 run_timing.py</pre>'
    '<p class="see">What you should see: Docker\'s download progress, then <code>pull: ... s</code> and three run times. The image '
    'is around 1 GB, so the pull can take a few minutes. <b>Don\'t wait for it.</b> Go to step 7 and come back when it '
    'prints "Saved timings.json". Then write <code>median()</code> in the same file and run <code>python3 check.py step6</code>. '
    'PASS if your ratio was within 3x; if not, the check asks for one sentence in <code>SURPRISE</code> on what you had wrong. '
    'That sentence is the most useful thing you\'ll write tonight.</p>',
    guess=["Before writing the numbers in the file, say them to the tutor: how long for the pull, how long for one run, and "
           "why you think the ratio is what it is."]),
   dict(kind="read", title="A container is a process", mins=12, body=
    '<p>While the pull runs, read <a href="https://jvns.ca/blog/2016/10/10/what-even-is-a-container/" target="_blank" '
    'rel="noopener">Julia Evans, "What even is a container: namespaces and cgroups"</a>. Note the word <i>namespace</i> each time '
    'it comes up, and what it hides. A <b>namespace</b> limits what a process can see (other processes, mounts, the hostname); a '
    '<b>cgroup</b> limits how much it can use (memory, CPU).</p>',
    guess=["Is a container a process, a virtual machine, or a third thing? What stops it from seeing your files?",
           "Three containers are running on one machine: how many kernels are running?"]),
  ], stop='Ask the tutor to run <code>python3 check.py</code> once more. <code>setup</code>, <code>step3</code>, '
         '<code>step5</code> and <code>step6</code> saying PASS means the first half is done; <code>step9</code> stays TODO '
         'until Tuesday. If you run out of energy after step 5, stop there instead, and the tutor will pick up step 6 next '
         'time. A short evening that ends with a passing check beats a long one that doesn\'t.'),
  dict(name="Second half", when="the following Tuesday", steps=[
   dict(kind="read", title="What a virtual machine is", mins=10, body=
    '<p>A <b>virtual machine</b> (VM) is a whole computer made of software. A program called a <b>hypervisor</b> pretends to be '
    'the hardware (CPU, memory, disk, network card), and a second, complete operating system, with its own kernel, boots inside '
    'it. A container shares the kernel of the machine it runs on. A VM brings its own.</p>'
    '<p>You have one running already. macOS can\'t run Linux containers, so Docker Desktop starts a small Linux VM, and every '
    'container from Thursday was a process inside it.</p>'
    f'<p>Read <a href="{OSTEP}vmm-intro.pdf" target="_blank" rel="noopener">OSTEP appendix B, "Virtual Machine Monitors"</a>, '
    'sections B.1 "Introduction" and B.2 "Motivation: Why VMMs?" (about two pages). A virtual machine monitor is the book\'s '
    'name for a hypervisor.</p>',
    guess=["What does a hypervisor have to pretend to be, so that an unmodified operating system can boot on it?",
           "Why would anyone run a second operating system on one computer?"]),
   dict(kind="do", title="Inside a container versus outside it", mins=15, check="step9", body=
    '<p>"Outside" a container, on a Mac, means Docker Desktop\'s Linux VM, not macOS. <code>run_compare.py</code> reaches the VM '
    'with <code>nsenter</code>, a command that joins the namespaces of another process.</p>'
    '<p>Open <code>step9_inside_outside.py</code>. For each of five commands, predict whether the container prints the '
    '<code>"same"</code> output as the Linux VM or <code>"different"</code> output. Then one True or False: when a container runs '
    '<code>sleep 300</code>, can the VM\'s process list see it? Fill everything in, then:</p>'
    '<pre class="term">python3 run_compare.py\npython3 check.py step9</pre>'
    '<p class="see">What you should see: the five commands in three places (your Mac, the VM, the container), then the check marks '
    'each wrong prediction. For each one, write a sentence in <code>NOTES</code> and run the check again until it says PASS. Look '
    'at the kernel version line in particular.</p>',
    guess=["Before filling in the file, tell the tutor your five same-or-different predictions and why."]),
   dict(kind="read", title="Why Amazon built something in between", mins=25, body=
    '<p>Read sections 1 and 2 (about three pages) of <a href="https://www.usenix.org/conference/nsdi20/presentation/agache" '
    'target="_blank" rel="noopener"><i>Firecracker: lightweight virtualization for serverless applications</i></a> (NSDI 2020). '
    'Firecracker is a <b>microVM</b>: a virtual machine with almost no pretend hardware, so it boots in a fraction of a second. '
    'Fly runs one under every Sprite.</p>',
    guess=["Why wasn't a container good enough for AWS Lambda? Why wasn't an ordinary VM?",
           "What boot time does the paper aim for, and what did it remove to get there?"]),
   dict(kind="do", title="Five lines: shared versus copied", mins=15,
    tutor="Read `compare.json` yourself first. Take his lines one at a time and check each against it. When all five hold, save them in the note for step 11 and in `evidence`.", body=
    '<p>Open <code>compare.json</code> from step 9: it is your evidence. Tell the tutor five lines: what the container shares '
    'with the kernel it runs on (the process list you could see from outside, the kernel version), and what it has its own copy '
    'of (hostname, mounts, the process tree it can see). Use Firecracker\'s framing where it helps: which of these would a '
    'microVM have its own copy of too? The tutor pushes back on any line that compare.json doesn\'t support, and records the '
    'final five in <code>progress.json</code>.</p>'),
   dict(kind="read", title="What a pull downloads", mins=15, body=
    '<p>Skim the <a href="https://github.com/opencontainers/image-spec/blob/main/spec.md" target="_blank" rel="noopener">OCI image '
    'specification overview</a> (10 minutes): layers, manifest, config. OCI is the Open Container Initiative, the group that '
    'wrote down the image format Docker uses. Then open the image you pulled in the first half and look at the layers that made '
    'the pull slow:</p>'
    '<pre class="term">docker save python:3.12 -o /tmp/img.tar &amp;&amp; tar tf /tmp/img.tar | head -20\nrm /tmp/img.tar</pre>',
    guess=["How many files is a container image? What is in the manifest?"]),
  ], stop='Then tell the tutor you want to pass the rung. It runs <code>check.py</code>, goes over your five lines, and records '
         'the result in <code>progress.json</code>.'),
 ],
}

def guess_html(qs, lead="Before you read"):
    if not qs: return ""
    return (f'<p class="guess"><b>{lead}:</b> tell the tutor your guess for each of these.</p>'
            '<ul class="guess">' + "".join(f"<li>{q}</li>" for q in qs) + "</ul>")

def sessions_html(r):
    out, k = [], -1
    for s in SESSIONS[r["id"]]:
        total = sum(st["mins"] for st in s["steps"])
        out.append(f'<h3 class="half">{s["name"]} · {s["when"]}, about {total} minutes</h3><ol class="steps" start="{k+1}">')
        for st in s["steps"]:
            k += 1
            lead = "Before you read" if st["kind"] == "read" else "Before you start"
            out.append(f'<li class="step"><div class="steph"><span class="kind {st["kind"]}">{st["kind"]}</span> <b>{st["title"]}</b> '
                       f'<span class="min">{st["mins"]} min</span></div>{st["body"]}{guess_html(st.get("guess"), lead)}</li>')
        out.append(f'</ol><div class="stop"><strong>{s["name"]} ends here</strong>{s["stop"]}</div>')
    return "".join(out)

# ---------------------------------------------------------------- tutor sessions (rungs/<id>/CLAUDE.md)
# Generated for every rung. The tutor reads progress.json, runs the current step as a conversation,
# and writes progress.json after each step. build.py never overwrites an existing progress.json.

def text(h):
    """HTML fragment to plain text for the tutor file: keep code in backticks, drop the rest of the markup."""
    h = re.sub(r"<pre[^>]*>(.*?)</pre>", lambda m: "\n\n```\n" + m.group(1) + "\n```\n\n", h, flags=re.S)
    h = re.sub(r"<code>(.*?)</code>", r"`\1`", h, flags=re.S)
    h = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', r"\2 (\1)", h, flags=re.S)
    h = re.sub(r"<li>", "\n- ", h)
    h = re.sub(r"</p>\s*", "\n\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h)
    h = re.sub(r"[ \t]+\n", "\n", h)
    return re.sub(r"\n{3,}", "\n\n", h).strip()

def tutor_steps(r):
    """A flat list of (kind, title, text, guesses, check) for the rung, numbered from 0 in order."""
    if r["id"] in SESSIONS:
        out = []
        for s in SESSIONS[r["id"]]:
            for st in s["steps"]:
                body = text(st["body"]) + (f'\n\nNote for the tutor: {st["tutor"]}' if st.get("tutor") else "")
                out.append((st["kind"], f'{st["title"]} ({s["name"].lower()}, {s["when"]}, {st["mins"]} min)',
                            body, st.get("guess") or [], st.get("check")))
        return out
    acts = ACTIVE.get(r["id"], [])
    out = []
    for k, (u, t, tag, why) in enumerate(r["read"]):
        a = acts[k] if k < len(acts) else {}
        body = f'Read {text(t)} ({u}), {tag}. {text(why)}'
        if a.get("trace"): body += "\n\nAlongside: " + text(a["trace"])
        out.append(("read", f"Reading {k+1}: {text(t)}", body, a.get("predict") or [], None))
    for k, m in enumerate(r["mission"]):
        out.append(("do", f"Mission step {k+1}", text(m), [], None))
    return out

TUTOR_RULES = """## How to run a session

You are Isaac's tutor for this rung. He opens `claude` in this folder and says "start" (or anything
like it). Then:

1. Read `progress.json` in this folder. The current step is the lowest-numbered step that is not
   done. Tell him in one line which step he is on and what it is, for example: "You're on step 3,
   A file's size versus the disk it takes." If a step was left half-done (a long download, a check
   still failing), say so and offer to finish it first.
2. Run that step with him, as a conversation, one question at a time:
   - **Before a reading or a prediction**, ask the step's guess questions (listed under the step
     below). Wait for his answer. Don't correct him yet: the point is that the guess exists before
     the reading does. Then send him to the reading with its link and page range.
   - **After a reading**, go back to his guesses. Say plainly which parts were right and which were
     wrong, and why. Then ask one or two recall questions about what he just read. Questions should
     need understanding, not memory of a sentence. If he gets one wrong, explain it and ask a
     variant.
   - **On a do-step**, give hints, never solutions. Don't write or edit his code in the starter
     files. If he is stuck, give the smallest hint that unblocks him: point at the line, name the
     function to look up, or ask what he expects a value to be and have him print it. When he thinks
     it's done, have him run the check (or run `python3 check.py <step>` yourself) and read the
     output with him.
3. **Explain any word he doesn't know** in plain words, in two or three sentences, with one concrete
   command he can run to see the thing (for example `ps aux | head` for "process"). If the rung's
   reading covers it, say where.
4. **After each step**, update `progress.json` (see the schema below): mark the step done with the
   time and a one-line note on what he got right or wrong. Write the file straight away, so the
   next session picks up from here.
5. **At the end of the session**, when he says he's stopping or the half is finished, print one line
   he can paste into his Log, in this shape:
   `Sprites <rung>: steps a to b done; <what he got wrong and now understands>; next: step c.`
   Print it only. Don't edit any file outside this folder.

## Passing the rung

He doesn't mark the rung passed himself. You check the evidence:
{pass_rule}
When all of it holds, set `"passed": true`, `"passed_at"` to the date, and `"evidence"` to a short
record of the numbers and lines that passed. If something is missing, say exactly what, and leave
`passed` false.

## progress.json

```json
{{"rung": "{rid}",
 "steps": {{"0": {{"done": true, "at": "2026-09-25T19:42", "note": "one line: what he got right or wrong"}}}},
 "passed": false, "passed_at": null, "evidence": ""}}
```

Step keys are the step numbers below, as strings. Get the time with `date +%Y-%m-%dT%H:%M`. Keep
notes to one line. Never delete a note he earned in an earlier session.

## How to talk

Plain words and complete sentences. Short answers, then a question back to him. No em-dashes, no
metaphors, no "great question". When he is wrong, say so directly and explain; when he is right,
say what exactly was right. He learns by doing, so keep each reading short and get him back to a
command or a line of code quickly. Evenings are his tired hours: if he says he's done, stop,
save progress, and print the Log line.
"""

def pass_rule(r):
    if r["id"] == "L0":
        return ("- Run `python3 check.py` yourself: all five lines (setup, step3, step5, step6, step9) must say PASS.\n"
                "- His five lines from step 11 (shared with the kernel versus its own copy) have been discussed and\n"
                "  each is supported by `compare.json`.\n"
                "- Record in `evidence`: the pull and run timings, his predicted and measured ratio, and the five lines.")
    return f"- The mission's check, from the rung page: {text(r['check'])}\n- Record the numbers it names in `evidence`."

def tutor_md(r):
    folder = r["id"].lower()
    say = "\n".join(f"- {text(x)}" for x in r["say"])
    steps = []
    for k, (kind, title, body, guesses, check) in enumerate(tutor_steps(r)):
        s = f"### Step {k} · {kind} · {title}\n\n{body}\n"
        if guesses:
            s += "\nGuess questions (ask before the reading or the prediction):\n" + "\n".join(f"- {text(q)}" for q in guesses) + "\n"
        if check:
            s += f"\nDone when `python3 check.py {check}` says PASS.\n"
        steps.append(s)
    if r["id"] in SESSIONS:
        layout = ("The steps are split into two halves: the first on Thursday at 19:30, the second the following "
                  "Tuesday at 19:30. The starter files and `check.py` are in this folder; each do-step's file name "
                  "starts with its step number. The step text below is the page's, written to Isaac as \"you\"; "
                  "the notes for the tutor are yours.")
    else:
        layout = ("This rung has not been cut into a two-half script yet, so the steps are the readings in order, "
                  "then the mission steps. The page lists them without these numbers, so when you tell him where he is, "
                  "name the reading or the mission step too (\"step 5, mission step 1\"). There are no starter files "
                  "yet: he writes the mission's code in this folder, and you don't write it for him. Before this rung "
                  "starts it should be re-cut into a two-half script with a check script, like L0.")
    return f"""# Tutor for rung {r["id"]} · {text(r["title"])}

Generated by `sprites-guide/build.py` from the rung page `../../{r["slug"]}`; edit `build.py` and
rerun it rather than editing this file. The rung page has the full text of every step, and is the
source of truth if this file and the page ever disagree.

{layout}

## After this rung he can say

{say}

Every item above must come with an explanation or a named source by the time a step relies on it.
If he asks about one and the steps below haven't covered it yet, explain it yourself.

{TUTOR_RULES.format(pass_rule=pass_rule(r), rid=r["id"])}
## The steps

{chr(10).join(steps)}"""

def write_tutors(here):
    import json
    for r in RUNGS:
        d = here / "rungs" / r["id"].lower()
        d.mkdir(parents=True, exist_ok=True)
        (d / "CLAUDE.md").write_text(tutor_md(r))
        p = d / "progress.json"
        if not p.exists():
            p.write_text(json.dumps({"rung": r["id"], "steps": {}, "passed": False, "passed_at": None, "evidence": ""}, indent=1) + "\n")


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    for i, r in enumerate(RUNGS):
        (here / r["slug"]).write_text(page(r, i))
    (here / "explainer-map.html").write_text(explainer_map())
    (here / "showcase.html").write_text(showcase())
    refresh_explainer_chips()
    write_tutors(here)
    print("built", len(RUNGS), "rung pages + explainer-map.html + showcase.html + rungs/*/CLAUDE.md; explainer chips refreshed")

