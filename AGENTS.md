# AGENTS.md

Instructions for AI coding assistants (Claude Code, Cursor, etc.)
working in this repository. Read this before making changes.

## Project

**GenAI Data Explorer** — lets business users ask questions about
enterprise data in plain English. A local LLM translates the question
to SQL; a governance layer validates and secures the query (role-based
table access, row filters, column masking) before it ever touches the
database.

Current state: **working Flask prototype with a browser chat UI**.
This is the backend-plus-frontend version — see `../backend-only/`
in the parent folder for a simpler single-file CLI version of the
same logic, with no web framework. See `BACKLOG.md` (parent folder)
for what's built vs. what's next.

## Stack

- Python 3, Flask (web server + UI)
- `sqlglot` — parses/validates generated SQL, injects row filters
- `requests` — calls a local Ollama server for NL→SQL
- SQLite — sample "enterprise" database (`enterprise.db`)
- Plain HTML/JS template (no frontend framework/build step)

## Setup

```bash
pip install -r requirements.txt
```

Requires Ollama running locally with the model pulled:
```bash
ollama pull qwen2.5-coder:7b
ollama serve   # if not already running as a background service
```

## Run

```bash
cd app
python3 app.py
```
Then open http://localhost:5050

Regenerate the sample database if needed:
```bash
python3 data/seed_db.py
```

## Project structure

```
app/
  app.py               # Flask server, /ask endpoint, ties everything together
  nl2sql.py            # builds role-scoped prompt, calls local Ollama model
  governance_rules.py  # per-role table access / row filters / column masks
  guard.py             # validates + secures generated SQL before execution
  templates/index.html # browser chat UI (user picker, question box, results table)
data/
  seed_db.py           # creates and seeds enterprise.db (Sales/HR domain)
  enterprise.db         # generated SQLite database
requirements.txt
README.md              # setup + demo script for judges
```

## Key conventions — read before editing

- **Governance rules live in the `ROLES` dict in
  `app/governance_rules.py`.** This is the source of truth for what
  each role (`sales_rep`, `finance`, `support`, `admin`) can see. Any
  new role or permission change goes here first.
- **Never let generated SQL run without going through
  `validate_and_secure_sql()` in `app/guard.py`.** This is the core
  safety property of the whole project — it parses the SQL, rejects
  anything that isn't a `SELECT`, checks the table allowlist, and
  injects row filters. Any new code path that executes SQL (including
  new Flask routes) must go through this function first, no
  exceptions.
- **The DB connection is opened read-only** (`mode=ro` in the SQLite
  URI) as a final backstop — keep this even if the guard layer above
  is trusted, it's defense-in-depth on purpose.
- **Column masking happens after the query runs**, in
  `apply_column_masking()` — it strips or redacts sensitive columns
  from the result set based on role, separate from row-level
  filtering.
- Keep dependencies minimal. This project intentionally avoids a web
  framework right now — don't add Flask/FastAPI/etc. unless the task
  is explicitly the "bring back browser UI" backlog item.

## Testing changes

A `pytest` suite lives in `tests/` (`test_guard.py`,
`test_governance_rules.py`, `test_app.py`). It covers the guard's
core safety properties directly (no Ollama needed -- `nl2sql.generate_sql`
is monkeypatched in the Flask-level tests). Run it with:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

When you change `app/guard.py` logic, extend these tests rather than
only sanity-checking by hand. The old manual pattern still works too,
run from inside the `app/` folder:

```python
from guard import validate_and_secure_sql, GovernanceViolation
# sales_rep should get region_id filter auto-injected
secured = validate_and_secure_sql(
    "SELECT product, SUM(quantity * unit_price) FROM orders GROUP BY product",
    "sales_rep", {"region_id": 3}
)
print(secured)  # should contain "WHERE region_id = 3"

# sales_rep should be blocked from employees table
try:
    validate_and_secure_sql("SELECT salary FROM employees", "sales_rep", {"region_id": 3})
    print("FAIL: should have been blocked")
except GovernanceViolation as e:
    print("OK, blocked:", e)
```

Before considering a governance-related change done, verify:
1. A disallowed table is still blocked
2. A write operation (DELETE/UPDATE/DROP) is still blocked regardless of role
3. Row filters still get injected for roles that have them
4. Column masking still applies to the right columns

## What not to do

- Don't remove the read-only DB connection, even "temporarily" for
  debugging — it's a safety backstop, not a performance choice.
- Don't let the LLM's raw SQL output reach `run_readonly_query()`
  without passing through `validate_and_secure_sql()` first.
- Don't hardcode a demo user's bypass around the governance checks,
  even for testing — write a new role in `ROLES`/`USERS` instead, so
  the guard logic is always exercised the same way.
