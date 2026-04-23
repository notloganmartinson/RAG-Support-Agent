# Mocking a Live Morningstar Production Database

SYSTEM_STATUS = {
    "DIRECT_API": {"status": "OPERATIONAL", "latency": "45ms"},
    "XRAY_FEED": {"status": "DEGRADED", "message": "High latency in European nodes"},
    "PORTFOLIO_ANALYSIS": {"status": "OPERATIONAL"},
    "FUND_88219": {"status": "SUSPENDED", "reason": "Awaiting regulatory filing update"},
}

def check_system_status(entity_name):
    """Simulates a live API call to Morningstar production monitors."""
    entity = entity_name.upper().replace(" ", "_")
    
    # Try direct match
    if entity in SYSTEM_STATUS:
        return SYSTEM_STATUS[entity]
    
    # Try fuzzy match for Fund IDs
    for key in SYSTEM_STATUS:
        if key in entity:
            return SYSTEM_STATUS[key]
            
    return {"status": "UNKNOWN", "message": "Entity not found in live monitors."}
