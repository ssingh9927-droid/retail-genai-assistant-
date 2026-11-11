import chromadb
import uuid

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="indore_retail_policies")

# 5 representative documents covering standard, updated, and conflicting policies
documents = [
    {
        "text": "Indore Electronics Return Policy (v1.0 - 2023): Customers can return any electronics item within 30 days of purchase with full refund.",
        "dept": "Returns", "version": "1.0", "status": "deprecated", "date": "2023-01-01"
    },
    {
        "text": "Indore Electronics Return Policy (v2.0 - 2024): All smartphones and laptops have a 7-day replacement-only window. Accessories retain a 15-day return window. Opened software is non-returnable.",
        "dept": "Returns", "version": "2.0", "status": "active", "date": "2024-03-01"
    },
    {
        "text": "Indore Express Logistics Delivery SOP: Same-day delivery applies strictly within Indore municipal limits (Zone A) for orders placed before 2:00 PM. Deliveries to Rau and Pithampur take 24-48 hours.",
        "dept": "Logistics", "version": "1.2", "status": "active", "date": "2024-02-15"
    },
    {
        "text": "Payment & Refund Processing Guidelines: Refunds via UPI are credited within 2 to 4 hours of pickup verification. Credit/Debit card refunds reflect in 3-5 business days. Staff must never ask for customer OTP or CVV.",
        "dept": "Finance", "version": "2.1", "status": "active", "date": "2024-04-10"
    },
    {
        "text": "Warranty Support SOP: All major brands (Samsung, Apple, Boat) must be directed to authorized Indore service centers. Local replacement is only issued if Dead on Arrival (DOA) within 48 hours.",
        "dept": "Customer Support", "version": "1.0", "status": "active", "date": "2024-01-10"
    }
]

for doc in documents:
    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[doc["text"]],
        metadatas=[{"dept": doc["dept"], "version": doc["version"], "status": doc["status"]}]
    )

print("Ingestion complete: Documents stored in ./chroma_db")
