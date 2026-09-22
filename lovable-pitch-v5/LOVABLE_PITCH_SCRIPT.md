# GenAI Data Explorer — pitch with the 66-second Lovable demo

## Production brief — not narrated

Use the workshop's seven-section order: **Hook → Problem and value → Solution and innovation → Demonstration → Impact → Credibility, risks and safeguards → Close**. Adapt the suggested timings to retain the existing **66-second demo**. Target **178 seconds**, leaving two seconds below the three-minute limit.

This file replaces the earlier 40-second-demo timing plan for this edit. Keep the original script as a reference. Do not concatenate the original architecture and future sections after this new timeline.

The user reports that Lovable has produced a 66-second video. The clip has not yet been inspected. Use the actual supplied clip; its internal scenes, figures, narration and music must be checked before final assembly. Do not assume its scene divisions match the old 28-second business / 12-second history plan.

## Timeline

| Section | Timing | Duration |
|---|---|---:|
| Hook | 00:00–00:10 | 10 seconds |
| Problem and value | 00:10–00:25 | 15 seconds |
| Solution and innovation | 00:25–00:57 | 32 seconds |
| Demonstration — existing Lovable clip | 00:57–02:03 | **66 seconds** |
| Impact | 02:03–02:23 | 20 seconds |
| Credibility, risks and safeguards | 02:23–02:48 | 25 seconds |
| Close | 02:48–02:58 | 10 seconds |
| **Total** | | **178 seconds** |

All transitions fit within these slots. Do not add opening logos, title cards, credits or pauses outside the timeline. Confirm final runtime after narration and editing; do not speed up the demonstration to fit.

## 00:00–00:10 — Hook

**Voiceover**

Your database holds the answers. But when a business question arrives, how quickly can the person who needs the answer actually get it?

**Visual**

Animate a person asking a question, a database and a waiting indicator. Caption: **The answer exists. Access takes time.** Use navy, white and orange. Keep this independent of a particular business domain.

## 00:10–00:25 — Problem and value

**Voiceover**

Today, a simple question can become an engineering request: obtain access, write SQL, extract results and send an update. Business users wait, while engineers repeat routine queries. Self-service access can shorten that journey.

**Visual**

Reveal **Question → Engineering request → SQL → Results**. Show the waiting gaps, then transition to **Self-service answers**. Do not add invented waiting times or measured savings.

## 00:25–00:57 — Solution and innovation

**Voiceover**

GenAI Data Explorer turns plain-English questions into controlled database queries. The API verifies the user's role. Approved schema and business context guide the language model to generate SQL, without training on transaction data. Application code validates each query; human approval is required only when review thresholds are exceeded. The data layer executes read-only queries and returns authorised results. Replaceable model and database connections support portability, with schema RAG as a future extension for complex databases.

**Visual**

- **00:25–00:52:** use `assets/01-system-architecture.svg` or PNG. Animate its stages in order rather than looping the 16.8-second GIF at full speed: user → API → schema context → LLM SQL generation → validation → conditional human approval → read-only execution → authorised results → user. Keep **Proposed design** visible.
- **00:52–00:57:** show the upper part of `assets/03-portability-and-extensions.png`: portable core and replaceable connections. Briefly reveal **Future: schema RAG**. Do not try to explain every extension in five seconds.
- Preserve the simplified diagram: no three side boxes, no cloud-vendor names or icons, no production-replica label, and Response Layer contains only **Authorised results**.
- Human review applies to otherwise permitted queries that exceed review thresholds. Mandatory access restrictions and validation failures are not overridable by approval.
- No-training refers to model training, not to inference data handling. Omitting summarisation from the diagram does not justify claiming no results reach a model if the implementation sends them.

## 00:57–02:03 — Demonstration

**Footage**

Insert the complete **66-second Lovable demo** here at normal playback speed. It is the demonstration, not an additional full pitch. Its preferred focus remains business questions and DevOps query traceability; no extra product owner or business-overview sequence is requested.

