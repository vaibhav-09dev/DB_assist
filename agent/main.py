import os
import uuid

from dotenv import load_dotenv

from langchain_core.messages import HumanMessage

from langgraph.checkpoint.postgres import PostgresSaver

from graph import build_graph


load_dotenv()


CHECKPOINT_DB_URI = os.getenv(
    "CHECKPOINT_DB_URI"
)


def main():

    if not CHECKPOINT_DB_URI:
        raise ValueError(
            "CHECKPOINT_DB_URI is missing from .env"
        )

    # ==========================================
    # PostgreSQL Checkpointer
    # ==========================================

    with PostgresSaver.from_conn_string(
        CHECKPOINT_DB_URI
    ) as checkpointer:

        # Create LangGraph checkpoint tables
        checkpointer.setup()

        # ======================================
        # Build LangGraph
        # ======================================

        graph = build_graph(
            checkpointer
        )

        print("\nText-to-SQL Agent")
        print("Type 'exit' to quit.\n")

        # ======================================
        # Create a unique conversation/thread
        # ======================================

        thread_id = str(
            uuid.uuid4()
        )

        print(
            f"Thread ID: {thread_id}"
        )

        # ======================================
        # LangGraph configuration
        # ======================================

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        # ======================================
        # Chat loop
        # ======================================

        while True:

            question = input(
                "\nYou: "
            ).strip()

            # Exit
            if question.lower() == "exit":
                break

            # Ignore empty input
            if not question:
                continue

            # ==================================
            # Initial graph state
            # ==================================

            initial_state = {

                "question": question,

                "messages": [
                    HumanMessage(
                        content=question
                    )
                ],

                "retry_count": 0,

                "validation_error": "",

                "sql": "",

                "schema": "",

                "query_result": "",

                "final_answer": "",
            }

            # ==================================
            # Run LangGraph
            # ==================================

            result = graph.invoke(
                initial_state,
                config=config
            )

            # ==================================
            # Display final answer
            # ==================================

            print(
                "\nAgent:",
                result["final_answer"]
            )


if __name__ == "__main__":
    main()