"""
Seeds a sample 'enterprise production' SQLite database.
Domain: Sales + HR, with fields that are realistic to want governed
(regional sales data, employee salaries, customer PII).
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "enterprise.db")

SCHEMA = """
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS regions;

CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL,           -- e.g. sales_rep, finance, support, admin
    region_id INTEGER,
    email TEXT,
    salary REAL,                  -- sensitive: should be masked for non-finance roles
    ssn TEXT,                     -- sensitive: PII, should never be exposed
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region_id INTEGER,
    email TEXT,
    phone TEXT,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    employee_id INTEGER,          -- the sales rep who owns the order
    region_id INTEGER,
    product TEXT,
    quantity INTEGER,
    unit_price REAL,
    order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);
"""

REGIONS = [
    (1, "North America"),
    (2, "Europe"),
    (3, "APAC"),
]

EMPLOYEES = [
    (1, "Asha Menon", "sales_rep", 3, "asha.menon@corp.com", 78000, "111-22-3333"),
    (2, "David Kim", "sales_rep", 1, "david.kim@corp.com", 82000, "222-33-4444"),
    (3, "Elena Rossi", "sales_rep", 2, "elena.rossi@corp.com", 79500, "333-44-5555"),
    (4, "Priya Nair", "finance", None, "priya.nair@corp.com", 95000, "444-55-6666"),
    (5, "Mark Owusu", "support", None, "mark.owusu@corp.com", 61000, "555-66-7777"),
    (6, "Sanjay Rao", "admin", None, "sanjay.rao@corp.com", 110000, "666-77-8888"),
]

CUSTOMERS = [
    (1, "Nimbus Retail", 3, "contact@nimbusretail.com", "+91-98765-11111"),
    (2, "Acme Corp", 1, "contact@acme.com", "+1-555-11111"),
    (3, "Nordic Systems", 2, "contact@nordicsys.eu", "+45-2222-1111"),
    (4, "TechWave APAC", 3, "hello@techwave.io", "+65-8888-2222"),
    (5, "Blue Harbor Inc", 1, "info@blueharbor.com", "+1-555-22222"),
]

ORDERS = [
    (1, 1, 1, 3, "Widget Pro", 50, 25.0, "2026-05-01"),
    (2, 4, 1, 3, "Widget Pro", 20, 25.0, "2026-05-14"),
    (3, 2, 2, 1, "Gadget X", 10, 199.0, "2026-05-20"),
    (4, 5, 2, 1, "Gadget X", 5, 199.0, "2026-06-02"),
    (5, 3, 3, 2, "Widget Pro", 30, 25.0, "2026-06-10"),
    (6, 3, 3, 2, "Service Plan", 1, 4999.0, "2026-06-15"),
    (7, 1, 1, 3, "Service Plan", 1, 4999.0, "2026-07-01"),
    (8, 2, 2, 1, "Widget Pro", 100, 25.0, "2026-07-05"),
]


def seed():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    cur.executemany("INSERT INTO regions VALUES (?,?)", REGIONS)
    cur.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?,?)", EMPLOYEES)
    cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", CUSTOMERS)
    cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?)", ORDERS)
    conn.commit()
    conn.close()
    print(f"Seeded database at {DB_PATH}")


if __name__ == "__main__":
    seed()
