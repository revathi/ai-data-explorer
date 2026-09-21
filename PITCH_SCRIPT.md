# GenAI Data Explorer — revised pitch script

## Production direction

- Target runtime: **2 minutes 58 seconds**. This technical revision gives architecture 45 seconds and security 25 seconds. The timings below supersede reference video v3; regenerate narration and synchronise the animations to this script.
- Use professional British English AI narration with subtle instrumental music underneath.
- Retain the navy background and orange highlights. Use short captions and an animation on every scene; do not display the full narration as slide text.
- Present the idea as a natural-language interface for databases generally. Payments is the synthetic demonstration dataset.
- Prototype order: **Business conversation → Product owner overview → Query history**. Mention DevOps only in query traceability. Do not frame the pitch around three users sharing a platform.
- Explain user roles and company identity and access management (IAM) integration in the final security section.
- Technical emphasis: the model generates SQL; explicit Lambda validation code and database permissions control execution. Describe these as the proposed design, rather than claiming unverified prototype controls.

## 0:00–0:08 — Your data. Your decisions.

**Voiceover**

Your database holds the answers. How quickly can your business get the information it needs?

**Visual / animation**

Animate database → question → business decision. Caption: **Your data. Your decisions.**

## 0:08–0:19 — Every handoff takes time.

**Voiceover**

A business request becomes an engineering task: obtain access, write SQL, extract results. Every handoff takes time.

**Visual / animation**

Reveal request → approved access → SQL → results, one step at a time. Caption: **Every handoff takes time.**

## 0:19–0:29 — Ask it. Know it.

**Voiceover**

GenAI Data Explorer turns business questions into database queries and understandable answers. Ask in plain English. Explore the result.

**Visual / animation**

Animate three actions: Ask → Retrieve → Understand. Caption: **Ask it. Know it.**

## 0:29–0:53 — A business question. A clear answer.

**Voiceover**

A business colleague needs an update on supplier POY. They ask: How many bookings processed for POY today? The prototype interprets bookings as payments, and returns twenty-eight, up to the dataset's reference time. A clear figure for their update. Follow-up suggestions help them explore another supplier or period.

**Visual / animation**

Show the supplied Business conversation screenshot. Highlight the POY question, then the answer **28**. Follow with a simple result card and the visible follow-up suggestions. Preserve the screen's reporting-period label.

## 0:53–1:10 — From overview to action.

**Voiceover**

Product owners get a near-real-time overview of the business through a connection to the production replica. Processing totals, rejections, and supplier service levels help them prioritise follow-up and make informed decisions.

**Visual / animation**

Show the actual Business overview, then highlight processing totals, rejections, and supplier SLA performance. Caption: **From overview to action.** Caption the data source **Production replica · Near-real-time overview**. Preserve the displayed data timestamp.

## 1:10–1:24 — Trace the question. Understand the result.

**Voiceover**

For traceability, authorised DevOps users can review recorded questions, executed SQL, timestamps, and outcomes within their permitted history. This helps explain how the application accessed the data.

**Visual / animation**

Show the supplied Query history screenshot, then enlarge the entries so the question, SQL, timestamp, status, and returned row count are readable. Caption: **Trace the question. Understand the result.**

## 1:24–2:09 — A clear path from question to answer.

**Voiceover**

In the proposed architecture, API Gateway forwards the question to Lambda. Lambda supplies Bedrock with approved table definitions, relationships, and business rules. No model training on organisational data is required. Bedrock generates SQL. Validation code in the same Lambda checks syntax, allowed tables and columns, and read-only operations. It applies query limits and timeouts before execution against the production replica, using restricted database permissions. Lambda sends the minimum authorised result back to Bedrock for a plain-English summary. One Lambda coordinates two model calls; validation and access controls operate independently of the model.

**Visual / animation**

Keep the label **Proposed AWS architecture** visible. Use the existing AWS icons and the same Lambda box throughout. Animate a single example from question to result:

1. **Question + approved context:** API Gateway → Lambda. Show the POY question with compact labels for tables, relationships, and business definitions; “processed” means successfully settled in this demo. Context is supplied at inference time, without model training.
2. **Model call 1 — SQL generation:** Lambda → Bedrock → the same Lambda. Reveal a short SQL preview or labelled query plan based on the approved schema; avoid a wall of code.
3. **Lambda validation:** Highlight the Lambda box. Sequential labels: **Parse syntax → Allowlisted tables / columns → Read-only operations → Limits / timeout**. These checks are validation code, not a promise from the model.
4. **Restricted execution:** Lambda → **Private RDS production replica**. Show **Database permissions enforced** and the compact result **processed_count: 28**. The result corresponds to the captured POY example.
5. **Model call 2 — summarisation:** Replica → same Lambda → Bedrock with **Minimum authorised result**, then Bedrock → Lambda → API Gateway → application. End on **One Lambda · Two model calls**.

Do not add another Lambda or a separate validation backend. Preserve the private-network boundary. Keep labels brief and reveal them in sync with narration. Refer to the proposed controls without implying syntax checking alone establishes answer correctness.

## 2:09–2:24 — Build on the foundation.

**Voiceover**

The architecture can extend to an autonomous SQL agent for complex schemas, with metadata retrieval and controlled query correction. Future AI predictions could help teams forecast demand and anticipate service-level breaches.

