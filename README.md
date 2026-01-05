# Customer Support Agent

A simple customer support chat agent built using:
- Groq LLM
- Retrieval-Augmented Generation (RAG)
- Conversation memory
- Basic action tools (ticket creation)

This project is part of a step-by-step learning series on AI agents.

---

## Features
- Chat-based customer support
- Answers questions using internal documents (RAG)
- Maintains conversation history
- Can create a support ticket (mock action)
- Runs locally (CLI)

---

## Tech Stack
- Python 3.10+
- Groq LLM
- LangChain
- ChromaDB (vector store)
- HuggingFace embeddings

---

## Project Structure
customer-support-agent/
├── src/
│ ├── app.py # Main CLI app
│ ├── rag.py # RAG logic
│ ├── memory.py # Conversation memory
│ ├── actions.py # Support actions (ticket creation)
│ └── prompts.py # System prompts
├── data/
│ └── documents/ # Knowledge base
├── requirements.txt
├── .gitignore
└── README.md