import os
import sys

# app.py itself does this same sys.path trick so its internal
# "from nl2sql import ..." style imports work regardless of cwd.
# Tests need the same thing to import guard/governance_rules/nl2sql/app
# as top-level modules instead of a package.
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
