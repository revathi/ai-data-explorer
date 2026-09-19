# Lovable update prompt — GenAI Data Explorer

Update the existing PayLens prototype to reflect this product direction. Inspect the current implementation and retain its useful working features and synthetic payments dataset.

## Product purpose

Payment processing teams rely on database information to answer everyday questions: What happened to this payment? What amount was recorded? Which payments are still pending? Getting these answers often requires SQL expertise and assistance from a colleague with authorised database access. Those handoffs slow routine work, investigations, and responses to business colleagues.

The project owner reports that the team's current CloudWatch dashboard is technical and does not provide the transaction-level lookup experience they need. Treat this as a gap in that team's current setup, not a claim that CloudWatch cannot support transaction investigation in general. Existing fraud detection and analytics platforms serve other needs.

Position GenAI Data Explorer as **an AI-assisted self-service interface for payment operations**. Its role is to turn an authorised user's plain-English question into a useful answer from payment records. It complements existing monitoring and specialist platforms. Do not pitch it as a replacement for fraud detection, anomaly detection, or enterprise business intelligence.

The core product promise is **one controlled access point to payment information, with the right experience for each team**. Support three equally important use cases: fast database-information retrieval for DevOps engineers, an overall payments dashboard for product owners, and natural-language questions for business users. Build these as connected views over the same data and definitions.

## Three audiences and experiences

1. **DevOps engineers — Find the details quickly.** Provide payment-reference lookup, status/amount/currency, available timestamps, and filtered pending or failed payment lists. Offer direct structured search as well as natural-language input. Keep technical query details accessible in an expandable panel. No arbitrary SQL editor or unrestricted database access is required.
2. **Product owners — See the overall picture.** Provide a smart Payments overview dashboard with total attempts, settled payment value, success rate, and pending count; date/channel filters; trends; and status/channel breakdowns. Add a short briefing calculated from the selected data, with comparisons against a clearly identified prior period. Clicking a metric should open its supporting records or a prefilled question while preserving the filters. Smart means relevant summaries and connected exploration, not fraud scoring or anomaly detection.
3. **Business users — Ask in everyday language.** Provide suggested questions, a prominent question box, understandable answers, and contextual follow-ups. Use tables or charts as appropriate and keep technical details collapsed.

Treat these as experience preferences, not automatic permission grants. Every view must respect the user's underlying access scope. Changing a workspace or demo persona must not be represented as real authentication.

## Value and messaging

Use these values to guide design and copy:

- **Independence:** Payment operations and business colleagues can retrieve permitted information without writing SQL for every request.
- **Visibility:** Product owners get a clear overall payments picture and can explore the records behind a metric.
- **Speed:** Reduce the steps and handoffs needed to answer routine questions. Treat faster responses as an intended benefit until measured.
- **Precision:** Return the correct transaction, amount, currency, status, and reporting period from the data. Make missing or ambiguous information explicit.
- **Continuity:** Let users refine an investigation without restarting or asking someone to write another query.
- **Controlled access:** Apply the user's verified permissions in the backend in the enterprise implementation; describe the prototype's actual enforcement accurately.

Use this concise product description in About/help content:
“GenAI Data Explorer brings fast payment lookup for DevOps, a clear payments overview for product owners, and plain-English answers for business teams into one controlled self-service interface.”

Describe the overall product as a self-service payment data interface, with a smart dashboard as the product-owner experience. Use familiar actions: find a payment, understand the overall picture, and ask a business question. Do not imply that the app processes, retries, cancels, or refunds payments: this is a read-only information interface.

## Name and landing page

Rename PayLens to **GenAI Data Explorer** throughout navigation, browser titles, help text, and other user-facing references.

Use this exact headline:

**Ask it. Know it.**

Place this short descriptor above the headline:

**Self-service payment information for every team.**

Supporting sentence:

**Find a payment. See the bigger picture. Ask your next question—all in one place.**

Place a large, clearly labelled question input directly beneath the headline. Use **What do you need to know?** as the placeholder and **Ask** as the visible submit-button label.

Make a shared Home page the first-visit landing page, with the question input and three audience cards visible on a typical laptop. Remember the preferred workspace for subsequent visits without changing permissions. Retain the existing navy, light surfaces, and warm accent colours. Use generous spacing, readable typography, a subtle data-inspired background, and restrained animation that respects reduced-motion preferences. Keep the input and suggestions stationary while users read or type.

Below the input, provide three clickable use-case cards:

- **DevOps — Find payment details:** Open Payment lookup, with reference search and operational filters.
- **Product owners — See the payments overview:** Open the smart dashboard, with summaries, comparisons, and drill-downs.
- **Business — Ask the data:** Open the conversational workspace with useful starter questions.

Make payment-reference lookup and pending-payment retrieval core demo capabilities. If the current synthetic dataset lacks these, add deterministic references and consistent pending records, then update dependent calculations. Offer other questions only when supported by the dataset.

Below the cards, show a compact example conversation focused on a single payment: a synthetic reference, an answer card showing status and amount, and a follow-up such as “When was it last updated?” Only offer that follow-up if a real synthetic update timestamp exists. Label the conversation **Example** until the user starts their own. Starting a question should move naturally into the results experience.

