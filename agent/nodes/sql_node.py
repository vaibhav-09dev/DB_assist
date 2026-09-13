import os
import re

from ollama import chat
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:1.7b"
)


SYSTEM_PROMPT = """
You are an expert PostgreSQL Text-to-SQL agent.

Your job is to convert READ-ONLY user questions into PostgreSQL SELECT queries.

IMPORTANT:
The database is READ-ONLY.

STRICT RULES:

1. Only generate SELECT queries.
2. Never generate INSERT.
3. Never generate UPDATE.
4. Never generate DELETE.
5. Never generate DROP.
6. Never generate ALTER.
7. Never generate CREATE.
8. Never modify the database.
9. Use only tables and columns present in the schema.
10. Do not invent tables or columns.
11. If the user asks to DELETE, UPDATE, INSERT, DROP, ALTER,
    CREATE, TRUNCATE, REMOVE, MODIFY or CHANGE database data,
    return exactly:

NOT_ALLOWED

12. Never convert a write request into a SELECT query.
13. Return ONLY SQL or NOT_ALLOWED.
14. Do not use markdown code blocks.

Examples:

User: Show all customers
Output:
SELECT * FROM customers;

User: List all customers from Delhi
Output:
SELECT * FROM customers WHERE city = 'Delhi';

User: How many customers are there?
Output:
SELECT COUNT(*) FROM customers;

User: Delete Eva
Output:
NOT_ALLOWED

User: Remove customer 5
Output:
NOT_ALLOWED

User: Update Eva's city to Mumbai
Output:
NOT_ALLOWED

User: Insert a new customer
Output:
NOT_ALLOWED

User: Drop the customers table
Output:
NOT_ALLOWED
"""


# ============================================================
# Check whether the user's request is a database modification
# ============================================================

def is_write_request(question: str) -> bool:

    write_patterns = [
        r"\bdelete\b",
        r"\bremove\b",
        r"\bupdate\b",
        r"\binsert\b",
        r"\bdrop\b",
        r"\balter\b",
        r"\bcreate\b",
        r"\btruncate\b",
        r"\bmodify\b",
        r"\bchange\b",
    ]

    question = question.lower()

    for pattern in write_patterns:

        if re.search(pattern, question):
            return True

    return False


# ============================================================
# SQL NODE
# ============================================================

def sql_node(state):

    question = state["question"]
    schema = state["schema"]

    # --------------------------------------------------------
    # FIRST SAFETY CHECK
    # --------------------------------------------------------

    if is_write_request(question):

        print("\n--- SQL GENERATION ---")
        print("Write operation detected.")
        print("SQL generation blocked.")

        return {
            "sql": "",
            "validation_error": (
                "This agent is read-only. "
                "INSERT, UPDATE, DELETE, DROP, ALTER, "
                "CREATE and other database modification "
                "operations are not allowed."
            ),
            "retry_count": state.get(
                "retry_count",
                0
            )
        }

    # --------------------------------------------------------
    # Conversation context
    # --------------------------------------------------------

    messages = state.get(
        "messages",
        []
    )

    previous_context = ""

    if messages:

        previous_context = (
            "\nPrevious conversation:\n"
        )

        for message in messages[-10:]:

            previous_context += (
                f"{message.type}: "
                f"{message.content}\n"
            )

    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

DATABASE SCHEMA:

{schema}

{previous_context}

CURRENT USER QUESTION:

{question}

Generate the PostgreSQL SELECT query.

Return ONLY SQL.
"""

    # --------------------------------------------------------
    # Call Ollama
    # --------------------------------------------------------

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql = response["message"]["content"].strip()

    # --------------------------------------------------------
    # Remove markdown code fences
    # --------------------------------------------------------

    sql = re.sub(
        r"```sql",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.replace(
        "```",
        ""
    ).strip()

    # --------------------------------------------------------
    # Handle NOT_ALLOWED from LLM
    # --------------------------------------------------------

    if sql.upper() == "NOT_ALLOWED":

        return {
            "sql": "",
            "validation_error": (
                "This agent is read-only. "
                "Database modification operations "
                "are not allowed."
            ),
            "retry_count": state.get(
                "retry_count",
                0
            )
        }

    # --------------------------------------------------------
    # Return generated SQL
    # --------------------------------------------------------

    print("\n--- GENERATED SQL ---")
    print(sql)

    return {
        "sql": sql,
        "validation_error": "",
        "retry_count": state.get(
            "retry_count",
            0
        )
    }