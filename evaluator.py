import json
from agent import run_agent, console
from rich.table import Table

def evaluate():
    with open("eval_dataset.json", "r") as f:
        tests = json.load(f)

    results = []
    
    console.quiet = True 

    for test in tests:
        query = test["query"]
        expected = test["expected_keywords"]
        
        # run_agent now returns (answer, context)
        final_answer, _ = run_agent(query)
        
        found_keywords = [kw for kw in expected if kw.lower() in final_answer.lower()]
        score = (len(found_keywords) / len(expected)) * 100
        
        results.append({
            "category": test["category"],
            "query": query[:30] + "...",
            "score": f"{score:.1f}%",
            "passed": score >= 70
        })

    console.quiet = False
    
    table = Table(title="Agent Accuracy Evaluation Report")
    table.add_column("Category", style="cyan")
    table.add_column("Query Snippet", style="magenta")
    table.add_column("Accuracy", justify="right", style="green")
    table.add_column("Status", justify="center")

    for res in results:
        status = "[bold green]PASS[/bold green]" if res["passed"] else "[bold red]FAIL[/bold red]"
        table.add_row(res["category"], res["query"], res["score"], status)

    console.print(table)

if __name__ == "__main__":
    evaluate()
