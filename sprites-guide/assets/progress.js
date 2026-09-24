/* Sprites ladder -- curriculum manifest, sidebar, progression state.
 *
 * Adapted from optimization-competitions/learning/guide/assets/progress.js.
 * Everything lives in localStorage under one key, so it works from file://
 * with no server. Nothing leaves the machine. Export before clearing browser
 * data. Rungs are never navigation-locked: a hollow dot means "not passed
 * yet", not "you may not read it".
 *
 * Three kinds of state:
 *   levels[id].done        -- the rung's checkpoint was passed (the mission's check)
 *   levels[id].attempts[]  -- one row per logged attempt: {at, score, note}
 *   ticks[id]              -- any checkbox on a page marked data-tick="..." (readings, steps, conditions)
 *   notes[id]              -- any textarea/input marked data-note="..." (publishing.html's notes box)
 *
 * Sep 24, 2026: the rung pages no longer carry the checkpoint widget (<div class="cpw">), tick boxes or
 * guess boxes. A rung's record is rungs/<id>/progress.json, kept by the tutor session in that folder,
 * and this file cannot read it from file://. So levels[id].done, and the sidebar dots and the start
 * page's "passed / next up" labels that come from it, only reflect what was saved before that date.
 * The widget code below is kept (it renders nothing when no page has a data-level mount).
 */
