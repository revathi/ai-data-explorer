"""
Sanity tests for app/governance_rules.py -- the source-of-truth config
dict. These mostly guard against typos/shape regressions when someone
edits ROLES or USERS.
"""
import pytest

from governance_rules import ROLES, USERS, get_role_config


def test_get_role_config_returns_known_role():
    cfg = get_role_config("sales_rep")
    assert cfg["allowed_tables"] == {"orders", "customers", "regions"}


def test_get_role_config_raises_on_unknown_role():
    with pytest.raises(ValueError, match="Unknown role"):
        get_role_config("not_a_real_role")


def test_every_user_maps_to_a_known_role():
    for user_key, user in USERS.items():
        assert user["role"] in ROLES, f"{user_key} has unknown role {user['role']}"


def test_admin_and_finance_never_expose_ssn():
    # org policy from README/AGENTS.md: SSNs never returned via the NL interface
    for role_name in ("finance", "admin"):
        masks = ROLES[role_name].get("column_masks", {}).get("employees", {})
        assert masks.get("ssn") == "hide"
