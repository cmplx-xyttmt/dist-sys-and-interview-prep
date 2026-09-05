# Interview Prep + Distributed Systems Roadmap

> **Owner:** Isaac Owomugisha · **Started:** July 6, 2026 · **Restarted:** Sep 4, 2026 (see §0)
> **Goal:** Interview-ready for senior (L5/E5) backend roles at FAANG-tier and strong non-FAANG companies.
> **Checkpoints are scoreboard triggers now, not dates** (§5). Projections at the current
> cadence: *applications open* ~Feb 2027 · *minimum viable readiness* ~Mar 2027 · *full
> readiness* ~mid-2027. A dedicated prep season (realistic after the edtech MVP ships)
> pulls all three in.

---

## 0. Reset — Sep 4, 2026

The first two months didn't go to this plan, and pretending otherwise would poison every
date below. Where Jul 6 – Sep 3 actually went: the ICPC/Huawei challenge push, two
hackathons (one killed deliberately, one not submitted), the Kaggriculture baseline bot,
and a full recovery week (Aug 30 – Sep 3). Scoreboard on restart day: 0/130 problems,
0 DDIA chapters, no Glomers, course not taken.

Not zero value, though. The video-streaming/DRM design note and `sprites-explainer.html`
(the seed of what is now exploration #1) both landed, and the ICPC/hackathon work itself
is behavioral-story and "efficiency under constraints" material.

Two structural changes, baked into everything below:

- **Hours follow the WEEK.md season, not this file.** Prep lives in the sharpening slots
  (~5–8 h/wk right now), not the imagined 12–15. This roadmap orders the material and
  defines the triggers; WEEK.md decides each week.
- **Checkpoints are scoreboard triggers, not calendar dates.** The stage dates in §5 are
  projections at the current cadence, re-estimated at every season boundary.

Current slots (season of Sep 4–13; the CodinGame contest is the primary block):

- **DSA** — daily 45 min, ~09:00. The one non-negotiable prep block.
- **System design** — Sunday half-day deep-dive (blog post → mini-visualization; doubles as §8).
- **From Sep 14:** work returns as the morning block; sharpening drops to one rotating
  slot per day (DSA ↔ security ↔ system design) plus the Sunday half-day.

---

## 1. Who this plan is for (honest starting position)

- **8 years of experience** → you'll be evaluated at the **senior bar**. System design and behavioral rounds carry as much weight as coding — a flawless coding loop with a weak design round means a down-level or a reject.
- **Strengths to lean on:** production AI/LLM systems (RAG, agent pipelines, cost optimization), Celery/Redis async architecture, Kubernetes, real migrations (Sagemaker→Vertex, self-hosted→AWS IoT), team leadership and mentorship. This is *exactly* what the new AI-enabled interview formats and "design a RAG pipeline" questions reward.
- **Declared weakest area:** system design → it gets the largest sustained time share.
- **Interview language: Python.** Go is for *learning distributed systems deeply*, not for interviews. Never mix these goals up in a timed round.
- **Location reality (Kampala):** most FAANG roles will mean relocation + visa sponsorship (Google Zurich/London/Warsaw, Meta London, Amazon Dublin/EU, Canada offices) — plus a parallel track of strong remote-first companies (Canonical, GitLab, Cloudflare, Fly.io, Grafana, Ably, etc.). Factor visa timelines into when you apply.

**Time budget (revised Sep 4, 2026):** prep runs on WEEK.md's sharpening slots — the daily
45-min DSA block plus the Sunday half-day deep-dive, ~5–8 focused hrs/week. 2brain-cc is
parked (§7). The original 12–15 hrs/week returns only when a dedicated prep season is
scheduled in WEEK.md (realistic after the edtech MVP ships) — and the §5 projections
compress by roughly half when it does.

---

## 2. The five tracks

| Track | What | Time share (early → late) |
|---|---|---|
| **A. Coding / DSA** | Pattern fluency in Python, timed practice, AI-enabled round drills | 35% → 25% |
| **B. System design** | DDIA (2nd ed) + interview-format practice + weekly design write-ups | 25% → 35% |
| **C. Distributed systems hands-on** | Go + Gossip Glomers (Python first, then Go) | 25% → 15% |
| **D. Behavioral** | Senior-bar story bank (STAR), leadership narratives | 5% → 15% |
| **E. Applications & logistics** | Resume, referrals, pipeline, company research | 10% (spiky) |

Track C is the *engine* for Track B: Glomers challenges turn DDIA theory into scar tissue you can cite in design interviews ("when I implemented gossip broadcast, the naive fanout melted under partition — here's what fixed it").

---

## 3. Track details

### A — Coding / DSA (Python)

- **Curated list, not volume:** work through **NeetCode 150** (superset of Blind 75), organized by pattern. Target ~130–150 problems total across the stages, each *understood*, not just passed.
- **Pattern order:** arrays/hashing → two pointers → sliding window → stack/monotonic stack → binary search → linked list → trees → tries → heaps → graphs (BFS/DFS/topo-sort/union-find) → backtracking → 1D/2D DP → intervals → greedy.
- **Rules of engagement:**
  - Timed from day one: 25 min mediums, 40 min hards. Struggle 20 min before hints.
  - Every solved problem gets a 2-line note in `dsa/`: pattern + the insight you missed.
  - **Spaced re-solves:** redo failed problems at +3 days and +2 weeks.
- **Go cross-training (optional, capped, deferred):** re-solve ~15–20 *easy* problems in Go purely for syntax muscle memory (slices, maps, structs) — now tied to the Go on-ramp in Stage 4 (§3C). All timed DSA is Python.

### B — System design

- **Primary text: DDIA 2nd edition** — but *actively*: each chapter produces a 1-page note in `notes/ddia/` answering "what interview question does this chapter arm me for?"
- **Interview-format layer** (DDIA is theory; interviews are a timed 35–45 min performance):
  - **Hello Interview** (learn their delivery framework + do their guided practice) and/or **System Design Interview vol 1 & 2 (Alex Xu)** for the question catalog.
  - **Jordan Has No Life** (YouTube) for the DDIA-flavored deep dives.
- **The 4-step skeleton to drill until automatic:**
  1. Requirements + scale estimates (QPS, storage, bandwidth — do the arithmetic out loud)
  2. API + data model
  3. High-level component diagram (write path / read path / async path — separately)
  4. Deep dives: bottlenecks, failure modes, consistency trade-offs
- **Cadence:** design work lives in the Sunday half-day, alternating with Glomers (§3C). Written designs (in `system-design/designs/`) from Stage 2; *timed verbal* designs from Stage 3 (talk to a wall, record yourself, or mock).
- **Memorize the math of scale:** latency numbers table, IOPS (NVMe ~100K+ vs HDD ~200), 1 Gbps ≈ 125 MB/s, back-of-envelope QPS→shards reasoning.
- **Your unfair advantage:** AI-system design (RAG pipelines, embedding/vector-DB sharding, inference latency vs token cost, prompt caching economics). Prepare 2–3 of these deeply — you've *built* them at Tunga; most candidates have only read about them.

### C — Distributed systems hands-on (Go + Gossip Glomers)

- **Cadence (revised Sep 4):** the Sunday half-day **alternates** — one week a design
  deep-dive/exploration (§3B, §8), the next a Glomers challenge in Python. The mapped DDIA
  reading happens before that Sunday. Half the old speed, but the DDIA→Glomers pairing
  survives.
- **Go on-ramp — deferred to Stage 4**, when a dedicated hands-on block exists (post-MVP):
  A Tour of Go → Effective Go → Exercism Go track (~15–20 exercises), then **Concurrency in
  Go** (Cox-Buday) alongside the backfill — goroutines, channels, `sync.Mutex`/`WaitGroup`,
  race detector. Until then, Glomers is Python-only.
- **Gossip Glomers (fly.io / Maelstrom), each challenge twice:** first in **Python** (nail the distributed logic fast), then in **Go** (learn the concurrency model — Stage 4 backfill). Layout:
  - `glomers/python/challenge-N-name/`
  - `glomers/go/cmd/<name>/` + shared primitives in `glomers/go/pkg/`
- **Challenge ↔ DDIA mapping** (do the reading *before* the challenge):

  | Challenge | DDIA fuel |
  |---|---|
  | 1 Echo | Ch. 4 encoding/JSON over the wire |
  | 2 Unique ID generation | Replication + ordering chapters (why not auto-increment; Snowflake-style IDs) |
  | 3a–e Broadcast | Replication, gossip, unreliable networks; 3d/3e force efficiency under latency budgets |
  | 4 Grow-only counter | Consistency chapters; CRDTs (G-counter) |
  | 5a–c Kafka-style log | Logs, partitioned streams, offsets |
  | 6a–c Totally-available transactions | Transactions + consistency/consensus; read-uncommitted → read-committed |

- **Stretch (only if ahead of schedule):** MIT 6.5840 labs (Raft). Otherwise read the Raft paper + play with the visualization — enough to discuss consensus in interviews.

### D — Behavioral (the senior bar)

- Build **6–8 STAR stories** in `behavioral/story-bank.md` (seeded from your resume already). Must cover: production incident, architectural disagreement resolved with data, mentorship/leadership, delivering under ambiguity, failure + lesson, cross-team influence, deep technical achievement.
- Amazon LP mapping, Meta "Jedi" style (impact, conflict, growth), Google (collaboration, ambiguity).
- Each story: 2–3 min spoken, with *numbers* (you have good ones: 90% cost reduction, 97K plots, 500+ companies/batch).
- From Stage 4: practice out loud weekly; get at least 2 behavioral mocks.

### E — Applications & logistics

- **Stage 2:** resume tailored per role family (backend / AI-platform / infra), LinkedIn refresh, referral hunting (Andela alumni network is genuinely valuable here — many are now at FAANG).
- **Applications trigger (replaces the old "Sept" date):** warm-up tier opens when the
  scoreboard shows **60+ problems · DDIA ch. 1–7 noted · 4+ written designs · 8 stories
  drafted** — projected ~Feb 2027 at the current cadence. Warm-up first: companies you'd
  be happy at but aren't your #1, to convert prep into live-interview calibration.
- **Stage 4:** FAANG applications with referrals; remote-first companies in parallel.
- Track every application in a simple table (company, role, stage, dates, notes). Interview processes take 4–8 weeks — the trigger firing means onsites land ~2 months later, which matches the readiness curve.

---

## 4. The AI-era layer (applies across tracks)

Interviews now come in **two modes**, and you must train both:

1. **Raw mode (still the majority):** no AI, shared editor or whiteboard. All timed DSA practice defaults to this.
2. **AI-enabled mode (growing — Meta's AI-assisted round, many take-homes):** you drive an LLM in an IDE and are graded on *judgment*, not typing:
   - **Task decomposition** — prompt for components ("write the BFS helper with this signature"), not solutions.
   - **Verification discipline** — read every generated line; narrate the bugs you catch (edge cases, off-by-ones, concurrency). *Catching an AI bug out loud is the strongest signal you can send.*
   - **Architecture ownership** — you decide the structure; AI fills in walls.
- **Practice ratio:** ~70% raw / 30% AI-assisted through Stage 3, then ~60/40. For AI-assisted drills, use Claude Code or Cursor on NeetCode problems *and* on small build-tasks ("build a rate limiter with tests in 45 min, AI allowed").
- **Kaggle × Google "5-Day AI Agents: Intensive Vibe Coding" course** — **runs in work
  hours (decision Sep 4):** building agents *is* the Tunga day job, so this and the other
  agentic-engineering shelf material (ADK graph-engineering codelab, twotimespi.dev, the
  PI-agent and effective-agents talks) count as work learning, not prep hours. One-week
  sprint after leave ends (Sep 14+), ~1–2 h/day × 5 days inside the work block, with each
  day's learnings referenced against a live work project (lead-id harness, outreach
  pipeline). Self-paced (the live run was Jun 15–19, 2026; whitepapers, codelabs, and
  recorded livestreams remain available):
  - Day 1 agents & vibe-coding fundamentals · Day 2 tools & interoperability (APIs, code execution, A2A) · Day 3 context engineering (sessions, skills, memory) · Day 4 agent quality & security (testing, guardrails, threat vectors) · Day 5 prototype → production (deployment, debugging, observability).
  - **Why it earns a slot:** it trains exactly the supervise-the-agent skill graded in AI-enabled rounds; days 3–5 map directly onto 2brain Phase 3+ (coach, Agent SDK, memory) and your Tunga agent work; the capstone is a portfolio/exploration artifact.
  - Deliverable: notes in `notes/agents-course.md` + one "what I'd change about how I use Claude Code" retro applied to this repo's workflow.
- **Take-homes:** assume LLM use is allowed unless stated. Differentiate with tests, a crisp README explaining trade-offs, and clean commit history — that's what graders look at now that everyone's code compiles.
- **Meta-skill:** your day job is *building* LLM systems. In behavioral and design rounds, this is a story generator — use it.

---

## 5. Stage schedule

Same material, same order — but the dates are **projections at the current cadence**
(~5–8 prep hrs/week), re-estimated at every WEEK.md season boundary. Stage boundaries
don't gate anything; the triggers do. A dedicated 12–15 hr/week prep season would
compress Stages 2–6 by roughly half.

### Stage 0 — Sep 4 → Sep 13, 2026: Re-entry (contest season)
- The CodinGame contest is the primary block; prep is the sharpening slots only.
- **DSA:** daily 45-min slot restarted Sep 4 (week goal: 6 of 10 days). Arrays/hashing first.
- **System design:** Sunday Sep 6 half-day — Fly.io Sprites deep-dive → exploration #1 (§8).

### Stage 1 — Sep 14 → Nov 8, 2026: Foundations
- **DSA:** arrays/hashing, two pointers, sliding window, stack, binary search (~34 problems, Python, timed).
- **DDIA:** ch. 1–5, 2nd-ed numbering (trade-offs, nonfunctional requirements, data models, storage engines — LSM vs B-tree cold, encoding). Notes per chapter, read ahead of the mapped Sundays.
- **Glomers:** Maelstrom environment set up; Challenge 1 (Echo) and Challenge 2 (Unique IDs) in **Python**, on alternating Sundays. Go on-ramp deferred to Stage 4 (§3C).
- **Logistics:** none yet. Heads-down.

### Stage 2 — Nov 9, 2026 → Jan 3, 2027: Replication
- **DSA:** linked lists, trees, tries, heaps (~36 problems).
- **DDIA:** replication + sharding chapters. This is the heart of interview system design.
- **Glomers:** Broadcast 3a–3e in Python (3d/3e are the efficiency targets — measure, don't guess).
- **System design:** learn the 4-step framework (Hello Interview); first 2 written designs (start easy: rate limiter, URL shortener).
- **Behavioral:** flesh out story bank to 8 drafted stories; identify gaps (need: a failure story, a conflict story).
- **Logistics:** resume + LinkedIn updated; referral list drafted.
- **Kaggle agents course:** runs in *work hours* (§4 — agent-building is the day job); should be done by this stage, notes + retro landed.

### Stage 3 — Jan 4 → Feb 28, 2027: Transactions & consistency · applications trigger
- **DSA:** graphs (BFS/DFS/topo/union-find), backtracking (~28 problems). First timed mock (any platform).
- **DDIA:** transactions, the trouble with distributed systems, consistency & consensus. The hardest and highest-yield reading — go slow, take notes.
- **Glomers:** Challenge 4 (G-counter) + Challenge 5 (Kafka-style log), Python.
- **System design:** 1 written + 1 timed-verbal design per week (Uber-lite, chat system, financial ledger, news feed).
- 🔓 **Applications trigger:** warm-up tier goes out when the scoreboard shows **60+ problems · DDIA ch. 1–7 · 4+ written designs · 8 stories drafted** (projected ~Feb 2027). Their loops become your live mocks.
- **✅ Minimum-viable-readiness checkpoint (end of stage):** most mediums in 25 min; a coherent 40-min design for standard questions; 8 stories ready; Glomers 1–5 done in Python.

### Stage 4 — Mar 1 → Apr 11, 2027: Interview simulation
- **DSA:** DP, intervals, greedy (~37 problems). Weekly timed sets (2 problems / 60 min).
- **DDIA:** batch + stream processing + derived-data chapters (lighter interview weight — read efficiently).
- **Glomers:** Challenge 6 (totally-available transactions) in Python; **Go starts here** — on-ramp (§3C) + backfill Go versions (1–3 and one of 4/5/6).
- **System design:** weekly mocks (peer or paid — Hello Interview / interviewing.io / Pramp). Add **AI-system design** practice: design a RAG pipeline, a semantic-search service, an LLM inference gateway.
- **AI-enabled drills:** weekly 45-min AI-assisted build task.
- **Logistics:** FAANG applications + referrals out. Behavioral mock #1.

### Stage 5 — Apr 12 → May 23, 2027: Sharpening
- **DSA:** review-and-redo stage — re-solve every problem you failed; company-tagged lists for live pipelines.
- **System design:** 2 mocks/week; deep-dive weak spots from mock feedback; live-debugging intuition (read 3–4 public postmortems: AWS, Cloudflare, Google SRE book chapters).
- **Glomers:** performance-tune broadcast (3e) and log (5c) in Go — great "efficiency under constraints" stories.
- **Behavioral:** all stories at 2–3 min spoken, drilled. Behavioral mock #2.
- **Logistics:** interviews likely live this stage. After each real round, write a retro in `PROGRESS.md`.

### Stage 6 — May 24 → Jun 30, 2027: Execution
- Interview execution + spaced review. No new material — only targeted patching of weaknesses exposed by real loops.
- Company-specific tuning per scheduled onsite (Meta: speed + 2 problems/round; Google: depth + follow-ups; Amazon: LP-heavy).
- Keep one build thread alive for sanity — you think better when you're building.

---

## 6. Weekly cadence (season-driven, ~5–8 hrs)

WEEK.md owns the calendar; this only says what the slots hold.

**Contest season (Sep 4–13):**

| Slot | Block | ~Time |
|---|---|---|
| Daily ~09:00 | DSA: 2 timed problems, log in PROGRESS.md | 45 min |
| Sunday morning | System-design deep-dive (Sep 6: Fly.io Sprites) | half-day |

**From Sep 14 (work back; one rotating sharpening slot per day + Sunday):**

| Slot | Block | ~Time |
|---|---|---|
| Rotating daily slot, DSA days (3–4×/wk) | 2 timed problems, or spaced re-solves | 45–60 min |
| Rotating daily slot, other days | Security track (separate plan, not counted here) | 45–60 min |
| Sunday morning, alternating weeks | Design deep-dive / exploration (§8) ↔ Glomers challenge in Python | half-day |
| Sunday tail | DDIA note wrap-up + weekly review in PROGRESS.md + behavioral (from Stage 2) | 45 min |

Miss a day? The DSA slot is the one that survives. Drop re-solves and polish first, never
timed practice; a skipped Sunday gets written in the WEEK.md Log, not silently absorbed.

The old ~13 hr template returns verbatim if a dedicated prep season gets scheduled.

---

## 7. Retention engine — WEEK.md now, 2brain-cc later

2brain-cc is **parked** (WEEK.md, Sep 4, 2026): it resumes once the WEEK habit has stuck
for a few weeks. The anti-abandonment job it was hired for — the known failure mode is
starting strong and drifting, which is exactly what §0 documents happening — is done for
now by the WEEK.md system (/standup, /shutdown, the Log, the seasons) plus this repo:

- **Capture:** DDIA notes in `notes/ddia/`, DSA insights in `dsa/`, weekly entries in
  `PROGRESS.md`.
- **Spaced repetition:** the quiz deck in `roadmap.html` (add 1–3 questions per finished
  chapter or challenge) plus the re-solve dates in `dsa/` notes. This was always the
  fallback; now it's the plan.
- **When 2brain resumes**, Phase 0 inherits all of this material, and the 2brain `/sync`
  design doc (write it after DDIA's replication chapters) still stands — offline-first
  sync, LWW, tombstones, delta endpoints are design-interview topics you'll have
  personally implemented.
- **Priority rule, unchanged at its core:** in a true crunch, live interviews win.

---

## 8. Learning in public — interactive explorations

Writing about what you learn compounds it (retrieval practice + the clearest-explanation test) and builds visibility ahead of applications. The format: **interactive explorations** on [cmplx-xyttmt.github.io](https://cmplx-xyttmt.github.io/) — not prose posts but self-contained interactive pages readers actively work through.

**Cadence (revised Sep 4):** explorations are now the output of the Sunday design deep-dive
(§6), so roughly one per 2–3 Sunday cycles, timeboxed to ~6–8 hrs each (the trap is
polishing explorations instead of prepping — the timebox is the guard). Sprites jumped the
queue because it's this Sunday's deep-dive and already seeded. Candidates in order:

1. **"Computers for agents"** — how Fly.io Sprites work: instant/durable/disposable VMs, the object-storage storage stack (chunks + WAL-shipped metadata + throwaway cache), checkpoint/restore *(seeded in `sprites-explainer.html`; deep-dive **Sunday Sep 6**. Ties Glomers 3 + Corrosion together. Motivated by Fly.io being a target employer — and, since their Jul 24 2026 pivot to "computers for agents" under new CEO Scott Johnston, directly relevant to the lead-id agent harness.)*
2. **"How fast is fast?"** — the math of scale: latency-numbers ordering game + back-of-envelope calculator *(after DDIA ch. 1–4, ~Stage 1–2)*
3. **"Gossip"** — broadcast simulator: watch rumors spread, toggle partitions, tune fanout vs. latency *(after Glomers 3a–e, ~Stage 2–3)*
4. **"Nobody agrees"** — replication conflicts & why unique IDs are hard *(after DDIA replication + Glomers 2/4, ~Stage 3–4)*
5. **"The log"** — Kafka-style partitioned log, offsets, and consumers *(after Glomers 5 — stretch beyond the required 3)*

**Interaction vocabulary to develop** (prototype each in `roadmap.html` first, promote what works to the blog and 2brain):
- **Predict-then-reveal** — reader commits to a guess before the answer appears (forced retrieval beats recognition)
- **Simulations with failure toggles** — kill a node, partition the network, watch the system respond
- **Parameter sliders** — replication factor, fanout, latency budgets; see trade-offs move in real time
- **Mini-games** — ordering/matching under light time pressure (latency ordering, consistency-model matching, spot-the-race-condition)
- **Test-yourself decks** — categorized quizzes with explanations for wrong answers
- **Progressive depth** — skim layer → dig layer → "here's the actual code" layer, reader chooses
- **Export-to-2brain hook** *(future)* — every exploration ends with "save these as spaced-rep cards," wiring the blog into the retention engine

`roadmap.html` (this repo) is the **living testbed**: it tracks the roadmap interactively *and* prototypes these mechanics — quiz deck, mini-game, progress persistence — before they graduate to 2brain or the blog.

---

## 9. Definition of "interview-ready" (exit criteria)

- [ ] 130+ NeetCode problems solved; mediums in ≤25 min at ~80% hit rate
- [ ] 10+ written system designs; 6+ timed verbal/mock designs with feedback
- [ ] DDIA 2nd ed finished with notes; can explain replication, partitioning, transactions, consensus *without notes*
- [ ] Gossip Glomers 1–6 complete in Python; 1–3 + one of {4,5,6} in Go
- [ ] 8 STAR stories drilled to 2–3 min spoken
- [ ] 2+ behavioral mocks, 4+ design mocks, 2+ coding mocks done
- [ ] Comfortable in both raw and AI-assisted coding modes (Kaggle agents course done + retro applied)
- [ ] 3+ interactive explorations published on the blog
- [ ] Application pipeline live with 15+ companies across FAANG / strong-remote / warm-up tiers
