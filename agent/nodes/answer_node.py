import os

from dotenv import load_dotenv
from ollama import chat
from langchain_core.messages import AIMessage

load_dotenv()

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:1.7b",
)


def answer_node(state):

    question = state["question"]

    result = state.get(
        "query_result",
        ""
    )

    validation_error = state.get(
        "validation_error",
        ""
    )

    # If SQL could not be generated after retries
    if validation_error and not result:

        return {
            "final_answer": (
                "I couldn't generate a valid SQL query "
                f"for this request.\n\nReason: {validation_error}"
            )
        }

    prompt = f"""
You are a helpful database assistant.

User question:
{question}

Database result:
{result}

Answer the user's question using ONLY the database result.

Rules:

1. Do not invent information.
2. Do not mention internal SQL unless useful.
3. Be concise.
4. If there are multiple rows, summarize them clearly.
"""

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        
    )
    final_answer = response[
        "message"
    ][
        "content"
    ].strip()
    return {
    "final_answer": final_answer,
    "messages": [
        AIMessage(content=final_answer)
    ]
}