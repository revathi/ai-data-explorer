# GenAI Data Explorer — Lovable pitch production script

## Production instructions — do not narrate

Create a professional narrated pitch video lasting **2 minutes 58 seconds**, with a hard maximum of three minutes. This is a fresh, vendor-neutral revision. Use this file as the source of truth rather than previous scripts or reference-video narration.

- Use a deep navy background, orange emphasis, clean white typography, restrained animation and subtle instrumental music. Match the supplied diagrams. Use a professional, conversational British English voice, with comfortable pauses.
- Show short captions and animated visuals; do not put narration paragraphs on slides. Reveal diagram stages as the voice explains them.
- Name the product **GenAI Data Explorer** consistently. Position it as self-service access to database information. Payments is the demonstration domain; the product idea applies across business domains.
- Do not add a product owner persona, business-overview scene, anomaly detection, fraud detection or a persona-switching tutorial.
- The prototype segment is **40 seconds**, from **00:29 to 01:09**. Business conversation occupies its first 28 seconds; query history occupies its final 12 seconds. Mention DevOps only for traceability.
- First try to capture the existing Lovable prototype's actual business conversation and query-history flow to create the 40-second demo. This request is for a video of the existing prototype, not for rebuilding or adding features. If capture is unavailable, use supplied footage; if neither is available, prepare the other scenes and reserve a clearly labelled editing placeholder. Do not export that placeholder as a finished submission or manufacture UI interactions or answers.
- The prototype clip should be silent. Generate a single consistent narration and music mix for the whole video. Preserve meaningful on-screen data timestamps and existing demo labels; avoid repetitive spoken disclaimers.
- All cloud-vendor branding and old cloud-specific diagrams are excluded. Use the separate diagram files listed below. Do not introduce FastAPI or a specific database engine into the visuals.
- Human review is part of the **proposed architecture**, not a feature demonstrated in the supplied prototype. Use the small on-screen label “Proposed design” during architecture and controls. Schema RAG, controlled SQL-agent iteration and predictions belong to the future section.
- No model training on organisational transaction data is required for this approach. This does not mean no data reaches the model: approved schema context and minimum authorised results are used for inference.
- Keep private database connectivity separate from the logical execution boundary. A private database does not establish where the model runs. Show the approved model connection explicitly.

## Timeline

| Scene | Global timing | Duration |
|---|---|---:|
| Hook | 00:00–00:08 | 8 s |
| Problem | 00:08–00:19 | 11 s |
| Solution | 00:19–00:29 | 10 s |
| Business conversation | 00:29–00:57 | 28 s |
| DevOps traceability | 00:57–01:09 | 12 s |
| Impact: customer experience and productivity | 01:09–01:21 | 12 s |
| Architecture and human review | 01:21–02:01 | 40 s |
| Credibility, Risks & Safeguards | 02:01–02:26 | 25 s |
| Portability and extensions | 02:26–02:46 | 20 s |
| Close | 02:46–02:58 | 12 s |

## 00:00–00:08 — Your data. Your decisions.

**Voiceover**

Your database holds the answers. How quickly can your business get the information it needs?

**Visual**

Animate database → question → decision. Show **Your data. Your decisions.**

## 00:08–00:19 — Every handoff takes time.

**Voiceover**

A business request becomes an engineering task: obtain access, write SQL, extract results. Every handoff takes time and delays the next decision.

**Visual**

Reveal request → access → SQL → results. Highlight waiting between steps. No invented time-saving statistics.

## 00:19–00:29 — Ask it. Know it.

**Voiceover**

GenAI Data Explorer gives business users a simpler path: ask in plain English, retrieve permitted information, and get an understandable answer.

**Visual**

Product name and consistent database/chat symbol. Animate **Ask → Retrieve → Understand**. Transition into actual prototype footage.

## 00:29–00:57 — A business question. A clear answer.

**Voiceover**

A business colleague needs an update on supplier P O Y. They ask: how many bookings were processed today? The application interprets bookings as payments and returns twenty-eight for the displayed reporting period. The answer includes its scope and assumptions. The colleague can then refine the question by supplier or reporting period, continuing the conversation in plain English.

**Visual**

Use the supplied business conversation showing “how many bookings processed for POY today”. Reveal the answer **28**, then the reporting scope and follow-up suggestions. If the new recording contains an actual follow-up, show it; otherwise show only the available suggestions, without animating a fabricated answer. Update the spoken number and period if the new recording differs.

## 00:57–01:09 — Behind the answer: DevOps traceability.

**Voiceover**

Behind the answer, authorised DevOps engineers can review recorded questions, executed SQL, timestamps and outcomes within their permitted history. Each answer has a traceable query.

**Visual**

Use actual query-history footage. Highlight question → SQL → timestamp → outcome. Caption **Behind the answer: DevOps traceability.** Do not claim universal monitoring of all database clients or all users based on a role-scoped history screen.

## 01:09–01:21 — Better customer experience. More productive teams.

**Voiceover**

The potential impact spans both themes: putting a smile on customers through quicker, clearer answers, and improving productivity through fewer manual queries and handoffs, freeing teams for higher-value work.

**Visual**

Reveal two equal cards using the contest theme names provided by the project owner:

- **Put a Smile on Customer** — quicker answers, clearer updates, less waiting.
- **Productivity** — fewer manual queries, fewer handoffs, more time for valuable work.

Connect both cards to **Self-service access to information**. Customer benefit can come through authorised partner self-service or employees answering customers sooner; do not imply unimplemented external access. Present these as expected benefits, without invented satisfaction scores, time savings or measured outcomes. Pilot measures: time to answer, manual effort and user feedback. This links the idea to both themes without asserting that contest rules allow entry in two categories.

