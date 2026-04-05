from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents):
    """Documents ko chunks mein todta hai"""
    
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,   # 500 se 1000 karo
    chunk_overlap=100, # overlap bhi badha do
)
    
    chunks = splitter.split_documents(documents)
    print(f"✅ Chunking done! Total chunks: {len(chunks)}")
    return chunks