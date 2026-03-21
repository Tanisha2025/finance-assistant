# 💰 FinanceAI — AI-Powered Financial Assistant

> An intelligent full-stack financial document assistant that lets you upload financial PDFs and get instant AI-powered insights using RAG (Retrieval-Augmented Generation).

![Tech Stack](https://img.shields.io/badge/LLM-LLaMA%203.3%2070B-00f5d4)
![Framework](https://img.shields.io/badge/Framework-LangChain-00bbf9)
![Backend](https://img.shields.io/badge/Backend-FastAPI-fee440)
![Frontend](https://img.shields.io/badge/Frontend-React-f15bb5)
![Vector DB](https://img.shields.io/badge/VectorDB-ChromaDB-9b5de5)

---

## 🎯 Problem Statement

Financial analysts spend 2-3 days manually reading 500+ page annual reports to extract key insights. FinanceAI solves this by letting users upload any financial PDF and get instant, accurate answers in seconds — powered by state-of-the-art AI.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Smart PDF Analysis | Upload any financial PDF and extract insights instantly |
| 💬 Natural Language Q&A | Ask questions in plain English — get precise answers |
| ⚖️ Multi-Document Comparison | Compare two companies side by side with AI analysis |
| 📊 Auto Report Generation | Generate professional PDF reports with one click |
| 🧠 RAG Pipeline | Retrieval-Augmented Generation for accurate responses |
| ⚡ Real-time Processing | Instant answers powered by LLaMA 3.3 70B |

---

## 🏗️ Architecture
```
User Uploads PDF
      ↓
Document Loader (pdfplumber)
      ↓
Text Chunking (LangChain)
      ↓
Embeddings (HuggingFace)
      ↓
Vector Store (ChromaDB)
      ↓
User Asks Question
      ↓
RAG Retrieval → LLaMA 3.3 70B
      ↓
Answer Generated ✅
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — REST API framework
- **LangChain** — LLM orchestration
- **LLaMA 3.3 70B** — Large Language Model (via Groq)
- **ChromaDB** — Vector database
- **HuggingFace Embeddings** — Text embeddings
- **pdfplumber** — PDF text extraction
- **fpdf2** — PDF report generation

### Frontend
- **React.js** — UI framework
- **Axios** — API communication
- **Custom CSS** — Professional dark theme UI

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API Key (free at console.groq.com)

### Backend Setup
```bash
# Clone the repo
git clone https://github.com/Tanisha2025/finance-assistant.git
cd finance-assistant/backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_groq_api_key" > .env

# Start backend
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd finance-assistant/frontend

# Install dependencies
npm install

# Start frontend
npm start
```

### Access the App
```
Frontend → http://localhost:3000
Backend  → http://127.0.0.1:8000
API Docs → http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure
```
finance-assistant/
│
├── backend/
│   ├── main.py                 ← FastAPI server
│   ├── requirements.txt
│   └── src/
│       ├── document_loader.py  ← PDF loading
│       ├── chunking.py         ← Text splitting
│       ├── embeddings.py       ← Vector embeddings
│       ├── vector_store.py     ← ChromaDB storage
│       ├── rag_pipeline.py     ← RAG chain
│       ├── multi_doc.py        ← Document comparison
│       └── report_generator.py ← PDF report generation
│
└── frontend/
    └── src/
        ├── App.js
        ├── App.css
        └── components/
            ├── Sidebar.js
            ├── ChatWindow.js
            ├── CompareDoc.js
            └── ReportGen.js
```

---

## 🌍 Real World Impact

This technology is being actively built by:
- **JPMorgan** — Internal document analysis
- **Goldman Sachs** — Research report Q&A
- **Big 4 Firms** — Audit document processing

FinanceAI is a production-ready prototype of this exact technology — built entirely with free, open-source tools.

---

## 👩‍💻 Author

**Tanisha**
- GitHub: [@Tanisha2025](https://github.com/Tanisha2025)

---

