import json
import os
import chromadb
from chromadb.utils import embedding_functions

# Configuration
CHROMA_DATA_PATH = "./chroma_data"
COLLECTION_NAME = "support_tickets"
DATA_FILE = "tickets.json"

def get_db_client():
    return chromadb.PersistentClient(path=CHROMA_DATA_PATH)

def get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def initialize_collection():
    client = get_db_client()
    embedding_function = get_embedding_function()
    
    # Reset or get collection
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass
        
    return client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

def ingest_data():
    collection = initialize_collection()
    
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, "r") as f:
        tickets = json.load(f)

    documents = []
    metadatas = []
    ids = []

    for ticket in tickets:
        # Combine issue description and error logs for the payload
        payload = f"Issue: {ticket['issue_description']}\nLogs: {ticket['error_logs']}"
        
        documents.append(payload)
        metadatas.append({
            "ticket_id": ticket["ticket_id"],
            "status": ticket["status"],
            "proven_resolution": ticket["proven_resolution"] or "",
            "troubleshooting_notes": ticket["troubleshooting_notes"] or "",
            "verified": False
        })
        ids.append(ticket["ticket_id"])

    # Batch add to collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully ingested {len(ids)} tickets into {COLLECTION_NAME}.")

def verify_ticket(ticket_id):
    client = get_db_client()
    collection = client.get_collection(name=COLLECTION_NAME)
    
    # Get existing metadata
    result = collection.get(ids=[ticket_id])
    if result['ids']:
        metadata = result['metadatas'][0]
        metadata['verified'] = True
        collection.update(ids=[ticket_id], metadatas=[metadata])
        return True
    return False

def search_tickets(query_text, n_results=3, status_filter=None):
    client = get_db_client()
    embedding_function = get_embedding_function()
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_function)
    
    # Professional Hybrid Filter
    where_clause = {"status": status_filter} if status_filter else None
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where_clause
    )
    
    output = []
    for i in range(len(results['ids'][0])):
        # Surgical Extraction: Only return the 'Needle'
        is_verified = results['metadatas'][0][i].get('verified', False)
        verified_tag = "[VERIFIED] " if is_verified else ""
        
        res = f"{verified_tag}[TICKET {results['ids'][0][i]}] "
        res += f"STATUS: {results['metadatas'][0][i]['status']} | "
        if results['metadatas'][0][i]['status'] == "Resolved":
            res += f"FIX: {results['metadatas'][0][i]['proven_resolution']}"
        else:
            res += f"PREVIOUS_FAILURES: {results['metadatas'][0][i]['troubleshooting_notes']}"
        output.append(res)
    
    return "\n".join(output) if output else "No matching historical data found."

def test_query(query_text, n_results=3):
    client = get_db_client()
    embedding_function = get_embedding_function()
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_function)
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    print(f"\nTest Query: '{query_text}'")
    for i in range(len(results['ids'][0])):
        print(f"--- Result {i+1} ---")
        print(f"ID: {results['ids'][0][i]}")
        print(f"Status: {results['metadatas'][0][i]['status']}")
        print(f"Resolution: {results['metadatas'][0][i]['proven_resolution']}")
        print(f"Notes: {results['metadatas'][0][i]['troubleshooting_notes']}")
        print(f"Distance: {results['distances'][0][i]}")

if __name__ == "__main__":
    ingest_data()
    test_query("NAV update failure")
