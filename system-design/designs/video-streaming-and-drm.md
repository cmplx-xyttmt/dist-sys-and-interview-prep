# Video streaming + DRM + the piracy adversary — study note

> **What this file is:** a *domain study note* (like a DDIA chapter note), not a finished
> written design. It arms me with the concepts, the scale math, and the questions to drill.
> The actual *timed written design* ("design YouTube/Netflix") is a separate rep I still owe
> myself — don't read this and think the rep is done.
>
> **Interview question this arms me for:** "Design a video streaming platform" (YouTube /
> Netflix / Twitch variants). Top-tier senior prompt, and it hits my weakest area head-on.
>
> **Blog angle:** the security/piracy layer is the *hook* — start with "why is there no
> download button, yet the episode is on a pirate site an hour after it airs?" and let that
> question pull the reader through the whole architecture. Story first, systems underneath.

---

## 0. The story hook (for the blog, and honestly for keeping the design memorable)

Two facts sit in tension and the whole design falls out of resolving them:

1. Netflix/Apple spend enormous effort so you *cannot* trivially save the video file.
2. The video is on a pirate site, in decent quality, remarkably fast.

Neither fact is an accident. Resolving the tension walks you through: adaptive streaming (why
there's no single file), CDN economics (why it's fast and cheap to serve), DRM (why you can't
just save it), and the **trusted-client problem** (why #1 can never fully win). That's the
essay, and it's also a complete system-design answer wearing a story.

---

## 1. How delivery actually works (the thing people call "the video")

**Key insight: there is no single video file.** Streaming is *adaptive bitrate (ABR)*.

- Source is **transcoded into multiple renditions** (e.g. 240p→4K), each at a target bitrate.
- Each rendition is **segmented** into 2–10s chunks (`.ts` for HLS, fMP4 `.m4s` for DASH).
- A **manifest** describes the tree:
  - **HLS** → `.m3u8` playlist (Apple, RFC 8216)
  - **MPEG-DASH** → `.mpd` XML (ISO/IEC 23009-1)
  - master manifest lists renditions + bandwidth; each rendition has a media playlist of
    ordered segment URLs.
- The browser player uses **MSE (Media Source Extensions)** to pull segments and feed the
  buffer, measuring throughput + buffer health between segments and **switching rendition**
  on the fly (that's the "blurry then sharp" moment).

Why this shape (the systems reasoning — this is what the interviewer wants):
- **Edge cacheability** — segments are *immutable static files* → CDN caches them hard at the
  edge. This is the core economic trick: one origin encode, served millions of times from
  cache.
- **Statelessness** — origin holds no per-viewer streaming state; the client drives.
- **Graceful degradation** — bad network → lower rendition, not a stall.

### The upstream pipeline (write path)
`ingest → transcode/encode (fan-out batch job) → package (segment + manifest) → encrypt →
push to origin/CDN`

- Transcode is embarrassingly parallel: split source into chunks, encode chunks across a
  worker fleet, stitch. Classic fan-out/fan-in batch job — good place to talk queues,
  idempotency, and retries.
- **Per-title / per-shot encoding** (Netflix): don't use fixed bitrate ladders; optimize the
  ladder per title (a cartoon needs fewer bits than an action scene) and even per shot. Big
  storage/quality win — a great "deep dive" flex.

---

## 2. Scale math (STEP 1 of my skeleton — do the arithmetic out loud)

This is the part I must be able to do cold. Numbers to anchor on:

- **1 Gbps ≈ 125 MB/s.** A single 1080p stream ≈ 5 Mbps ≈ 0.625 MB/s.
- So **1 Gbps ≈ ~200 concurrent 1080p streams.** 1 Tbps edge ≈ ~200K streams.
- Netflix peak is *tens of Tbps* globally → why they built **Open Connect** (their own CDN
  appliances embedded inside ISPs) instead of renting CDN. Egress at that scale dominates
  cost; caching close to users is existential, not optional.
- **Storage per title**: runtime × bitrate × (sum over renditions) × DRM variants. A 2hr movie
  across ~6 renditions can be hundreds of GB → TB before replication. Multiply by catalog.
- **Read:write ratio** is extreme (write once, read millions). This justifies the whole
  cache-everything design and cheap-origin/expensive-edge split.

> Drill: given "X million concurrent viewers, avg 4 Mbps," compute required edge Tbps and
> number of PoPs. Should be reflex.

---

## 3. The security layer — why you can't just save the segments

If segments were plain HTTP files, ripping = trivial. So:

- **Encryption**: segments encrypted, typically AES-128 under **Common Encryption (CENC,
  ISO/IEC 23001-7)** so one encrypted asset serves multiple DRM systems.
- **DRM systems**: **Widevine** (Google/Chrome/Android), **PlayReady** (MS), **FairPlay**
  (Apple). Manifest points at a **license server**.
- **License exchange**: browser's **CDM (Content Decryption Module)**, driven via **EME
  (Encrypted Media Extensions, W3C)**, sends a license request → license server checks
  entitlement (logged in? subscribed? device allowed?) → returns content keys **into a
  protected environment**, never to the page's JavaScript.
- **Security levels (Widevine L1/L2/L3)**:
  - **L1** — keys + decryption inside a hardware **TEE (Trusted Execution Environment)** the OS
    itself can't read. Decrypted frames go to the display pipeline without touching
    user-addressable memory.
  - **L3** — *software-only*. Reversible given effort; publicly documented breaks exist. This
    is why L3 is **capped at low resolution** (≈≤480/720p) and **4K/HDR is contractually
    gated to L1**.
- **Output protection**: **HDCP** on HDMI/DisplayPort aims to stop capture downstream at the
  cable.

Legit path end-to-end: `entitlement → license → keys in black box → decrypt → decode →
display`, ideally with no point where high-res cleartext sits where a user can copy it.

---

## 4. The adversary — two separate questions

### 4a. Why the *sites* are hard to take down (infrastructure, not clever code)
The theme is **indirection + jurisdiction + cost asymmetry**.

- **Index ≠ content.** The frontend site usually hosts *no video*; it iframes a player from
  interchangeable third-party file hosts. Kill the frontend, content survives, and vice versa.
- **CDN fronting** (Cloudflare et al.) hides the origin IP → you can't find what to subpoena.
  Also gives them free DDoS protection + edge caching (same properties Netflix uses, aimed
  differently).
- **Bulletproof/offshore hosting** in non-cooperative jurisdictions + domain privacy.
- **Domain hopping** (`.pro`/`.to`/`.cc`, number-prefix churn) — audience follows the brand;
  it's a hydra. (This is why the URL "might be different.")
- **Fast-flux DNS** — rapidly rotating A-records → IP blocking is like hitting water.
- **The asymmetry**: a takedown is slow, per-target, jurisdiction-bound (O(hard)); a new
  mirror is a push + DNS change (O(cheap)). Same reason spam/phishing persist.
- **What actually works** attacks the *periphery*, not content: court-ordered ISP DNS
  blocking, payment-processor/ad-network cutoffs (starve revenue), search de-indexing.

### 4b. How content leaks despite DRM (best→worst quality)
Leaks happen at the **weakest link**, and there's always one because the video must become
visible to a human.

- **Pre-release / insider sources** — screeners, post-production copies, compromised vendors.
  Many earliest HQ leaks are *inside jobs*; no DRM was "broken" — the copy leaked beside the
  protected path.
- **Weak DRM tiers** — Widevine **L3** software black box → reversible → low-res leaks. (Why
  studios cap L3 resolution.)
- **The analog/display hole** — the fundamental one. To be watched it must be decoded + shown;
  anything displayable can be re-captured. HDCP is a speed bump, not a wall. Information-
  theoretically, a visible signal can be re-recorded.
- **Endpoint compromise** — DRM trusts *some* client component (TEE/OS/CDM). Rooted devices,
  modified players, extracted CDM secrets attack that. Constant key-revoke / re-extract
  cat-and-mouse.

### The unifying principle (the essay's thesis + a real security law)
**The trusted-client problem / analog hole:** *you cannot hand someone the ciphertext, the
key, and the means to decrypt, and also stop them keeping the plaintext.* DRM doesn't make
copying impossible — it makes it inconvenient/expensive enough that most people pay, and keeps
the high-value tiers (4K/HDR) costly enough to leak that the exclusivity window retains value.
**It's economics enforced by engineering, not prevention.** Generalizes far past video: software
licensing, API abuse, client-side rate limiting, "never trust client-reported data."

---

## 5. The interview skeleton, as PROMPTS (my rep — answer these out loud, timed)

Don't read answers here — this is the drill. 4-step framework from ROADMAP §B:

1. **Requirements + scale**: functional (upload/ingest, transcode, browse, adaptive playback,
   DRM/entitlement, resume, offline download). Non-functional (availability > consistency for
   playback; low startup latency; global). *Do the Tbps + storage math out loud.*
2. **API + data model**: `GET /manifest/{title}/{profile}`, `POST /license` (entitlement),
   catalog/metadata store, per-title encode ladder metadata. What's the CDN URL scheme?
3. **Components — three paths separately**:
   - *write*: ingest → transcode fan-out → package → encrypt → origin
   - *read*: client → manifest → CDN edge (cache hit path) → origin miss
   - *async*: encode jobs, catalog indexing, recommendation, analytics
4. **Deep dives / probes to answer**:
   - Where's the bottleneck at 10× traffic? (egress → CDN tiering, Open-Connect-style embeds)
   - Cache hit ratio math — what's the origin offload? What's the long-tail (cold catalog)?
   - Failure: an edge PoP dies mid-stream — what does the client do? (rendition/host failover)
   - Consistency: is stale manifest OK? (yes, mostly — immutable segments help)
   - Live vs VOD: what changes? (low-latency HLS/DASH, sliding window, smaller segments)
   - Security deep dive: how does entitlement gate keys without leaking them to JS?
   - **AI-flavored flex** (my unfair advantage): recommendation/thumbnail selection, per-shot
     encode optimization as an ML problem, abuse detection on leak fingerprints (watermarking).

> **Forensic watermarking** is the one countermeasure that *does* fit the analog hole: embed a
> per-session invisible ID so a leaked copy traces back to the account/screener. Doesn't
> prevent the leak — makes the leaker identifiable. Good "so what do you actually do about it?"
> answer.

---

## 6. References (specs + neutral/educational sources — no circumvention tooling)

- **HLS** — RFC 8216 (Apple HTTP Live Streaming).
- **MPEG-DASH** — ISO/IEC 23009-1.
- **Common Encryption (CENC)** — ISO/IEC 23001-7.
- **MSE** — W3C Media Source Extensions spec.
- **EME** — W3C Encrypted Media Extensions spec (and the surrounding controversy — good for
  the essay's tension).
- **Widevine** — Google Widevine DRM architecture overview (L1/L2/L3, TEE).
- **HDCP** — Digital Content Protection LLC spec overview.
- **Netflix TechBlog** — "Per-Title Encode Optimization", "Dynamic Optimizer / per-shot
  encodes", and **Open Connect** (their embedded-CDN appliance program).
- **EFF** — writing on DRM, the analog hole, and DMCA §1201 anti-circumvention (the legal
  layer + why the trusted-client problem is also a policy fight).
- **Hello Interview / Alex Xu vol 2** — "Design YouTube / Netflix" breakdown for the
  interview-delivery framing.
- **Jordan Has No Life (YT)** — DDIA-flavored deep dives on CDN/streaming if I want video.

> TODO when I study each: pull 1 concrete number or diagram from each source into this note,
> and turn the best 3 into QUIZ entries in roadmap.html.

---

## 7. Quiz seeds (promote to roadmap.html `QUIZ` array once verified — medium difficulty)

Draft; refine when I actually study the sources:
- *Why does adaptive streaming chop video into immutable segments instead of range-requesting
  one file?* (edge cacheability + clean rendition switching + stateless origin)
- *A 1 Gbps link serves roughly how many concurrent 1080p (~5 Mbps) streams, and why does that
  number force a CDN?* (~200; egress cost/scale)
- *Why is Widevine L3 capped at low resolution while 4K requires L1?* (L3 is software-
  reversible; hardware TEE required contractually for high-value renditions)
- *What is the "analog hole" and why does it make perfect DRM impossible in principle?*
  (trusted-client problem — visible signal is re-recordable)

## 8. Open threads / next actions
- [ ] Do the *timed written design* rep for "Design YouTube" using §5 prompts (counts toward
      the 10+; this note does not).
- [x] Decide the interactive-exploration mechanic → **"Defender's Dilemma"** (spec in §9).
- [ ] Build the Defender's Dilemma widget in the roadmap.html Lab tab (per §9 spec).
- [ ] Decide whether it becomes a **5th EXPL entry** (`expl-5`, "Ship it or leak it") — if yes,
      update ROADMAP §8 + roadmap.html's `EXPL` array honestly rather than silently.
- [ ] Pull real numbers/diagrams from §6 sources; convert best 3 into QUIZ entries.
- [ ] Log this study session in PROGRESS.md weekly entry.

---

## 9. Game design spec — "Defender's Dilemma" (build-ready; no code yet)

> **One-line pitch:** you're the distributor shipping a hit show; spend a limited defense
> budget on design/security measures, then watch a deterministic adversary attack your weakest
> link. You *never* hit zero leaks — winning means pushing the leak to low-quality, slow, and
> traceable while keeping reach high and cost sane. The loop teaches the thesis: **security is
> economics, enforced by engineering.**

### The loop (per round)
1. New high-value release announced (stakes escalate each round).
2. Reader spends a **budget** (start 5 pts/round) across **measures** (toggles below).
3. **Predict-then-reveal:** before "SHIP IT", reader guesses *which link the adversary will
   hit* (insider / L3 rip / analog hole).
4. `resolve()` runs the deterministic adversary → outcome + a tuned one-line lesson.
5. Meters update; round score + verdict shown. Next round.

### Meters (state)
`{ reach, cost, leakSeverity, traceability }` — plus `budget`, `round`, `measures:Set`,
`history[]`. Persist `best` under the existing `S.game` localStorage shape (don't restructure).

### Measures (cost → effect) — each maps to a concept in this note
| Measure | Cost | Effect | Teaches (§ref) |
|---|---|---|---|
| Allow **L3 software DRM** for device reach | 0 | reach+, opens L3 leak path | §3 soft DRM reversible |
| Gate **4K/HDR to hardware L1** | 1 | closes HQ-via-L3 path, small reach− | §3 TEE / contractual gating |
| **Own CDN** (Open-Connect style) | 2 | cost−ongoing, resilience+ (not a leak lever) | §2 egress economics |
| **Forensic watermarking** (per-session) | 1 | traceability+ (never prevents) | §4b analog-hole countermeasure |
| **HDCP** output-protection enforcement | 1 | raises analog-hole cost, reach− (breaks setups) | §3 output protection = speed bump |
| **Screener/pre-release controls** | 1 | closes insider path, press-reach− | §4b insider = top HQ source |
| **Aggressive legal takedowns** | 2 | reactive, low ROI, burns budget | §4a takedown asymmetry |
| **Day-and-date global + good UX** | 2 | reduces *demand* for piracy (the real win) | §4b economics beats tech |

### Adversary logic — `resolve(measures)` — DETERMINISTIC (no RNG; teachable + resume-safe)
Attack the cheapest **open** path in priority order:
1. Screeners uncontrolled → **insider leak**: HQ, pre-air. Worst severity.
2. Else 4K *not* gated to L1 (L3 allowed for HQ) → **L3 software rip**: HQ leak.
3. Else L3 allowed (low-res only) → **L3 rip**: low-res leak (limited).
4. Else all hardened → **analog hole**: *always succeeds* (unblockable), but slow +
   quality-degraded; if watermarking on → **traced**; if HDCP on → slower/worse still.

**The point:** step 4 always fires — the adversary never comes away empty because the analog
hole can't be closed. So `leakSeverity` never reaches 0. Score rewards *minimizing* severity
while *maximizing* reach at *sane* cost — not elimination.

### Scoring & verdict
`round score = w1·reach − w2·leakSeverity − w3·cost + w4·traceability`. Map to an emoji verdict
+ a lesson string keyed to the actual `leakPath` (e.g. insider → "no DRM was even involved —
you leaked before the protected path existed"). End-screen delivers the thesis + a
**predict-vs-actual** recap and an **export-to-2brain** "save as cards" hook (§ROADMAP mechanics).

### Build notes
- Pure `resolve()` function, unit-testable, no `Math.random()` (keeps it deterministic and
  offline-safe from `file://` per CLAUDE.md).
- Lives as one Lab card in `roadmap.html`; mechanics reused: toggles-as-sliders,
  predict-then-reveal, failure simulation, test-yourself recap, export hook.
- Keep it small and self-contained — it's a prototype for the blog exploration, not the final
  polished piece.
