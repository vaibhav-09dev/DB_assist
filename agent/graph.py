from langgraph.graph import StateGraph, START, END

from state import AgentState

from nodes.schema_node import schema_node
from nodes.sql_node import sql_node
from nodes.validate_node import validate_node
from nodes.execute_node import execute_node
from nodes.answer_node import answer_node


def validation_router(state: AgentState):

    validation_error = state.get(
        "validation_error",
        ""
    )

    retry_count = state.get(
        "retry_count",
        0
    )

    # SQL is valid
    if not validation_error:
        return "execute"

    # Maximum retries reached
    if retry_count >= 2:
        return "answer"

    # Try generating SQL again
    return "retry"


def retry_node(state: AgentState):

    return {
        "retry_count": state.get(
            "retry_count",
            0
        ) + 1
    }


def build_graph(checkpointer):

    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node(
        "get_schema",
        schema_node
    )

    builder.add_node(
        "generate_sql",
        sql_node
    )

    builder.add_node(
        "validate_sql",
        validate_node
    )

    builder.add_node(
        "retry",
        retry_node
    )

    builder.add_node(
        "execute_sql",
        execute_node
    )

    builder.add_node(
        "answer",
        answer_node
    )

    # Edges

    builder.add_edge(
        START,
        "get_schema"
    )

    builder.add_edge(
        "get_schema",
        "generate_sql"
    )

    builder.add_edge(
        "generate_sql",
        "validate_sql"
    )

    builder.add_conditional_edges(
        "validate_sql",
        validation_router,
        {
            "execute": "execute_sql",
            "retry": "retry",
            "answer": "answer",
        }
    )

    builder.add_edge(
        "retry",
        "generate_sql"
    )

    builder.add_edge(
        "execute_sql",
        "answer"
    )

    builder.add_edge(
        "answer",
        END
    )

    return builder.compile(
        checkpointer=checkpointer
    )