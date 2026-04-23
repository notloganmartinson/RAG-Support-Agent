# Sprint 2: The Vector Pipeline

## Sprint Goal
Build a lightweight, purely local script to chunk the JSON data, generate embeddings using a small local model, and load them into ChromaDB.

## Tasks

### 1. Build `db.py`
* Initialize a persistent ChromaDB client saving to a local `./chroma_data` directory.
* Load the `SentenceTransformerEmbeddingFunction` using `all-MiniLM-L6-v2`. This ensures embedding generation happens instantly on your CPU/RAM without fighting Qwen for VRAM.

### 2. Chunking and Metadata Strategy
* Read `tickets.json`.
* Combine `issue_description` and `error_logs` into a single text payload for the vector embedding.
* Attach the rest of the fields (`ticket_id`, `status`, `proven_resolution`, `troubleshooting_notes`) strictly as metadata dictionaries.

### 3. Ingestion & Testing
* Run the script to populate the ChromaDB collection.
* Write a quick 5-line test function in `db.py` to run a hardcoded query (e.g., "NAV update failure") and print the top 3 metadata results to verify the embeddings work.

## Definition of Done
A populated `./chroma_data` directory exists, and `db.py` successfully returns semantically relevant historical tickets (both resolved and unresolved) based on a test query.
