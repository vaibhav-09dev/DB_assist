from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    question: str

    schema: str

    sql: str

    validation_error: str

    query_result: str

    final_answer: str

    retry_count: int