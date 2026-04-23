# Sprint 4: Institutional Grade (Live Data & Security)

## Sprint Goal
Bridge the gap between "Historical RAG" and "Corporate Infrastructure" by adding live system checks, data privacy layers, and a human feedback loop.

## Tasks

### 1. The PII Scrubber (Security Layer)
* Create `scrubber.py`. 
* Use regex to detect and mask:
    * Emails: `test@morningstar.com` -> `[EMAIL]`
    * Client IDs: `CID-12345` -> `[CLIENT_ID]`
    * ISINs/Account Numbers: `US123456789` -> `[SENSITIVE_ID]`
* Integrate this into `agent.py` so the LLM never sees raw PII.

### 2. The Live Data Bridge (Real-time Context)
* Create `mock_systems.py` to simulate a live Morningstar Production Database.
* Add a tool: `Check_System_Status(entity_id)`.
* If a ticket mentions a specific Fund or API, the agent must check its *current* status before suggesting historical fixes.

### 3. The Feedback Loop (Self-Improving Memory)
* Update `chat.py` to ask the user: "Was this resolution helpful? (y/n)".
* If "y", update the metadata of the matched ticket in ChromaDB with `verified: True`.
* Update `db.py` to prioritize `verified` tickets in search results.

## Definition of Done
The agent successfully scrubs a user's email from the prompt, checks a live mock database for "System Outages," and updates the vector database based on user feedback.
