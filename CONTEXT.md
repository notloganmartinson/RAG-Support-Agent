# Context: Phase 1 - Morningstar Support ReAct Agent

## Project Objective
Build an air-gapped, proof-of-concept ReAct agent that intercepts complex B2B financial software support tickets. The agent queries a local vector database of historical tickets. If a proven solution exists, it drafts a step-by-step resolution protocol. If the issue is historically unsolved or novel, it synthesizes a proposed troubleshooting plan based on similar symptom data before routing to a human.

## Architecture Stack
* **LLM:** Qwen2.5:3b (Running locally via Ollama/Llama.cpp).
* **Vector Store:** ChromaDB (Local, fast).
* **Embeddings:** `all-MiniLM-L6-v2` (Lightweight, runs easily in 16GB RAM/6GB VRAM alongside the 3B model).
* **Framework:** Custom Python ReAct loop (No LangChain).
* **Interface:** FastAPI backend with a CLI entry point for testing.

## Core Agent Logic Updates
* **The Dataset:** The historical dataset must contain a mix of resolved and unresolved tickets.
* **The Fallback:** The agent must not simply give up if a ticket lacks a `proven_resolution`. It must use semantic similarities from unresolved or partially related tickets to propose a set of logical next steps.

## Phase 1 Deliverables
* `sprint-1-data.md`: Synthesize the mixed-status dataset.
* `sprint-2-vector-db.md`: Build the ChromaDB ingestion pipeline.
* `sprint-3-react-agent.md`: Build the custom routing logic and strict ReAct parser.
