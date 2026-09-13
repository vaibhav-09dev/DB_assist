# DBAssist — Agentic AI Database Assistant

DBAssist is an **agentic AI database assistant** that allows users to interact with a PostgreSQL database using natural language. It converts user questions into SQL, validates the generated query for safety, executes it, and generates a human-readable response.

## ✨ Features

- 🧠 Natural-language database querying
- 🤖 Agentic workflow powered by LangGraph
- 📝 Automatic SQL generation using LLMs
- 🔍 Database schema inspection
- 🛡️ SQL validation and safe query execution
- 🐘 PostgreSQL database integration
- 🔄 Automatic retry when SQL validation fails
- 💬 Context-aware responses
- ⚡ Modular node-based architecture

## 🏗️ Architecture

DB Assist follows a **tool-calling agent architecture** with short-term conversational context.

```text
                    ┌──────────────────────┐
                    │      User Query      │
                    └──────────┬───────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │     Context Builder     │
                  │                         │
                  │ • System Prompt         │
                  │ • Previous Messages     │
                  │ • Current Question      │
                  └────────────┬────────────┘
                               │
                               ▼
                      ┌────────────────┐
                      │     Qwen3      │
                      │   via Ollama   │
                      └───────┬────────┘
                              │
                       Tool Selection
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
       ┌─────────────┐ ┌──────────────┐ ┌──────────────┐
       │ get_schema  │ │ validate_sql │ │ execute_sql  │
       └──────┬──────┘ └──────┬───────┘ └──────┬───────┘
              │               │                │
              └───────────────┴────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   PostgreSQL DB  │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   Query Result   │
                     └────────┬─────────┘
                              │
                              ▼
                      ┌────────────────┐
                      │     Qwen3      │
                      │ Final Response │
                      └───────┬────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │     User     │
                       └──────────────┘
