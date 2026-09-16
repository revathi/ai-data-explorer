"""
Guardrail layer: the LLM's generated SQL is NEVER trusted or executed
directly. Every query passes through here first.

Defense in depth, in order:
  1. Parse-level check      -> must be a single SELECT statement
  2. Table allowlist check  -> every referenced table must be allowed for the role
  3. Row-level filter inject-> WHERE clause enforced per role (can't be bypassed by the LLM)
  4. (DB connection itself is opened read-only as a final backstop)
"""
import sqlglot
from sqlglot import exp

from governance_rules import get_role_config


class GovernanceViolation(Exception):
    """Raised when a query fails a governance check. Message is safe to show the user."""
    pass


def validate_and_secure_sql(raw_sql: str, role: str, user_attrs: dict) -> str:
    role_cfg = get_role_config(role)

    # --- 1. Parse ---
    try:
        parsed = sqlglot.parse_one(raw_sql, read="sqlite")
    except Exception as e:
        raise GovernanceViolation(f"Generated query could not be parsed as valid SQL: {e}")

    # --- 2. Must be SELECT only ---
    if not isinstance(parsed, exp.Select):
        raise GovernanceViolation(
            "Blocked: only read-only SELECT queries are permitted. "
            f"Detected statement type: {type(parsed).__name__}"
        )

    # Reject any nested write/DDL statements sneaking in (defense in depth)
    forbidden = (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create, exp.Alter)
    for node in parsed.walk():
        n = node[0] if isinstance(node, tuple) else node
        if isinstance(n, forbidden):
            raise GovernanceViolation(f"Blocked: query contains a forbidden operation ({type(n).__name__}).")

    # --- 3. Table allowlist check ---
    referenced_tables = {t.name for t in parsed.find_all(exp.Table)}
    disallowed = referenced_tables - role_cfg["allowed_tables"]
    if disallowed:
        raise GovernanceViolation(
            f"Blocked: role '{role}' is not permitted to access table(s): {', '.join(sorted(disallowed))}"
        )

    # --- 4. Enforce a LIMIT (protect against runaway result sets) ---
    if parsed.args.get("limit") is None:
        parsed = parsed.limit(200)

    # --- 5. Row-level filter injection ---
    row_filters = role_cfg.get("row_filter", {})
    for table in referenced_tables:
        if table in row_filters:
            filter_sql = row_filters[table].format(**user_attrs)
            condition = sqlglot.condition(filter_sql)
            existing_where = parsed.args.get("where")
            if existing_where:
                # AND the governance filter onto whatever the LLM already wrote
                new_where = exp.and_(existing_where.this, condition)
                parsed.set("where", exp.Where(this=new_where))
            else:
                parsed = parsed.where(condition)

    return parsed.sql(dialect="sqlite")


def apply_column_masking(columns: list[str], rows: list[tuple], role: str, table_hint: str) -> tuple[list[str], list[tuple]]:
    """Applies 'hide' (strip column) / 'redact' (replace value) masking to a result set."""
    role_cfg = get_role_config(role)
    masks = role_cfg.get("column_masks", {}).get(table_hint, {})
    if not masks:
        return columns, rows

    hide_idx = {i for i, c in enumerate(columns) if masks.get(c) == "hide"}
    redact_idx = {i for i, c in enumerate(columns) if masks.get(c) == "redact"}

    new_columns = [c for i, c in enumerate(columns) if i not in hide_idx]
    new_rows = []
    for row in rows:
        new_row = []
        for i, val in enumerate(row):
            if i in hide_idx:
                continue
            if i in redact_idx:
                new_row.append("***")
            else:
                new_row.append(val)
        new_rows.append(tuple(new_row))
    return new_columns, new_rows