**Visual / animation**

When the voiceover says “The architecture can extend to an autonomous SQL agent for complex schemas,” show the supplied **SQL agent architecture diagram** (`assets/sql-agent.png` in the upload package; `architecture/sql-agent.png` in the GitHub repository). Replace the generic schema-retrieval / SQL-generation animation in this section with this diagram. Enlarge it for readability and highlight ConverseSQLAgent Lambda and its connections to Bedrock and RDS as the narration describes the extension. Keep the label **Future: autonomous SQL agent** visible. When the narration moves to business predictions, transition to the forecast graphic labelled **Future: business predictions**. The preceding main architecture section continues to use the existing architecture diagram.

## 2:24–2:49 — Your role determines your data access.

**Voiceover**

Every GenAI Data Explorer user's data access is determined by their verified role through company identity and access management. Application policies and database permissions enforce access to permitted records and fields. The production replica remains private. Only the minimum authorised results reach Bedrock for summarisation, while query history supports traceability.

**Visual / animation**

Animate user sign-in → company IAM → verified role → application/data policies → permitted records and fields. Highlight the private production replica and restricted database permissions. Show the minimum-result path to Bedrock and query history briefly. Caption: **Your role determines your data access.**

## 2:49–2:58 — Ask it. Know it.

**Voiceover**

Fewer handoffs. Faster answers. GenAI Data Explorer. Let's start with a focused pilot.

**Visual / animation**

Reveal **Fewer handoffs. Faster answers.** End on **GenAI Data Explorer — Ask it. Know it.** and **Next step: a focused pilot.**

## Accuracy and editing notes — not spoken

- The business screenshot asks, “how many bookings processed for POY today.” The application interprets bookings as payments and returns **28**, counted by successful completion time up to the dataset's reference time. Do not substitute the earlier illustrative monthly question or its figures for this captured interaction.
- The walkthrough uses actual supplied prototype screenshots with animated highlights. It is not a recording of live interactions. Follow-up suggestions are visible; their resulting answers have not been supplied or verified.
- Query history shows **permitted history only**. Describe the question, executed SQL, timestamp, execution status, and row count that are visible. Do not claim that this screenshot proves DevOps can see every user's query or every access across the database. Broader audit coverage requires appropriately authorised logging and verified coverage, including other database clients where relevant.
- The Business overview is timestamped synthetic data. The intended deployment reads the production replica. Near-real-time freshness depends on replication lag and application refresh timing; do not promise instantaneous updates or imply queries run against the production primary. Supplier SLA settings are illustrative.
- The architecture is proposed: API Gateway → Lambda with approved schema context → Bedrock generates SQL → the same Lambda validates syntax, permitted operations, and user access → read-only RDS production-replica execution → same Lambda sends minimum authorised results to Bedrock for summarisation → Lambda returns the answer. **No Kendra and no separate validation service.** Validation does not by itself guarantee that SQL correctly interprets every business question.
- Autonomous handling of complex schemas, metadata retrieval, controlled query correction, and AI business predictions are future extensions, not demonstrated capabilities. Corrections remain bounded and subject to the same validation and permissions. Predictions need suitable historical data and evaluation.
- Company IAM establishes identity and role context. Application and database policies enforce record and field permissions; IAM alone does not automatically filter business data. Database connectivity remains private in the proposed deployment.
- No model training is required for this design: schema context and permitted query results are supplied during inference. The same Lambda makes two Bedrock calls, for SQL generation and result summarisation. Only the minimum authorised results are sent for summarisation; no-training does not mean no data is processed by the model.
- Human approval and anomaly/fraud detection are outside this demo. Keep the narrative focused on successful retrieval, business value, traceability, and responsible adoption.
- Expected benefits are fewer handoffs, quicker answers, and more informed decisions. Measure correctness, time to answer, and manual effort saved in a focused pilot; do not invent performance or business-impact results.
- Pronounce POY as “P O Y” and SQL consistently. Preserve the slower architecture and security pacing when editing narration; keep the complete export below three minutes.

## Assets for Lovable

Use the accompanying upload package. Paths below are relative to its root; they are not Windows paths.

- Reference video: `assets/reference-v3.mp4`. Match its design, voice, and music; use the new scene timings in this script. Replace the generic future SQL-agent animation with the supplied SQL-agent diagram.
- Previous narration reference: `assets/narration.mp3`. Regenerate narration from this technical revision and align it to the new timeline. Use the old track only as a voice/style reference; never layer old and new speech.
- Original music: `assets/music.mp3`. Keep quiet beneath narration; the reference mix uses approximately 28% of this source amplitude.
- Business conversation: `assets/business-conversation.png`.
- Product owner overview: `assets/business-overview.png`.
- Query history: `assets/query-history.png`.
- Main architecture: `assets/main-architecture.svg` or `assets/main-architecture.png`. Animate the SQL response back to the same Lambda for validation, following this script.
- Future SQL agent: `assets/sql-agent.png`. Use only during the autonomous-agent explanation, then switch to the future predictions graphic.
- Target timeline and current narration text: `timeline.json`. Recheck timing after synthesising the revised segments.
- Production instructions: `LOVABLE_VIDEO_PROMPT.md`.

Read production notes as editing guidance. Speak only the Voiceover sections, using the updated timing plan. Keep technical notes and file paths out of the video.
