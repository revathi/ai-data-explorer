"""
Unit tests for the governance guard (app/guard.py).

These cover the checklist AGENTS.md already calls out as the
must-not-regress behaviors:
1. disallowed tables are blocked
2. write/DDL operations are blocked regardless of role
3. row filters get injected for roles that have them
4. column masking (hide vs redact) applies correctly
"""
import pytest

from guard import validate_and_secure_sql, apply_column_masking, GovernanceViolation


# --- 1. Table allowlist ---

def test_disallowed_table_is_blocked():
    with pytest.raises(GovernanceViolation, match="employees"):
        validate_and_secure_sql(
            "SELECT salary FROM employees", "sales_rep", {"region_id": 3}
        )


def test_allowed_table_passes():
    secured = validate_and_secure_sql(
        "SELECT product, SUM(quantity * unit_price) FROM orders GROUP BY product",
        "sales_rep",
        {"region_id": 3},
    )
    assert "orders" in secured


# --- 2. Only SELECT, ever ---

@pytest.mark.parametrize(
    "raw_sql",
    [
        "DELETE FROM orders",
        "UPDATE orders SET quantity = 0",
        "DROP TABLE orders",
        "INSERT INTO orders (order_id) VALUES (999)",
    ],
)
def test_write_and_ddl_statements_blocked_regardless_of_role(raw_sql):
    for role in ("sales_rep", "finance", "support", "admin"):
        with pytest.raises(GovernanceViolation):
            validate_and_secure_sql(raw_sql, role, {"region_id": None})


def test_non_sql_input_is_blocked_not_raised_as_generic_error():
    with pytest.raises(GovernanceViolation):
        validate_and_secure_sql("this is not sql at all;;;", "admin", {"region_id": None})


# --- 3. Row-filter injection ---

def test_row_filter_injected_for_sales_rep():
    secured = validate_and_secure_sql(
        "SELECT product, SUM(quantity * unit_price) FROM orders GROUP BY product",
        "sales_rep",
        {"region_id": 3},
    )
    assert "region_id = 3" in secured


def test_row_filter_anded_onto_existing_where_clause():
    secured = validate_and_secure_sql(
        "SELECT product FROM orders WHERE product = 'Widget Pro'",
        "sales_rep",
        {"region_id": 3},
    )
    assert "region_id = 3" in secured
    assert "Widget Pro" in secured


def test_no_row_filter_for_roles_without_one():
    # finance has no row_filter configured -- region_id should not appear
    secured = validate_and_secure_sql(
        "SELECT * FROM orders", "finance", {"region_id": None}
    )
    assert "region_id =" not in secured


# --- Defense-in-depth: LIMIT enforcement ---

def test_limit_added_when_missing():
    secured = validate_and_secure_sql(
        "SELECT * FROM orders", "admin", {"region_id": None}
    )
    assert "LIMIT" in secured.upper()


def test_existing_limit_not_duplicated():
    secured = validate_and_secure_sql(
        "SELECT * FROM orders LIMIT 5", "admin", {"region_id": None}
    )
    assert secured.upper().count("LIMIT") == 1


# --- 4. Column masking ---

def test_redact_masks_value_but_keeps_column():
    columns = ["customer_name", "email", "phone"]
    rows = [("Acme Corp", "contact@acme.com", "+1-555-11111")]
    new_columns, new_rows = apply_column_masking(columns, rows, "sales_rep", "customers")
    assert new_columns == ["customer_name", "email", "phone"]
    assert new_rows == [("Acme Corp", "***", "***")]


def test_hide_strips_column_entirely():
    columns = ["full_name", "salary", "ssn"]
    rows = [("Priya Nair", 95000, "444-55-6666")]
    new_columns, new_rows = apply_column_masking(columns, rows, "finance", "employees")
    assert new_columns == ["full_name", "salary"]
    assert new_rows == [("Priya Nair", 95000)]


def test_no_masking_rules_returns_data_unchanged():
    columns = ["region_id", "region_name"]
    rows = [(1, "North America")]
    new_columns, new_rows = apply_column_masking(columns, rows, "admin", "regions")
    assert new_columns == columns
    assert new_rows == rows
