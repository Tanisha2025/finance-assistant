from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    """Embeddings model load karta hai — FREE HuggingFace se"""
    
    embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'}, # Agar GPU hai toh 'cuda' likh dena
    encode_kwargs={'normalize_embeddings': True} # BGE ke liye zaroori hai
)
    
    print("✅ Embeddings model loaded!")
    return embeddings