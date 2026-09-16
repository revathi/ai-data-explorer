# GenAI Data Explorer — Backlog

## Original requirements

**Objective:** Get a GenAI Data Explorer built.

**Problem:**
1. Online payments are currently stored in AWS DynamoDB, and stream
   into RDS immediately via DynamoDB Streams.
2. Batch data goes directly into RDS.
3. The team gets business queries on payments processed. Pain points:
   - DynamoDB requires a partition key or sort key to query.
   - RDS lives in a private network — a teammate needs elevated
     access to hop in and reach the production database.
   - That teammate also needs SQL knowledge to query and extract the
     data, and to transfer it out of the AWS private network.
   - Business users depend on engineering teams to access data from a
     highly secured production database.
   - Net result: manual effort, delayed insights, limited self-service
     analytics.
4. Proposed solution: a GenAI Data Explorer.
   - AI-powered natural language interface for the database.
   - Challenge: enable secure natural-language access to enterprise
     data while respecting existing security boundaries and
     governance requirements.

**Solution description:**
- Provide a conversational interface where users can ask business
  questions in plain English.
- An LLM interprets user intent, understands the underlying database
  schema, and automatically generates optimized, read-only queries.
- Before execution, all queries are validated against predefined
  security and governance rules to ensure safe, compliant access to
  enterprise data.

---

## Vision
Let business users ask questions about production data in plain
English, without engineering having to write queries for them —
while every query respects existing security boundaries and
governance rules automatically.

---

## ✅ MVP — already built and tested working
- [x] Sample enterprise database (SQLite): Sales/HR domain —
      orders, customers, employees (salary, SSN), regions
- [x] Governance rules engine — per-role table allowlist, row-level
      filters (e.g. own region only), column masking (redact/hide)
- [x] NL → SQL generation via local Ollama (`qwen2.5-coder:7b`),
      schema-scoped prompt (only shows tables the role can see)
- [x] Guard layer (`sqlglot`-based) — blocks non-SELECT statements,
      blocks forbidden operations (DROP/DELETE/etc.), enforces table
      allowlist, injects row filters, enforces a result LIMIT
- [x] Read-only DB connection as a final backstop
- [x] CLI interface — login as a demo user, ask questions, see
      generated SQL → secured SQL → results in the terminal

---

## 🔜 Next up (v2 priorities — pick based on remaining time)
- [ ] Bring back the browser-based chat UI — "Explorer" framing
      benefits from something visual/interactive for the demo, not
      just a terminal
- [ ] Audit logging — persist every question + generated SQL +
      secured SQL + user + timestamp (shows governance isn't just a
      buzzword)
- [ ] Polish the demo script — rehearse the "same question, two
      roles, two different results" moment; rehearse the "blocked"
      moment with a clear on-screen reason

## 🧩 Nice-to-have (if time allows)
- [ ] Follow-up / conversational memory — "now break that down by
      month" without repeating full context
- [ ] Suggested next questions based on the columns just returned
- [ ] Natural-language summary of results, not just a raw table
- [ ] Query plan check (`EXPLAIN QUERY PLAN`) to flag expensive
      full-table scans before running

## 🎯 Stretch / pitch talking points (mention in Q&A, don't build)
- [ ] Schema-RAG instead of full-schema-in-prompt, for scaling to
      large production schemas
- [ ] External policy source (e.g. OPA) instead of hardcoded rules,
      so security teams manage rules without touching app code
- [ ] Real auth/SSO instead of a demo user picker
- [ ] Multi-database support (Postgres/MySQL) beyond the SQLite demo

---

## Demo script (for judges)
1. Log in as sales rep (Region A), ask a revenue question — scoped
   results, automatically
2. Switch to sales rep (Region B), ask the *same* question —
   different, correctly scoped results
3. As a sales rep, ask for customer emails/phone — values come back
   redacted
4. As a sales rep, ask for employee salaries — **blocked**, with a
   clear governance reason shown
5. Switch to finance, ask the same salary question — full access,
   but SSNs are still never exposed to any role

---

## Notes
- Governance rules currently live in a Python dict in the code —
  fine for a hackathon demo, call out in Q&A that production would
  back this with an external policy engine
- Everything currently runs against a local Ollama model — no API
  keys, no cloud dependency, works fully offline for the demo
