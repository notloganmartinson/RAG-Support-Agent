import json
import random

def generate_tickets(count=50):
    tickets = []
    
    scenarios = [
        {
            "category": "Sharpe Ratio",
            "issue": "Sharpe ratio calculation anomaly in Portfolio Analysis tool.",
            "error_logs": "ERROR: [CalcEngine] Invalid arithmetic operation in volatility normalization. Code: CALC-003",
            "resolution": "Update the risk-free rate configuration in the local settings. Ensure it matches the 10-year Treasury yield format.",
            "notes": "User reported that Sharpe ratios were appearing as negative despite positive returns."
        },
        {
            "category": "Direct API",
            "issue": "Direct API timeout when fetching historical NAVs for European mutual funds.",
            "error_logs": "TIMEOUT: [API-Gateway] Request to /v1/historical/nav timed out after 30000ms. Code: TIMEOUT-101",
            "resolution": "Increase the timeout parameter in the request header to 60000ms for large datasets.",
            "notes": "Occurs mostly during peak trading hours in London."
        },
        {
            "category": "X-Ray Feed",
            "issue": "X-Ray feed latency causing delayed portfolio composition updates.",
            "error_logs": "LATENCY: [FeedSync] Sync delay exceeds 300s. Warning: FEED-99",
            "resolution": "Flush the local feed cache and trigger a manual resync using the /sync/force endpoint.",
            "notes": "L1 checked the server status, but the issue persists on the client side."
        },
        {
            "category": "Mutual Fund NAVs",
            "issue": "Missing mutual fund NAVs for specific bond funds in the Direct database.",
            "error_logs": "NULL_VAL: [DB-Query] Expected NAV for ID:88219 not found. Code: DB-404",
            "resolution": "Map the fund ID to the correct ticker symbol in the Data Manager mapping table.",
            "notes": "Funds were recently reclassified from Equity to Fixed Income."
        },
        {
            "category": "Authentication",
            "issue": "User cannot login to Morningstar Direct Desktop client.",
            "error_logs": "AUTH_FAIL: [LoginManager] Token verification failed. Error: ERR-AUTH-702",
            "resolution": "Clear the application cookies and re-authenticate using SSO.",
            "notes": "User has valid credentials but gets a 'Forbidden' error after login attempt."
        },
        {
            "category": "Report Generation",
            "issue": "PDF report generation fails for large portfolios (500+ holdings).",
            "error_logs": "MEM_EXCEEDED: [ReportSrv] Heap space error during PDF rendering. Code: MEM-500",
            "resolution": "Increase the JVM memory allocation for the report service in config.ini.",
            "notes": "Small portfolios work fine."
        },
        {
            "category": "Data Discrepancy",
            "issue": "Discrepancy in Dividend Yield between X-Ray and Direct API.",
            "error_logs": "DATA_MISMATCH: [Validator] Diff found in field 'DivYield' for Security:ISIN123. Code: DATA-001",
            "resolution": "Check the data source priority in the Portfolio Settings. Ensure 'Direct API' is set as primary.",
            "notes": "Direct API uses trailing 12 months, while X-Ray was using forward-looking estimates."
        },
        {
            "category": "Proxy Configuration",
            "issue": "Morningstar Direct cannot connect through the corporate proxy.",
            "error_logs": "PROXY_AUTH: [NetworkSrv] 407 Proxy Authentication Required. Code: NET-407",
            "resolution": "Add the proxy credentials to the 'Connection' tab in the application settings.",
            "notes": "User is behind a Zscaler proxy."
        }
    ]

    unresolved_scenarios = [
        {
            "category": "Unknown Error",
            "issue": "Intermittent crash when switching between 'Equity' and 'Fixed Income' tabs in Portfolio Manager.",
            "error_logs": "CRASH: [UI-Thread] Fatal signal 11 (SIGSEGV). Address: 0xdeadbeef",
            "notes": "Occurs only on Windows 11 with 4K monitors. L1 tried reinstalling, but it didn't help."
        },
        {
            "category": "Novel Security Type",
            "issue": "Unable to calculate risk metrics for new 'Green ESG' crypto-linked bonds.",
            "error_logs": "UNSUPPORTED: [RiskEngine] Security type 'ESG-CRYPTO-BOND' not recognized. Code: RISK-404",
            "notes": "Product team hasn't added support for this security type yet. Escalated to engineering."
        },
        {
            "category": "Data Corruption",
            "issue": "Portfolio returns showing 1000%+ for standard S&P 500 tracking funds.",
            "error_logs": "VAL_RANGE: [AuditLog] Return calculation for ID:9912 out of bounds. Code: VAL-999",
            "notes": "Database seems to have corrupted historical prices for certain dates in 2023."
        }
    ]

    for i in range(count):
        is_unresolved = random.random() < 0.20
        if is_unresolved:
            base = random.choice(unresolved_scenarios)
            status = "Unresolved"
            resolution = None
        else:
            base = random.choice(scenarios)
            status = "Resolved"
            resolution = base["resolution"]
        
        ticket = {
            "ticket_id": f"TCK-{8000 + i}",
            "issue_description": base["issue"],
            "error_logs": base["error_logs"],
            "status": status,
            "proven_resolution": resolution,
            "troubleshooting_notes": base["notes"]
        }
        tickets.append(ticket)
    
    return tickets

if __name__ == "__main__":
    tickets = generate_tickets(100)
    with open("tickets.json", "w") as f:
        json.dump(tickets, f, indent=4)
    print(f"Generated {len(tickets)} tickets in tickets.json")
