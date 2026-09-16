"""
Converts a natural language question into a SQL query using a local
Ollama model. The schema shown to the model is filtered to only the
tables the user's role is allowed to see -- this is the first layer
of governance (least-privilege prompting), before the guard.py
validation layer double-checks everything downstream.
"""
import json
import re
from datetime import date

import requests

from governance_rules import get_role_config

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"

FULL_SCHEMA = {
    "regions": "region_id INTEGER, region_name TEXT",
    "employees": "employee_id INTEGER, full_name TEXT, role TEXT, region_id INTEGER, email TEXT, salary REAL, ssn TEXT",
    "customers": "customer_id INTEGER, customer_name TEXT, region_id INTEGER, email TEXT, phone TEXT",
    "orders": "order_id INTEGER, customer_id INTEGER, employee_id INTEGER, region_id INTEGER, product TEXT, quantity INTEGER, unit_price REAL, order_date TEXT",
}


def build_prompt(question: str, role: str) -> str:
    role_cfg = get_role_config(role)
    allowed = role_cfg["allowed_tables"]
    schema_lines = [f"- {t}({FULL_SCHEMA[t]})" for t in allowed if t in FULL_SCHEMA]
    schema_block = "\n".join(schema_lines)

    return f"""You are a SQL generator for a SQLite database. Translate the user's
question into a single read-only SELECT query.

Today's date is {date.today().isoformat()}. Resolve relative date references
("this year", "last quarter", "last month", etc.) against that date, not
against any other assumption. If the question names a calendar month
(January, February, ..., December, or an abbreviation) anywhere, even in
an unusual word order like "this year may" meaning "May of this year",
treat that as the intended month rather than as an ordinary word.

Rules:
- Only use these tables/columns (others do not exist for this user):
{schema_block}
- Only generate SELECT statements. Never INSERT/UPDATE/DELETE/DROP.
- Return ONLY the raw SQL query, no explanation, no markdown fences.
- Use standard SQLite syntax.

Question: {question}

SQL:"""


def generate_sql(question: str, role: str) -> str:
    prompt = build_prompt(question, role)
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0}},
        timeout=60,
    )
    response.raise_for_status()
    raw = response.json().get("response", "").strip()

    # Strip markdown fences if the model added them anyway
    raw = re.sub(r"^```sql\s*|^```\s*|```$", "", raw, flags=re.MULTILINE).strip()
    # Take just the first statement if the model rambles
    if ";" in raw:
        raw = raw.split(";")[0] + ";"
    return raw
