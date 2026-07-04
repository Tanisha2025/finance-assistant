import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.vector_store import load_vector_store  # Fix: ab yeh function exist karta hai

load_dotenv()


def get_llm():
    """Groq LLM load karta hai"""
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=1024
    )
    return llm


def build_rag_pipeline():
    strict_prompt = """
You are a Strict Financial Auditor. Use ONLY the provided context to answer the user's question.

Rules:
1. If the answer is not in the context, say: "I'm sorry, I cannot find this specific information in the document."
2. DO NOT make up any numbers or percentages.
3. If you find a table, represent the data clearly.
4. Always mention the source/page number if available.

If the data contains multiple figures, present them in a Markdown table. Use bold text for key financial metrics like Net Profit or Revenue.

Context: {context}
Question: {question}
Answer:"""

    vector_store = load_vector_store()  # Fix: ab crash nahi karega
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    llm = get_llm()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs,
         "question": RunnablePassthrough()}
        | PromptTemplate.from_template(strict_prompt)
        | llm
        | StrOutputParser()
    )

    print("✅ RAG Pipeline ready!")
    return rag_chain


def ask_question(question):
    """Question puchho — answer pao"""
    rag_chain = build_rag_pipeline()
    answer = rag_chain.invoke(question)

    print(f"\n❓ Question: {question}")
    print(f"\n💬 Answer: {answer}")
    return answer