**Audio and narration**

- If the clip already has suitable narration, retain it and match volume across the edit. Do not speak a second narration track over it.
- If silent, write and synchronise narration only after inspecting the actual clip. Describe the question, returned answer, any demonstrated follow-up and the visible query history. Do not invent figures, successful actions or screen transitions.
- If the clip includes music, avoid layering two soundtracks. Use an agreed single music bed or duck the surrounding soundtrack during the clip.
- Preserve timestamps and existing demo labels. Do not claim that role-scoped history covers every database access or every client.
- Mention DevOps only where their permitted query history is shown. Do not give a persona-dropdown tutorial.

**Editing boundary**

The outside pitch resumes at **02:03**. Do not force the old POY result of 28 or the old 40-second walkthrough narration onto this new video. Confirm its actual duration and audio before final export. If its duration differs from 66 seconds, retime the surrounding scenes and keep the final film below 180 seconds.

## 02:03–02:23 — Impact

**Voiceover**

The potential impact spans both contest themes. Put a smile on customers through quicker answers, clearer updates and less waiting. Improve productivity through fewer manual queries and handoffs, freeing teams for higher-value work. A focused pilot would measure time to answer, manual effort saved and user feedback.

**Visual**

Reveal two equal cards:

- **Put a Smile on Customer** — quicker answers; clearer updates; less waiting.
- **Productivity** — fewer manual queries; fewer handoffs; more time for valuable work.

Connect both to **Self-service access to information**. Customer benefit may be direct for authorised business partners or indirect through employees responding sooner. Do not imply that external-party access is already implemented. Use the theme names as supplied by the project owner, without claiming eligibility to enter two contest categories. Do not invent realised benefits or metrics.

## 02:23–02:48 — Credibility, risks and safeguards

**Voiceover**

Every query passes read-only, access and SQL validation checks, with result limits and timeouts. Routine queries run automatically. Exceptional queries pause for an authorised reviewer to approve, revise or reject. Unsafe queries are blocked. Company identity integration establishes the user's role; application and database policies enforce their access. Decisions and executions are recorded for traceability.

**Visual**

Use `assets/04-human-oversight-and-guardrails.png` or SVG. Reveal **Automatic path → Blocked by guardrails → Human review for exceptional queries**. Keep the **Proposed policy** label. Hold the bottom message: **Routine queries run automatically. Exceptional queries require approval. Unsafe queries are blocked.**

This is the single safeguards visual. Do not also insert the old diagram 02 or a separate constraints slide. Do not imply these enterprise controls have all been verified in the prototype. Reviewer decisions cannot bypass hard access/safety rules; edits repeat validation, and execution rechecks current permissions.

## 02:48–02:58 — Close

**Voiceover**

Fewer handoffs. Faster answers. Controlled access. GenAI Data Explorer. Let's turn everyday questions into informed decisions, starting with a focused pilot.

**Visual**

Show **GenAI Data Explorer — Ask it. Know it.** Then **Next step: a focused pilot**. Hold the final brand for two seconds within the allocated ten seconds. Fade music out by 02:58.

## Final handoff checks

- Actual 66-second clip inspected; audio treatment confirmed; no invented demo content.
- Seven workshop sections retained in order. 112 seconds of surrounding pitch plus 66 seconds of demonstration = 178 seconds.
- No separate long architecture, product owner, prediction or future-agent section added. Those are technical Q&A material for this edit; schema RAG receives one brief future mention.
- The demo is unchanged in length. Architecture has 32 seconds and safeguards 25 seconds; adjust narration delivery naturally rather than accelerating speech to force timing.
- Diagram files remain separate artifacts as well as appearing in the video.
- Use consistent professional English narration, subtle music, short captions and one clear animation at a time. Target 1920 × 1080 landscape MP4.
- This document is an updated edit plan, not a claim that a new complete video has already been rendered.