## 01:21–02:01 — From question to controlled execution.

**Voiceover**

In the proposed design, the API authenticates the user and establishes their role. The orchestration layer supplies authorised schema and business context to a language model. The model generates a SQL query; it does not execute it. No training on organisational transaction data is required. Application code validates every query. Human approval is required only when configured review thresholds are exceeded. Within those thresholds, validated and authorised queries proceed automatically. The data layer rechecks permissions and executes the read-only query. Authorised results return to the user, while review decisions and execution outcomes are recorded for traceability.

**Visual**

Use **assets/01-system-architecture-animated.gif**, or animate the matching SVG/PNG. The GIF loops in 16.8 seconds; retime the stages to the 40-second narration rather than repeatedly rushing through the loop. Preserve the symbols and four layer groupings. Keep **Proposed design** visible. Show the user sending a question to the API and receiving the response back. Do not restore the removed side boxes.

Reveal in order:

1. **API Layer**: identity → verified role → question.
2. **Approved schema & business context** → **LLM: Natural language → SQL**. Highlight **Result-bounded read-only query generation**. The validator enforces these constraints independently of model output.
3. **SQL syntax & policy validation** → conditional **Human review & approval (Only when configured review thresholds are exceeded)**. Within review thresholds, validated and authorised queries proceed automatically. Unsafe or unauthorised requests are rejected; review cannot override mandatory restrictions. Persist required review state while waiting.
4. **Data & Audit Layer**: **Read-only query execution** and **Audit log**. Do not show a production-replica label in this simplified diagram. Recheck current permissions and any required approval before execution.
5. **Response Layer**: show only **Authorised results**, with the return arrow to the user. The footer reads **AI-powered intelligence accelerates operations within controlled boundaries.**

The LLM icon must explicitly identify SQL generation. Omit summarisation from this simplified visual, but do not claim that results never reach a model if the implementation uses model-based summaries. This visual simplification does not change implementation or data handling. Audit covers application workflow events.

## 02:01–02:26 — Credibility, Risks & Safeguards.

**Voiceover**

Every query passes read-only, access and SQL validation checks, with result limits and timeouts. Routine queries run automatically. Exceptional queries require human approval; unsafe queries are blocked. Company identity and access management verifies each user's role. Application and database policies enforce what they can access, independently of the model's instructions.

**Visual**

Use **assets/04-human-oversight-and-guardrails.svg** or PNG. Reveal the three columns sequentially: **Automatic path → Blocked by guardrails → Human review for exceptional queries**. End on **Routine queries run automatically. Exceptional queries require approval. Unsafe queries are blocked.** This replaces the older trust-boundaries image in the pitch; do not add a second constraints slide.

Use **Configurable result limits** in the architecture material. Do not assert a 200-row implementation limit until verified in the current prototype. The separately suggested query returning more than 200 matching payments is an optional test, not an extra required demo scene.

## 02:26–02:46 — Portable by design. Extensible by choice.

**Voiceover**

The core workflow is designed for portability, with replaceable model and database connections. For complex databases, schema RAG can retrieve relevant, authorised metadata. A future SQL agent could refine queries within the same controls, while predictive capabilities could help teams anticipate business demand and service-level risks.

**Visual**

Use **assets/03-portability-and-extensions.svg** or PNG. First highlight the portable application core and model, database and identity adapters. Then reveal the **Future extensions** group: schema RAG → controlled query refinement → business predictions. Label all three as future; do not portray prediction or autonomous iteration as demonstrated.

## 02:46–02:58 — Fewer handoffs. Faster answers.

**Voiceover**

Fewer handoffs. Faster answers. Clear accountability. GenAI Data Explorer helps teams move from questions to informed decisions. Our next step: a focused pilot with measurable business value.

**Visual**

Reveal **Fewer handoffs. Faster answers.** Then **GenAI Data Explorer — Ask it. Know it.** Close on **Next: a focused pilot**. Hold the final product name for two seconds; fade music out before 02:58.

## Deliverables

- Final 1920 × 1080 landscape MP4, target 178 seconds and maximum 180 seconds. Use 30 fps if supported. Check narration timing by rendering; do not assume word count guarantees duration.
- Separate architecture artifacts: PNG for easy upload and SVG for editable diagrams. Keep them available independently of the video.
- One consistent narration track, quiet music and optional separate subtitle file. No overlapping old audio.
- The current package contains script and diagrams, not a newly rendered video or newly recorded prototype footage.

## Final checks — not narrated

- Exactly 40 seconds allocated to the prototype: 28 business, 12 traceability. No product owner or business-overview section.
- No cloud-vendor names/icons or old cloud diagrams.
- No model training claim confused with no inference data processing.
- All generated SQL validated; approval binds to the exact statement and parameters. Edits require renewed validation/review. Permissions checked again at execution.
- Read-only accounts, approved objects, limits and timeouts supplement validation; SELECT syntax alone is insufficient to establish safety or business correctness.
- Human approval, portability and enterprise identity integration presented as the proposed design where not implemented. Reusing a container does not automatically make database dialects or model behaviour interchangeable.
- Preserve existing demo labels and timestamps. Do not invent working follow-ups, result counts, accuracy scores, savings or production controls.
- Keep schema RAG and predictions in future scope. Retrieval is restricted by role before metadata enters the model context.
- A pilot should measure answer correctness, time to answer and manual effort saved. No production rollout or external publishing is authorised by this production brief.
