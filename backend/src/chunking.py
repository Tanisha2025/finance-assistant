from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    """Documents ko chunks mein todta hai"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Chunking done! Total chunks: {len(chunks)}")
    return chunks

# Fix: get_finance_chunks() dead code tha — hata diya
