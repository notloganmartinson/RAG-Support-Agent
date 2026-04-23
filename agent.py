import requests
import re
import json
from db import search_tickets
from scrubber import scrub_text
from mock_systems import check_system_status
from rich.console import Console
from rich.panel import Panel

console = Console()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

SYSTEM_PROMPT = """You are a Morningstar Support Specialist.
Your task is to resolve a user's ticket using:
1. [LIVE SYSTEM STATUS]: Current real-time data from production monitors.
2. [HISTORICAL DATA]: Past tickets from our database.

INSTRUCTIONS:
- Prioritize [LIVE SYSTEM STATUS]. If a system is 'DEGRADED' or 'SUSPENDED', mention this first as the likely cause.
- Use [HISTORICAL DATA] to provide specific technical fixes (timeouts, error codes).
- You MUST include technical values (e.g., 60000ms).
- IF NO RESOLVED FIX EXISTS: 
    1. You MUST start with the header: "⚠️ NO PROVEN RESOLUTION FOUND IN HISTORICAL DATABASE."
    2. You MUST list the steps that ALREADY FAILED (from PREVIOUS_FAILURES) and tell the user NOT to repeat them.
    3. Label your synthesis clearly as "PROPOSED EXPERIMENTAL STEPS".
- If PII is masked (e.g., [EMAIL]), refer to it by the placeholder.
"""

def call_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0}
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]

def run_agent(user_query):
    # Step 1: PII Scrubbing (Institutional Safety)
    clean_query = scrub_text(user_query)
    if clean_query != user_query:
        console.print("[bold red]Security Notice:[/bold red] PII detected and masked.")

    # Step 2: Live System Check (Institutional Context)
    # Detect entities (Simple heuristic for demo)
    live_context = ""
    entities = ["DIRECT API", "XRAY FEED", "FUND 88219", "PORTFOLIO ANALYSIS"]
    for entity in entities:
        if entity.lower() in clean_query.lower():
            status = check_system_status(entity)
            live_context += f"- {entity}: {status}\n"

    # Step 3: Historical Retrieval
    console.print(f"[bold cyan]Searching for relevant data...[/bold cyan]")
    historical_context = search_tickets(clean_query, n_results=3)
    
    # Audit Layer: Force Guardrails in code, not just prompt
    is_resolved = "STATUS: Resolved" in historical_context
    warning_prefix = ""
    if not is_resolved and "STATUS: Unresolved" in historical_context:
        warning_prefix = "⚠️ NO PROVEN RESOLUTION FOUND IN HISTORICAL DATABASE.\n"
        warning_prefix += "NOTE: The following steps have ALREADY FAILED and should NOT be repeated: "
        # Extract failed steps from the context to warn the user
        failed_match = re.findall(r"PREVIOUS_FAILURES: (.*?)(?=\n|\||$)", historical_context)
        if failed_match:
            warning_prefix += ", ".join(set(failed_match)) + "\n\n"

    # Step 4: Final Synthesis
    prompt = f"{SYSTEM_PROMPT}\n\n[LIVE SYSTEM STATUS]\n{live_context or 'No specific system match.'}\n\n[HISTORICAL DATA]\n{historical_context}\n\nUser Ticket: {clean_query}\n\nFinal Answer:"
    
    response = call_llm(prompt)
    
    # Prepend the hardcoded audit warning if necessary
    final_output = warning_prefix + response
    
    console.print(f"[bold yellow]Agent Response:[/bold yellow]")
    console.print(final_output)
    
    return final_output, historical_context 

if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Sharpe ratio anomaly"
    run_agent(query)
