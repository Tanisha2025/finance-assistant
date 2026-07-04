import os
import shutil
from langchain_chroma import Chroma
from src.embeddings import get_embeddings

CHROMA_PATH = "./chroma_db"

def get_vector_db():
    """ChromaDB object initialize ya load karta hai"""
    embeddings = get_embeddings()
    vector_db = Chroma(
        collection_name="finance_docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )
    return vector_db

# Fix: rag_pipeline.py is calling this — it was missing before
def load_vector_store():
    """Alias for get_vector_db — used by rag_pipeline"""
    return get_vector_db()

def store_chunks(chunks):
    embeddings = get_embeddings()
    
    # Fix: Folder delete mat karo — sirf collection reset karo
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        # Purana collection delete karo agar exist karta hai
        try:
            client.delete_collection("finance_docs")
        except:
            pass  # Pehli baar hai toh collection exist nahi karega
    except:
        pass

    # Fresh collection ke saath naya vector store banao
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="finance_docs"
    )
    
    print(f"✅ Vector store ready! Total chunks stored: {len(chunks)}")
    return vector_store

def search_docs(query, k=5):
    """Similarity search perform karta hai"""
    vector_db = get_vector_db()
    results = vector_db.similarity_search(query, k=k)
    return results
