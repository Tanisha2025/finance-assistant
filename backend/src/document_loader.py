import pdfplumber
from langchain_core.documents import Document
from langchain_community.document_loaders.csv_loader import CSVLoader
import os

def load_pdf(file_path):
    """PDF file load karta hai pdfplumber se"""
    documents = []
    
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                documents.append(Document(
                    page_content=text,
                    metadata={"page": i + 1, "source": file_path}
                ))
    
    print(f"✅ PDF loaded! Total pages with text: {len(documents)}")
    return documents

def load_csv(file_path):
    """CSV file load karta hai"""
    loader = CSVLoader(file_path)
    documents = loader.load()
    print(f"✅ CSV loaded! Total rows: {len(documents)}")
    return documents

def load_document(file_path):
    """Auto detect karta hai PDF ya CSV hai"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".csv":
        return load_csv(file_path)
    else:
        raise ValueError(f"❌ Unsupported file: {ext}")