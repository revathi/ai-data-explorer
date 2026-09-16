"""
End-to-end tests for the /ask Flask route (app/app.py), driven through
Flask's test client against the real seeded SQLite DB.

The local Ollama call (nl2sql.generate_sql) is monkeypatched so these
tests don't require Ollama to be running -- we're testing our own
governance/execution pipeline, not the LLM's SQL-writing ability.
"""
import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def fake_generate_sql(sql):
    """Returns a monkeypatch replacement for generate_sql that ignores
    the question/role and always returns `sql`."""
    def _fake(question, role):
        return sql
    return _fake


def test_missing_question_returns_400(client):
    resp = client.post("/ask", json={"user": "asha (sales_rep, APAC)"})
    assert resp.status_code == 400


def test_unknown_user_returns_400(client):
    resp = client.post("/ask", json={"question": "hi", "user": "nobody"})
    assert resp.status_code == 400


def test_ollama_unreachable_returns_500(client, monkeypatch):
    def _raise(question, role):
        raise ConnectionError("Ollama is not running")

    monkeypatch.setattr(app_module, "generate_sql", _raise)
    resp = client.post(
        "/ask",
        json={"question": "anything", "user": "asha (sales_rep, APAC)"},
    )
    assert resp.status_code == 500
    assert "Ollama" in resp.get_json()["error"]


def test_sales_rep_query_gets_region_filtered_and_returns_rows(client, monkeypatch):
    monkeypatch.setattr(
        app_module,
        "generate_sql",
        fake_generate_sql(
            "SELECT product, SUM(quantity * unit_price) AS revenue "
            "FROM orders GROUP BY product"
        ),
    )
    resp = client.post(
        "/ask",
        json={
            "question": "revenue by product",
            "user": "asha (sales_rep, APAC)",  # region_id 3
        },
    )
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["blocked"] is False
    assert "region_id = 3" in body["log"]["secured_sql"]
    assert body["columns"] == ["product", "revenue"]
    assert len(body["rows"]) > 0


def test_sales_rep_blocked_from_employees_table(client, monkeypatch):
    monkeypatch.setattr(
        app_module, "generate_sql", fake_generate_sql("SELECT salary FROM employees")
    )
    resp = client.post(
        "/ask",
        json={"question": "show salaries", "user": "asha (sales_rep, APAC)"},
    )
    body = resp.get_json()
    assert body["blocked"] is True
    assert "employees" in body["reason"]


def test_sales_rep_customer_contact_info_is_redacted(client, monkeypatch):
    monkeypatch.setattr(
        app_module,
        "generate_sql",
        fake_generate_sql("SELECT customer_name, email, phone FROM customers"),
    )
    resp = client.post(
        "/ask",
        json={"question": "customer contact info", "user": "asha (sales_rep, APAC)"},
    )
    body = resp.get_json()
    assert body["blocked"] is False
    assert body["columns"] == ["customer_name", "email", "phone"]
    for row in body["rows"]:
        assert row[1] == "***"
        assert row[2] == "***"


def test_finance_sees_salary_but_never_ssn(client, monkeypatch):
    monkeypatch.setattr(
        app_module,
        "generate_sql",
        fake_generate_sql("SELECT full_name, salary, ssn FROM employees"),
    )
    resp = client.post(
        "/ask",
        json={"question": "employee comp", "user": "priya (finance)"},
    )
    body = resp.get_json()
    assert body["blocked"] is False
    # ssn column must be stripped entirely, not just redacted
    assert "ssn" not in body["columns"]
    assert "salary" in body["columns"]


def test_write_statement_from_llm_is_blocked_not_executed(client, monkeypatch):
    monkeypatch.setattr(
        app_module,
        "generate_sql",
        fake_generate_sql("DELETE FROM orders WHERE 1=1"),
    )
    resp = client.post(
        "/ask",
        json={"question": "delete everything", "user": "sanjay (admin)"},
    )
    body = resp.get_json()
    assert body["blocked"] is True
