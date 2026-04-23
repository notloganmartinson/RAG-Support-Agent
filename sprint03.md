# Sprint 3: The Custom ReAct Loop

## Sprint Goal
Write the core ReAct loop in `agent.py` that interacts with Qwen2.5:3b. Since 3B models are notorious for breaking formatting, implement strict regex parsing to keep the agent on track.

## Tasks

### 1. The Local LLM Connector
* Set up a clean Python function to POST to your local LLM endpoint (e.g., Ollama's `http://localhost:11434/api/generate`).

### 2. The Tool Definitions
* Define Python functions for the agent to call.
* `Search_Past_Tickets(query)`: Takes a string, queries ChromaDB, and returns the top 3 results formatted as a single string block.

### 3. The ReAct Prompt Template
* Write a rigid system prompt.
* Format constraint: Force the model to use exactly `Thought:`, `Action:`, `Action Input:`, and `Observation:`.
* Logic constraint: "If the search returns a 'Resolved' ticket, extract the exact steps. If the search returns 'Unresolved' tickets, analyze the 'troubleshooting_notes', synthesize a new proposed solution avoiding what already failed, and state clearly that this is a PROPOSED solution."

### 4. The Loop and Parser
* Build the `while` loop (max 5 iterations to prevent infinite loops).
* Write regex to extract the `Action` and `Action Input`.
* If the LLM breaks format, catch the exception, append an error message to the context ("System Error: Invalid format, please use Thought/Action/Action Input"), and force it to try again.

## Definition of Done
A CLI-executable `agent.py` where a user can type a complex support issue, and the terminal prints the LLM's step-by-step reasoning, tool execution, and final resolution protocol.
