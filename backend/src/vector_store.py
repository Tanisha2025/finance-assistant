from langchain_community.vectorstores import Chroma
from src.embeddings import get_embeddings
import os

CHROMA_PATH = "chroma_db"  # Yahan store hoga

def store_chunks(chunks):
    """Chunks ko ChromaDB mein store karta hai"""
    
    embeddings = get_embeddings()
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print(f"✅ Vector store ready! Total chunks stored: {len(chunks)}")
    return vector_store

def load_vector_store():
    """Already stored ChromaDB load karta hai"""
    
    embeddings = get_embeddings()
    
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    
    print("✅ Vector store loaded!")
    return vector_store

def search_docs(query, k=5):  # k=3 se k=5 karo
    vector_store = load_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return results