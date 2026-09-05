# STAR Story Bank

> Target: 8 stories, each 2–3 min spoken, with concrete numbers. Status: **seeded from resume — needs S/T/A/R detail, metrics verification, and out-loud practice.**
>
> Coverage needed: production incident · architectural disagreement (resolved with data) · leadership/mentorship · ambiguity · failure + lesson · cross-team influence · deep technical achievement · managing tech debt.

## Seeded candidates (from resume)

### 1. Tunga-agent — end-to-end AI matching & outreach pipeline
**Themes:** ownership, ambiguity, deep technical achievement.
Led end-to-end: multi-stage agent pipeline, RAG w/ Pinecone + OpenAI embeddings, SendGrid webhook-driven follow-ups, Hunter.io/Clay integrations, K8s + Celery/Redis deploy.
*Sharpen: what was ambiguous at the start? What did you decide alone vs escalate? Business result?*

### 2. Hybrid LLM mode — 90% API cost reduction
**Themes:** trade-offs with data, cost/quality engineering, initiative.
OpenAI + local Ollama hybrid. Great "disagree-and-commit with data" candidate *if* there was a debate about quality risk — dig for it.

### 3. Lead-ID — expanding the company's product line
**Themes:** business impact, influence, building for non-engineers.
Multi-signal scoring (15+ signal types, recency decay), config dashboard so marketing tunes weights without code, 500+ companies/batch.
*Sharpen: how did you win buy-in to expand scope from talent matching to lead gen?*

### 4. Sagemaker → Vertex AI migration (Sunbird)
**Themes:** technical migration, risk management.
*Sharpen: why migrate, what could have broken, how did you de-risk, downtime story?*

### 5. Sunbird API + team lead role
**Themes:** leadership, mentorship, productizing ML.
Led team + interns; API adopted by Ugandan companies, used in IndabaX hackathon.
*Sharpen: one specific mentee turnaround story with before/after.*

### 6. Noise monitoring → AWS IoT migration
**Themes:** reliability engineering, operating a real system.
Self-hosted → AWS IoT; the Mayor of Entebbe depends on it. Memorable hook — use it.
*Sharpen: what reliability failures triggered the migration? Any incident story here = the production-incident slot.*

### 7. N+1 queries, invoicing, USD payments (Tunga)
**Themes:** performance diagnosis, developer empathy, incremental impact.
*Sharpen: quantify the endpoint latency improvements.*

### 8. Andela mentorship
**Themes:** mentorship, code review culture, growing others.
*Likely merges into #5 unless there's a distinct arc.*

## Gaps to fill (no resume evidence yet — mine your memory)

- [ ] **A real production outage / incident** you owned end-to-end (detection → mitigation → postmortem)
- [ ] **A genuine failure** and what changed in how you work
- [ ] **A conflict** with a senior engineer/PM over architecture, resolved with data
- [ ] **Tech debt** you prioritized (or deliberately didn't) and the consequence

## Format per finished story

```
### Story name
**Companies/questions it answers:** ...
**S (20s):** ...
**T (15s):** ...
**A (90s, "I" not "we"):** ...
**R (30s, numbers):** ...
**What I'd do differently:** ...
```
