import os
import sqlite3
import sys

from flask import Flask, request, jsonify, render_template

sys.path.insert(0, os.path.dirname(__file__))
from nl2sql import generate_sql
from guard import validate_and_secure_sql, GovernanceViolation, apply_column_masking
from governance_rules import USERS
from sqlglot import parse_one, exp

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "enterprise.db")

app = Flask(__name__)


def run_readonly_query(sql: str):
    # Open the connection in read-only mode as a final backstop --
    # even if every layer above somehow failed, the DB itself refuses writes.
    uri = f"file:{os.path.abspath(DB_PATH)}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    cur = conn.cursor()
    cur.execute(sql)
    columns = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()
    return columns, rows


@app.route("/")
def index():
    return render_template("index.html", users=list(USERS.keys()))


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    user_key = data.get("user")

    if not question or user_key not in USERS:
        return jsonify({"error": "Missing question or unknown user."}), 400

    user = USERS[user_key]
    role = user["role"]
    user_attrs = {"region_id": user["region_id"]}

    log = {"question": question, "user": user_key, "role": role}

    # 1. NL -> SQL
    try:
        raw_sql = generate_sql(question, role)
    except Exception as e:
        return jsonify({"error": f"Could not reach local LLM (Ollama running?): {e}"}), 500
    log["generated_sql"] = raw_sql

    # 2. Governance validation + row-filter injection
    try:
        secured_sql = validate_and_secure_sql(raw_sql, role, user_attrs)
    except GovernanceViolation as e:
        log["blocked_reason"] = str(e)
        return jsonify({"log": log, "blocked": True, "reason": str(e)})
    log["secured_sql"] = secured_sql

    # 3. Execute against read-only connection
    try:
        columns, rows = run_readonly_query(secured_sql)
    except Exception as e:
        return jsonify({"log": log, "error": f"Query execution failed: {e}"}), 500

    # 4. Column masking on results
    try:
        table_hint = next(t.name for t in parse_one(secured_sql, read="sqlite").find_all(exp.Table))
    except StopIteration:
        table_hint = ""
    columns, rows = apply_column_masking(columns, rows, role, table_hint)

    return jsonify({
        "log": log,
        "blocked": False,
        "columns": columns,
        "rows": rows,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5050)
