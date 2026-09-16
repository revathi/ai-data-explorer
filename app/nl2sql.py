"""
Converts a natural language question into a SQL query using an LLM. The
schema shown to the model is filtered to only the tables the user's role
is allowed to see -- this is the first layer of governance (least-privilege
prompting), before the guard.py validation layer double-checks everything
downstream.

Two providers are supported, selected via the LLM_PROVIDER env var:
- "ollama" (default): local Ollama model, for offline demo rehearsal.
- "bedrock": Claude Sonnet 4.5 on AWS Bedrock, for the office deployment.
"""
import os
import re
from datetime import date

import requests

from governance_rules import get_role_config

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "ollama").lower()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:7b"

# Sonnet 4.5 requires cross-region inference on Bedrock -- the bare model ID
# is rejected with "on-demand throughput isn't supported". The "global."
# prefix is AWS's recommended inference profile (best availability, no
# regional pricing premium); override with BEDROCK_MODEL_ID if the office
# environment requires a regional profile (e.g. "us.anthropic...") instead.
BEDROCK_MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID", "global.anthropic.claude-sonnet-4-5-20250929-v1:0"
)

_bedrock_client = None

FULL_SCHEMA = {
    "regions": "region_id INTEGER, region_name TEXT",
    "employees": "employee_id INTEGER, full_name TEXT, role TEXT, region_id INTEGER, email TEXT, salary REAL, ssn TEXT",
    "customers": "customer_id INTEGER, customer_name TEXT, region_id INTEGER, email TEXT, phone TEXT",
    "orders": "order_id INTEGER, customer_id INTEGER, employee_id INTEGER, region_id INTEGER, product TEXT, quantity INTEGER, unit_price REAL, order_date TEXT",
}


def build_system_prompt(role: str) -> str:
    role_cfg = get_role_config(role)
    allowed = role_cfg["allowed_tables"]
    schema_lines = [f"- {t}({FULL_SCHEMA[t]})" for t in allowed if t in FULL_SCHEMA]
    schema_block = "\n".join(schema_lines)

    return f"""You are a SQL generator for a SQLite database. Translate the user's
question into a single read-only SELECT query.

Rules:
- Only use these tables/columns (others do not exist for this user):
{schema_block}
- Only generate SELECT statements. Never INSERT/UPDATE/DELETE/DROP.
- Return ONLY the raw SQL query, no explanation, no markdown fences.
- Use standard SQLite syntax."""


def build_user_prompt(question: str) -> str:
    return f"""Today's date is {date.today().isoformat()}. Resolve relative date references
("this year", "last quarter", "last month", etc.) against that date, not
against any other assumption. If the question names a calendar month
(January, February, ..., December, or an abbreviation) anywhere, even in
an unusual word order like "this year may" meaning "May of this year",
treat that as the intended month rather than as an ordinary word.

Question: {question}

SQL:"""


def _clean_sql(raw: str) -> str:
    raw = raw.strip()
    # Strip markdown fences if the model added them anyway
    raw = re.sub(r"^```sql\s*|^```\s*|```$", "", raw, flags=re.MULTILINE).strip()
    # Take just the first statement if the model rambles
    if ";" in raw:
        raw = raw.split(";")[0] + ";"
    return raw


def _generate_sql_ollama(question: str, role: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "system": build_system_prompt(role),
            "prompt": build_user_prompt(question),
            "stream": False,
            "options": {"temperature": 0},
        },
        timeout=60,
    )
    response.raise_for_status()
    return _clean_sql(response.json().get("response", ""))


def _get_bedrock_client():
    global _bedrock_client
    if _bedrock_client is None:
        from anthropic import AnthropicBedrock

        _bedrock_client = AnthropicBedrock()
    return _bedrock_client


def _generate_sql_bedrock(question: str, role: str) -> str:
    client = _get_bedrock_client()
    response = client.messages.create(
        model=BEDROCK_MODEL_ID,
        max_tokens=1024,
        temperature=0,
        system=build_system_prompt(role),
        messages=[{"role": "user", "content": build_user_prompt(question)}],
    )
    raw = next((b.text for b in response.content if b.type == "text"), "")
    return _clean_sql(raw)


def generate_sql(question: str, role: str) -> str:
    if LLM_PROVIDER == "bedrock":
        return _generate_sql_bedrock(question, role)
    return _generate_sql_ollama(question, role)
