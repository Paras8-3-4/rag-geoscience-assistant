import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from config import EMBEDDING_MODEL, FAISS_INDEX_PATH, TOP_K

_vectorstore = None
_embeddings = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        print("Loading embedding model...")
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        embeddings = get_embeddings()
        if os.path.exists(os.path.join(FAISS_INDEX_PATH, "index.faiss")):
            print("Loading existing FAISS index...")
            _vectorstore = FAISS.load_local(
                FAISS_INDEX_PATH,
                embeddings,
                allow_dangerous_deserialization=True
            )
            print("Vector store loaded successfully.")
        else:
            print("No existing index found. Please upload documents first.")
            _vectorstore = None
    return _vectorstore


def get_retriever():
    vs = get_vectorstore()
    if vs is None:
        return None
    return vs.as_retriever(search_kwargs={"k": TOP_K})


def add_documents(chunks: list[Document]) -> int:
    global _vectorstore
    embeddings = get_embeddings()

    if _vectorstore is None:
        print("Creating new FAISS index from uploaded documents...")
        _vectorstore = FAISS.from_documents(chunks, embeddings)
    else:
        print(f"Adding {len(chunks)} chunks to existing index...")
        _vectorstore.add_documents(chunks)

    _vectorstore.save_local(FAISS_INDEX_PATH)
    print(f"Index updated and saved. Added {len(chunks)} chunks.")
    return len(chunks)