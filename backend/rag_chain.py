import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from retriever import get_retriever
from config import GROQ_API_KEY, LLM_MODEL

SYSTEM_PROMPT = """You are an expert Geoscience Assistant with deep knowledge
of geology, geophysics, hydrology, environmental science, and earth observation.

Use ONLY the provided context to answer the question.
If the context does not contain enough information, say:
"I don't have enough information in my knowledge base to answer this accurately."

Always mention which document your answer is based on.

Context:
{context}

Question: {question}

Answer:"""

prompt = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question"]
)

_chain = None


def reset_chain():
    global _chain
    _chain = None


def get_qa_chain():
    global _chain
    if _chain is None:
        retriever = get_retriever()
        if retriever is None:
            return None
        print("Initializing LLM...")
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=LLM_MODEL,
            temperature=0.2
        )
        _chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        print("RAG chain ready.")
    return _chain


def query(question: str) -> dict:
    chain = get_qa_chain()
    if chain is None:
        return {
            "answer": "No documents uploaded yet. Please upload files using the sidebar first.",
            "sources": []
        }

    result = chain.invoke({"query": question})
    sources = []
    for doc in result["source_documents"]:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        excerpt = doc.page_content[:200]
        sources.append({
            "file": os.path.basename(str(source)),
            "page": page,
            "excerpt": excerpt
        })

    return {
        "answer": result["result"],
        "sources": sources
    }