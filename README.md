# Secure NL Analytics — Hackathon Demo

Ask business questions in plain English. The system translates them to
read-only SQL, enforces role-based security/governance rules (which
tables you can see, what rows you're restricted to, which columns get
masked), then runs the query and shows you the result.

## How it works

1. **NL → SQL**: your question + a role-scoped schema (only tables you're
   allowed to see) go to a local LLM (`qwen2.5-coder:7b` via Ollama),
   which generates a SQL query.
2. **Governance guard** (`app/guard.py`): the generated SQL is NEVER
   trusted or run directly. It's parsed, checked to be SELECT-only,
   checked against a table allowlist for the role, and has row-level
   filters (e.g. "only your region") injected automatically.
3. **Read-only execution**: the DB connection itself is opened
   read-only as a final backstop.
4. **Column masking**: sensitive columns (PII, salary) are redacted or
   stripped from results based on role, even after the query runs.

## Setup

1. Install Ollama and pull the model (if you haven't already):
   ```
   ollama pull qwen2.5-coder:7b
   ```
   Make sure Ollama is running (`ollama serve` or it's already running
   as a background service).

2. Install Python dependencies:
   ```
   pip install -r requirements.txt --break-system-packages
   ```
   (drop `--break-system-packages` if you're using a virtualenv)

3. Seed the demo database (already done, but to reset/re-run):
   ```
   python3 data/seed_db.py
   ```

4. Run the app:
   ```
   cd app
   python3 app.py
   ```

5. Open http://localhost:5050 in your browser.

## Demo script (for judges)

1. Log in as **asha (sales_rep, APAC)**, ask: *"What's our total revenue
   by product?"* — she only sees APAC-region numbers, auto-filtered.
2. Switch to **david (sales_rep, NA)**, ask the same question — different
   numbers, his own region only.
3. Ask a sales_rep: *"Show me customer emails and phone numbers"* — the
   values come back redacted (`***`).
4. Ask a sales_rep: *"Show me employee salaries"* — request is **blocked**
   at the governance layer with an explicit reason, because `employees`
   isn't in their allowlist.
5. Switch to **priya (finance)**, ask the same salary question — she
   gets full salary data, but SSNs are still stripped from the schema
   entirely (org policy: never expose SSNs via the NL interface, for
   any role).

## Testing

Automated tests live in `tests/` and don't require Ollama to be
running (the LLM call is mocked for the Flask-level tests):

```
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Project structure

```
data/
  seed_db.py       # creates + seeds the sample enterprise SQLite DB
  enterprise.db     # generated database (Sales/HR domain)
app/
  nl2sql.py         # builds role-scoped prompt, calls local Ollama model
  governance_rules.py  # per-role table access / row filters / column masks
  guard.py          # validates + secures generated SQL before execution
  app.py            # Flask app tying it together
  templates/index.html  # demo chat UI
tests/
  test_guard.py             # guard.py unit tests (allowlist, row filters, masking)
  test_governance_rules.py  # ROLES/USERS config sanity checks
  test_app.py               # end-to-end /ask tests (Ollama call mocked)
```

## Roadmap / talking points for Q&A

- **Scaling schema context**: for large production DBs, replace the
  full-schema-in-prompt approach with schema RAG — embed table/column
  metadata and retrieve only relevant tables per question.
- **Policy source**: governance rules currently live in a Python dict;
  in production this would be backed by an external policy engine
  (e.g. OPA) or the org's existing IAM/RBAC system, so security teams
  manage rules without touching app code.
- **Query optimization**: could add EXPLAIN QUERY PLAN checks to catch
  full table scans before execution, and enforce indexed filters.
- **Audit logging**: every question + generated SQL + secured SQL +
  user is already captured in the `log` object returned by `/ask` —
  next step is persisting this to an append-only audit table.
