import streamlit as st
import os
import tempfile
from src.document_loader import load_document
from src.chunking import chunk_documents
from src.vector_store import store_chunks
from src.rag_pipeline import ask_question
from src.multi_doc import compare_documents
from src.report_generator import generate_report_content, create_pdf_report
from src.rag_pipeline import build_rag_pipeline

st.set_page_config(
    page_title="FinanceAI Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0a0a0f; color: #e0e0e0; }
    [data-testid="stSidebar"] {
        background-color: #0f0f1a;
        border-right: 1px solid #1e1e2e;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00f5d4, #00bbf9);
        color: #0a0a0f; border: none; border-radius: 8px;
        padding: 10px 24px; font-weight: 700;
        font-size: 14px; width: 100%; transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,245,212,0.3);
    }
    .stTextInput > div > div > input {
        background-color: #1a1a2e;
        border: 1px solid #2e2e4e;
        border-radius: 8px; color: #e0e0e0;
        padding: 12px; font-size: 14px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00f5d4;
        box-shadow: 0 0 0 2px rgba(0,245,212,0.2);
    }
    .chat-user {
        background: #1a1a2e;
        border: 1px solid #2e2e4e;
        border-radius: 12px 12px 2px 12px;
        padding: 12px 16px; margin: 8px 0;
        font-size: 14px; color: #00bbf9;
    }
    .chat-bot {
        background: linear-gradient(135deg, #0f1a2e, #1a0f2e);
        border: 1px solid #00f5d433;
        border-radius: 12px 12px 12px 2px;
        padding: 12px 16px; margin: 8px 0;
        font-size: 14px; color: #e0e0e0;
    }
    .stat-card {
        background: #1a1a2e; border: 1px solid #2e2e4e;
        border-radius: 10px; padding: 16px; text-align: center;
    }
    .stat-number { font-size: 28px; font-weight: 700; color: #00f5d4; }
    .stat-label { font-size: 12px; color: #666; margin-top: 4px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────
if "processed" not in st.session_state:
    st.session_state.processed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "doc_stats" not in st.session_state:
    st.session_state.doc_stats = {"pages": 0, "chunks": 0, "filename": ""}

# ── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0;'>
        <div style='font-size:40px;'>💰</div>
        <div style='font-size:20px; font-weight:700; color:#00f5d4;'>FinanceAI</div>
        <div style='font-size:12px; color:#555; margin-top:4px;'>
            Powered by LLaMA + RAG
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<p style='color:#666; font-size:12px; letter-spacing:2px;'>UPLOAD DOCUMENT</p>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.markdown(f"""
        <div style='background:#1a1a2e; border:1px solid #2e2e4e;
             border-radius:8px; padding:12px; margin:12px 0;'>
            <div style='color:#00f5d4; font-size:12px;'>📄 {uploaded_file.name}</div>
            <div style='color:#555; font-size:11px; margin-top:4px;'>
                {round(uploaded_file.size/1024, 1)} KB
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡ Process Document"):
            with st.spinner("Processing..."):
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".pdf"
                ) as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    tmp_path = tmp.name

                docs = load_document(tmp_path)
                chunks = chunk_documents(docs)

                if len(chunks) == 0:
                    st.error("❌ Could not extract text!")
                else:
                    store_chunks(chunks)
                    st.session_state.processed = True
                    st.session_state.chat_history = []
                    st.session_state.doc_stats = {
                        "pages": len(docs),
                        "chunks": len(chunks),
                        "filename": uploaded_file.name
                    }
                    os.unlink(tmp_path)
                    st.success("✅ Ready!")

    st.markdown("---")

    if st.session_state.processed:
        stats = st.session_state.doc_stats
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>{stats['pages']}</div>
                <div class='stat-label'>Pages</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-number'>{stats['chunks']}</div>
                <div class='stat-label'>Chunks</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#444; padding:8px 0;'>
        <div style='color:#555; letter-spacing:2px; 
             font-size:10px; margin-bottom:8px;'>TECH STACK</div>
        <div style='margin:4px 0;'>🧠 LLaMA 3.3 70B</div>
        <div style='margin:4px 0;'>🔗 LangChain</div>
        <div style='margin:4px 0;'>🗄️ ChromaDB</div>
        <div style='margin:4px 0;'>🤗 HuggingFace</div>
    </div>
    """, unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "💬 Single Document Q&A",
    "⚖️ Compare Documents",
    "📊 Charts & Reports"
])

# ── TAB 1 — Single Document Q&A ──────────────────────
with tab1:
    if not st.session_state.processed:
        st.markdown("""
        <div style='text-align:center; padding:60px 20px;'>
            <div style='font-size:64px; margin-bottom:16px;'>💰</div>
            <h1 style='font-size:36px; font-weight:700; color:#fff; margin:0;'>
                AI Financial Assistant
            </h1>
            <p style='color:#555; font-size:16px; margin:12px 0 40px;'>
                Upload your financial documents and get instant AI-powered insights
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        features = [
            ("📄", "Smart PDF Analysis",
             "Extract insights from annual reports & statements"),
            ("💬", "Natural Language Q&A",
             "Ask questions in plain English"),
            ("⚡", "Powered by RAG",
             "Retrieval-Augmented Generation for accuracy"),
        ]
        for col, (icon, title, desc) in zip([col1, col2, col3], features):
            with col:
                st.markdown(f"""
                <div style='background:#1a1a2e; border:1px solid #2e2e4e;
                     border-radius:12px; padding:24px;
                     text-align:center; height:160px;'>
                    <div style='font-size:32px;'>{icon}</div>
                    <div style='color:#00f5d4; font-weight:600;
                         margin:8px 0;'>{title}</div>
                    <div style='color:#555; font-size:13px;'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align:center; margin-top:40px;
             color:#444; font-size:14px;'>
            ← Upload a PDF from the sidebar to get started
        </div>
        """, unsafe_allow_html=True)

    else:
        stats = st.session_state.doc_stats
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px;
             background:#1a1a2e; border:1px solid #2e2e4e;
             border-radius:10px; padding:16px; margin-bottom:24px;'>
            <div style='font-size:24px;'>📄</div>
            <div>
                <div style='color:#fff; font-weight:600;'>
                    {stats['filename']}
                </div>
                <div style='color:#555; font-size:12px;'>
                    {stats['pages']} pages · {stats['chunks']} chunks indexed
                </div>
            </div>
            <div style='margin-left:auto; background:rgba(0,245,212,0.1);
                 border:1px solid #00f5d4; border-radius:6px;
                 padding:4px 12px; color:#00f5d4; font-size:12px;'>
                ● Ready
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.chat_history:
            st.markdown(
                "<p style='color:#444; font-size:12px; "
                "letter-spacing:2px;'>CONVERSATION</p>",
                unsafe_allow_html=True
            )
            for chat in st.session_state.chat_history:
                st.markdown(
                    f"<div class='chat-user'>❓ {chat['question']}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div class='chat-bot'>💬 {chat['answer']}</div>",
                    unsafe_allow_html=True
                )
            st.markdown("---")

        st.markdown(
            "<p style='color:#666; font-size:12px; "
            "letter-spacing:2px;'>QUICK QUESTIONS</p>",
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns(3)
        suggestions = [
            "What is the total revenue?",
            "What are the main risk factors?",
            "Summarize key highlights",
        ]
        for col, suggestion in zip([col1, col2, col3], suggestions):
            with col:
                if st.button(suggestion, key=f"suggest_{suggestion}"):
                    with st.spinner("Thinking..."):
                        answer = ask_question(suggestion)
                        st.session_state.chat_history.append({
                            "question": suggestion,
                            "answer": answer
                        })
                        st.rerun()

        st.markdown("---")
        question = st.text_input(
            "Your question",
            placeholder="e.g. What is the net profit margin?",
            label_visibility="collapsed"
        )

        if st.button("🚀 Ask Question"):
            if question:
                with st.spinner("Analyzing document..."):
                    answer = ask_question(question)
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer
                    })
                    st.rerun()
            else:
                st.warning("Please enter a question!")

        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

# ── TAB 2 — Compare Documents ─────────────────────────
with tab2:
    st.markdown("""
    <div style='padding:16px 0;'>
        <h2 style='color:#fff; margin:0;'>⚖️ Compare Two Documents</h2>
        <p style='color:#555; font-size:13px;'>
            Upload two financial PDFs and compare them side by side
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<p style='color:#00f5d4; font-size:13px;'>📄 Document 1</p>",
            unsafe_allow_html=True
        )
        doc1_name = st.text_input("Company Name 1",
                                   placeholder="e.g. Tesla",
                                   key="doc1_name")
        doc1_file = st.file_uploader("Upload PDF 1",
                                      type=["pdf"],
                                      key="doc1")

    with col2:
        st.markdown(
            "<p style='color:#00bbf9; font-size:13px;'>📄 Document 2</p>",
            unsafe_allow_html=True
        )
        doc2_name = st.text_input("Company Name 2",
                                   placeholder="e.g. Apple",
                                   key="doc2_name")
        doc2_file = st.file_uploader("Upload PDF 2",
                                      type=["pdf"],
                                      key="doc2")

    compare_question = st.text_input(
        "Comparison Question",
        placeholder="e.g. Compare the revenue and profit margins",
        key="compare_q"
    )

    if st.button("⚖️ Compare Now!", key="compare_btn"):
        if doc1_file and doc2_file and compare_question \
                and doc1_name and doc2_name:
            with st.spinner("Analyzing both documents..."):
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".pdf"
                ) as f1:
                    f1.write(doc1_file.getbuffer())
                    path1 = f1.name

                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".pdf"
                ) as f2:
                    f2.write(doc2_file.getbuffer())
                    path2 = f2.name

                result = compare_documents(
                    path1, path2,
                    doc1_name, doc2_name,
                    compare_question
                )
                os.unlink(path1)
                os.unlink(path2)

            st.markdown("---")
            st.markdown("### 📊 Comparison Results")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style='background:#1a1a2e; border:1px solid #00f5d4;
                     border-radius:12px; padding:20px;'>
                    <div style='color:#00f5d4; font-weight:600;
                         margin-bottom:12px;'>
                         📄 {result['doc1_name']}
                    </div>
                    <div style='color:#ccc; font-size:13px; line-height:1.7;'>
                        {result['doc1_answer']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div style='background:#1a1a2e; border:1px solid #00bbf9;
                     border-radius:12px; padding:20px;'>
                    <div style='color:#00bbf9; font-weight:600;
                         margin-bottom:12px;'>
                         📄 {result['doc2_name']}
                    </div>
                    <div style='color:#ccc; font-size:13px; line-height:1.7;'>
                        {result['doc2_answer']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### 🏆 Final Comparison")
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, #0f1a2e, #1a0f2e);
                 border:1px solid #9b5de5; border-radius:12px; padding:24px;'>
                <div style='color:#ccc; font-size:14px; line-height:1.8;'>
                    {result['comparison']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Please fill all fields and upload both PDFs!")

# ── TAB 3 — Auto Report Generator ────────────────────
with tab3:
    st.markdown("""
    <div style='padding:16px 0;'>
        <h2 style='color:#fff; margin:0;'>📊 Auto Report Generator</h2>
        <p style='color:#555; font-size:13px;'>
            Generate a professional PDF report from your document
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.processed:
        st.markdown("""
        <div style='text-align:center; padding:40px;
             background:#1a1a2e; border:1px solid #2e2e4e;
             border-radius:12px;'>
            <div style='font-size:40px;'>⚠️</div>
            <p style='color:#555; margin-top:12px;'>
                Please upload and process a document first!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        stats = st.session_state.doc_stats

        st.markdown(f"""
        <div style='background:#1a1a2e; border:1px solid #2e2e4e;
             border-radius:10px; padding:16px; margin-bottom:24px;'>
            <div style='color:#fff; font-weight:600;'>
                📄 {stats['filename']}
            </div>
            <div style='color:#555; font-size:12px;'>
                Ready to generate report
            </div>
        </div>
        """, unsafe_allow_html=True)

        company_name = st.text_input(
            "Company Name",
            placeholder="e.g. Tesla, Apple, Paytm",
            key="report_company"
        )

        st.markdown("""
        <div style='background:#1a1a2e; border:1px solid #2e2e4e;
             border-radius:10px; padding:16px; margin:16px 0;'>
            <p style='color:#00f5d4; font-size:13px; 
               font-weight:600; margin:0 0 8px;'>
               Report will include:
            </p>
            <div style='color:#666; font-size:12px; line-height:2;'>
                ✅ Executive Summary<br>
                ✅ Key Financial Metrics<br>
                ✅ Risk Factors Analysis<br>
                ✅ Key Highlights<br>
                ✅ Future Outlook
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📄 Generate PDF Report"):
            if company_name:
                with st.spinner(
                    "Generating report... This will take 30-60 seconds!"
                ):
                    # RAG pipeline build karo
                    rag_chain = build_rag_pipeline()
                    
                    # Content generate karo
                    content = generate_report_content(
                        rag_chain, company_name
                    )
                    
                    # PDF banao
                    report_path = create_pdf_report(
                        content,
                        company_name,
                        output_path=f"{company_name}_report.pdf"
                    )

                st.success("✅ Report generated successfully!")

                # Preview dikhao
                st.markdown("### 📋 Report Preview")

                sections = {
                    "Executive Summary": content["executive_summary"],
                    "Key Metrics": content["key_metrics"],
                    "Risk Factors": content["risk_factors"],
                    "Highlights": content["highlights"],
                    "Outlook": content["outlook"],
                }

                for title, body in sections.items():
                    with st.expander(f"📌 {title}"):
                        st.write(body)

                # Download button
                with open(report_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=f,
                        file_name=f"{company_name}_Financial_Report.pdf",
                        mime="application/pdf"
                    )
            else:
                st.warning("Please enter company name!")