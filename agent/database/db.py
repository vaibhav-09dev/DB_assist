import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

engine=create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

def get_schema():
    inspector=inspect(engine)
    schema={}
    for table in inspector.get_table_names():
        columns=inspector.get_columns(table)
        schema[table]=[
            {
                "name": column["name"],
                "type": str(column["type"])
            }
            for column in columns
        ]
    return schema

def execute_sql(sql:str):
    with engine.connect() as connection:
        result=connection.execute(text(sql))
        rows=result.fetchall()
        columns=result.keys()
        return {
            "columns": list(columns),
            "rows": [list(row) for row in rows]
        }
def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True

    except Exception as e:
        print(f"Database connection error: {e}")
        return False