Convey fast self-service access through the interaction design. Show a useful loading state and return results as soon as available. Do not fabricate response times or guarantee instant results.

## Navigation and scope

- **Home:** Shared question input and three audience entry points.
- **Payment lookup:** Primary workspace for DevOps, including structured search and operational lists.
- **Payments overview:** Primary workspace for product owners, with KPI cards, charts, a concise briefing, and drill-downs.
- **Ask the data:** Primary workspace for business questions and contextual follow-ups, also available to other audiences.
- **Query history:** Previous questions and results, with technical audit details in expandable sections.

Remove the Anomalies page and anomaly detection features. Human approval is future scope; do not add approval queues, reviewer screens, or approval steps. Focus the presentation on successful retrieval and exploration. Retain automated access checks and error handling without making blocked requests a featured demo scenario.

## Suggested questions

DevOps:
- Find payment [a selectable synthetic payment reference].
- What amount and currency were recorded for this payment?
- Which payments are still pending from yesterday?
- Show failed payments by channel and reason.

Product owners (dashboard and optional questions):
- Show total attempts, settled value, success rate, and pending payments for the selected period.
- Compare this period with the previous equivalent period.
- Show the channel breakdown behind this metric.

Business:
- How many payments settled yesterday, and what was their total value?
- Show settled payments for a specified merchant and date, if those fields are available.
- Compare payment volumes across channels for a defined period.

Only display supported examples. Do not silently substitute another question or invent an answer.

## Answer and follow-up experience

Present each response in this order:
1. A concise, plain-English answer.
2. The reporting period, filters, and applicable access scope.
3. A useful results table.
4. A chart when it helps explain a trend or comparison.
5. Relevant follow-up suggestions.

For a single payment, show a compact detail card with its reference, status, amount, currency, channel, and available timestamps. Use a table for multiple payments and allow selecting a row to open its details. Show an explicit choice if a reference matches more than one record; never arbitrarily choose a match. Indicate when results are limited. Put SQL under a collapsed **View query details** panel. Distinguish illustrative SQL from queries actually executed.

Support follow-ups such as “What was its recorded amount?”, “Only show iDEAL payments,” and “Show payments still pending.” Preserve the active transaction reference or list scope, dates, and filters unless explicitly changed. Show the updated scope. Ask for clarification when a request is ambiguous and explain unsupported requests. Distinguish empty results from errors.

## Data correctness and transparency

Use synthetic payments only. Calculate metrics, summaries, tables, and charts from those records. Keep definitions consistent across Payments overview, Payment lookup, and conversational answers, particularly success rate and settled payment value. A dashboard count and equivalent natural-language question must agree for the same period and access scope. Show currency and avoid summing different currencies without an explicit conversion basis. Explain pending-payment treatment in success-rate denominators; use percentage points for changes between rates, and handle a zero prior-period baseline explicitly.

Show a demo reference date and data-through timestamp where available. Resolve relative periods consistently against the dataset's reference date so recording is repeatable.

For unrelated questions such as “What is AWS Bedrock?”, explain that the application supports payment-data questions and suggest relevant examples. Do not generate SQL containing a general AI explanation and present it as a retrieved data answer.

Inspect which functions actually use a model or database and label simulations accurately. Keep a discreet **Synthetic demo data** label. Do not infer that synthetic data means AI or execution is simulated, or imply live execution where it does not exist.

## Access and architecture messaging

Keep a compact role/access indicator. If sign-in is simulated, label the selector **Demo persona**. Verify permission enforcement before making claims about it. Keep credentials and real database connection details out of frontend code.

For an architecture explanation, use:
“The database stays within the private network. Users access insights through an authorised application, with role-based permissions controlling what they can see.”

Label this **Proposed enterprise architecture** unless that deployment has actually been implemented and verified. Security details should support the results experience without dominating the landing page.

## Demo journey and verification

Optimise three concise moments for a three-minute presentation:
**DevOps finds a payment → a product owner checks the overall picture → a business user asks and refines a question.**

For an approximately 55-second demonstration section, target 15 seconds for a payment lookup, 15 seconds for the product-owner dashboard and one drill-down, and 25 seconds for a business question and follow-up. Use a consistent date/channel example so the scenes feel connected. Present workspace changes as demo navigation, not as evidence of authenticated role changes. Keep the complete video, including problem, value, safeguards, and closing, within three minutes.

Emphasise fewer handoffs, faster access to information, and more independent operations and business teams as intended benefits. Do not invent measured savings. For a future pilot, measure time to retrieve a correct answer, routine requests resolved without engineering assistance, and correctness of returned transaction details.

Provide a repeatable demo reset. Verify all three audience entry points, reference lookup, dashboard calculations and drill-down filters, suggested questions, follow-up context, consistency between views, relative dates, empty results, unsupported questions, and access-scope behaviour. Keep generation, validation, execution, and presentation separate for future integrations.

After making the changes, summarise what works, what was verified, and what remains simulated or planned.
