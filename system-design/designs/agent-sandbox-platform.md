# Design rep — Agent Sandbox Platform ("Sprites-style")

> **This is a REP (a written-design repetition), not a study note.** *I* fill this in — Claude
> plays interviewer and probes; Claude does **not** write the design. Counts toward the 10+.
> Background material: `video-streaming-and-drm.md` (unrelated) and `sprites-explainer.html`
> (the domain). Read the explainer *before* if I want; the point of the rep is to reason it out.
>
> **Format:** target 35–45 min if timing it. Follow the 4-step skeleton. Talk/write out loud —
> especially the arithmetic in Step 1.

## The prompt (as an interviewer would give it)

> "Design the compute platform behind an AI-agent product. Users (or their agents) spin up
> **sandboxes** — isolated Linux environments where an agent runs code, edits files, and calls
> tools over a long-running task. Sandboxes must be **fast to create**, keep their **state**
> across pauses, and be **cheap when idle**. Design the platform that provisions, runs,
> persists, and tears them down at scale."

Deliberately open-ended — like a real senior loop. I clarify scope myself.

---

## Step 1 — Requirements + scale estimates  *(do the arithmetic OUT LOUD)*

**Functional (what it must do):**
> _my answer_

**Non-functional (the -ilities + the trade I'm optimizing):**
> _my answer_

**Scale assumptions I'm stating (I pick the numbers, then compute):**
> _my answer — e.g. concurrent sessions, create rate, avg session lifetime, disk/session,_
> _idle:active ratio → derive: peak VMs, storage total, object-storage bandwidth, create QPS_

**Interviewer probes to make sure I answered (don't skip):**
- What's the create-latency budget, and why that number?
- What's the idle:active ratio, and why does it dominate the cost model?
- Storage per sandbox × concurrent × replication = ? Does that fit anywhere sane?
- Is this read-heavy or write-heavy, and where?

---

## Step 2 — API + data model

**Core API (verbs a client/agent calls):**
> _my answer — create / exec / checkpoint / restore / fork / expose-port / destroy …_

**Data model (what the control plane stores):**
> _my answer — sandbox record, state pointer, metadata, ownership, network mapping_

**Interviewer probes:**
- What is the durable "identity" of a sandbox — what exactly persists, and where?
- How does a caller reconnect to a sandbox after it slept?
- Idempotency: what happens if `create` is retried?

---

## Step 3 — High-level components  *(write path / read path / async path SEPARATELY)*

**Provision / create path:**
> _my answer_

**Run + persist path (how state survives pause/idle):**
> _my answer_

**Async / control path (scheduling, sleep/wake, GC, billing):**
> _my answer_

**Interviewer probes:**
- Where does the create-latency go, and how do you get it under budget? (pre-warming?)
- How is state made durable without anchoring a sandbox to one physical host?
- Who decides to put a sandbox to sleep, and how does it wake?

---

## Step 4 — Deep dives: bottlenecks, failure modes, consistency

Pick 3–4 and go deep. Candidates:
> _my answer — e.g.:_
> - _Storage: how do you get durable + fast + cheap at once? (truth vs cache; immutability)_
> - _Cold-start vs warm-pool economics at 10× load_
> - _Failure: a physical host dies with 500 live sandboxes — what happens to each?_
> - _Isolation & security: multi-tenant, agent runs untrusted code, credential brokering_
> - _Checkpoint/restore: what makes it cheap enough to use casually?_
> - _Fleet coordination: how does a new public URL / sandbox location propagate?_

**Interviewer probes:**
- Name the single biggest bottleneck at 10× and defend your fix.
- One consistency trade-off you made — what anomaly did you accept, and why is it OK?
- Where does this design STOP working (the honest limits)?

---

## Self-review rubric (fill after)

- [ ] Did I do real scale arithmetic in Step 1 (not hand-wave)?
- [ ] Did I separate write/read/async paths in Step 3?
- [ ] Did I name a concrete bottleneck and a concrete fix?
- [ ] Did I state at least one explicit consistency/availability trade-off?
- [ ] Did I say where the design breaks?
- [ ] Could I now compare my design to how Fly's Sprites actually did it? (the learning payoff)

## Post-rep notes (gaps to patch, next re-do date)
> _fill in_
