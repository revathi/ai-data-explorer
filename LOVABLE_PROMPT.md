# Lovable update prompt — GenAI Data Explorer

Refine the existing prototype using this specification. It supersedes earlier instructions about separate DevOps lookup screens, a shared landing/question screen, and identical question suggestions for all audiences. Retain useful working features and synthetic payment data.

## Purpose and scope

GenAI Data Explorer is an AI-assisted self-service interface to payment information. DevOps engineers need operational answers quickly, business users need answers in plain English, and product owners need an overall view of payment processing. These experiences share the same data, definitions, and access policies.

The team's current monitoring setup is technical and does not provide the self-service database access experience they need. Complement existing monitoring and specialist platforms. Keep anomaly detection outside this prototype and human approval in future scope. This application retrieves information; it does not process, retry, cancel, or refund payments.

## Brand and icon

Use **GenAI Data Explorer** everywhere: Home, navigation, page headers, browser title, and help text. Replace remaining PayLens references.

Create a simple, distinctive product icon combining a data motif with a conversation or discovery motif. Use a reusable vector component that stays recognisable at navigation and favicon sizes. Use the same icon, proportions, and colour treatment on every page. Maintain the existing navy, light surfaces, and orange accents, with readable typography, generous spacing, and accessible contrast. Provide accessible labels for icon-only controls.

## Home page

Create a separate Home page explaining the product and the three audiences. Make it the default landing page.

Product name: **GenAI Data Explorer**
Descriptor: **Self-service payment information for every team.**
Headline: **Ask it. Know it.**
Supporting text: **Get operational answers, understand payment performance, and explore your data in plain English—all in one place.**

Use a prominent orange primary button labelled exactly **Talk to your Data**. Clicking it opens **Ask your data**, retaining the current user's identity/access context and showing sample questions appropriate to their role. Do not submit a question automatically.

Below the hero, explain three benefits using concise cards:
- **DevOps:** Get answers about payment processing without writing a new database query every time.
- **Business:** Ask everyday payment questions and refine the answers naturally.
- **Product owners:** See the payments overview and ask questions about the numbers.

These are explanations, not separate audience-specific screens or permission selectors. Keep the product introduction and primary button visible without scrolling on a typical laptop. Use restrained animation and respect reduced-motion preferences. Keep synthetic-data disclosure visible.

## Pages and access

| Page | DevOps | Business | Product owner / PM |
| --- | --- | --- | --- |
| Home | Yes | Yes | Yes |
| Ask your data | Yes | Yes | Yes |
| Business overview | Yes | No in the current prototype | Yes |
| Query history | Own permitted history | Own permitted history | Own permitted history |

For this prototype, treat PM and product owner as the same audience and label it **Product owner** consistently. Do not add a fourth role merely because both terms are used.

Navigation should contain Home, Ask your data, Business overview where permitted, and Query history. All links and route titles must agree. Enforce page/data permissions on the backend where one exists; hiding a navigation item is not authorisation. If identity/access is simulated, label the selector **Demo persona** and describe its limits accurately. Do not present a client-controlled role switch as secure sign-in.

## Ask your data — one shared, personalised screen

Use one route and one shared layout for all three audiences. There is no dedicated DevOps lookup screen, reference-search form, or arbitrary SQL editor. Users ask questions, including questions about individual payments, through the same natural-language input.

Show a heading, a short role-appropriate introduction, sample question chips, and a prominent question box. Personalise the starter questions and follow-up suggestions for the active role; preserve consistent branding, interaction patterns, and answer layout. The UI copy and examples change with the role, not the basic page structure.

DevOps sample questions:
- Which POY payments are still pending today?
- Show rejected MRX payments and their recorded rejection reasons today.
- Which payments are currently beyond their supplier's processing SLA?
- What is the status and recorded amount of payment [existing synthetic reference]?

Business sample questions:
- How many payments were processed today?
- What was the processed payment value for POY this month?
- How many payments were rejected this week, grouped by supplier?
- Compare processed payments for POY and MRX this month.

Product-owner sample questions:
- Summarise this month's payment processing performance.
- How does the month-to-date processed count compare with the equivalent period last month?
- Which suppliers are below their configured demo SLA target?
- Break down this month's processed and rejected payments by supplier.

Questions must be supported by the synthetic data. Add necessary synthetic fields and deterministic examples consistently; do not offer a question that can only receive an invented answer. Supplier SLA questions and corresponding data are available only where the configured policy permits them.

