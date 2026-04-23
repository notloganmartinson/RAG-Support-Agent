# Sprint 1: Data Synthesis (The Morningstar Dataset)

## Sprint Goal
Generate a realistic JSON dataset of 50-100 Morningstar B2B support tickets. Crucially, 20% of these tickets must represent unresolved, escalated, or pending issues to test the agent's fallback logic.

## Tasks

### 1. Environment & Script Setup
* Initialize a Python virtual environment.
* Install dependencies: `pip install requests chromadb sentence-transformers pydantic`.
* Create `data_generator.py`. 

### 2. Generate the JSON Data
* You can use a local script calling Qwen, or manually use a larger API off-the-record to generate the base file quickly so you have high-quality synthetic data.
* Ensure domain-specific Morningstar terminology (e.g., Sharpe ratio anomalies, Direct API timeout, X-Ray feed latency, missing mutual fund NAVs).

### 3. Schema Enforcement
* `ticket_id`: String (e.g., "TCK-8921").
* `issue_description`: String (Detailed B2B software complaint).
* `error_logs`: String (Synthetic stack traces or exact error codes).
* `status`: String ("Resolved" or "Unresolved").
* `proven_resolution`: String (Actionable steps if Resolved. Null/Empty if Unresolved).
* `troubleshooting_notes`: String (Steps already tried by L1/L2 reps—especially important for Unresolved tickets).

## Definition of Done
A strictly formatted `tickets.json` file sits in the root directory, containing a realistic mix of solved and unsolved financial software issues.
