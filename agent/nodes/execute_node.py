from tools.tools import execute_safe_sql


def execute_node(state):

    sql = state["sql"]

    result = execute_safe_sql(sql)

    return {
        "query_result": str(result)
    }