Present answers as a concise finding, reporting period and filters, then a table or useful chart. For an individual payment, display a compact detail card. Put technical query details in a collapsed panel where policy permits, distinguishing executed SQL from illustrative SQL. Use contextual follow-ups such as “Only MRX,” “Show this month instead,” or “Break that down by supplier.” Preserve relevant context and distinguish a new question from a follow-up.

When a different demo persona is selected, clear the previous conversation and cached results from view and load the new persona's permitted history and suggestions. Do not leak answers between roles.

## Business overview — product owners and DevOps

Create a clear overview with a prominent data timestamp, supplier filters, payment summary cards, and a supplier SLA table. Include POY and MRX as business suppliers; keep supplier distinct from payment channel and merchant.

Required cards:
1. **Payments processed today:** From midnight in the displayed reporting timezone up to the data-as-of timestamp.
2. **Payments processed this month:** From the start of the current reporting month up to that same timestamp.
3. **Payments rejected:** Count for a clearly labelled period, defaulting to today up to the same timestamp.

For the initial prototype, interpret “processed until the current timestamp” as today's processed count to the displayed data-as-of timestamp. Make that scope explicit in the UI. Define processed as successfully completed processing in the dataset, excluding pending and rejected records. If an existing status such as settled is used, document its mapping and use it consistently in cards and answers.

Show supporting amounts only with currency and a clear definition. Optional charts should support the overview without crowding out the cards and SLA table. Clicking a permitted metric should open Ask your data with a prefilled question and matching filters, without automatically executing it.

Required supplier SLA table columns:
- Business supplier, including POY and MRX.
- Configured processing-time threshold.
- Target on-time completion percentage.
- Completed payments in the selected period.
- Payments completed within SLA.
- On-time completion percentage.
- Pending payments currently overdue.
- Target met / Below target / No completed payments.

All thresholds and targets are **illustrative demo settings**, configurable per supplier; do not imply they are actual supplier agreements. Label the synthetic SLA policy clearly.

Calculate processing duration from recorded receipt and completion timestamps. Define on-time completion percentage as successful completions within the supplier threshold divided by all successful completions in the selected completion-time window. Exclude rejected and pending payments from that denominator and show pending breaches separately. Count pending overdue records as of the data timestamp using their receipt time and supplier threshold. Explain this definition in a tooltip; display N/A for a zero denominator. Use UTC elapsed durations and display the reporting timezone consistently. Handle invalid/missing timestamps explicitly.

## Data, freshness, and correctness

Use synthetic records with supplier, payment reference, amount, currency, status, received timestamp, applicable completion/rejection timestamps, and rejection reason where relevant. Maintain supplier SLA settings separately. Include realistic processed, rejected, and pending examples for POY and MRX. Never include real payment credentials or personal customer data.

Calculate cards, tables, summaries, and conversational answers from the same records and definitions. Do not hardcode unrelated display numbers. Dashboard and equivalent questions must agree for the same access scope, period, and timestamp. Use event timestamps appropriate to each metric and label their meaning.

Always distinguish the current clock time from **Data as of**. If the dataset is fixed, use a clearly labelled fixed demo reference timestamp and resolve “today,” “this month,” and “yesterday” against it. Do not keep advancing a clock or claim live refresh over stale static data. If synthetic data refreshes, update records, the data timestamp, and all affected calculations together. A reset must reproduce the same starting state.

Handle unrelated questions with a payment-scope explanation and useful suggestions. Do not generate SQL containing a general AI explanation and present it as a database answer. Keep empty results, errors, unsupported questions, and ambiguity distinct.

## Security and presentation accuracy

Use a compact role/access indicator and synthetic-data label. Describe actual model calls, SQL execution, and permissions accurately. Synthetic data does not itself mean AI or database execution is simulated. Keep credentials and connection details out of browser code.

Architecture copy, labelled **Proposed enterprise architecture** unless verified as implemented:
“The database stays within the private network. Users access information through an authorised application, with role-based permissions controlling what they can see.”

Focus the pitch on useful results, fewer handoffs, and self-service access. Do not invent measured speed improvements. Security supports the experience; blocked requests are not a featured recording scenario.

## Completion checks

Verify consistent icon/name across pages, Home-to-Ask navigation, distinct starter questions for all three roles, product-owner access to Ask your data, and Business overview access for DevOps and product owners. Verify overview calculations, POY/MRX SLA rows, zero denominators, overdue pending records, reporting-time boundaries, follow-up context, role-change result clearing, unsupported questions, and reset behaviour.

Keep data access, generation, policy validation, execution, and presentation separate. After implementation, summarise what changed, what was verified, and what remains simulated or planned. The full pitch video will be no more than three minutes; the app must support a concise results-focused recording.
