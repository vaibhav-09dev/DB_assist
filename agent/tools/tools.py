
import re

import sqlglot
from sqlglot import exp

from database.db import execute_sql


def get_schema() -> str:
    """
    Return database schema information for the LLM.
    """

    return """
DATABASE: customers

TABLE: customers
--------------------------------
id      INTEGER PRIMARY KEY
name    VARCHAR(150)
email   VARCHAR(200)
city    VARCHAR(100)
age     INTEGER


TABLE: products
--------------------------------
id       INTEGER PRIMARY KEY
name     VARCHAR(150)
category VARCHAR(100)
price    NUMERIC(10,2)


TABLE: orders
--------------------------------
id          INTEGER PRIMARY KEY
customer_id INTEGER REFERENCES customers(id)
product_id  INTEGER REFERENCES products(id)
quantity    INTEGER
amount      NUMERIC(10,2)
order_date  DATE


RELATIONSHIPS
--------------------------------
orders.customer_id -> customers.id
orders.product_id -> products.id
"""


def validate_sql(sql: str) -> str:
    """
    Validate that generated SQL is safe and is a SELECT query.
    """

    sql = sql.strip()

    # Remove markdown code fences
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = sql.replace("```", "").strip()

    if not sql:
        return "INVALID: Empty SQL."

    try:
        parsed = sqlglot.parse_one(
            sql,
            dialect="postgres"
        )

    except Exception as e:
        return f"INVALID SQL: {e}"

    # Only allow SELECT queries.
    if not isinstance(parsed, exp.Select):
        return (
            "INVALID: Only SELECT queries are allowed. "
            "INSERT, UPDATE, DELETE, DROP, ALTER and other "
            "statements are forbidden."
        )

    forbidden = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke",
    ]

    lowered = sql.lower()

    for keyword in forbidden:

        if re.search(rf"\b{keyword}\b", lowered):

            return f"INVALID: Forbidden SQL operation: {keyword}"

    return f"VALID SQL:\n{sql}"


def execute_safe_sql(sql: str):
    """
    Execute validated read-only SQL.
    Only SELECT queries are allowed.
    """
    sql_clean = sql.strip()

    if not sql_clean.upper().startswith("SELECT"):
        return {
            "success": False,
            "error": "Only SELECT queries are allowed. Write operations are not permitted.",
            "rows": [],
            "row_count": 0,
        }
    validation = validate_sql(sql)

    validation = validate_sql(sql_clean)

    if not validation.startswith("VALID SQL"):
        return {
            "success": False,
            "error": validation,
            "rows": [],
            "row_count": 0,
        }

    try:

        rows = execute_sql(sql_clean)

        return {
            "success": True,
            "rows": rows,
            "row_count": len(rows),
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "rows": [],
            "row_count": 0,
        }