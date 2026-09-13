from tools.tools import get_schema

def schema_node(state):
    schema=get_schema()

    return{
        "schema":schema
    }

