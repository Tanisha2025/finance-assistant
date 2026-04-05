import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.vector_store import load_vector_store

load_dotenv()

def get_llm():
    """Groq LLM load karta hai"""
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    return llm

def build_rag_pipeline():
    """RAG pipeline banata hai"""

    prompt_template = PromptTemplate.from_template("""
    You are a helpful financial assistant.
    Use the following context to answer the question.
    If you don't know the answer, say "I don't have 
    enough information in the document."
    
    Context: {context}
    Question: {question}
    
    Answer:
    """)

    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )
    llm = get_llm()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, 
         "question": RunnablePassthrough()}
        | prompt_template
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