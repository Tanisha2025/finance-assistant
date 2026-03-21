from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    """Embeddings model load karta hai — FREE HuggingFace se"""
    
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    print("✅ Embeddings model loaded!")
    return embeddings