(function () {
  "use strict";

  var KEY = "sprites-ladder-v1";

  var CURRICULUM = [
    { id: "L0", slug: "l0-a-computer-from-the-inside.html", title: "A computer from the inside",
      tag: "operating systems",
      blurb: "Process versus kernel, filesystem versus block device, container versus virtual machine, and what a container image is. The vocabulary the explainer's section 03 uses without stopping.",
      cp: "Two timings (image pull, container start) with your written prediction within 3x of the measured ratio, and five lines on what a container shares with the host.",
      how: "The mission produces two timings and a prediction. Type them in below (seconds; the run time is the median of three). The page computes the measured ratio. Then tick each condition you met and mark the rung passed.",
      cmd: "time docker pull python:3.12\ntime docker run --rm python:3.12 python -c 'print(1)'   # run three times",
      evidence: [
        { key: "pull_s", label: "image pull, seconds", ph: "e.g. 38" },
        { key: "run_s", label: "container start, seconds (median of 3)", ph: "e.g. 0.9" },
        { key: "pred_ratio", label: "the ratio you predicted before running (pull ÷ start)", ph: "e.g. 20" }
      ],
      derived: function (f) { var a = +f.pull_s, b = +f.run_s, p = +f.pred_ratio; if (!(a > 0 && b > 0)) return ""; var r = a / b; var s = "measured ratio: " + r.toFixed(1) + "x"; if (p > 0) s += " · your prediction was off by " + (r > p ? (r / p) : (p / r)).toFixed(1) + "x" + ((r / p <= 3 && p / r <= 3) ? " (within 3x: pass)" : " (outside 3x: write one sentence on what you had wrong)"); return s; },
      criteria: ["Both timings recorded, container start as the median of three runs", "Predicted ratio within 3x of the measured one (or the one-sentence correction written)", "Five lines written: what the container shares with the kernel, what it has its own copy of"] },
    { id: "L1", slug: "l1-bytes-files-and-the-log.html", title: "Bytes, files, and why the log comes first",
      tag: "storage",
      blurb: "How blocks become files, what SQLite is, what a write-ahead log protects against. The metadata layer of the explainer's section 04, from the bottom.",
      cp: "A 60-line append-only key-value store, killed with kill -9 three ways: buffered (loses acknowledged keys), flushed (loses nothing, three trials of three), and fsync (no change under kill -9, but you can say which crash it is for and what it costs).",
      how: "Each trial is: start the writer, kill -9 it from a second terminal, run --verify. Record the last key the writer printed (acknowledged) and the last good key --verify found. In trial A (no flush) they differ, and the gap is the lesson. In trial B (flush) they match; log three of those. Trial C is two timings: 1,000 sets with and without fsync.",
      cmd: "python kv.py --write            # terminal 1: prints each key as set() returns\npkill -9 -f 'kv.py --write'     # terminal 2, mid-loop\npython kv.py --verify           # records read, torn lines dropped, last good key\npython kv.py --bench 1000       # trial C: seconds for 1,000 sets, with and without fsync",
      evidence: [
        { key: "acked", label: "trial B: last key the writer printed before the kill", ph: "e.g. 4812" },
        { key: "found", label: "trial B: last good key --verify found after replay", ph: "e.g. 4812" },
        { key: "lostA", label: "trial A (buffered): acknowledged keys lost", ph: "e.g. 312" },
        { key: "bench", label: "trial C: seconds for 1,000 sets, flush only / flush + fsync", ph: "e.g. 0.02 / 3.1" }
      ],
      derived: function (f) { var s = []; if (f.acked && f.found) s.push(f.acked === f.found ? "trial B: acknowledged and replayed keys match" : "acknowledged and replayed keys differ by " + (+f.acked - +f.found) + ": fine for trial A (the buffer died with the process); in trial B it means flush() is not running before the print"); if (f.lostA !== undefined && f.lostA !== "") s.push(+f.lostA > 0 ? "trial A lost " + f.lostA + " acknowledged keys: that is user-space buffering" : "trial A lost nothing: values too small, see the hint"); return s.join(" · "); },
      criteria: ["Trial A (buffered) lost acknowledged keys, and you can say where they were", "Trial B (flushed) lost nothing, three kills out of three", "Trial C timed, and one sentence names the crash fsync protects against (machine, not process)", "--verify reports torn lines and drops them rather than crashing"] },
    { id: "L2", slug: "l2-hashing-and-immutability.html", title: "Hashing, immutability, content addressing",
      tag: "storage",
      blurb: "Store a blob under its hash and it can never go stale. Git's object model, deduplication for free, and why a snapshot is a small manifest rather than a copy.",
      cp: "A chunk store that rebuilds a file byte-for-byte from a manifest, writes one new chunk for a near-duplicate file, and whose checkpoint is about 11 KB against 10 MB of data.",
      how: "Three numbers come out of the mission: how many chunk files the first put created, how many new ones the near-duplicate added, and the size of a checkpoint file. Record them, confirm cmp printed nothing, tick the conditions.",
      cmd: "python chunks.py put big.bin && ls store | wc -l\npython chunks.py put big2.bin && ls store | wc -l      # big2 = big + one appended line\npython chunks.py get big.bin out.bin && cmp big.bin out.bin && echo identical\npython chunks.py checkpoint big.bin v1 && wc -c checkpoints/v1.json\npython chunks.py restore v1 && python chunks.py get big.bin out2.bin && cmp big.bin out2.bin",
      evidence: [
        { key: "chunks1", label: "chunk files after the first put", ph: "e.g. 160 for 10 MB at 64 KB" },
        { key: "chunks_new", label: "new chunk files added by the near-duplicate", ph: "e.g. 1" },
        { key: "cp_bytes", label: "checkpoint file size, bytes", ph: "e.g. 10900" }
      ],
      derived: function (f) { var n = +f.chunks_new, c = +f.cp_bytes; var s = []; if (f.chunks_new !== undefined && f.chunks_new !== "") s.push(n <= 2 ? "dedup works: the near-duplicate cost " + n + " chunk(s)" : n + " new chunks: your change was not at the end, or chunk size differs between puts"); if (c > 0) s.push(c < 20000 ? "a checkpoint is " + c + " bytes (about 160 hashes) for a 10 MB file, which is the whole point" : "checkpoint looks large; it should be a list of hashes, not data"); return s.join(" · "); },
      criteria: ["cmp reports the rebuilt file identical", "Near-duplicate added one new chunk (two at most)", "Checkpoint is a manifest copy of about 11 KB, not a data copy", "restore(label) puts the manifest back and get() then rebuilds the file"] },
    { id: "L3", slug: "l3-object-storage-and-caches.html", title: "Object storage, caches, and easy invalidation",
      tag: "storage",
      blurb: "The S3 model, the latency gap between a local disk and object storage, what a read-through cache is, and why immutable chunks make the hard problem of caching disappear.",
      cp: "The L2 chunk store behind MinIO with a local LRU cache: nothing lost after deleting the cache, warm read at least 10x faster than cold.",
      how: "Time a cold read (empty cache) and a warm read (same file again). Record both in milliseconds; the page computes the speed-up. Then delete the cache directory, read again, and confirm cmp is silent.",
      cmd: "docker run -d --name minio -p 9000:9000 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=minio12345 minio/minio server /data\nrm -rf cache && time python chunks.py --backend s3 get big.bin out.bin     # cold\ntime python chunks.py --backend s3 get big.bin out.bin                     # warm\nrm -rf cache && python chunks.py --backend s3 get big.bin out.bin && cmp big.bin out.bin && echo identical",
      evidence: [
        { key: "cold_ms", label: "cold read, milliseconds", ph: "e.g. 2400" },
        { key: "warm_ms", label: "warm read, milliseconds", ph: "e.g. 90" },
        { key: "inval_lines", label: "lines of cache-invalidation code you had to write", ph: "0" }
      ],
      derived: function (f) { var a = +f.cold_ms, b = +f.warm_ms; if (!(a > 0 && b > 0)) return ""; var r = a / b; return "speed-up: " + r.toFixed(1) + "x" + (r >= 10 ? " (pass)" : " (below 10x: is the cache actually being hit? add a counter)"); },
      criteria: ["Warm read at least 10x faster than cold", "After deleting the cache directory the file still rebuilds identically", "Eviction works: with N set to half the chunk count, cache/ never holds more than N files (step 4)", "No invalidation logic needed, and you can say why in one sentence"] },
    { id: "L4", slug: "l4-replication-by-shipping-a-log.html", title: "Replication by shipping a log",
      tag: "replication",
      blurb: "Leader-based replication as 'ship the log'. Statement, write-ahead and logical log shipping, point-in-time restore, and what Litestream does to SQLite.",
      cp: "Litestream replicating SQLite to MinIO; kill the process, delete the file, restore, and the row count matches the last acknowledged write within one replication interval.",
      how: "Record the last row count the writer printed before you killed everything, the row count in the restored database, and Litestream's sync interval. The gap between the two counts is replication lag; it must be no more than one interval's worth of writes.",
      cmd: "litestream replicate -config litestream.yml      # terminal 1\npython writer.py                                    # terminal 2: one row per second, prints the count after each commit\n# after a minute kill both, then:\nrm app.db app.db-wal app.db-shm && litestream restore -config litestream.yml -o restored.db app.db\nsqlite3 restored.db 'select count(*) from rows'\nlitestream restore -config litestream.yml -timestamp <30 s before the kill> -o then.db app.db",
      evidence: [
        { key: "acked_rows", label: "last row count the writer printed", ph: "e.g. 143" },
        { key: "restored_rows", label: "row count in the restored database", ph: "e.g. 142" },
        { key: "interval_s", label: "Litestream sync interval, seconds", ph: "1" },
        { key: "pit_rows", label: "rows in the point-in-time restore (30 s before the kill)", ph: "e.g. 113" }
      ],
      derived: function (f) { var a = +f.acked_rows, b = +f.restored_rows, s = +f.interval_s || 1; if (!(a > 0 && b >= 0)) return ""; var gap = a - b; return "replication lag: " + gap + " row(s)" + (gap <= s ? " (within one interval: pass)" : " (more than one interval of writes lost: check the interval setting or that replicate was running)"); },
      criteria: ["Restored row count within one replication interval of the acknowledged count", "Point-in-time restore has about 30 fewer rows, matching the timestamp", "You can name which of statement, write-ahead or logical log shipping Litestream does, and why", "Stretch, optional: WAL header and frame headers read with struct"] },
    { id: "L5", slug: "l5-snapshots-and-copy-on-write.html", title: "Snapshots, copy-on-write, forking",
      tag: "storage",
      blurb: "Overlay filesystems, copy-on-write block devices, why a virtual-machine snapshot takes milliseconds, why forking from a snapshot is cheap, and why Sprites can't fork yet.",
      cp: "Three overlay mounts over one unchanged lower directory, each upper holding only its own diff; then fork() added to the chunk store with shared chunks counted.",
      how: "This rung's check is mostly yes/no, plus one count. After editing through the three merged views: diff the lower directory against the copy you made before (must print nothing), count files in each upper directory, and on the Mac count shared chunks after fork() in chunks.py.",
      cmd: "mkdir /ov && mount -t tmpfs tmpfs /ov && cd /ov      # inside: docker run --rm -it --privileged ubuntu bash\ncp -r lower lower.orig && mount -t overlay overlay -o lowerdir=lower,upperdir=upper1,workdir=work1 merged1   # x3\necho changed > merged1/a.txt; echo changed > merged2/b.txt; echo changed > merged3/c.txt\ndiff -r lower lower.orig && echo 'lower unchanged'; ls upper1 upper2 upper3\npython chunks.py fork v1 big-fork && python chunks.py put big-fork.bin --as big-fork && python chunks.py shared big.bin big-fork   # on the Mac",
      evidence: [
        { key: "lower_diff", label: "files diff -r reported changed in lower/", ph: "0" },
        { key: "upper_files", label: "files in upper1, upper2, upper3", ph: "1, 1, 1" },
        { key: "shared", label: "chunks shared between the original and the fork, out of total", ph: "e.g. 159 of 160" }
      ],
      derived: function (f) { if (f.lower_diff === undefined || f.lower_diff === "") return ""; return +f.lower_diff === 0 ? "lower is untouched: copy-on-write did its job" : "lower changed: you wrote to lower/ directly instead of through merged/"; },
      criteria: ["lower/ is byte-unchanged after all three edits", "Each upper directory holds only the file changed through its own merged view", "fork() in chunks.py shares all but the changed chunks with the original", "Two sentences written on why Sprites can't fork from a checkpoint yet (from the community thread reading)"] },
    { id: "L6", slug: "l6-gossip-and-service-discovery.html", title: "Gossip, membership, service discovery",
      tag: "distributed systems",
      blurb: "How a fact spreads across a fleet in a logarithmic number of rounds, SWIM-style failure detection, what a CRDT is, and how a Sprite's URL finds its host.",
      cp: "Maelstrom set up and Echo passing; Gossip Glomers broadcast 3a and 3b valid; 3c (partitions) and the ten-line Corrosion mapping as the second-week stretch.",
      how: "Maelstrom prints 'Everything looks good!' when a workload is valid, then a results block. Record the verdict for echo, 3a, 3b and (stretch) 3c. For 3c also copy :msgs-per-op from under :net :servers in that block; Glomers 3d later asks you to lower it, here it is just recorded.",
      cmd: "./maelstrom test -w echo --bin ./echo.py --node-count 1 --time-limit 10                                     # echo\n./maelstrom test -w broadcast --bin ./broadcast.py --node-count 1 --time-limit 20 --rate 10                 # 3a\n./maelstrom test -w broadcast --bin ./broadcast.py --node-count 5 --time-limit 20 --rate 10                 # 3b\n./maelstrom test -w broadcast --bin ./broadcast.py --node-count 5 --time-limit 20 --rate 10 --nemesis partition   # 3c",
      evidence: [
        { key: "verdicts", label: "Maelstrom verdict for echo, 3a, 3b, 3c", ph: "valid, valid, valid, (stretch)" },
        { key: "msgs_per_op", label: "3c: :msgs-per-op from the results block", ph: "e.g. 24" },
        { key: "mapping_lines", label: "lines written mapping your broadcast onto Corrosion", ph: "10" }
      ],
      derived: null,
      criteria: ["Maelstrom installed and Echo valid", "3a valid (single node)", "3b valid (five nodes, every node sees every message)", "Stretch: 3c valid under partitions (retries plus idempotent receipt), and ten lines mapping your design onto Corrosion"] },
    { id: "L7", slug: "l7-capabilities-not-credentials.html", title: "Capabilities, not credentials",
      tag: "security",
      blurb: "Holding a secret versus holding the right to use it. Token brokers, why an agent's machine should never contain the API key, and how Sprites Connectors do this.",
      cp: "A fake upstream that demands a Bearer key, a 100-line broker that injects it for one allowed host, and a toy agent running as another user that gets 200 through the broker and cannot read the key from env, disk or /proc.",
      how: "Two facts to record: the HTTP status the agent got through the broker (must be 200), and how many ways you tried to read the key from the agent's side versus how many succeeded (must be zero). List the attempts in the note. All of it runs inside one Ubuntu container as two users; see the mission.",
      cmd: "# inside: docker run --rm -it ubuntu bash; apt update && apt install -y python3 && useradd -m agent\nREAL_KEY=sk-ladder-test python3 upstream.py &      # as root: fake API, wants Authorization: Bearer <key>\nREAL_KEY=sk-ladder-test python3 broker.py &        # as root: injects the key for 127.0.0.1:9000 only\nsu agent -c 'env -i PATH=$PATH API_BASE=http://127.0.0.1:8787 python3 agent.py'                  # the call: expect 200\nsu agent -c 'env -i PATH=$PATH API_BASE=http://127.0.0.1:8787 python3 agent.py --try-to-leak'    # env, files, /proc/<broker pid>/environ",
      evidence: [
        { key: "status", label: "HTTP status the agent received via the broker", ph: "200" },
        { key: "attempts", label: "leak attempts tried", ph: "e.g. 4" },
        { key: "leaked", label: "leak attempts that printed the key", ph: "0" }
      ],
      derived: function (f) { if (f.leaked === undefined || f.leaked === "") return ""; return +f.leaked === 0 ? "the agent never saw the key: this is what a Connector gives a Sprite" : "the key leaked. Most likely both processes run as the same user, so /proc/<pid>/environ is readable; run the broker as another user or in another container"; },
      criteria: ["The agent gets 200 through the broker (and 401 if it calls the upstream directly without the key)", "Every leak attempt failed: env, filesystem search, /proc/<broker pid>/environ", "The broker allows exactly one upstream host and logs each call", "Agent and broker run as different users"] },
    { id: "L8", slug: "l8-read-it-again.html", title: "Read it again, then the sources",
      tag: "synthesis",
      blurb: "The explainer end to end with the quiz, then the two Fly.io posts, the Sprites docs, and the four Sprites blog posts that map onto the showcase project.",
      cp: "Explainer quiz at least 4 of 5 taken cold, and a one-paragraph summary of the storage stack written from memory that a stranger followed with at most two questions.",
      how: "Take the explainer's quiz cold and record the score. Then write the storage-stack paragraph from memory and test it on someone (or on Claude with the explainer hidden): record how many sentences they asked you to clarify. Finally count the things you still can't explain; that list is the next season's reading.",
      cmd: null,
      evidence: [
        { key: "quiz", label: "quiz score, correct out of 5 (pass is 4)", ph: "e.g. 4/5" },
        { key: "unclear", label: "sentences the stranger asked you to clarify (pass is 2 or fewer)", ph: "e.g. 1" },
        { key: "gaps", label: "things you still can't explain (count; list them in the note)", ph: "e.g. 2" }
      ],
      derived: null,
      criteria: ["Quiz taken cold, at least 4 of 5", "Storage-stack paragraph written from memory and tested on a stranger, at most two sentences questioned", "The two Fly.io posts, the docs page and the four blog posts read", "Remaining gaps listed by name"] }
  ];

  var PAGES = [
    { slug: "index.html", title: "Start here" },
    { slug: "explainer.html", title: "The explainer (what the ladder leads to)" },
    { slug: "explainer-map.html", title: "Map: explainer sections → rungs" },
    { slug: "showcase.html", title: "Showcase: course from a link" },
    { slug: "publishing.html", title: "Publishing: the series and its title" }
  ];

  /* ------------------------------------------------------------- state */

  function blank() { return { v: 1, levels: {}, days: [], ticks: {}, notes: {} }; }

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return blank();
      var s = JSON.parse(raw);
      if (!s || !s.levels) return blank();
      if (!s.days) s.days = [];
      if (!s.ticks) s.ticks = {};
      if (!s.notes) s.notes = {};
      return s;
    } catch (e) { return blank(); }
  }

  function save(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); }
    catch (e) { alert("Could not save progress: " + e.message); }
  }

  function today() { return new Date().toISOString().slice(0, 10); }

  function touch(s) {
    var d = today();
    if (s.days.indexOf(d) === -1) s.days.push(d);
  }

  function lvl(s, id) {
    if (!s.levels[id]) s.levels[id] = { done: false, attempts: [] };
    if (!s.levels[id].attempts) s.levels[id].attempts = [];
    return s.levels[id];
  }

  function status(s, i) {
    var e = s.levels[CURRICULUM[i].id];
    if (e && e.done) return "done";
    if (i === 0) return "ready";
    var prev = s.levels[CURRICULUM[i - 1].id];
    return (prev && prev.done) ? "ready" : "locked";
  }

  /* ----------------------------------------------------------- sidebar */

  var DOTS = { done: "●", ready: "▸", locked: "○" };

  function here() {
    var p = location.pathname.split("/").pop();
    return p === "" ? "index.html" : p;
  }

  function buildSidebar() {
    var s = load(), cur = here(), i, st, done = 0;
    for (i = 0; i < CURRICULUM.length; i++) if (status(s, i) === "done") done++;

    var h = '<a class="brand" href="index.html">Sprites ladder'
          + '<span>what to learn before the explainer makes sense</span></a>'
          + '<div class="meter"><div class="bar"><i style="width:'
          + Math.round(100 * done / CURRICULUM.length) + '%"></i></div>'
          + '<div class="txt"><span>' + done + ' / ' + CURRICULUM.length + ' rungs</span>'
          + '<span>' + s.days.length + ' day' + (s.days.length === 1 ? "" : "s") + ' active</span>'
          + '</div></div><h4>Rungs</h4>';

    for (i = 0; i < CURRICULUM.length; i++) {
      var L = CURRICULUM[i];
      st = status(s, i);
      h += '<a class="lvl ' + st + (L.slug === cur ? " current" : "") + '" href="' + L.slug + '">'
        + '<span class="dot">' + DOTS[st] + '</span>'
        + '<span class="n">' + L.id + '</span>'
        + '<span class="t">' + L.title + '</span></a>';
    }

    h += "<h4>Reference</h4>";
    for (i = 0; i < PAGES.length; i++) {
      h += '<a class="pg' + (PAGES[i].slug === cur ? " current" : "") + '" href="'
        + PAGES[i].slug + '">' + PAGES[i].title + "</a>";
    }
    h += '<div class="tools">'
      + '<button data-act="export">Export</button>'
      + '<button data-act="import">Import</button>'
      + '<button data-act="reset">Reset</button></div>';

    var el = document.getElementById("sidebar");
    if (!el) { el = document.createElement("nav"); el.id = "sidebar"; document.body.insertBefore(el, document.body.firstChild); }
    el.innerHTML = h;
    document.body.classList.add("has-sidebar");

    if (!document.getElementById("navtoggle")) {
      var b = document.createElement("button");
      b.id = "navtoggle"; b.textContent = "≡ Menu";
      b.onclick = function () { el.classList.toggle("open"); };
      document.body.insertBefore(b, document.body.firstChild);
    }

    if (el.dataset.wired) return;
    el.dataset.wired = "1";
    el.addEventListener("click", function (ev) {
      var act = ev.target && ev.target.getAttribute("data-act");
      if (!act) return;
      if (act === "export") {
        var blob = new Blob([JSON.stringify(load(), null, 2)], { type: "application/json" });
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "sprites-ladder-progress-" + today() + ".json";
        a.click();
      } else if (act === "import") {
        var inp = document.createElement("input");
        inp.type = "file"; inp.accept = ".json";
        inp.onchange = function () {
          var f = inp.files[0]; if (!f) return;
          var r = new FileReader();
          r.onload = function () {
            try { save(JSON.parse(r.result)); location.reload(); }
            catch (e) { alert("That is not a progress file: " + e.message); }
          };
          r.readAsText(f);
        };
        inp.click();
      } else if (act === "reset") {
        if (confirm("Erase all rung checkpoints, ticks and attempt history? Export first if you want it back.")) {
          localStorage.removeItem(KEY); location.reload();
        }
      }
    });
  }

  /* -------------------------------------------------------- roadmap tree */

  function buildTree() {
    var mount = document.getElementById("tree");
    if (!mount) return;
    var s = load(), h = "", i;
    for (i = 0; i < CURRICULUM.length; i++) {
      var L = CURRICULUM[i], st = status(s, i), e = s.levels[L.id];
      var label = st === "done" ? "passed" : (st === "ready" ? "next up" : "not yet");
      if (st === "done" && e && e.doneAt) label = "passed · " + e.doneAt;
      h += '<a class="card ' + st + '" href="' + L.slug + '">'
        + '<span class="hd"><span class="lv">' + L.id + " · " + L.tag + "</span>"
        + '<span class="ti">' + L.title + "</span>"
        + '<span class="st">' + label + "</span></span>"
        + "<p>" + L.blurb + "</p>"
        + '<div class="cp"><b>To pass:</b> ' + L.cp + "</div></a>";
    }
    mount.innerHTML = h;
  }

  /* ---------------------------------------------------- checkpoint widget */

  function esc(t) {
    return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderCp(mount) {
    var id = mount.getAttribute("data-level");
    var L = null, i;
    for (i = 0; i < CURRICULUM.length; i++) if (CURRICULUM[i].id === id) L = CURRICULUM[i];
    if (!L) return;
    var s = load(), e = lvl(s, id);
    e.evidence = e.evidence || {};

    var h = '<h3>Checkpoint · ' + L.id
          + (e.done ? '<span class="badge">passed</span>' : "") + "</h3>"
          + "<p><b>Passed means:</b> " + L.cp + "</p>"
          + '<p class="how">' + L.how + "</p>";
    if (L.cmd) h += '<div class="cmd"><div class="cmdlabel">What produces the evidence</div><pre><code>' + esc(L.cmd) + "</code></pre></div>";

    h += '<div class="fields">';
    for (i = 0; i < L.evidence.length; i++) {
      var f = L.evidence[i];
      h += '<label class="field"><span>' + f.label + '</span>'
        + '<input type="text" data-f="' + f.key + '" value="' + esc(e.evidence[f.key] || "") + '" placeholder="' + esc(f.ph) + '"></label>';
    }
    h += "</div>";
    var derived = L.derived ? L.derived(e.evidence) : "";
    h += '<p class="derived"' + (derived ? "" : ' hidden') + '>' + esc(derived) + "</p>";

    h += '<div class="criteria"><b>Conditions</b><ul>';
    for (i = 0; i < L.criteria.length; i++) {
      var tid = id + "-crit-" + (i + 1);
      h += '<li><label><input type="checkbox" data-crit="' + tid + '"' + (s.ticks[tid] ? " checked" : "") + '> <span>' + L.criteria[i] + "</span></label></li>";
    }
    h += "</ul></div>";

    h += '<div class="row">'
      + '<input type="text" data-f="note" placeholder="one line: what you built or changed this time, and what surprised you">'
      + '<button data-a="log">Log this run</button>'
      + '<button class="ghost" data-a="done">' + (e.done ? "Mark not passed" : "Mark passed") + "</button></div>";

    if (e.attempts.length) {
      h += '<div class="log"><b>' + e.attempts.length + " run" + (e.attempts.length === 1 ? "" : "s") + " logged</b><ol>";
      for (i = e.attempts.length - 1; i >= 0; i--) {
        var a = e.attempts[i], parts = [];
        if (a.fields) for (var k = 0; k < L.evidence.length; k++) { var fk = L.evidence[k].key; if (a.fields[fk]) parts.push(L.evidence[k].label.split(",")[0] + " " + esc(a.fields[fk])); }
        else if (a.score) parts.push(esc(a.score));
        h += "<li><b>" + parts.join(" · ") + "</b>" + (a.note ? " — " + esc(a.note) : "") + " <time>" + esc(a.at) + "</time></li>";
      }
      h += "</ol></div>";
    }

    mount.className = "cpw" + (e.done ? " is-done" : "");
    mount.innerHTML = h;

    // evidence fields save as you type and recompute the derived line
    var inputs = mount.querySelectorAll('.fields input[data-f]');
    for (i = 0; i < inputs.length; i++) inputs[i].addEventListener("input", function (ev) {
      var st = load(), en = lvl(st, id); en.evidence = en.evidence || {};
      en.evidence[ev.target.getAttribute("data-f")] = ev.target.value.trim();
      save(st);
      var d = L.derived ? L.derived(en.evidence) : "", el = mount.querySelector(".derived");
      el.textContent = d; el.hidden = !d;
    });
    var crits = mount.querySelectorAll('input[data-crit]');
    for (i = 0; i < crits.length; i++) crits[i].addEventListener("change", function (ev) {
      var st = load(), tid = ev.target.getAttribute("data-crit");
      if (ev.target.checked) st.ticks[tid] = today(); else delete st.ticks[tid];
      touch(st); save(st); buildSidebar();
    });
    mount.querySelector('[data-a="log"]').onclick = function () {
      var st = load(), en = lvl(st, id), any = false, fields = {};
      for (var k in (en.evidence || {})) if (en.evidence[k]) { fields[k] = en.evidence[k]; any = true; }
      if (!any) { alert("Fill in at least one evidence field first. A run without its numbers is a feeling."); return; }
      en.attempts.push({ at: today(), fields: fields, note: mount.querySelector('[data-f="note"]').value.trim() });
      touch(st); save(st); renderCp(mount); buildSidebar();
    };
    mount.querySelector('[data-a="done"]').onclick = function () {
      var st = load(), en = lvl(st, id);
      if (!en.done) {
        var missing = 0;
        for (var c = 0; c < L.criteria.length; c++) if (!st.ticks[id + "-crit-" + (c + 1)]) missing++;
        if (missing && !confirm(missing + " condition" + (missing === 1 ? "" : "s") + " not ticked. Mark passed anyway?")) return;
      }
      en.done = !en.done;
      en.doneAt = en.done ? today() : null;
      touch(st); save(st); renderCp(mount); buildSidebar(); buildTree();
    };
  }

  function buildCheckpoints() {
    var ms = document.querySelectorAll("[data-level]");
    for (var i = 0; i < ms.length; i++) renderCp(ms[i]);
  }

  /* ------------------------------------------------------------ ticks */
  /* Any <input type="checkbox" data-tick="L0-read-1"> persists. */

  function buildTicks() {
    var s = load();
    var boxes = document.querySelectorAll('input[type="checkbox"][data-tick]');
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i], id = b.getAttribute("data-tick");
      b.checked = !!s.ticks[id];
      if (b.checked && b.parentNode) b.parentNode.classList.add("ticked");
      b.addEventListener("change", function (ev) {
        var st = load(), tid = ev.target.getAttribute("data-tick");
        if (ev.target.checked) st.ticks[tid] = today(); else delete st.ticks[tid];
        if (ev.target.parentNode) ev.target.parentNode.classList.toggle("ticked", ev.target.checked);
        touch(st); save(st); buildSidebar();
      });
    }
  }

  /* ------------------------------------------------------------ notes */
  /* Any <textarea data-note="..."> or <input data-note="..."> persists as you type. */

  function buildNotes() {
    var s = load();
    var els = document.querySelectorAll('[data-note]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i], id = el.getAttribute("data-note");
      if (s.notes[id]) el.value = s.notes[id];
      el.addEventListener("input", function (ev) {
        var st = load(), nid = ev.target.getAttribute("data-note"), v = ev.target.value;
        if (v.trim()) st.notes[nid] = v; else delete st.notes[nid];
        touch(st); save(st);
      });
    }
  }

  /* ---------------------------------------------------------------- pager */

  function buildPager() {
    var f = document.querySelector("footer.pager[data-auto]");
    if (!f) return;
    var cur = here(), i, idx = -1;
    for (i = 0; i < CURRICULUM.length; i++) if (CURRICULUM[i].slug === cur) idx = i;
    var prev = idx > 0 ? CURRICULUM[idx - 1] : (idx === 0 ? { slug: "index.html", title: "Start here", id: "" } : null);
    var next = idx >= 0 && idx < CURRICULUM.length - 1 ? CURRICULUM[idx + 1] : null;
    f.innerHTML =
      (prev ? '<a href="' + prev.slug + '">← ' + (prev.id ? prev.id + " · " : "") + prev.title + "</a>" : "<span></span>")
      + (next ? '<a href="' + next.slug + '">' + next.id + " · " + next.title + " →</a>" : "<span></span>");
  }

  function init() { buildSidebar(); buildTree(); buildCheckpoints(); buildTicks(); buildNotes(); buildPager(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();

  window.SL = { load: load, save: save, curriculum: CURRICULUM };
})();
