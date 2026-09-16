"""
Governance rule definitions.

In a real production system, this would be sourced from an external
policy store (OPA, a database, an IAM system, etc.) rather than
hardcoded. For the hackathon demo, rules live here so they're easy
to show and modify live during a demo.

Each role defines:
- allowed_tables: which tables this role may query at all
- column_masks: {table: {column: mask_strategy}}
    mask_strategy: "hide"   -> column is stripped from results entirely
                    "redact" -> column value is replaced with '***'
- row_filter: optional SQL WHERE fragment auto-injected into every
              query this role issues (e.g. restrict to their own region)
"""

ROLES = {
    "sales_rep": {
        "description": "Regional sales rep — sees only their own region's data, no salary/PII.",
        "allowed_tables": {"orders", "customers", "regions"},
        "column_masks": {
            "customers": {"email": "redact", "phone": "redact"},
        },
        # {region_id} gets substituted with the logged-in rep's region at query time
        "row_filter": {
            "orders": "region_id = {region_id}",
            "customers": "region_id = {region_id}",
        },
    },
    "finance": {
        "description": "Finance — full visibility into orders and employee compensation, no SSNs.",
        "allowed_tables": {"orders", "customers", "regions", "employees"},
        "column_masks": {
            "employees": {"ssn": "hide"},
        },
        "row_filter": {},  # no regional restriction
    },
    "support": {
        "description": "Support — can see orders/customers for service purposes, no financial or HR data.",
        "allowed_tables": {"orders", "customers", "regions"},
        "column_masks": {
            "customers": {"email": "redact", "phone": "redact"},
        },
        "row_filter": {},
    },
    "admin": {
        "description": "Admin — full access, still no raw SSNs (org policy: never return SSNs via NL interface).",
        "allowed_tables": {"orders", "customers", "regions", "employees"},
        "column_masks": {
            "employees": {"ssn": "hide"},
        },
        "row_filter": {},
    },
}

# Demo users mapped to roles + attributes used in row filters (e.g. their region)
USERS = {
    "asha (sales_rep, APAC)": {"role": "sales_rep", "region_id": 3},
    "david (sales_rep, NA)": {"role": "sales_rep", "region_id": 1},
    "priya (finance)": {"role": "finance", "region_id": None},
    "mark (support)": {"role": "support", "region_id": None},
    "sanjay (admin)": {"role": "admin", "region_id": None},
}


def get_role_config(role: str) -> dict:
    if role not in ROLES:
        raise ValueError(f"Unknown role: {role}")
    return ROLES[role]
