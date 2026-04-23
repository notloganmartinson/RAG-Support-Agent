import re

PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "CLIENT_ID": r"CID-\d{5,8}",
    "ISIN": r"[A-Z]{2}[A-Z0-9]{9}\d",
    "IP_ADDRESS": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
}

def scrub_text(text):
    if not text:
        return text
    
    scrubbed = text
    for label, pattern in PII_PATTERNS.items():
        scrubbed = re.sub(pattern, f"[{label}]", scrubbed)
    
    return scrubbed
