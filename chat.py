from agent import run_agent
from db import verify_ticket
from rich.console import Console
import re

console = Console()

def main():
    console.clear()
    console.print("[bold green]Morningstar Support - Institutional Grade Agent[/bold green]")
    console.print("System Status: [bold blue]PII Scrubber Active[/bold blue] | [bold blue]Live Monitors Connected[/bold blue]\n")

    while True:
        try:
            query = input("User Ticket > ")
            
            if query.lower() in ["exit", "quit"]:
                break
                
            if not query.strip():
                continue

            # Run agent and get context for feedback
            answer, context = run_agent(query)
            
            # Feedback Loop
            feedback = input("\nWas this resolution helpful? (y/n): ")
            if feedback.lower() == 'y':
                # Extract ticket IDs from context to verify them
                ticket_ids = re.findall(r"TICKET (TCK-\d+)", context)
                for tid in ticket_ids:
                    if verify_ticket(tid):
                        console.print(f"[bold green]Ticket {tid} marked as VERIFIED.[/bold green]")
            
            console.print("\n" + "="*50 + "\n")
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Closing session...[/yellow]")
            break

if __name__ == "__main__":
    main()
