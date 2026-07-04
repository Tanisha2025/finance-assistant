import os
import time
import shutil
from src.document_loader import load_document
from src.chunking import chunk_documents
from src.embeddings import get_embeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Fix: get_llm() ek hi jagah define hai ab
def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )

# Fix: Sirf ek definition hai ab (duplicate hata diya)
# Fix: Unique timestamp-based collection name use ho raha hai
def create_doc_vectorstore(file_path, collection_name):
    docs = load_document(file_path)
    chunks = chunk_documents(docs)
    embeddings = get_embeddings()

    # ← Timestamps hatao — fixed names use karo
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=f"chroma_db_{collection_name}",
        collection_name=collection_name
    )
    return vector_store, len(docs), len(chunks)


# Fix: Sirf ek definition hai ab (duplicate hata diya)
def ask_single_doc(vector_store, question):
    prompt = PromptTemplate.from_template("""
    You are a financial analyst assistant.
    Use ONLY the context below to answer.
    If information is not available, say "Not found in document."

    IMPORTANT RULES:
    - Keep answer SHORT and CONCISE — max 5-6 lines
    - Only give KEY numbers and percentages
    - No lengthy explanations
    - Use bullet points only for key metrics

    Context: {context}
    Question: {question}

    Short Answer:
    """)

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs,
         "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke(question)


def compare_documents(file_path_1, file_path_2, name_1, name_2, question):
    # Fix: persist_dir track kar rahe hain cleanup ke liye
    vs1, pages1, chunks1, dir1 = create_doc_vectorstore(file_path_1, "doc1")
    vs2, pages2, chunks2, dir2 = create_doc_vectorstore(file_path_2, "doc2")

    answer1 = ask_single_doc(vs1, question)
    answer2 = ask_single_doc(vs2, question)

    llm = get_llm()
    comparison_prompt = f"""
    You are a senior financial analyst.
    Compare these two companies briefly.

    STRICT RULES:
    - Maximum 10 lines total
    - Be direct and concise
    - Only KEY differences and numbers
    - Give clear winner at end
    - No lengthy explanations

    {name_1} Data: {answer1}
    {name_2} Data: {answer2}
    Question: {question}

    Brief Comparison (max 10 lines):
    1. {name_1} Summary (2 lines)
    2. {name_2} Summary (2 lines)
    3. Key Differences (3 lines)
    4. Final Verdict (2 lines)
    """

    response = llm.invoke([HumanMessage(content=comparison_prompt)])

    # Fix: Temporary chroma folders delete karo after use
    try:
        vs1._client.close()
    except:
        pass
    try:
        vs2._client.close()
    except:
        pass
    shutil.rmtree(dir1, ignore_errors=True)
    shutil.rmtree(dir2, ignore_errors=True)

    return {
        "doc1_name": name_1,
        "doc2_name": name_2,
        "doc1_answer": answer1,
        "doc2_answer": answer2,
        "comparison": response.content,
        "doc1_stats": {"pages": pages1, "chunks": chunks1},
        "doc2_stats": {"pages": pages2, "chunks": chunks2},
    }
