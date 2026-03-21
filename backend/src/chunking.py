from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents):
    """Documents ko chunks mein todta hai"""
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # Har chunk 500 words ka
        chunk_overlap=50,      # 50 words overlap — context na toote
        separators=["\n\n", "\n", ".", " "]
    )
    
    chunks = splitter.split_documents(documents)
    print(f"✅ Chunking done! Total chunks: {len(chunks)}")
    return chunks