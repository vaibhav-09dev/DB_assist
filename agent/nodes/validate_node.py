from tools.tools import validate_sql


def validate_node(state):

    sql = state["sql"]

    result = validate_sql(sql)

    print("\n--- VALIDATION RESULT ---")
    print(result)

    

    if isinstance(result, str):

        if result.strip().upper().startswith("VALID SQL"):
            return {
                "validation_error": ""
            }

        return {
            "validation_error": result
        }

    # If your validator returns True / False
    if isinstance(result, bool):

        if result:
            return {
                "validation_error": ""
            }

        return {
            "validation_error": "SQL validation failed."
        }

    # If your validator returns a dictionary
    if isinstance(result, dict):

        if result.get("valid") is True:
            return {
                "validation_error": ""
            }

        return {
            "validation_error": result.get(
                "error",
                "SQL validation failed."
            )
        }

    return {
        "validation_error": "Unknown validation result."
    }