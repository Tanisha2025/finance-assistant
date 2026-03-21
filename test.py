from src.document_loader import load_document
from src.chunking import chunk_documents
from src.vector_store import store_chunks, search_docs

# Step 1 - Load
docs = load_document("docs/tsla-20231231-gen.pdf")

# Step 2 - Chunkp
chunks = chunk_documents(docs)

# Step 3 - Store
store_chunks(chunks)

# Step 4 - Search
query = "What is the revenue?"
results = search_docs(query)

print("\n--- Most Relevant Chunk ---")
print(results[0].page_content)

from src.rag_pipeline import ask_question

ask_question("What is Tesla's total revenue for year 2021?")