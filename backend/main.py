import os
import tempfile
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Import RAG modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.document_loader import load_document
from src.chunking import chunk_documents
from src.vector_store import store_chunks
from src.rag_pipeline import ask_question, build_rag_pipeline
from src.multi_doc import compare_documents
from src.report_generator import generate_report_content, create_pdf_report

app = FastAPI(
    title="FinanceAI API",
    description="AI Financial Assistant powered by RAG",
    version="1.0.0"
)

# CORS — React ko allow karo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
doc_processed = False
doc_stats = {}

# ── REQUEST MODELS ────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str

class CompareRequest(BaseModel):
    question: str
    company1: str
    company2: str

class ReportRequest(BaseModel):
    company_name: str

# ── ROUTES ────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "message": "FinanceAI API is running!",
        "status": "ok"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """PDF upload aur process karta hai"""
    global doc_processed, doc_stats

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed!"
        )

    try:
        # Temp file save karo
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".pdf"
        ) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Process karo
        docs = load_document(tmp_path)
        chunks = chunk_documents(docs)

        if len(chunks) == 0:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF!"
            )

        store_chunks(chunks)

        # Stats save karo
        doc_processed = True
        doc_stats = {
            "filename": file.filename,
            "pages": len(docs),
            "chunks": len(chunks)
        }

        os.unlink(tmp_path)

        return {
            "success": True,
            "message": "Document processed successfully!",
            "stats": doc_stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
async def ask(request: QuestionRequest):
    """Question ka answer deta hai"""
    global doc_processed

    if not doc_processed:
        raise HTTPException(
            status_code=400,
            detail="Please upload a document first!"
        )

    try:
        answer = ask_question(request.question)
        return {
            "success": True,
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare")
async def compare(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    company1: str = "Company 1",
    company2: str = "Company 2",
    question: str = "Compare the revenue and profit margins"
):
    """Do documents compare karta hai"""
    try:
        # File 1 save karo
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".pdf"
        ) as f1:
            f1.write(await file1.read())
            path1 = f1.name

        # File 2 save karo
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".pdf"
        ) as f2:
            f2.write(await file2.read())
            path2 = f2.name

        result = compare_documents(
            path1, path2,
            company1, company2,
            question
        )

        os.unlink(path1)
        os.unlink(path2)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-report")
async def generate_report(request: ReportRequest):
    """Auto PDF report generate karta hai"""
    global doc_processed

    if not doc_processed:
        raise HTTPException(
            status_code=400,
            detail="Please upload a document first!"
        )

    try:
        rag_chain = build_rag_pipeline()
        content = generate_report_content(
            rag_chain,
            request.company_name
        )

        report_path = create_pdf_report(
            content,
            request.company_name,
            output_path=f"{request.company_name}_report.pdf"
        )

        return FileResponse(
            path=report_path,
            media_type="application/pdf",
            filename=f"{request.company_name}_Financial_Report.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def get_status():
    """Document processing status"""
    return {
        "processed": doc_processed,
        "stats": doc_stats
    }
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)